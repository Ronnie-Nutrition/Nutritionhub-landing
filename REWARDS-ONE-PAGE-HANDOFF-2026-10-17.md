# One-page rewards and optional offers — review candidate

Website-only implementation in the existing task branch. Not committed or deployed; parent owns review, server/runtime work, publication and any sending decision.

- One phone field and one optional, unchecked consent choice. The same choice moves below the balance after rewards check-in.
- Coupon-only action checks trusted-device status, uses the existing OTP once if needed, then calls `/api/sms-optin` with `{phone,sms_consent:false,purpose:'offers'}` and credentials included. A validated account/session response is followed by the existing phone-bound `/api/consent/winback` capture. No geolocation, point award, name/email form, staff-PIN bypass or second OTP is used.
- Rewards-only signup uses `{phone,first_name,sms_consent:false,purpose:'rewards',pin?}` with credentials included. First name is optional; last name/email/profile completion are absent. After creating the zero-point account, the page calls the actual points-check-in endpoint and displays its result; it never invents an awarded point.
- Staff PIN stays transiently in memory only between staff check-in and new rewards join, is sent only to the rewards join/check-in calls, and clears on success, failure, Back and Done. It never goes to marketing consent.
- Returning members go straight to their balance. The optional text choice remains explicit and separate. STOP/help guidance does not clear provider or local suppression, and signing up again does not promise another coupon.
- Existing approved disclosure text/version, tracking consent controls, no-form-PII analytics, and truthful pending-handoff wording are retained.
- `/sms` redirects to `/rewards/` and has a visible fallback link. All old form submission code is removed.

## Required paired server contract

Parent must deploy the matching verified `/api/sms-optin` purpose handling before this UI: offers require exact-phone proof; staff PIN is rewards-only; create-only/exact-existing-ID identity handling must replace ambiguous upsert; new accounts start at zero visits/points. Expected success includes `success:true`, `contactId`, `sessionToken`, and optional `isNew`. Existing check-in supplies its normal authenticated balance. No frontend code grants authority.

## Validation

- `node --test tests/legacy-signup-response.test.cjs`: 1/1 passed (redirect/fallback, no legacy form or sender).
- `/usr/local/bin/node tests/rewards-one-page.browser.mjs`: 16/16 isolated Chromium scenarios passed. Fresh temporary profile, saved analytics decline, all browser requests intercepted, DNS disabled, synthetic API responses only. Zero live provider requests; zero tracking requests or advanced-matching data.
- Evidence summary and source hashes: `tests/rewards-one-page-results.json`. Full synthetic trace: `/tmp/nh-rewards-one-page-results.json`; mobile screenshot: `/tmp/nh-rewards-one-page.png`.
- Initial sandboxed Chromium startup failed before navigation. The approved isolated-process rerun and final layout rerun both passed. These are offline UI checks, not production E2E or SMS delivery proof.
- `git diff --check` passed. No source or production credentials read, real account created, text sent, hold changed, or application deployed by this subtask.

## Production completion
Deployed October 17 at 08:56 Central; public readback at 08:57 confirms rewards, sms and analytics files match source. Old order-host checkin.html redirects here and all three unsafe legacy APIs return410. No provider writes, real signup or texts used for verification. Sender stays held/inactive;8 prior attempts preserved. 314runtime tests on both Node20/24 and10deployment recovery tests pass. First health check used default3500; code-only rollback confirmed, checker corrected to actual8087, and subsequent deployment passed.

Remaining delivery prerequisites at08:58Central: dated owner-token replacement receipt absent; zero of14opt-in receipts have new destination binding (16totalrecords). No delivered SMS claimed. Fresh voluntary customer consent, private credential installation, current suppression/provider-history/no-duplicate checks and authorized timing remain required. Do not release hold or reuse consumed attempts. Full runtime handoff: Nutrition_Hub_Automation/handoffs/2026-10-17-essential-signup-release.md in Agentic_OS task branch.
