"""Generation step: run the skill against garden photos + a location.

We load `SKILL.md` (minus its YAML frontmatter) and append the skill's reference
files, then use the result as the system prompt. This mirrors how the skill behaves
at runtime (where Claude would read the referenced files on its own) so the test is
exercising the real instructions.
"""

from __future__ import annotations

import base64
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

_MEDIA_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".gif": "image/gif",
}


def build_system_prompt() -> str:
    """SKILL.md body + the reference files it points at, as one system prompt."""
    skill = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")
    body = _strip_frontmatter(skill)

    schema = (REPO_ROOT / "reference" / "plan.schema.json").read_text(encoding="utf-8")
    taxonomy = (REPO_ROOT / "reference" / "task-taxonomy.md").read_text(encoding="utf-8")

    return (
        body
        + "\n\n---\n# reference/plan.schema.json\n\n```json\n"
        + schema
        + "\n```\n\n---\n# reference/task-taxonomy.md\n\n"
        + taxonomy
    )


def _strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4 :].lstrip("\n")
    return text


def _image_block(path: Path) -> dict:
    media_type = _MEDIA_TYPES.get(path.suffix.lower())
    if media_type is None:
        raise ValueError(f"Unsupported image type: {path.suffix} ({path})")
    data = base64.standard_b64encode(path.read_bytes()).decode("utf-8")
    return {
        "type": "image",
        "source": {"type": "base64", "media_type": media_type, "data": data},
    }


def generate_plan(
    client,
    images: list[Path],
    location: str,
    notes: str | None = None,
    *,
    model: str,
    system_prompt: str | None = None,
    max_tokens: int = 16000,
) -> str:
    """Call the model with the skill + photos + location; return the text output."""
    if system_prompt is None:
        system_prompt = build_system_prompt()

    content: list[dict] = [_image_block(Path(p)) for p in images]
    text = f"Location: {location}\n"
    if notes:
        text += f"Notes: {notes}\n"
    text += (
        "\nIdentify the plants in these photos and produce the month-by-month "
        "maintenance plan exactly as instructed, including the canonical JSON block."
    )
    content.append({"type": "text", "text": text})

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        thinking={"type": "adaptive"},
        system=system_prompt,
        messages=[{"role": "user", "content": content}],
    )
    return "".join(b.text for b in response.content if b.type == "text")
