# Visual QA - cumulative Units 001-003

Date: 2026-08-22
Artifact: `output/pdf/topologi-aljabar-unit-001-003-id.pdf`
Artifact SHA-256: `2c9bf67e74c94bca9aad0238e910816188a957892a6cf811f7f615e221b4066d`

## Scope and method

All 25 physical A4 pages were rendered with Poppler at 110 dpi. Pages 1-5, 6-10, 11-15, 16-20, and 21-25 were inspected as five ordered contact sheets. Pages 16, 18, 21, 22, and 25 were also inspected individually at full rendered resolution because they contain the Unit 3 transition, dense piecewise or categorical formulas, the solved-mastery transition, or the final-page boundary.

## PDF result

PASS. No clipping, overlap, margin escape, missing glyph, broken formula, blank object, accidental blank page, or orphaned terminal page was observed. The contents page is legible; unit, section, exercise, and mastery transitions remain visually distinct; all displayed formulas remain within the text area. Page 25 contains the substantive conclusion of Solusi Latihan 3.5 and is not an orphan page. The PDF is A4, unencrypted, contains no JavaScript or form, embeds all fonts, exposes `/Lang` as `id-ID`, and is intentionally untagged. The self-contained HTML with native MathML remains the primary accessibility surface.

## Browser and responsive result

PASS. The cumulative HTML was loaded from a local HTTP origin in the Codex in-app Chromium browser and inspected at 1280 x 720 and 390 x 844 viewports. At desktop width the 928 px reading column was centered within the 1265 px document viewport (center delta below 0.1 px after accounting for the scrollbar). At mobile width it reflowed to the 375 px document viewport with zero page-level horizontal overflow. All 109 stable IDs were present with no duplicates; all 41 local fragment links resolved; all 1007 native MathML elements loaded; no scripts, images, external stylesheets, console errors, or warnings were present.

The title/contents, Unit 3 opening, and Unit 3 solved-mastery section were visually inspected at desktop and mobile sizes and remained centered, readable, and structurally distinct. At the mobile breakpoint, 12 formulas were wider than their local boxes and all 12 exposed `overflow-x: auto`; no non-math element overflowed. This keeps wide mathematics locally scrollable without widening the page.
