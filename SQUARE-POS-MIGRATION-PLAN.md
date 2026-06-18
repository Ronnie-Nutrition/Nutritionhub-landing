# In-Store POS: Clover → Square — Migration Plan

**Created:** 2026-06-18 · **Status:** Planning · **Owner:** Ronnie
**Context:** Online ordering already cut over to Square production (2026-06-18). This plan covers moving
the **physical register** (currently Clover) to Square POS — the step that unlocks **true blended ROAS**.

---

## 1. Why do this (the payoff)

Right now sales live in two systems:
- **Online** → Square ✅ (just migrated; already fires Meta CAPI per order)
- **In-store register** → Clover ❌ (separate system, no automatic Meta feed)

Because in-store is on Clover, foot-traffic sales can't be fed to Meta automatically — today that's done
manually via HLMI/Clover CSV exports, which is painful (Meta retired CSV upload May 2025; CAPI rejects
events older than 7 days — see `project_nutritionhub_meta_offline_lookalike`).

**Move the register to Square and ALL sales (online + in-store) sit in one system.** Then we build ONE
automated **Square → Meta CAPI feed** that reports every dollar — counter + online — back to your ads.
That's the first time you'd see **real blended ROAS** (true cost-per-sale across foot traffic and online),
instead of the "blind ROAS" the Meta dashboard shows today.

Secondary wins: one catalog, one sales report, one place to reconcile, and you drop the Clover monthly/
processing bill once fully off it.

---

## 2. Current state → target state

| | Now | After |
|---|-----|-------|
| In-store register | Clover | Square POS |
| Online ordering | Square ✅ | Square ✅ |
| Item catalog | Clover (in-store) + `menu-data.js` (online) | One Square catalog |
| Loyalty / check-in | GHL (via order.nutritionhub101.com `/checkin`) | **Keep GHL** (see §6) |
| In-store → Meta | Manual HLMI CSV push | Automated Square→Meta CAPI feed |

---

## 3. Hardware (Clover hardware will NOT work with Square — it's proprietary)

You need a Square device or a tablet/phone running the free Square POS app. Current prices (2026):

| Option | Price | Best for | Notes |
|--------|-------|----------|-------|
| **Square Reader** (chip/contactless) | $59 (first magstripe reader free) | Cheapest start | Pairs to a phone/tablet you already own |
| **Square Stand** | $149 | Counter register | Needs a **compatible iPad** (do you have one?) |
| **Square Terminal** ⭐ | $299 (or ~$27/mo ×12) | All-in-one counter | Handheld, **built-in receipt printer**, no iPad needed |
| Square Register | $799 | Big counters | Overkill for a single drink counter |
| Square Handheld | $399 | Mobile order-taking | Nice-to-have, not needed day 1 |

**Recommendation:** If you already have an iPad → **Square Stand ($149)**. If not → **Square Terminal
($299)** is the clean single-device counter setup (printer included, nothing else to buy). Avoid the
$799 Register — you don't need it.

Cheapest possible bridge: free/$59 reader + a phone to *test* Square POS this week before buying a counter device.

---

## 4. Software / plan & fees

- **Square POS app: free.** No monthly software fee on the Free plan.
- **In-person processing (Free plan, 2026): 2.6% + 15¢ per tap/dip/swipe.** (Square raised the per-transaction
  cents from 10¢→15¢ in Oct 2025.) Plus plan ($49/mo) drops it to 2.5% + 15¢ — not worth it at your volume.
- **➡️ ACTION:** pull your current **Clover in-store rate** off a recent statement and compare. On low-ticket
  drink sales the *per-transaction* cents matters more than the %. (e.g. on a $7 shake, 15¢ ≈ 2.1% on its own.)

---

## 5. Catalog migration

Your Square catalog is currently empty (the online site charges card-only; it doesn't use Square's catalog).
You'll build the item library once in Square — it then serves the register.
- You already have the full item list + prices in `menu-data.js` and your Clover menu.
- Square supports **bulk import via CSV** (Dashboard → Items → Import) — I can generate that CSV from
  `menu-data.js` so you're not typing items by hand.
- Modifiers (sizes, add-ins, boosts) get set up as Square **modifier sets**.

---

## 6. Loyalty / check-in — KEEP GHL

Your check-in + rewards run through GHL today (`/checkin` page → GHL points/visits). **Don't move to Square
Loyalty** — it's a paid add-on (~$45+/mo) and you'd lose the GHL automation you already built. Keep the
GHL check-in flow exactly as is; it's independent of which POS rings the sale.

---

## 7. Migration steps (low-risk, parallel run)

1. **Get a Square device** (per §3) + confirm your bank/deposit is set on the **The Nutritional Hub**
   location (`LN9BK0S2ZGN4Q`) — same location the online site already deposits to, so reporting stays unified.
2. **Build the Square catalog** (I generate the CSV from `menu-data.js`; you import + add modifiers).
3. **Parallel-run for a few days:** keep Clover plugged in, ring a few real sales on Square, confirm
   deposits land + receipts read "The Nutritional Hub."
4. **Train** yourself + Ysela + staff on the Square flow (it's simple — tap item, take payment).
5. **Cut over:** make Square the primary register. Keep Clover unplugged-but-active as a backup for ~1 week.
6. **Decommission Clover** once Square is stable (cancel Clover plan/hardware billing). Coordinate with the
   online-site Clover decommission (`project_nutritionhub_ordering_site` item d).

---

## 8. The blended-ROAS feed (what I build once in-store is on Square)

Once register sales are in Square, I build a **recurring job on the VPS** (cron) that:
- Pulls completed Square payments via the Payments API (online + in-store, location `LN9BK0S2ZGN4Q`),
- Hashes buyer phone/email and pushes them to the Meta pixel via **Conversions API** as Purchase events
  (deduped against the online pixel events already firing),
- Runs frequently enough to stay inside Meta's 7-day CAPI window (no more stale CSV rejects).

Result: Meta attributes **foot-traffic + online** purchases to your ads → true blended ROAS, and the
lookalike audience (the 2,422-buyer 1% LAL) keeps refreshing automatically instead of by manual export.

---

## 9. Costs summary

| Item | One-time | Monthly |
|------|----------|---------|
| Square Terminal *or* Stand | $299 / $149 | — |
| Square POS software | — | $0 (Free plan) |
| Processing | — | 2.6% + 15¢ per in-person sale |
| Square Loyalty | — | $0 (keeping GHL) |
| Blended-ROAS CAPI feed (I build it) | $0 | $0 (runs on existing VPS) |
| **Clover** (after cutover) | — | **drops off** |

---

## 10. Decisions / inputs needed from Ronnie

1. **Do you have an iPad?** (→ Stand $149) or want the all-in-one (→ Terminal $299)?
2. **Your current Clover in-store rate + any contract lock-in / early-termination fee?** (decides timing)
3. **Roughly how many people need training** (just you + Ysela, or counter staff too)?
4. Go/no-go on ordering a Square device to start the parallel run.

---

## 11. Risks / watch-outs

- **Clover contract lock-in** — check for an early-termination fee before cancelling.
- **Clover hardware is not reusable** — budget for the Square device.
- **Catalog accuracy** — verify prices/modifiers after CSV import before going live.
- **Don't rush §6** — keep GHL loyalty; moving it adds cost + breaks working automation.
- **Parallel-run discipline** — don't cancel Clover until Square has run clean for ~1 week.
