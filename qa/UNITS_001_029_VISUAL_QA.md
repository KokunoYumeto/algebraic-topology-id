# Units 001-029 cumulative visual and responsive QA

Status: **PDF PASS; live desktop/mobile HTML geometry PASS.**

The final deterministic reader is 343 A4 pages, 2,211,479 bytes, SHA-256
`0a140fbfb48960fa178b3409bd6cca03c2819fedec4c84e12486f662dac9a317`.
Pandoc 3.9.0.2 and MiKTeX-pdfTeX 4.27 (MiKTeX 26.5) produced two
byte-identical PDF outputs under `SOURCE_DATE_EPOCH=1787529600`.

## Complete new-span PDF inspection

Poppler 24.04.0 rendered the title page and **every PDF page containing Unit
29** at 144 dpi and 1,191 by 1,684 pixels. The inspected set is exactly pages
**1 and 334-343**. Page 334 is the Unit 28-to-29 transition: it closes the
comparison-map solution and exact Unit 28 boundary, then contains the complete
Unit 29 provenance. Unit 29 continues through page 343 and closes there with
the exact source cursor for Unit 30.

All 11 rendered PNGs were inspected at original resolution. Their exact page
coverage, byte counts, dimensions, and SHA-256 identities are recorded in
`qa/UNITS_001_029_RENDER_INVENTORY.csv`, 2,233 bytes, SHA-256
`10c0c9ea2780a171ac629c7e76ed9ce4e94810beff8e0c93db3098b398df76c4`.
The render witnesses total 2,867,137 bytes. They were removed only after the
inventory and inspection result were sealed; every witness is reproducible
from the final PDF, page number, Poppler version, dpi, and recorded hash.

No inspected page has clipping, overlap, missing or broken glyphs, unreadable
mathematics, positional-figure dependence, an orphaned heading, or a collision
with a margin or page number. In particular:

- page 1 has a centered title and balanced three-line expanded subtitle, with
  authorship, date, and opening contents inside the A4 text area;
- page 334 preserves the complete Unit 28-to-29 transition and all Unit 29
  source, rights, correction, and provenance statements without crowding;
- pages 335-336 preserve comparison naturality, both complete five-term rows,
  the relative comparison factor, and the finite-dimensional theorem with all
  arrows and subscripts readable;
- page 337 preserves the Five Lemma close, all-Delta-set extension including
  stabilization in degrees `k` and `k-1` and the Milnor `lim^1` term, the
  practical consequences, and the CW opening;
- pages 338-340 preserve the CW filtration and pushout, the semantic attachment
  figure, manifold qualification, typed CW pairs and homotopy categories, and
  all four Eilenberg-Steenrod clauses with no reflow loss;
- pages 341-343 contain all six problem/hint/full-solution triples without
  clipping or bottom-margin collision; and
- page 343 closes with the axiom-recognition solution and exact boundary to
  Unit 30 at source cursor 6271, followed by adequate whitespace.

## Reflowable HTML verification

The final self-contained HTML is 4,751,974 bytes, SHA-256
`67e5dd915cbbdf9b1961368efb1538b9ce0da8a4596d7ade11a4af051a189167`.
Two independent Pandoc outputs were byte-identical. Structural inspection
found 11,519 native MathML nodes (1,991 display and 9,528 inline), 64 semantic
figures, 1,597 unique DOM IDs, zero duplicate IDs, 330 fragment links with
zero unresolved targets, zero raw-TeX fallback, zero external runtime
dependency, `lang="id-ID"`, an explicit document title and TOC role, exact
model provenance, and all 49 Unit 29 IDs.

The in-app browser loaded the local final reader successfully with zero console
errors or warnings. At a requested 1,440 by 900 viewport, the root content
width was 1,425 pixels (the remaining 15 pixels were the vertical scrollbar),
the body was exactly 1,152 pixels wide, and its measured left/right margins
were 136.444/136.556 pixels. Root horizontal overflow and elements crossing
the viewport were both zero.

At a requested 390 by 844 mobile viewport, the layout engine reported a
375-pixel root content width, a full-width 375.111-pixel body with 17.6-pixel
side padding, and zero root horizontal overflow. Of 11,519 MathML nodes, 243
were genuinely wider than their own content boxes: 241 display and two inline.
All 243 exposed local horizontal scrolling. The 2,117 descendant boxes that
extended beyond the viewport all belonged to one of those local scrollers;
the count of uncontained overflow elements was zero. No responsive media
overflow was present. The temporary viewport override was reset after the
measurements.

## PDF structure and accessibility

- Metadata: title `Topologi Aljabar - Unit 1-29`, A4, 343 pages,
  `/Lang=id-ID`, zero page rotation, no encryption, form, widget, JavaScript
  name tree, JavaScript annotation action, additional action, or suspect flag.
- All 461 annotations are links: 336 ordinary internal `GoTo` actions and 125
  URI actions. The catalog `/OpenAction` is an ordinary `/GoTo` destination
  fitted to the opening page, not executable code.
- The 27 PDF font objects are all embedded, subset, and mapped with
  `/ToUnicode`.
- Structural tagging is honestly absent (`/Marked=false` and no
  `/StructTreeRoot`). The self-contained reflowable HTML remains the primary
  accessible surface.
- Normalized extracted text from pages 334-343 contains the exact model note,
  source-author credit, Unit 29 heading, boundary to Unit 30, and source cursor
  6271. It contains no credential marker, placeholder, or local user path.

This review covers every page newly contributed by Unit 29 and the title and
transition surfaces. It does not claim manual reinspection of unchanged
interior pages from the separately frozen Units 001-028 baseline.
