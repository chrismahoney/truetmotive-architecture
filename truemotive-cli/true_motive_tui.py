#!/usr/bin/env python3
"""TrueMotive mahoney‑mac progress TUI

Displays a progress bar and summary for the mahoney‑mac instance
based on the data in architecture/punch-list/MATRIX.md.

Requirements
------------
pip install textual   (or use the script as a reference for a curses version)
"""

from textual.app import App, ComposeResult
from textual.widgets import Header, Static, ProgressBar
from textual.containers import Container
from textual.reactive import reactive
import datetime


# ----------------------------------------------------------------------
# Static data extracted from MATRIX.md (mahoney‑mac row)
# ----------------------------------------------------------------------
# The row in MATRIX.md reads:
#   | mahoney-mac | dev | 28 | 0 | 11 |
# Columns: Instance | Environment | Done | Failing | Not checked
DONE = 28
FAILING = 0
NOT_CHECKED = 11
TOTAL = DONE + FAILING + NOT_CHECKED  # 39
PERCENT = round(100 * DONE / TOTAL)  # 72

# ----------------------------------------------------------------------
# TUI application
# ----------------------------------------------------------------------
class TrueMotiveProgressApp(App):
    """Shows the mahoney‑mac progress as a TUI."""

    # The percentage is reactive so we could animate it later if desired.
    progress_value = reactive(PERCENT)

    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            yield Static(
                f"🟢  mahoney‑mac (dev) – {DONE}/{TOTAL} tasks complete",
                id="summary",
                classes="title",
            )
            yield ProgressBar(
                id="progress",
                total=TOTAL,
            )
        # Optional: show last‑updated timestamp from the matrix file
        yield Static(
            f"Last updated: 2026‑11‑24 (MATRIX.md)",
            id="meta",
            classes="meta",
        )

    def on_mount(self) -> None:
        # Give the widgets a little style – Textual makes this easy.
        self.query_one("#summary").add_class("title")
        # Set the progress bar's completed count after the widget is created
        self.query_one("#progress").completed = DONE
        self.query_one("#meta").add_class("meta")


# ----------------------------------------------------------------------
# Run the app
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = TrueMotiveProgressApp()
    app.run()