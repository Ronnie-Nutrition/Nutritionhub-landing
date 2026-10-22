#!/usr/bin/env python3
"""Extend Nutrition Hub GHL Social Planner schedule: 2026-09-01 -> 2026-10-31.

Continues the cadence set by extend_nh_schedule.py (which ran dry 8/31 stories+GBP,
9/2 reels):
  - stories 4/day (FB page + IG) at 14:00/17:00/20:00/23:00 UTC = 9a/12p/3p/6p CT
  - GBP post daily at 12:30 UTC (7:30a CT)  -- Nutrition Hub GBP ONLY
  - reels Mon/Wed/Fri at 12:30 UTC (FB page + TikTok + YouTube; no IG)

Content pools are harvested from existing posts, same as v1.

NOTE: Broadway Nutrition's GBP (connected 2026-08-08, accountId
6a7770144303710f91dea0c5_HJl01216dIdKMhk1SSn1_10923482578739590763) is deliberately
NOT added here. Every NH GBP caption hard-codes "Nutrition Hub" and "Suite 113",
which would publish NH's NAP onto Broadway's profile. Broadway needs its own pool.

Usage: extend_nh_schedule_v2.py [--dry | --test | --go]
"""
import json, os, sys, time, urllib.request
from datetime import date, timedelta

TOKEN = os.environ.get("GHL_NUTRITION_HUB_TOKEN") or os.environ["GHL_TOKEN"]
LOC = "HJl01216dIdKMhk1SSn1"
BASE = "https://services.leadconnectorhq.com"
USER = "mkC7CKXwuE6ViKqQg8Pj"

FB = "6a29a13b965956f459d7c15e_HJl01216dIdKMhk1SSn1_409790662219191_page"
IG = "68cd77a40f1b9b39fe419b5e_HJl01216dIdKMhk1SSn1_17841408224499449"
TT = "6a29a1b9b09bd821d0e9fb98_HJl01216dIdKMhk1SSn1_000shqOX7HcItWo1iNuN1r0tIuKLdIoBPd_business"
YT = "6a29bbd4e5f6a39a723079d6_HJl01216dIdKMhk1SSn1_UCCqbzVh4L3jtUk40686nhsA_profile"
NH_GBP = "6a29a115d325c1c5f71eaf36_HJl01216dIdKMhk1SSn1_12102537292225108267"

STORY_ACCTS = [FB, IG]
GBP_ACCTS = [NH_GBP]
REEL_ACCTS = [FB, TT, YT]
STORY_SLOTS = ["14:00", "17:00", "20:00", "23:00"]

START = date(2026, 9, 1)
END = date(2026, 10, 31)
REEL_WEEKDAYS = {0, 2, 4}  # Mon/Wed/Fri


def api(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method)
    req.add_header("Authorization", "Bearer " + TOKEN)
    req.add_header("Version", "2021-07-28")
    req.add_header("Content-Type", "application/json")
    data = json.dumps(body).encode() if body is not None else None
    with urllib.request.urlopen(req, data=data, timeout=30) as r:
        return json.loads(r.read())


def all_posts():
    posts, skip = [], 0
    while True:
        d = api("POST", f"/social-media-posting/{LOC}/posts/list",
                {"type": "all", "limit": "100", "skip": str(skip)})
        batch = d.get("results", {}).get("posts", [])
        posts += batch
        if len(batch) < 100:
            return posts
        skip += 100


def build_pools(posts):
    """Harvest rotation pools. Dedupe by media url / caption text."""
    story_media, reel_items, gbp_pairs = [], [], []
    seen_s, seen_r, seen_c = set(), set(), set()
    for p in posts:
        if p.get("deleted"):
            continue
        media = p.get("media") or []
        if not media:
            continue
        url = media[0].get("url")
        t = p.get("type")
        if t == "story" and url not in seen_s:
            seen_s.add(url)
            story_media.append(media[0])
        elif t == "reel" and url not in seen_r:
            seen_r.add(url)
            reel_items.append({"summary": p.get("summary") or "", "media": media[0]})
        elif t == "post" and p.get("summary") and p["summary"] not in seen_c:
            seen_c.add(p["summary"])
            gbp_pairs.append({"summary": p["summary"], "media": media[0]})
    return story_media, reel_items, gbp_pairs


def mk(accts, typ, day_iso, hhmm, media, summary=""):
    return {"accountIds": accts, "type": typ, "userId": USER,
            "summary": summary, "status": "scheduled", "source": "composer",
            "scheduleDate": f"{day_iso}T{hhmm}:00.000Z", "media": [media]}


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--dry"
    posts = all_posts()
    stories, reels, gbps = build_pools(posts)
    print(f"pools: {len(stories)} story videos | {len(reels)} reels | {len(gbps)} GBP pairs")
    if not (stories and reels and gbps):
        sys.exit("ERROR: an empty pool — aborting rather than scheduling blanks")

    existing = {(str(p.get("scheduleDate"))[:16], p.get("type"))
                for p in posts if p.get("status") == "scheduled" and not p.get("deleted")}

    payloads = []
    d, day_i, reel_i = START, 0, 0
    while d <= END:
        iso = d.isoformat()
        for s_i, slot in enumerate(STORY_SLOTS):
            if (f"{iso}T{slot}", "story") not in existing:
                payloads.append(mk(STORY_ACCTS, "story", iso, slot,
                                   stories[(day_i * 4 + s_i) % len(stories)]))
        if (f"{iso}T12:30", "post") not in existing:
            g = gbps[day_i % len(gbps)]
            payloads.append(mk(GBP_ACCTS, "post", iso, "12:30", g["media"], g["summary"]))
        if d.weekday() in REEL_WEEKDAYS and (f"{iso}T12:30", "reel") not in existing:
            r = reels[reel_i % len(reels)]
            payloads.append(mk(REEL_ACCTS, "reel", iso, "12:30", r["media"], r["summary"]))
            reel_i += 1
        day_i += 1
        d += timedelta(days=1)

    n = {}
    for p in payloads:
        n[p["type"]] = n.get(p["type"], 0) + 1
    print(f"to create: {len(payloads)}  {n}")
    print(f"window: {START} -> {END}")

    if mode == "--dry":
        print("\nDRY RUN — nothing sent. Sample:")
        print(json.dumps(payloads[0], indent=1)[:420])
        return
    if mode == "--test":
        r = api("POST", f"/social-media-posting/{LOC}/posts", payloads[0])
        print("TEST created:", json.dumps(r)[:300])
        return
    if mode != "--go":
        sys.exit("pass --dry, --test or --go")

    created, failed = 0, 0
    for i, p in enumerate(payloads):
        try:
            api("POST", f"/social-media-posting/{LOC}/posts", p)
            created += 1
        except Exception as e:
            failed += 1
            print(f"FAIL {p['scheduleDate']} {p['type']}: {e}")
        if i % 25 == 24:
            print(f"...{i+1}/{len(payloads)}")
        time.sleep(0.15)
    print(f"DONE: created={created} failed={failed}")


main()
