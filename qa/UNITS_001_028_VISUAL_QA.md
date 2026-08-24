# Units 001-028 cumulative visual and responsive QA

Status: **PDF PASS; live desktop/mobile HTML geometry PASS.**

The final deterministic reader is 334 A4 pages, 2,159,838 bytes, SHA-256
`9f3e1f7fcad396d3e654362ab232bdcd2497346cec6f0aacf7122e6450381657`.
Pandoc 3.9.0.2 and MiKTeX-pdfTeX 4.27 (MiKTeX 26.5) produced two
byte-identical PDF outputs under `SOURCE_DATE_EPOCH=1787529600`.

## Complete new-span PDF inspection

Poppler 24.04.0 rendered the title page and **every PDF page containing Unit
28** at 144 dpi and 1,191 by 1,684 pixels. The inspected set is exactly pages
**1 and 325-334**. Page 325 is the Unit 27-to-28 transition: it closes the
sphere-cohomology solution and exact Unit 27 boundary, then begins the Unit 28
provenance. Unit 28 continues through page 334 and closes there with the exact
source cursor for Unit 29.

All 11 rendered PNGs were inspected at original resolution. Their exact page
coverage, byte counts, dimensions, and SHA-256 identities are recorded in
`qa/UNITS_001_028_RENDER_INVENTORY.csv`, 2,241 bytes, SHA-256
`e2370f505a64dc15e7ba3913992227d24212f65e820aed8e3e980cf08d1eba4b`.
The render witnesses total 2,817,662 bytes. They were removed only after the
inventory and inspection result were sealed; every witness is reproducible
from the final PDF, page number, Poppler version, dpi, and recorded hash.

No inspected page has clipping, overlap, missing or broken glyphs, unreadable
mathematics, positional-figure dependence, an orphaned heading, or a collision
with a margin or page number. In particular:

- page 1 has a centered title and balanced three-line expanded subtitle, with
  authorship, date, and opening contents inside the A4 text area;
- page 325 preserves the complete Unit 27-to-28 transition and begins the
  exact source, rights, and provenance statement without crowding;
- pages 326-327 preserve the Unit 28 provenance close, the full sphere
  calculation, the nonzero-coefficient qualification, dimension invariance,
  and the opening of excision;
- pages 328-329 preserve both contravariant arrows, the complete quotient
  theorem proof, the long exact corollary, the Hatcher neighborhood reference,
  and all four skeleton-quotient identifications;
- pages 330-331 preserve the wedge definition and repairs, product-valued
  infinite-wedge cohomology proof, sphere example, and the corrected
  singular-to-simplicial restriction map with all wide displays readable;
- pages 332-334 contain all six problem/hint/full-solution triples without
  clipping or bottom-margin collision; and
- page 334 closes with the comparison-map proof and exact boundary to Unit 29
  at source cursor 6053, followed by adequate whitespace.

## Reflowable HTML verification

The final self-contained HTML is 4,624,723 bytes, SHA-256
`30f4821960a310bfb6f457f05838b6d8355e2a6df5c35b3a3dcdd9c1afa0a13e`.
Two independent Pandoc outputs were byte-identical. Structural inspection
found 11,261 native MathML nodes (1,952 display and 9,309 inline), 63 semantic
figures, 1,539 unique DOM IDs, zero duplicate IDs, 321 fragment links with
zero unresolved targets, zero raw-TeX fallback, zero external runtime
dependency, `lang="id-ID"`, an explicit document title and TOC role, exact
model provenance, and all 47 Unit 28 IDs.

The in-app browser loaded the local final reader successfully with zero console
errors or warnings. At a requested 1,440 by 900 viewport, the root content
width was 1,425 pixels (the remaining 15 pixels were the vertical scrollbar),
the body was exactly 1,152 pixels wide, and its measured left/right margins
were 136.444/136.556 pixels. Root horizontal overflow and elements crossing
the viewport were both zero.

At a requested 390 by 844 mobile viewport, the layout engine reported a
375-pixel root content width, a full-width 375.111-pixel body with 17.6-pixel
side padding, and zero root horizontal overflow. Of 11,261 MathML nodes, 235
were genuinely wider than their own content boxes: 233 display and two inline.
All 235 exposed local horizontal scrolling. The 1,919 descendant boxes that
extended beyond the viewport all belonged to one of those local scrollers;
the count of uncontained overflow elements was zero. No responsive media
overflow was present. The temporary viewport override was reset after the
measurements.

## PDF structure and accessibility

- Metadata: title `Topologi Aljabar - Unit 1-28`, A4, 334 pages,
  `/Lang=id-ID`, zero page rotation, no encryption, form, widget, JavaScript
  name tree, JavaScript annotation action, additional action, or suspect flag.
- All 447 annotations are links: 327 ordinary internal `GoTo` actions and 120
  URI actions. The catalog `/OpenAction` is an ordinary `/GoTo` destination
  fitted to the opening page, not executable code.
- The 27 PDF font objects are all embedded, subset, and mapped with
  `/ToUnicode`.
- Structural tagging is honestly absent (`/Marked=false` and no
  `/StructTreeRoot`). The self-contained reflowable HTML remains the primary
  accessible surface.
- Normalized extracted text from pages 325-334 contains the exact model note,
  source-author credit, Unit 28 heading, boundary to Unit 29, and source cursor
  6053. It contains no credential marker, placeholder, or local user path.

This review covers every page newly contributed by Unit 28 and the title and
transition surfaces. It does not claim manual reinspection of unchanged
interior pages from the separately frozen Units 001-027 baseline.
