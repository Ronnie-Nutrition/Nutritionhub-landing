#!/usr/bin/env python3
"""
Square -> Meta CAPI blended-ROAS feed  (Nutrition Hub)
=====================================================
Pulls COMPLETED Square payments for the The Nutritional Hub location and pushes
them to the Meta pixel via the Conversions API as Purchase events, so that BOTH
in-store (Square Terminal/POS) AND any online Square channels get attributed to
the ad account -- the first time Meta sees true blended ROAS.

DEDUP (the important part)
--------------------------
The order.nutritionhub101.com site (server.js) ALREADY fires a realtime CAPI
Purchase for every order it processes. Those payments are created by the Square
application whose id == SQUARE_APP_ID (sq0idp-faZfw...). This feed SKIPS those so
they are never double-counted. Everything else -- Terminal device sales, cash,
and any other Square online channel -- is NOT otherwise attributed, so the feed
sends it.

Two layers of safety against re-sending: (1) a local ledger of payment ids we've
already pushed, and (2) a deterministic event_id ('sq-<payment_id>') so Meta
de-dups server-side even if a run overlaps.

STAGED OFF BY DEFAULT
---------------------
Set CAPI_FEED_ENABLED=1 in the environment to actually POST to Meta. With it
unset/0 the script does a full DRY RUN: it pulls, classifies, and logs exactly
what it WOULD send, but sends nothing. This lets us deploy + verify before the
Terminal is live, then flip it on once in-store sales start flowing.

Reads config from /opt/nutritionhub-menu/.env (same file the order site uses).
"""
import os, sys, json, time, hashlib, urllib.request, urllib.error, urllib.parse
from datetime import datetime, timedelta, timezone

# ── config ──────────────────────────────────────────────────────
ENV_PATH    = os.environ.get("CAPI_ENV_PATH", "/opt/nutritionhub-menu/.env")
DATA_DIR    = os.environ.get("CAPI_DATA_DIR", "/opt/nutritionhub-menu/data")
LEDGER_PATH = os.path.join(DATA_DIR, "capi_sent.json")
LOG_PATH    = os.path.join(DATA_DIR, "capi_feed.log")
LOOKBACK_HOURS = int(os.environ.get("CAPI_LOOKBACK_HOURS", "36"))
META_API_VER   = os.environ.get("CAPI_META_VER", "v19.0")
# Square applications whose payments must NOT be attributed to ads. Default:
# sq0idp-eWgeI2OSLAabneRPOcL87g = Herbalife's "Engage" ordering app. Existing
# customers (e.g. Lianny Sophia) log into Engage, which charges through Square
# and surfaces here noted "Herbalife - The Nutritional Hub". These are repeat
# app orders, NOT ad-driven foot traffic -- attributing them would inflate ROAS
# and skew the lookalike audience, so they're excluded.
EXCLUDE_APP_IDS = set(filter(None, os.environ.get(
    "CAPI_EXCLUDE_APP_IDS", "sq0idp-eWgeI2OSLAabneRPOcL87g").split(",")))
# Meta hard-rejects events whose event_time is older than 7 days; keep a margin.
MAX_EVENT_AGE_DAYS = 6.5


def load_env(path):
    """Read KEY=VALUE lines from the order-site .env without disturbing os.environ."""
    cfg = {}
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                cfg[k.strip()] = v.strip().strip('"').strip("'")
    # environment overrides file (lets cron flip flags without editing .env)
    cfg.update({k: v for k, v in os.environ.items() if k in cfg or k.startswith(("SQUARE_", "META_", "CAPI_"))})
    return cfg


