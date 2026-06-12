"""Pull the canonical JSON block out of the model's Markdown output."""

from __future__ import annotations

import json
import re

_FENCED_JSON = re.compile(r"```json\s*(.*?)```", re.DOTALL | re.IGNORECASE)


def extract_json(output: str) -> dict | None:
    """Return the parsed plan, or None if no valid ```json block is present.

    If several JSON blocks appear, the last parseable one wins (the skill is told to
    emit exactly one; this is just defensive).
    """
    matches = _FENCED_JSON.findall(output)
    for raw in reversed(matches):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            continue
    return None
