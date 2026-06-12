"""Deterministic structural checks on the generated plan.

These exercise the live output but don't call the judge — they enforce the machine
contract that the downstream calendar tool depends on.
"""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

from harness.extract import extract_json

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO_ROOT / "reference" / "plan.schema.json").read_text(encoding="utf-8"))

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

pytestmark = pytest.mark.llm


def _markdown_part(output: str) -> str:
    """The human-readable plan: everything before the canonical ```json block.

    Splitting off the JSON keeps month names inside the JSON from masking a month
    that's missing from the readable plan.
    """
    head, _, _ = output.partition("```json")
    return head


@pytest.fixture(scope="module")
def plan(generated_output) -> dict:
    parsed = extract_json(generated_output)
    assert parsed is not None, "Output did not contain a parseable ```json block"
    return parsed


def test_output_contains_json_block(generated_output):
    assert extract_json(generated_output) is not None


def test_matches_schema(plan):
    jsonschema.validate(instance=plan, schema=SCHEMA)


def test_plants_and_tasks_present(plan):
    assert plan["plants"], "no plants identified"
    assert plan["tasks"], "no tasks produced"


def test_task_plant_refs_resolve(plan):
    plant_ids = {p["id"] for p in plan["plants"]}
    for task in plan["tasks"]:
        if task["plant_id"] is not None:
            assert task["plant_id"] in plant_ids, (
                f"task {task['id']} references unknown plant_id {task['plant_id']!r}"
            )


def test_year_is_covered(plan):
    months = {task["month"] for task in plan["tasks"]}
    assert len(months) >= 6, f"plan only spans {sorted(months)} — expected a fuller year"


def test_markdown_lists_every_month(generated_output):
    """The readable plan must walk through all twelve months, Jan–Dec, even quiet ones."""
    markdown = _markdown_part(generated_output)
    missing = [m for m in MONTHS if m not in markdown]
    assert not missing, (
        f"month-by-month plan is missing {missing} — the readable plan must list "
        f"every month January through December, including dormant ones"
    )
