# Visual QA - Roberts 001-030 plus Fomberg 001-006

Date: 2026-08-25T21:48:52Z
Status: **PASS**
Inspector/model provenance: OpenAI Codex gpt-5.6-sol, Ultra

## Source PDF identity

- File: `output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-006-id.pdf`
- Bytes: 6,723,586
- SHA-256: `136dc7f6fa744e87fe067a96a36a8fbee8098aad9167629653bc085f6a718c37`
- Physical properties: 452 A4 pages, PDF 1.5, not encrypted, and not tagged.

## Render evidence

The exact PDF pages 438-452 inclusive were rendered with Poppler `pdftoppm` at 120 dpi into `tmp/pdfs/unit006-visual-qa-120`. The render set contains 15 individual page PNGs, each 993 x 1404 pixels, plus one contact sheet. The individual page renders total 3,455,926 bytes. The contact sheet is `contact-sheet-pages-438-452.png`, 1002 x 2590 pixels, 3,955,188 bytes, SHA-256 `5b9c7c7943388d3662d45f3275a981a73a09c32a55978faae10c042afff20298`. All 16 render artifacts total 7,411,114 bytes. Exact per-file sizes and SHA-256 identities are recorded in `qa/ROBERTS_001_030_FOMBERG_001_006_RENDER_INVENTORY.csv`.

## Inspection coverage

The full contact sheet was inspected for continuity and page-wide anomalies. Every individual page render, pages 438-452, was then inspected at original 993 x 1404 resolution. The review explicitly checked text and mathematics for clipping, overlap, missing glyphs, black boxes, broken line wrapping, margin intrusion, and unreadable scale; figures for cropping, raster damage, label collision, and semantic-arrow visibility; and page numbers, whitespace, and section transitions for continuity.

- Page 438 is the seam page that cleanly closes Fomberg Unit 005. It ends with the prior component boundary and states the next source cursor at line 3123.
- Page 439 cleanly starts Fomberg Unit 006 with the component title, rights/provenance notice, and the `Kompleks Seluler` section. There is no duplicated, missing, or overlapping material at the seam.
- Pages 439-452 contain Unit 006. Pages 440-446 include the diagram-rich CW-complex material. Original-resolution checks confirmed sharp labels and intact geometry for the CW construction, attaching versus characteristic maps, Hawaiian earring, Petersen graph, sphere, torus, and real/complex projective-space figures.
- Pages 447-451 carry the six mastery checks, hints, complete solutions, and displayed mathematics without clipping or collisions.
- Page 452 cleanly closes Unit 006, states the translated source span 3123-3517, and identifies line 3518 as the next cursor. The intentionally open lower-page whitespace is a clean end-of-unit boundary, not missing content.

## Result

Detected visual defects: 0.

The inspected span has consistent margins, readable typography, clear hierarchy, stable page numbering, intact mathematics, and sharp, correctly placed figures. No clipped text, overlapping objects, broken diagrams, unreadable glyphs, accidental black regions, footer collisions, or seam discontinuities were found. Visual QA therefore passes for the Unit 006 PDF boundary.

This receipt records visual-layout QA only. The PDF's untagged accessibility limitation remains disclosed and is not represented here as repaired.

## Reflowing HTML browser QA

The exact local HTML artifact
`output/html/roberts-001-030-fomberg-001-006/index.html` was served unchanged
over a loopback-only HTTP endpoint and inspected in the Codex in-app browser.
At 1440 x 900, the 1,152-pixel reader body was centered at approximately
136.44 pixels from the left and 136.56 pixels from the right. At 375 x 812,
the document and body were both 360 pixels wide and had 360-pixel scroll
widths, so page-level horizontal overflow was zero. Unit 006 was inspected at
both sizes; its heading, prose, display mathematics, semantic blocks, and
figures remained readable and within the viewport.

The application DOM contained 2,231 unique reader IDs. The browser added one
separate annotation-root ID, `codex-browser-sidebar-comments-root`; it is not
part of the artifact and was excluded from the application census. All 431
local fragment links resolved, all 15,273 MathML nodes and 142 semantic
`.figure` blocks were present, and all 16 embedded figure images remained in
bounds. At phone width,
426 wide mathematics nodes and one table used their own local horizontal
scrollers while the page itself did not widen. Desktop centering, mobile
reflow, Unit 006 navigation, fragment closure, and image bounds therefore
pass.

## Public GitHub Pages browser QA

The deployed reader at
`https://kokunoyumeto.github.io/algebraic-topology-id/roberts-001-030-fomberg-001-006/`
returned HTTP 200 and exactly 12,555,960 bytes with SHA-256
`80a7d092cb786e4d4f7ecab31ba40746cf59398db50f0adca50f2431746f7c92`,
identical to the local HTML artifact. The GitHub Pages workflow run
`32904157067` and deploy job `97984350511` both completed successfully.

In the public browser at `1440x900`, the 1,152-pixel body remained centered
inside a 1,425-pixel document viewport, with no page-level horizontal
overflow. The application exposed 2,231 unique IDs, 431/431 resolved local
fragment links, 15,273 MathML nodes, 142 semantic `.figure` blocks, and 16
embedded figure images, all in bounds. The Unit 006 anchor opened directly at
`Kompleks Seluler`, and the console produced zero warnings or errors.

At `375x812`, the rendered document and body both measured 360 pixels wide
with 360-pixel scroll widths and zero page-level horizontal overflow. The
reader confined 426 wide mathematics nodes and one table to 427 local
scrollers; all 16 images remained in bounds. A fresh navigation to the public
Unit 006 anchor showed the component heading, introductory remark, cellular
construction definition, and display mathematics cleanly at phone width.
Public desktop centering, mobile reflow, fragment closure, navigation, image
bounds, and runtime console checks therefore pass.
