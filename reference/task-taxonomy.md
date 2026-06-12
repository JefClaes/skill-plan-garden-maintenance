# Task taxonomy & conventions

Shared vocabulary for the JSON contract so the skill output and the tests/downstream
tools stay aligned. Keep this in sync with `plan.schema.json`.

## Task categories (`task.category`)

| category      | use for |
|---------------|---------|
| `pruning`     | Cutting back woody growth: hedges, shrubs, fruit trees, roses. |
| `fertilizing` | Feeding lawn, beds, or specific plants. |
| `mowing`      | Cutting the lawn. Usually `recurrence: monthly` across the growing season. |
| `planting`    | Sowing, planting out, bulb planting, gap-filling. |
| `pest`        | Pest/disease inspection and treatment. |
| `watering`    | Deep-watering guidance (esp. dry spells, new plants). |
| `mulching`    | Applying mulch/compost; soil improvement. |
| `dividing`    | Lifting and splitting perennials/grasses. |
| `cleanup`     | Leaf clearing, deadheading, bed tidying, weeding paths. |
| `protection`  | Winter protection, fleece, wrapping, moving tender plants. |

## Plant types (`plant.type`)

`lawn`, `hedge`, `shrub`, `perennial`, `ornamental_grass`, `tree`, `climber`,
`groundcover`, `bulb`, `annual`, `other`.

## Recurrence (`task.recurrence`)

- `once` — a one-off this year (e.g. plant a new shrub).
- `monthly` — repeats every month within the active season; the `month` field is the
  **start** month. The downstream calendar tool expands this (e.g. mowing April→October).
- `seasonal` — a few times per season (e.g. hedge trim in June and September → two tasks,
  or one `seasonal` task whose instructions name the months).
- `yearly` — once per year, every year (e.g. winter prune in February).

## Month (`task.month`)

Full English month name. For tasks that span months, set `month` to the primary/start
month and describe the span in `instructions`.

The readable Markdown plan lists **all twelve months, January–December, in order**,
even when a month carries no JSON task (note it as dormant). The JSON itself stays
task-driven — genuinely empty months don't need filler tasks.

## Priority (`task.priority`)

- `high` — skipping it harms plant health or timing is tight (e.g. fruit-tree winter prune).
- `medium` — normal upkeep.
- `low` — nice-to-have / cosmetic.

## IDs

- `plant.id`: `p1`, `p2`, … `task.id`: `t1`, `t2`, …
- `task.plant_id` references a `plant.id`, or is `null` for whole-garden tasks
  (e.g. "weed the paths", "spread compost on all beds").
