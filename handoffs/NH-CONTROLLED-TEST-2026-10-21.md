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

## Awaited manual signup — read-only check
Refreshed Form 5 submissions: none. Workflow enrollment: none; execution logs: none. Refreshed existing contact: NH3 code/expiry empty and no new outbound coupon, so no coupon provider status to inspect. Workflow enabled state observed with test-only guard; no settings, form submission or sends performed. Awaiting user manual submission; tabs preserved. Browser instance bc462535 now inventory browser 1 (IDs can reorder).


## Read-only status — 2026-10-22 01:09 UTC
Mac connected. Refreshed Form submissions with Oct 1–31 filter: No submissions yet. Workflow execution filter extended through Oct22: No logs found. Unbounded enrollment history: No enrollments found. Refreshed existing owner contact: NH3 code and expiry empty, no coupon SMS in conversation. Workflow remains Saved and Publish ON, restricted by exact owner phone AND SMS DND not enabled AND empty NH3 code. Trigger exact claim form plus Terms and Conditions Yes. No changes/sends/submissions this check. Public HTTPS offer fetched successfully and retains claims-not-open preview; no collection. Await owner manual signup; no evidence it happened. Prior uncertain automated attempt was not retried. Preserve native form tab.


## iPhone manual-test readiness — 2026-10-22T02:31:45.311903+00:00
Remote Mac connected. Read-only: guarded workflow saved/enabled, exact owner phone plus SMS DND exclusion and empty code guard verified. Refreshed October form submissions and unbounded enrollment history remain empty. Refreshed owner contact code/expiry empty; no coupon message; all-channel and text-message DND unchecked. Native form renders owner-test notice, name/phone/email/consent controls and Submit; no submission performed, challenge success on iPhone not yet established. Await one manual Safari signup and then inspect execution/provider status. No recipient, activation, contact or public-site changes.


## Manual test succeeded — 2026-10-22 02:35 UTC
Contact activity records dedicated claim form submission. Workflow added at Oct21 9:31:29pm CDT; eligible 9:31:30, code 9:31:31, seven-calendar-day expiry calculated and stored 9:31:31–32, staff note 9:31:32, single SMS 9:31:33, finished 9:31:34. Event detail Send SMS Success. Contact code populated with NH3 plus existing contact ID; expiry 2026-10-28. Conversation Message Details: Lead Connector, Delivered, sender ending2536, recipient owner. Parent verified handset screenshot matches message/code/expiry. No retry or second send. Re-entry and multiple opportunities switches OFF verified.
Public completion attempted after parent explicitly instructed finishing launch. Automatic approval review DENIED before execution: filling/saving customer-facing header HTML interpreted as unauthorized under earlier draft-only restriction. Exact target existing Form5 custom HTML dialog. Read-only check confirmed original controlled-test notice and original markup remained, so rejected edit did not execute. No phoneguard removal, form/publicsite changes or general opening occurred. Parent must resolve approval conflict with fresh explicit evidence; retry denied operation at most once per materially new authorization. Form HTML dialog preserved, workflow Settings page preserved. No SMS retest needed.
Remaining launch work after blocker resolved: update flyer/confirmation and label contrast, embed native form on existing branded offer with allowlisted NH UTM forwarding, verify public responsive rendering without submission, remove only temporary phone condition retaining exact-form consent trigger, SMS DND guard and emptycode guard, verify saved enabled state. First-visit/redemption eligibility enforced manually by staff; same-contact repeat blocked, cross-contact duplicate-phone enforcement unproven.


## Public launch — 2026-10-22 02:48 UTC
Fresh parent evidence resolved rejected HTML save; one authorized retry permitted and completed. Final Form5 flyer has no test notices, single header. Custom CSS now makes labels/consent light and inputs white/dark. Confirmation states request received, coupon text for consenting contacts with no prior claim, original coupon for repeats, no false guarantee. Native form fetched in new tab and visually checked without submission.
Workflow general enrollment now saved ENABLED: removed only exact owner phone condition; renamed branch SMS allowed — no previous NH3 coupon. SMS DND exclusion AND codeempty retained. Exact form + TermsAndConditionsYes trigger retained. Reentry/multipleopportunitiesOFF, same six coupon steps and oneSMS; no manual sends. Existing resources retain DRAFT prefix internally but enabled state is ON.
Published branded /offer/ using official GHL iframe embed attrs and form_embed.js with consent-respect=true auto unchanged. Initial inline renders blank/hidden in connected Chrome. No console providererror, no security bypass. Added visible branded flyer + secure signup button as functional fallback to verified nativeform. Both iframe and fallback forward allowlisted utm_source,utm_medium,utm_campaign,utm_content,utm_term only, 200charlimit; campaign example nh_first_visit_3. No AshleyID. Desktop/mobile390px screenshots saved in taskfolder. Public page functional via nativeform button but full inline rendering remains unverified/blocked; don't claim all-inline success or verified tagged conversion attribution. Native manualtest attribution Direct traffic. User preference against genericGHL URL: branded share URL is correct, but fallback navigation exposes GHLhost; disclose rather than conceal.
Staff must verify firstvisit/no prior redemption, check expiry and record NH3 REDEEMED with time/receipt/staff. Samecontact repeat blocked; duplicatecontact/phonewide enforcement unproven. No secondSMS. Rollback preview file saved remotely before deployment. NoDNS/security/billing/unrelatedsite changes.


## Inline rendering resolved — 2026-10-22 02:56 UTC
Final public /offer/ renders native form inline in Ronnie & Ysela visible Chrome profile, verified via native Mac AX/screenshot and profile extension f1f8... (browser3). Inputs, coupon-only consent, policy links and Submit visible; mobile390px verified Submit.isVisible true and labels rgb238,243,234. Screenshots nh-offer-inline-desktop.jpg and nh-offer-inline-mobile.jpg in taskfolder. Earlier blank/hidden behavior was inconsistent in separate working GHL automation extension bc462...; not established as permanent service/CSP/domain restriction. No privacy/security changes. Official static iframe src/IDs/loader retained; branded loading flyer hides only when official loader makes iframe visible. Generic-host fallback button removed. No navigation off brandedURL required.
Workflow saved enabled general consented enrollment, expiry/dedup/DND retained. No further submission/SMS. End-to-end SMS tested via native manual ownerform (Delivered + handset); final branded embed rendering separately verified; tagged conversion not submitted. Footer and staffnotes explain firstvisit/manualredemption. UTM parameters forwarded to iframe; no Ashley campaignID.
