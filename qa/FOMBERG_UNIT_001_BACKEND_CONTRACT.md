# Fomberg Unit 001 append-only backend integration contract

Date: 2026-08-24  
Status: design frozen; no backend append performed by this contract  
Scope: Fomberg `algebraic_topology.tex:31-614`, Sections 1.1-1.2, course route `D60-R08`

## Purpose and write boundary

This contract governs the first Fomberg component transaction after the
complete Roberts Units 001-030 semantic boundary. It is an append-only design
for the existing `curriculum.interop` schema version `0.1.0`. The future
producer may append canonical records to the eleven existing JSONL files only
after the reader, audits, ledgers, and QA evidence are final. It may not
rewrite, reorder, truncate, normalize, or regenerate any existing byte.

The canonical reader path is:

`source/id-ID/fomberg/units/fomberg-unit-001-delta-complexes-simplicial-homology.md`

This contract does not authorize reader, ledger, backend, control, Git,
publication, or upstream-contact changes.

## Immutable Roberts prefix

The complete live prefix is exactly 4,761 records and 5,213,679 bytes, with
bundle SHA-256
`51b8c7f611560b9b5e88e97b3a943b54e0eb687c703f0cd34c1a3d164e4fb920`.
The bundle digest is computed in the fixed file order below by hashing each
UTF-8 filename, a NUL byte, and its complete live bytes.

| Backend file | Records | Bytes | SHA-256 |
|---|---:|---:|---|
| `artifacts.jsonl` | 160 | 128,377 | `dcafca44e0fdd9daea5534f9cb6e12ddc85d66e83657cf7905f0c76287d99356` |
| `assets.jsonl` | 34 | 21,271 | `70623b74c22df743708785dd6a213d8086dd4280db983ea14b8f08075b3e8ee6` |
| `authority.jsonl` | 4 | 2,721 | `f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368` |
| `concepts.jsonl` | 364 | 114,998 | `0ba79f3eb7f33775e2fc1e9897de40652522ebb426688617521f226cf5ee159b` |
| `corrections.jsonl` | 407 | 397,287 | `39c7fbc05989e947f4de409ef43b50f55534fecb04d6c662501401c3e295d0d8` |
| `qa.jsonl` | 134 | 75,118 | `2cdfe9c1a159e2d6b1c80e158b16a991814983f07d704c30776c2ccc54108706` |
| `relations.jsonl` | 533 | 218,443 | `cc56f5be615b567baf381505a883b6dd2344f8eaf1318f3f0ec4f5b4d70c418e` |
| `rights.jsonl` | 86 | 79,588 | `2540e545302261e342f8a41211295e7c435e870ad52e267485d4a66f5b439d0e` |
| `segments.jsonl` | 1,326 | 1,912,371 | `054699f1e9d902de23f5dff26d3ecee7b7e1da502fb971468bb17975c7ca65eb` |
| `terms.jsonl` | 357 | 226,725 | `27c19bbacd1fd21fc371b29c64cf7e3b1f37bae6472e3670697830a98279c67f` |
| `units.jsonl` | 1,356 | 2,036,780 | `53b5f8d6a688a71bc7f38f80bda670141109b974742dec7e9428ad43de0f495e` |

The prior cumulative receipt is
`qa/BACKEND_APPEND_ONLY_UNIT_030_CUMULATIVE_RECEIPT.json`, 3,976 bytes,
SHA-256
`d4f7c7310ae22b8fc53d354b72beefad637ac353be418b9fbc56ddd8cd0a65f7`.
The new transaction must bind this receipt and every per-file prefix identity
above before constructing a suffix.

## Frozen component authority

- Resource ID: `resource:fomberg-algebraic-topology-2025`
- Edition ID: `edition:fomberg-at-2025-563194f`
- Edition-unit/root ID: `unit:o012-fom-u001`
- Course ID: `course:o012-d60`
- Route view: `D60-R08`
- Program ID: `program:o012-id`
- Commit: `563194fae879178b9a6871b249513bfc27968975`
- Tree: `fb678966d1533d529bdd72f49d8496a3bdc14a9b`
- Authoring source: `algebraic_topology.tex`
- Notes author: Yeheli Fomberg
- Based on lectures by: Nir Lazarovich
- Source-component license: CC BY-SA 4.0

