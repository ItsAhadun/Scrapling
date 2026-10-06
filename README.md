# Scrapling

A workspace for using [Scrapling](https://github.com/D4Vinci/Scrapling) with Claude Code to
research things to buy in Pakistan. Claude reads product pages, reviews and prices through Scrapling's
MCP server.

## Setup (your own computer)

macOS/Linux:

```bash
git clone https://github.com/ItsAhadun/Scrapling.git
cd Scrapling
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
scrapling install        # downloads the browsers used by stealthy_fetch
```

Windows (PowerShell):

```powershell
git clone https://github.com/ItsAhadun/Scrapling.git
cd Scrapling
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
scrapling install
```

If `pip install` fails with a connection error (e.g. `ConnectionResetError 10054`), retry with
`pip install -r requirements.txt --retries 10 --timeout 60`.

Then point Claude Code at the venv's `scrapling` with a local MCP override (run inside the repo
folder; it only applies to this folder on your machine and doesn't change `.mcp.json`):

```bash
# macOS/Linux
claude mcp add --scope local scrapling -- "$PWD/.venv/bin/scrapling" mcp
```

```powershell
# Windows
claude mcp add --scope local scrapling -- "$PWD\.venv\Scripts\scrapling.exe" mcp
```

Check it with `claude mcp get scrapling` (should say Connected), then start `claude` in this
folder. Because the override uses the full path, the venv doesn't need to be active. Start
`claude` from the repo folder itself, not a parent folder, or the local override won't load.

## Cloud sessions (claude.ai/code)

`.claude/hooks/session-start.sh` installs Scrapling and its browsers automatically. Set the
environment's **Network access** to **Full** so it can reach shopping sites
([docs](https://code.claude.com/docs/en/cloud-environments#network-access)). Some stores
(Daraz search, iShopping, Czone and other Cloudflare-protected sites) block cloud IPs; see `CLAUDE.md` for the current list.
They usually work when you run Claude Code on your own computer.

## Usage

Just ask, for example:

> Find me the best noise-cancelling headphones under Rs 30,000 and compare prices on Daraz,
> PriceOye and TeleX.

For wide sweeps, `tools/catalog.py` collects listings from many Shopify/WooCommerce stores and
Daraz into one JSON file and explains why any other store can't be read (see `CLAUDE.md`).

Each shopping chat gets one summary file in `results/` (what you wanted, options compared
with prices and links, the recommendation and what you decided). See `results/README.md` for
the list of past sessions and `CLAUDE.md` for the workflow and buying preferences Claude
follows.
