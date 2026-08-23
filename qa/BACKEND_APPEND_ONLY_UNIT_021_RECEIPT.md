# O012 Unit 021 backend append-only receipt

Date: 2026-08-23  
Status: PASS

## Boundary

The verified Units 001–020 backend is an immutable 2,959-record prefix:
2,738,760 bytes, bundle SHA-256
`7abd10e468c5f8b75853a67fcfb67d09f0470720fa88efcc84f5c3647cbb1fe5`.
The Unit 021 producer checked every per-file prefix count, byte length, and
SHA-256 before writing. It appended 137 canonical records and did not rewrite
any historical byte.

The new backend contains 3,096 records and 2,886,546 JSONL bytes. Its bundle
SHA-256 (lexical filename order, filename + NUL + file bytes) is
`84920281207fc4088aa4f1f812d78333fd530e9f157eeebaa3b09cbfb53b431d`.

## Unit 021 authority

- Upstream: `Notes.tex:4346–4500`, 7,267 span bytes, SHA-256
  `281ba27f0f52f35fd9842954c223546e84ce1a0909ee84c14b2081c38c11f150`.
- Indonesian reader: `source/id-ID/units/unit-021-lecture-021.md`, 26,237
  bytes, 786 LF lines, SHA-256
  `47fa3994dc59370fc464e9d150d62512a4602a3cffa5996f1027f93a427e0eec`.
- Stable semantic IDs: 47. Next upstream cursor: line 4501.
- Terminology controls: `O012-TERM-0290` through `O012-TERM-0292`.
- Adverse/correction controls: `O012-ADV-0290` through `O012-ADV-0297`;
  upstream disposition remains `not_contacted`.

## Records appended

| JSONL file | Previous | Added | Current | Current SHA-256 |
|---|---:|---:|---:|---|
| artifacts.jsonl | 96 | 4 | 100 | `f52ad11802bb22255344b1a01b35378a69f6d4eb26cfae3e1abe4890082a85bd` |
| assets.jsonl | 22 | 1 | 23 | `623f8d7948504405fb8f57379987136e5f89297f0152f3eb9408cab6a3ed153c` |
| authority.jsonl | 4 | 0 | 4 | `f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368` |
| concepts.jsonl | 286 | 3 | 289 | `b05d4ec9646338ea76991eb08d5a260a087699a76d51fde507b0c5583b5921bb` |
| corrections.jsonl | 280 | 8 | 288 | `7c06a04c7072051d28879297291d37bccca70c132339c8226e889701dc1de835` |
| qa.jsonl | 94 | 3 | 97 | `621ec0d75a3307b8acec242220c0fc39c06a4c978c89378405b4f9661f569c79` |
| relations.jsonl | 261 | 17 | 278 | `a262f8db2f816e7a1155b5749e1b18199bb1d62b7e232e9e8ee9ba365e3dbc3d` |
| rights.jsonl | 51 | 3 | 54 | `f217f667ddb845de00ce819f6facefdef0247305968d209d4b2422cdb25108b0` |
| segments.jsonl | 783 | 47 | 830 | `e3fc479798493bad011f36e302cd4da7b0daa48f45252d7095dc10adc50b3530` |
| terms.jsonl | 279 | 3 | 282 | `f6bb58da10c5970087c4ff2074b25163a3a3bd6e0f820f9df0782a4e00490deb` |
| units.jsonl | 803 | 48 | 851 | `7851c5a529337802a6eb62f7aa51d107c38e18ecf8299fcfc86d6dc5b87c46a6` |

## Validation

`scripts/validate-backend-append-only-unit-021.py` passed exact prefix
immutability, canonical/sorted suffixes, generic shapes, references, artifact
manifests, source locators and content hashes, stable-ID bijection, hierarchy,
six mastery hint/solution closures, terminology, correction, rights, artifact,
QA, and final-bundle checks. `scripts/qa-unit-021.py` independently passed.

No Unit 021 source, controls, ledger, build output, Git state, release file, or
publication destination was changed by this backend task.
