# Rewards privacy and truthful response repair — offline only

Prepared on October 17 UTC / October 16 late evening Central. No website or application code was deployed.

- Rewards removes unconditional Meta initialization, pixel fallback, and form-field advanced matching. The paired main-host analytics helper emits only an aggregate rewards-join event after consent; saved decline and withdrawal block it. Reaccept restores permissions without duplicate SDK initialization. Persistent privacy links and Privacy choices let customers reopen consent controls.
- If durable consent is recorded but its delivery queue handoff needs reconciliation, the page says the choice was recorded and directs the customer to a team member. It leaves the captured checkbox disabled and does not repeat the capture or send.
- A fresh visit restores an enabled, unchecked optional text-offer checkbox. OTP/staff check-in and optional marketing choice remain separate.
- The legacy `/sms` form now shows errors instead of claiming a failed request succeeded. It still sends affirmative legacy consent, so the paired server containment will reject it. Decide the verified-signup handoff or retirement before releasing this legacy flow.

Validated with 22 analytics lifecycle scenarios (515 assertions), an isolated Chromium synthetic rewards journey with all external requests intercepted, and five legacy-form failure tests. These do not establish actual SDK behavior, live GHL saves, or SMS delivery. No personal records, credentials, real signup, or send were used.

The proposed server guards and sender binding/storage work are on the separate Agentic_OS branch `codex/nh-winback-standing-20261014`, under `Nutrition_Hub_Automation/reviews/2026-10-17-pipeline-repairs/`. Read that handoff before any release. It records signup/upsert identity risks, old receipts without destination proof, credential rotation, recovery timing, exact recipient reconciliation, and dependency/package checks.

Ronnie explicitly approved only engaging the existing customer sender kill switch in production. It was verified engaged at 2026-10-17T04:18:09Z; all attempt records and timer definitions were preserved. That approval does not authorize deployment or releasing the hold.

Deploy `rewards/index.html` with the root `analytics-consent.js` as a reviewed main-host pair. Do not overwrite the separately maintained order-host helper. No deployment script was run. The `/sms` page requires its own flow decision; the code here is truthful-error containment.
