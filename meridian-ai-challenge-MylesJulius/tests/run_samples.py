"""Runs every sample in Task/sample-inputs through the agent: python -m tests.run_samples"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # lets the IDE "Run" button work too

from agent.core import ProposalAgent
from agent.samples import load_samples

# Fields where the agent must match the expected output exactly. Prose fields (needs,
# riskProfile) are printed for human review rather than compared word-for-word.
EXACT_FIELDS = [
    "clientName",
    "introGreetTo",
    "applyModel",
    "goalAssessment.clientType",
    "goalAssessment.currency",
    "goalAssessment.keyFigures.totalInvestment",
    "goalAssessment.keyFigures.incomeValue",
    "objective.targetReturn",
    "fees.advisorFee",
    "replacements.isReplacement",
]


def get(obj, dotted):
    for key in dotted.split("."):
        obj = obj.get(key) if isinstance(obj, dict) else None
    return obj


def main():
    agent = ProposalAgent()
    failures = 0
    for sample in load_samples():
        # Leave the sample under test out of the worked examples, so the agent can't just copy it.
        proposal, _ = agent.process_notes(sample["notes"], exclude_sample_id=sample["id"])
        expected = sample["expected"]

        mismatches = [
            f"  {f}: got {json.dumps(get(proposal, f))}, expected {json.dumps(get(expected, f))}"
            for f in EXACT_FIELDS
            if get(proposal, f) != get(expected, f)
        ]
        flags_gaps = "[TO CONFIRM" in (proposal.get("needs") or "")
        should_flag = "[TO CONFIRM" in (expected.get("needs") or "")
        if flags_gaps != should_flag:
            mismatches.append(f"  gap flag: got {flags_gaps}, expected {should_flag}")

        print(f"{'FAIL' if mismatches else 'PASS'}  {sample['file']}")
        if mismatches:
            print("\n".join(mismatches))
        print(f"  needs: {proposal.get('needs')}\n")
        failures += bool(mismatches)

    print(f"{failures} sample(s) failed." if failures else "All samples passed.")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
