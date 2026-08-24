# Units 001-026 cumulative visual QA

Status: **PDF PASS; static HTML PASS; live browser geometry NOT RUN because no
browser surface was available.** The unrun browser-only measurements are
disclosed rather than inferred from CSS.

The final deterministic reader is 311 A4 pages, 2,042,637 bytes, SHA-256
`27a5a6f2635328dbd3576a92900d110ae627f48da8c514c40f0d94f2d153f19d`.
Pandoc 3.9.0.2 and MiKTeX-pdfTeX 4.27 (MiKTeX 26.5) produced byte-identical
PDFs in two passes under `SOURCE_DATE_EPOCH=1787529600`.

## Complete new-span PDF inspection

Poppler 24.04.0 rendered the title page, the preceding transition page, and
**every PDF page containing Unit 26** at 144 dpi and 1,191 by 1,684 pixels.
The inspected set is exactly pages **1, 298, and 299-311**. Unit 26 begins on
page 299 after the complete Unit 25 boundary on page 298 and closes on page
311 with the exact source cursor for Unit 27.

All 15 rendered PNGs were inspected at original render resolution. The exact
page-by-page coverage, byte count, and SHA-256 inventory is
`qa/UNITS_001_026_RENDER_INVENTORY.csv`, 2,880 bytes, SHA-256
`90bc6d15c91ce36fd266ad752e374449ab54956278b4fc79b6735214b8200d5f`.
The task-local PNG witnesses were removed only after the inventory and this
inspection result were fixed; they remain reproducible from the final PDF,
page numbers, Poppler version, dpi, dimensions, and recorded hashes.

No inspected page has clipping, overlap, missing or broken glyphs, unreadable
mathematics, positional-figure dependence, or collision with the margins or
page number. In particular:

- page 1 has a centered, balanced title and expanded subtitle, with the
  authorship and opening contents fully inside the A4 text area;
- page 298 preserves the complete Unit 25-to-26 boundary without dropping or
  duplicating content;
- pages 299-304 preserve the provenance notice, Stokes display, square-zero
  proof, complete relative long exact sequence, reduced-degree repair, and
  finite-coproduct proof with consistent spacing and readable formulas;
- pages 305-307 preserve all three homotopy corollaries, the cochain-homotopy
  lemma, and the complete signed prism construction and dualisation;
- pages 308-311 contain all six problem/hint/full-solution triples without
  orphaned headings or bottom-margin collisions; and
- page 311 closes with the complete low-degree prism check and exact boundary
  to Unit 27 at source cursor 5824, followed by adequate whitespace.

## Reflowable HTML verification

The final self-contained HTML is 4,306,392 bytes, SHA-256
`a9e4bea73cab5e90136822fbb94a11a1006f7e81ffcdf0a5740da52e335b4e3b`.
Two independent Pandoc outputs were byte-identical. Structural checks found:

- 10,541 native MathML nodes: 1,818 display and 8,723 inline;
- 62 semantic figures;
- 1,431 unique DOM IDs and zero duplicate IDs;
- 306 fragment links, all resolving to internal targets;
- zero raw-TeX math fallback;
- zero external runtime script, stylesheet, frame, or remote image dependency;
- `lang="id-ID"`, exact model provenance, and all 62 Unit 26 IDs present; and
- embedded rules for a centered `min(100%, 72rem)` desktop body, full-width
  mobile body below 700 pixels, global border-box sizing, responsive media,
  and local horizontal scrolling for both display and inline MathML.

The browser-control runtime reported **zero available browser surfaces**.
Consequently no live desktop/mobile layout engine was available to measure
body centering, root scroll width, crossing descendant boxes, or the count of
actually wide local MathML scrollers. This receipt therefore does **not** claim
zero root overflow from static CSS alone. Those browser-only measurements are
the sole unexecuted part of this checkpoint; all source, build, DOM, link,
dependency, and CSS-containment gates passed.

## PDF structure and accessibility

- Metadata: title `Topologi Aljabar - Unit 1-26`, A4, 311 pages,
  `/Lang=id-ID`, no encryption, form, widget, JavaScript name tree,
  additional action, suspect flag, or page rotation.
- Its 422 annotations are links only. The catalog `/OpenAction` is an ordinary
  `/GoTo` destination fitted to the opening page, not executable JavaScript.
- Fonts: 27 distinct PDF font objects; every font is embedded, subset, and
  carries a `/ToUnicode` map.
- Structural tagging is honestly **absent** (`/Marked=false` and no
  `/StructTreeRoot`). The self-contained reflowable HTML remains the primary
  accessible surface.
- Extracted pages 298-311 contain **OpenAI Codex gpt-5.6-sol, Ultra**,
  Roberts's source credit, the Unit 26 heading, the boundary to Unit 27, and
  source cursor 5824. They contain no credential marker, placeholder, or local
  user path.

This review covers every page newly contributed by Unit 26 and representative
title/transition pages. It does not claim manual reinspection of unchanged
interior pages from the separately frozen Units 001-025 baseline.
