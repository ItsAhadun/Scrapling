#!/bin/bash
# Installs Scrapling in Claude Code cloud sessions so the MCP server in .mcp.json can start.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

if ! command -v scrapling >/dev/null 2>&1; then
  pip install -q -r "$CLAUDE_PROJECT_DIR/requirements.txt"
fi
