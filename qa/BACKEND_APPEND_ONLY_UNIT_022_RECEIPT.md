# Unit 022 append-only backend receipt

Date: 2026-08-23  
Status: **PASS**  
Scope: frozen Unit 22 semantic/source/rights/QA admission only; no cumulative
build, release, publication, source, control, cursor, or current-state change.

## Immutable boundary

The producer and the independent validator both proved that every byte of the
public Units 001–021 backend remained an immutable prefix:

- records: **3,111**;
- bytes: **2,896,429**;
- ordered-file bundle SHA-256:
  `cf5acacf3ad2351869297dd8d3827787377422fa30c8c1385e60833b23913db9`.

The transaction appended 211 canonical records: 4 artifacts, 1 source asset,
8 concepts, 14 corrections, 3 QA events, 19 relations, 3 rights records,
75 segments, 8 terms, and 76 units. `authority.jsonl` received no record.

## Frozen evidence

- Indonesian source: `source/id-ID/units/unit-022-lecture-022.md` — 44,066
  bytes, 1,349 LF lines, 75 stable IDs, SHA-256
  `0857e51568d77c811d5d79255ac75bfddc87a04b27356ae457d4e66eeffb7d0d`.
- Authority: Roberts `Notes.tex:4501–4938` — 20,585 bytes, SHA-256
  `86275c590cfcdf8519d3ce8d077fc48619bb94c3fdf039ca805ae4b7df995b7f`.
- Terminology closure: `O012-TERM-0293..0300`.
- Adverse/correction closure: `O012-ADV-0298..0311`.
- The complete signed-cancellation proof for the upstream `Exercise!` locus is
  component-marked as edition-original and linked to Lemma 22.3.
- All six mastery problems have exactly one hint and one complete solution.
- Model/process provenance: `OpenAI Codex gpt-5.6-sol, Ultra`.

## Final backend

- records: **3,322**;
- bytes: **3,166,412**;
- ordered-file bundle SHA-256:
  `2329606117578210ce927123ec01639390f2e493fcc995899606eaa38996f2bc`.

| File | Records | Bytes | SHA-256 |
|---|---:|---:|---|
| `artifacts.jsonl` | 110 | 86,473 | `5d16598495a6df0a0855f6c413cc78def50cf653d30c6699bcef5b5455cb72ea` |
| `assets.jsonl` | 24 | 14,831 | `69020caaf45628941c57ee5cf58f3c11a31505c3416ec9d65c9ac82b47ba97aa` |
| `authority.jsonl` | 4 | 2,721 | `f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368` |
| `concepts.jsonl` | 297 | 93,358 | `2e8f93bfa8b7622960716b8a6bd33811c630c877696c5cbf031cb14eadfa110b` |
| `corrections.jsonl` | 302 | 295,241 | `718a14732930b546a3c38bf2e131d23066b2f90f09d4dd80a781294296f5cbc6` |
| `qa.jsonl` | 102 | 57,849 | `86591e4710dcf61a1cc29c1ad94187b5d4bd362f4df8d9e7d63ac14bbb88dfaf` |
| `relations.jsonl` | 303 | 122,094 | `8c28ab28cfbe752f32c95746355dde648fa7b005d0f1d4550c3933e1d804fa28` |
| `rights.jsonl` | 58 | 52,476 | `2aaf92fd5c0853ddaea495ca7e3a20caba6de445193d9f5888e38523bc359434` |
| `segments.jsonl` | 905 | 1,094,552 | `491b68e826f0221353d7a7782515be769fc8048e468bba5937c797ca0390bb8c` |
| `terms.jsonl` | 290 | 177,339 | `bf1c79fc4bbaf0a9bd71545f4d69d9dc36dcb728f23710ad33a9bf9791421695` |
| `units.jsonl` | 927 | 1,169,478 | `56fdf925d6e547b4a936d4ac7fb483cdbd9d845ac292989a7162efae108fcf8f` |

## Deterministic transaction

- Producer: `scripts/extend-backend-unit-022.py` — 33,107 bytes, 616 lines,
  SHA-256
  `f0950038713c4ed9bbfeb08588ec5a237f561237f446efa04cdf8c3785cf7a2e`.
- Independent validator:
  `scripts/validate-backend-append-only-unit-022.py` — 17,313 bytes, 316
  lines, SHA-256
  `3ca78febd9181e0d8a83c6e3d1616bbf73312e823c38128d46b2b4e2148d0761`.
- Validator result: **PASS**; generic schema, reference, artifact-manifest,
  exact-prefix, canonical-suffix, stable-ID/locator, hierarchy, rights,
  terminology, correction, proof, and mastery closure all passed.
- Cumulative build artifacts added: **0**.

