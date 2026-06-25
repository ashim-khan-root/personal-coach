# Contributing

## Setup

```bash
pip install -r coach/requirements.txt
```

## Code Style

- Python 3.11+ type hints everywhere
- No comments unless necessary — code should be self-documenting
- Immutable patterns preferred
- Functions under 50 lines, files under 800 lines
- No mutation of function arguments

## Before Submitting

- Run the tool once: `py -3 coach/tools/<file>.py --help`
- Check no secrets are committed (API keys, tokens, passwords)
- Keep the root directory clean — no temp files, no logs, no generated assets

## Architecture

See `AGENTS.md` and `coach/user-manual.md` for full reference.
