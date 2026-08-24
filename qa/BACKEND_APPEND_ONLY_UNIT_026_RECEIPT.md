# Unit 026 semantic backend append-only receipt

Date: 2026-08-24  
Status: **PASS**

## Immutable prefix

The exact cumulative Units 001--025 backend remains the byte prefix of every
live backend file: **3,913 records**, **4,007,903 bytes**, bundle SHA-256
`8b50629f25c5fcbedb6d5547f8f7151c622aa90e04f71583008bd176058a4f78`.
No pre-existing byte was rewritten or reordered.

## Unit 026 semantic suffix

The transaction appended **192 canonical JSONL records**: 3 artifacts, 1
source asset, 8 locale-neutral concepts, 13 source/edition corrections, 3 QA
events, 28 relations, 3 component/cumulative rights records, 62 segments, 8
Indonesian term attestations, and 63 units (one reader root plus the 62 stable
reader IDs). The live cumulative backend now contains **4,105 records** and
**4,305,218 bytes**, bundle SHA-256
`89556c5fa2224820837fc8956b1a48797929f28bef013baf9a613e73e6cf28eb`.

The per-file prefix and final identities are fixed by
`qa/BACKEND_APPEND_ONLY_UNIT_026_FILE_MANIFEST.csv`.

## Bound source and closure

- Authority: Roberts `Notes.tex:5612-5823`, 9,763 LF bytes, SHA-256
  `52663b3e60d5d6f3041b8ede449c52a04700ee670c201ef5674c4aa3973203a9`.
- Reader: `source/id-ID/units/unit-026-lecture-026.md`, 38,537 bytes,
  1,201 LF lines, SHA-256
  `7a2cf4ea31546b8258e3e91c819d3ad516973c8f861249fccc7334b9ade9d835`.
- Evidence: exact source audit, independent review, and PASS QA JSON are
  registered as backend artifacts; open review counts are P1=0, P2=0, P3=0.
- Structure: 62 stable IDs have a unit/segment bijection and exact target-span
  hashes; both source aliases are preserved; the terminal cursor is line 5824.
- Learning closure: nine proof objects, six exact exercise/hint/checked-solution
  triples, the Unit 24 long-exact-sequence dependency, and the prism proof of
  homotopy invariance are explicitly related.
- Rights and provenance: Roberts CC BY 4.0, edition-original CC BY 4.0,
  independent non-endorsement, and `OpenAI Codex gpt-5.6-sol, Ultra` remain
  component-distinguishable. No upstream contact occurred.

The independent semantic validator passed against the final live tree. This
transaction did not change control files, the reader/audit/review/QA witnesses,
HTML/PDF outputs, Git, publication state, another unit, or upstream material.
