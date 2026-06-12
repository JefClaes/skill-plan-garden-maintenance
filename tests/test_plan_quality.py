"""LLM-as-judge tests: an independent model grades the plan against rubrics."""

from __future__ import annotations

import pytest

from conftest import judge_model
from harness.judge import judge_plan
from rubrics import RUBRICS

pytestmark = pytest.mark.llm


@pytest.fixture(scope="module")
def judge_report(client, generated_output, garden_case):
    """Judge the generated plan once; one verdict per rubric."""
    return judge_plan(
        client,
        images=garden_case["images"],
        location=garden_case["location"],
        output=generated_output,
        rubrics=RUBRICS,
        model=judge_model(),
    )


@pytest.fixture(scope="module")
def verdicts_by_id(judge_report):
    return {v.rubric_id: v for v in judge_report.verdicts}


@pytest.mark.parametrize("rubric", RUBRICS, ids=[r["id"] for r in RUBRICS])
def test_rubric(rubric, verdicts_by_id):
    verdict = verdicts_by_id.get(rubric["id"])
    assert verdict is not None, f"judge returned no verdict for rubric {rubric['id']!r}"
    assert verdict.passed and verdict.score >= rubric["threshold"], (
        f"[{rubric['id']}] scored {verdict.score}/5 (passed={verdict.passed}) — "
        f"{verdict.reasoning}"
    )
