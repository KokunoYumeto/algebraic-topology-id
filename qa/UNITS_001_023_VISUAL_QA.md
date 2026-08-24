# Units 001-023 cumulative visual QA

Status: **PASS** for the verified cumulative checkpoint.

The final deterministic reader is 273 A4 pages, 1,801,983 bytes, SHA-256
`e51aa739eefaa12f4b1d7a4fe99073c525775f113aa62e4506395a01fe1fcbaf`.
Pandoc 3.9.0.2 and MiKTeX pdfTeX 1.40.29 produced byte-identical PDFs in
two independent passes under `SOURCE_DATE_EPOCH=1787529600`.

## Complete new-span render inspection

Poppler 24.04.0 rendered the title page, the preceding transition page, and
**every PDF page containing Unit 23** at 144 dpi and 1,191 by 1,684 pixels.
The inspected set is exactly pages **1, 260, and 261-273**. Unit 23 begins on
page 261 after the complete Unit 22 solution and its safe boundary, its heading
appears on page 262, and its terminal boundary to Unit 24 closes page 273.

All 15 rendered PNGs were inspected at original render resolution. The compact
page-by-page coverage, byte-count, and SHA-256 inventory is
`qa/UNITS_001_023_RENDER_INVENTORY.csv`, 2,621 bytes, SHA-256
`54b564278bcdafcec8b18420286de6b0f5274922e540fe70bd78a6be7f2d5b21`.
The task-local PNG witnesses were removed only after this inventory and the
inspection result were fixed; they remain reproducible from the PDF, page
numbers, Poppler version, dpi, dimensions, and recorded hashes.

No inspected page has clipping, overlap, missing or broken glyphs, unreadable
mathematics, table overflow, positional-figure dependence, or collision with
the margins or page number. In particular:

- page 1 has a centered, balanced title/subtitle and a readable contents start;
- pages 260-262 preserve a coherent Unit 22-to-23 transition without a false
  source-environment closure;
- both semantic diagrams are centered and retain their labels, arrow
  directions, domain/codomain information, and explanatory prose;
- the tetrahedral simplex census table on page 266 remains fully inside the
  text block and is legible;
- the long exactness, product, quotient, and reduced-function displays on
  pages 267-273 remain within the A4 text area; and
- page 273 closes with the exact continuation cursor to Unit 24 and adequate
  bottom margin.

## Reflowable HTML inspection

The final self-contained HTML was served only on `127.0.0.1` and inspected in
the in-app Chromium surface at both desktop and mobile viewport overrides.

- Desktop: effective viewport 1,425 by 1,000 pixels; body width 1,152 pixels;
  left/right margins 136.444 pixels; centering delta 0.056 pixels; document
  scroll width exactly 1,425 pixels; zero uncontained overflow.
- Mobile: requested width 390 pixels and effective content viewport 375 by 844
  pixels; body and document scroll width exactly 375 pixels; body side padding
  17.6 pixels; all figures remain between x=17.6 and x=357.5 pixels; zero
  uncontained overflow.
- The 168 display-MathML nodes wider than their mobile containers are retained
  losslessly inside their explicit horizontal scrollers. No wide expression
  expands or clips the page itself.
- The desktop and mobile Unit 23 opening, heading hierarchy, prose, formula,
  and semantic Diagram 23.1 were visually inspected. The reading column is
  centered on desktop and fills the narrow viewport with readable padding on
  mobile. No external runtime script, stylesheet, frame, or image was loaded.

## PDF and accessibility verification

- PDF metadata: title `Topologi Aljabar - Unit 1-23`, A4, 273 pages,
  `/Lang=id-ID`, no encryption, form, widget, JavaScript, suspect flag, or page
  rotation.
- Fonts: 26 Poppler rows; every row is embedded, subset, and has a Unicode map.
- Structural tagging: the PDF is honestly **untagged**. The reflowable,
  self-contained HTML is the accessible primary structure and contains 9,167
  native MathML nodes, 57 semantic figures, 1,225 unique DOM IDs, and zero raw
  TeX math fallback.
- The extracted Unit 23 PDF span contains the exact model provenance
  **OpenAI Codex gpt-5.6-sol, Ultra**, the Unit 23 heading, the boundary to Unit
  24, and source cursor 5113, with no credential marker, placeholder, or local
  user path.

This review covers every page newly contributed by Unit 23 and representative
title/transition pages. It does not claim manual reinspection of unchanged
interior pages from the separately frozen Units 001-022 baseline.
