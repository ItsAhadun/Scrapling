# Microswitches for LPKF ProtoMat S103 (fetched 2026-10-27)

Full list: [microswitches_pakistan_2026-10-27.csv](microswitches_pakistan_2026-10-27.csv) (182 rows).
Session log: [2026-10-27-lpkf-microswitches.md](2026-10-27-lpkf-microswitches.md).

## Bottom line

**No Pakistani seller has a priced, in-stock genuine Cherry DB, Marquardt 1045 or Omron SS switch.**
Daraz, OLX and ~25 electronics/industrial stores only have generic lever clones, standard-size
V-15/KW switches (~28 x 16 mm, wrong footprint), or quote-only listings. The genuine parts have to be imported.

Two things to check before ordering:

- **Omron SS-5GL and SS-01GL are hinge-lever switches**, not pin plunger. The pin-plunger codes are
  **SS-5 / SS-01**, plus `T` for quick-connect (SS-5T, SS-01T). Datasheet: omronfs.omron.com/en_US/ecb/products/pdf/en-ss.pdf
- **Quick-connect tabs on DB3C-B1AA, Marquardt 1045.1xxx and SS-xxT are 2.8 x 0.5 mm**, not 4.8 mm.
  Measure the spade on your original before buying. If it is 4.8, none of these fit directly (use solder tags `-A1`/`.0xxx`, or 2.8 -> 4.8 adapters).
- "1045/48" is the series mark: the datasheet covers types 1045 (IP67), 1046 and 1048 (wired). You want `1045.xxxx`.
- DB3 = gold contacts is **likely but unverified** (RS's page says silver-nickel). Gold matters little for a homing signal; a silver DB1C also works.

## Top 3 for the Y-axis switch (Cherry DB3C-B1AA: button, SPDT, 2.8 mm QC)

1. **DB3C-B1AA, TME**: about USD 2.36 each, ~PKR 17,500 landed for 4 pcs (estimate). TME blocks scrapers, so price is from Octopart: https://octopart.com/search?q=DB3C-B1AA (find the TME row, 962 in stock).
2. **DB3C-B1AA, RS Export**: GBP 2.70 each, 342 in stock (read directly), ~PKR 19,600 landed for 2 pcs / ~22,600 for 4 (shipping and duty are estimates): https://export.rsdelivers.com/productlist/search?query=DB3C-B1AA
3. **DB3C-B1AA, element14 APAC**: PKR 681 each, 2,840 in stock, ~PKR 19,700 landed for 4. Does element14 ship to Pakistan? Unverified: https://octopart.com/search?q=DB3C-B1AA

Silver fallback: DB1C-B1AA (TME 496 in stock, https://octopart.com/search?q=DB1C-B1AA). Omron alternative: SS-01T (gold, QC), TME ~PKR 17,800 for 4.

## Top 2 for the depth limiter (Marquardt 1045, pin plunger, SPDT)

1. **1045.0151 (gold, solder) as `01045.0151-00`, element14 APAC**: PKR 1,448 each, only 28 in stock: https://octopart.com/search?q=01045.0151-00
2. **1045.1151 (gold, QC 2.8) or 1045.0151, Mouser**: PKR 2,345 / 2,389 each, 44 / 65 in stock, ~PKR 31,600 landed for 4. https://octopart.com/search?q=1045.1151

Marquardt 1045 is marked discontinued at RS, and Bürklin (cheapest at PKR 1,238 each) doesn't ship to Pakistan.
If the Marquardt is too dear, a Cherry DB3C-B1AA in that position is within your accepted equivalents.

## Cheapest genuine vs fastest local

- **Cheapest genuine:** 4 x DB3C-B1AA from TME, ~PKR 17,500 all-in (covers both positions, 2 spares). Freight is most of the cost, so buy all four in one order; two switches alone cost almost as much.
- **Fastest local:** nothing is in stock locally. Local routes are quote-only and unverified:
  - **HAT Industries** (Omron SS-5GL/SS-01 as sourcing listings, 4-5 weeks, not an authorized distributor): info@hatindustries-pk.com, https://hatindustries-pk.com/product/ss-01/
  - **Noorstar** (Omron reseller, Dera Ismail Khan, 0333 9972495): https://noorstar.pk/product/omron-basic-switches/
  - **Industry Parts** (Lahore, 0323 0453838, Omron/CNTD limit switches, none subminiature): https://industryparts.pk/collections/limit-switch
  - Ask for **SS-01 or SS-5** (pin plunger), not the "GL" codes. Hall Road (Lahore/Karachi) shops weren't checked online: a phone call is worth it.

## International landed cost (4 switches, one order)

FX USD/PKR 276.81. Duty assumption +47% plus PKR 1,500 clearance, which is an **estimate**, as is freight for everything except DigiKey.

| Basket | Landed PKR |
|---|---|
| 4 x DB3C-B1AA, TME | ~17,500 |
| 2 x DB3C-B1AA + 2 x 01045.0151-00, element14 APAC (if it ships to PK) | ~22,000 |
| 2 x SS-01T + 2 x 1045.0151, Mouser | ~28,100 |
| 2 x DB1C-B1AA + 2 x SS-01, DigiKey (flat USD 75 freight) | ~36,800 |

Traps: DigiKey's DB3C-A1AA is bulk-only (MOQ 2,400). Mouser, element14, Newark and TME blocked Scrapling (403/Cloudflare), so their prices come from Octopart and weren't checked on the stores' own pages. Pakistani courier clearance may ask for CNIC/NTN details.

## Budget generic fallback (clearly generic, not original quality)

- **AliExpress "Cherry DB3 gold contact" DB3C-A1AA**, PKR 589 + 888 shipping, ~PKR 5,300 for 4. Solder terminals, originals doubtful: https://www.aliexpress.com/item/1005008450882767.html
- **Local Daraz KW12 subminiature SPDT, 2 pcs Rs 230** (Megatronics.pk). It's a hinge-lever generic: you'd remove the lever, and its footprint and plunger height are unverified: https://www.daraz.pk/products/2pcs-kw12-3-spdt-5a-125vac-i1964816346.html
- Local **ZZ Marts SW-116 mini push-button**, Rs 250 per 5: footprint unverified, ask for dimensions first: https://zzmarts.com/products/sw-116-mini-micro-switch-push-button
- Daraz "DB2-510P D5" (Rs 299 per 5) is a Cherry DB2 look-alike but roller-lever only.

## Not verified

- Shipping to Pakistan from element14, TME and Mouser; all duty and clearance figures.
- DB3C gold-contact mapping; whether your originals use 2.8 or 4.8 mm tabs.
- Daraz shipping fees (shown only with an address); makerselectronics.com has an SS-5GL listing but sits behind Cloudflare, so I didn't read it.

**Scanned:** about 1,950 unique listings (Daraz 687, OLX 115, Pakistani stores 499, international ~650). 182 are in the CSV, and the ~20 genuine ones that match your spec are all international.
