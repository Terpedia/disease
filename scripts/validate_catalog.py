#!/usr/bin/env python3
"""Validate the disease catalog's structural and provenance requirements."""

import json
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "disease-catalog.json"
CONFIDENCE = {"high", "moderate", "low", "uncertain"}
STATUSES = {"draft", "reviewed", "published"}
REVIEW_STATUSES = {"needs-review", "in-review", "approved"}


def fail(message: str) -> None:
    raise SystemExit(f"catalog validation failed: {message}")


def main() -> None:
    try:
        catalog = json.loads(CATALOG.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        fail(str(exc))

    diseases = catalog.get("diseases")
    if not isinstance(diseases, list) or not diseases:
        fail("diseases must be a non-empty list")

    ids = set()
    claim_ids = set()
    for disease in diseases:
        for field in ("id", "name", "overview", "status", "claims"):
            if field not in disease:
                fail(f"{disease.get('id', '<unknown>')} is missing {field}")
        if disease["id"] in ids:
            fail(f"duplicate disease id: {disease['id']}")
        ids.add(disease["id"])
        if disease["status"] not in STATUSES:
            fail(f"invalid disease status: {disease['id']}")
        for claim in disease["claims"]:
            for field in ("id", "statement", "evidence_type", "confidence", "source", "review_status"):
                if field not in claim:
                    fail(f"{disease['id']} claim is missing {field}")
            if claim["id"] in claim_ids:
                fail(f"duplicate claim id: {claim['id']}")
            claim_ids.add(claim["id"])
            if claim["confidence"] not in CONFIDENCE:
                fail(f"invalid confidence: {claim['id']}")
            if claim["review_status"] not in REVIEW_STATUSES:
                fail(f"invalid review status: {claim['id']}")
            url = claim["source"].get("url", "")
            if urlparse(url).scheme not in {"http", "https"}:
                fail(f"source URL must be http(s): {claim['id']}")

    print(f"validated {len(diseases)} disease(s) and {len(claim_ids)} claim(s)")


if __name__ == "__main__":
    main()
