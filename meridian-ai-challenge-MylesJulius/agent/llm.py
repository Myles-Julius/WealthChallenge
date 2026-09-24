import json
import os
import re

import anthropic

from agent.paths import CONFIG_PATH
from agent.prompt_builder import build_system_prompt, build_user_prompt

CONFIG = json.loads(CONFIG_PATH.read_text())["anthropic"]


class ClaudeClient:
    def __init__(self, api_key=None):
        self.client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = os.environ.get("ANTHROPIC_MODEL") or CONFIG["model"]

    def generate_proposal(self, notes, schema, exclude_sample_id=None):
        message = self.client.messages.create(
            model=self.model,
            max_tokens=CONFIG["maxTokens"],
            temperature=CONFIG["temperature"],
            system=build_system_prompt(schema, exclude_sample_id),
            messages=[{"role": "user", "content": build_user_prompt(notes)}],
        )
        text = next((block.text for block in message.content if block.type == "text"), "")
        match = re.search(r"```json\s*(.*?)```", text, re.DOTALL) or re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError(f"Could not extract JSON from model response:\n{text}")
        return json.loads(match.group(1) if match.re.groups else match.group(0))
