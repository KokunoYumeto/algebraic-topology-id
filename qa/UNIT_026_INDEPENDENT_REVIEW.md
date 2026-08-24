# Unit 026 — independent mathematical and structural review

Date: 2026-08-24

## Review scope

This review independently compared
`source/id-ID/units/unit-026-lecture-026.md` and
`qa/UNIT_026_SOURCE_AUDIT.md` against the frozen Roberts authority
`Notes.tex:5612–5823` at commit
`b947ad2e9f9e301bfe24590a9db653bc54fa1a53`. It checked the exact source
boundary and census, every source object and formula, all edition repairs and
proof closures, the singular/relative/reduced cohomology constructions, the
coproduct argument, both levels of homotopy invariance, the signed prism
operator, all six mastery solutions, Indonesian terminology, source-versus-
edition labeling, stable identifiers, rights, provenance, and the terminal
cursor.

## Snapshot and fail-closed verdict

Final reader snapshot: **38,537 bytes, 1,201 LF lines, SHA-256
`7a2cf4ea31546b8258e3e91c819d3ad516973c8f861249fccc7334b9ade9d835`**.
Source-audit snapshot: **7,693 bytes, 130 LF lines, SHA-256
`658a2586c58fd4149cf4959bc9b405d67896984f61621b1533f873836a9c8bb5`**.

- P1: 0
- P2: 0
- P3: 0
- Overall status: **PASS**.
- The active authority span is exactly 212 physical lines and 9,763
  LF-normalized UTF-8 bytes, SHA-256
  `52663b3e60d5d6f3041b8ede449c52a04700ee670c201ef5674c4aa3973203a9`.
  Line 5612 contains the complete Lecture 26 marker, line 5823 is the retained
  terminal blank line, and line 5824 begins Lecture 27 and remains excluded.
- The reader contains 62 unique declared stable IDs: eight identified headings
  and 54 balanced fenced semantic objects. The fenced inventory is three
  asides, one boundary, three corollaries, three definitions, two examples,
  six exercises, six hints, one lemma, nine proofs, four propositions, one
  remark, six solutions, seven source audits, and two theorems.

### Resolved pre-admission findings

1. `UNIT026-MATH-P2-001` — **P2**, reader lines 100–125 and source-audit
   dossier item 1. The initial draft repeated the source margin's convention
   that interior smoothness plus continuous extension to the boundary was
   enough, then invoked Stokes without strengthening that regularity. Mere
   continuous boundary extension does not generally guarantee Stokes's
   hypotheses. The reader now distinguishes the weak source convention and
   assumes that the simplex map is smooth up to the boundary (for example,
   extends smoothly to a neighbourhood) for the displayed Stokes identity.
   The source audit records the same repair. No source formula, stable ID, or
   source boundary changed.
2. `UNIT026-TERM-P3-001` — **P3**, twelve reader occurrences. The initial
   draft used `funktor` and `funktorialitas`, contrary to admitted controls
   `O012-TERM-0004`, `O012-TERM-0072`, and `O012-TERM-0297`. All occurrences
   now use `fungtor` and `fungtorialitas`. No deprecated occurrence remains;
   mathematics, IDs, and object order are unchanged.

Both findings were corrected before admission and are therefore retained as
transparent history rather than counted as open findings.

## Source closure and mathematical fidelity

The direct authority census is exact: one lecture marker, three definitions,
two propositions, two theorems, one lemma, three corollaries, one remark, two
examples, three source proof environments, three margins, two labels, and two
references. There is no formal source exercise or question, Xy-pic, TikZ,
external graphic, citation, `input`, or `include`. The reader preserves this
order, translates every source object, places all three margins in ordinary
reading order, and distinguishes edition-supplied propositions, proofs,
audits, and mastery material with semantic classes and `data-origin` where
needed. Source labels `prop:les_of_pair_of_spaces` and
`thm:homotopy_invariance_cohom` are retained as aliases of their reader IDs.

- The geometric-realisation reminder, distinguished simplex maps, and
  differential-form motivation preserve the source content. The Stokes
  display has the correct dimension shift, alternating boundary signs, and
  now an adequate regularity hypothesis.
- The singular coboundary has the correct variance and indexing. The added
  proof of `delta^2=0` pairs codimension-two faces by the cosimplicial identity;
  the induced map is correctly typed as
  `f^*:C^k(Y;R)->C^k(X;R)` and commutes with the coboundary.
- The one-point differential alternates between zero and the identity in the
  stated degrees. The interval-cardinality example is treated as a size
  illustration, while its vanishing cohomology is derived later from
  contractibility.
- The relative cochain complex is the kernel of restriction. Degreewise
  extension by zero proves surjectivity without falsely claiming a cochain-map
  splitting. The connecting map has degree `+1`, is well defined, and its
  naturality follows from maps of pairs.
- The reduced-cohomology repair is correct: constant zero-cocycles make
  `H^0(X;R)->R` surjective, so the connecting map vanishes and
  `H^k(X,x;R) ~= H^k(X;R)` for every `k>=1`. Pointed functoriality and the
  degree-zero calculation for a pointed discrete space are fully closed.
- The coproduct proof explicitly uses connectedness of every standard simplex,
  decomposes the function modules, restrictions, kernels, and differentials,
  and is correctly limited to the finite binary direct sum. The mastery
  counterexample accurately isolates why a disconnected domain would fail.
- The three homotopy-invariance corollaries have the correct contravariant
  composition order. The contractible-space corollary restores the missing
  degree in the source, and the basepoint-change argument correctly identifies
  the same degree-zero kernel along a path.
- The cochain-homotopy lemma repairs the source's `x/c` variable slip and uses
  the correct degree `-1` identity. The final theorem's prism map has the
  correct ordered vertices and alternating sign. Boundary cancellation yields
  `partial P + P partial = g_# - f_#`; defining
  `h(phi)=-phi composed with P` consequently gives
  `delta h + h delta = f^* - g^*`. The low-degree mastery calculation confirms
  the same orientation convention.

Each of the six edition-original exercises has exactly one hint and one full
solution. They cover the square-zero identity, the point and interval,
relative interval cohomology, a pointed finite discrete space, coproduct
connectedness, and prism dualisation. No theorem or requested solution in the
unit depends on an omitted proof.

## Structure, rendering, rights, and provenance

All 62 declared reader IDs are unique, all 54 fenced objects close exactly,
and the one same-unit fragment resolves. The second fragment targets
`o012-rbt-l24-thm-001`, whose admitted Unit 24 declaration exists. Pandoc
3.9.0.2 converts the corrected reader to standalone HTML5 with native MathML,
warnings fatal, at exit zero: 423 MathML nodes, 63 unique DOM IDs, no duplicate
DOM ID, no script, and no external stylesheet dependency. The isolated
single-unit render naturally leaves the cross-unit Unit 24 link for the
cumulative reader, where its target is present.

The reader retains David Michael Roberts's authorship, exact commit and line
span, CC BY 4.0, change/repair disclosures, independent non-endorsement, human
credit, and the exact production note **OpenAI Codex gpt-5.6-sol, Ultra**. It
contains no credential, private path, placeholder, official-affiliation claim,
or directing-user identity. The exact next source cursor is Notes.tex line
5824. Mathematics, source closure, Indonesian terminology, stable structure,
rights, and provenance have no open P1, P2, or P3 finding. This review does not
advance the cursor, append a backend, run a cumulative build, or claim
publication.
