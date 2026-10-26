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