def log(msg):
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    line = f"[{stamp}] {msg}"
    print(line)
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(LOG_PATH, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def sha256(s):
    return hashlib.sha256(s.strip().lower().encode("utf-8")).hexdigest()


def digits(s):
    return "".join(ch for ch in (s or "") if ch.isdigit())


def load_ledger():
    try:
        with open(LEDGER_PATH) as f:
            return set(json.load(f))
    except Exception:
        return set()


def save_ledger(ids):
    os.makedirs(DATA_DIR, exist_ok=True)
    tmp = LEDGER_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(sorted(ids), f)
    os.replace(tmp, LEDGER_PATH)


def square_get(host, path, token, version):
    req = urllib.request.Request(
        f"https://{host}{path}",
        headers={"Authorization": f"Bearer {token}", "Square-Version": version,
                 "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def list_payments(host, token, version, location_id, begin_iso):
    """Yield all COMPLETED payments since begin_iso (paginated)."""
    cursor = None
    while True:
        qs = (f"/v2/payments?location_id={location_id}&sort_order=DESC"
              f"&begin_time={begin_iso}&limit=100")
        if cursor:
            qs += f"&cursor={urllib.parse.quote(cursor)}"
        data = square_get(host, qs, token, version)
        for p in data.get("payments", []):
            yield p
        cursor = data.get("cursor")
        if not cursor:
            break


def to_epoch(iso):
    # Square returns RFC3339 like 2026-06-18T19:06:29.621Z
    return int(datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp())


def build_event(p):
    """Return a Meta CAPI event dict for a payment, or None if unmatchable."""
    email = (p.get("buyer_email_address") or "").strip()
    # Square sometimes carries a phone on the billing address of the card.
    phone = ""
    cd = (p.get("card_details") or {}).get("card", {}) or {}
    ba = cd.get("billing_address") or {}
    # (Square rarely populates phone on payments; receipt opt-in is the main source.)
    phone = digits(ba.get("phone") or p.get("buyer_phone_number") or "")

    user_data = {}
    if email:
        user_data["em"] = [sha256(email)]
    if phone and len(phone) >= 10:
        user_data["ph"] = [sha256(phone)]
    if not user_data:
        return None  # Meta requires >=1 user identifier; can't match this one.

    in_store = bool(p.get("device_details"))
    amt = (p.get("amount_money") or {}).get("amount", 0) / 100.0
    return {
        "event_name": "Purchase",
        "event_time": to_epoch(p["created_at"]),
        "event_id": "sq-" + p["id"],
        "action_source": "physical_store" if in_store else "website",
        "user_data": user_data,
        "custom_data": {
            "currency": (p.get("amount_money") or {}).get("currency", "USD"),
            "value": round(amt, 2),
            "order_id": p["id"],
        },
    }


def post_to_meta(pixel_id, token, events, test_code=None):
    payload = {"data": events}
    if test_code:
        payload["test_event_code"] = test_code
    body = json.dumps(payload).encode()
    url = f"https://graph.facebook.com/{META_API_VER}/{pixel_id}/events?access_token={urllib.parse.quote(token)}"
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return True, r.read().decode()
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}: {e.read().decode()[:400]}"
    except Exception as e:
        return False, str(e)


def main():
    cfg = load_env(ENV_PATH)
    token   = cfg.get("SQUARE_ACCESS_TOKEN", "")
    version = cfg.get("SQUARE_VERSION", "2025-05-21")
    loc     = cfg.get("SQUARE_LOCATION_ID", "")
    site_app = cfg.get("SQUARE_APP_ID", "")  # order-site app -> already CAPI'd
    sq_env  = (cfg.get("SQUARE_ENV", "sandbox")).lower()
    host    = "connect.squareup.com" if sq_env == "production" else "connect.squareupsandbox.com"
    pixel   = cfg.get("META_PIXEL_ID", "")
    capi_tok = cfg.get("META_CAPI_TOKEN", "")
    test_code = cfg.get("META_CAPI_TEST_CODE", "") or None
    enabled = cfg.get("CAPI_FEED_ENABLED", "0") == "1"

    if not (token and loc and pixel and capi_tok):
        log("FATAL: missing SQUARE_ACCESS_TOKEN / SQUARE_LOCATION_ID / META_PIXEL_ID / META_CAPI_TOKEN")
        sys.exit(1)

    mode = "LIVE" if enabled else "DRY-RUN (set CAPI_FEED_ENABLED=1 to send)"
    begin = (datetime.now(timezone.utc) - timedelta(hours=LOOKBACK_HOURS))
    begin_iso = begin.strftime("%Y-%m-%dT%H:%M:%SZ")
    now_epoch = int(datetime.now(timezone.utc).timestamp())
    too_old_before = now_epoch - int(MAX_EVENT_AGE_DAYS * 86400)

    log(f"=== Square->Meta CAPI feed | mode={mode} | lookback={LOOKBACK_HOURS}h | loc={loc} ===")

    ledger = load_ledger()
    events, sent_ids = [], []
    n_total = n_skip_site = n_skip_ledger = n_skip_nopii = n_skip_old = n_skip_status = n_skip_excl = 0
    unmatched_value = 0.0

    for p in list_payments(host, token, version, loc, begin_iso):
        n_total += 1
        if p.get("status") != "COMPLETED":
            n_skip_status += 1
            continue
        pid = p["id"]
        if pid in ledger:
            n_skip_ledger += 1
            continue
        app_id = (p.get("application_details") or {}).get("application_id", "")
        if app_id and app_id == site_app:
            n_skip_site += 1  # order-site already fired realtime CAPI
            continue
        if app_id and app_id in EXCLUDE_APP_IDS:
            n_skip_excl += 1  # recurring card-on-file channel -- not ad-driven
            continue
        if to_epoch(p["created_at"]) < too_old_before:
            n_skip_old += 1
            continue
        ev = build_event(p)
        if ev is None:
            n_skip_nopii += 1
            unmatched_value += (p.get("amount_money") or {}).get("amount", 0) / 100.0
            continue
        events.append(ev)
        sent_ids.append(pid)

    log(f"pulled={n_total} | skip_order_site={n_skip_site} | skip_recurring_excluded={n_skip_excl} | "
        f"skip_already_sent={n_skip_ledger} | skip_non_completed={n_skip_status} | "
        f"skip_too_old={n_skip_old} | skip_no_PII={n_skip_nopii} (${unmatched_value:.2f} unmatchable) | "
        f"TO_SEND={len(events)}")

    for ev in events:
        src = ev["action_source"]
        log(f"  -> {src:14s} ${ev['custom_data']['value']:.2f}  event_id={ev['event_id']}  "
            f"keys={'+'.join(ev['user_data'].keys())}")

    if not events:
        log("nothing to send this run.")
        return

    if not enabled:
        log(f"DRY-RUN: would POST {len(events)} event(s) to pixel {pixel}. Not sent.")
        return

    ok, resp = post_to_meta(pixel, capi_tok, events, test_code)
    if ok:
        ledger.update(sent_ids)
        save_ledger(ledger)
        log(f"SENT {len(events)} event(s) to Meta. resp={resp[:200]}")
    else:
        log(f"META POST FAILED -> {resp}")
        sys.exit(2)


if __name__ == "__main__":
    main()
