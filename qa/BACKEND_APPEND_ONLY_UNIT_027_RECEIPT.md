# Unit 027 semantic backend append-only receipt

Date: 2026-08-24  
Status: **PASS**

## Immutable prefix

The exact Units 001--026 cumulative semantic backend remains the byte prefix
of every live backend file: **4,105 records**, **4,305,218 bytes**, bundle
SHA-256
`89556c5fa2224820837fc8956b1a48797929f28bef013baf9a613e73e6cf28eb`.
No earlier byte was rewritten or reordered.

## Unit 027 suffix

The transaction appended **159 canonical JSONL records**: 3 artifacts, 1
source asset, 8 locale-neutral concepts, 16 source/edition corrections, 3 QA
events, 24 relations, 3 rights records, 46 segments, 8 reviewed term
attestations, and 47 units. The live backend now contains **4,264 records** and
**4,532,994 bytes**, bundle SHA-256
`09aa16e8d9387171445c4d465d00a5399e39517a210cb347e30d2d285c703f8c`.

The exact per-file prefix and final identities are fixed by
`qa/BACKEND_APPEND_ONLY_UNIT_027_FILE_MANIFEST.csv`.

## Bound closure

- Authority: Roberts `Notes.tex:5824-5923`, 7,012 LF bytes, SHA-256
  `65d2c393ddf29183f36d6e9ab65c65f8030110334f89c7f68ba88461fc30afa1`.
- Reader: 35,879 bytes, 1,175 LF lines, SHA-256
  `a3238bbc429e4c3689bce3b3bb78c5514e0fae74f276c9efebe694730b2df2a0`.
- Structure: 46 stable IDs have exact unit/segment pairs and target-span
  hashes; four source aliases and the Xy-pic semantic reflow are preserved.
- Learning closure: three proof blocks and six exact exercise/hint/checked-
  solution triples, including the preserved and solved source exercise.
- The corrected small-chain comparison, Mayer--Vietoris dependency chain,
  sphere calculation, 16 correction records, and cursor line 5924 are explicit.
- Roberts CC BY 4.0, edition-original CC BY 4.0, non-endorsement, and
  `OpenAI Codex gpt-5.6-sol, Ultra` remain component-distinguishable.

The independent semantic validator passed. This transaction changed no
control file, reader/audit/review/QA witness, HTML/PDF output, Git or
publication state, another unit, or upstream material.