The edition authority record describes the complete selected component span,
lines 31-4185. The first edition unit binds lines 31-614:

- 584 lines;
- 21,875 bytes preserving LF;
- SHA-256
  `68cb0dea7aa24a42e979877a95acf61b8152c87ed86d88ad7deac7cb5cea2fe3`;
- next source line 615, whose exact heading is
  `\subsection{Singular homology}`;
- `terminal_source_eof: false`.

The authority append contains exactly two records: the resource and the
edition. The edition record binds the 2,236,609-byte official archive
`authority/upstream/math-notes-563194fae879178b9a6871b249513bfc27968975/archive/math-notes-563194fae879178b9a6871b249513bfc27968975.tar.gz`,
SHA-256
`423c2c34b62a1b443e63be72e80a5c35d5cd6daf4e5b3be8e48dad1d1f897443`,
and names `unit:o012-fom-u001` as its first local derivative unit.

The future producer must also verify the existing 55/55 PASS authority gate,
including commit/tree/archive/source/header/license identities, the two
byte-identical clean builds, and the separately licensed CC0 build overlay.

## Rights partition

Add these five globally unique records:

1. `rights:fomberg-cc-by-sa-4.0` for source-derived prose, mathematics,
   formulas, and source-diagram adaptations.
2. `rights:fomberg-build-overlay-cc0-1.0` for the corrected
   `commath.sty` build overlay only.
3. `rights:o012-fom-u001-companion-cc-by-sa-4.0` for original Indonesian
   mastery, hints, solutions, proof repairs, accessibility descriptions, and
   other original additions.
4. `rights:o012-fom-u001-composite-cc-by-sa-4.0` for the integrated Unit 001
   reader while preserving component-level attribution.
5. `rights:o012-d60-integrated-route-cc-by-sa-4.0` for the course-route
   adaptation/arrangement.

The integrated route record must explicitly preserve Roberts material under CC
BY 4.0, Fomberg material under CC BY-SA 4.0, and the original layer under CC
BY-SA 4.0. It must not claim to relicense the Roberts component or erase
component provenance. Every rights record preserves attribution, changes,
non-endorsement, license URL, and third-party/component status.

The historic program/course authority records are immutable even though their
early cumulative-rights pointer is stale. A new `xref` relation from
`course:o012-d60` to the integrated-route rights record exposes the current
route rights without duplicating or mutating the course ID.

## Edition, route, and stable-ID namespaces

The reader root is `unit:o012-fom-u001`. It has:

- `edition_id: edition:fomberg-at-2025-563194f`;
- `edition_unit_id: unit:o012-fom-u001`;
- `course_route_unit_id: D60-R08`;
- `component_source_id: resource:fomberg-algebraic-topology-2025`;
- the full component commit;
- course sibling `order: 31`, plus `edition_order: 1` and
  `route_order: 8`;
- `source_local_id: null`;
- a source locator for lines 31-614 and a target locator spanning the complete
  final reader.

Every stable anchor uses `o012-fom-u001` or `o012-fom-u001-*`. Its paired
backend IDs are `unit:<stable-id>` and `segment:<stable-id>`. The source
heading `o012-fom-u001` is also the edition-unit/root ID, so it is emitted once
as a root/heading unit and still receives its paired segment; no duplicate root
record is created. Both record types carry the same
`edition_unit_id`, `course_route_unit_id`, component identity, target
locator, model provenance, and component-specific rights. There is exactly one
unit and one segment per non-root stable anchor.

The frozen reader's source headings use:

- `o012-fom-u001` for Homology, source lines 31-614, also serving as the
  edition-unit/root ID;
- `o012-fom-u001-s01` for Delta-complexes, lines 32-345;
- `o012-fom-u001-s02` for simplicial homology, lines 346-614.

