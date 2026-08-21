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
