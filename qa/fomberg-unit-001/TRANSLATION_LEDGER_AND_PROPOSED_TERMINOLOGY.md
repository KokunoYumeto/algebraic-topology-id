# Fomberg Unit 001 — translation ledger and proposed terminology

Date: 2026-08-24  
Status: translated and independently reviewed at P1/P2/P3 zero; append-only backend admitted; deterministic HTML/PDF and live responsive/visual QA pass; not yet committed or published  
Edition unit: O012-FOM-001  
Course route: D60-R08  
Reader:
source/id-ID/fomberg/units/fomberg-unit-001-delta-complexes-simplicial-homology.md  
Reader bytes: 34,773  
Reader SHA-256:
d9b64140f9340c75bc34c12bc02ee843d87de3566e331c50c2374075718aa2c6

## Frozen source and cursor

- Authority commit: 563194fae879178b9a6871b249513bfc27968975.
- Authority tree: fb678966d1533d529bdd72f49d8496a3bdc14a9b.
- File: algebraic_topology.tex.
- Contiguous source: lines 31–614, Sections 1.1–1.2.
- Normalized source slice: 584 lines; 21,875 bytes; SHA-256
  68cb0dea7aa24a42e979877a95acf61b8152c87ed86d88ad7deac7cb5cea2fe3.
- Next source cursor: line 615, start of Section 1.3.
- Rights: CC BY-SA 4.0; attribution, change notice, and non-endorsement are
  present in the reader.
- Exclusions: commented “to be added” placeholders are not reader content;
  no excluded Fomberg problem-bank prompt and no MIT prose was used.

## Closure census

The active source surface is represented in source order:

| Kind | Source/reader count | Closure |
|---|---:|---|
| Definitions | 14 | all translated |
| Examples | 10 | all translated |
| Remarks | 14 | all translated |
| Lemmas | 1 | translated and proof repaired |
| Proofs | 1 | translated and made type-correct |
| Corollaries | 1 | translated under normalized boundary indexing |
| Functional diagrams | 10 | all redrawn semantically; labels/orientations retained |
| Source labels | 5 | retained as data-source-label metadata and internal links |
| Source-audit blocks | 12 | explicit in reader |
| Mastery triples | 6 exercise + 6 hint + 6 full solution | complete; edition-original |

Static checks after the final edit: 87 declared stable IDs, all unique (five
identified headings and 82 identified semantic blocks); 82
semantic block openings and 82 closings; 116 display-math delimiter lines
(even); eight internal links, all resolving. The reader uses only the
o012-fom-u001 namespace and does not alter or reuse Roberts unit numbering.

## Explicit source repairs

| Source lines | Reader audit ID | Decision |
|---|---|---|
| 48–50 | o012-fom-u001-audit-pi-n | Normalize raw maps to based homotopy classes of based maps for pi_n, n at least 1. |
| 52–56 | o012-fom-u001-audit-affine-ambient | Use v_0,…,v_n in R^m with n at most m, consistent with the following simplex definition. |
| 70–76 | o012-fom-u001-audit-001 | Replace terminal e_N by e_n and normalize triangle/Delta notation to Delta throughout. |
| 95–102 | o012-fom-u001-audit-002 | Restore vertices v_0,…,v_n and face indices 0 through n. |
| 183–184 | o012-fom-u001-audit-003 | Correct T^1 to T^2 because the source itself defines S^1 times S^1. |
| 347–360 | o012-fom-u001-audit-005 | Permit C_0 by changing n at least 1 to n at least 0. |
| 379–386 | definition o012-fom-u001-def-boundary | Type-close the boundary family: n at least 1 and partial_0=0, equivalently C_{-1}=0. |
| 392–430 | o012-fom-u001-audit-006 | Correct e/σ and σ(σ)/partial_2(σ); retain that e_2+e_0−e_1 and e_0−e_1+e_2 are identical. |
| 432–448 | o012-fom-u001-audit-007 | Normalize Z to blackboard-bold integers and σ_1 to partial_1. |
| 497–505 | o012-fom-u001-audit-face-sign | Keep the face restriction as simplex g; use −g only as a chain coefficient induced by orientation. |
| 517–548 | o012-fom-u001-audit-008 | Put σ in C_n and replace the repeated omitted v_j with the two distinct face indices; retain the source’s pairwise-cancellation proof. |
| 555–582 | o012-fom-u001-audit-009 | Normalize globally to B_n=im(partial_{n+1}) inside C_n, B_n inside Z_n, H_n=Z_n/B_n, and z_1−z_2 in B_n; document all three inconsistent source forms. |
| 610–613 | o012-fom-u001-audit-010 | Correct H^1 to H_1 with integer coefficients and state path-connected/basepoint hypotheses. |

