# Nutrition Hub — Toll-Free SMS Verification Submission Package
**Number:** +1 (844) 748-2536 · **GHL Location:** Nutrition Hub (`HJl01216dIdKMhk1SSn1`)
**Prepared:** July 1, 2026 · Copy-paste each field into GHL → Phone System → **Trust Center → Toll-Free Verification**.

---

## ⚠️ DO THIS FIRST (2 manual steps in GHL — API can't set these)
1. **GHL → Settings → Business Profile** (Nutrition Hub location):
   - **Website:** `https://nutritionhub101.com`
   - **Business Email:** `ronnie@nutritionhub101.com`
   *(Both are currently blank; the toll-free form pre-fills from here. Reviewers cross-check the email domain against the website — a domain-matched email is a green flag.)*
2. Then go to **Phone System → Trust Center** (or the ⚠️ "Verification Required" link next to the number) and start the **Toll-Free Verification** form.

---

## FORM FIELDS (paste these)

**Business name:** Nutrition Hub
**Legal entity / EIN:** The Nutrition Hub · EIN 88-4164610 *(already VETTED with Twilio)*
**Business address:** 8201 Broadway St, Suite 113, Pearland, TX 77581, US
**Business website:** https://nutritionhub101.com
**Business contact email:** ronnie@nutritionhub101.com
**Business contact phone:** (844) 748-2536  *(or Ronnie's cell 520-560-5447 if a mobile is required)*
**Business type / industry:** Health & wellness — retail (smoothie / nutrition club)

**Use-case category:** Mixed — Marketing + Customer Care

**Use-case summary / description** (paste verbatim):
> Nutrition Hub is a smoothie and nutrition club in Pearland, TX. We send recurring text messages only to customers who opt in through the consent form at https://nutritionhub101.com/sms. Messages include loyalty and rewards updates, appointment and consultation reminders, and promotional offers on our in-store products. Customers enter their first name and mobile number and check an unchecked consent box agreeing to receive recurring automated marketing and informational texts. Message frequency varies (approximately 2–6 messages per month). Message and data rates may apply. Customers can reply STOP to unsubscribe or HELP for help at any time.

**Opt-in type:** Web form (online opt-in)
**Opt-in URL:** https://nutritionhub101.com/sms

**Opt-in workflow description** (paste verbatim):
> Consumers visit https://nutritionhub101.com/sms, enter their first name and mobile number, and check a consent checkbox that is unchecked by default. The checkbox reads: "I agree to receive recurring automated marketing and informational text messages from Nutrition Hub at the number provided (loyalty rewards, appointment reminders, and promotions). Consent is not a condition of any purchase. Msg frequency varies (approx. 2–6 msgs/month). Msg & data rates may apply. Reply STOP to cancel, HELP for help." The page links to the Privacy Policy (https://nutritionhub101.com/privacy-policy) and Terms & Conditions (https://nutritionhub101.com/terms). No number is collected and no consent is recorded unless the box is checked.

**Privacy Policy URL:** https://nutritionhub101.com/privacy-policy
**Terms & Conditions URL:** https://nutritionhub101.com/terms

**Estimated monthly message volume:** ~2,000

**Sample messages** (use 3–4; each names the business and includes STOP):
1. `Nutrition Hub: 🍓 New protein shake special — show this text for $2 off today! Reply STOP to opt out, HELP for help.`
2. `Nutrition Hub: You've earned a free tea reward 🎉 Redeem it this week in-store. Reply STOP to unsubscribe.`
3. `Nutrition Hub: Reminder — your wellness eval is tomorrow at 3:00 PM, 8201 Broadway Ste 113. Reply C to confirm, STOP to opt out.`
4. `Nutrition Hub: You're in! Loyalty rewards, reminders & promos. Msg freq varies, msg & data rates may apply. Reply HELP for help, STOP to cancel.` *(opt-in confirmation / welcome message)*

**Opt-out message** (if asked): `Nutrition Hub: You've been unsubscribed and will not receive further texts. Reply START to rejoin.`
**Help message** (if asked): `Nutrition Hub: For help call (844) 748-2536 or email ronnie@nutritionhub101.com. Msg & data rates may apply. Reply STOP to cancel.`

---

## WHY THIS SHOULD CLEAR FIRST-PASS
- **Single opt-in channel** (web form) that actually exists and is live — no fabricated keyword/paper channels for a reviewer to fail us on.
- **Privacy Policy carries the mandatory carrier line** verbatim: "No mobile information will be shared with third parties/affiliates for marketing or promotional purposes. All the above categories exclude text messaging originator opt-in data and consent; this information will not be shared with any third parties."
- **Consent box is unchecked by default** and consent language is complete (brand, msg types, frequency, rates, STOP/HELP, "not a condition of purchase").
- **Every sample** names "Nutrition Hub" and includes STOP.
- **Domain-matched contact email** (ronnie@nutritionhub101.com) matches the website and the EIN-vetted brand.

## LIVE ASSET CHECK (all verified 2026-07-01)
- https://nutritionhub101.com/privacy-policy → real Privacy Policy (HTTP 200)
- https://nutritionhub101.com/terms → real Terms (HTTP 200)
- https://nutritionhub101.com/sms → opt-in form w/ unchecked consent box (HTTP 200)
- Homepage footer links to all three.

## TIMELINE EXPECTATION
GHL/LeadConnector routes toll-free verification to Twilio's toll-free team. Typical review is ~1–3 business days; a clean, matching single-channel package like this is what avoids the rejection→resubmit loops that add a week. We control first-pass correctness; the clock itself is on the carrier reviewer.

## POST-APPROVAL TODO (not required for verification)
- Wire the /sms form to capture into GHL (native GHL form or an inbound-webhook endpoint) so real signups land in the CRM. Right now the page validates + confirms client-side; submissions are not yet stored.
- Add the same SMS consent checkbox to the order/check-in flows on order.nutritionhub101.com to close the TCPA gap on transactional texts.
