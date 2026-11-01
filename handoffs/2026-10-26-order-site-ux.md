# Order site UX pass — 2026-10-26 (order.nutritionhub101.com)

Live code = VPS `/opt/nutritionhub-menu/` (source of truth). `menu/` is gitignored here (it holds orders.json), so a local copy of today's index.html + analytics-consent.js + 3 new images sits in `menu/` UNTRACKED; the VPS is the only real backup plus the .bak files below.

## Done (all live, each with a VPS backup)
1. Photos: 4:5 cover crop, shimmer placeholder. Slim mobile cookie bar (`analytics-consent.js`).
2. Drink photos resized to <=800px (12.9MB -> ~3.4MB for referenced files). Originals: `images.bak-pre-shrink-20261026-161916`.
3. Sticky one-row category bar, search box, "Customer favorites" / Popular (top 6 from orders.json: bougie-shake, wonder-woman, strawberry-cheesecake, banana-pudding, blueberry-cheesecake, strawberry-sunrise — hard-coded `POPULAR_IDS`, refresh occasionally). Header no longer sticky.
4. Cards: neutral tags shown only in All/Popular/search; boosts render as compact rows; stepper fits on phones; shorter header.
5. Open/closed line (Mon-Thu 6:30-5, Fri 6:30-3, Sat 8-2, Sun 12-3 — confirmed by Ronnie 10/26), favicon.svg, apple-touch-icon, og-order.png.

## Not done / open
- Tax: checkout adds no tax (server charges cart total). Needs Ronnie's decision before any tax line.
- "Order your usual" already exists; nothing to build.
- Not tested on a real iPhone/Safari or via a paid checkout.
- Possible next: hide/disable ordering when closed; Popular list auto-refresh; Broadway site (order.broadwaynutrition.com) could reuse these changes.

VPS backups in /opt/nutritionhub-menu/: index.html.bak-pre-{photocrop-20261026-161731, stickybar-20261026-162214, cardcleanup-20261026-162557, polish-20261026-162955}, analytics-consent.js.bak-pre-banner-20261026-161731.

## Addendum (evening 10/26): Broadway port, tax line, card fee, Broadway UX pass

**Where the code lives:** VPS only (`menu/` is gitignored). NH = `/opt/nutritionhub-menu/` (service `nutritionhub-menu`, :8087). Broadway = `/opt/broadway-order/` (service `broadway-order`, :8099). Static files need no restart; `server.js` / `order-safeguards.js` do.

**Shipped (all verified live):**
- Broadway got the NH UX pass: sticky category bar, search, 4:5 photo cards, stepper, favicon/share image, pink `#c2185b` accent.
- Card fee: first 3.011%, **changed to 3% (`CARD_FEE_RATE_NUM=3, DEN=100`) on BOTH sites**, same integer math client and server (`Math.round(subtotalCents*3/100)`). Applies to item subtotal only; included in Meta CAPI value and SMS note ("incl. $X card fee"). $9.97 drink -> $10.27.
- Broadway: Popular row (Wonder Woman, Bougie Shake, Strawberry Cheesecake, Fruity Pebbles; chosen by owner), coffee/latte Small+Large merged into one card with a size picker (cart ids unchanged: `*-sm` / `*-lg`), compact bottom-bar cookie banner on phones, 4 coffee items use NH `proteincoffee.jpeg`.
- NH Popular list is by real order count (213 orders): bougie-shake, wonder-woman, strawberry-cheesecake, banana-pudding, blueberry-cheesecake, strawberry-sunrise.

**Backups (same folder as the file):**
- NH: `index.html.bak-pre-3pct-20261026-193132`, `order-safeguards.js.bak-pre-3pct-20261026-193132`, plus earlier `*-pre-cardfee-20261026-165122`, `*-pre-taxline-*`, `*-pre-polish-*`, `*-pre-cardcleanup-*`, `*-pre-stickybar-*`, `*-pre-photocrop-*`; `images.bak-pre-shrink-20261026-161916`.
- Broadway: `index.html.bak-pre-ux2-20261026-193132`, `order-safeguards.js.bak-pre-3pct-20261026-193132`, `analytics-consent.js.bak-pre-ux2-20261026-193132`, `menu-data.js.bak-pre-coffeephoto-20261026-185125`, plus `*-pre-cardfee-20261026-165122`, `index.html.bak-pre-taxline-*`, `index.html.bak-pre-uxpass-*`.
- Rollback: copy the backup over the live file; restart the service only if it is `server.js` or `order-safeguards.js` (restart BOTH client and server together or in-flight pages get "cart total has changed").

**Gotchas learned:**
- Any fee/validation change makes already-open customer pages fail with 400 until refreshed (hit on Ronnie's iPhone at 4:56 PM). Logs do not print the rejection reason.
- Broadway only accepts orders Mon-Fri 7am-1pm CT, so it can only be test-ordered then.

**Still open:** real paid test on Broadway (tomorrow AM) incl. fee line/SMS/receipt; confirm 3% surcharge is OK with Square; photos for Cookies N' Cream (NH photo has NH label), Hot Latte S/L, BCAA, Creatine; Broadway socials/GBP to its own GHL sub-account by Oct 31; sales tax; decide whether Broadway should accept orders when closed.
