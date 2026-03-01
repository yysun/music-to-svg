# music-to-svg Agent Skill

This repository provides an Agent Skill that converts MusicXML into a Markdown-embedded SVG image:

`![score](data:image/svg+xml;base64,...)`

The skill contract is defined in `SKILL.md` and is intended for tool-driven agent workflows.

## Install With `npx skills`

Install from GitHub:

```bash
npx skills add yysun/music-to-svg
```

Useful options:

- Install globally: `npx skills add yysun/music-to-svg -g`
- Skip prompts: `npx skills add yysun/music-to-svg -y`

## Local Setup (After `npx skills add`)

If you want to run or test this repository locally, follow this exact sequence:

1. Install Verovio (macOS):

```bash
brew install verovio
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Skill Purpose

- Accept MusicXML input (typically a string)
- Write input to a temporary `.musicxml` file
- Run `scripts/convert.py <temp-file>`
- Return markdown image output on stdout (not raw SVG, not file paths)

## Skill Rules

The skill behavior is:

1. Save MusicXML content to a file (for example `/tmp/score.musicxml`).
2. Execute `scripts/convert.py /tmp/score.musicxml`.
3. Do not call renderer CLI tools directly.
4. Return stdout markdown output as `![score](data:image/svg+xml;base64,...)`.

## Local Usage (Manual Verification)

Quick check from terminal:

```bash
python scripts/convert.py /tmp/score.musicxml
```

Expected output format:

```text
![score](data:image/svg+xml;base64,...)
```

## Tests

Run tests:

```bash
pytest -q
```

Notes:

- Integration-style rendering tests are skipped when Verovio is unavailable.
- CLI output behavior is covered with mocked conversion internals.
