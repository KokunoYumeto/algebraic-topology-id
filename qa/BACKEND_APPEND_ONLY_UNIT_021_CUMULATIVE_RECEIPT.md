# O012 Units 001–021 cumulative backend receipt

Date: 2026-08-23  
Status: **PASS**  
Supersedes as the current boundary:
`qa/BACKEND_APPEND_ONLY_UNIT_021_RECEIPT.json` and
`qa/BACKEND_APPEND_ONLY_UNIT_021_RECEIPT.md`. Those source-stage receipts
remain immutable historical evidence.

## Append-only boundary

The complete Unit 021 source backend—3,096 records, 2,886,546 bytes, bundle
SHA-256
`84920281207fc4088aa4f1f812d78333fd530e9f157eeebaa3b09cbfb53b431d`—
was verified byte-for-byte as the immutable prefix.

The cumulative transaction appended 15 canonical records:

- six artifacts: deterministic builder, HTML, PDF, manifest, build receipt,
  and visual receipt;
- two passed QA events: deterministic build and representative visual QA;
- six relations: manifest closure, build boundary, builder dependency, and QA
  witnesses;
- one final cumulative rights pointer, preserving CC BY 4.0 attribution,
  component-level provenance, and non-endorsement.

The builder is included as an artifact because the build receipt identifies it
as the exact fail-closed, two-build reproducibility mechanism. It is 17,129
bytes with SHA-256
`f0678ae5af4d08059747106a9711a3a63139dc3782a36de28d2041643e075eec`.

## Final backend identity

- Records: **3,111**.
- JSONL bytes: **2,896,429**.
- Bundle SHA-256:
  `cf5acacf3ad2351869297dd8d3827787377422fa30c8c1385e60833b23913db9`.

| JSONL file | Immutable prefix | Added | Final records | Final bytes | Final SHA-256 |
|---|---:|---:|---:|---:|---|
| artifacts.jsonl | 100 | 6 | 106 | 83,103 | `1708f7276cb28e295d578c8e4411618291c7294c8faee863c89461c63378a978` |
| assets.jsonl | 23 | 0 | 23 | 14,215 | `623f8d7948504405fb8f57379987136e5f89297f0152f3eb9408cab6a3ed153c` |
| authority.jsonl | 4 | 0 | 4 | 2,721 | `f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368` |
| concepts.jsonl | 289 | 0 | 289 | 90,816 | `b05d4ec9646338ea76991eb08d5a260a087699a76d51fde507b0c5583b5921bb` |
| corrections.jsonl | 288 | 0 | 288 | 280,684 | `7c06a04c7072051d28879297291d37bccca70c132339c8226e889701dc1de835` |
| qa.jsonl | 97 | 2 | 99 | 56,340 | `249c2f6110269d1daef7fff472e4fb17c2f7060b8cd39f662884fd8bba0f0145` |
| relations.jsonl | 278 | 6 | 284 | 114,295 | `3a1b930dbe14992819fcaeca39edb96e915641e62247a2e7ea879809a998c2e9` |
| rights.jsonl | 54 | 1 | 55 | 49,832 | `1dca76e63699015d393009a8ed263ea4f1adb4e9be3a9668aae8e19bdcf55524` |
| segments.jsonl | 830 | 0 | 830 | 982,695 | `e3fc479798493bad011f36e302cd4da7b0daa48f45252d7095dc10adc50b3530` |
| terms.jsonl | 282 | 0 | 282 | 171,661 | `f6bb58da10c5970087c4ff2074b25163a3a3bd6e0f820f9df0782a4e00490deb` |
| units.jsonl | 851 | 0 | 851 | 1,050,067 | `7851c5a529337802a6eb62f7aa51d107c38e18ecf8299fcfc86d6dc5b87c46a6` |

## Frozen cumulative artifacts

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `output/html/units-001-021/index.html` | 3,306,661 | `aec7e94d3697a7feeae87134da983c59faaf29dc8d961bca28b6bfa9c53cdfa6` |
| `output/pdf/topologi-aljabar-unit-001-021-id.pdf` | 1,645,350 | `aee3f74109bafd1614d01d6593b8b2edbcbfdbf3b841b6beee878a01d7ddec16` |
| `output/ARTIFACT_MANIFEST_UNITS_001_021.csv` | 249 | `40386b62066854272e8902c1f2c886a78de2c98f0dce845cbf6179c845bf1498` |
| `qa/UNITS_001_021_BUILD_RECEIPT.json` | 3,850 | `e3afdb61c3787eac1b84601609a89eadb34e9eee5b9c5481ba18c5e441a51032` |
| `qa/UNITS_001_021_VISUAL_QA.md` | 3,350 | `f42bc668ab68a3f05993ac4d56a565160f4a94a417f656dd3f29f1e12475c6fa` |

The PDF has 246 A4 pages. HTML and PDF passed two-build byte identity; the
representative seven-page visual inspection passed after the documented
builder-only multiline-link repair. Unit 021 source bytes were not changed.

## Validation

`scripts/validate-backend-append-only-unit-021-cumulative.py` passed exact
prefix immutability, canonical and sorted suffixes, generic shapes and
references, manifest closure, artifact identities, QA content, rights scope,
relation closure, and final bundle identity. The hardened
`scripts/qa-unit-021.py` independently passed with SHA-256
`6039f254104d713c31f95650b627135154e08541a7d596643118977447002837`.

No source, terminology/adverse ledger, current-state cursor, Git state, release
file, or publication destination was modified by this transaction.
