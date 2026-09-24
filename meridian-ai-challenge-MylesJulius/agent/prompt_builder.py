import json
import re

from agent.paths import PROMPTS_DIR
from agent.samples import load_samples


def read_prompt(name):
    """Reads a prompt file, dropping the <!-- ... --> notes that are meant for humans only."""
    text = (PROMPTS_DIR / name).read_text(encoding="utf-8")
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL).strip()


def build_system_prompt(schema, exclude_sample_id=None):
    """Assembles the system prompt from the editable prompt files, the schema and worked examples.

    `exclude_sample_id` keeps a sample out of the examples when it is the one being tested.
    """
    examples = "\n\n".join(
        f"### Example {s['id']}\nNotes:\n{s['notes'].strip()}\n\n"
        f"Output:\n```json\n{json.dumps(s['expected'], indent=2, ensure_ascii=False)}\n```"
        for s in load_samples()
        if s["id"] != exclude_sample_id
    )
    return "\n\n---\n\n".join([
        read_prompt("instructions.md"),
        read_prompt("financial-knowledge.md"),
        f"# Output schema (JSON Schema)\n\n```json\n{json.dumps(schema, indent=2)}\n```",
        f"# Worked examples\n\n{examples}",
    ])


def build_user_prompt(notes):
    return f"Portfolio Manager's notes:\n\n<notes>\n{notes.strip()}\n</notes>\n\nProduce the proposal JSON."
