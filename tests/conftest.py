"""Shared pytest fixtures.

The garden is generated once per session and reused by every test, so a full run
costs one generation call plus one judge call.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

from harness.generate import build_system_prompt, generate_plan

load_dotenv()

FIXTURES = Path(__file__).parent / "fixtures" / "gardens"
DEFAULT_GENERATION_MODEL = "claude-opus-4-8"
DEFAULT_JUDGE_MODEL = "claude-sonnet-4-6"


def generation_model() -> str:
    return os.environ.get("GENERATION_MODEL", DEFAULT_GENERATION_MODEL)


def judge_model() -> str:
    return os.environ.get("JUDGE_MODEL", DEFAULT_JUDGE_MODEL)


@pytest.fixture(scope="session")
def client():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        pytest.skip("ANTHROPIC_API_KEY not set — skipping live LLM tests")
    import anthropic

    return anthropic.Anthropic()


@pytest.fixture(scope="session")
def garden_case() -> dict:
    """Load the garden_01 fixture: its photos + location metadata."""
    case_dir = FIXTURES / "garden_01"
    meta = json.loads((case_dir / "case.json").read_text(encoding="utf-8"))
    images = sorted(
        p for p in case_dir.iterdir()
        if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    )
    if not images:
        pytest.skip(f"No garden photos found in {case_dir} — add one to run the suite")
    return {
        "images": images,
        "location": meta["location"],
        "notes": meta.get("notes"),
    }


@pytest.fixture(scope="session")
def generated_output(client, garden_case) -> str:
    """Run the skill once; share the result across all tests."""
    return generate_plan(
        client,
        images=garden_case["images"],
        location=garden_case["location"],
        notes=garden_case["notes"],
        model=generation_model(),
        system_prompt=build_system_prompt(),
    )
