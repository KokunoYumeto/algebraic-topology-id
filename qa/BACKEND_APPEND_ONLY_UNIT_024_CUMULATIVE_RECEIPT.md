# Units 001--024 cumulative backend append-only receipt

Date: 2026-08-24  
Status: **PASS**

## Frozen semantic prefix

The complete Unit 24 semantic backend was preserved byte-for-byte in every
JSONL file:

- records: **3,706**;
- bytes: **3,714,904**;
- bundle SHA-256:
  `b0a182615e96995b6afa9ad0d8b25f221b9ad6fb58feca01b284b08211db1066`.

## Cumulative build append

The transaction added exactly **17** canonical records: seven build/QA
artifacts, two passed QA events, seven relations, and one final built-rights
pointer. It changed no source, terminology, adverse ledger, unit, segment,
concept, correction, asset, control, Git, publication, or upstream record.

The resulting backend contains **3,723 records** and **3,726,427 bytes**.
Bundle SHA-256:
`ffa8c7cb45b6d8170d7bc83df24ec487fd0c2777297b55eff2d5e7b3ae63fe25`.

## Bound artifacts

- deterministic builder: 21,976 bytes, SHA-256
  `8e62da597b783f56e0a9174a7822ee453de6de8be01fc5493cb2ab93c41a3c44`;
- self-contained HTML: 3,927,104 bytes, SHA-256
  `28a84406de9e196070965920a7f7937177197977f9ddf118f0f8b07d464cbf0f`;
- 286-page PDF: 1,907,368 bytes, SHA-256
  `5189b04f2f28d7e8192c16e8ef070e23bbf98085d150d1f2124d15c071ccf9b8`;
- two-row manifest: 249 bytes, SHA-256
  `23d2b33dd8eb08ba82bb020e3607abbf24925d79e774ca177be228656800a0ff`;
- build receipt: 7,560 bytes, SHA-256
  `a050b3d282d43033ccdd7565bc6ee301eee6c30014ef6d8b84c5ec490406129a`;
- visual receipt: 4,928 bytes, SHA-256
  `7aff942b47ec489a56923879aee189fc3911e0eded232a511de66aff8ee01a27`;
- 15-row render inventory: 2,659 bytes, SHA-256
  `1d9554d98de7d4751fc7ee2d1b5a6cb45edb580e62226b030aea389dff9de683`.

## Independent validation

The validator reconstructed and hashed the semantic prefix; checked every
final JSONL identity and sorted transaction suffix; re-parsed the build
receipt, exact manifest, visual receipt, and render inventory; checked the
seven artifact records, two QA witness closures, seven relations, 24-unit
rights scope, two-build reproducibility, 60 Unit 24 IDs, 286-page boundary,
responsive reflow, and absence of raw-math, unresolved-fragment, and external
runtime fallbacks. Result: **PASS**.

Producer: `scripts/append-cumulative-unit-024-artifacts.py`, 18,251 bytes,
SHA-256
`d212969036b86f0b0cba84cf49fe057896c13d8b34a0364a248a5a10ff1fa1dc`.

Validator: `scripts/validate-backend-append-only-unit-024-cumulative.py`,
16,052 bytes, SHA-256
`920afabdcff3f8228caeab41f57e2cca973e41502a5abb08b33d755083566fcc`.

Model/process provenance: OpenAI Codex gpt-5.6-sol, Ultra.
