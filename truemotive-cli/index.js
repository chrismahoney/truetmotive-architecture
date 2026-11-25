#!/usr/bin/env node
"use strict";

const { execSync } = require("child_process");
const path = require("path");

// Resolve the path to the Python script relative to this module's location.
const pythonScript = path.join(
  __dirname,
  "true_motive_tui.py"
);

// Guard: ensure the script exists before trying to run it.
if (!require("fs").existsSync(pythonScript)) {
  console.error("❌  Python TUI script not found at", pythonScript);
  process.exit(1);
}

// Run the Python script using the system's `python3` (or `python` fallback).
try {
  // Use `execSync` so the CLI blocks until the TUI exits.
  execSync(`python3 "${pythonScript}"`, { stdio: "inherit" });
} catch (e) {
  // If the Python process exits with a non‑zero code we still exit the CLI cleanly.
  console.error("❌  TUI exited with an error:", e.message);
  process.exit(1);
}