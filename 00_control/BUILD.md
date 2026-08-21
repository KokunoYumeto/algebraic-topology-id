# Build record

## Frozen upstream baseline

Input: exact `Notes.tex` at SHA-256 `cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7`.

Toolchain: MiKTeX 26.5, pdfTeX 1.40.29, LaTeX2e 2025-11-01. Two-pass builds used `SOURCE_DATE_EPOCH=1586154268` and `FORCE_SOURCE_DATE=1`. Two independent output directories produced byte-identical 119-page PDFs: 759,694 bytes, SHA-256 `933abb8920e4f8959d8c1b444b182d121efc860e7c0b8bdb32023974b1f51a76`.

Baseline caveats: 59 overfull boxes (six above 100 pt), two underfull boxes, 225 Tufte margin-note moves, untagged PDF, and no HTML/EPUB.

## Indonesian Unit 001

Canonical semantic source: `source/id-ID/reader-unit-001.md`.

Build command:

```powershell
powershell -NoProfile -File scripts/build-unit-001.ps1
```

Pinned builder inputs:

- Pandoc 3.9.0.2
- MiKTeX pdfLaTeX
- `SOURCE_DATE_EPOCH=1787270400`
- `FORCE_SOURCE_DATE=1`
- MathML HTML with embedded CSS and no runtime JavaScript

The script builds the PDF twice, requires byte-identical SHA-256, removes its temporary duplicate PDFs, and writes `output/ARTIFACT_MANIFEST.csv`. HTML is the primary accessibility surface; the PDF is intentionally disclosed as untagged until a tagged-PDF toolchain is admitted.

Final Unit 001 artifacts:

- HTML: 85,580 bytes; SHA-256 `5cc4a29f2c29b274328b574d6698a51d75af0939f9959937db8d679c38ad51b8`.
- PDF: 321,743 bytes; 5 A4 pages; SHA-256 `6f71546a616c02ef81f8747ecfce3875784842065fc131cc82e5060b066a59c9`.
- Manifest: 228 bytes; SHA-256 `13772b2e2400923351225f422effe5f958e1dd8e178b9f6a32207682f791bcc3`.

Strict checks:

```powershell
python scripts/qa-unit-001.py
python scripts/validate-backend.py
```

The first command verifies the authority bytes, source span and structure, 29 stable IDs, exercise/solution closure, exact source correction, 259 MathML nodes, local fragments, offline/privacy properties, PDF metadata/text/fonts, and artifact manifest. The second validates the 139-record locale-neutral graph, canonical JSONL, every reference, source-span and artifact hash, rights separation, and exercise/solution relation. All 5 PDF pages were rendered at 120 dpi and inspected twice.

## Indonesian cumulative Units 001–002

Canonical semantic sources:

- `source/id-ID/reader-unit-001.md`: 16,179 bytes; SHA-256 `c80b51c22a2fa7ea116201028b78d5f8d708ef4d8355d34092ac7a9c88415e15`.
- `source/id-ID/units/unit-002-lecture-002.md`: 25,090 bytes; SHA-256 `4d2acc43557db9b3c419ee177545d285b9fcf50b2aa2dd3b2c6c44182f3a6a01`.

Build and QA:

```powershell
powershell -NoProfile -File scripts/build-units-001-002.ps1
python scripts/qa-units-001-002.py
python scripts/validate-backend.py
```

The cumulative builder first requires the exact frozen Unit 1 source and artifacts, removes each unit's YAML header in a temporary assembly, adds one cumulative metadata header, and uses the same pinned Pandoc/MiKTeX/fixed-epoch toolchain. It writes only new cumulative artifacts, builds the PDF twice, requires byte identity, and removes its exact temporary assembly and duplicate PDFs.

Final cumulative artifacts:

- HTML: 220,035 bytes; SHA-256 `d3b5cbfaa3511823821ecf9ba26a4eaec7c84d937417927d11bde3f66abc9f54`.
- PDF: 395,385 bytes; 15 A4 pages; SHA-256 `0413c3a3280955cc482a5c0c2d7615b78128dccba3b6b1901dee1bf34d133b8e`.
- Manifest: 247 bytes; SHA-256 `93e98f6cbbc60775bb934df5b49141f63d7cd2c76582a26c61d4192ff320d721`.
- QA receipt: 2,690 bytes; SHA-256 `075546f6a856638dc420ed62b23ec78c7a57f839444e4f2101233d6421f776f0`.

Strict QA binds 70 stable IDs, 43 semantic blocks, all nine exercise–solution pairs, the Unit 2 question–answer pair, seven disclosed source corrections, 621 native MathML nodes, all fragments, offline/privacy properties, PDF metadata/text/fonts, and both cumulative manifest rows. All 15 physical PDF pages were rendered and manually inspected; the HTML was also checked in Chromium at 1280×720 and 390×844 for centering, reflow, local formula scrolling, and page-level overflow. P1/P2/P3 are zero. The frozen Unit 1 HTML and PDF remain byte-identical.

The cumulative locale-neutral backend contains 315 canonical records in 11 JSONL files and validates with bundle SHA-256 `f1999b5d33466ba9a15a32f50a16173fbb7659f1a7b28a3452bc5d2ec3094e6e`. It maps the exact union of all 70 stable IDs one-to-one to units and segments, closes all nine exercise–solution relations plus the Unit 2 question–answer relation, and binds every source, rights, correction, QA, and artifact reference.
