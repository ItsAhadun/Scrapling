# Scrapling

A workspace for using [Scrapling](https://github.com/D4Vinci/Scrapling) with Claude Code to
research things to buy in Pakistan. Claude reads product pages, reviews and prices through Scrapling's
MCP server.

## Setup (your own computer)

```bash
git clone https://github.com/ItsAhadun/Scrapling.git
cd Scrapling
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
scrapling install        # downloads the browsers used by stealthy_fetch
claude                   # start Claude Code in this folder
```

Claude Code picks up the `scrapling` MCP server from `.mcp.json`. Run `/mcp` inside Claude
Code to check that it's connected. Keep the virtualenv activated when you start `claude` so
the `scrapling` command is on your PATH.

## Cloud sessions (claude.ai/code)

`.claude/hooks/session-start.sh` installs Scrapling automatically. Cloud environments only
reach the hosts their network policy allows, so set the environment's **Network access** to
a broader level, or add the shopping sites you use under Allowed domains
([docs](https://code.claude.com/docs/en/cloud-environments#network-access)).

## Usage

Just ask, for example:

> Find me the best noise-cancelling headphones under Rs 30,000 and compare prices on Daraz,
> PriceOye and Telemart.

Each shopping chat gets one summary file in `results/` (what you wanted, options compared
with prices and links, the recommendation and what you decided). See `results/README.md` for
the list of past sessions and `CLAUDE.md` for the workflow and buying preferences Claude
follows.
