
## What the agent does

1. You give it a Portfolio Manager's meeting notes.
2. It sends the notes to Claude, together with the house rules in `prompts/`.
3. Claude returns a draft proposal as structured data (JSON).
4. The agent checks that data and loads it into the proposal tool (`Task/challenge-generator.html`).

## What's in the folder

| Folder / file | What it's for | Will you edit it? |
|---------------|---------------|-------------------|
| `prompts/financial-knowledge.md` | Investment Methodology
| `prompts/instructions.md` | Fixed rules (never invent figures, flag gaps) | Rarely |
| `Task/` | The original challenge pack: brief, schema, proposal tool, sample notes | No |
| `agent/` | The Python code | No |
| `tests/run_samples.py` | Runs the sample notes and checks the results | No |
| `config/default.json` | Which Claude model to use | Only if the model name changes |
| `.env` | Your private API key (you create this in step 3) | Once |
| `.venv/` | The project's own copy of Python and its libraries | No |

---

## One-time setup

### Step 1: Open a terminal in the project folder

In Terminal, type:

```bash
cd ~/Downloads/meridian-ai-challenge
```

You'll need to do this each time you open a new Terminal window.

### Step 2: Create the project's Python environment

**This has already been done on this Mac.** You only need it on a new computer, or if `.venv` is deleted.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### Step 3: Add your Anthropic API key

1. Create a key at **console.anthropic.com**: sign up, add billing, then go to **API Keys** and **Create Key**.
   Each test run costs a few cents.
2. Create your private settings file and open it:
   ```bash
   cp .env.example .env
   open -e .env
   ```
3. Replace `your_anthropic_api_key_here` with your key, then save and close.

Never paste the key into chat, email or code. `.env` is excluded from git, so it won't be committed.

### Step 4 (optional): Point your editor at the project's Python

This makes the editor's Run button use the right Python.

1. Press **Cmd + Shift + P**.
2. Type **Python: Select Interpreter** and pick the entry that shows `.venv`.

This is already pre-set in `.vscode/settings.json`, so you may only need to reload the editor.

---

## Everyday use

**Always use `.venv/bin/python`, not plain `python3`.** Plain `python3` is your Mac's main Python,
which doesn't have the agent's libraries.

### A. Test against the four sample notes

```bash
.venv/bin/python -m tests.run_samples
```

Example output:

```
PASS  01-notes-retiree-income.txt
  needs: Mr Whitfield, aged 63, has recently retired...

FAIL  03-notes-sparse.txt
  goalAssessment.keyFigures.totalInvestment: got "3000000", expected null
  needs: ...

1 sample(s) failed.
```

How to read it:

- **PASS / FAIL** compares the key facts exactly: client name, who it's addressed to, model portfolio,
  client type, currency, amounts, income, target return, adviser fee, replacement, and whether gaps were
  flagged with `[TO CONFIRM WITH CLIENT: ...]`.
- **`got ... expected ...`** shows what the agent produced and what the answer key says.
- **`needs:`** is the prose paragraph. Read it with a professional eye; you're the judge of its quality.
- **Watch sample 03 closely.** It checks that the agent never invents numbers. The example FAIL above,
  where "a few million" became `3000000`, is the kind of mistake to fix first.
- Each sample is hidden from the agent's worked examples while it's being tested, so it can't copy the answer.

### B. Use the web interface (for demos and your screen recording)

```bash
.venv/bin/python -m agent.server
```

1. Open **http://localhost:3000** in your browser.
2. Click a **Sample** button, or paste your own notes.
3. Click **Generate proposal**. It takes a few seconds, then shows the JSON and a validation message.
4. Click **Open in proposal tool**. The proposal renders in a new tab.
5. When finished, go back to Terminal and press **Ctrl + C** to stop the server.

### C. Run a single notes file from the command line

```bash
.venv/bin/python -m agent Task/sample-inputs/01-notes-retiree-income.txt
```

The proposal is printed and saved to `generated-proposal.json`. To load it by hand:

1. Open `Task/challenge-generator.html` in your browser.
2. Open the console with **Cmd + Option + J** in Chrome.
3. Type `window.loadProposal(` then paste the file contents and add `)`.

---

## Adding your financial logic

1. Open `prompts/financial-knowledge.md`.
2. Edit the sections in plain English, as if briefing a junior analyst. Short, specific rules work best.
   - Grey text between `<!--` and `-->` is a note for you; the AI never sees it.
   - Keep the three model IDs exactly as written: `balanced`, `global-growth`, `income`.
3. Save, then re-run the tests (step A).
4. Repeat until the results and the prose read the way you want.

Also try notes you write yourself, especially messy ones with missing amounts, contradictions or
unusual phrasing. Four samples is a small test set.

---

## Troubleshooting

| You see | What it means | Fix |
|---------|---------------|-----|
| `The agent's libraries aren't available to this Python` | You used your Mac's main Python | Run with `.venv/bin/python ...`, or select the `.venv` interpreter (step 4) |
| `No module named 'agent'` | Started from the wrong folder | Run `cd ~/Downloads/meridian-ai-challenge` first |
| `No Anthropic API key found` | `.env` is missing or still has the placeholder | Step 3 |
| `authentication_error` / `invalid x-api-key` | The key is wrong or was revoked | Create a new key and update `.env` |
| `not_found_error` mentioning the model | The model name in `config/default.json` is out of date | Update `"model"` to a current name from docs.anthropic.com |
| `credit balance is too low` | No billing on the Anthropic account | Add credit at console.anthropic.com |
| `Address already in use` (web interface) | The server is already running in another window | Stop it with Ctrl + C, or run `PORT=3001 .venv/bin/python -m agent.server` |
| "Open in proposal tool" opens a blank proposal | Your browser blocked the pop-up, or the tool loaded slowly | Allow pop-ups for localhost, or use **Copy loadProposal(...) call** and paste into the tool's console |
