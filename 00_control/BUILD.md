# Build record

## Frozen upstream baseline

Input: exact `Notes.tex` at SHA-256 `cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7`.

Toolchain: MiKTeX 26.5, pdfTeX 1.40.29, LaTeX2e 2025-11-01. Two-pass builds used `SOURCE_DATE_EPOCH=1586154268` and `FORCE_SOURCE_DATE=1`. Two independent output directories produced byte-identical 119-page PDFs: 759,694 bytes, SHA-256 `933abb8920e4f8959d8c1b444b182d121efc860e7c0b8bdb32023974b1f51a76`.

Baseline caveats: 59 overfull boxes (six above 100 pt), two underfull boxes, 225 Tufte margin-note moves, untagged PDF, and no HTML/EPUB.

## Indonesian Unit 001

Canonical semantic source: `source/id-ID/reader-unit-001.md`.

Build command:

```powershell
pwsh -NoProfile -File scripts/build-unit-001.ps1
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
pwsh -NoProfile -File scripts/build-units-001-002.ps1
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

## Indonesian cumulative Units 001-003

Canonical semantic sources:

- `source/id-ID/reader-unit-001.md`: 16,179 bytes; SHA-256 `c80b51c22a2fa7ea116201028b78d5f8d708ef4d8355d34092ac7a9c88415e15`.
- `source/id-ID/units/unit-002-lecture-002.md`: 25,090 bytes; SHA-256 `4d2acc43557db9b3c419ee177545d285b9fcf50b2aa2dd3b2c6c44182f3a6a01`.
- `source/id-ID/units/unit-003-lecture-003.md`: 25,822 bytes; SHA-256 `993e5941895a9b6f4b197b4c236f5a4990f6ae621e2bb7911353b28a5e1abffd`.

Build and QA:

```powershell
pwsh -NoProfile -File scripts/build-units-001-003.ps1
python scripts/qa-units-001-003.py
python scripts/validate-backend.py
```

The cumulative builder requires the exact frozen Unit 1, Units 1-2, all three source files, and embedded cumulative CSS before writing only the new Units 1-3 paths. It removes unit YAML headers in a temporary assembly, applies `SOURCE_DATE_EPOCH=1787356800`, builds the PDF twice, requires byte identity, and removes the exact temporary assembly and duplicate PDF.

Final cumulative artifacts and witnesses:

- HTML: 359,397 bytes; SHA-256 `33281cc46faa3d560c968b657526cd914786c991d1475b5563911a265bd316c1`.
- PDF: 460,320 bytes; 25 A4 pages; SHA-256 `2c9bf67e74c94bca9aad0238e910816188a957892a6cf811f7f615e221b4066d`.
- Manifest: 247 bytes; SHA-256 `1e211afb4b165435ece5f72a2b4e9b084975db35d111127880255473302f5049`.
- QA receipt: 3,983 bytes; SHA-256 `fb511086669846b6c8a68a6c1fecc4bd774016a6c95eb27219e3babbd177a873`.
- Extracted-text witness: 71,549 bytes; SHA-256 `2e8eabce2e0b8c3114b49d630187a6a0217e3ae90c466b5441f9eedccb299702`.
- Independent Unit 3 review: 2,464 bytes; SHA-256 `b2cffbcc2167c3d620f1af53224cc064e8ce34400561868339e69c280845619c`.
- Visual/browser receipt: 2,310 bytes; SHA-256 `4d7d603c2276bd570e3bf47897c67d98bf6507d2bd9ffed2acd10ab1a509130e`.

Strict QA binds 109 stable IDs, 68 semantic blocks, all 14 exercise-solution pairs, the Unit 2 question-answer pair, ten Unit 3 source corrections, four Unit 3 accessibility reflows, 1007 native MathML nodes, all fragments, offline/privacy properties, PDF metadata/text/fonts, and both cumulative manifest rows. All 25 physical PDF pages were rendered and inspected. The HTML was checked in the Codex in-app Chromium browser at 1280 x 720 and 390 x 844 for centering, reflow, formula-local scrolling, page-level overflow, fragment closure, and console errors. P1/P2/P3 are zero. Unit 1 and Units 1-2 artifacts remain byte-identical.

The cumulative locale-neutral backend contains 496 canonical records in 11 JSONL files and validates with bundle SHA-256 `0c08bebf7cbac289e94a7de571d3c2bab4d161c8a6a75c35b8a997f07ff6c939`. It maps the exact union of all 109 stable IDs one-to-one to units and segments, closes every exercise-solution and question-answer relation, records all 24 corrections/reflows, and binds every current source, rights, QA, and artifact reference.

## Indonesian cumulative Units 001-004

Canonical Unit 004 source:

- `source/id-ID/units/unit-004-lecture-004.md`: 24,582 bytes; 632 lines; 33 unique stable IDs; SHA-256 `826fcb368275cdad02f72a5cec951fc8466ba68b09ca0139d72c81a4c5591fea`.
- Exact authority span: frozen `Notes.tex:878-1131`; the Lecture 5 marker and proof of the terminal proposition begin at lines 1132-1134 and remain outside this boundary.

Build and QA:

```powershell
pwsh -NoProfile -File scripts/build-units-001-004.ps1
python scripts/qa-units-001-004.py
python scripts/validate-backend.py
```

The cumulative builder freezes every earlier source and public artifact, writes only the new Units 1-4 paths, uses Pandoc 3.9.0.2 with `SOURCE_DATE_EPOCH=1787356800`, and requires two PDF builds to be byte-identical.

Final cumulative artifacts and witnesses:

- HTML: 494,732 bytes; SHA-256 `8c8f5e1ad8172a2d97e3931fc3b4f2a3aa7f9e8a709260a27103f7eca0f1357d`.
- PDF: 539,006 bytes; 35 A4 pages; SHA-256 `5e92c4c6ed60bca9f2f4d362d4c48b4f01aa156b330e2adacd1bf88dd7de9e87`.
- Manifest: 247 bytes; SHA-256 `4c8bf407e426feb8db92308c4b28bdbbc0738416a85a13539ef7915e4c1aad83`.
- QA receipt: 4,478 bytes; SHA-256 `1670bbe2377712c9f96b9a68cdb75589ae461512f77cea7ad0c9290193724bd5`.
- Extracted-text witness: 100,684 bytes; SHA-256 `3d27bc1ab5a780bffce12d5951623b60929069238a210961740234502e71bf35`.
- Independent Unit 4 review: 3,031 bytes; SHA-256 `ac993a10e22738197775ae5c3f4e72948983c4e99ff602a52943b40ed417b6f9`.
- Visual/browser receipt: 2,257 bytes; SHA-256 `74e609e94ea47b89db223c21e12cae682048f0a60d8780dae96d5b0164f2c5ca`.

Strict QA binds 142 stable IDs and 88 fenced semantic blocks; all 18 exercise-solution pairs and both question-answer pairs; 18 Unit 4 source corrections/clarifications plus one accessibility reflow; 1,384 native MathML nodes; all 54 local fragments; offline/privacy properties; PDF metadata, fonts, text, and pages; and both manifest rows. All 35 PDF pages and the HTML at 1280 x 720 and 390 x 844 passed visual inspection. Fourteen wide phone-width formulas all scroll locally without widening the page. P1/P2/P3 are zero, and every earlier publication boundary remains byte-identical.

The cumulative locale-neutral backend contains 638 canonical records in 11 JSONL files and validates with bundle SHA-256 `590d28189a06cb46b47151de5359b245914a0a51f172e5e0cba6595f29712589`. It maps all 142 stable IDs one-to-one to units and segments, closes every exercise-solution and question-answer relation, binds all 53 adverse-ledger events, and registers the real cumulative artifacts and six passed Unit 4/cumulative QA events. Two deterministic generator reruns were byte-identical.
