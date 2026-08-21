# Unit 001 visual QA

Date: 2026-08-21 (Europe/Berlin)

Target: `output/pdf/topologi-aljabar-unit-001-id.pdf`

- PDF: 321,743 bytes; SHA-256 `6f71546a616c02ef81f8747ecfce3875784842065fc131cc82e5060b066a59c9`
- Render command: `pdftoppm -png -r 120 -f 1 -l 5`
- Scope: all 5 physical pages, not a sample.
- Verdict: PASS.

## Page inventory

| Page | Render bytes | SHA-256 |
|---:|---:|---|
| 1 | 179,919 | `b2ad976bcf52d870a5596708105d00838df4daa313f20adc4960500c026a8422` |
| 2 | 296,144 | `32a82ca9795902daf7d2375c13a992abf509bcaba4a0466ed6ec891d6f800313` |
| 3 | 340,585 | `0e3ed49752c4db4958361dbc5f20270d85213632b400d36d5dd8c61e676a17e0` |
| 4 | 280,499 | `ebd664127812bff65d5dca93fb6413aea903b4a0f04126b492aaa457ba2900ea` |
| 5 | 199,250 | `6a9efe7a836a9673ab11dfac4e4c3362a4dc2835e7dee08c77f4ba3474e641f8` |

## Observations

- Title, attribution, contents, source/core boundary, and mastery boundary are legible.
- Mathematics, lists, headings, and hyperlinks remain inside the printable area.
- No clipping, overlap, missing glyph, blank object, or accidental empty page was seen.
- The prior nearly empty sixth page was removed by changing the deterministic A4 build margin from 26 mm to 23 mm; the final fifth page now contains a substantial continuous block and ends cleanly.
- Page balance is acceptable. The remaining lower whitespace on page 5 is normal for the end of a bounded unit and does not create an orphan fragment.
- PDF remains a secondary, untagged surface. The semantic, native-MathML HTML reader is the primary accessibility surface.
