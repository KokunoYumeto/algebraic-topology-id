# Unit 18 — bounded source audit and translator handoff

Date: 2026-08-22
Authority: Roberts Notes.tex at commit b947ad2e9f9e301bfe24590a9db653bc54fa1a53
Exact span: lines 3482–3677 inclusive; Lecture 19 starts at line 3678.

This durable audit records the complete active-source inventory, mathematical
defects, proof gaps, accessibility work, and mastery obligations for Unit 18.
It is not itself the translation or an independent final review.

## Frozen boundary and source identity

- Notes.tex: 331,447 bytes; 6,368 lines; SHA-256
  cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7.
- Lecture 18 begins at line 3482 and ends with the blank line 3677: 196
  physical lines.
- Lecture 19 begins at line 3678 and is excluded.
- The lecture remains in the Higher homotopy groups section begun before this
  unit; a standalone reader needs a short dependency recap.

## Exact active-source census

The span contains:

- two propositions, two lemmas, one theorem, and two definitions;
- ten examples and six remarks;
- three formal proof environments, of which one is explicitly a sketch and
  one only an idea;
- twelve displayed mathematical blocks;
- two inline Xy-pic diagrams: a basepoint-change triangle and the
  local-trivialization square in a margin note;
- five substantive margin notes;
- no formal exercise or question environment;
- no labels, references, TikZ, figures, external images, inputs, includes, or
  other assets.

The commented lines 3499–3501 contain an inactive example about freely
linearising a set-valued representation. It must remain recorded as inactive
source and must not be silently promoted into Roberts reader content.

## Formal source map

| Source lines | Source object | Required reader treatment |
|---|---|---|
| 3482–3487 | higher-homotopy functor | correct type and state range |
| 3489–3495 | two examples | preserve |
| 3497–3501 | representation targets and inactive comment | preserve active prose; audit inactive comment |
| 3503–3519 | basepoint-transport proposition and sketch | repair norm and complete proof |
| 3521–3529 | n=1 comparison and two remarks | preserve; expose classification hypothesis |
| 3531–3533 | product lemma | supply omitted proof |
| 3535–3550 | homotopic-map lemma | reflow triangle and complete reduction |
| 3552–3558 | homotopy-invariance proposition | complete basepoint-sensitive proof |
| 3560–3578 | fibre bundles and Hopf example | define precisely; prove local triviality |
| 3580–3606 | exactness definitions and examples | preserve; fix pointed fibre |
| 3608–3620 | homotopy LES and pointed-set tail | preserve theorem status; repair types and cosets |
| 3622–3638 | covering-space consequences | preserve; add global connectedness |
| 3640–3657 | complex Hopf calculation | preserve logical strength |
| 3659–3677 | vanishing, quaternionic Hopf example, Serre note | preserve; normalize typos |

## Required mathematical corrections and proof closure

1. P1, line 3485: the source prints
   $f_*:\pi_1(X,x)\to\pi_n(Y,y)$. The typed domain is
   $\pi_n(X,x)$. The target category is Ab only for fixed $n\geq2$;
   for $n=1$ it is Grp in general.

2. P1, lines 3508–3514: the symbol $|\mathbf{x}|$ is undefined. It must be
   the maximum norm. Euclidean norm would leave the stated domain of the
   radial reparameterisation at cube corners. Give the inner-cube rescaling,
   both seam values, and the outer-boundary value.

3. P2, lines 3516–3518: representative independence, composition, identity,
   inverse, and especially the group-homomorphism property are compressed or
   omitted. Supply the collar/reparameterisation argument and preserve the
   source pointer to Hatcher as a pointer, not as copied prose.

4. P1, lines 3521–3524: keep the chronological concatenation convention
   visible when describing conjugation and basepoint transport. Canonical
   independence requires a simply connected path component, not merely two
   points with no component qualification.

5. P2, line 3528: converting the underlying-set representation into an
   actual covering invokes the SLSC classification proved earlier. State the
   hypothesis instead of suggesting the conclusion for every space.

6. P2, lines 3531–3533: prove the product lemma by coordinate projections
   and pairing; verify well-definedness, group law, inverse identities, and
   naturality.

