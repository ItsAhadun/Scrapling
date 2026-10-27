# Replacement microswitches for LPKF ProtoMat S103

- **Date:** 2026-10-27
- **Status:** In progress (waiting on user to pick a route)

## What the user wants

Two homing/limit switches for an LPKF ProtoMat S103 PCB router:

1. Y-axis: Cherry DB-series subminiature, pin/button plunger, SPDT (C/NO/NC), spade terminals.
2. Depth limiter: Marquardt 1045 series ("1045/48"), pin plunger, SPDT.

Accepted equivalents (20 x 6.4 mm body, 2 holes 9.5 mm apart, DIN 41635 B): Cherry DB1C/DB2C/DB3C
(prefer DB3C gold), Marquardt 1045 pin plunger, Omron SS-5GL / SS-01GL / D2F (prefer gold "01"),
no lever. Honeywell V4, Saia-Burgess, C&K only if specs match. Budget not stated; international
options wanted too (explicit exception to the "no importing" rule for this task).

Deliverables: `results/microswitches_pakistan_2026-10-27.csv` and `results/summary.md`.

## Options compared

See `microswitches_pakistan_2026-10-27.csv` (182 rows) and `summary.md`. No Pakistani seller stocks genuine Cherry DB / Marquardt 1045 / Omron SS; genuine parts are import-only.

## Recommendation

Order 4 x Cherry DB3C-B1AA (TME ~PKR 17,500 landed, estimate) or DB3C-B1AA x2 + Marquardt 01045.0151-00 x2 (element14 APAC ~PKR 22,000). Use SS-01/SS-5 (not SS-5GL/GL = hinge lever). Check spade width (2.8 vs 4.8 mm) first.

## Outcome

## Couldn't verify

Element14/TME/Mouser/Newark blocked Scrapling (prices via Octopart); shipping/duty estimates; DB3 gold mapping; makerselectronics.com (Cloudflare); tronics.pk (HTTP 402); Daraz shipping fees.
