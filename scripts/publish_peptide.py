#!/usr/bin/env python3
"""
Flip a peptide's status. Defaults to publishing; --draft reverts it to draft
(e.g. to pull a peptide back for edits without deleting it).

Usage:
    python scripts/publish_peptide.py bpc-157
    python scripts/publish_peptide.py bpc-157 --draft
    python scripts/publish_peptide.py bpc-157 --api-url https://your-service.onrender.com
"""
import argparse
import os
import sys

import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("peptide_id")
    parser.add_argument("--draft", action="store_true", help="Set back to draft instead of publishing")
    parser.add_argument("--api-url", default=os.getenv("API_URL", "http://127.0.0.1:8000"))
    args = parser.parse_args()

    admin_key = os.getenv("ADMIN_API_KEY")
    if not admin_key:
        sys.exit("ADMIN_API_KEY not set. Put it in your .env or export it before running this script.")

    status = "draft" if args.draft else "published"
    url = f"{args.api_url}/peptides/{args.peptide_id}/status"
    resp = requests.patch(
        url,
        headers={"X-Admin-Key": admin_key, "Content-Type": "application/json"},
        json={"status": status},
    )

    if resp.status_code >= 400:
        print(f"FAILED ({resp.status_code}): {resp.text}", file=sys.stderr)
        sys.exit(1)

    result = resp.json()
    print(f"OK — {result['name']} ({result['id']}) is now status: {result['status']}")


if __name__ == "__main__":
    main()
