#!/usr/bin/env python3
"""
Push a single peptide YAML file to the encyclopedia API as a draft.

Usage:
    python scripts/add_peptide.py peptides_source/ipamorelin.yaml
    python scripts/add_peptide.py peptides_source/ipamorelin.yaml --update   # PUT instead of POST
    python scripts/add_peptide.py peptides_source/ipamorelin.yaml --api-url https://your-service.onrender.com

Reads ADMIN_API_KEY from the environment (or a local .env file via python-dotenv).
New peptides always land as status: draft — review them (GET /peptides/{id} or
the /docs Swagger UI) before publishing with publish_peptide.py.
"""
import argparse
import os
import sys
import json

import requests
import yaml

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("yaml_file", help="Path to a peptide YAML file")
    parser.add_argument("--update", action="store_true", help="PUT to an existing peptide instead of creating one")
    parser.add_argument("--api-url", default=os.getenv("API_URL", "http://127.0.0.1:8000"), help="Base API URL")
    args = parser.parse_args()

    admin_key = os.getenv("ADMIN_API_KEY")
    if not admin_key:
        sys.exit("ADMIN_API_KEY not set. Put it in your .env or export it before running this script.")

    with open(args.yaml_file, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    headers = {"X-Admin-Key": admin_key, "Content-Type": "application/json"}

    if args.update:
        peptide_id = data.get("id")
        if not peptide_id:
            sys.exit("--update requires an 'id' field in the YAML.")
        url = f"{args.api_url}/peptides/{peptide_id}"
        resp = requests.put(url, headers=headers, data=json.dumps(data))
    else:
        url = f"{args.api_url}/peptides"
        resp = requests.post(url, headers=headers, data=json.dumps(data))

    if resp.status_code >= 400:
        print(f"FAILED ({resp.status_code}):", file=sys.stderr)
        print(json.dumps(resp.json(), indent=2), file=sys.stderr)
        sys.exit(1)

    result = resp.json()
    print(f"OK — {result['name']} ({result['id']}) is now status: {result['status']}")
    print(f"Review at: {args.api_url}/peptides/{result['id']}")
    if result["status"] == "draft":
        print(f"When ready: python scripts/publish_peptide.py {result['id']}")


if __name__ == "__main__":
    main()
