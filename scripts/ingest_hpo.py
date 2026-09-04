#!/usr/bin/env python3
"""Fetch HPO disease annotations and retain a small, reproducible seed set."""

import argparse
import json
from datetime import date
from pathlib import Path
from urllib.request import urlopen


URL = "https://purl.obolibrary.org/obo/hp/hpoa/phenotype.hpoa"
ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--omim", nargs="+", default=["104300", "125853", "168600"])
    args = parser.parse_args()
    wanted = {f"OMIM:{value}" for value in args.omim}
    text = urlopen(URL, timeout=60).read().decode("utf-8")
    rows = []
    version = None
    for line in text.splitlines():
        if line.startswith("#version:"):
            version = line.split(":", 1)[1].strip()
        if not line or line.startswith("#") or line.startswith("database_id"):
            continue
        fields = line.split("\t")
        if fields[0] in wanted:
            rows.append({
                "disease_id": fields[0], "disease_name": fields[1],
                "qualifier": fields[2] or None, "hpo_id": fields[3],
                "reference": fields[4], "evidence": fields[5],
                "onset": fields[6] or None, "frequency": fields[7] or None,
                "sex": fields[8] or None, "modifier": fields[9] or None,
                "aspect": fields[10], "biocuration": fields[11]
            })
    output = {
        "source": URL, "source_version": version, "retrieved": date.today().isoformat(),
        "disease_ids": sorted(wanted), "annotations": rows
    }
    path = ROOT / "data" / "phenotype-annotations.json"
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(f"ingested {len(rows)} HPO annotations for {len(wanted)} diseases (release {version})")


if __name__ == "__main__":
    main()