The reader mixes sequential and descriptive suffixes—for example
`def-001`, `def-delta-complex`, `exa-circle`, `rem-order`,
`lem-boundary-square`, `proof-001`, and `fig-001`. The producer must derive
the exact 87 declared IDs from the frozen reader; it must not force a guessed
`def-001`--`def-014` or `sec-001` naming scheme.

The independent audit found 14 source diagrams grouped, without loss, into 10
semantic figure blocks. The semantic diagram asset therefore records
`source_diagram_count: 14`, `semantic_figure_block_count: 10`, the source
format census from the audit, and exactly ten `semantic_unit_ids`. Each
figure block has one accessible caption/description and one `illustrates`
relation. Do not regress to the earlier incomplete count of eight environments.

Preserve these five source aliases:

| Source label | Stable object |
|---|---|
| `def:sigma-complex` | `o012-fom-u001-def-delta-complex` |
| `exmp:delta-complex-rp2` | `o012-fom-u001-exa-rp2` |
| `rem:order` | `o012-fom-u001-rem-order` |
| `def:simplicial-complex` | `o012-fom-u001-def-simplicial-complex` |
| `lem:partial-partial-zero` | `o012-fom-u001-lem-boundary-square` |

## Minimum stable-anchor derivation

The frozen reader declares exactly 87 stable anchors: five identified headings
(notice, source root, two source subsections, and mastery) plus 82 identified
semantic blocks. The blocks are 14 definitions, 10 examples, 14 remarks, one
lemma, one proof, one corollary, 10 semantic figures, 12 source-audit blocks,
six exercises, six hints, six complete solutions, and one continuation
boundary. All 87 IDs are unique and survive Pandoc. Because the source-root
heading doubles as the edition root, the backend transaction adds exactly 87
unit records and 87 paired segment records—not a separate duplicate root.

## Proof and mastery closure

The selected span contains one source proof, proving the lemma at source lines
517-520. The backend must include:

- one `proves` relation from `proof-001` to `lem-boundary-square`;
- one `depends-on` relation from `cor-001` to `lem-boundary-square`;
- `proof_status` on the lemma, corollary, and proof records;
- exact source locators and any applicable repair IDs.

None of the controlling `FOM-PR-01` through `FOM-PR-08` loci lies in lines
31-614; the first begins at line 1001. The Unit 001 validator must reject any
claim that those later repairs have been closed. Any defect newly established
inside this unit receives a distinct `FOM-U001-PR-nnn` repair ID, an exact
correction record, adverse-ledger evidence, and a complete replacement proof or
solution before admission.

The source span contains no formal exercise environment. Therefore all six
ordinary mastery items required for `D60-R08` are edition-original. Use
`mcheck-001` through `mcheck-006`, `hint-001` through `hint-006`, and
`sol-001` through `sol-006`. Each exercise has exactly one `hints`
relation and exactly one `solves` relation; each solution has
`solution_status: complete_checked_solution`.

## Required append surfaces and minimum counts

| Backend file/type | Fixed minimum addition |
|---|---:|
| Authority records | 2 |
| Rights records | 5 |
| Assets | 3 |
| Evidence artifacts | 6 |
| QA events | 4 |
| Unit records | 87 |
| Segment records | 87 |
| Relations | 31 |

The three assets are the canonical Markdown reader source, the semantic
diagram/accessibility layer, and the CC0 build overlay. The six artifacts are
the three frozen authority-gate witnesses plus the Unit 001 source audit,
independent review, and final QA receipt. The four QA events cover authority
and build admission, source integrity, mathematics, and Indonesian language.

The 31 fixed-minimum relations comprise:

- one root-to-edition `adapts` relation;
- one course-to-root route `contains` relation carrying `D60-R08`;
- one learner-route `precedes` relation from Roberts Unit 019
  (`D60-R07` terminus) to Fomberg Unit 001;
- one integrated-rights-to-root `contains` relation;
- one course-to-integrated-rights `xref` relation;
- one source-body-to-mastery `precedes` relation;
- one edition-to-CC0-overlay `depends-on` relation;
- one proof-to-lemma `proves` relation;
- one corollary-to-lemma `depends-on` relation;
- twelve mastery relations: six `hints` and six `solves`;
- ten semantic-figure-to-diagram-asset `illustrates` relations.

