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
