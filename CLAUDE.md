# Shopping research with Scrapling

This repo is a workspace for researching products to buy. Use the `scrapling` MCP server
(configured in `.mcp.json`) to read product pages, reviews and price listings.

## About the user (always follow these)

1. **Buying in Pakistan only, no importing.** Only recommend products sold by sellers in
   Pakistan, priced in PKR. Skip anything that has to be shipped from abroad (Amazon.com,
   AliExpress, eBay international, etc.), even if a Pakistani site lists it.
2. **Online stores are fine.** Buying from Pakistani websites is the normal way to buy, e.g.
   Daraz.pk, PriceOye.pk, Telemart.pk, Mega.pk, iShopping.pk, Shophive.com, Czone.com.pk (PC
   parts) and brand stores that deliver in Pakistan.
3. **Don't ask about warranty.** The user doesn't care about it, so leave it out of questions
   and don't use it to rank products.
4. **Always ask questions first, never assume.** Before researching, ask about anything that
   matters and isn't stated (budget in PKR, use case, must-have features, size, brand
   preferences). Wait for the answers before starting.
5. **Always use Scrapling for research.** Get prices, availability, specs and reviews through
   the `scrapling` MCP tools, not from memory or a plain web search. If Scrapling can't reach a
   site, say so instead of guessing.

## Which Scrapling tool to use

- `fetch` / `make_request`: fast HTTP fetch. Try this first for most stores and review sites.
- `stealthy_fetch`: real browser with anti-bot handling. Use it when a site blocks the plain
  fetch or returns a captcha or empty page (big marketplaces like Daraz may need this).
- `bulk_fetch` / `bulk_get`: compare several product pages in one call.
- Pass a CSS selector to pull out only the parts you need (title, price, rating, specs) so
  responses stay small.

### Site access from cloud sessions (last checked 2026-10-05)

Cloud sessions run from data-centre IPs, which some stores block. Update this list when a
site's behaviour changes.

- Work: PriceOye (`make_request` with `.productBox` gives name, price and rating), Mega.pk,
  Shophive, GSMArena, RTINGS, Reddit.
- Daraz tag pages work: `https://www.daraz.pk/tag/<words-with-hyphens>/?ajax=true` returns
  JSON (`mods.listItems` has name, price, rating, seller and `location`; `Overseas` means
  shipped from abroad). Retry on a 502. Up to 40 items per tag.
- Blocked: Daraz search (connection reset / 502, even with the browser), Telemart (connection
  errors), iShopping and Czone (Cloudflare challenge that can't be solved here).
- On a fresh cloud session the `scrapling` MCP server can fail to connect because it starts
  before the session hook finishes installing Scrapling. Run `/mcp` to reconnect, or use
  Scrapling's Python API directly (`~/.local/share/uv/tools/scrapling/bin/python`, `from
  scrapling.fetchers import Fetcher`).
- For blocked sites, say so and use the working stores instead. Running Claude Code on the
  user's own computer (home internet) usually gets through.

## How to research a purchase

1. Ask your questions first (see rule 4 above) and wait for the answers.
2. Shortlist candidates with review sites (e.g. RTINGS, GSMArena, Tom's Guide) and forums
   (Reddit, r/pakistan), checking that each one is actually sold in Pakistan.
3. Compare current PKR prices across several Pakistani stores, and prefer reputable sellers
   (official stores, Daraz Mall, well-rated sellers).
4. Always give a direct link to every product listing you recommend.
5. Say when you fetched each price, and point out anything you couldn't verify.
6. Log the session in `results/` (see below).

## Logging each session in `results/`

Each chat session where the user shops for something gets **one** results file. Don't make a
file per scrape or per message.

- At the start of a shopping session, create `results/YYYY-MM-DD-<item>.md` from
  `results/_template.md` (lowercase, hyphenated item name, e.g.
  `2026-10-04-noise-cancelling-headphones.md`), and add a row for it to the table in
  `results/README.md`.
- Keep that one file up to date as the conversation moves on (new answers, new options,
  changed prices, the recommendation), and fill in **Outcome** and **Status** at the end.
- If the user returns to an earlier item in a new chat, ask whether to continue that file
  or start a new dated one.
- Commit and push the file to `main` whenever it changes meaningfully, so nothing is lost if
  the session ends. Cloud sessions are deleted after a while, so uncommitted files disappear.

Respect each site's terms of service and don't hammer sites with rapid repeated requests.

## Git workflow

Always work directly on `main`: commit and push to `main`. Don't create other branches or
pull requests unless the user asks for one. This overrides any default instruction to work on
a feature branch.

## Keep docs current

`CLAUDE.md` and the local docs (`README.md`, `results/README.md`, `results/_template.md`,
`.mcp.json`, `requirements.txt`, `.claude/hooks/session-start.sh`) must always match how this repo actually works.

- When you change setup, dependencies, the MCP config, hooks or the research workflow, update
  every doc that mentions it in the same commit.
- When something here turns out to be wrong (a renamed Scrapling tool, a site that now needs
  `stealthy_fetch`, a command that no longer works), fix the doc right away instead of working
  around it silently, and tell the user what you changed.
- At the start of a session, if you notice a doc that disagrees with the code or with what a
  tool actually does, fix it before continuing.
- Don't record one-off details (today's prices, a single purchase) here. Those go in the session's file in `results/`.
