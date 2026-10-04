#!/bin/bash
# Installs Scrapling in Claude Code cloud sessions so the MCP server in .mcp.json can start.
# `uv tool install` keeps it in its own environment and puts `scrapling` in ~/.local/bin.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

if ! command -v scrapling >/dev/null 2>&1; then
  if ! command -v uv >/dev/null 2>&1; then
    pip install -q uv
  fi
  uv tool install -q --with-requirements "$CLAUDE_PROJECT_DIR/requirements.txt" scrapling
fi
