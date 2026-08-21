# Visual QA — cumulative Units 001–002

Date: 2026-08-21
Artifact: `output/pdf/topologi-aljabar-unit-001-002-id.pdf`
Artifact SHA-256: `0413c3a3280955cc482a5c0c2d7615b78128dccba3b6b1901dee1bf34d133b8e`

## Scope and method

All 15 physical A4 pages were rendered with Poppler at 110 dpi. Pages 1–5, 6–10, and 11–15 were inspected as three ordered contact sheets; pages 10, 11, 12, 13, 14, and 15 were also inspected individually at full rendered resolution because they contain the densest formulas, the Unit 2 transition, or the final-page boundary.

## Result

PASS. No clipping, overlap, margin escape, missing glyph, broken formula, blank object, accidental blank page, or orphaned terminal page was observed. The contents page is legible; section and mastery transitions are visually distinct; long coproduct, contraction, product, and piecewise formulas remain within the text area. Page 15 contains the substantive final solution and is not an orphan page.

The PDF is intentionally secondary and untagged. The cumulative self-contained HTML with native MathML is the primary accessibility surface.

## Browser and responsive review

The cumulative HTML was also loaded from a local HTTP origin in the Codex in-app Chromium browser and inspected at 1280×720 and 390×844 viewports. At desktop width the 928 px reading column was centered (equal computed left and right margins); at mobile width it reflowed to the available page width. Both viewports had no page-level horizontal overflow, no duplicate HTML IDs, all 621 native MathML nodes, and all 41 Unit 2 stable IDs. Wide display formulas use local `overflow-x: auto`, so they scroll within their formula blocks rather than widening the page. The contents page and the Unit 2 solved-mastery section were visually inspected at both scales and remained readable.
