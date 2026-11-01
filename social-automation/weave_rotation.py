#!/usr/bin/env python3
"""Re-weave NH scheduled story rotation: interleave new uploads (freshest first) with existing pool.

Usage: weave_rotation.py [--dry | --go]
"""
import json, os, re, sys, time, urllib.request
from datetime import datetime, timezone, timedelta

import os
TOKEN = os.environ["GHL_NUTRITION_HUB_TOKEN"]  # from /Users/apple/GTM-Workspace/.env
LOC = "HJl01216dIdKMhk1SSn1"
BASE = "https://services.leadconnectorhq.com"
DROP = "/Users/apple/Desktop/NH-Story-Drop"
MAP = os.path.join(DROP, ".work", "upload_map.jsonl")

def api(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method)
    for k, v in [("Authorization", "Bearer " + TOKEN), ("Version", "2021-07-28"),
                 ("Content-Type", "application/json")]:
        req.add_header(k, v)
    data = json.dumps(body).encode() if body is not None else None
    with urllib.request.urlopen(req, data=data, timeout=30) as r:
        return json.loads(r.read())

# --- new media, freshest original first ---
uploads = [json.loads(l) for l in open(MAP)]
def orig_mtime(name):
    base = os.path.splitext(name)[0]
    for ext in (".MOV", ".mov", ".MP4", ".mp4"):
        p = os.path.join(DROP, base + ext)
        if os.path.exists(p):
            return os.path.getmtime(p)
    return 0
uploads.sort(key=lambda u: orig_mtime(u["name"]), reverse=True)
new_media = [{"url": u["url"], "type": "video/mp4", "thumbnail": "", "defaultThumb": ""}
             for u in uploads]
print(f"new media: {len(new_media)} (freshest: {uploads[0]['name']})")

# --- fetch all posts ---
posts, skip = [], 0
while True:
    b = api("POST", f"/social-media-posting/{LOC}/posts/list",
            {"type": "all", "limit": "100", "skip": str(skip)})["results"]["posts"]
    posts += b
    if len(b) < 100:
        break
    skip += 100

# --- existing story media pool (old content only) ---
new_urls = {m["url"] for m in new_media}
old_pool, seen = [], set()
for p in posts:
    if p.get("type") == "story" and (p.get("media") or []):
        m = p["media"][0]
        if m["url"] not in seen and m["url"] not in new_urls:
            seen.add(m["url"])
            old_pool.append(m)
print(f"old story pool: {len(old_pool)}")

# --- interleaved pool: n1,o1,n2,o2,... then remaining old ---
pool = []
for i in range(max(len(new_media), len(old_pool))):
    if i < len(new_media):
        pool.append(new_media[i])
    if i < len(old_pool):
        pool.append(old_pool[i])
print(f"combined pool: {len(pool)}")

# --- target slots: future scheduled stories, ascending ---
cutoff = (datetime.now(timezone.utc) + timedelta(minutes=30)).strftime("%Y-%m-%dT%H:%M")
slots = sorted((p for p in posts if p.get("status") == "scheduled" and not p.get("deleted")
                and p.get("type") == "story" and str(p["scheduleDate"])[:16] > cutoff),
               key=lambda p: p["scheduleDate"])
print(f"future story slots to reweave: {len(slots)} "
      f"({slots[0]['scheduleDate'][:16]} .. {slots[-1]['scheduleDate'][:16]})")

mode = sys.argv[1] if len(sys.argv) > 1 else "--dry"
if mode != "--go":
    for i, s in enumerate(slots[:8]):
        m = pool[i % len(pool)]
        tag = "NEW" if m["url"] in new_urls else "old"
        print(f"  {s['scheduleDate'][:16]} <- {tag} {m['url'][-24:]}")
    print("dry run; pass --go to apply")
    sys.exit(0)

ok = fail = 0
for i, s in enumerate(slots):
    m = pool[i % len(pool)]
    payload = {"accountIds": s["accountIds"], "type": "story",
               "userId": s.get("createdBy", "mkC7CKXwuE6ViKqQg8Pj"),
               "summary": s.get("summary", ""), "status": "scheduled",
               "source": "composer", "scheduleDate": s["scheduleDate"],
               "media": [m]}
    try:
        api("PUT", f"/social-media-posting/{LOC}/posts/{s['_id']}", payload)
        ok += 1
    except Exception as e:
        fail += 1
        print(f"FAIL {s['scheduleDate']}: {e}")
    if i % 25 == 24:
        print(f"...{i+1}/{len(slots)}")
    time.sleep(0.15)
print(f"WEAVE DONE ok={ok} fail={fail}")