Counts for new concepts, Indonesian terms, corrections, additional
cross-component dependencies, and real correction-note blocks remain
evidence-dependent. They must be obtained from the final translation and
audits. In particular, `concept:delta-complex` must remain distinct from the
existing `concept:delta-set`.

The fixed minimum append is 225 records before evidence-dependent concepts,
terms, corrections, dependency relations, or extra reader blocks.

## Canonical append rules

1. Use schema `curriculum.interop`, version `0.1.0`, and workflow
   `o012-d60-id-reader-production`.
2. Every record has the common fields, a globally unique ID, UTC-second
   timestamp, active or pending status, and explicit supersession state.
3. Serialize each object as canonical UTF-8 JSON with sorted keys, compact
   separators, and exactly one terminal LF; CR bytes are forbidden.
4. Sort only the new IDs within each backend-file suffix. Preserve every prefix
   byte exactly.
5. Every scalar/list reference resolves against the immutable prefix or the
   same transaction.
6. Every source-derived segment uses the Fomberg component rights record.
   Every original segment uses the companion record. The reader root and
   composite evidence use the Unit 001 composite record.
7. Every source-derived segment has an exact component commit and source
   line-span locator. Every original segment uses an exact target-span locator.
8. Every target locator binds path, final reader hash, exact line range, and
   content hash.
9. New terms bind admitted terminology-control rows; new corrections bind
   adverse-ledger rows and retain `upstream_report_disposition: not_contacted`.
10. Do not add HTML, PDF, build, visual, publication, next-unit, or later-proof
    completion records in this semantic transaction.

## Producer and independent-validator gates

The implementation should use:

- `scripts/extend-backend-fomberg-unit-001.py`;
- `scripts/validate-backend-append-only-fomberg-unit-001.py`;
- `scripts/validate-backend-append-only-fomberg-unit-001-cumulative.py`;
- `qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_001_FILE_MANIFEST.csv`;
- machine and human semantic receipts;
- machine and human cumulative receipts.

The producer must fail closed unless it verifies:

1. all eleven immutable prefix identities and the Unit 30 cumulative receipt;
2. Fomberg commit, tree, archive, source, header, license, selected-span, and
   authority/build-gate identities;
3. the exact lines 31-614 span and exact continuation heading at line 615;
4. the final reader identity, LF discipline, single model-provenance notice,
   stable-ID inventory/order, and absence of duplicate IDs;
5. all five source aliases and all 14 diagrams represented by exactly ten
   semantic figure blocks;
6. exact one-to-one unit/segment mappings and parent/path/sibling order;
7. component, companion, composite, overlay, and integrated-route rights;
8. complete result/proof status and the absence of false later-repair claims;
9. six complete mastery triples;
10. exact terminology/adverse-ledger endpoints and evidence mappings;
11. source, mathematical, and language QA with no open P1, P2, or P3 finding;
12. generic shape/reference/artifact checks over the complete merged backend.

Before writing, the producer constructs and validates the complete merged state
in memory. It then writes only canonical suffixes and proves the old prefix
remains byte-identical.

The independent validator must:

1. rederive the exact suffix ID sets and per-file counts from the frozen reader
   and evidence;
2. verify canonical serialization, lexical suffix order, global uniqueness,
   and every final file identity;
3. independently check authority, source/target locators, aliases, diagram
   census, proof closure, mastery closure, rights partition, terminology, and
   corrections;
4. emit a per-file prefix/delta/final manifest;
5. reject premature reader-build or publication claims.

The cumulative validator must bind the producer, semantic validator, manifests,
and receipts by bytes and SHA-256; reconstruct the exact prefix in a temporary
directory; replay the producer; compare every generated byte with the live
backend; rerun the semantic validator; self-bind its own receipt; and report the
new combined record/byte/bundle identity.

The admitted cursor is `next_source_line: 615` with
`terminal_source_eof: false`. No Fomberg Unit 002 record or completion claim
enters this transaction.
