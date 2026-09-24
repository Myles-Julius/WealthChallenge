import sys
from pathlib import Path

try:
    import anthropic, dotenv, flask  # noqa: E401,F401
except ImportError:
    venv_python = Path(__file__).resolve().parent.parent / ".venv" / "bin" / "python"
    sys.exit(
        f"\nThe agent's libraries aren't available to this Python ({sys.executable}).\n"
        f"Run it with the project's own Python instead, for example:\n\n"
        f"    {venv_python} -m tests.run_samples\n\n"
        f"If .venv doesn't exist yet, see RUNNING.md step 2.\n"
    )
