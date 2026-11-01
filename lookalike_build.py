#!/usr/bin/env python3
"""
Build a Meta Custom Audience from HLMyClub club members + a 1% US lookalike.
Reads the Customer Report CSV (name -> phone/email), hashes PII, uploads to a
USER_PROVIDED_ONLY customer-list audience, then seeds a similarity lookalike.

Creds from env: META_ACCESS_TOKEN (ads_management), META_AD_ACCOUNT_ID (act_...).
Run with --go to actually create/upload (default: dry-run preview).
"""
import os, sys, csv, json, hashlib, argparse, urllib.request, urllib.parse, urllib.error

VER = "v19.0"
AUD_NAME = "NH Club Members (HLMyClub)"


def sha256(s):
    return hashlib.sha256(s.strip().lower().encode("utf-8")).hexdigest()


def digits(s):
    return "".join(ch for ch in str(s or "") if ch.isdigit())


def masked(v):
    v = str(v or "")
    return ("*" in v) or ("x" in v.lower())


def norm_phone(p):
    d = digits(p)
    if len(d) == 10:
        d = "1" + d
    return d if len(d) >= 11 else ""


def load_members(csv_path):
    rows = []
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            ph, em = r.get("Phone") or "", r.get("Email") or ""
            ph = norm_phone(ph) if (ph and not masked(ph)) else ""
            em = em.strip().lower() if (em and not masked(em)) else ""
            if ph or em:
                rows.append((em, ph))
    return rows


def api(method, path, token, params=None, data=None):
    url = f"https://graph.facebook.com/{VER}/{path}"
    body = None
    if data is not None:
        body = urllib.parse.urlencode(data).encode()
    elif params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return True, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return False, e.read().decode()[:500]
    except Exception as e:
        return False, str(e)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--customers", default=None)
    ap.add_argument("--go", action="store_true")
    args = ap.parse_args()

    cust = args.customers
    if not cust:
        import glob
        c = sorted(glob.glob(os.path.expanduser("~/Downloads/Customer Report*.csv")), key=os.path.getmtime)
        cust = c[-1] if c else None
    members = load_members(cust)
    token = os.environ.get("META_ACCESS_TOKEN", "")
    acct = os.environ.get("META_AD_ACCOUNT_ID", "")
    print(f"members file : {os.path.basename(cust)}")
    print(f"usable members (phone or email): {len(members)}")
    print(f"  with email: {sum(1 for e,p in members if e)} | with phone: {sum(1 for e,p in members if p)}")

    if not args.go:
        print("\nDRY-RUN: pass --go to create the audience + upload + build lookalike.")
        return
    if not (token and acct):
        print("FATAL: META_ACCESS_TOKEN / META_AD_ACCOUNT_ID required."); sys.exit(1)

    # 1. create (or reuse) the custom audience
    ok, existing = api("GET", f"{acct}/customaudiences", token, params={"fields": "id,name", "limit": 200})
    aud_id = None
    if ok:
        for a in existing.get("data", []):
            if a.get("name") == AUD_NAME:
                aud_id = a["id"]; print(f"reusing audience {aud_id}"); break
    if not aud_id:
        ok, res = api("POST", f"{acct}/customaudiences", token, data={
            "name": AUD_NAME,
            "subtype": "CUSTOM",
            "description": "Nutrition Hub club members from HLMyClub export (hashed).",
            "customer_file_source": "USER_PROVIDED_ONLY",
        })
        if not ok:
            print("FAILED to create audience:", res); sys.exit(2)
        aud_id = res["id"]; print(f"created audience {aud_id}")

    # 2. upload hashed users (schema EMAIL + PHONE, pre-hashed)
    data_rows = [[sha256(e) if e else "", sha256(p) if p else ""] for e, p in members]
    payload = {"schema": ["EMAIL", "PHONE"], "data": data_rows}
    ok, res = api("POST", f"{aud_id}/users", token, data={"payload": json.dumps(payload)})
    if not ok:
        print("FAILED to upload users:", res); sys.exit(2)
    print(f"uploaded users -> {json.dumps(res)}")

    # 3. seed 1% US lookalike
    ok, res = api("POST", f"{acct}/customaudiences", token, data={
        "name": "NH Club Members - Lookalike 1% US",
        "subtype": "LOOKALIKE",
        "origin_audience_id": aud_id,
        "lookalike_spec": json.dumps({"type": "similarity", "country": "US", "ratio": 0.01}),
    })
    if ok:
        print(f"created lookalike -> {res.get('id')}")
    else:
        print("lookalike not created (often needs ~100 matched users; audience still grows on weekly uploads):")
        print("  ", res)


if __name__ == "__main__":
    main()
