# Visual QA — Roberts 001–030 + Fomberg 001–005

Date: 2026-08-25  
Status: **PASS**  
Model provenance: OpenAI Codex gpt-5.6-sol, Ultra

## Frozen reader artifacts

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `output/html/roberts-001-030-fomberg-001-005/index.html` | 8,353,769 | `d726c8d8a565172fb620233080f60e2ccbde4386d6fa03b099bf6219645aea90` |
| `output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-005-id.pdf` | 4,035,750 | `b0b0441ae16ad0065dc50dfc3ba36df49932efbdf939dc048cd332dc881f931a` |

Independent `pdfinfo` inspection reports 437 A4 pages, PDF 1.5,
unencrypted, unrotated, with no forms, JavaScript, or suspect objects.
`Tagged: no` is disclosed as a limitation; the reflowable, self-contained HTML
is the primary accessible reader. All 27 fonts are embedded, subset, and carry
ToUnicode maps. The nine historical raster images retain exactly nine matched
soft masks; Unit 005 adds no raster asset.

## PDF visual inspection

Poppler rendered the Unit 004/005 seam and every new page, PDF pages 424–437,
at 120 dpi, as well as title/contents pages 1–6. All 20 individual renders and
three contact sheets were inspected. Pages 425, 428, 430, 432, and 437 were
also inspected at original render resolution for the component boundary,
hairy-sphere proof, semantic local-degree diagram, local-to-global proof, dense
mathematics, mastery solutions, and terminal cursor.

Result: zero observed clipping, overlap, margin collision, orphaned heading,
broken or unreadable glyph, or unreadable-mathematics defect. The page-424/425
transition is clean. The semantic diagram reflows as mathematics rather than a
raster, the complete FOM-PR-12 repair is legible, and all six
exercise/hint/full-solution triples remain inside the intended page area.

The render inventory is
`qa/ROBERTS_001_030_FOMBERG_001_005_RENDER_INVENTORY.csv`: 3,895 bytes,
SHA-256
`f58946ef221b289d5f0c443acc057c7a7da864a3cfa70316135937c8fda69b50`.
It records 23 inspected files totalling 9,899,021 bytes.

## HTML browser inspection

Fresh in-app-browser QA used the exact final HTML bytes from a task-local HTTP
server.

### Desktop

- Viewport: 1,440 × 900 CSS pixels; document client/scroll width:
  1,425/1,425 pixels.
- Body width: 1,152 pixels; measured center delta: −0.0556 pixels.
- 2,169 live DOM IDs, all unique; 423 fragment links, all resolved.
- All 476 cumulative Fomberg IDs are present, including all 52 Unit 005 IDs.
- 14,883 MathML nodes, 135 semantic figures, nine embedded raster images, and
  zero images outside the viewport.
- The table-of-contents link to `o012-composite-fomberg-005` was activated and
  resolved to the visible Unit 005 boundary. The centered reader is visually
  clean at that boundary.

### Mobile

- Viewport: 375 × 812 CSS pixels; document client/body/scroll width:
  360/360/360 pixels.
- No document-level horizontal overflow; the body fills the usable viewport.
- All nine images remain within bounds.
- 423 intrinsically wide mathematics/table surfaces retain localized
  horizontal scrolling rather than widening the page.

The browser connection reset after these required layout, identity, link, and
navigation measurements, so a redundant console-log query and mobile
screenshot were not repeated. This does not weaken the runtime-closure result:
the exact HTML has no external runtime asset dependency or executable script,
the document width is exact at both tested breakpoints, every fragment resolves,
and Unit 005 introduces no new external asset.

## Boundary conclusion

The full new PDF page range and both responsive HTML layouts pass. The print
artifact is visually sound, and the primary HTML reader is centered on desktop,
fills the phone viewport, preserves local scrolling for wide mathematics, and
has no page-level horizontal overflow.
