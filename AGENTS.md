# AGENTS.md

Guidance for coding agents working in this repository.

## What this repo is

An Anthropic **Agent Skill** (`SKILL.md` + `reference/`) that turns garden photos + a
location into a month-by-month maintenance plan, plus a Python **LLM-as-judge** test
suite that proves the skill produces a good, well-structured plan.

## Layout

- `SKILL.md` — the skill: trigger (`description` frontmatter) + instructions + the exact
  output contract. This is the primary artifact.
- `reference/plan.schema.json` — canonical JSON schema for the machine-readable output.
- `reference/task-taxonomy.md` — enums and conventions (categories, recurrence, months).
- `reference/example-output.md` — a worked example.
- `tests/harness/` — generation, JSON extraction, and the judge (reusable, no test logic).
- `tests/test_schema.py` — deterministic structural checks (no judge).
- `tests/test_plan_quality.py` — LLM-as-judge rubric checks; rubrics in `tests/rubrics.py`.
- `tests/fixtures/gardens/<name>/` — a photo (`*.jpg/png/...`) + `case.json` (location/notes).

## The golden rule: keep three things in sync

The skill output, the JSON schema, and the tests describe the **same contract**. If you
change one, change the others:

1. `SKILL.md` (the inline JSON shape + rules)
2. `reference/plan.schema.json` (and `reference/task-taxonomy.md` enums)
3. `tests/test_schema.py` assertions

Adding a task `category`, plant `type`, or `recurrence` value means updating all three.

## Conventions

- **Models** are never hard-coded in test logic: read `GENERATION_MODEL` /
  `JUDGE_MODEL` from the environment (defaults: `claude-opus-4-8` / `claude-sonnet-4-6`).
  Keep the judge model different from the generator to limit self-preference bias.
- **Default to current models.** Don't downgrade to an older/cheaper model without being
  asked.
- The generation step uses `SKILL.md` (frontmatter stripped) **plus** the `reference/`
  files as the system prompt, so the test exercises the real skill instructions. If you
  add a reference file the skill relies on, include it in `build_system_prompt()`.
- Tests that hit the API are marked `@pytest.mark.llm` and skip when `ANTHROPIC_API_KEY`
  is unset. Keep that behavior — never make the suite hard-fail without a key.
- The plan is generated once per session (`generated_output` fixture, session scope) and
  judged once per module. Don't add per-test generation/judge calls.

## Adding a garden fixture

1. `tests/fixtures/gardens/garden_02/` with one or more photos.
2. A `case.json`: `{"location": "...", "season_taken": "...", "notes": "..."}`.
3. To run every garden through the suite, parametrize the `garden_case` fixture in
   `tests/conftest.py` over the fixture directories (currently it loads `garden_01`).

## Commands

```bash
./run-tests.sh              # set up venv (first run) + install + run full suite
./run-tests.sh -m llm       # forwards args to pytest (here: only live LLM tests)

# or manually:
pip install -e .
pytest                      # full suite
pytest tests/test_schema.py # structural checks only
```
