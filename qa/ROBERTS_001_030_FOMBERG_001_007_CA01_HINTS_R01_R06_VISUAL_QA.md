# CA01 plus R01-R06 ordinary-hint PDF visual QA

Status: **PASS**  
QA date: 2026-08-26  
Scope: frozen predecessor boundary page 477 and the complete five-page ordinary-hint appendix on physical pages 478-482.

## Bound artifact identities

- PDF: `output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-id.pdf`
  - 8,592,243 bytes
  - 482 A4 pages
  - SHA-256 `4da7f1368c17423cd6845c36b7d5190dac98d515ecbd32467c0c59961dd9afcb`
- Deterministic build draft: `qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_BUILD_DRAFT.json`
  - 8,992 bytes
  - SHA-256 `e845fc16ae248cc81370ea65177c318d2709b89341368900c79f8ea1e34bf692`
- Render inventory: `qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_RENDER_INVENTORY.csv`
  - 1,829 bytes
  - SHA-256 `ce997bf4d974a7dae8f798dd92fa65063dd68b3d50ab9a168e323b41dfefe352`

These identities were recomputed immediately before rendering. No conclusion below applies to an earlier build candidate.

## Method

Poppler `pdftoppm` 24.04.0 rendered physical pages 477-482 at 160 dpi. Each of the six 1,323 x 1,871 px PNGs was inspected at original raster detail. Page 477 tests the frozen CA01-to-hint transition; pages 478-482 are the entire appended hint surface. `pdfinfo` 24.04.0, `pdffonts` 24.04.0, pdfplumber 0.11.10, and pypdf 6.12.2 supplied independent structural checks. The PNGs were temporary inspection artifacts; their exact identities are retained in the inventory and the loose renders are removed after this receipt is finalized.

## Manual page inspection

| Physical page | Displayed folio | Result | Inspection |
|---:|---:|:---:|---|
| 477 | 5 | PASS | The frozen CA01 final page remains nonblank and intact. Equations, section 1.9, the three-column assessment table, final source note, and footer are legible and stay inside the page. |
| 478 | 1 | PASS | The hint appendix begins immediately on the next page. Centered title/date, status prose, R01 heading, all reference links, formulas, and six R01 hints are readable. The last reference line clears the footer. |
| 479 | 2 | PASS | R02 and the start of R03 preserve a clear heading hierarchy, reference/hint separation, mathematical symbols, paragraph spacing, and margins. |
| 480 | 3 | PASS | The end of R03 and start of R04 retain every reference line and hint boundary. Page extraction confirms the two reference lines that are visually compact below the R04 heading; neither is omitted. |
| 481 | 4 | PASS | The end of R04 and R05 material remain readable. Long hints continue naturally across page boundaries without overlap, clipping, or an orphaned heading. |
| 482 | 5 | PASS | The end of R05 and all six R06 hints are complete. Links, formulas, prose, and the final footer remain inside the page with no truncation. |

Across the six pages there is no blank page, clipping, overlap, tofu/black-square glyph, missing formula, unreadable text, or broken section transition. Blue reference links are consistently visible and are also labelled in text, so their meaning does not depend on color alone.

## Structural corroboration

- All inspected pages are A4, 595.276 x 841.89 points, rotation 0.
- `pdffonts` reports 59 font objects; every row has `emb=yes`, `sub=yes`, and `uni=yes`.
- The 477-page predecessor has 2,873 unchanged named destinations and 389 unchanged outline entries.
- The merged PDF has 2,988 named destinations: the 2,873 predecessor names, 72 reviewed predecessor stable-ID names required by the hint links, and 43 new hint-layer names. It has 396 outline entries: the 389-entry predecessor prefix plus seven source-derived hint headings.
- An independent bounded audit matched every one of the 72 exercise/solution names to the leading rendered text on its mapped physical predecessor page: 72/72 PASS, zero name collisions, zero wrong-page findings.

Per-page extraction and bounding-box results:

| Page | Extracted characters | Replacement/black-square characters | PDF glyph boxes | Boxes outside page | Observed x range (pt) | Observed vertical range (pt) |
|---:|---:|---:|---:|---:|---:|---:|
| 477 | 1,112 | 0 | 922 | 0 | 59.124-536.041 | 71.901-814.366 |
| 478 | 2,234 | 0 | 1,887 | 0 | 59.528-537.868 | 100.365-814.366 |
| 479 | 2,710 | 0 | 2,297 | 0 | 59.135-537.868 | 61.694-814.366 |
| 480 | 2,917 | 0 | 2,499 | 0 | 59.255-537.865 | 60.104-814.366 |
| 481 | 3,051 | 0 | 2,597 | 0 | 59.244-537.265 | 61.694-814.366 |
| 482 | 2,949 | 0 | 2,518 | 0 | 59.528-537.869 | 61.694-814.366 |

Every page contains extractable text. No glyph box crosses an inspected page boundary.

## Defect classification

- P1 (release-blocking missing, unreadable, blank, clipped, or mislinked content): **0**
- P2 (material layout, transition, font, formula, hierarchy, or navigation defect): **0**
- P3 (minor visible cosmetic defect): **0**

Overall disposition: **PASS for the complete additive PDF boundary.**

## Limitations

- This pass rerenders page 477 and pages 478-482, not predecessor pages 1-476. The deterministic build receipt independently proves the 477 predecessor pages have unchanged content streams, resources, boxes, extracted text, and visual signatures.
- The PDF remains untagged. The self-contained native-MathML HTML is the primary reflowable and accessibility-oriented surface.
- Browser QA, public-byte readback, and publication are separate gates.
