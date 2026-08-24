# Unit 024 semantic backend append-only receipt

Date: 2026-08-24  
Status: **PASS**

## Immutable prefix

The transaction preserved the complete Units 001--023 cumulative backend as
an exact byte prefix in every JSONL table:

- records: **3,528**;
- bytes: **3,434,879**;
- bundle SHA-256:
  `0c8b27890f8423fc3224c89f2bcf60ed6cbcb9d93fabef7b53c399784f0aaaef`.

No prefix record was rewritten, reordered, deleted, or superseded in place.

## Unit 024 semantic append

The producer admitted **178** records: 3 artifacts, 1 source asset, 7 new
locale-neutral concepts, 9 correction records, 3 QA events, 24 relations, 3
rights records, 60 segments, 7 Indonesian term records, and 61 units (the
reader root plus one unit for each of 60 stable reader IDs). No cumulative
HTML, PDF, build, publication, or release artifact was added.

The resulting backend contains **3,706 records** and **3,714,904 bytes**.
Bundle SHA-256:
`b0a182615e96995b6afa9ad0d8b25f221b9ad6fb58feca01b284b08211db1066`.

## Source and topology closure

- Frozen authority span: `Notes.tex:5113--5369`, 12,837 LF bytes, SHA-256
  `b2128930a56a0a8c04c327a397e72e21b215ffe742bb684e8dd166f0e04b0aea`.
- Reader: `source/id-ID/units/unit-024-lecture-024.md`, 43,085 bytes,
  1,156 LF lines, SHA-256
  `993ad0c3493caff6bd15ab2bcf435f6cbb1f49ed9a1e11bc1009d649ae2d3647`.
- Stable structure: 60 unique IDs, 50 fenced objects, one unit/segment
  bijection for every stable ID, route `D60-R13` throughout.
- The example left open in Unit 23 is explicitly resumed at source line 5113
  and closed at line 5121. The next exact source cursor is line 5370.
- Six complete proof closures and six problem/hint/full-solution triples are
  linked explicitly.

## Controls, evidence, and validation

Terminology controls `O012-TERM-0316` through `O012-TERM-0322` and adverse
controls `O012-ADV-0323` through `O012-ADV-0331` map one-to-one into the
backend. Existing controls for short/long exact sequences, kernels, cokernels,
complex morphisms, relative simplicial cochains, and connecting maps are reused
without duplication.

The backend binds the frozen Unit 024 audit, independent review, and PASS QA
JSON. The independently implemented validator checked final and prefix file
identities, canonical JSONL, global references, target-span hashes, aliases,
hierarchy/order, continuation closure, route bindings, proof/mastery closure,
terms, corrections, rights, and evidence files. It returned **PASS**.

Producer: `scripts/extend-backend-unit-024.py`, 38,551 bytes, SHA-256
`2c093e176d968f00802c7d263115337e421158f9bbc2d94956bd9ff9bdd58898`.

Validator: `scripts/validate-backend-append-only-unit-024.py`, 23,062 bytes,
SHA-256
`83ceb0dde71256632fa958712bcfd582d61c383485e7469520ed0ba1e38826a2`.

Model/process provenance: OpenAI Codex gpt-5.6-sol, Ultra.
