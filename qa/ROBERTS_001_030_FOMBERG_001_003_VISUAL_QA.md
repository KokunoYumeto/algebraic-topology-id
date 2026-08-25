# Visual QA — Roberts 001–030 + Fomberg 001–003

Date: 2026-08-25  
Status: **PASS**
Model provenance: OpenAI Codex gpt-5.6-sol, Ultra

## Frozen reader artifacts

The identities below were read from
`output/ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_003.csv` at this
boundary.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `output/html/roberts-001-030-fomberg-001-003/index.html` | 7,190,228 | `484a2a501df79b1810567810d0b454a18298a4cb43ef466c4e082622216b9542` |
| `output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-003-id.pdf` | 3,550,987 | `57382750a561667bf02eb98bd7f4806618c3a785f4ca18ceb4c6679c46543b4b` |

Independent `pdfinfo` inspection reports 397 A4 pages, PDF 1.5,
unencrypted, and `Tagged: no`. The absence of PDF tagging is recorded here and
is not represented as an accessibility feature.

## PDF visual inspection

Poppler rendered every new cumulative-boundary page, PDF pages 377–397. The
render inventory contains all 21 individual page renders and four contact
sheets. The contact sheets were inspected in full, with additional full-size
inspection of pages 386, 387, and 397 for the densest new figure, mathematics,
and terminal-boundary layouts.

Result: zero observed clipping, overlap, or unreadable-glyph defects across
pages 377–397. The six Unit 003 figures, surrounding prose, displayed
mathematics, headings, page margins, and terminal page remain readable and
inside their intended page areas.

## HTML browser inspection

Fresh in-app browser QA was performed against the final HTML identity above.

### Desktop

- Viewport: 1440 × 900 CSS pixels; document client width: 1,425 pixels.
- Body width: 1,152 pixels; centered with measured center delta −0.0556 pixels.
- Document scroll width: 1,425 pixels; no exposed horizontal overflow.
- DOM census: 1,983 IDs, 385 fragment links, 13,466 MathML elements, and 6 figures.
- Browser console: zero warnings and zero errors.
- Desktop screenshot: visually clean.

### Mobile

- Viewport: 375 × 812 CSS pixels; document client width: 360 pixels.
- Body width and document scroll width: 360 pixels; no exposed document-level
  horizontal overflow.
- All 6 of 6 images remain within bounds.
- 370 wide elements retain localized horizontal scrolling rather than widening
  the document.
- Mobile screenshot: visually clean.

## Boundary conclusion

The final HTML and PDF are bound to the hashes above. The complete new PDF
page range and both responsive HTML layouts pass the recorded visual checks,
with no observed clipping, overlap, unreadable glyphs, broken figure bounds,
or page-level horizontal overflow.
