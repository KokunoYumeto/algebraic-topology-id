# Unit 025 semantic backend append-only receipt

Date: 2026-08-24  
Status: **PASS**

## Immutable prefix

The transaction preserved the complete cumulative Units 001--024 backend as
an exact byte prefix in every JSONL table:

- records: **3,723**;
- bytes: **3,726,427**;
- bundle SHA-256:
  `ffa8c7cb45b6d8170d7bc83df24ec487fd0c2777297b55eff2d5e7b3ae63fe25`.

No prefix record was rewritten, reordered, deleted, or superseded in place.

## Unit 025 semantic append

The producer admitted **173** records: 3 evidence artifacts, 1 canonical
source asset, 6 locale-neutral concepts, 10 correction records, 3 QA events,
22 relations, 3 rights records, 59 segments, 6 Indonesian term records, and
60 units (the reader root plus one unit for each of 59 stable reader IDs). No
cumulative HTML, PDF, build, publication, release, or output artifact was
added.

The resulting backend contains **3,896 records** and **3,996,359 bytes**.
Bundle SHA-256:
`55372b9c2853fa479e731c73c407b234ad2f1219e07efbedbad2a99f1e2abf47`.

## Source, topology, and closure

- Frozen authority span: `Notes.tex:5370--5611`, 12,732 LF bytes, SHA-256
  `d05781ae58b1b6fd6174d030e52ca9ee6a08048be96f7c103e5be8de473b60b0`.
- Reader: `source/id-ID/units/unit-025-lecture-025.md`, 36,578 bytes,
  1,104 LF lines, SHA-256
  `df72add4e57236b51ff7d2a0c99af4b65299365874163cb334be5d0988c0f769`.
- Stable structure: 59 unique IDs, 52 fenced objects, and an exact
  unit/segment bijection for every stable ID under route `D60-R13`.
- Four complete proof closures and six problem/hint/full-solution triples are
  linked explicitly. Source label
  `eg:dim_minus_one_skeleton_rel_cochains` resolves to the stable Unit 25
  example.
- The exact next source cursor is `Notes.tex` line **5612**.

## Controls and validation

Terminology controls `O012-TERM-0323` through `O012-TERM-0328` and adverse
controls `O012-ADV-0332` through `O012-ADV-0341` map one-to-one into the
backend. `O012-ADV-0341` transparently records the independently found and
pre-admission-resolved `UNIT025-TERM-P3-001`: the draft's `simplicial` was
changed to the admitted lane form `simpleksial`, with the corrected reader,
review, and PASS QA identities bound above.

The independently implemented validator checked the immutable prefix and
final identities, canonical and sorted JSONL suffixes, global references,
reader span hashes, hierarchy and sibling order, route/model bindings, source
alias resolution, proof/mastery relations, rights, ledgers, evidence files,
the resolved terminology finding, and the terminal cursor. It returned
**PASS**.

Producer: `scripts/extend-backend-unit-025.py`, 37,829 bytes, 708 LF lines,
SHA-256
`8eec9cc135c96df1c2ea403edea22ccf13e38810f7b4acff46c6a6ba28905230`.

Validator: `scripts/validate-backend-append-only-unit-025.py`, 19,589 bytes,
359 LF lines, SHA-256
`aacd0f797989cb10ea664d27af8c16e854a22ee90990e5b00b8b038eaebf2664`.

Model/process provenance: OpenAI Codex gpt-5.6-sol, Ultra.
