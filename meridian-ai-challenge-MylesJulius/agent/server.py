"""Web interface: python -m agent.server, then open http://localhost:3000"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # lets the IDE "Run" button work too

from flask import Flask, jsonify, request, send_file

from agent.core import ProposalAgent
from agent.paths import TOOL_PATH
from agent.samples import load_samples

app = Flask(__name__)
agent = ProposalAgent()
INDEX_PATH = Path(__file__).parent / "static" / "index.html"


@app.get("/")
def index():
    return send_file(INDEX_PATH)


@app.get("/tool")
def tool():
    return send_file(TOOL_PATH)


@app.get("/api/samples")
def samples():
    return jsonify([{"id": s["id"], "file": s["file"], "notes": s["notes"]} for s in load_samples()])


@app.post("/api/proposal")
def proposal():
    notes = (request.get_json(silent=True) or {}).get("notes")
    if not notes:
        return jsonify(error="Notes are required"), 400
    try:
        result, errors = agent.process_notes(notes)
    except Exception as error:
        app.logger.exception("Error generating proposal")
        return jsonify(error="Failed to generate proposal", details=str(error)), 500
    return jsonify(proposal=result, validation={"valid": not errors, "errors": errors})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    print(f"Meridian AI Agent running at http://localhost:{port}")
    app.run(port=port)
