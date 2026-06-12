"""LLM-as-judge: an independent model scores the plan against rubrics.

The judge sees the same garden photos and location as the generator, plus the full
generated output, and returns one structured verdict per rubric. Using a different
model from the generator reduces self-preference bias.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

from pydantic import BaseModel

from harness.generate import _image_block  # reuse the image-block builder


class Verdict(BaseModel):
    rubric_id: str
    score: int  # 1 (poor) .. 5 (excellent)
    passed: bool
    reasoning: str


class JudgeReport(BaseModel):
    verdicts: List[Verdict]


def _render_rubrics(rubrics: list[dict]) -> str:
    lines = []
    for r in rubrics:
        lines.append(f"- id: {r['id']}\n  criterion: {r['title']}\n  guidance: {r['description']}")
    return "\n".join(lines)


def judge_plan(
    client,
    images: list[Path],
    location: str,
    output: str,
    rubrics: list[dict],
    *,
    model: str,
    max_tokens: int = 4000,
) -> JudgeReport:
    content: list[dict] = [_image_block(Path(p)) for p in images]
    instructions = (
        "You are a meticulous horticulture reviewer grading the output of a garden "
        "maintenance assistant. You are shown the garden photo(s), the location the "
        "assistant was given, and the assistant's full response.\n\n"
        f"Location given to the assistant: {location}\n\n"
        "Score the response against EACH rubric below. For each rubric return:\n"
        "  - score: integer 1-5 (1 = poor, 3 = acceptable, 5 = excellent)\n"
        "  - passed: true if it clearly meets the criterion, else false\n"
        "  - reasoning: one or two sentences citing concrete evidence from the photo "
        "or the response.\n"
        "Be strict and specific. Judge plausibility against what is actually visible "
        "and against the stated location's climate.\n\n"
        "Rubrics:\n"
        f"{_render_rubrics(rubrics)}\n\n"
        "=== ASSISTANT RESPONSE START ===\n"
        f"{output}\n"
        "=== ASSISTANT RESPONSE END ==="
    )
    content.append({"type": "text", "text": instructions})

    response = client.messages.parse(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": content}],
        output_format=JudgeReport,
    )
    report = response.parsed_output
    if report is None:  # parsing failed (e.g. refusal / truncation)
        raise AssertionError(
            "Judge did not return a parseable report. stop_reason="
            f"{response.stop_reason!r}; raw=\n{_first_text(response)}"
        )
    return report


def _first_text(response) -> str:
    for b in response.content:
        if getattr(b, "type", None) == "text":
            return b.text
    return json.dumps([getattr(b, "type", "?") for b in response.content])
