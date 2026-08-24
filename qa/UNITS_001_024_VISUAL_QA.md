# Units 001-024 cumulative visual QA

Status: **PASS** for the verified cumulative checkpoint.

The final deterministic reader is 286 A4 pages, 1,907,368 bytes, SHA-256
`5189b04f2f28d7e8192c16e8ef070e23bbf98085d150d1f2124d15c071ccf9b8`.
Pandoc 3.9.0.2 and MiKTeX-pdfTeX 4.27 (MiKTeX 26.5) produced
byte-identical PDFs in two passes under `SOURCE_DATE_EPOCH=1787529600`.

## Complete new-span render inspection

Poppler 24.04.0 rendered the title page, the preceding transition page, and
**every PDF page containing Unit 24** at 144 dpi and 1,191 by 1,684 pixels.
The inspected set is exactly pages **1, 273, and 274-286**. Unit 24 begins on
page 274 after the Unit 23 terminal boundary and closes on page 286 with the
exact source cursor for Unit 25.

All 15 rendered PNGs were inspected at original render resolution. The exact
page-by-page coverage, byte-count, and SHA-256 inventory is
`qa/UNITS_001_024_RENDER_INVENTORY.csv`, 2,659 bytes, SHA-256
`1d9554d98de7d4751fc7ee2d1b5a6cb45edb580e62226b030aea389dff9de683`.
The task-local PNG witnesses were removed only after the inventory and this
inspection result were fixed; they remain reproducible from the final PDF,
page numbers, Poppler version, dpi, dimensions, and recorded hashes.

No inspected page has clipping, overlap, missing or broken glyphs, unreadable
mathematics, table overflow, positional-figure dependence, or collision with
the margins or page number. In particular:

- page 1 has a centered, balanced title/subtitle and a readable contents start;
- pages 273-274 preserve the cross-unit example and the Unit 23-to-24 boundary
  without duplicating or dropping the source continuation;
- all three semantic diagrams fit the text block and preserve their nodes,
  arrow directions, labels, domains, codomains, and explanatory prose;
- the six Snake Lemma obligations, preparation diagram, kernel/cokernel
  quotients, and long exact sequences remain legible and inside the A4 text
  area;
- all six problem/hint/full-solution triples flow without orphaned labels or
  bottom-margin collisions; and
- page 286 closes with the exact boundary to Unit 25 and adequate whitespace.

## Reflowable HTML inspection

The final self-contained HTML is 3,927,104 bytes, SHA-256
`28a84406de9e196070965920a7f7937177197977f9ddf118f0f8b07d464cbf0f`.
It was served only on `127.0.0.1` and inspected in the in-app Chromium
surface with explicit desktop and mobile viewport overrides.

- Desktop: requested viewport 1,425 by 1,000 pixels; effective document width
  1,410 pixels; body width 1,152 pixels; left/right margins 129.111 and
  128.889 pixels; centering delta 0.222 pixels; document scroll width exactly
  1,410 pixels; zero uncontained overflow. All 60 semantic figures stay
  between x=193.111 and x=1,217.111 pixels.
- Mobile: requested viewport 390 by 844 pixels; effective content width 375
  pixels; body width 375.111 pixels with 17.6-pixel side padding; document
  scroll width exactly 375 pixels; all 60 figures stay between x=17.597 and
  x=357.514 pixels; zero uncontained overflow.
- The final mobile reader has 186 display-MathML and two inline-MathML
  expressions wider than their local containers. All 188 are retained
  losslessly inside explicit horizontal scrollers; none expands or clips the
  document.
- The first mobile check correctly failed with 198 pixels of document overflow:
  two long inline formulas in the new Unit 24 margin note escaped the
  display-math-only rule. The cumulative builder now constrains inline MathML
  to an inline-block local scroller. A fresh two-pass rebuild and browser
  reload reduced document overflow to zero at both viewports.
- The final Unit 24 opening and closing proof surfaces were visually inspected
  at desktop and mobile widths. The reading column is centered on desktop and
  fills the narrow viewport with readable padding on mobile.

The HTML contains 9,669 native MathML nodes, 60 semantic figures, 1,295 unique
DOM IDs, 288 resolving fragment links, zero raw-TeX math fallbacks, and no
external runtime script, stylesheet, frame, or image dependency.

## PDF and accessibility verification

- PDF metadata: title `Topologi Aljabar - Unit 1-24`, A4, 286 pages,
  `/Lang=id-ID`, no encryption, form, widget, JavaScript, suspect flag, or
  page rotation.
- Fonts: 27 Poppler rows; every row is embedded, subset, and has a Unicode map.
- Structural tagging: the PDF is honestly **untagged**. The reflowable,
  self-contained HTML is the accessible primary structure.
- The extracted Unit 24 span contains **OpenAI Codex gpt-5.6-sol, Ultra**, the
  Unit 24 heading, the boundary to Unit 25, and source cursor 5370, with no
  credential marker, placeholder, or local user path.

This review covers every page newly contributed by Unit 24 and representative
title/transition pages. It does not claim manual reinspection of unchanged
interior pages from the separately frozen Units 001-023 baseline.
