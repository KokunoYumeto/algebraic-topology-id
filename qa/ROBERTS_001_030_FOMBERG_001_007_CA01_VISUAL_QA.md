# CA01 PDF visual QA

Status: **PASS**  
QA date: 2026-08-26  
Scope: frozen predecessor transition page 472 and the complete appended CA01 surface on physical pages 473-477.

## Bound artifact identities

- PDF: `output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-007-ca01-id.pdf`
  - 8,358,561 bytes
  - 477 pages
  - SHA-256 `476b0de3bbb2cbfe03a151ac3060e121c5f89364e70b54d918ab270f4c965ade`
- Deterministic build draft: `qa/ROBERTS_001_030_FOMBERG_001_007_CA01_BUILD_DRAFT.json`
  - 6,960 bytes
  - SHA-256 `3c82d0e81a352dad47649a44c6acec9cefd6d5c0eeefa2996eabe583f3f0319c`
- Render inventory: `qa/ROBERTS_001_030_FOMBERG_001_007_CA01_RENDER_INVENTORY.csv`
  - 1,794 bytes
  - SHA-256 `3734130dcebd7c8df1d359c3b147883c62e02c77e8a72d9d667bb4abe10fae0c`

These identities were recomputed immediately before the final render. No QA conclusion below applies to an earlier candidate PDF.

## Method

Poppler `pdftoppm` 24.04.0 rendered physical pages 472-477 as PNG at 150 dpi. Each of the six 1,241 x 1,754 px, sRGB, 8-bit images was inspected at full raster detail. Page 472 was included specifically to test the predecessor-to-CA01 transition; pages 473-477 are the entire appended CA01 reader. `pdfinfo`, `pdffonts`, `pdftotext`, pdfplumber 0.11.10, ImageMagick 7.1.2-22, and pypdf 6.12.2 supplied independent structural checks.

## Manual page inspection

| Physical page | Displayed folio | Result | Inspection |
|---:|---:|:---:|---|
| 472 | 472 | PASS | Final predecessor page is nonblank and intact. Equations, prose, source-boundary note, next-cursor notice, and footer are legible and remain within the page. |
| 473 | 1 | PASS | CA01 starts on the immediately following page without a blank separator. The centered title, date, section 1, sections 1.1-1.2, formulas, prompt, hint, and solution blocks are legible. The exercise prompts do not run into subsection headings. |
| 474 | 2 | PASS | The page continuation and sections 1.3-1.4 preserve clear prompt/hint/solution separation. Displayed formulas and the lower-page heading have adequate space and no collision. |
| 475 | 3 | PASS | Sections 1.5-1.6, group presentations, displayed equations, and surrounding prose remain inside the margins with no overlap or broken glyphs. |
| 476 | 4 | PASS | Sections 1.7-1.8, exact sequences, lifting criterion, formulas, and prose are aligned and readable. No heading run-in or bottom clipping is visible. |
| 477 | 5 | PASS | The last solution, section 1.9, three-column coverage table, final rights/source note, and footer are readable. Table rules and columns do not collide or leave the page. |

The transition is visually coherent: the predecessor ends at physical folio 472, and the distinct CA01 supplement then uses a consistent internal folio sequence 1-5. Across the six rendered pages there is no clipping, overlap, blank page, tofu/black-square glyph, missing formula, broken table, or unreadably small text.

## Structural corroboration

`pdfinfo -f 472 -l 477 -box` reports every inspected page as A4, 595.276 x 841.89 points, rotation 0. MediaBox, CropBox, BleedBox, TrimBox, and ArtBox are identical for all six pages.

`pdffonts` reports 43 font objects. Every row reports `emb=yes`, `sub=yes`, and `uni=yes`; no unembedded or non-ToUnicode font was found.

Per-page extraction and bounding-box results:

| Page | Extracted characters | Replacement/black-square characters | PDF glyph boxes | Boxes outside page | Observed x range (pt) | Observed vertical range (pt) |
|---:|---:|---:|---:|---:|---:|---:|
| 472 | 1,901 | 0 | 1,405 | 0 | 59.244-537.864 | 59.578-812.250 |
| 473 | 2,177 | 0 | 1,730 | 0 | 59.124-537.865 | 100.365-814.366 |
| 474 | 2,219 | 0 | 1,706 | 0 | 59.124-537.864 | 61.694-814.366 |
| 475 | 2,455 | 0 | 1,963 | 0 | 59.124-537.867 | 61.694-814.366 |
| 476 | 1,711 | 0 | 1,255 | 0 | 59.244-536.043 | 60.851-814.366 |
| 477 | 1,220 | 0 | 922 | 0 | 59.124-536.041 | 71.901-814.366 |

All six pages contain extractable text. The glyph-box check found no character whose box crosses an inspected page boundary.

Because an earlier candidate had an outline regression, this frozen PDF received an additional read-only check: all 389 outline entries resolve to valid pages, all 2,873 named destinations are present, and the CA01 targets cover physical pages 473-477. This is a structural resolution check, not a GUI-specific interaction test.

## Defect classification

- P1 (release-blocking missing, unreadable, blank, or clipped content): **0**
- P2 (material layout, transition, font, formula, or table defect): **0**
- P3 (minor visible cosmetic defect): **0**

Overall disposition: **PASS for the inspected PDF boundary.**

## Limitations

- This pass deliberately rerenders page 472 and pages 473-477, not predecessor pages 1-471. The deterministic build draft separately binds the predecessor prefix.
- A 150 dpi visual pass plus extraction and bounding-box checks cannot prove mathematical correctness or semantic accessibility. The PDF remains untagged; the reflowable HTML is the accessibility-oriented surface.
- Live-browser HTML QA, public-byte readback, and publication are outside this visual-PDF task.
