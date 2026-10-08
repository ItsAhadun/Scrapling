"""Collect product listings from Pakistani stores and Daraz into one JSON file.

Usage (from the repo root):
    python tools/catalog.py --keyword chair --stores offisits.com.pk lunarfurniture.pk \
        --daraz "ergonomic chair" "mesh chair" --out _work/listings.json
    python tools/catalog.py --selftest

Reads Shopify stores via /products.json and WooCommerce stores via the Store API
(/wp-json/wc/store/v1/products). When a store is neither, it prints a diagnosis
(platform, login wall, foreign currency, DNS/TLS failure, ...) so you know which
Scrapling tool to use on it instead. See CLAUDE.md "Reading store catalogues".
"""
import argparse
import html
import json
import re
import sys
import time

def strip(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h or ""))).strip()

def get(url, **kw):
    from scrapling.fetchers import Fetcher
    return Fetcher.get(url, timeout=30, retries=1, **kw)

def body(r):
    return r.body.decode("utf-8", "ignore") if isinstance(r.body, bytes) else str(r.body)

def shopify(store, kw):
    rows = []
    for page in range(1, 11):
        try:
            prods = json.loads(body(get(f"https://{store}/products.json", params={"limit": 250, "page": page})))["products"]
        except Exception:
            return None if page == 1 else rows
        if not prods:
            break
        for p in prods:
            if kw and not re.search(kw, p["title"] + " " + p.get("product_type", ""), re.I):
                continue
            v = p["variants"][0]
            rows.append(dict(src=store, title=p["title"], price=float(v["price"]),
                             avail=any(x.get("available") for x in p["variants"]),
                             url=f"https://{store}/products/{p['handle']}", desc=strip(p.get("body_html"))[:1500],
                             img=p["images"][0]["src"] if p["images"] else ""))
        time.sleep(1)
    return rows

def woo(store, kw):
    rows = []
    for page in range(1, 11):
        try:
            prods = json.loads(body(get(f"https://{store}/wp-json/wc/store/v1/products",
                                        params={"per_page": 100, "page": page, "search": kw or ""})))
            assert isinstance(prods, list)
        except Exception:
            return None if page == 1 else rows
        for p in prods:
            pr = p.get("prices", {})
            rows.append(dict(src=store, title=strip(p["name"]),
                             price=int(pr.get("price") or 0) / 10 ** int(pr.get("currency_minor_unit") or 0),
                             currency=pr.get("currency_code"), avail=p.get("is_in_stock"), url=p["permalink"],
                             desc=strip(p.get("short_description", "") + " " + p.get("description", ""))[:1500],
                             img=p["images"][0]["src"] if p.get("images") else "",
                             rating=p.get("average_rating"), reviews=p.get("review_count")))
        if len(prods) < 100:
            break
        time.sleep(1)
    return rows

def daraz_search(q, page, flt):
    """One Daraz search page as JSON. Retries once on 502/odd responses. Returns (items, total_results)."""
    for attempt in range(3):
        try:
            d = json.loads(body(get("https://www.daraz.pk/catalog/", params={"ajax": "true", "page": page, "q": q, **flt})))
            return d["mods"]["listItems"], int(d["mainInfo"]["totalResults"])
        except Exception:
            time.sleep(3)
    return [], 0

def daraz(queries, pages=3, min_price=None, max_price=None, sort=None, min_rating=None, mall=False, overseas=False):
    """Daraz search via its JSON endpoint. Filters run on Daraz's server, so --pages goes to real matches.
    Only Pakistan-based sellers (location=Local) unless overseas=True. sort: priceasc | pricedesc | popularity."""
    flt = {}
    if min_price is not None or max_price is not None:
        flt["price"] = f"{min_price or 0}-{max_price or 9999999}"
    if sort:
        flt["sort"] = sort
    if min_rating:
        flt["rating"] = min_rating
    if mall:
        flt["service"] = "reseller"
    if not overseas:
        flt["location"] = "Local"
    rows, seen = [], set()
    for q in queries:
        for page in range(1, pages + 1):
            items, total = daraz_search(q, page, flt)
            if not items:
                break
            for it in items:
                if it["itemId"] in seen:
                    continue
                seen.add(it["itemId"])
                u = it["itemUrl"]
                rows.append(dict(src="daraz:" + it.get("sellerName", ""), title=it["name"], price=float(it.get("price", 0)),
                                 was=float(it["originalPrice"]) if it.get("originalPrice") else None,
                                 avail=it.get("inStock", True), url=("https:" + u if u.startswith("//") else u).split("?")[0],
                                 loc=it.get("location"), rating=it.get("ratingScore"), reviews=it.get("review"),
                                 sold=it.get("itemSoldCntShow"), brand=it.get("brandName"), item_id=it["itemId"],
                                 desc=" | ".join(it.get("description") or [])[:1500], img=it.get("image", "")))
            if page * 40 >= total:
                break
            time.sleep(2)
    return rows

def daraz_reviews(item_id, pages=1, size=20):
    """Review texts for one Daraz product (item_id is the number in the listing JSON / the -i<number>.html in its URL)."""
    out = []
    for page in range(1, pages + 1):
        m = json.loads(body(get("https://my.daraz.pk/pdp/review/getReviewList",
                                params={"itemId": item_id, "pageSize": size, "filter": 0, "sort": 0, "pageNo": page})))["model"]
        out += [dict(stars=r["rating"], date=r.get("reviewTime"), text=r.get("reviewContent")) for r in m["items"]]
        if page >= m["paging"]["totalPages"]:
            break
        time.sleep(1)
    return out

