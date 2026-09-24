import json
import os
import sys

from dotenv import load_dotenv

from agent.llm import ClaudeClient
from agent.paths import ROOT, SCHEMA_PATH
from agent.validation import validate_proposal

load_dotenv(ROOT / ".env")

if not os.environ.get("ANTHROPIC_API_KEY") or os.environ["ANTHROPIC_API_KEY"] == "your_anthropic_api_key_here":
    sys.exit(f"\nNo Anthropic API key found. Add it to {ROOT / '.env'} (see RUNNING.md step 3).\n")


class ProposalAgent:
    def __init__(self):
        self.schema = json.loads(SCHEMA_PATH.read_text())
        self.llm = ClaudeClient()

    def process_notes(self, notes, exclude_sample_id=None):
        """Notes in -> (proposal dict, list of validation problems) out."""
        proposal = self.llm.generate_proposal(notes, self.schema, exclude_sample_id)
        return proposal, validate_proposal(proposal)
