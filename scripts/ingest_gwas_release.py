#!/usr/bin/env python3
"""Download the official ontology-annotated GWAS Catalog bulk release."""

import hashlib
import json
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bulk"
URL = "https://ftp.ebi.ac.uk/pub/databases/gwas/releases/latest/gwas-catalog-associations_ontology-annotated-full.zip"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    request = Request(URL, headers={"User-Agent": "Terpedia-disease-data-sync/0.1"})
    with urlopen(request, timeout=600) as response:
        payload = response.read()
    filename = OUT / "gwas-catalog-associations-ontology-annotated-full.zip"
    filename.write_bytes(payload)
    with ZipFile(filename) as archive:
        members = [{"name": item.filename, "bytes": item.file_size} for item in archive.infolist()]
    manifest_path = OUT / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {"sources": {}}
    manifest["retrieved"] = date.today().isoformat()
    manifest["sources"]["gwas-catalog-full"] = {
        "url": URL, "file": str(filename.relative_to(ROOT)), "format": "ZIP",
        "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest(), "members": members
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"file": str(filename), "bytes": len(payload), "members": members}, indent=2))


if __name__ == "__main__":
    main()
