# Units 001-005 visual QA

Date: 2026-08-22

Verdict: **PASS**

## Frozen artifacts inspected

- Semantic HTML: `output/html/units-001-005/index.html`, 610,594 bytes, SHA-256 `8d3accf480101565409909c05f987f44b73f1c98889128e2f5074a4e049f48f3`.
- Secondary PDF: `output/pdf/topologi-aljabar-unit-001-005-id.pdf`, 589,065 bytes, SHA-256 `d6929434a9bc7ae78fb71fc060e9cc54dce85d37e4997ffe042ccbab982e64e2`.
- PDF geometry: A4, 44 pages, 21 mm cumulative-only margins, 11 pt body text.

## PDF review

The final PDF was rendered with Poppler at 105 dpi. All 44 rendered pages were inspected in five ordered contact sheets, with the final page also inspected at full-page scale. The first 23 mm cumulative build had a 45th page containing only the last equation and one sentence of Solution 5.4. A bounded layout correction changed only this new cumulative builder to 21 mm margins. The resulting 44-page build keeps comfortable whitespace, moves the complete Solution 5.4 onto a coherent final page, and remains byte-reproducible across two fixed-epoch builds.

No clipping, overlap, overfull visible content, broken formula, missing glyph, blank object, accidental blank page, or isolated continuation page remains. Title, contents, all five unit transitions, semantic block styling as expressed in PDF, page numbers, and the complete Unit 5 mastery section are legible and consistently aligned.

## Responsive HTML review

The local embedded reader was inspected in the Codex in-app browser at desktop 1280 x 720 and mobile 390 x 844.

- Desktop: the body is 928 px wide (`max-width: 58rem`), centered within the 1,265 px content viewport with a 0.06 px rounding delta; there is no page-level horizontal overflow.
- Mobile: the body reflows to 375.11 px within the 375 px content viewport with a 0.06 px rounding delta; there is no page-level horizontal overflow.
- All 30 Unit 5 stable IDs are present in the rendered DOM.
- All 1,659 mathematics nodes remain native MathML.
- Seventeen formulas exceed the mobile inline width; all 17 are contained by local horizontal-scroll surfaces. Maximum local overflow is 261 px, while document-level overflow remains zero.
- There are no script elements, no external stylesheet links, and no browser console warnings or errors.

The desktop title/contents surface and the mobile title/contents and Unit 5 proof opening were visually inspected. Text remains readable, the reader is centered, navigation wraps cleanly, semantic blocks retain visible distinction, and wide mathematics scrolls locally rather than widening or clipping the page.

## Accessibility disposition

The semantic HTML with `lang="id-ID"`, native MathML, stable anchors, reflow, and formula-local scrolling is the primary accessible surface. The PDF is intentionally secondary and untagged; it has embedded fonts with ToUnicode maps and a verified UTF-8 text witness.
