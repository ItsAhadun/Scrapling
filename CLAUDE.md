# Shopping research with Scrapling

This repo is a workspace for researching products to buy. Use the `scrapling` MCP server
(configured in `.mcp.json`) to read product pages, reviews and price listings.

## About the user (always follow these)

1. **Buying in Pakistan only, no importing.** Only recommend products sold by sellers in
   Pakistan, priced in PKR. Skip anything that has to be shipped from abroad (Amazon.com,
   AliExpress, eBay international, etc.), even if a Pakistani site lists it.
2. **Online stores are fine.** Buying from Pakistani websites is the normal way to buy, e.g.
   Daraz.pk, PriceOye.pk, TeleX.pk (formerly Telemart), Mega.pk, iShopping.pk, Shophive.com, Czone.com.pk (PC
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

Go down this list and stop at the first step that returns the products. Don't skip to a browser
when a JSON API exists, because the API is faster, cheaper and more complete.

1. **Known store API, wide sweep** (many listings, many stores): `tools/catalog.py`. It uses
   Scrapling's Python `Fetcher` against Shopify, WooCommerce, Webx, Hostinger and Daraz JSON.
2. **One page or a few pages:** `make_request` (plain HTTP, the default) or `bulk_get` for
   several URLs. Pass `css_selector` so responses stay small.
3. **Page loads its products with JavaScript, or the HTML has no results:** `fetch` /
   `bulk_fetch`. This is a headless Chromium driven by Playwright, so it renders the page.
4. **Blocked, a challenge page, or an empty page even in step 3:** `stealthy_fetch` /
   `bulk_stealthy_fetch`. This is a hardened browser with anti-bot handling.
5. **Still nothing, but the page shows products:** they come from a hidden JSON request. Find it
   (API Anything's `capture <url> --outline`, or the browser's Network tab), then call it with
   `make_request` and add it to `tools/catalog.py` if the platform is shared by other stores.
6. **Captcha (reCAPTCHA, Turnstile) or login wall:** stop. Don't bypass it. Tell the user the
   site can't be read and use other stores.

For several requests to one site, `open_session` + `session_fetch` (browser) or
`open_request_session` + `session_make_request` (plain HTTP) is faster. Always `close_session`.
Pass a CSS selector to pull out only the parts you need (title, price, rating, specs).

### Site access from cloud sessions (last checked 2026-10-05)

Cloud sessions run from data-centre IPs, which some stores block. Update this list when a
site's behaviour changes.

- **Redirects:** `make_request`'s default `follow_redirects="safe"` rejects every redirect in
  cloud sessions, because traffic goes through a local proxy on 127.0.0.1 and Scrapling treats
  that as an internal IP ("Redirect to internal IP 127.0.0.1 rejected"). Pass
  `follow_redirects=True` (Python API: `Fetcher.get(url, follow_redirects=True)`).
- Work: PriceOye (`make_request` with `.productBox` gives name, price and rating), Mega.pk,
  Shophive, GSMArena, RTINGS, Reddit.
- TeleX (formerly Telemart): `telemart.pk` now redirects to `www.telex.pk`, so it needs
  `follow_redirects=True`. It's a Shopify store: `https://www.telex.pk/search/suggest.json?q=<query>&resources[type]=product`
  returns JSON.
- OLX: `https://www.olx.com.pk/<category>_c<id>/q-<words-with-hyphens>` (phone cases are
  `covers-cases_c1471`). A 404 means no results, not a block. Rate-limits (429) after a few
  quick requests, so wait about 10 s between them.
- Daraz tag pages work: `https://www.daraz.pk/tag/<words-with-hyphens>/?ajax=true` returns
  JSON (`mods.listItems` has name, price, rating, seller and `location`; `Overseas` means
  shipped from abroad). Retry on a 502. Up to 40 items per tag.
- Blocked, and can't be fixed from inside a cloud session:
  - Daraz search (`/catalog/?q=`): Daraz's server closes the connection from cloud IPs right
    after the request, even with the browser.
  - Cloudflare-protected stores (iShopping, Czone, allmytech.pk, others showing "Just a
    moment..."): Cloudflare rejects data-centre IPs, and the session's egress proxy
    re-terminates TLS, which hides Scrapling's browser fingerprint. `stealthy_fetch` with
    `solve_cloudflare=True` can't help: the Turnstile widget never loads
    (`challenges.cloudflare.com` frame fails with `ERR_TOO_MANY_RETRIES`, and
    `brunhild.challenges.cloudflare.com` is refused by the proxy), and Scrapling's solver then
    waits forever, so the MCP call times out. Don't use `solve_cloudflare` in cloud sessions.
- On a fresh cloud session the `scrapling` MCP server can fail to connect because it starts
  before the session hook finishes installing Scrapling. Run `/mcp` to reconnect, or use
  Scrapling's Python API directly (`~/.local/share/uv/tools/scrapling/bin/python`, `from
  scrapling.fetchers import Fetcher`).
- For blocked sites, say so and use the working stores instead. Running Claude Code on the
  user's own computer (home internet) usually gets through.

### Site access from my computer (checked 2026-10-06)

From the user's home connection (Windows, local MCP override, see `README.md`):

- **Daraz search** works with `make_request`, but the HTML has no products (they're rendered by
  JavaScript). Use the JSON version instead:
  `https://www.daraz.pk/catalog/?ajax=true&page=<N>&q=<query>` returns `mods.listItems` (name,
  price, originalPrice, location, sellerName, brandName, ratingScore, review, itemSoldCntShow,
  description (highlights list), itemId, itemUrl) and `mainInfo.totalResults` (40 items per page).
  `stealthy_fetch` with `css_selector="[data-qa-locator=product-item]"` also works.
  Daraz filters on its server (checked 2026-10-09), so add them to the URL instead of sweeping
  thousands of listings and filtering locally: `price=10000-30000`, `sort=priceasc|pricedesc|popularity`,
  `rating=4` (4 stars and up), `location=Local` (Pakistan-based sellers only; `Overseas` is the
  imports, region names like `Punjab` also work), `service=reseller` (Mall / official stores),
  `service=Free_Shipping`. The response's `mods.filter.filterItems` lists the category, brand and
  product-attribute filters for that query (attribute ones go in `ppath=<value>`, e.g.
  `ppath=40115:108866` = Ergonomic Chair). Queries for things Daraz doesn't sell (cars) return
  accessories only; search the item itself, not the model it fits.
  Reviews: `https://my.daraz.pk/pdp/review/getReviewList?itemId=<id>&pageSize=20&filter=0&sort=0&pageNo=<N>`
  returns `model.items` (rating, reviewContent, reviewTime) and `model.paging.totalPages`. The product
  page (`/products/-i<id>.html`) embeds `__moduleData__` JSON with the full description HTML.
- **iShopping, Czone, allmytech.pk:** plain `make_request` returns 200, no Cloudflare challenge.
  `stealthy_fetch` with `solve_cloudflare=True` also works (logs "No Cloudflare challenge
  found"), so it isn't needed here but does no harm.
- **TeleX:** `telemart.pk` redirects to `www.telex.pk` and works with the default
  `follow_redirects="safe"` (there's no 127.0.0.1 proxy locally, so `True` isn't needed).
- **OLX:** `covers-cases_c1471/q-<words>` returns 200 with results.
- **Finding smaller stores:** plain `make_request` to Bing or DuckDuckGo returns junk or a
  captcha. `stealthy_fetch` on `https://www.bing.com/search?q=<query>&cc=PK&setlang=en` works
  (read `li.b_algo`: `h2` title, `cite` domain). Pakistani phone-case stores are mostly Shopify,
  so `https://<store>/search/suggest.json?q=<query>&resources[type]=product&resources[limit]=10`
  returns JSON (title, price, availability, url); WooCommerce stores use
  `/?s=<query>&post_type=product`.
  Bing's `count=30` parameter returns an empty page, so page through results with `&first=11`
  instead. After about 4 quick searches Bing starts redirecting to `&rdr=1&rdrig=...` and returns
  an empty page or unrelated junk (checked 2026-10-08), so make every search count. Waiting a
  few hours resets it; spacing searches 90 s apart (a background script with `StealthyFetcher`)
  gets about 5 more good results before the junk returns (checked 2026-10-09). When that happens,
  `html.duckduckgo.com` returns 202 with no results and Google returns a captcha, so neither is
  a fallback. Only use domains that show up in search results: guessing one from a seller name
  (e.g. `chairs.pk` from the Daraz seller "Chairs.PK") gives a domain that doesn't resolve.
- **Temu** (`temu.com/pk-en`, prices in PKR, but ships from China, so it's an import): blocked.
  Search pages and `-s.html` listing pages have no products in the HTML, and `stealthy_fetch`
  gets redirected to a login page or a "Security verification" captcha.

### Reading store catalogues in bulk (`tools/catalog.py`)

To sweep many stores at once (hundreds or thousands of listings), use `tools/catalog.py`
instead of writing a new script. It reads Shopify stores (`/products.json`, up to 2,500 products),
WooCommerce stores (Store API `/wp-json/wc/store/v1/products?search=`), Webx stores (homecart.pk, xtra.pk),
Hostinger AI Builder stores (dexx.pk), plus Daraz search
JSON, and writes one JSON file (title, price, stock, url, description, image, and rating where
the store has one):

```
python tools/catalog.py --keyword chair --stores offisits.com.pk lunarfurniture.pk \
    --daraz "ergonomic chair" "mesh chair" --out _work/listings.json
```

`_work/` is gitignored. In cloud sessions run it with
`~/.local/share/uv/tools/scrapling/bin/python`. Filter the JSON afterwards with a short script
(store-side budget, keywords in `title`/`desc`). Use `python tools/catalog.py --selftest`
to check the diagnosis logic.

To find a hidden JSON API on a JavaScript-rendered store, use [API Anything](https://github.com/goodnight000/api-anything)
(`capture <url> --outline` lists the page's network calls and shows what each returns). It isn't installed
globally. It was cloned and built in a scratch folder, with `channel: "chrome"` changed to `"msedge"` in
`src/browser.ts` because this PC has Edge but no Chrome. Once you've found the request, call it with Scrapling
(as `webx()` and `hostinger()` do) and don't keep the Node tool in the loop. Don't use its `login` or cookie import.

For stores it can't read, it prints a diagnosis and what to use instead.
What it found for these stores (checked 2026-10-06; Webx/Hostinger rows rechecked 2026-10-09):

| Store | Why the API fails | What works |
|---|---|---|
| fokusoffice.com | Custom site, no product API | Category pages (`/shop/office-chairs`) and `/shop?search=<q>` with `make_request`. `api-anything capture` confirms the HTML is the only source (2026-10-09) |
| homecart.pk, xtra.pk | Webx Ecommerce (Nuxt): no Shopify/Woo API, search is rendered by JavaScript | **`tools/catalog.py` reads them** (`webx`): the home page embeds an anonymous ~15 min JWT, `POST https://frontapi.mywebx.pk/api/ProductListing/GetProductListingV2` with `{keyword, categoryID, startRow, results, priceRange, sortBy, ...}` and headers `authorization: Bearer <jwt>`, `origin`, `referer` returns price, list price, stock, rating. Works for any Webx store (checked 2026-10-09) |
| zahcomputers.pk | WordPress, but Cloudflare returns 403 on `/wp-json/` | `/?s=<query>` HTML (a loose search that also returns unrelated deals) and `/category/<slug>`. `api-anything capture` of `/?s=ssd` found only cart calls and no product API (2026-10-09) |
| dexx.pk | Hostinger AI Builder, products load with JavaScript | **`tools/catalog.py` reads it** (`hostinger`): the page HTML holds a `scha_...` id, and `GET https://api-ecommerce.hostinger.com/store/<scha_id>/products?offset=0&limit=100&q=<query>` (with `origin`/`referer` headers) returns title, slug, variants with prices (`amount` / 100 = PKR). Product URL is `https://dexx.pk/<slug>`. Only a chair shop with 26 products (checked 2026-10-09) |
| alfamall.com | Redirects to `/login` | Nothing: needs an account |
| wellshop.pk | Amazon reseller (imports to order) | Excluded by rule 1 |
| autobrandhouse.pk | Custom site behind a "Please wait while your request is being verified" page | `stealthy_fetch` on `/?s=<query>` with `wait=8000`, `network_idle=True`. Also tried `api-anything capture`: it hits a reCAPTCHA wall (checked 2026-10-09), so don't try to get around it |
| autoaxis.pk | Custom marketplace behind Cloudflare | `stealthy_fetch` on `/search?keyword=<query>` (category pages like `/running-boards` load but list nothing) |
| homefactree.com | HTTPS connection reset even in a real browser; HTTP returns 503 | Nothing: the site is down |

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

## Shell commands

If Bash commands ask for permission even in bypass mode, check `~/.claude/settings.json` for
`"permissions": {"blockReadsOutsideWorkingDirectories": true}` and remove it. While it's on,
Claude Code prompts for every Bash command its parser can't fully trace (pipes into
`python`, heredocs, `cd`, subshells), even in bypass mode
([docs](https://code.claude.com/docs/en/permission-modes#actions-no-mode-auto-approves)).
Answering a read prompt with "No, and block reads outside the working directories from now
on" turns it on. A running session keeps the old setting, so start a new session after
removing it.

Run commands from the repo root (paths like `_work/x.py`, `git -C <dir>`) instead of `cd`:
a standalone `cd` moves the session's working folder.

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
