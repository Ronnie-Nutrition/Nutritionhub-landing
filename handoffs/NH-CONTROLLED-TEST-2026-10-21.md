# Controlled coupon validation — 2026-10-21

## Executed under explicit owner approval
- Checked prior execution logs: no logs. Existing owner contact had empty NH3 code/expiry, SMS DND unchecked and no new coupon conversation entry.
- Saved temporary exact-phone AND condition in the existing first-action guard, alongside SMS DND and empty-code checks. Guard name: TEST ONLY — Ronnie phone, SMS allowed, no coupon. Reopened and verified saved restriction before execution.
- Selected existing default sending number explicitly in workflow settings.
- Restored existing form controls for controlled test only, with prominent owner-only test notice and truthful submission confirmation. Public branded /offer/ remains non-collecting preview.
- Briefly enabled restricted existing workflow. Clicked Submit exactly once on the native form with existing owner identity and requested coupon-only consent. No separate Run test, second submission, or manual SMS.

## Blocker and outcome
- Native form remained on disabled Submit/spinner; no success confirmation.
- Browser console: [Cloudflare Turnstile] Error: 300030. Timestamp 2026-10-21T21:38:21.038Z.
- Form submissions view: No submissions yet. Workflow execution view: No logs found. NH3 coupon code and expiry remained empty. No provider delivery result exists in the inspected views.
- Treat submission as uncertain/stalled, not a confirmed carrier failure. Do not repeat or bypass anti-bot verification.
- Workflow turned OFF again and Saved verified. Temporary recipient guard and explicit sender remain saved.
- Pending native-form tab preserved without reload; form builder and workflow preserved. No general enrollment launched; no payment methods/credits/services changed.

## Exact next step
Resolve the visible GHL form/Cloudflare validation issue through ordinary user interaction or GHL support. Have owner inspect the preserved pending page; do not ask them to resubmit blindly. Check for a delayed submission/execution before any further send. If a human-verification challenge appears, owner can complete it directly; do not disable or bypass Turnstile. A fresh submission would be another attempt requiring reconciliation of this one.

## Remaining launch work
After a successful controlled validation: verify provider delivery and handset receipt, actual rendered expiry and code; fix native label/consent contrast seen on dark background; restore public wording and claim CTA; embed form in existing branded /offer/ with allowed UTMs; remove temporary recipient guard only when general claims are ready. Staff redemption is manual and first-visit eligibility is checked at redemption.

## Read-only Turnstile follow-up
- Preserved native form now shows Cloudflare widget spinner but no human checkbox/puzzle or actionable verification control. Submit re-enabled; no success confirmation. Do not infer success or click it again.
- Console repeats 300030, with crashed_retry challenge URLs at 21:41:04–05Z. Native host is api.leadconnectorhq.com; challenge script loads from challenges.cloudflare.com. No observed domain-not-authorized or invalid-sitekey code.
- Refreshed form submissions still No submissions yet; workflow enrollment history No enrollments found. Workflow remains OFF. No reload/resubmission/security changes.
- Official Cloudflare error table classifies 300* as generic challenge failure/bot detection; suffix internal. Domain unauthorized is 110200 and invalid keys have separate codes. No evidence supports DNS/domain/key edits here.
- Official supported-browser docs state automated browsers/frameworks are unsupported for production challenge solving. Automation interference is plausible, not proven account-specific root cause.
- Smallest supported user step: manually open https://debug.challenges.cloudflare.com/ in an ordinary up-to-date browser (no coupon data/submission) and report result. This can diagnose browser compatibility without another SMS attempt. No need to change security settings. If manual diagnostics pass, coordinate a human-driven form validation only after reconciling current pending request and explicitly authorizing any fresh submission. If failure persists manually, provide GHL support form ID, native URL, timestamps/error, and console/HAR through an approved support channel. No support message sent.
Sources:
https://developers.cloudflare.com/turnstile/troubleshooting/client-side-errors/error-codes/
https://developers.cloudflare.com/cloudflare-challenges/reference/supported-browsers/
https://developers.cloudflare.com/cloudflare-challenges/troubleshooting/challenge-solve-issues/

## Manual compatibility screenshot confirmation
Viewed both newest Desktop screenshots (4.45.05 PM and 4.45.00 PM, Oct 21). Cloudflare diagnostic timestamp 2026-10-21T21:44:53.519Z: Success, Diagnostics passed, no automation detected, clock synchronized, no privacy-tool interference, server reachable. This proves the manual diagnostic passed, not coupon submission or SMS delivery. Refreshed GHL submissions and enrollment remain empty. No new send or submission. Next: coordinate one human-driven signup after approval/reconciliation, enable only saved exact-recipient-guarded workflow first, user completes security check and submits once, inspect execution/provider/handset before opening general claims. Workflow remains off now.

## Manual signup ready — supersedes OFF state above
Reconciled again: no submissions/enrollments, no coupon conversation entry, NH3 fields empty, all DND boxes unchecked. Verified exact-phone AND SMS-permitted AND code-empty guard, dedicated consented form trigger, one approved SMS with native NH3 fields, explicit existing default sender and re-entry off. Enabled only this guarded workflow; Publish checked and Saved verified. No form submission or SMS test performed. Owner is to submit once manually in normal browser, then report confirmation/receipt for immediate read-only inspection. Public branded /offer remains noncollecting. Workflow intentionally remains enabled with owner-phone restriction awaiting manual validation.
