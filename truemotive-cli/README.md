# truemotive-cli

A node‑based CLI wrapper that launches the **TrueMotive mahoney‑mac progress TUI**.

## What it does

- Parses `architecture/punch-list/MATRIX.md` and shows the current completion percentage for the *mahoney‑mac (dev)* instance.
- Displays a progress bar using the **Textual** TUI toolkit (fallback to curses if Textual is not installed).
- Refreshes the data every **30 seconds** (configurable).
- Can be invoked simply as `truemotive-cli` after installation.

## Installation

```bash
# 1. Clone / cd into the TrueMotive architecture repo
git clone <repo-url>   # or just use the existing folder
cd TrueMotiveArchitecture

# 2. Install the Python dependencies (Textual)
pip install textual

# 3. Install this CLI globally (optional) so you can run `truemotive-cli` from anywhere
npm install -g .
#   or run locally via `npx truemotive-cli`
```

## Usage

```bash
# Run the TUI
truemotive-cli
# or, if you installed locally:
npx truemotive-cli
```

The terminal will show a window like:

```
┌─────────────────────────────────────┐
│ TrueMotive                           │
├─────────────────────────────────────┤
│ 🟢  mahoney‑mac (dev) – 28/39 tasks │
│ ──────────────────────────────────── │
│ ██████████████████████████████████░░ │ 72%   │
│ Last updated: 2026‑11‑24 18:05:12    │
└─────────────────────────────────────┘
```

Press **`q`** (curses mode) or close the window (Textual) to exit.

## Development / TODO

- [ ] Dynamically parse MATRIX.md instead of hard‑coding counts.
- [ ] Integrate Linear API to fetch issue counts for the mahoney‑mac project.
- [ ] Make refresh interval configurable via env var or config file.
- [ ] Add custom colour theme / CSS.
- [ ] Generalise script to support other instances (turbo‑1, helpy, etc.).
- [ ] Add unit tests for the parser and percentage calculation.
- [ ] Create Docker / CI integration to output the percentage as an annotation.

## License

MIT