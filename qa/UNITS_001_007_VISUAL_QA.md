# Units 001-007 visual QA

Date: 2026-08-22

Verdict: **PASS**

## Frozen artifacts reviewed

- HTML: `output/html/units-001-007/index.html`, 899,803 bytes, SHA-256 `55135048eafe0f097c45936add885e008392eefdf475270fea37adf6a2a7b7bb`.
- PDF: `output/pdf/topologi-aljabar-unit-001-007-id.pdf`, 702,470 bytes, 66 A4 pages, SHA-256 `3764b75ecfb9200e25a165db1f0f97a680384378e2a9a22e129aab57dd860d93`.
- Build: Pandoc 3.9.0.2; PDF produced by MiKTeX pdfTeX 1.40.29 at the fixed source epoch; two independent HTML builds and two independent PDF builds were byte-identical.

## Complete PDF review

Poppler rendered all 66 pages at 110 dpi. Six contact sheets covered pages 1-11, 12-22, 23-33, 34-44, 45-55, and 56-66, so no page was omitted. Pages 1, 45, 57, and 66 were additionally inspected at full rendered size because they are the title/contents surface, the Unit 6 opening, the Unit 7 opening, and the terminal page.

The review found no clipped line, formula, heading, link, or page number; no overlap, missing glyph, black box, blank page, isolated continuation page, or excessive underfull terminal sheet; and no broken unit transition. Unit 6 begins cleanly on page 45 after Unit 5 ends on page 44. Unit 7 begins cleanly on page 57 after the Unit 6 proof ends on page 56. Page 66 contains the substantive end of Solution 7.4 and closes without an orphan page. The 21 mm cumulative-only margins remain readable throughout.

The PDF is intentionally a secondary, untagged surface. Font inspection reports 23 embedded, subsetted fonts, all with Unicode mappings. The semantic HTML is the primary accessibility surface.

## Responsive HTML review

The local standalone HTML was inspected in the Codex in-app Chromium browser. No browser warning or error was recorded.

At 1280 by 720 CSS pixels, the document client width was 1,265 px and the body was exactly 928 px (`58rem`) wide. Its left and right outer spaces were 168.444 px and 168.556 px (0.111 px rounding delta), and document-level horizontal overflow was zero. All 135 semantic blocks had a visible left border and background treatment; theorem, corollary, and remark blocks therefore follow the same explicit visual grammar as the pre-existing definition, proposition, lemma, example, exercise, proof, note, and question blocks.

At 390 by 844 CSS pixels, the browser's content width was 375 px, the body reflowed to that full width with 17.6 px side padding and no box shadow, and document-level horizontal overflow remained zero. Of 382 display-math elements, 32 were wider than their local box; all 32 exposed local horizontal scrolling through `overflow-x: auto`, so wide formulae did not widen the page. Both the title/contents and the Unit 7 reading surface were visually inspected at this viewport.

The rendered HTML has `lang="id-ID"`, 2,344 native MathML nodes, no scripts, no external stylesheet or runtime asset, 315 unique HTML IDs, all 89 local fragment links resolving, all 224 edition stable IDs present, and exactly one preserved `data-source-label="eg:piS^1_infinite"` alias.

## Disposition

No visual repair is required. The cumulative Units 001-007 HTML and PDF pass the boundary's centering, reflow, formula-overflow, legibility, pagination, and accessibility-surface checks.
