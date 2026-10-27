#!/usr/bin/env python3
"""Extend Nutrition Hub GHL Social Planner schedule.

- Collect rotation pools from existing story/GBP posts
- Add 20:00 UTC (3 PM CT) story slot for 7/14-7/20
- Schedule 7/21-8/31: stories at 14/17/20/23 UTC + GBP post at 12:30 UTC
Usage: extend_nh_schedule.py [--test | --go]
"""
import json, sys, time, urllib.request
from datetime import date, timedelta

import os
TOKEN = os.environ["GHL_NUTRITION_HUB_TOKEN"]  # from /Users/apple/GTM-Workspace/.env
LOC = "HJl01216dIdKMhk1SSn1"
BASE = "https://services.leadconnectorhq.com"
USER = "mkC7CKXwuE6ViKqQg8Pj"
STORY_ACCTS = [
    "6a29a13b965956f459d7c15e_HJl01216dIdKMhk1SSn1_409790662219191_page",
    "68cd77a40f1b9b39fe419b5e_HJl01216dIdKMhk1SSn1_17841408224499449",
]
GBP_ACCTS = ["6a29a115d325c1c5f71eaf36_HJl01216dIdKMhk1SSn1_12102537292225108267"]
STORY_SLOTS = ["14:00", "17:00", "20:00", "23:00"]  # UTC = 9a/12p/3p/6p CT

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
    story_media, gbp_pairs, seen_m, seen_c = [], [], set(), set()
    for p in posts:
        if p.get("deleted"):
            continue
        media = p.get("media") or []
        if p.get("type") == "story" and media:
            u = media[0]["url"]
            if u not in seen_m:
                seen_m.add(u)
                story_media.append(media[0])
        if p.get("type") == "post" and media and p.get("summary"):
            c = p["summary"]
            if c not in seen_c:
                seen_c.add(c)
                gbp_pairs.append({"summary": c, "media": media[0]})
    return story_media, gbp_pairs

def mk_story(day_iso, slot, media):
    return {"accountIds": STORY_ACCTS, "type": "story", "userId": USER,
            "summary": "", "status": "scheduled", "source": "composer",
            "scheduleDate": f"{day_iso}T{slot}:00.000Z",
            "media": [media]}

def mk_gbp(day_iso, pair):
    return {"accountIds": GBP_ACCTS, "type": "post", "userId": USER,
            "summary": pair["summary"], "status": "scheduled", "source": "composer",
            "scheduleDate": f"{day_iso}T12:30:00.000Z",
            "media": [pair["media"]]}

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--test"
    posts = all_posts()
    story_media, gbp_pairs = build_pools(posts)
    print(f"pools: {len(story_media)} story videos, {len(gbp_pairs)} GBP caption+image pairs")
    existing = {(str(p.get("scheduleDate"))[:16], p.get("type"))
                for p in posts if p.get("status") == "scheduled" and not p.get("deleted")}

    payloads = []
    # A) extra 20:00 slot for remaining pre-7/21 days
    d = date(2026, 7, 14)
    i = 0
    while d < date(2026, 7, 21):
        iso = d.isoformat()
        if (f"{iso}T20:00", "story") not in existing:
            payloads.append(mk_story(iso, "20:00", story_media[i % len(story_media)]))
        i += 1
        d += timedelta(days=1)
    # B) full days 7/21 - 8/31
    d = date(2026, 7, 21)
    day_i = 0
    while d <= date(2026, 8, 31):
        iso = d.isoformat()
        for s_i, slot in enumerate(STORY_SLOTS):
            if (f"{iso}T{slot}", "story") not in existing:
                payloads.append(mk_story(iso, slot, story_media[(day_i * 4 + s_i) % len(story_media)]))
        if (f"{iso}T12:30", "post") not in existing:
            payloads.append(mk_gbp(iso, gbp_pairs[day_i % len(gbp_pairs)]))
        day_i += 1
        d += timedelta(days=1)

    print(f"posts to create: {len(payloads)}")
    if mode == "--test":
        p = payloads[0]
        print("TEST MODE — creating only first payload:")
        print(json.dumps(p, indent=1)[:500])
        r = api("POST", f"/social-media-posting/{LOC}/posts", p)
        print("result:", json.dumps(r)[:400])
        return
    if mode != "--go":
        print("dry run only (pass --test or --go)")
        return
    created, failed = 0, 0
    for n, p in enumerate(payloads):
        try:
            api("POST", f"/social-media-posting/{LOC}/posts", p)
            created += 1
        except Exception as e:
            failed += 1
            print(f"FAIL {p['scheduleDate']} {p['type']}: {e}")
        if n % 20 == 19:
            print(f"...{n+1}/{len(payloads)}")
        time.sleep(0.15)
    print(f"DONE: created={created} failed={failed}")

main()