7. P2, lines 3537–3550: the source says the result follows for, rather than
   from, the cylinder special case and omits the reduction. Let
   $\lambda(t)=H(t,x)$ and prove
   $T_\lambda f_*=g_*$ by applying $H$ to a representative cube.

8. P2, lines 3552–3558: the homotopy-equivalence proof must not identify
   $g(f(x))$ with $x$. Use both homotopy-inverse composites together with
   the basepoint-transport isomorphisms to prove injectivity and surjectivity.

9. P1, line 3563: replace an unspecified isomorphism over $U$ by a
   homeomorphism $\Phi_U$ satisfying
   $\operatorname{pr}_1\Phi_U=q$. Reflow the positional Xy-pic square into
   an arrow list plus this equation.

10. P2, lines 3574–3576: identifying each Hopf fibre with $U(1)$ does not
    prove local triviality. Give explicit charts $U_z,U_w$, normalized local
    sections, homeomorphisms with $U(1)$, and the transition function.
    State $\mathbb{CP}^1\cong S^2$ before later writing the base as $S^2$.

11. P1, line 3606: replace the ill-typed
    $p\in F=\pi^{-1}(F)$ by $p\in F=q^{-1}(x)$.

12. P2, lines 3608–3616: retain the theorem and its Hatcher proof pointer
    honestly. Explain that a bundle has homotopy lifting and that boundary
    behaviour of a lifted cube defines the connecting map; do not falsely
    label the complete outsourced theorem proof as supplied.

13. P1, line 3619: normality concerns
    $H=q_*\pi_1(P,p)\leq\pi_1(X,x)$, not the abstract source group.
    Replace $i_*^{-1}(p)$ by $i_*^{-1}([p])$ and type
    $\delta:\pi_1(X,x)\to[\mathrm{pt},F]$.

14. P1, line 3619: under the edition's chronological right transport, the
    orbit is the right-action coset set $H\backslash G$, with elements $Hg$
    and action $Hg\cdot k=Hgk$. It is not a quotient group unless $H$ is
    normal, and the source's bare slash must not reverse the action.

15. P2, line 3637: SLSC in the course convention includes local path
    connectedness but not global connectedness. Add path connectedness or
    formulate the contractible-universal-cover conclusion componentwise.

16. P2, lines 3643–3657: distinguish what the exact sequence alone proves
    from the later black-box inputs $\pi_2(S^3)=0$ and
    $\pi_3(S^3)\cong\mathbb Z$. Use the image of $\pi_2(S^3)$ until
    injectivity has been stated.

17. P3, lines 3660 and 3676: normalize “These is,” singular “sphere,” and
    “calulate” without changing the mathematical content.

18. P3 accessibility, lines 3539–3545 and 3563: replace both positional
    diagrams with semantic arrow inventories and explicit commutativity
    equations. Move all five margin notes into the main reading order.

## Mastery closure

There are no source exercises to solve. Add exactly six separately marked
edition-original checks, each with a hint and complete solution:

1. basepoint transport, composition, inverse, homomorphism, and canonical
   independence;
2. the product isomorphism and naturality;
3. the moving-basepoint homotopy triangle and homotopy invariance;
4. explicit local trivializations of the complex Hopf bundle;
5. injection, surjection, and isomorphism tests from five exact terms;
6. computations combining a double cover, the complex Hopf bundle, and the
   quaternionic Hopf bundle.

## Terminology decisions

Retain the admitted preferred forms fungtor and the morfisma family. Use
bundel serat for fibre bundle, with the English form on first occurrence;
berkas remains available for sheaf terminology later. Use lembaran and
tertutup rata only for covering spaces with discrete fibre. New candidate
terms include ruang total, trivialisasi lokal, bundel Hopf, garis projektif
kompleks, koordinat homogen, barisan eksak, barisan eksak pendek, barisan
eksak panjang, pemetaan penghubung, kernel, and citra.

## Exit gate

Unit 18 is not frozen until the complete active sequence is present; all
eighteen obligations above are resolved; six hint-and-solution checks are
paired; source, line, licence, changes, model provenance, and non-endorsement
are visible; terminology and adverse ledgers are contiguous; IDs are unique;
the next cursor is exactly line 3678; and an independent review reports no
open P1, P2, or P3 issue.
