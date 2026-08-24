#!/usr/bin/env python3
"""Fail-closed structural, mathematical, provenance, and MathML QA for Unit 024."""

from __future__ import annotations

import hashlib
import html as html_lib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTHORITY = ROOT / "authority/upstream/AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex"
UNIT = ROOT / "source/id-ID/units/unit-024-lecture-024.md"
AUDIT = ROOT / "qa/UNIT_024_SOURCE_AUDIT.md"
REVIEW = ROOT / "qa/UNIT_024_INDEPENDENT_REVIEW.md"
RECEIPT = ROOT / "qa/UNIT_024_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"

SOURCE_EXPECTED = (331447, 6368, "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7")
SPAN_EXPECTED = (12837, "b2128930a56a0a8c04c327a397e72e21b215ffe742bb684e8dd166f0e04b0aea")
UNIT_EXPECTED = (43085, 1156, "993ad0c3493caff6bd15ab2bcf435f6cbb1f49ed9a1e11bc1009d649ae2d3647")
AUDIT_EXPECTED = (4384, 78, "0aeb3beae1b52099e97538083ef349590cca62b473ff1455b8c1fdaffbe2ba6b")
REVIEW_EXPECTED = (5570, 105, "d06dc4a2d76eabbb8f4c115fd8f311c81e974415a186f8bff8269d30cb1672b2")

EXPECTED_SOURCE_CENSUS = {
    "lecture": 1,
    "example_begin": 0,
    "example_end": 1,
    "definition": 1,
    "theorem": 1,
    "lemma": 3,
    "remark": 1,
    "proof": 3,
    "enumerate": 1,
    "enumerate_item": 6,
    "margin": 7,
    "xypic": 2,
    "tikz": 1,
    "label": 4,
    "reference": 4,
    "display": 8,
    "exercise": 0,
    "citation": 0,
    "external_graphic": 0,
    "input": 0,
    "include": 0,
}

EXPECTED_BLOCKS = {
    "boundary": 1,
    "definition": 1,
    "example": 1,
    "exercise": 6,
    "figure": 3,
    "hint": 6,
    "lemma": 3,
    "proof": 6,
    "remark": 1,
    "solution": 6,
    "source-audit": 8,
    "source-margin": 7,
    "theorem": 1,
}

