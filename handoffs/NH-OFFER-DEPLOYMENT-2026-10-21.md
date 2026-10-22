# Nutrition Hub offer deployment handoff — 2026-10-21

## Completed
- Published an honest, non-collecting branded preview at https://nutritionhub101.com/offer/ using existing nginx static root /var/www/nutritionhub-home/offer/index.html.
- No DNS, server configuration, restart, or other page changes. /offer redirects to /offer/; public GET returned 200.
- Preserved approved first-visit $3 off one drink, seven days after signup. Clear claims-not-open notices; no form, input, iframe, or script in this preview.
- Official website palette: background #0a0d0a, lime #b6ff2e, orange #ff7a18, pink #ff2e88, cyan #23e0ff, text #eef3ea.
- Browser visually verified branded flyer and preview notice.

## Pending
- GHL coupon workflow remains draft/off. Prior single Run test has no recorded enrollment/execution/SMS result; latest execution view still No logs found. Handset receipt was denied by owner. This does not establish provider rejection or guarantee no queued message.
- Existing trigger matches dedicated form and consent. Guard checks SMS DND and empty coupon code. Re-entry disabled. Seven-calendar-day date math and one coupon SMS configured; rendered expiry and delivery not validated.
- Do not resend blindly. Proposed next validation: add a temporary exact-recipient allowlist before every issuing/sending action; verify existing contact has no queued coupon, no DND, no previous code; explicitly authorize one further controlled attempt with potential delayed-duplicate risk disclosed. Use a consented real form submission, verify enrollment, code/date, provider status and handset receipt; keep all other contacts excluded. No marketing sequence.
- After successful controlled validation: restore GHL claim controls and truthful thank-you text, remove preview-only CSS, embed existing GHL form here, forward allowlisted UTM parameters, verify attribution, then open general enrollment with owner authorization.
- Staff redemption remains manual: validate first visit, original expiry and no prior redemption, record receipt/staff redemption note. No POS-enforced coupon currently.

## Validation evidence
http=200 final_url=https://nutritionhub101.com/offer/
Deployed SHA256: 6c2691f6329c7084f617d8c07b990c5881bbc03a7effca318fd221a6c79d317a

## Rollback
Remove only newly added offer/index.html and empty offer directory after authorization; no shared configuration was modified.
