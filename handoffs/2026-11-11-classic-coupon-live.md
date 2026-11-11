# First-visit coupon redesign — November 11, 2026

Owner approved the ivory/charcoal drink-photo preview and explicitly requested publishing at the same URL with signup preserved.

Published https://nutritionhub101.com/offer/ from branch codex/nh-coupon-classic-20261111, implementation commit ff8305b. Isolated source checkout /private/tmp/nh-coupon-live-20261111. Existing shared checkout was not edited. Static site is not in ops/verify registry (verified); only /var/www/nutritionhub-home/offer/index.html and drink.png shipped. No /opt files, server config, services, rewards pages or workflows changed.

Original live index SHA256 matched source before deployment: 9ad2fa92373eeb59a506d6d28f50417ea9d0aaafdb042bcbf516c1efad313a30. Backup /root/deploy-backups/nh-offer/20261111-classic/index.html. New public index hash c7aedd72ae1a604ea3715377f3ed16d0bb4b5f217690e9cd72187bae0ead069a. Public HTTPS response compared byte-for-byte to installed file, PASS. Drink image HTTP 200.

GHL native form vrXCifpkphOjHh5tgplv retained. Updated only HTML 1 custom header via normal builder, saved and confirmed public render. New CSS/header is offer/ghl-header.html; prior header backup offer/ghl-header-before-20261111.html. Existing separate custom CSS still present; new header overrides its neon colors. No fields, consent text, validation, submit behavior, confirmation or automation changed. Native button retains Submit label. Original official iframe attributes/loader and allowlisted UTM forwarding retained. Live native fields stack vertically (slight difference from mockup's paired names).

Verification:
- Live desktop and 390px mobile render; image loads, no horizontal overflow; official iframe autosizes and Submit visible.
- Empty submit produces Phone is required and Email is required, no contact data submitted.
- Original coupon workflow 06e48c91-7a42-4cda-8d67-7478f1a61601 remains Saved/Publish ON; form-specific trigger plus Terms and Conditions Yes verified. Eligibility guard still excludes SMS DND, requires NH3 code empty and excludes nh-register-return-active. Read-only inspection, canceled panel.
- Existing browser held cached old outer HTML. Fetch with cache:reload followed by navigating the SAME /offer/ URL verified new heading and ivory background. New visitors get current source; previous visitors may need refresh.
- No fresh coupon enrollment or SMS delivery test performed. Owner already has prior claim; do not clear code or bypass duplicate guard. Asked owner to have a new eligible tester submit once on their own phone, then confirm text delivery. Browser automation produces Cloudflare challenge console errors (also observed before edits); do not bypass it or claim end-to-end delivery from form rendering. Earlier manual native test was Delivered October 21; this is historical, not today's verification.

Raw deploy result: PASS: public offer page matches deployed source; backup saved.
