from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASK_DIR = ROOT / "Task"
SCHEMA_PATH = TASK_DIR / "schema.json"
TOOL_PATH = TASK_DIR / "challenge-generator.html"
SAMPLES_DIR = TASK_DIR / "sample-inputs"
CUSTOM_SAMPLES_DIR = ROOT / "custom-samples"
PROMPTS_DIR = ROOT / "prompts"
CONFIG_PATH = ROOT / "config" / "default.json"