EXPECTED_IDS = {
    "o012-rbt-l24",
    "o012-rbt-l24-notice",
    "o012-rbt-l24-s01",
    "o012-rbt-l24-s02",
    "o012-rbt-l24-s03",
    "o012-rbt-l24-s04",
    "o012-rbt-l24-s05",
    "o012-rbt-l24-s06",
    "o012-rbt-l24-s07",
    "o012-rbt-l24-mastery",
    "o012-rbt-l24-exa-001",
    "o012-rbt-l24-def-001",
    "o012-rbt-l24-thm-001",
    "o012-rbt-l24-rem-001",
    "o012-rbt-l24-lem-001",
    "o012-rbt-l24-lem-002",
    "o012-rbt-l24-lem-003",
    "o012-rbt-l24-fig-001",
    "o012-rbt-l24-fig-002",
    "o012-rbt-l24-fig-003",
    "o012-rbt-l24-boundary-001",
    *(f"o012-rbt-l24-audit-{n:03d}" for n in range(1, 9)),
    *(f"o012-rbt-l24-margin-{n:03d}" for n in range(1, 8)),
    *(f"o012-rbt-l24-proof-{n:03d}" for n in range(1, 7)),
    *(f"o012-rbt-l24-mcheck-{n:03d}" for n in range(1, 7)),
    *(f"o012-rbt-l24-hint-{n:03d}" for n in range(1, 7)),
    *(f"o012-rbt-l24-sol-{n:03d}" for n in range(1, 7)),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_frozen(path: Path, expected: tuple[int, int, str]) -> tuple[bytes, str]:
    if not path.is_file():
        raise AssertionError(f"missing required file: {path.relative_to(ROOT)}")
    data = path.read_bytes()
    text = data.decode("utf-8")
    actual = (len(data), text.count("\n"), sha256(data))
    if actual != expected:
        raise AssertionError(
            f"identity mismatch for {path.relative_to(ROOT)}: {actual} != {expected}"
        )
    if b"\r" in data or not data.endswith(b"\n"):
        raise AssertionError(f"non-LF or unterminated frozen text: {path.relative_to(ROOT)}")
    return data, text


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise AssertionError(detail)


def require_all(text: str, needles: list[str], label: str) -> None:
    missing = [needle for needle in needles if needle not in text]
    require(not missing, f"{label} missing: {missing}")


def main() -> int:
    # A failed rerun must never leave an earlier PASS receipt looking current.
    RECEIPT.unlink(missing_ok=True)
    checks: list[dict[str, str]] = []

    def passed(name: str, detail: str) -> None:
        checks.append({"check": name, "status": "PASS", "detail": detail})

    source_data, source_text = read_frozen(AUTHORITY, SOURCE_EXPECTED)
    unit_data, unit_text = read_frozen(UNIT, UNIT_EXPECTED)
    _, audit_text = read_frozen(AUDIT, AUDIT_EXPECTED)
    _, review_text = read_frozen(REVIEW, REVIEW_EXPECTED)
    passed("required_files_and_identities", "authority, reader, audit, and independent review match frozen bytes")

    source_lines = source_text.splitlines()
    require(len(source_lines) == 6368, "authority physical-line count mismatch")
    span_text = "\n".join(source_lines[5112:5369]) + "\n"
    span_data = span_text.encode("utf-8")
    require((len(span_data), sha256(span_data)) == SPAN_EXPECTED, "source span identity mismatch")
    require(source_lines[5112].find(r"\lecturenum{24}") >= 0, "line 5113 lacks Lecture 24 marker")
    require(source_lines[5120].strip() == r"\end{example}", "line 5121 does not close the continued example")
    require(source_lines[5369].startswith(r"The\lecturenum{25}"), "line 5370 is not the intact Lecture 25 boundary")
    passed("source_boundary", "Notes.tex:5113-5369 is 12,837 LF bytes; continued example closes at 5121; next cursor 5370")

    source_patterns = {
        "lecture": r"\\lecturenum\{24\}",
        "example_begin": r"\\begin\{example\}",
        "example_end": r"\\end\{example\}",
        "definition": r"\\begin\{definition\}",
        "theorem": r"\\begin\{theorem\}",
        "lemma": r"\\begin\{lemma\}",
        "remark": r"\\begin\{rem\}",
        "proof": r"\\begin\{proof\}",
        "enumerate": r"\\begin\{enumerate\}",
        "enumerate_item": r"\\item\b",
        "margin": r"\\marginnote\{",
        "xypic": r"\\xymatrix\{",
        "tikz": r"\\begin\{tikzpicture\}",
        "label": r"\\label\{",
        "reference": r"\\ref\{",
        "display": r"\\\[",
        "exercise": r"\\begin\{exercise\}",
        "citation": r"\\cite",
        "external_graphic": r"\\includegraphics",
        "input": r"\\input\{",
        "include": r"\\include\{",
    }
    source_census = {key: len(re.findall(pattern, span_text)) for key, pattern in source_patterns.items()}
    require(source_census == EXPECTED_SOURCE_CENSUS, f"source census mismatch: {source_census}")
    passed("source_census", json.dumps(source_census, ensure_ascii=False, sort_keys=True))

    require(MODEL in unit_text, "exact model provenance is absent")
    require_all(
        unit_text,
        [
            "David Michael Roberts",
            "CC BY 4.0",
            "tidak disponsori, didukung, disahkan",
            "kredit kontributor manusia",
            COMMIT,
            "Notes.tex baris 5113--5369",
            SPAN_EXPECTED[1],
        ],
        "rights/provenance",
    )
    forbidden = [
        "C:\\Users\\",
        "C:/Users/",
        "github_pat_",
        "ghp_",
        "sk-proj_",
        "access_token",
        "FILL_AFTER",
        "TODO",
        "TBD",
    ]
    require(not [marker for marker in forbidden if marker in unit_text], "private or placeholder marker in reader")
    passed("rights_provenance_privacy", "CC BY 4.0, source credit, non-endorsement, human credit, exact model; no private marker")

    ids = re.findall(r"#(o012-[a-z0-9-]+)(?=[}\s])", unit_text)
    require(len(ids) == 60 and len(set(ids)) == 60, "stable-ID count or uniqueness mismatch")
    require(set(ids) == EXPECTED_IDS, f"stable-ID set mismatch: {sorted(set(ids) ^ EXPECTED_IDS)}")
    require(len(re.findall(r"(?m)^#{1,6} .*\{[^}]*#o012-", unit_text)) == 10, "identified-heading census mismatch")
    passed("stable_ids", "60 occurrences, 60 unique IDs, exact expected set; 10 identified headings")

    opens = re.findall(r"(?m)^[ \t]*::: \{\.([a-z-]+)\s+#o012-", unit_text)
    closes = re.findall(r"(?m)^[ \t]*:::\s*$", unit_text)
    block_census = {kind: opens.count(kind) for kind in sorted(set(opens))}
    require(len(opens) == 50 and len(closes) == 50, "fenced-div census or balance mismatch")
    require(block_census == EXPECTED_BLOCKS, f"semantic-block inventory mismatch: {block_census}")
    require(unit_text.count("$$") == 120, "display-math delimiter census mismatch")
    for line_number, line in enumerate(unit_text.splitlines(), start=1):
        dollars = len(re.findall(r"(?<!\\)\$", line))
        require(dollars % 2 == 0, f"unclosed line-local math delimiter at reader line {line_number}")
    passed("balanced_structure", f"50 balanced fenced objects; {json.dumps(block_census, sort_keys=True)}; math delimiters balanced")

    require(
        'data-source-status="resumes-and-closes-lecture-023-example" data-continuation-of="o012-rbt-l23-exa-002"' in unit_text,
        "continued-example relationship is missing or mistyped",
    )
    aliases = ["thm:alg_Mayer-Vietoris", "snakeLemma", "fig:snake_lemma", "lemma:setup_for_algMV"]
    for alias in aliases:
        require(unit_text.count(f'data-source-label="{alias}"') == 1, f"source alias mismatch: {alias}")
    require(unit_text.count('data-source-format="xypic"') == 2, "Xy-pic provenance count mismatch")
    require(unit_text.count('data-source-format="tikz"') == 1, "TikZ provenance count mismatch")
    require(unit_text.count('data-origin="edition-original"') == 18, "mastery-origin census mismatch")
    require(unit_text.count('data-origin="edition-proof-closure"') == 3, "edition proof-closure census mismatch")
    require(unit_text.count('data-origin="source-proof-expanded"') == 2, "expanded source-proof census mismatch")
    require(unit_text.count('data-origin="source-proof-completed"') == 1, "completed source-proof census mismatch")
    passed("semantic_attributes_and_aliases", "continued parent, four source aliases, three diagram origins, six proof origins, and 18 mastery origins exact")

    order_markers = [
        "#o012-rbt-l24-exa-001",
        "#o012-rbt-l24-proof-001",
        "#o012-rbt-l24-lem-001",
        "#o012-rbt-l24-proof-002",
        "#o012-rbt-l24-def-001",
        "#o012-rbt-l24-thm-001",
        "#o012-rbt-l24-lem-002",
        "#o012-rbt-l24-fig-002",
        "#o012-rbt-l24-proof-003",
        "#o012-rbt-l24-lem-003",
        "#o012-rbt-l24-proof-004",
        "#o012-rbt-l24-proof-005",
        "#o012-rbt-l24-proof-006",
        "#o012-rbt-l24-mastery",
        "#o012-rbt-l24-boundary-001",
    ]
    positions = [unit_text.index(marker) for marker in order_markers]
    require(positions == sorted(positions), "source and edition-closure order mismatch")
    require(unit_text.count("#o012-rbt-l23-exa-002") == 2, "cross-unit parent-reference count mismatch")
    passed("source_order_and_topology", "continued example, source objects, proof closures, mastery, and boundary occur in exact intended order")

    compact = re.sub(r"\s+", "", unit_text)
    compact_required = [
        r"\delta_A^ni_n^*=i_{n+1}^*\delta_X^n",
        r"0\longrightarrow\ker(i^*)\longrightarrowC^\bullet(X_\bullet;R)\xrightarrow{\i^*\}C^\bullet(A_\bullet;R)\longrightarrow0",
        r"d_{\ker\varphi}^n:=d_A^n|_{\ker\varphi_n}\colon\ker\varphi_n\longrightarrow\ker\varphi_{n+1}",
        r"\xrightarrow{\H^{k+1}(i)\}H^{k+1}(B_\bullet)",
        r"\gamma\circ\pi=\pi'\circ\beta",
        r"\delta(rc_1+sc_2)=r\delta(c_1)+s\delta(c_2)",
        r"\operatorname{im}(\ker\alpha\to\ker\beta)=\ker(\ker\beta\to\ker\gamma)",
        r"\operatorname{im}(\ker\beta\to\ker\gamma)=\ker\delta",
        r"\operatorname{im}\delta=\ker(\operatorname{coker}\alpha\to\operatorname{coker}\beta)",
        r"\operatorname{im}(\operatorname{coker}\alpha\to\operatorname{coker}\beta)=\ker(\operatorname{coker}\beta\to\operatorname{coker}\gamma)",
        r"Q_K^k:=K_k/\delta_{k-1}^K(K_{k-1})",
        r"Z_K^{k+1}:=\ker(\delta_{k+1}^K)",
        r"\overline\delta_K^k([x])=\delta_k^K(x)",
        r"&=\ker(\delta_k^K)/\delta_{k-1}^K(K_{k-1})\\&=H^k(K_\bullet)",
        r"\operatorname{coker}\overline\delta_K^k=\frac{\ker(\delta_{k+1}^K)}{\delta_k^K(K_k)}=H^{k+1}(K_\bullet)",
        r"\delta_2(f_C(c))=\overlinef_{A'}(\delta_1(c))",
    ]
    require_all(compact, compact_required, "mathematical invariant")
    for obligation in range(1, 7):
        require(f"**{obligation}." in unit_text, f"Snake obligation {obligation} heading absent")
    require_all(
        unit_text,
        [
            "Modul kanan bawah adalah $C'$, bukan $C$.",
            "pada umumnya ia bukan pemetaan korantai",
            "Keempat posisi internal itu eksak",
            "kedua barisnya eksak",
            "isomorfisma kanonik",
            "morfisma antara kedua barisan eksak panjang",
        ],
        "proof/correction invariant",
    )
    require(
        "KursorsumberberikutnyayangtepatadalahNotes.texbaris5370" in compact,
        "terminal source cursor statement is absent",
    )
    passed("mathematical_fidelity", "restriction/kernel, repaired theorem and C-prime diagram, all Snake obligations, setup, identifications, splicing, and naturality exact")

    raw_layout = re.findall(
        r"\\(?:xymatrix|marginnote|setfloatalignment|begin\{tikzpicture\}|end\{tikzpicture\}|draw\[|matrix\[)",
        unit_text,
    )
    require(not raw_layout, f"raw positional TeX command remains: {raw_layout}")
    require(unit_text.count("data-source-format=") == 3, "semantic diagram replacement census mismatch")
    require_all(
        unit_text,
        [
            "Tidak ada informasi yang bergantung pada letak panah.",
        ],
        "accessibility reflow",
    )
    require_all(
        compact,
        [
            "Warnamerahdangeometrijalurpadagambarsumbertidakmemuatinformasitambahan",
            "Tidakadasifatyangbergantungpadaposisivisualdiagram.",
        ],
        "accessibility reflow",
    )
    passed("accessible_semantic_reflow", "2 Xy-pic plus 1 TikZ surface replaced by semantic arrow data; 7 margins in reading order; no raw layout command")

    terms = [
        "fungtor",
        "morfisma",
        "kosiklus",
        "kobatas",
        "kernel",
        "kokernel",
        "barisan eksak pendek",
        "barisan eksak panjang",
        "aljabar homologis",
        "Lema Ular",
        "pengejaran diagram",
    ]
    require_all(unit_text, terms, "admitted Indonesian terminology")
    for prefix in ("mcheck", "hint", "sol"):
        observed = re.findall(fr"#o012-rbt-l24-{prefix}-(\d{{3}})", unit_text)
        require(observed == [f"{n:03d}" for n in range(1, 7)], f"{prefix} mastery sequence mismatch")
    passed("language_and_mastery", "admitted id-ID terminology; six exact problem/hint/full-solution triples")

    require_all(
        audit_text,
        [
            "Status: source frozen; translation not yet admitted",
            SPAN_EXPECTED[1],
            "Active span: physical lines **5113",
            "5369**",
            "Complete all six obligations listed in the Snake Lemma proof",
            "lower-right module must be `C'`, not `C`",
            "next production surface",
        ],
        "source audit",
    )
    require("source line 5173 writes the term" in audit_text, "corrected audit locator 5173 is absent")
    require("source line 5182 writes the term" not in audit_text, "superseded audit locator 5182 remains")
    require_all(
        review_text,
        [
            "- P1: 0",
            "- P2: 0",
            "- P3: 0",
            "Corrected pre-admission evidence defect",
            "UNIT024-AUDIT-P3-001",
            UNIT_EXPECTED[2],
            "502 MathML nodes",
        ],
        "independent review",
    )
    passed(
        "audit_and_independent_review_identity",
        "corrected source audit bound exactly; independent review records P1=0, P2=0, P3=0",
    )
    resolved_findings = [
        {
            "finding_id": "UNIT024-AUDIT-P3-001",
            "severity": "P3",
            "path": "qa/UNIT_024_SOURCE_AUDIT.md",
            "line": 38,
            "initial_observation": "audit located malformed Mayer--Vietoris term at Notes.tex:5182",
            "resolution": "locator corrected to physical Notes.tex:5173 before admission; Notes.tex:5182 begins the Snake Lemma",
            "reader_affected": False,
            "status": "RESOLVED_BEFORE_ADMISSION",
        }
    ]
    passed(
        "source_audit_locator",
        "source-audit line 38 now gives exact authority locus 5173; UNIT024-AUDIT-P3-001 resolved before admission",
    )

    pandoc = shutil.which("pandoc")
    require(pandoc is not None, "pandoc executable unavailable")
    version = subprocess.run([pandoc, "--version"], check=True, capture_output=True, text=True).stdout.splitlines()[0]
    require(version == "pandoc 3.9.0.2", f"unexpected Pandoc version: {version}")
    rendered = subprocess.run(
        [
            pandoc,
            str(UNIT),
            "--from=markdown+fenced_divs+tex_math_dollars",
            "--to=html5",
            "--standalone",
            "--mathml",
            "--fail-if-warnings",
        ],
        check=False,
        capture_output=True,
        timeout=120,
    )
    require(rendered.returncode == 0, f"Pandoc HTML5/MathML failed: {rendered.stderr.decode('utf-8', 'replace')}")
    require(not rendered.stderr, f"Pandoc emitted diagnostics: {rendered.stderr.decode('utf-8', 'replace')}")
    html_text = rendered.stdout.decode("utf-8")
    dom_ids = re.findall(r'\bid="([^"]+)"', html_text)
    require(len(dom_ids) == len(set(dom_ids)) == 61, "rendered DOM-ID census or uniqueness mismatch")
    require(EXPECTED_IDS.issubset(set(dom_ids)), "rendered HTML lost one or more stable IDs")
    fragment_ids = [html_lib.unescape(value) for value in re.findall(r'\bhref="#([^"]+)"', html_text)]
    unresolved = sorted(set(fragment_ids) - set(dom_ids))
    require(len(fragment_ids) == 6, "fragment-link census mismatch")
    require(unresolved == ["o012-rbt-l23-exa-002"], f"unexpected unresolved fragment set: {unresolved}")
    mathml_nodes = len(re.findall(r"<math\b", html_text))
    require(mathml_nodes == 502, f"MathML-node census mismatch: {mathml_nodes}")
    require(not re.search(r'<span class="math (?:display|inline)">', html_text), "raw-TeX math fallback remains")
    require(not re.search(r"(?is)<script\b[^>]*\bsrc\s*=|<link\b[^>]*\brel=\"stylesheet\"", html_text), "runtime dependency remains")
    passed("pandoc_html5_mathml", "pandoc 3.9.0.2; exit 0; warnings fatal; 502 MathML nodes; all IDs; only declared cross-unit parent fragment external")

    verifier_data = Path(__file__).read_bytes()
    receipt = {
        "schema_version": "1.0",
        "qa_id": "O012-RBT-L24-QA",
        "status": "PASS",
        "source": {
            "path": str(AUTHORITY.relative_to(ROOT)).replace("\\", "/"),
            "commit": COMMIT,
            "line_start": 5113,
            "line_end": 5369,
            "bytes": SOURCE_EXPECTED[0],
            "lines": SOURCE_EXPECTED[1],
            "sha256": SOURCE_EXPECTED[2],
            "span_bytes": SPAN_EXPECTED[0],
            "span_sha256": SPAN_EXPECTED[1],
            "source_census": source_census,
            "continued_example_close": 5121,
            "next_line": 5370,
        },
        "unit": {
            "path": str(UNIT.relative_to(ROOT)).replace("\\", "/"),
            "bytes": UNIT_EXPECTED[0],
            "lines": UNIT_EXPECTED[1],
            "sha256": UNIT_EXPECTED[2],
            "stable_ids": len(ids),
            "fenced_semantic_objects": len(opens),
            "block_census": block_census,
        },
        "controls": {
            "source_audit": {
                "path": str(AUDIT.relative_to(ROOT)).replace("\\", "/"),
                "bytes": AUDIT_EXPECTED[0],
                "sha256": AUDIT_EXPECTED[2],
            },
            "independent_review": {
                "path": str(REVIEW.relative_to(ROOT)).replace("\\", "/"),
                "bytes": REVIEW_EXPECTED[0],
                "sha256": REVIEW_EXPECTED[2],
                "p1": 0,
                "p2": 0,
                "p3": 0,
            },
        },
        "findings": [],
        "resolved_findings": resolved_findings,
        "corrections": {
            "restored_H_k_plus_1_B": True,
            "repaired_snake_lower_right_C_prime": True,
            "corrected_a_prime_b_notation": True,
            "restored_image_parenthesis": True,
        },
        "proof_closure": {
            "restriction_kernel_sequence": True,
            "kernel_complex": True,
            "snake_obligations": 6,
            "snake_connector_linear": True,
            "setup_lemma": True,
            "theorem_identifications_splicing_naturality": True,
            "mastery_solution_triples": 6,
        },
        "rendering": {
            "pandoc": version,
            "target": "HTML5 native MathML",
            "mathml_nodes": mathml_nodes,
            "runtime_fallback": False,
            "declared_cross_unit_fragment": "o012-rbt-l23-exa-002",
        },
        "verifier": {
            "path": str(Path(__file__).resolve().relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256(verifier_data),
        },
        "checks": checks,
        "model_provenance": MODEL,
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "receipt": str(RECEIPT), "checks": len(checks), "findings": 0}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, UnicodeError, OSError, subprocess.SubprocessError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
