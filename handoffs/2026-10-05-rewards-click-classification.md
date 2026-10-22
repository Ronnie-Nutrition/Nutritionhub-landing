# Approved rewards-click classification correction — October 5, 2026

Ronnie approved separating rewards signup clicks from order-entry clicks. Added one pathname-specific classifier before the existing ordering-domain classifier in assets/portfolio-measurement.js. Consent gates, other sites, ordering links, purchase emitters and page copy remain unchanged.

Published only the equivalent one-line addition to the current live NH script, using an exact before-hash guard and atomic replacement; no whole-site deployment. Live/source scripts have pre-existing differences, preserved rather than overwriting either version.

Validation: eight offline stubbed cases passed (rewards with/without query; order root with/without slash; denied consent for both; existing directions; unrelated host). Public GET HTTP200 returned bytes identical to tested live candidate. New SHA256: 3a6c00d5ada51dea9fbea8326c0f14787889db363da2805507e95a2985aad2bc.

Remote rollback file: /root/nh-measurement-before-rewards-20261005T201519Z.js. Target: /var/www/nutritionhub-home/assets/portfolio-measurement.js. Restore backup only if current live hash still matches this release; then verify public bytes. No restart needed. No production synthetic events or purchase test sent, so subsequent processed rewards_signup_click collection remains unverified. Historical order_site_click totals may include rewards clicks and cannot be corrected from the old payload.

The same approved review verified Casa phone_click collection and marked only that event as a GA4 key event; directions_click was not observed and remains unmarked. Detailed restricted portfolio evidence and owner-session handoff remain in the Codex task workspace, not this site repository.

Next: retain this distinction in future builds and verify naturally occurring processed rewards/order events without generating test sales. No sales uplift claim.
