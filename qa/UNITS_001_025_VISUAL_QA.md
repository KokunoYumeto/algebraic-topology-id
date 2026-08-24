# Units 001-025 cumulative visual QA

Status: **PASS** for the verified cumulative checkpoint.

The final deterministic reader is 298 A4 pages, 1,972,209 bytes, SHA-256
`581d62162633a6624687517c5cf1595f5fc02a2701c2222b279711e0520b9a3f`.
Pandoc 3.9.0.2 and MiKTeX-pdfTeX 4.27 (MiKTeX 26.5) produced
byte-identical PDFs in two passes under `SOURCE_DATE_EPOCH=1787529600`.

## Complete new-span render inspection

Poppler 24.04.0 rendered the title page, the preceding transition page, and
**every PDF page containing Unit 25** at 144 dpi and 1,191 by 1,684 pixels.
The inspected set is exactly pages **1, 286, and 287-298**. Unit 25 begins on
page 287 after the Unit 24 terminal boundary and closes on page 298 with the
exact source cursor for Unit 26.

All 14 rendered PNGs were inspected at original render resolution. The exact
page-by-page coverage, byte-count, and SHA-256 inventory is
`qa/UNITS_001_025_RENDER_INVENTORY.csv`, 2,731 bytes, SHA-256
`a55ff205e621fbc750baaf086fa18883c72dba5bdfe1f66e4554247d22fdc12f`.
The task-local PNG witnesses were removed only after the inventory and this
inspection result were fixed; they remain reproducible from the final PDF,
page numbers, Poppler version, dpi, dimensions, and recorded hashes.

No inspected page has clipping, overlap, missing or broken glyphs, unreadable
mathematics, table overflow, positional-figure dependence, or collision with
the margins or page number. In particular:

- page 1 has a centered, balanced title/subtitle and a readable contents start;
- page 286 preserves the Unit 24-to-25 transition and begins the complete Unit
  25 provenance notice without duplicating or dropping content;
- the two former Xy-pic surfaces are preserved as readable semantic sequences,
  object-and-arrow data, and commutativity identities;
- the relative long exact sequence, complete Five Lemma chase, infinite-line
  recursion, and repaired Euler calculation remain inside the A4 text area;
- all six problem/hint/full-solution triples flow without orphaned labels or
  bottom-margin collisions; and
- page 298 closes with the exact boundary to Unit 26 and adequate whitespace.

## Reflowable HTML inspection

The final self-contained HTML is 4,112,563 bytes, SHA-256
`38cd8437f3b4235ac6269f4e3365123fa06485269d35a424ad4f5ddd589025c1`.
It was served only on `127.0.0.1` and inspected in the in-app Chromium surface
with explicit desktop and mobile viewport overrides.

- Desktop: requested viewport 1,425 by 1,000 pixels; effective document width
  1,410 pixels; body width 1,152 pixels; left/right margins 129.111 and
  128.889 pixels; centering delta 0.222 pixels; document scroll width exactly
  1,410 pixels; zero uncontained overflow. All 62 semantic figures stay
  between x=193.111 and x=1,217.111 pixels.
- Mobile: requested viewport 390 by 844 pixels; effective content width 375
  pixels; body width 375.111 pixels with 17.6-pixel side padding; document
  scroll width exactly 375 pixels; all 62 figures stay between x=17.597 and
  x=357.514 pixels; zero uncontained overflow.
- The mobile reader has 199 display-MathML and two inline-MathML expressions
  wider than their local containers. All 201 are retained losslessly inside
  explicit horizontal scrollers; none expands or clips the document. The
  1,661 descendant boxes geometrically crossing the narrow root all belong to
  those local scrollers, leaving zero uncontained crossing element.
- The Unit 25 opening and closing boundary were visually inspected at mobile
  width. The reading column fills the narrow viewport with readable padding,
  and long formulae scroll locally without displacing text or semantic blocks.

The HTML contains 10,118 native MathML nodes, 62 semantic figures, 1,361
unique DOM IDs, 296 resolving fragment links, zero raw-TeX math fallbacks, and
no external runtime script, stylesheet, frame, or image dependency.

## PDF and accessibility verification

- PDF metadata: title `Topologi Aljabar - Unit 1-25`, A4, 298 pages,
  `/Lang=id-ID`, no encryption, form, widget, JavaScript name tree, additional
  action, suspect flag, or page rotation. Its 409 annotations are links only.
- Fonts: 27 Poppler rows; every row is embedded, subset, and has a Unicode map.
- Structural tagging: the PDF is honestly **untagged**. The reflowable,
  self-contained HTML is the accessible primary structure.
- The extracted pages 286-298 contain **OpenAI Codex gpt-5.6-sol, Ultra**,
  Roberts's source credit, the Unit 25 heading, the boundary to Unit 26, and
  source cursor 5612, with no credential marker, placeholder, or local user
  path.

This review covers every page newly contributed by Unit 25 and representative
title/transition pages. It does not claim manual reinspection of unchanged
interior pages from the separately frozen Units 001-024 baseline.
