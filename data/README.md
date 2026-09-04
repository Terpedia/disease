# Data directory

- `disease-catalog.json` is the reader-facing catalog used by the site.
- `disease-records.json` is the structured research layer for disease biology.
- `phenotype-annotations.json` is generated from the current HPO disease annotation release and contains only the requested seed diseases.
- `source-registry.json` records upstream sources, release dates, and intended use.
- `bulk/` contains compressed JSONL/TSV snapshots produced by `scripts/ingest_bulk.py` plus a checksum manifest.

Generated files should retain their upstream version and retrieval date. Never overwrite a source file without updating its provenance metadata.
