#!/usr/bin/env python3
"""
HLMyClub -> Meta CAPI in-store blended-ROAS feed  (Nutrition Hub)
================================================================
The in-store Square Terminal sales are driven by HLMyClub, which sends Square only
a dollar amount (no customer identity) -- so the Square payment data is anonymous
and can't be attributed. BUT HLMyClub itself knows the members. This feed closes
the loop from the HLMyClub side:

  * Receipts export (Receipts.xlsx)        -> dated POS sale: customer name + total
  * Customer Report export (Customer*.csv) -> name -> phone / email

We JOIN them on customer name, then push each matched in-store sale to the Meta
pixel via the Conversions API as a physical_store Purchase event with hashed PII.

Dedup / safety:
  * event_id = 'hl-<ReceiptNumber>' (Meta de-dups server-side)
  * local ledger data/hl_sent.json (don't resend across runs)
  * these are POS sales, a different channel from the order site (which fires its
    own realtime CAPI) and from the Square feed (which sends no in-store events) ->
    no double-count.

Meta rejects events whose event_time is older than 7 days, so only recent receipts
are sendable -- run/export at least weekly. The dry-run reports how many are too old.

STAGED OFF: dry-run unless HL_FEED_ENABLED=1. Reads Meta creds from env
(META_PIXEL_ID, META_CAPI_TOKEN) or a --env file.
"""
import os, sys, csv, json, time, hashlib, argparse, urllib.request, urllib.parse, urllib.error
from datetime import datetime, timezone

META_API_VER = os.environ.get("HL_META_VER", "v19.0")
MAX_EVENT_AGE_DAYS = 6.5
DEFAULT_DL = os.path.expanduser("~/Downloads")


def sha256(s):
    return hashlib.sha256(s.strip().lower().encode("utf-8")).hexdigest()


def digits(s):
    return "".join(ch for ch in str(s or "") if ch.isdigit())


def masked(v):
    v = str(v or "")
    return ("*" in v) or ("x" in v.lower())


def money(v):
    if v is None:
        return 0.0
    return float(str(v).replace("$", "").replace(",", "").strip() or 0)


def load_contacts(csv_path):
    """name(upper) -> (phone_digits, email) for unmasked, usable rows."""
    out = {}
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            nm = (r.get("Customer Name") or "").strip().upper()
            ph = r.get("Phone") or ""
            em = r.get("Email") or ""
            ph = digits(ph) if (ph and not masked(ph)) else ""
            em = em.strip() if (em and not masked(em)) else ""
            if nm and (ph or em):
                out[nm] = (ph, em)
    return out


def load_receipts(xlsx_path):
    import openpyxl
    wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]
    it = ws.iter_rows(values_only=True)
    hdr = next(it)
    H = {h: i for i, h in enumerate(hdr)}
    for row in it:
        if not row or row[H["Receipt Number"]] is None:
            continue
        yield {
            "receipt": str(row[H["Receipt Number"]]),
            "date": str(row[H["Date Created"]]),
            "status": row[H["Status"]],
            "rtype": row[H["Receipt Type"]],
            "name": (row[H["Customer Name"]] or "").strip().upper(),
            "total": money(row[H["Receipt Total"]]),
        }


