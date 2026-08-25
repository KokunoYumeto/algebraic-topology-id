# Visual QA — Roberts 001–030 + Fomberg 001–004

Date: 2026-08-25  
Status: **PASS**  
Model provenance: OpenAI Codex gpt-5.6-sol, Ultra

## Frozen reader artifacts

The exact reader identities at this boundary are:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `output/html/roberts-001-030-fomberg-001-004/index.html` | 8,155,605 | `cd620d5557ff05fb81fb9cf044e8bd4848a6f92ef8fcd06078b8a124f6e79326` |
| `output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-004-id.pdf` | 3,964,018 | `bbe4b2392991ace6922230374833bf0982e00a8b6d2fddb94a990b663c8440bf` |

Independent `pdfinfo` inspection reports 424 A4 pages, PDF 1.5,
unencrypted, unrotated, with no forms, JavaScript, or suspect objects.
`Tagged: no` is disclosed as a limitation; the reflowable, self-contained HTML
is the primary accessible reader.

## PDF visual inspection

Poppler rendered every newly added cumulative-boundary page, PDF pages
398–424, at 120 dpi. All 27 individual renders and five contact sheets were
inspected. Pages 399, 412, 414, 422, 423, and 424 were additionally inspected
at original render resolution for the three new raster diagrams, dense
mathematics, mastery solutions, and the terminal cursor.

Result: zero observed clipping, overlap, margin collision, orphaned heading,
unreadable glyph, or unreadable-mathematics defects across pages 398–424. The
three Unit 004 diagrams, their captions and semantic explanations, proof
repairs, displayed sequences, and all seven exercise/hint/solution triples are
legible and remain inside the intended page area.

The render inventory is
`qa/ROBERTS_001_030_FOMBERG_001_004_RENDER_INVENTORY.csv`: 5,422 bytes,
SHA-256
`51e504fbd50968a290d6ac40c2eced605fc314d31d0600c1e5cb295fcf56e94f`.
It records 32 inspected files totalling 16,745,653 bytes.

## HTML browser inspection

Fresh in-app-browser QA used the exact final HTML identity above from a
task-local HTTP server. The test tab was closed and the temporary viewport
override was reset afterward.

### Desktop

- Viewport: 1,440 × 900 CSS pixels; document client/scroll width:
  1,425/1,425 pixels.
- Body width: 1,152 pixels; measured center delta: −0.0556 pixels.
- 2,109 DOM IDs, all unique; 407 fragment links, all resolved.
- 14,396 MathML nodes, nine embedded raster images, and zero images outside
  the viewport.
- The centered reader and table of contents are visually clean.

### Mobile

- Viewport: 375 × 812 CSS pixels; document client/body/scroll width:
  360/360/360 pixels.
- No document-level horizontal overflow and zero exposed overflow elements.
- All nine images remain within bounds.
- 408 intrinsically wide mathematics/table surfaces retain localized
  horizontal scrolling rather than widening the page.
- Zero external runtime asset references and zero browser warning/error logs.
- The title, attribution, table of contents, and body text reflow legibly.

## Boundary conclusion

The complete new PDF page range and both responsive HTML layouts pass. The
fixed-page artifact is visually sound, and the primary HTML reader is
centered on desktop, fills the phone viewport, preserves local scrolling for
wide mathematics, and has no exposed page-level overflow.
