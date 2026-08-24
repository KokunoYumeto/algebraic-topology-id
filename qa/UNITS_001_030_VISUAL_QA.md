# Units 001-030 cumulative visual and responsive QA

Status: **PDF PASS; live desktop/mobile HTML geometry PASS.**

The final deterministic reader is 351 A4 pages, 2,257,988 bytes, SHA-256
`b9d37776c64541123345c7b28fd26df161b878e8c105c16670455fd532dc08a4`.
Pandoc 3.9.0.2 and MiKTeX-pdfTeX 4.27 (MiKTeX 26.5) produced two
byte-identical PDF outputs under `SOURCE_DATE_EPOCH=1787529600`.

## Complete new-span PDF inspection

Poppler 24.04.0 rendered the title page and **every PDF page containing Unit
30** at 144 dpi and 1,191 by 1,684 pixels. The inspected set is exactly pages
**1 and 343-351**. Page 343 is the Unit 29-to-30 transition: it closes the
Unit 29 suspension calculation and exact boundary, then contains the complete
Unit 30 provenance, lecture heading, and Brouwer opening. Unit 30 continues
through page 351 and closes there at the terminal Roberts source boundary.

All 10 rendered PNGs were inspected at original resolution. Their exact page
coverage, byte counts, dimensions, and SHA-256 identities are recorded in
`qa/UNITS_001_030_RENDER_INVENTORY.csv`, 2,059 bytes, SHA-256
`b776c8bda19ccbb1fca9ad0fb2940e9bd6bb468cea98ac655d63210f832e137f`.
The render witnesses total 2,435,788 bytes. They were removed only after the
inventory and inspection result were sealed; every witness is reproducible
from the final PDF, page number, Poppler version, dpi, and recorded hash.

No inspected page has clipping, overlap, missing or broken glyphs, unreadable
mathematics, positional-figure dependence, an orphaned heading, or a collision
with a margin or page number. In particular:

- page 1 has a centered title and balanced three-line expanded subtitle, with
  authorship, date, and opening contents inside the A4 text area;
- page 343 preserves the complete Unit 29-to-30 transition, all Unit 30 source,
  rights, correction, and provenance statements, and the lecture opening
  without crowding;
- pages 344-345 preserve the free-map definition, explicit continuous Brouwer
  retraction, semantic ray figure, correctly directed reduced-cohomology
  contradiction, source audit, and algebra-theorem opening;
- page 346 preserves the quantitative leading-term bound, nonzero straight-line
  homotopy, winding contradiction, source audit, and hairy-sphere opening;
- pages 347-348 preserve the ambient-sphere tangent-field formulation, reduced
  degree definition, all four degree properties, reflection lemma, antipodal
  corollary, and both directions of the hairy-sphere theorem;
- pages 349-351 contain all six problem/hint/full-solution triples without
  clipping or bottom-margin collision; and
- page 351 closes with the odd-dimensional tangent-field verification and exact
  terminal boundary at EOF after `Notes.tex` line 6368, followed by adequate
  whitespace.

## Reflowable HTML verification

The final self-contained HTML is 4,861,791 bytes, SHA-256
`ed9da5653b3eacf7418d6e08760fcd2ecff4d75799c47f08689b940798099891`.
Two independent Pandoc outputs were byte-identical. Structural inspection
found 11,787 native MathML nodes (2,035 display and 9,752 inline), 65 semantic
figures, 1,651 unique DOM IDs, zero duplicate IDs, 337 fragment links with zero
unresolved targets, zero raw-TeX fallback, zero script tags, zero external
runtime asset references, `lang="id-ID"`, an explicit document title and TOC
role, exact model provenance, and all 47 Unit 30 IDs.

The in-app browser loaded the local final reader successfully with zero console
errors or warnings. At a requested 1,440 by 900 viewport, the root content
width was 1,425 pixels (the remaining 15 pixels were the vertical scrollbar),
the body was exactly 1,152 pixels wide, and its measured left/right margins
were 136.444/136.556 pixels. Root horizontal overflow and elements crossing
the viewport were both zero.

At a requested 390 by 844 mobile viewport, the layout engine reported a
375-pixel root content width, a full-width 375.111-pixel body with 17.6-pixel
side padding, and zero root horizontal overflow. Of 11,787 MathML nodes, 255
were genuinely wider than their own content boxes: 253 display and two inline.
All 255 exposed local horizontal scrolling. One wide table was also a local
horizontal scroller. The 2,133 descendant boxes that extended beyond the
viewport all belonged to one of those 256 local overflow containers; the count
of uncontained overflow elements was zero. No responsive media overflow was
present. The temporary viewport override was reset after the measurements.

The live accessibility evidence includes the Indonesian document language,
the exact reader title, a banner heading, a `doc-toc` navigation role, native
MathML, stable semantic headings and figures, zero unnamed links, and zero
images missing alternative text. This is evidence about the delivered surface,
not a claim of formal WCAG conformance.

## PDF structure and accessibility

- Metadata: title `Topologi Aljabar - Unit 1-30`, A4, 351 pages,
  `/Lang=id-ID`, zero page rotation, no encryption, form, widget, JavaScript
  name tree, JavaScript annotation action, additional action, or suspect flag.
- All 473 annotations are links: 343 ordinary internal `GoTo` actions and 130
  URI actions. The catalog `/OpenAction` is an ordinary `/GoTo` destination
  fitted to the opening page, not executable code.
- The 27 PDF font objects are all embedded, subset, and mapped with
  `/ToUnicode`.
- Structural tagging is honestly absent (`/Marked=false` and no
  `/StructTreeRoot`). The self-contained reflowable HTML remains the primary
  accessible surface.
- Normalized extracted text from pages 343-351 contains the exact model note,
  three source-author credits, the Unit 30 heading, the Unit 29-to-30 boundary,
  and the final EOF cursor after line 6368. A whole-PDF extracted-text scan
  contains no credential marker, placeholder, or local user path.

This review covers every page newly contributed by Unit 30 and the title and
transition surfaces. It does not claim manual reinspection of unchanged
interior pages from the separately frozen Units 001-029 baseline.
