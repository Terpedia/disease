# Terpedia Disease

An evidence-first disease knowledge base and presentation layer for Terpedia.

This repository is intentionally designed to keep three things distinct:

1. **Disease entities** — stable identity, aliases, classifications, and plain-language descriptions.
2. **Evidence claims** — source-linked statements with an evidence type, population, and confidence.
3. **Presentation** — a readable public view that shows what is established, suggestive, or unknown.

The current catalog is a small, reviewable starter dataset. It is not a diagnostic tool and does not provide medical advice.

## Local development

Serve the repository with any static file server:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

Validate the catalog with:

```bash
python3 scripts/validate_catalog.py
```

## Data model

`data/disease-catalog.json` is the source of truth. Each disease has a stable `id`, a display name, aliases, a short overview, and an array of evidence claims. Claims must identify their evidence type and include a source URL. Confidence is deliberately categorical (`high`, `moderate`, `low`, or `uncertain`) so it can be displayed without implying unwarranted precision.

See [docs/data-model.md](docs/data-model.md) for contribution guidance.

## Scope and safeguards

- This project is for knowledge organization and public education, not diagnosis or treatment.
- Claims should be narrow, source-linked, and written so that limitations remain visible.
- Do not turn an association into a causal claim, or a graph relationship into clinical evidence.
- Preserve source dates and review status as the catalog grows.

## License

Code and original content are MIT licensed. External sources and datasets remain under their respective terms.
