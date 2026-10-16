# Rewards benefit headline — October 16, 2026

## Result

Published the approved headline **“Get $2 off your next visit”** to https://nutritionhub101.com/rewards/ at **1:46 p.m. America/Chicago**. It now appears before the phone field and is repeated in the optional text-offer summary. Supporting copy explains one drink, one use, eligible new U.S. mobile signups, and showing the offer text within seven days of receiving it.

Previously the first screen said “Enter your phone to check in” without mentioning the $2 offer. The optional section was titled “Want occasional drink offers by text? Optional.”

The original brand heading was “Nutrition Hub” with “R E W A R D S” below it. The original first-screen button was “Check In & See Points”; the optional SMS button was “Get text offers.” Both button labels remain unchanged.

Only static wording in `/var/www/nutritionhub-home/rewards/index.html` changed. All script blocks, stylesheet blocks, form-control attributes, links, consent disclosure, checkbox default, disabled offer button, verification requirements, and backend behavior remain byte-for-byte unchanged. No check-in, consent submission, manual SMS, payment, provider retry, settings change, or service reload was performed.

## Source and deployment

- Task branch: `codex/nh-rewards-benefit-20261016`.
- Baseline commit `2f91c85` preserves the exact deployed HTML before changing the copy. The repository's older rewards file lacked newer verification/consent code; restoring it would have regressed the live page.
- Copy commit: `6357021` (five insertions, one deletion).
- Live site is Nginx on the VPS, rooted at `/var/www/nutritionhub-home`; the repository's GitHub Pages main branch is not the live custom-domain deployment path. No main or SEO branch was changed.
- Backup: `/root/nh-rewards-benefit-copy-20261016T184606Z/index.html.before`.
- Before SHA256: `7d1d11d28ca1abbcbafb0bb0fa776efc0fc7b66c5f667d5b0661e7e0fa379b52`.
- After SHA256: `cc156e9c85617a1a681f81ac53b4f566fa5cebb01fdd0b9d87be34aeb82a7b9e`.
- Deployment asserted the live baseline checksum, made a backup, and atomically replaced one HTML file while preserving owner/group and mode `0644`.

## Verification

Twelve static checks passed, including unchanged scripts/controls/disclosure and HTTP 200 for the Privacy Policy and Terms links. Isolated cached Chromium rendered 390px and 320px widths, with every HTTP(S) request blocked and no user Chrome profile. Both landing and expanded consent layouts fit without horizontal overflow. The consent checkbox stayed unchecked, the offer button stayed disabled, and STOP wording remained visible. The expanded consent screenshot is a presentation-only preview, not a real customer enrollment.

Raw public verification after deployment:

```json
{
  "checked_at_utc": "2026-10-16T18:46:14.536501+00:00",
  "url": "https://nutritionhub101.com/rewards/",
  "http_status": 200,
  "public_bytes_match_tested_file": true,
  "sha256": "cc156e9c85617a1a681f81ac53b4f566fa5cebb01fdd0b9d87be34aeb82a7b9e",
  "headline": "Get $2 off your next visit",
  "bytes": 28962
}
```

Local receipts, before/served HTML, validation scripts and mobile screenshots are in `/Users/apple/Documents/Codex/2026-10-09/task-2/rewards-offer-release/`. Public served bytes exactly match the rendered file. Full customer enrollment or SMS delivery was not tested because the task excludes synthetic consent and manual sends.

## Owner-number status — separate from page deployment

At **1:37:47 p.m. Central**, the existing read-only lookup succeeded (HTTP 200) for the owner's number ending **6922**, found the Rewards contact, and confirmed the returned number matched exactly. Only masked status was retained.

At that point the queue had six total entries and one fresh post-cutoff entry; the fresh consent status count was `opted_in: 1`. The encrypted queue and protected identity mapping did not permit a safe exact join to the owner's number using available read-only outputs. Therefore this does **not** confirm that the owner's scan completed SMS consent, entered the eligible queue, or received a message. A rewards check-in alone is not SMS opt-in. No credentials were read, identities exported, or messages sent.

Eligibility clarification: this is a fresh queued candidate plus an aggregate fresh opt-in, not proof that the complete sender gate has passed. The normal 2 p.m. Central run is its next scheduled opportunity. That run still validates receipt linkage and freshness, exact customer identity, current consent and GHL suppression status, U.S. destination, prior-attempt exclusion, daily/monthly limits, signed authorization/fee basis, and the kill switch. Passing the scheduled time does not itself prove a provider attempt or delivery.

Source review explains the read-only identity limit: the outbox encrypts the GHL contact ID with AES-256-GCM, while the consent ledger uses a separate canonical customer UUID. The identity ledger bridges them through an HMAC of the GHL contact ID. The public Rewards lookup confirms the contact/phone match but does not expose that consent linkage. The existing aggregate evidence can be read without keys; an exact join would require a permitted authenticated read interface or protected identity/encryption keys. None were loaded or bypassed for this check.

Next session: if requested, verify the owner's explicit consent/normal scheduled delivery through an authorized existing read-only interface. Do not infer the fresh queue entry's identity from timing alone, decrypt it by loading production secrets, manually run the sender, create synthetic consent, or retry an unknown provider attempt. No further page work is pending.
