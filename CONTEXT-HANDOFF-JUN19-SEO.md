# Context Handoff — Nutrition Hub Local SEO (June 19, 2026)

## TL;DR
Built and deployed a free local-SEO foundation for **nutritionhub101.com**. Phase 1 (technical/schema) done. Phase 2 (local landing pages) started — first page live. Everything verified live, Meta Pixel/CAPI untouched, all committed to PR #1.

---

## What was done this session

### Phase 1 — technical SEO (DONE, live)
- **Homepage** (`nutritionhub-neon-home.html` → deploys as `/var/www/nutritionhub-home/index.html`):
  - FoodEstablishment JSON-LD schema (name, address, hours, menu, cuisine, **geo** lat 29.559174 / lng -95.345263)
  - `<link rel="canonical">`, Open Graph + Twitter cards
  - Added "Pearland, TX" to the H1
- **Order site** (`/opt/nutritionhub-menu/index.html`, separate Node app — patched in place, NOT overwritten):
  - Title fixed: "Order Online — Protein Shakes & Energy Teas | Nutrition Hub Pearland, TX"
  - Added meta description + canonical + OG
- **robots.txt + sitemap.xml** deployed to web root, serving real content
- **Google Search Console**: verified via HTML file (`googled00c38b198f8183f.html` — lives in web root, DO NOT DELETE), sitemap submitted, homepage indexed + re-crawl requested

### Phase 2 — local landing pages (IN PROGRESS)
- **`/energy-teas-pearland/`** — LIVE. Targets "energy teas / lit teas pearland." Neon design (cyan accent), FoodEstablishment + **FAQPage** schema (5 Q&As → FAQ rich results), internal link FROM homepage, added to sitemap. Template for future pages.
  - Uses lit-tea price **$9.15** + flavors **Mamacita / Blue Ocean / Blue Margarita** — Ronnie approved on preview; re-verify if menu changes.

---

## 🚨 Critical rules (read before touching anything)
1. **Meta Pixel `915336731481586` is sacred** — init + PageView + Lead events on order buttons. A live Meta ad + server-side CAPI depend on it. SEO edits are **additive `<head>` metadata ONLY**. Verify pixel count unchanged after every deploy.
2. **Never overwrite the order site wholesale** — `/opt/nutritionhub-menu/` live copy is newer than the local repo copy. Patch the `<head>` in place (use a Python script, scp it over — not heredocs).
3. **Always back up the live file first** before any deploy: `cp index.html index.html.bak-<reason>-<timestamp>`.
4. **Homepage is NOT git-auto-deployed** — merging PR ≠ live. Deploy = scp to VPS web root. No nginx restart needed (static file). Order site also reads from disk per request — no restart.

---

## Infra / deploy cheat-sheet
- **VPS**: `ssh -o IdentitiesOnly=yes -i ~/.ssh/id_ed25519 root@64.23.156.59`
- **Homepage web root**: `/var/www/nutritionhub-home/` (`index.html` = neon home; repo file is `nutritionhub-neon-home.html`)
- **Order site**: `/opt/nutritionhub-menu/` (Node app, systemd `nutritionhub-menu`)
- **New landing pages**: deploy as `/var/www/nutritionhub-home/<slug>/index.html` → clean URL `/<slug>/`
- **Repo**: `~/GTM-Workspace/nutritionhub-landing` → GitHub `Ronnie-Nutrition/Nutritionhub-landing`
- **PR #1**: branch `seo/phase1-local-optimization` — open, holds all homepage/sitemap/landing commits. Order-site patch was deployed directly (folder not tracked in repo).
- **Backup of this session**: `~/Desktop/_Backups/BACKUP-2026-06-19-nutritionhub-seo/` (repo + live VPS copies)

---

## Next session — pick up here
**Goal: keep building the local landing-page cluster (Ronnie wants steady ongoing buildout).**

Queued pages (reuse `energy-teas-pearland.html` as template — swap keyword, content, schema, flavors):
1. **Meal Replacement / Weight Loss Shakes Pearland** ← highest buyer intent, do next
2. **B12 Shots Pearland**
3. **Protein Shakes Pearland**

For each new page: build → preview in browser → Ronnie approves → deploy to `/<slug>/` → add internal link from homepage → add to sitemap.xml → redeploy homepage+sitemap → commit to PR → **Ronnie requests indexing in Search Console**.

Other free wins still open:
- Verify Google Business Profile NAP exactly matches the site (#1 local ranking factor)
- Eventually: blog/content cluster around each landing page for topical authority (write in-repo with Claude, no paid tool)
- Consider merging PR #1 to keep `main` in sync (cosmetic; production already live)

See memory: `project_nutrition_hub_seo.md` for the durable version of all this.
