# Units 001-027 cumulative visual and responsive QA

Status: **PDF PASS; live desktop/mobile HTML geometry PASS.**

The final deterministic reader is 325 A4 pages, 2,108,928 bytes, SHA-256
`c001b170d7f3bf3554e507350ef2c29652d265c0661c8cdcf407113f843705d7`.
Pandoc 3.9.0.2 and MiKTeX-pdfTeX 4.27 (MiKTeX 26.5) produced two
byte-identical PDF outputs under `SOURCE_DATE_EPOCH=1787529600`.

## Complete new-span PDF inspection

Poppler 24.04.0 rendered the title page and **every PDF page containing Unit
27** at 144 dpi and 1,191 by 1,684 pixels. The inspected set is exactly pages
**1 and 312-325**. Page 312 is the Unit 26-to-27 transition: it closes the
signed-prism solution and exact Unit 26 boundary, then begins the Unit 27
provenance. Unit 27 continues through page 325 and closes there with the exact
source cursor for Unit 28.

All 15 rendered PNGs were inspected at original resolution. Their exact page
coverage, byte counts, dimensions, and SHA-256 identities are recorded in
`qa/UNITS_001_027_RENDER_INVENTORY.csv`, 2,892 bytes, SHA-256
`f57b3d4e775b9c2314897e9d60d96294be01c6a3b24cb9e8721b971568b314ee`.
The render witnesses total 3,760,885 bytes. They were removed only after the
inventory and inspection result were sealed; every witness is reproducible
from the final PDF, page number, Poppler version, dpi, and recorded hash.

No inspected page has clipping, overlap, missing or broken glyphs, unreadable
mathematics, positional-figure dependence, an orphaned heading, or a collision
with a margin or page number. In particular:

- page 1 has a centered title and balanced two-line subtitle, with authorship,
  date, and opening contents inside the A4 text area;
- page 312 preserves the complete Unit 26-to-27 transition and begins the
  exact source, rights, and provenance statement without crowding;
- pages 313-316 preserve the model/process disclosure, source exercise and
  solution, typed evaluation repair, splitting lemma, canonical reduced
  degree-zero theory, and the semantic pushout diagram;
- pages 317-320 preserve the corrected small-cochain model and map direction,
  the complete small-chain proof, both long exact sequences, the
  Mayer--Vietoris connector, and the expanded exactness proof;
- page 321 contains the hemisphere calculation and complete sphere-cohomology
  recurrence with all wide displays readable;
- pages 322-325 contain all remaining problem/hint/full-solution triples
  without a split or bottom-margin collision; and
- page 325 closes with the noncontractibility argument and exact boundary to
  Unit 28 at source cursor 5924, followed by adequate whitespace.

## Reflowable HTML verification

The final self-contained HTML is 4,504,569 bytes, SHA-256
`d98c2c29344e1e3cc3e81863e426fbf775ca6b70c0a5534d888d80ad2269486d`.
Two independent Pandoc outputs were byte-identical. Structural inspection
found 11,000 native MathML nodes (1,907 display and 9,093 inline), 63 semantic
figures, 1,484 unique DOM IDs, zero duplicate IDs, 313 fragment links with
zero unresolved targets, zero raw-TeX fallback, zero external runtime
dependency, `lang="id-ID"`, exact model provenance, and all 46 Unit 27 IDs.

The in-app browser loaded the local final reader successfully. At a requested
1,440 by 900 viewport, the root content width was 1,425 pixels (the remaining
15 pixels were the vertical scrollbar), the body was exactly 1,152 pixels
wide, and its measured left/right margins were 136.444/136.556 pixels. Root
horizontal overflow and elements crossing the viewport were both zero.

At a requested 390 by 844 mobile viewport, the layout engine reported a
375-pixel root content width, a full-width 375.111-pixel body with 17.6-pixel
side padding, and zero root horizontal overflow. Of 11,000 MathML nodes, 228
were genuinely wider than their own content boxes: 226 display and two inline.
All 228 exposed local horizontal scrolling. The 1,826 descendant boxes that
extended beyond the viewport all belonged to one of those local scrollers;
the count of uncontained overflow elements was zero. No responsive media
overflow was present. The temporary viewport override was reset after the
measurements.

## PDF structure and accessibility

- Metadata: title `Topologi Aljabar - Unit 1-27`, A4, 325 pages,
  `/Lang=id-ID`, zero page rotation, no encryption, form, widget, JavaScript
  name tree, JavaScript annotation action, additional action, or suspect flag.
- All 434 annotations are links. The catalog `/OpenAction` is an ordinary
  `/GoTo` destination fitted to the opening page, not executable code.
- The 27 PDF font objects are all embedded, subset, and mapped with
  `/ToUnicode`.
- Structural tagging is honestly absent (`/Marked=false` and no
  `/StructTreeRoot`). The self-contained reflowable HTML remains the primary
  accessible surface.
- Normalized extracted text from pages 312-325 contains the exact model note,
  source-author credit, Unit 27 heading, boundary to Unit 28, and source cursor
  5924. It contains no credential marker, placeholder, or local user path.

This review covers every page newly contributed by Unit 27 and the title and
transition surfaces. It does not claim manual reinspection of unchanged
interior pages from the separately frozen Units 001-026 baseline.