def parse_date_epoch(d):
    # HLMyClub dates look like '6/19/2026'; stamp at local noon (17:00 UTC ~ CT midday)
    for fmt in ("%m/%d/%Y", "%-m/%-d/%Y", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(d, fmt).replace(hour=17, tzinfo=timezone.utc)
            return int(dt.timestamp())
        except ValueError:
            continue
    return None


def load_ledger(p):
    try:
        return set(json.load(open(p)))
    except Exception:
        return set()


def save_ledger(p, ids):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(sorted(ids), open(p, "w"))


def post_to_meta(pixel, token, events, test_code=None):
    payload = {"data": events}
    if test_code:
        payload["test_event_code"] = test_code
    body = json.dumps(payload).encode()
    url = f"https://graph.facebook.com/{META_API_VER}/{pixel}/events?access_token={urllib.parse.quote(token)}"
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return True, r.read().decode()
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}: {e.read().decode()[:400]}"
    except Exception as e:
        return False, str(e)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--receipts", default=None, help="Receipts export (default: newest 'Receipts*.xlsx' in ~/Downloads)")
    ap.add_argument("--customers", default=None, help="Customer Report CSV (default: newest 'Customer Report*.csv' in ~/Downloads)")
    ap.add_argument("--ledger", default=os.path.join(os.path.dirname(__file__), "data", "hl_sent.json"))
    ap.add_argument("--send", action="store_true", help="actually POST to Meta (default: dry-run)")
    args = ap.parse_args()

    cust_path = args.customers
    if not cust_path:
        import glob
        cands = sorted(glob.glob(os.path.join(DEFAULT_DL, "Customer Report*.csv")), key=os.path.getmtime)
        cust_path = cands[-1] if cands else None
    if not cust_path or not os.path.exists(cust_path):
        print("FATAL: no Customer Report CSV found"); sys.exit(1)

    receipts_path = args.receipts
    if not receipts_path:
        import glob
        cands = sorted(glob.glob(os.path.join(DEFAULT_DL, "Receipts*.xlsx")), key=os.path.getmtime)
        receipts_path = cands[-1] if cands else None
    if not receipts_path or not os.path.exists(receipts_path):
        print("FATAL: no Receipts*.xlsx found"); sys.exit(1)
    args.receipts = receipts_path

    enabled = args.send or os.environ.get("HL_FEED_ENABLED") == "1"
    pixel = os.environ.get("META_PIXEL_ID", "")
    token = os.environ.get("META_CAPI_TOKEN", "")
    test_code = os.environ.get("META_CAPI_TEST_CODE") or None

    print(f"contacts file : {os.path.basename(cust_path)}")
    print(f"receipts file : {os.path.basename(args.receipts)}")
    print(f"mode          : {'LIVE (will POST)' if enabled else 'DRY-RUN'}")

    contacts = load_contacts(cust_path)
    ledger = load_ledger(args.ledger)
    now = int(datetime.now(timezone.utc).timestamp())
    too_old = now - int(MAX_EVENT_AGE_DAYS * 86400)

    events, sent_ids = [], []
    n = matched = sent = 0
    skip_status = skip_nomatch = skip_old = skip_ledger = 0
    matched_val = old_val = 0.0

    for rc in load_receipts(args.receipts):
        n += 1
        if rc["status"] != "Accepted":
            skip_status += 1
            continue
        if rc["receipt"] in ledger:
            skip_ledger += 1
            continue
        c = contacts.get(rc["name"])
        if not c:
            skip_nomatch += 1
            continue
        matched += 1
        matched_val += rc["total"]
        ep = parse_date_epoch(rc["date"])
        if ep is None or ep < too_old:
            skip_old += 1
            old_val += rc["total"]
            continue
        ph, em = c
        ud = {}
        if em:
            ud["em"] = [sha256(em)]
        if ph and len(ph) >= 10:
            ud["ph"] = [sha256(ph)]
        if not ud:
            continue
        events.append({
            "event_name": "Purchase",
            "event_time": ep,
            "event_id": "hl-" + rc["receipt"],
            "action_source": "physical_store",
            "user_data": ud,
            "custom_data": {"currency": "USD", "value": round(rc["total"], 2), "order_id": rc["receipt"]},
        })
        sent_ids.append(rc["receipt"])

    print(f"\nreceipts={n} | skip_not_accepted={skip_status} | skip_no_contact_match={skip_nomatch} "
          f"| skip_already_sent={skip_ledger}")
    print(f"MATCHED to contact = {matched} (${matched_val:.2f})  <- attributable in-store revenue")
    print(f"  of which too old for Meta (>7d) = {skip_old} (${old_val:.2f})  -> export/run weekly to capture these")
    print(f"SENDABLE NOW = {len(events)} event(s)")
    by_day = {}
    for e in events:
        d = datetime.fromtimestamp(e["event_time"], timezone.utc).strftime("%m/%d")
        by_day[d] = by_day.get(d, 0) + 1
    if by_day:
        print("  sendable by day:", dict(sorted(by_day.items())))

    if not events:
        print("nothing sendable this run."); return
    if not enabled:
        print(f"\nDRY-RUN: would POST {len(events)} Purchase event(s) to pixel {pixel or '(META_PIXEL_ID unset)'}. Not sent.")
        return
    if not (pixel and token):
        print("FATAL: META_PIXEL_ID / META_CAPI_TOKEN required to send."); sys.exit(1)
    ok, resp = post_to_meta(pixel, token, events, test_code)
    if ok:
        ledger.update(sent_ids)
        save_ledger(args.ledger, ledger)
        print(f"SENT {len(events)} event(s). resp={resp[:200]}")
    else:
        print(f"META POST FAILED -> {resp}"); sys.exit(2)


if __name__ == "__main__":
    main()
