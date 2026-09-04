# Data model

The catalog uses stable IDs so the presentation can evolve without breaking links or citations.

## Disease entity

- `id`: lowercase, URL-safe identifier that does not change when copy or display names change.
- `name`: preferred display name.
- `aliases`: alternate names or abbreviations; keep these discoverable but do not use them as IDs.
- `classification`: broad category, when useful and well-supported.
- `overview`: short reader-facing orientation, not a clinical definition.
- `status`: `draft`, `reviewed`, or `published`.
- `claims`: source-linked evidence statements about the entity.

## Evidence claim

- `statement`: one checkable assertion; avoid bundling multiple findings.
- `evidence_type`: for example `guideline`, `systematic-review`, `observational`, `trial`, or `editorial`.
- `confidence`: `high`, `moderate`, `low`, or `uncertain`; this is a communication label, not a statistical estimate.
- `source.title` and `source.url`: enough information for a reader to inspect the source.
- `review_status`: `needs-review`, `in-review`, or `approved`.

When adding a disease, start with identity and provenance. Add claims only after checking the source directly, and state important population, outcome, and time-window limitations in the claim or its supporting notes.
