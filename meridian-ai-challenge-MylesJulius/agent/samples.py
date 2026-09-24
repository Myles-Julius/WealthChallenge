import json

from agent.paths import CUSTOM_SAMPLES_DIR, SAMPLES_DIR


def load_samples():
    """Pairs each sample notes file (NN-*.txt) with its NN-expected.json.

    Reads the challenge pack's samples first, then the firm's own cases in custom-samples/.
    """
    samples = []
    for folder in (SAMPLES_DIR, CUSTOM_SAMPLES_DIR):
        if not folder.is_dir():
            continue
        for notes_file in sorted(folder.glob("*.txt")):
            sample_id = notes_file.name[:2]
            samples.append({
                "id": sample_id,
                "file": notes_file.name,
                "notes": notes_file.read_text(encoding="utf-8"),
                "expected": json.loads((folder / f"{sample_id}-expected.json").read_text(encoding="utf-8")),
            })
    return samples
