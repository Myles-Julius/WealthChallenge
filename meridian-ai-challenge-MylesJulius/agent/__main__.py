"""Command line: python -m agent <notes-file> [output-file]"""
import json
import sys
from pathlib import Path

from agent.core import ProposalAgent

if len(sys.argv) < 2:
    print("Usage: python -m agent <notes-file> [output-file]")
    print("Example: python -m agent Task/sample-inputs/01-notes-retiree-income.txt")
    sys.exit(1)

output_file = Path(sys.argv[2] if len(sys.argv) > 2 else "generated-proposal.json")
proposal, errors = ProposalAgent().process_notes(Path(sys.argv[1]).read_text(encoding="utf-8"))

output_file.write_text(json.dumps(proposal, indent=2, ensure_ascii=False))
print(json.dumps(proposal, indent=2, ensure_ascii=False))
print(f"\nSaved to {output_file}")
if errors:
    print("Validation warnings:", "; ".join(errors))
