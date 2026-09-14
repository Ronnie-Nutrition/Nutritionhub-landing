#!/usr/bin/env python3
# Additive patch: add a standalone $3 B12 Energy Drink to the live order menu.
# Idempotent — safe to re-run. Inserts after the Daily Detox special line.
import sys, re

PATH = "/opt/nutritionhub-menu/menu-data.js"
NEW_ITEM = "  { id: 'b12-energy-drink',     name: 'B12 Energy Drink',       type: 'special', price: 3.00, image: PLACEHOLDER },\n"
ANCHOR = "id: 'daily-detox'"

with open(PATH, "r", encoding="utf-8") as f:
    src = f.read()

if "b12-energy-drink" in src:
    print("ALREADY_PRESENT — no change")
    sys.exit(0)

lines = src.splitlines(keepends=True)
out = []
inserted = False
for ln in lines:
    out.append(ln)
    if (not inserted) and ANCHOR in ln:
        out.append(NEW_ITEM)
        inserted = True

if not inserted:
    print("ANCHOR_NOT_FOUND — aborting, no change")
    sys.exit(1)

with open(PATH, "w", encoding="utf-8") as f:
    f.write("".join(out))
print("INSERTED b12-energy-drink $3.00 after daily-detox")
