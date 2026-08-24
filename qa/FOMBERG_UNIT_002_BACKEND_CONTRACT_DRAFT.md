# Independent backend-contract review — Fomberg Unit 002

Date: 2026-08-24  
Verdict: **PASS**

## Frozen review boundary

- Reader: `source/id-ID/fomberg/units/fomberg-unit-002-singular-homology-homotopy-invariance.md`; 44,407 bytes; 1,342 LF lines; SHA-256 `0851ab7d9f5ded1e836a0e73aa055fbd28b82998208d8136ec0cf4757747435c`.
- Backend constructor: `scripts/fomberg-unit-002-common.py`; 46,896 bytes; SHA-256 `5398d2aa1a791892d573d8d26bff0a4af35d8468399b1c1988617f72c5645f01`.
- Authority span: `algebraic_topology.tex` lines 615–1290; 676 lines; 22,924 bytes with preserved LF; SHA-256 `9b28e159825e020b262a51b9c50372b2fafc26270fab6480d860aaaeefdda84f`; exact next cursor line 1291, `\subsection{Exact sequences}`.
- Source audit: 297,184 bytes; SHA-256 `1f0d9772761b7fb1dbc56f8e714aa92826e6a089fed2b53b29513821d9b1054d`.
- Static QA: 24,692 bytes; SHA-256 `4845a7717196b7caaa9e22f35fe5f17b1db2a90bbef16d7e01e9f8ec1cae82e8`.
- All three independent reader reviews bind the final reader hash, state `PASS`, and carry exact `FINAL_SEVERITY_COUNTS` of `{"P1":0,"P2":0,"P3":0}`.

This was a read-only reconstruction. No backend writer, Git command, network operation, or build was run.

## Immutable-prefix and append-only checks

The live Unit 001 backend prefix matched every frozen per-file record count, byte count, and SHA-256. All 5,060 prefix records are canonical LF-only JSONL with globally unique IDs. The exact prefix is 5,658,648 bytes with bundle SHA-256 `17f57575a062025e434e79f7f3797d05de1a41e520202521ae39a409d4b6450d`.

The Unit 002 suffix was reconstructed in memory twice from the frozen reader, authority, controls, and five evidence files. Every file-local suffix is canonically serialized and lexically ordered by ID; it contains no prefix mutation, global ID collision, private absolute path, credential marker, or premature publication claim. Generic `validate-backend.py` shape and reference rules pass over the resulting 5,342-record cumulative graph.

| Backend file | Added records |
|---|---:|
| `artifacts.jsonl` | 5 |
| `assets.jsonl` | 2 |
| `authority.jsonl` | 0 |
| `concepts.jsonl` | 7 |
| `corrections.jsonl` | 31 |
| `qa.jsonl` | 4 |
| `relations.jsonl` | 34 |
| `rights.jsonl` | 2 |
| `segments.jsonl` | 95 |
| `terms.jsonl` | 7 |
| `units.jsonl` | 95 |
| **Total** | **282** |

Both JSON receipts' exact `record_ids_by_file`, artifact paths in physical record order, record counts, root/edition/course/resource identities, and 282-record total equal the derived suffix. The producer enforces this before append and immediately before mutation; the read-only validator repeats it for both its initial and refreshed reconstructions.

## Semantic-record checks

All 95 reader anchors map one-to-one to 95 units and 95 paired segments. Their parent references, complete paths, contiguous sibling orders, stable IDs, target line spans, full-file hashes, and per-span content hashes are exact. The five-heading and 90-fenced-object census agrees with the frozen class inventory, including 14 semantic figures and six complete exercise–hint–solution triples.

The root architecture matches the immutable Unit 001 convention:

- `unit:o012-fom-u002` covers the complete 1–1342 reader and carries composite provenance and composite CC BY-SA 4.0 rights;
- `segment:o012-fom-u002` isolates the translated source body at lines 37–1022 and carries Fomberg-source provenance and rights;
- the mastery heading ends at line 1336, while the independently indexed continuation boundary begins at line 1337.

The provenance/rights partition is internally consistent. Units comprise 59 source-derived records, 32 ordinary edition-original records, three edition-original proof repairs, and one composite root. Segments comprise 60 source-derived records (including the source-body root segment), 32 ordinary edition-original records, and three proof repairs. In particular, the three source-omission notices remain source-derived, while the corresponding complete repairs remain separately identified original companion material. Every audit evidence record agrees exactly with the emitted unit/segment target locators, provenance relations, and rights component IDs.

All seven terms and seven locale-neutral concepts bind admitted controls `O012-TERM-0394` through `O012-TERM-0400`; every preferred Indonesian form occurs in its cited evidence segment. All 31 correction records bind exactly to resolved adverse-ledger entries `O012-ADV-0426` through `O012-ADV-0456`, retain the ledger text and disposition, and resolve every affected-unit and evidence-segment reference.

The 34 relations close as follows: one `adapts`, two `contains`, two `precedes`, three `proves`, six `hints`, six `solves`, and fourteen `illustrates`. The fourteen semantic-figure relations bind the diagram asset whose independently checked source-format census is exactly 13 `tikzcd` plus one `tikzpicture`. The five artifacts match their live path, byte count, media type, and SHA-256; the four QA events resolve to those witnesses. Both new rights records preserve CC BY-SA 4.0, component scoping, attribution/change notices, and non-endorsement.

## Findings

```json
{"P1":0,"P2":0,"P3":0}
```

No unresolved contract defect remains at this frozen boundary. **PASS**.
