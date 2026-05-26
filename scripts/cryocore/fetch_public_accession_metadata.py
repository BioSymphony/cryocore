#!/usr/bin/env python3
"""Build public accession metadata ledgers without downloading heavy data."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


def normalize_empiar(value: str) -> str:
    return value.upper().removeprefix("EMPIAR-")


def normalize_emdb(value: str) -> str:
    value = value.upper()
    if value.startswith("EMD-"):
        return value
    return f"EMD-{value}"


def normalize_pdb(value: str) -> str:
    return value.upper()


def validation_report_urls(pdb_id: str) -> list[str]:
    lower = pdb_id.lower()
    shard = lower[1:3]
    base = f"https://files.wwpdb.org/pub/pdb/validation_reports/{shard}/{lower}"
    return [
        f"{base}/{lower}_validation.xml.gz",
        f"{base}/{lower}_full_validation.pdf.gz",
    ]


def endpoint_plan(empiar: list[str], emdb: list[str], pdb: list[str]) -> list[str]:
    endpoints: list[str] = []
    for accession in empiar:
        endpoints.append(f"https://www.ebi.ac.uk/empiar/api/entry/{normalize_empiar(accession)}")
    for accession in emdb:
        emdb_id = normalize_emdb(accession)
        endpoints.extend(
            [
                f"https://www.ebi.ac.uk/emdb/api/entry/{emdb_id}",
                f"https://www.ebi.ac.uk/emdb/api/entry/map/{emdb_id}",
                f"https://www.ebi.ac.uk/emdb/api/entry/fitted/{emdb_id}",
                f"https://www.ebi.ac.uk/emdb/api/analysis/{emdb_id}",
                f"https://www.ebi.ac.uk/emdb/api/annotations/{emdb_id}",
            ]
        )
    for accession in pdb:
        endpoints.append(f"https://data.rcsb.org/rest/v1/core/entry/{normalize_pdb(accession)}")
    return endpoints


def fetch_endpoint(url: str, timeout: float) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "CryoCore-public-metadata/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read()
            content_type = response.headers.get("content-type", "")
            record: dict[str, Any] = {
                "url": url,
                "status": response.status,
                "content_type": content_type,
                "byte_count": len(body),
                "sha256": hashlib.sha256(body).hexdigest(),
            }
            if "json" in content_type.lower():
                try:
                    parsed = json.loads(body.decode("utf-8"))
                    if isinstance(parsed, dict):
                        record["json_top_level_keys"] = sorted(parsed.keys())[:50]
                except (UnicodeDecodeError, json.JSONDecodeError):
                    record["json_parse_error"] = True
            return record
    except urllib.error.HTTPError as exc:
        return {
            "url": url,
            "status": exc.code,
            "error": str(exc),
        }
    except urllib.error.URLError as exc:
        return {
            "url": url,
            "status": None,
            "error": str(exc.reason),
        }


def build_ledger(args: argparse.Namespace) -> dict[str, Any]:
    empiar = [normalize_empiar(item) for item in args.empiar]
    emdb = [normalize_emdb(item) for item in args.emdb]
    pdb = [normalize_pdb(item) for item in args.pdb]
    endpoints = endpoint_plan(empiar, emdb, pdb)
    report_urls = [url for accession in pdb for url in validation_report_urls(accession)]
    responses = [fetch_endpoint(url, args.timeout) for url in endpoints] if args.fetch else []

    return {
        "schema_version": 1,
        "retrieved_at": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"),
        "raw_data_download_required": False,
        "accessions": {
            "empiar": [f"EMPIAR-{item}" for item in empiar],
            "emdb": emdb,
            "pdb": pdb,
        },
        "source_api_endpoints": endpoints,
        "linked_accessions": [*([f"EMPIAR-{item}" for item in empiar]), *emdb, *pdb],
        "validation_report_urls": report_urls,
        "api_response_sha256": {
            response["url"]: response["sha256"]
            for response in responses
            if "sha256" in response
        },
        "responses": responses,
        "fetch_performed": bool(args.fetch),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--empiar", action="append", default=[], help="EMPIAR ID, with or without EMPIAR- prefix")
    parser.add_argument("--emdb", action="append", default=[], help="EMDB ID, with or without EMD- prefix")
    parser.add_argument("--pdb", action="append", default=[], help="PDB ID")
    parser.add_argument("--fetch", action="store_true", help="Fetch metadata endpoints and record response hashes")
    parser.add_argument("--timeout", type=float, default=20.0, help="Per-request timeout in seconds")
    parser.add_argument("--out", type=Path, help="Output JSON path; stdout when omitted")
    args = parser.parse_args()

    ledger = build_ledger(args)
    output = json.dumps(ledger, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output)
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
