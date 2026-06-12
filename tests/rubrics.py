"""Rubrics the judge model scores the plan against.

`threshold` is the minimum score (1-5) required to pass that rubric, on top of the
judge's own boolean `passed`.
"""

RUBRICS = [
    {
        "id": "plants_plausible",
        "title": "Plant identification is plausible for the photo",
        "description": (
            "The identified plants and features match what is actually visible in the "
            "photo (e.g. lawn, hedge, border shrubs, trees, paths) and are sensible for "
            "the stated location. Confidence levels are reasonable, not overconfident."
        ),
        "threshold": 4,
    },
    {
        "id": "tasks_actionable",
        "title": "Tasks are concrete and actionable",
        "description": (
            "Tasks read as specific, do-able instructions (what to do, to which plant) "
            "rather than vague generic advice."
        ),
        "threshold": 4,
    },
    {
        "id": "timing_climate_appropriate",
        "title": "Timing is tailored to the location's climate",
        "description": (
            "Months assigned to tasks make sense for the stated hardiness zone and frost "
            "window (e.g. no frost-tender work scheduled mid-winter; pruning at the right "
            "season for the species). The plan reflects the location, not a generic year."
        ),
        "threshold": 4,
    },
    {
        "id": "year_coverage",
        "title": "Plan covers the whole year",
        "description": (
            "Tasks are spread across multiple seasons rather than clustered in one or two "
            "months, giving a genuine year-round maintenance schedule."
        ),
        "threshold": 4,
    },
    {
        "id": "json_faithful",
        "title": "JSON faithfully mirrors the Markdown plan",
        "description": (
            "The machine-readable JSON block lists the same plants and tasks described in "
            "the human-readable Markdown — nothing important is added or dropped between "
            "the two."
        ),
        "threshold": 4,
    },
]
