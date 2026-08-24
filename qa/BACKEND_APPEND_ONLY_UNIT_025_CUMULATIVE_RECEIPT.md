# Units 001--025 cumulative backend append-only receipt

Date: 2026-08-24  
Status: **PASS**

## Nested immutable boundaries

The independent validator proved both inherited layers byte-for-byte before
checking the cumulative suffix:

1. Units 001--024 cumulative prefix: **3,723 records**, **3,726,427 bytes**,
   bundle SHA-256
   `ffa8c7cb45b6d8170d7bc83df24ec487fd0c2777297b55eff2d5e7b3ae63fe25`.
2. Unit 25 semantic boundary: **3,896 records**, **3,996,359 bytes**, bundle
   SHA-256
   `55372b9c2853fa479e731c73c407b234ad2f1219e07efbedbad2a99f1e2abf47`.

The semantic boundary is independently sealed by
`qa/BACKEND_APPEND_ONLY_UNIT_025_RECEIPT.json`, 6,957 bytes, SHA-256
`7814c3586ab5e25989ddbed45ab8569d8406fb9022c5fa52e74e5b8b1aef37aa`.
No record in either inherited layer was rewritten, reordered, or deleted.

## Cumulative build append

The cumulative transaction added exactly **17** canonical records: seven
artifact records, two PASS QA events, seven relations, and one final
CC BY 4.0 rights pointer. The final backend contains **3,913 records** and
**4,007,903 bytes**. Bundle SHA-256:
`8b50629f25c5fcbedb6d5547f8f7151c622aa90e04f71583008bd176058a4f78`.

The seven exact witnesses are:

- builder: `scripts/build-units-001-025.ps1`, 21,986 bytes, SHA-256
  `d346b18845f8fc9314ae588fc7877d38275110ab23c60f10b7bad649bc3371c2`;
- HTML: `output/html/units-001-025/index.html`, 4,112,563 bytes, SHA-256
  `38cd8437f3b4235ac6269f4e3365123fa06485269d35a424ad4f5ddd589025c1`;
- PDF: `output/pdf/topologi-aljabar-unit-001-025-id.pdf`, 1,972,209 bytes,
  298 A4 pages, SHA-256
  `581d62162633a6624687517c5cf1595f5fc02a2701c2222b279711e0520b9a3f`;
- manifest: `output/ARTIFACT_MANIFEST_UNITS_001_025.csv`, 249 bytes,
  SHA-256
  `37175a8d7023bf394c50c4809122b1f3244b5d0b1b95a3b724bdb2ff184ab142`;
- build receipt: `qa/UNITS_001_025_BUILD_RECEIPT.json`, 7,729 bytes,
  SHA-256
  `dd2fa5b52ed84ac939c33cfa5b9f68be4b904b014321abcb54c2ae664d0f9727`;
- visual receipt: `qa/UNITS_001_025_VISUAL_QA.md`, 4,804 bytes, SHA-256
  `ae49496b676472f6c69a3468cc76c323c45905ce7ed86a048ce11556079137a3`;
- render inventory: `qa/UNITS_001_025_RENDER_INVENTORY.csv`, 2,731 bytes,
  SHA-256
  `a55ff205e621fbc750baaf086fa18883c72dba5bdfe1f66e4554247d22fdc12f`.

The task packet called the manifest
`output/units-001-025-manifest.sha256`; that path does not exist. The live
build receipt and exact 249-byte witness identify the CSV path above. The
transaction binds the primary artifact and records this supplied-path
correction rather than inventing a file.

## Build and accessibility evidence

HTML and PDF repeat builds are byte-identical. The self-contained HTML has
1,361 unique IDs, 296 resolving fragments, 10,118 native MathML nodes, 62
semantic figures, no raw-math fallback, and no external runtime dependency.
Desktop and mobile tests have zero uncontained overflow; wide mathematics is
losslessly contained in local scrollers.

The PDF is A4 with `/Lang=id-ID`; all 27 reported font rows are embedded,
subset, and Unicode-mapped. It is honestly untagged, so the reflowable HTML is
the primary accessible surface. Every Unit 25 page plus the title and
transition pages passed visual inspection.

Final rights pointer:
`rights:o012-units-001-025-composite-cc-by-4.0-final-df72`. It supersedes the
semantic source-stage pointer while preserving component attribution,
CC BY 4.0, and non-endorsement.

Producer: `scripts/append-cumulative-unit-025-artifacts.py`, 19,321 bytes,
357 LF lines, SHA-256
`b7572851e6798591abbc4e119573f3ded4050d827dd6c749eea50c33f599bbbf`.

Independent validator:
`scripts/validate-backend-append-only-unit-025-cumulative.py`, 18,551 bytes,
316 LF lines, SHA-256
`1ef5f15a91f662abc61540007813039fe14b29dc92e224d47dea1249241f4c27`.

Model/process provenance: OpenAI Codex gpt-5.6-sol, Ultra.
