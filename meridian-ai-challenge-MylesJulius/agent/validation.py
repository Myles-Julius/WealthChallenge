import re

MODEL_IDS = ["balanced", "global-growth", "income"]


def validate_proposal(proposal):
    """Returns a list of problems with the proposal; an empty list means it passed."""
    errors = []
    figures = (proposal.get("goalAssessment") or {}).get("keyFigures") or {}
    advisor_fee = (proposal.get("fees") or {}).get("advisorFee")

    if not proposal.get("clientName"):
        errors.append("clientName is missing")
    if proposal.get("applyModel") and proposal["applyModel"] not in MODEL_IDS:
        errors.append(f"applyModel must be one of: {', '.join(MODEL_IDS)}")
    for field in ("totalInvestment", "incomeValue"):
        if figures.get(field) and not re.fullmatch(r"\d+", str(figures[field])):
            errors.append(f"{field} must be digits only")
    if advisor_fee and not re.fullmatch(r"\d*\.?\d+", str(advisor_fee)):
        errors.append('advisorFee must be a plain percentage, e.g. "0.75"')
    return errors
