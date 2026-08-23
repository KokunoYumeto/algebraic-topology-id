# Units 001–022 cumulative backend receipt

Date: 2026-08-23  
Status: **PASS**  
Scope: exact cumulative builder, HTML, PDF, manifest, build receipt, visual
receipt, QA events, relations, and final built-rights pointer only.

This receipt supersedes the Unit 22 semantic admission receipt as the current
backend boundary; it does not invalidate that earlier evidence:

- `qa/BACKEND_APPEND_ONLY_UNIT_022_RECEIPT.json` — 5,703 bytes, SHA-256
  `1ab81c3d1f79fb2e6ca4231014eb0473ced50b5e136444cc3d59138eef5f6e06`;
- `qa/BACKEND_APPEND_ONLY_UNIT_022_RECEIPT.md` — 3,518 bytes, SHA-256
  `1d722546edc13675159554bc602c6732fa1df5eb2431830500d37679f2a5e556`.

## Immutable prefix and append

The complete Unit 22 semantic backend remained byte-for-byte unchanged:

- 3,322 records;
- 3,166,412 bytes;
- ordered-file bundle SHA-256
  `2329606117578210ce927123ec01639390f2e493fcc995899606eaa38996f2bc`.

The transaction appended exactly 15 canonical sorted records: six artifact
records, two QA events, six relations, and one final built-rights pointer.
No source, asset, authority, concept, correction, segment, term, or unit record
was appended.

## Cumulative build witnesses

| Witness | Bytes | SHA-256 |
|---|---:|---|
| `scripts/build-units-001-022.ps1` | 18,956 | `6d3ada82dbc5afbcec8b394c64694e392ceae55db165a8363d88b8c57b1464b7` |
| `output/html/units-001-022/index.html` | 3,520,527 | `15938aac7515e4ad7de66f8cf2d825744f9eb08b654165b835bfeace31aef8f4` |
| `output/pdf/topologi-aljabar-unit-001-022-id.pdf` | 1,728,316 | `5dabcbdc98fdc7203ca2fe4f42aff86b9e3cb761136f676e0dd43b350768fb77` |
| `output/ARTIFACT_MANIFEST_UNITS_001_022.csv` | 249 | `3a79a520d0281504edd2449fdfd13c5a874ec675f8187a9e6cb516a760ef35c8` |
| `qa/UNITS_001_022_BUILD_RECEIPT.json` | 5,315 | `347569120a698d2738472fb6d194fa6109f8b638b9e16b08c473fc9e793312b5` |
| `qa/UNITS_001_022_VISUAL_QA.md` | 4,747 | `35a5b00b6bdda6b77041ff568f14c91702818be3f939d9e3df36829ae168251b` |

The PDF has 261 A4 pages. Both HTML and PDF two-build byte identities passed;
all 75 Unit 22 IDs survived in HTML, raw-TeX math fallbacks are zero, the
manifest closes exactly over the HTML/PDF readers, and representative visual
QA passed. Provenance remains `OpenAI Codex gpt-5.6-sol, Ultra`.

## Final backend

- records: **3,337**;
- bytes: **3,176,534**;
- ordered-file bundle SHA-256:
  `38b98ca6258133036ded9e3cb72894f4181d4b6faa46af9e96a2128ab25c9df2`.

| File | Records | Bytes | SHA-256 |
|---|---:|---:|---|
| `artifacts.jsonl` | 116 | 91,395 | `05a9525a470df9a106ad785a026b45f8913c1dfc40d363eff12df5cea3d0a58e` |
| `assets.jsonl` | 24 | 14,831 | `69020caaf45628941c57ee5cf58f3c11a31505c3416ec9d65c9ac82b47ba97aa` |
| `authority.jsonl` | 4 | 2,721 | `f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368` |
| `concepts.jsonl` | 297 | 93,358 | `2e8f93bfa8b7622960716b8a6bd33811c630c877696c5cbf031cb14eadfa110b` |
| `corrections.jsonl` | 302 | 295,241 | `718a14732930b546a3c38bf2e131d23066b2f90f09d4dd80a781294296f5cbc6` |
| `qa.jsonl` | 104 | 59,176 | `b8c439539b4bd566bb3b46423e19ab925f2cbcb8075a77b5df6a76ba7b9cf516` |
| `relations.jsonl` | 309 | 124,723 | `2d58a794206f07915c18c98c220e143354429c57d14bc93f27eb1806a2277ab6` |
| `rights.jsonl` | 59 | 53,720 | `f734f3649cc4e8a40ec7d63bd92843c1d04cf835d46f9fcef9224168a9142bd2` |
| `segments.jsonl` | 905 | 1,094,552 | `491b68e826f0221353d7a7782515be769fc8048e468bba5937c797ca0390bb8c` |
| `terms.jsonl` | 290 | 177,339 | `bf1c79fc4bbaf0a9bd71545f4d69d9dc36dcb728f23710ad33a9bf9791421695` |
| `units.jsonl` | 927 | 1,169,478 | `56fdf925d6e547b4a936d4ac7fb483cdbd9d845ac292989a7162efae108fcf8f` |

## Transaction evidence

- Producer `scripts/append-cumulative-unit-022-artifacts.py`: 15,610 bytes,
  285 lines, SHA-256
  `5724ad79fd24e0b00e617e456d98928d57e1f2c4551e5892135335c349847176`.
- Independent validator
  `scripts/validate-backend-append-only-unit-022-cumulative.py`: 13,799
  bytes, 249 lines, SHA-256
  `c3b4c65205e4743693f4f8b9f6120b6df0a1cf14ec95a2ad60fee4eaa7726c1e`.
- Validator result: **PASS** for exact prefix, suffix scope/order, schema,
  references, artifacts, manifest rows, build/visual QA, reproducibility,
  rights, and final bundle.

