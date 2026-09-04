#!/usr/bin/env python3
"""Ingest human gene-function and pathway overview snapshots."""

import gzip
import hashlib
import json
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bulk"
GOA_URL = "https://current.geneontology.org/annotations/goa_human.gaf.gz"
REACTOME_URL = "https://reactome.org/ContentService/data/pathways/top/9606"
REACTOME_VERSION_URL = "https://reactome.org/ContentService/data/database/version"


def fetch(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "Terpedia-disease-data-sync/0.1"})
    with urlopen(request, timeout=180) as response:
        return response.read()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest_path = OUT / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {"retrieved": date.today().isoformat(), "sources": {}}
    manifest["retrieved"] = date.today().isoformat()

    goa_gz = fetch(GOA_URL)
    goa_raw = gzip.decompress(goa_gz)
    (OUT / "goa-human.gaf.gz").write_bytes(goa_gz)
    manifest["sources"]["gene-ontology-human"] = {
        "url": GOA_URL, "file": "data/bulk/goa-human.gaf.gz", "format": "GAF.gz",
        "bytes": len(goa_raw), "lines": goa_raw.count(b"\n"), "sha256": hashlib.sha256(goa_raw).hexdigest()
    }

    reactome = fetch(REACTOME_URL)
    pathways = json.loads(reactome)
    (OUT / "reactome-human-top-pathways.json").write_bytes(reactome + b"\n")
    version = fetch(REACTOME_VERSION_URL).decode().strip()
    manifest["sources"]["reactome-human"] = {
        "url": REACTOME_URL, "version_url": REACTOME_VERSION_URL,
        "reactome_release": version, "file": "data/bulk/reactome-human-top-pathways.json",
        "pathways": len(pathways), "bytes": len(reactome), "sha256": hashlib.sha256(reactome).hexdigest()
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"gene_ontology_annotations": goa_raw.count(b"\n"), "reactome_top_pathways": len(pathways), "reactome_release": version}, indent=2))


if __name__ == "__main__":
    main()
