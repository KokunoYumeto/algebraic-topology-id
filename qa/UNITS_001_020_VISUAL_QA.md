# Units 001-020 cumulative visual QA

Status: **PASS** for the verified cumulative checkpoint.

The deterministic builder produced the same HTML bytes twice and the same PDF
bytes twice under Pandoc 3.9.0.2, `SOURCE_DATE_EPOCH=1787443200`, and the
unchanged Units 001-019 baseline builder. The final PDF is 237 A4 pages,
1,598,235 bytes, SHA-256
`30fdde6ddfc937df3e93bb59d58e72e593c87262d6a2535214113e5ebab64457`.

Representative rendered pages were inspected at 120 dpi with Poppler:

- page 1 (title and contents),
- page 119 (mid-reader proof and equations),
- pages 222, 224, 227, and 230 (Unit 20 entry, semantic figure tables,
  chain/cohomology material, and the Klein-bottle correction),
- page 237 (final page and deferred Unit 21 boundary).

All inspected pages had readable text, stable margins, no clipping or overlap,
and no raw positional TikZ/Xy-pic surface. Unit 20’s seven diagrams are
reader-first semantic descriptions/tables retaining labels and orientations.
This is representative visual QA, not a claim that every page was manually
inspected.

The HTML artifact has 1,030 unique DOM IDs (no duplicates), 7,944 MathML
nodes, 48 semantic figures, and 245 table-of-contents links; all 73 Unit 20
stable IDs survive the Pandoc parse. The model/process provenance note is
present in the reader text as `OpenAI Codex gpt-5.6-sol, Ultra` after normal
whitespace extraction.
