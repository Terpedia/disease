#!/usr/bin/env python3
"""Bulk-ingest compact, public disease relationship snapshots."""

import gzip
import hashlib
import json
from datetime import date
from pathlib import Path
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bulk"
HPO_URL = "https://purl.obolibrary.org/obo/hp/hpoa/phenotype.hpoa"
CLINVAR_URLS = {
    "disease_names.tsv": "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/disease_names",
    "gene_condition_source_id.tsv": "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/gene_condition_source_id",
}


def fetch(url: str) -> bytes:
    with urlopen(url, timeout=180) as response:
        return response.read()


def write_gzip(name: str, payload: bytes) -> dict:
    path = OUT / f"{name}.gz"
    path.write_bytes(gzip.compress(payload, compresslevel=9, mtime=0))
    return {"file": str(path.relative_to(ROOT)), "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}


def ingest_hpo(manifest: dict) -> None:
    raw = fetch(HPO_URL).decode("utf-8")
    rows = []
    release = None
    for line in raw.splitlines():
        if line.startswith("#version:"):
            release = line.split(":", 1)[1].strip()
        if not line or line.startswith("#") or line.startswith("database_id"):
            continue
        fields = line.split("\t")
        rows.append({
            "disease_id": fields[0], "disease_name": fields[1], "qualifier": fields[2] or None,
            "hpo_id": fields[3], "reference": fields[4], "evidence": fields[5],
            "onset": fields[6] or None, "frequency": fields[7] or None,
            "sex": fields[8] or None, "modifier": fields[9] or None,
            "aspect": fields[10], "biocuration": fields[11]
        })
    payload = ("\n".join(json.dumps(row, separators=(",", ":")) for row in rows) + "\n").encode()
    manifest["hpo"] = {"url": HPO_URL, "release": release, "rows": len(rows), **write_gzip("hpo-phenotype-annotations.jsonl", payload)}


def ingest_clinvar(manifest: dict) -> None:
    for name, url in CLINVAR_URLS.items():
        payload = fetch(url)
        manifest[name] = {"url": url, **write_gzip(name, payload), "lines": payload.count(b"\n")}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {"retrieved": date.today().isoformat(), "sources": {}}
    ingest_hpo(manifest["sources"])
    ingest_clinvar(manifest["sources"])
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
