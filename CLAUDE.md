# Shopping research with Scrapling

This repo is a workspace for researching products to buy. Use the `scrapling` MCP server
(configured in `.mcp.json`) to read product pages, reviews and price listings.

## Which Scrapling tool to use

- `fetch` / `make_request`: fast HTTP fetch. Try this first for most stores and review sites.
- `stealthy_fetch`: real browser with anti-bot handling. Use it when a site blocks the plain
  fetch or returns a captcha or empty page (Amazon, Best Buy and Walmart often need this).
- `bulk_fetch` / `bulk_get`: compare several product pages in one call.
- Pass a CSS selector to pull out only the parts you need (title, price, rating, specs) so
  responses stay small.

## How to research a purchase

1. Ask what the user needs: budget, must-have features, where they live (for store
   availability and shipping), and brands they like or want to avoid.
2. Shortlist candidates from review sites (e.g. RTINGS, Wirecutter, Tom's Guide) and forums
   (Reddit), then check current prices on several retailers.
3. Always give a direct link to every product listing you recommend.
4. Say when you fetched each price, and point out anything you couldn't verify.
5. Save longer comparisons as Markdown in `research/` when the user wants to keep them.

Respect each site's terms of service and don't hammer sites with rapid repeated requests.

## Keep docs current

`CLAUDE.md` and the local docs (`README.md`, `.mcp.json`, `requirements.txt`,
`.claude/hooks/session-start.sh`) must always match how this repo actually works.

- When you change setup, dependencies, the MCP config, hooks or the research workflow, update
  every doc that mentions it in the same commit.
- When something here turns out to be wrong (a renamed Scrapling tool, a site that now needs
  `stealthy_fetch`, a command that no longer works), fix the doc right away instead of working
  around it silently, and tell the user what you changed.
- At the start of a session, if you notice a doc that disagrees with the code or with what a
  tool actually does, fix it before continuing.
- Don't record one-off details (today's prices, a single purchase) here. Those go in `research/`.
