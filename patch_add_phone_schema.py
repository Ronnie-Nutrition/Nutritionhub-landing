#!/usr/bin/env python3
# Additive patch: add "telephone" to the homepage FoodEstablishment JSON-LD.
# Idempotent. Inserts right after the schema "url" line. Touches metadata only —
# does NOT alter the Meta Pixel or any other markup.
import sys

PATH = "/var/www/nutritionhub-home/index.html"
ANCHOR = '"url": "https://nutritionhub101.com/",'
NEW = '  "telephone": "(844) 748-2536",'

with open(PATH, "r", encoding="utf-8") as f:
    src = f.read()

if '"telephone"' in src:
    print("ALREADY_PRESENT — no change")
    sys.exit(0)

if ANCHOR not in src:
    print("ANCHOR_NOT_FOUND — aborting, no change")
    sys.exit(1)

# Replace only the first occurrence (the schema url line)
idx = src.index(ANCHOR) + len(ANCHOR)
patched = src[:idx] + "\n" + NEW + src[idx:]

with open(PATH, "w", encoding="utf-8") as f:
    f.write(patched)
print("INSERTED telephone after schema url line")
