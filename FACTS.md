# FACTS — nutritionhub101.com

⭐ **This file is the ONLY source of truth for prices and products on this site.**
Menu images (`assets/menu-*.png`), old page copy, and search-engine snippets are **NOT**
sources of truth. On 2026-08-21 Broadway shipped a page advertising 33g-protein waffles
that the club does not make; the claim came from a menu PNG and had propagated to four
live pages before Ronnie caught it. **Repetition across files is not verification.**

## Rules
1. ⛔ **Never publish a price or product that is not ✅ CONFIRMED below.**
2. To confirm: ask Ronnie directly, then record the date here. Not the menu image. Not another page.
3. When a price changes, change it HERE first, then sweep the site for the old value.
4. ⚠️ **Never sweep a bare number globally** — `$7.80` was both the hot latte and the 20oz shake.
5. `seo_audit.py` flags any `$` figure on a live page that is not listed here.

| Item | Price | Status | Confirmed | Notes |
|---|---|---|---|---|
| Gourmet protein shake | $9.97 | ✅ CONFIRMED | 2026-08-21 Ronnie | 30 mentions live · live SKU ✔ name+price (Bougie/Keto Berry/Protein Coffee) |
| Protein shake 20oz | $7.80 | ✅ CONFIRMED | 2026-08-21 Ronnie | 15 mentions live · live SKUs ✔ 8 `smallshake` SKUs at $7.80. ⚠️ $7.80 was ALSO the old hot latte — never sweep this number globally |
| Loaded / energy tea 32oz | $9.15 | ✅ CONFIRMED | 2026-08-21 Ronnie | 23 mentions; matches Broadway's confirmed $9.15 · live SKUs ✔ 12 `tea` SKUs at $9.15 |
| Protein balls (4-pack) | $4.50 | ✅ CONFIRMED | 2026-08-21 Ronnie | matches Broadway's confirmed $4.50 · live SKU ✔ "Protein Balls (4 pack)" |
| Mini donuts (6 to a bag) | $4.00 | ✅ CONFIRMED | 2026-08-21 Ronnie | matches Broadway's confirmed $4.00 · live SKU ✔ "Mini Donuts (6 pack)" |
| Acai bowl | $14.00 | ✅ CONFIRMED | 2026-08-21 Ronnie | live SKU ✔ "Acai Bowl" |
| BCAA add-on | $3.00 | ✅ CONFIRMED | 2026-08-21 Ronnie | live SKU ✔ "BCAA's Boost" $3.00 (name is double-quoted in menu-data.js — apostrophe) |
| Creatine add-on | $2.00 | ✅ CONFIRMED | 2026-08-21 Ronnie | live SKU ✔ "Creatine Boost" |
| B12 energy add-on | $3.00 | ✅ CONFIRMED | 2026-08-21 Ronnie | live SKU ✔ "B12 Energy Drink" $3.00 (sold standalone too) |
| Delivery fee | $3.00 | ✅ CONFIRMED | 2026-08-21 Ronnie | order site · ⚠️ NOT a menu SKU — order-site fee, nothing to corroborate against |
| Typical spend, snack + drink | $10–15 | ✅ CONFIRMED | 2026-08-21 Ronnie | a claimed *range*, not a menu price (grab-and-go, healthy-food) |
| **Loaded waffle** | $12.75 | ✅ CONFIRMED | 2026-08-21 Ronnie | Flavors: Banana, Chocolate, Dulce. 6 live mentions. ⚠️ **NH makes these; Broadway does NOT** — never copy this row to Broadway. |

✅ **Every price on this site is verbally confirmed by Ronnie as of 2026-08-21.**

## Corroboration vs the live ordering system (2026-08-21)
`order.nutritionhub101.com/menu-data.js` is Clover-backed and takes real money, so it is the
strongest **non-human** source available. It does **NOT** satisfy rule 2 — it only makes
Ronnie's walkthrough a yes/no per line instead of a recall exercise.

⚠️ **Two traps found building that cross-check, both worth remembering:**
1. Matching on **price alone** falsely 'confirmed' the BCAA add-on against *B12 Energy Drink* —
   both $3.00. **A check that falsely confirms is worse than no check.** Match name AND price.
2. `name: "BCAA's Boost"` is **double-quoted** because of the apostrophe. A single-quote-only
   regex drops it silently and you conclude the product does not exist. It does.
