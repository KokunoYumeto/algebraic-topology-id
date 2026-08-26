# Visual QA — Roberts 001–030 plus Fomberg 001–007

Date: 2026-08-26T00:25:00Z  
Status: **PASS**  
Inspector/model provenance: OpenAI Codex gpt-5.6-sol, Ultra

## Source PDF identity

- File: `output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-007-id.pdf`
- Bytes: 8,326,404
- SHA-256: `1beca2d03f04c1fcca7eb01bd2654567908febc1ba7941b459c06b90ef865c22`
- Physical properties: 472 A4 pages, not encrypted, and not structurally tagged.

## Render evidence

The exact PDF pages 438–472 inclusive were rendered with Poppler `pdftoppm` at
120 dpi. The render set contains 35 individual page PNGs (993 × 1404 pixels)
and one contact sheet. Every page render and the contact sheet is listed with
byte count and SHA-256 in
`qa/ROBERTS_001_030_FOMBERG_001_007_RENDER_INVENTORY.csv` (36 rows, all
`inspection_result=PASS`).

The contact sheet was inspected for continuity and page-wide anomalies. Full-
resolution checks covered the seam pages 438–439, representative diagram pages
440, 442, 444–445, 462–463, and the closing page 472; the remaining pages were
checked in the full contact sheet. Inspection covered clipping, overlap,
missing glyphs, black boxes, line wrapping, margin intrusion, figure cropping,
label collisions, arrow visibility, page numbers, whitespace, and section
transitions.

- Page 438 cleanly closes the preceding Fomberg component.
- Page 439 starts Unit 007 with its rights/provenance notice and `Kompleks
  Seluler` section; no seam duplication or omission is visible.
- Pages 440–463 contain the cellular-complex construction, Hawaiian earring,
  Petersen graph, sphere, torus, genus-two, and Klein-bottle redraws. Labels,
  arrows, and geometry remain inside the page margins.
- Pages 464–471 carry the cellular boundary calculations and six mastery
  checks with hints and complete solutions without collisions.
- Page 472 closes the selected source span at line 4185 and states the next
  source line 4186 (`Extras before cohomology`); the end whitespace is an
  intentional unit boundary.

Detected visual defects: 0.

## Reflowing HTML browser QA

The exact local HTML artifact was served over a loopback-only HTTP endpoint and
inspected in the Codex in-app browser at 1440 × 900 and 375 × 812. At desktop
size, the reader body is 1152 px wide and centered (136.44 px left offset;
151.56 px right offset after the vertical scrollbar). At phone size, body and
document scroll widths are both 360 px, so page-level horizontal overflow is
zero. The HTML contains 2,315 unique IDs, 440 local fragment links (440/440
resolve), 15,945 MathML nodes, 159 semantic figure blocks, and 19 embedded
images; all 19 images remain in bounds at both viewports. The page has no
external scripts or stylesheet links, and all 492 wide math nodes use local
scrolling at phone width rather than widening the document.

The browser emitted no errors. Two non-fatal MathJax component-version warnings
were emitted by the browser's instrumentation while inspecting already-present
MathML; they do not alter the self-contained artifact or its layout.

The PDF remains intentionally untagged; the self-contained HTML is the primary
accessible and reflowable reader surface. No formal accessibility-tree
conformance claim is made.