def diagnose_html(final_url, server, page):
    """Explain why a 200-OK store has no Shopify/Woo API, and what to try instead."""
    notes = []
    if re.search(r"/(login|signin|account/login)", final_url or ""):
        notes.append("redirects to a login page: needs an account, skip it")
    if re.search(r"Just a moment|cf-chl|challenges\.cloudflare\.com", page):
        notes.append("Cloudflare challenge: try stealthy_fetch (works from home, not from cloud sessions)")
    gen = re.search(r'<meta name="generator" content="([^"]+)"', page)
    if gen:
        notes.append(f"generator: {gen.group(1)}")
    for key, msg in [("__NUXT", "Nuxt app: category/search pages are server-rendered, read them with make_request"),
                     ("__NEXT_DATA__", "Next.js app: read category pages with make_request"),
                     ("self.__next_f", "Next.js app router: read category pages with make_request"),
                     ("wp-content", "WordPress: Store API may be blocked (403); try /?s=<query>&post_type=product"),
                     ("Hostinger", "Hostinger builder: products render with JS, use stealthy_fetch on /shop")]:
        if key in page:
            notes.append(msg)
    # Bare "$" is skipped: it matches JavaScript on almost every page.
    cur = set(re.findall(r"(£|US\$|€|AED)\s?[0-9]", page))
    if cur and not re.search(r"(Rs\.?|PKR|₨)\s?[0-9]", page):
        notes.append(f"prices in {''.join(sorted(cur))}, not PKR: probably an import shop, excluded by rule 1")
    if re.search(r"amazon (products|items) in pakistan|from amazon|amazon (usa|uk)\b", page, re.I):
        notes.append("Amazon reseller: imports to order, excluded by rule 1")
    if not notes:
        notes.append("unknown platform: find its search form or category links and read the HTML")
    if server:
        notes.append(f"server: {server}")
    return notes

def diagnose(store):
    try:
        r = get(f"https://{store}/")
    except Exception as e:
        name = type(e).__name__
        if "DNS" in name or "resolve host" in str(e):
            return ["domain doesn't resolve: wrong or dead domain (don't guess store domains, take them from search results)"]
        if "SSL" in name or "reset" in str(e).lower():
            return ["HTTPS connection reset: site is likely down (check http:// and stealthy_fetch; a 503 there confirms it)"]
        return [f"{name}: {str(e)[:120]}"]
    return [f"status {r.status}"] + diagnose_html(str(r.url), r.headers.get("server"), body(r))

def selftest():
    assert any("login" in n for n in diagnose_html("https://x.com/login", None, ""))
    assert any("import" in n for n in diagnose_html("https://x.com/", None, "<b>£ 12.99</b>"))
    assert not any("import" in n for n in diagnose_html("https://x.com/", None, "Rs 1,200 and $5"))
    assert not any("import" in n for n in diagnose_html("https://x.com/", None, "s.replace('$1', x) $0"))
    assert any("Amazon reseller" in n for n in diagnose_html("https://x.com/", None, "Amazon Products in Pakistan"))
    assert any("unknown platform" in n for n in diagnose_html("https://x.com/", "cloudflare", "<html></html>"))
    assert any("Nuxt" in n for n in diagnose_html("https://x.com/", None, "window.__NUXT__={}"))
    assert any("Hostinger" in n for n in diagnose_html("https://x.com/", None, '<meta name="generator" content="Hostinger AI Builder">'))
    assert strip("<p>A &amp; B</p>") == "A & B"
    print("selftest ok")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stores", nargs="*", default=[], help="store domains, e.g. offisits.com.pk")
    ap.add_argument("--keyword", default="", help="regex for Shopify titles / search term for WooCommerce")
    ap.add_argument("--daraz", nargs="*", default=[], help="Daraz search queries")
    ap.add_argument("--pages", type=int, default=3, help="Daraz pages per query (40 items each)")
    ap.add_argument("--min-price", type=int, help="Daraz: minimum price in PKR")
    ap.add_argument("--max-price", type=int, help="Daraz: maximum price in PKR")
    ap.add_argument("--sort", choices=["popularity", "priceasc", "pricedesc"], help="Daraz sort order")
    ap.add_argument("--min-rating", type=int, choices=[1, 2, 3, 4], help="Daraz: minimum star rating")
    ap.add_argument("--mall", action="store_true", help="Daraz: Mall (official brand stores) only")
    ap.add_argument("--overseas", action="store_true", help="Daraz: also include sellers shipping from abroad (default: Pakistan only)")
    ap.add_argument("--daraz-reviews", metavar="ITEM_ID", help="print reviews for one Daraz item id and exit")
    ap.add_argument("--out", default="_work/listings.json")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.daraz_reviews:
        for r in daraz_reviews(a.daraz_reviews, a.pages):
            print(r["stars"], r["date"], r["text"], sep=" | ")
        return
    rows = []
    for s in a.stores:
        got, kind = shopify(s, a.keyword), "shopify"
        if got is None:
            got, kind = woo(s, a.keyword), "woocommerce"
        if got is None:
            print(f"{s}: not readable via API -> " + "; ".join(diagnose(s)), flush=True)
            continue
        print(f"{s}: {kind}, {len(got)} listings", flush=True)
        rows += got
    if a.daraz:
        got = daraz(a.daraz, a.pages, a.min_price, a.max_price, a.sort, a.min_rating, a.mall, a.overseas)
        print(f"daraz: {len(got)} unique listings ({sum(r.get('loc') == 'Overseas' for r in got)} Overseas)", flush=True)
        rows += got
    import os
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    json.dump(rows, open(a.out, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"wrote {len(rows)} listings to {a.out}")

if __name__ == "__main__":
    sys.exit(main())
