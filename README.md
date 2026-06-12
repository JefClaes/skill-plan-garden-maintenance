# Garden Maintenance Planner — an Anthropic Agent Skill

Give Claude **photos of your garden + your location**, and it identifies the plants and
returns a **month-by-month maintenance plan** (mow, fertilize, cut back grasses, trim
hedges, prune the fruit tree, …). The output is written for two readers at once:

- a **human** — a readable Markdown plan, grouped by month;
- a **machine** — a schema-validated `json` block that a downstream LLM/MCP can turn
  into Google Calendar events.

It ships with a Python **LLM-as-judge** test suite: one model generates the plan, a
*different* model grades it against rubrics — a worked example of "LLM as a judge".

```
SKILL.md                      the skill (instructions + output contract)
reference/plan.schema.json    canonical JSON schema for the output
reference/task-taxonomy.md    categories / recurrence / month conventions
reference/example-output.md   a worked example
tests/                        LLM-as-judge + schema tests (pytest)
```

## Using the skill with Claude

The skill is a standard Agent Skill (a folder with a `SKILL.md`). Three ways to use it:

### 1. Claude Code

Copy this folder into your skills directory and Claude Code will load it automatically
when a request matches the skill's description:

- Personal: `~/.claude/skills/garden-maintenance-planner/`
- Project: `<your-project>/.claude/skills/garden-maintenance-planner/`

Then, in a session, attach your garden photos and ask:

> Here are photos of my garden. I'm in Geel, Belgium — give me a month-by-month
> maintenance plan.

### 2. claude.ai

A Skill is `SKILL.md` **plus** its `reference/` files — upload both, keeping `reference/`
next to `SKILL.md` so the links resolve. Run `./package-skill.sh` to get an upload-ready
artifact containing only the skill (not the test harness):

```
dist/garden-maintenance-planner/       # the folder
dist/garden-maintenance-planner.zip    # same, zipped
```

Upload that folder/zip as a Skill in your workspace, attach the photos, and ask the same
question.

### 3. API / your own app

Use `SKILL.md` (its body, plus the `reference/` files) as the **system prompt**, and
send the photos as image blocks with the location as text. `tests/harness/generate.py`
is a working reference implementation:

```python
import anthropic
from harness.generate import build_system_prompt, generate_plan

client = anthropic.Anthropic()
output = generate_plan(
    client,
    images=["my-garden.jpg"],
    location="Ghent, Belgium",
    model="claude-opus-4-8",
    system_prompt=build_system_prompt(),
)
print(output)
```

### Handing the plan to Google Calendar

The `json` block is the integration point. Feed it to a calendar tool / MCP server and
map each task to an event: `title` → summary, `instructions` → description, `month` →
`DTSTART`, and `recurrence` → a recurrence rule (e.g. `yearly` → `RRULE:FREQ=YEARLY`,
`monthly` → a `FREQ=MONTHLY` rule bounded by the growing season). See
[`reference/plan.schema.json`](reference/plan.schema.json) for the full contract.

## Running the tests

The tests make **live API calls** (generate with one model, judge with another), so
they need an API key.

Quickest path — the runner script creates the venv, installs deps, and runs pytest
(forwarding any extra args):

```bash
./run-tests.sh                       # full suite
./run-tests.sh tests/test_schema.py  # just the structural checks
```

Or do it by hand:

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows PowerShell:  .venv\Scripts\Activate.ps1
pip install -e .

copy .env.example .env          # then edit .env and set ANTHROPIC_API_KEY
pytest
```

- **No key set?** The suite skips cleanly (nothing fails).
- **Models** are configurable in `.env`: `GENERATION_MODEL` (default `claude-opus-4-8`)
  and `JUDGE_MODEL` (default `claude-sonnet-4-6`).
- `tests/test_schema.py` — deterministic structural checks against the JSON schema.
- `tests/test_plan_quality.py` — the LLM-as-judge rubric checks (see `tests/rubrics.py`).

A full run costs **one generation call + one judge call** — the plan is generated once
per session and reused.

### Testing against your own garden

Drop your photo(s) into `tests/fixtures/gardens/garden_01/` and edit `case.json` with
your real location. To add more gardens, create `garden_02/`, `garden_03/`, … each with
a photo and a `case.json` (see [AGENTS.md](AGENTS.md)).