## Pre-admission independent-review repairs

The first independent review of reader SHA-256
`20cb76761248ad0650fa726cbfad578da2c15b09dae128014798c0b97c4782ee`
found one P1, three P2, and two P3 defects. The current reader resolves all six:

- it distinguishes the 2-simplex characteristic map $V$ from its three
  1-simplex face restrictions;
- it states the clockwise direction of every repeated loop diagram;
- it spells out every paired-edge and diagonal direction in the torus and
  projective-plane square descriptions;
- it states the abelianization theorem for singular $H_1$ and defers its
  identification with $H_1^\Delta$ to the comparison theorem;
- it retains the $\Delta$ superscript throughout the homologous-cycle
  definition; and
- it naturalizes the two flagged Indonesian phrases.

The durable correction rows are `O012-ADV-0420` through `O012-ADV-0425`.
Admission remains contingent on the independent re-review of the current
reader bytes.

## Proposed terminology for root integration

These are proposals/evidence notes only. No shared terminology or adverse
ledger was edited.

| English source term | Reader-facing id-ID | Decision/evidence |
|---|---|---|
| topological space | ruang topologis | Existing edition usage. |
| path-connected component | komponen terhubung lintasan | Existing edition usage; avoids conflating connected and path-connected. |
| based map / based homotopy class | pemetaan bertitik / kelas homotopi bertitik | Existing Roberts convention. |
| affinely independent | bebas afin | Concise mathematical adjective; new candidate. |
| convex hull | selubung konveks | Standard descriptive form; new candidate. |
| barycentric map | pemetaan barisentris | Consistent with existing subdivisi barisentris. |
| simplex / n-simplex | simpleks / simpleks-n | Existing edition usage. |
| face | muka | Keeps the simplex face distinct from edge. |
| vertex | simpul | Existing graph/topology usage. |
| edge | sisi | Required by frozen TERM-0206; replaces the earlier draft’s rusuk. |
| Delta-complex | kompleks-Delta | Preserves Fomberg’s geometric characteristic-map object; do not silently merge it with Roberts’s combinatorial himpunan-Delta. |
| simplicial complex | kompleks simpleksial | Existing adjective simpleksial. |
| simplicial homology | homologi simpleksial | Parallel to kohomologi simpleksial. |
| chain / n-chain | rantai / rantai-n | Existing chain-complex usage. |
| boundary map | pemetaan batas | Context distinguishes the algebraic map from topological boundary. |
| boundary element / n-boundary | batas / batas-n | Paired with the normalized B_n convention. |
| cycle / n-cycle | siklus / siklus-n | Existing algebraic usage. |
| homologous | homolog | Short relational adjective; classes remain kelas homologi. |
| free abelian group | grup abelian bebas | Existing algebra terminology. |
| nonexample | bukan contoh | Natural reader-facing phrase. |

## Mastery mapping

All six tasks are separately marked edition-original and mapped to D60-R08:

1. o012-fom-u001-mcheck-001 — affine independence and barycentric coordinates;
2. o012-fom-u001-mcheck-002 — Delta-complex versus simplicial complex;
3. o012-fom-u001-mcheck-003 — explicit boundary-of-boundary cancellation;
4. o012-fom-u001-mcheck-004 — homology of the one-vertex circle;
5. o012-fom-u001-mcheck-005 — torus boundary matrix and integral homology;
6. o012-fom-u001-mcheck-006 — homologous and non-homologous torus cycles.

Every task has an adjacent hint and a complete solution. The computations use
the normalized B_n=im(partial_{n+1}) convention. The torus quotient is
torsion-free because the image generator (1,1,−1) is primitive.

## Bounded algebra checks

A direct exact-integer check returned: affine determinant 6; the displayed
triangle boundary vector maps to (0,0,0) under the vertex-boundary matrix; the
torus boundary matrix has rank 1, Smith diagonal (1,0), and kernel generated
by V−L up to sign; and z_1−z_2=(1,1,−1), exactly the image generator. These
checks support all six written solutions without invoking a document build.
