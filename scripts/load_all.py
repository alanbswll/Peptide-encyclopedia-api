#!/usr/bin/env python3
"""
Load (or reload) every peptide in peptides_source/ into the API. Upserts —
creates a peptide if it doesn't exist yet, updates it if it does. This is
the "rebuild the database from git" command: wipe the DB, reseed lookup
tables, run this, and the encyclopedia is back exactly as it was.

Usage:
    python scripts/load_all.py
    python scripts/load_all.py --api-url https://your-service.onrender.com
"""
import argparse
import glob
import json
import os
import sys

import requests
import yaml

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--api-url", default=os.getenv("API_URL", "http://127.0.0.1:8000"))
    parser.add_argument(
        "--source-dir",
        default=os.path.join(os.path.dirname(__file__), "..", "peptides_source"),
    )
    args = parser.parse_args()

    admin_key = os.getenv("ADMIN_API_KEY")
    if not admin_key:
        sys.exit("ADMIN_API_KEY not set. Put it in your .env or export it before running this script.")
    headers = {"X-Admin-Key": admin_key, "Content-Type": "application/json"}

    files = sorted(
        f for f in glob.glob(os.path.join(args.source_dir, "*.yaml"))
        if not os.path.basename(f).startswith("_")  # skip _template.yaml
    )
    if not files:
        sys.exit(f"No peptide YAML files found in {args.source_dir}")

    ok, failed = 0, 0
    for path in files:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        pid = data.get("id")
        name = data.get("name", pid)
        if not pid:
            print(f"SKIP {path}: no 'id' field")
            failed += 1
            continue

        # Try create first; if it already exists, fall back to update.
        resp = requests.post(f"{args.api_url}/peptides", headers=headers, data=json.dumps(data))
        if resp.status_code == 409:
            resp = requests.put(f"{args.api_url}/peptides/{pid}", headers=headers, data=json.dumps(data))

        if resp.status_code >= 400:
            print(f"FAILED {pid} ({resp.status_code}): {resp.text}")
            failed += 1
            continue

        result = resp.json()
        print(f"OK {result['name']} ({result['id']}) -> {result['status']}")
        ok += 1

    print(f"\n{ok} loaded, {failed} failed, {len(files)} total.")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
