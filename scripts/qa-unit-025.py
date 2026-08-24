#!/usr/bin/env python3
"""Fail-closed source, mathematics, structure, terminology, and MathML QA for Unit 025."""

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
UNIT = ROOT / "source/id-ID/units/unit-025-lecture-025.md"
AUDIT = ROOT / "qa/UNIT_025_SOURCE_AUDIT.md"
REVIEW = ROOT / "qa/UNIT_025_INDEPENDENT_REVIEW.md"
RECEIPT = ROOT / "qa/UNIT_025_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"

SOURCE_EXPECTED = (331447, 6368, "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7")
SPAN_EXPECTED = (12732, "d05781ae58b1b6fd6174d030e52ca9ee6a08048be96f7c103e5be8de473b60b0")
UNIT_EXPECTED = (36578, 1104, "df72add4e57236b51ff7d2a0c99af4b65299365874163cb334be5d0988c0f769")
AUDIT_EXPECTED = (6386, 109, "f252e9f15e0980ed2a2c15dfbd1c22fd6fd99990333e2de9a9372f695523e903")
REVIEW_EXPECTED = (6933, 124, "c7be12ea116b76ea2789b9e1d81cca973ea4d108e97f821eaeba4491ddcb7c08")

EXPECTED_SOURCE_CENSUS = {
    "lecture": 1,
    "definition": 3,
    "lemma": 2,
    "proposition": 2,
    "example": 6,
    "proof": 2,
    "enumerate": 1,
    "enumerate_item": 2,
    "margin": 8,
    "xypic": 2,
    "label": 1,
    "reference": 1,
    "display": 15,
    "exercise": 0,
    "question": 0,
    "citation": 0,
    "external_graphic": 0,
    "input": 0,
    "include": 0,
}

EXPECTED_BLOCKS = {
    "aside": 7,
    "boundary": 1,
    "definition": 3,
    "example": 6,
    "exercise": 6,
    "figure": 2,
    "hint": 6,
    "lemma": 2,
    "proof": 4,
    "proposition": 2,
    "remark": 1,
    "solution": 6,
    "source-audit": 6,
}

EXPECTED_IDS = {
    "o012-rbt-l25",
    "o012-rbt-l25-notice",
    "o012-rbt-l25-s01",
    "o012-rbt-l25-s02",
    "o012-rbt-l25-s03",
    "o012-rbt-l25-s04",
    "o012-rbt-l25-mastery",
    *(f"o012-rbt-l25-def-{n:03d}" for n in range(1, 4)),
    *(f"o012-rbt-l25-exa-{n:03d}" for n in range(1, 7)),
    *(f"o012-rbt-l25-lem-{n:03d}" for n in range(1, 3)),
    *(f"o012-rbt-l25-prop-{n:03d}" for n in range(1, 3)),
    *(f"o012-rbt-l25-fig-{n:03d}" for n in range(1, 3)),
    *(f"o012-rbt-l25-proof-{n:03d}" for n in range(1, 5)),
    *(f"o012-rbt-l25-aside-{n:03d}" for n in range(1, 8)),
    *(f"o012-rbt-l25-audit-{n:03d}" for n in range(1, 7)),
    "o012-rbt-l25-rem-001",
    *(f"o012-rbt-l25-mcheck-{n:03d}" for n in range(1, 7)),
    *(f"o012-rbt-l25-hint-{n:03d}" for n in range(1, 7)),
    *(f"o012-rbt-l25-sol-{n:03d}" for n in range(1, 7)),
    "o012-rbt-l25-boundary-001",
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
    # Any failing rerun removes the earlier PASS receipt before doing work.
    RECEIPT.unlink(missing_ok=True)
    checks: list[dict[str, str]] = []

    def passed(name: str, detail: str) -> None:
        checks.append({"check": name, "status": "PASS", "detail": detail})

    _, source_text = read_frozen(AUTHORITY, SOURCE_EXPECTED)
    _, unit_text = read_frozen(UNIT, UNIT_EXPECTED)
    _, audit_text = read_frozen(AUDIT, AUDIT_EXPECTED)
    _, review_text = read_frozen(REVIEW, REVIEW_EXPECTED)
    passed("required_files_and_identities", "authority, corrected reader, audit, and final independent review match frozen bytes")

    source_lines = source_text.splitlines()
    require(len(source_lines) == 6368, "authority physical-line count mismatch")
    span_text = "\n".join(source_lines[5369:5611]) + "\n"
    span_data = span_text.encode("utf-8")
    require((len(span_data), sha256(span_data)) == SPAN_EXPECTED, "source span identity mismatch")
    require(r"\lecturenum{25}" in source_lines[5369], "line 5370 lacks the Lecture 25 marker")
    require(source_lines[5610] == "", "line 5611 is not the retained blank terminal line")
    require(source_lines[5611].startswith(r"Recall\lecturenum{26}"), "line 5612 is not the intact Lecture 26 boundary")
    passed("source_boundary", "Notes.tex:5370-5611 is 12,732 LF bytes; next cursor 5612 is intact")

    source_patterns = {
        "lecture": r"\\lecturenum\{25\}",
        "definition": r"\\begin\{definition\}",
        "lemma": r"\\begin\{lemma\}",
        "proposition": r"\\begin\{prop\}",
        "example": r"\\begin\{example\}",
        "proof": r"\\begin\{proof\}",
        "enumerate": r"\\begin\{enumerate\}",
        "enumerate_item": r"\\item\b",
        "margin": r"\\marginnote\{",
        "xypic": r"\\xymatrix\{",
        "label": r"\\label\{",
        "reference": r"\\ref\{",
        "display": r"\\\[",
        "exercise": r"\\begin\{exercise\}",
        "question": r"\\begin\{q\}",
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
            "tidak disponsori, didukung,",
            "disahkan, ataupun diberi status resmi",
            "kredit kontributor manusia",
            COMMIT,
            "Notes.tex baris 5370--5611",
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
    require(len(ids) == 59 and len(set(ids)) == 59, "stable-ID count or uniqueness mismatch")
    require(set(ids) == EXPECTED_IDS, f"stable-ID set mismatch: {sorted(set(ids) ^ EXPECTED_IDS)}")
    require(len(re.findall(r"(?m)^#{1,6} .*\{[^}]*#o012-", unit_text)) == 7, "identified-heading census mismatch")
    passed("stable_ids", "59 occurrences, 59 unique IDs, exact expected set; 7 identified headings")

    opens = re.findall(r"(?m)^[ \t]*::: \{\.([a-z-]+)\s+#o012-", unit_text)
    closes = re.findall(r"(?m)^[ \t]*:::\s*$", unit_text)
    block_census = {kind: opens.count(kind) for kind in sorted(set(opens))}
    require(len(opens) == len(closes) == 52, "fenced-div census or balance mismatch")
    require(block_census == EXPECTED_BLOCKS, f"semantic-block inventory mismatch: {block_census}")
    require(unit_text.count("$$") == 148, "display-math delimiter census mismatch")
    for line_number, line in enumerate(unit_text.splitlines(), start=1):
        dollars = len(re.findall(r"(?<!\\)\$", line))
        require(dollars % 2 == 0, f"unclosed line-local math delimiter at reader line {line_number}")
    passed("balanced_structure", f"52 balanced fenced objects; {json.dumps(block_census, sort_keys=True)}; math delimiters balanced")

    require(unit_text.count('data-source-label="eg:dim_minus_one_skeleton_rel_cochains"') == 1, "source-label alias mismatch")
    require(unit_text.count('data-origin="edition-original"') == 18, "mastery-origin census mismatch")
    require(unit_text.count('data-origin="edition-proof-closure"') == 2, "edition proof-closure census mismatch")
    require(unit_text.count('data-origin="source-proof-completed-by-edition"') == 1, "completed source-proof census mismatch")
    require(unit_text.count('data-origin="source-proof-repaired-by-edition"') == 1, "repaired source-proof census mismatch")
    require(unit_text.count("#o012-rbt-l25-exa-001") == 2, "source-label cross-reference topology mismatch")
    passed("semantic_attributes_and_alias", "one source alias/reference, four proof origins, and 18 mastery origins exact")

    order_markers = [
        "#o012-rbt-l25-def-001",
        "#o012-rbt-l25-exa-001",
        "#o012-rbt-l25-proof-001",
        "#o012-rbt-l25-prop-001",
        "#o012-rbt-l25-fig-001",
        "#o012-rbt-l25-proof-002",
        "#o012-rbt-l25-exa-002",
        "#o012-rbt-l25-exa-003",
        "#o012-rbt-l25-def-002",
        "#o012-rbt-l25-exa-004",
        "#o012-rbt-l25-def-003",
        "#o012-rbt-l25-exa-005",
        "#o012-rbt-l25-lem-002",
        "#o012-rbt-l25-fig-002",
        "#o012-rbt-l25-proof-003",
        "#o012-rbt-l25-exa-006",
        "#o012-rbt-l25-prop-002",
        "#o012-rbt-l25-proof-004",
        "#o012-rbt-l25-rem-001",
        "#o012-rbt-l25-mastery",
        "#o012-rbt-l25-boundary-001",
    ]
    positions = [unit_text.index(marker) for marker in order_markers]
    require(positions == sorted(positions), "source and edition-closure order mismatch")
    passed("source_order", "all source objects, edition proof closures, mastery, and terminal boundary occur in intended order")

    compact = re.sub(r"\s+", "", unit_text)
    compact_required = [
        r"C^0(X_\bullet,\operatorname{sk}_{n-1}X_\bullet;R)",
        r"C^n(X_\bullet,\operatorname{sk}_{n-1}X_\bullet;R)&=\ker\!\left(R^{X_n}\longrightarrowR^\varnothing=0\right)",
        r"&=R^{X_n}",
        r"H^k(\operatorname{sk}_nX_\bullet;R)\congH^k(X_\bullet;R)",
        r"C^{k-1}\xrightarrow{\delta_{k-1}}C^k\xrightarrow{\delta_k}C^{k+1}",
        r"0\longrightarrowC^\bullet(X_\bullet,A_\bullet;R)\xrightarrow{j}C^\bullet(X_\bullet;R)\xrightarrow{i^*}C^\bullet(A_\bullet;R)\longrightarrow0",
        r"\partial^k[a]:=[\deltax]\inH^{k+1}(X_\bullet,A_\bullet;R)",
        r"\rho_{x_0}(a_0,a_1)=a_0",
        r"0\longrightarrowR\xrightarrow{0}R\xrightarrow{\operatorname{id}}R\xrightarrow{0}R\xrightarrow{\operatorname{id}}R\longrightarrow\cdots",
        r"C^\bullet(Pt_\bullet;R)\longrightarrowC^\bullet(\operatorname{sk}_0Pt_\bullet;R)",
        r"\betaf=f'\alpha",
        r"\gammag=g'\beta",
        r"\deltah=h'\gamma",
        r"\varepsilonk=k'\delta",
        r"\delta(h(c))=h'(\gamma(c))=0",
        r"\beta(f(a))=f'(\alpha(a))=f'(a')=\beta(b)",
        r"g(n)=g(n+1)-h(n)",
        r"|X_d|=\dimC^d=h_d+r_{d-1}+r_d",
        r"\sum_{d=0}^{\infty}(-1)^dr_{d-1}=-\sum_{j=0}^{\infty}(-1)^jr_j",
        r"\sum_{d=m}^{m+N}(-1)^d\dimV_d=\sum_{d=m}^{m+N}(-1)^d\dimH^d(V_\bullet)",
    ]
    require_all(compact, compact_required, "mathematical invariant")
    require_all(
        unit_text,
        [
            "ketakbergantungan dari pilihan",
            "Kealamian mengikuti",
            r"ada $b'\in B'$",
            r"Karena $\beta$ injektif, $f(a)=b$",
            "rank--nulitas",
            "Dua jumlah yang memuat peringkat diferensial saling meniadakan",
        ],
        "proof-closure invariant",
    )
    require("Kursorsumberberikutnyayangtepatadalah**Notes.texbaris5612**" in compact, "terminal source cursor statement is absent")
    passed("mathematical_fidelity", "skeleton proof, relative LES, Five Lemma completion, infinite-line recursion, Euler correction, and closing identity exact")

    raw_layout = re.findall(
        r"\\(?:xymatrix|marginnote|setfloatalignment|begin\{tikzpicture\}|includegraphics)",
        unit_text,
    )
    require(not raw_layout, f"raw positional TeX command remains: {raw_layout}")
    require_all(
        unit_text,
        [
            "penggambaran ulang diagram Xy-pic sumber tanpa ketergantungan pada posisi",
            "Daftar objek, panah, dan persamaan ini menggambar ulang diagram Xy-pic",
            "Notasi aljabar homologis",
            "Aproksimasi yang lebih halus",
            "Dua catatan tentang contoh",
            "Mengapa disebut tebal?",
            "Tentang nama",
            "Mengapa jumlahnya berhingga?",
            "Koefisien",
        ],
        "semantic reflow and margin coverage",
    )
    passed("accessible_semantic_reflow", "2 Xy-pic surfaces replaced semantically; all 8 source margins are in reading order; no raw layout command")

    terms = [
        "himpunan-$\\Delta$",
        "kompleks korantai simpleksial relatif",
        "kohomologi relatif",
        "kohomologi tereduksi",
        "bertitik dasar",
        "kuasi-isomorfisma",
        "barisan eksak panjang",
        "Lema Lima",
        "karakteristik Euler",
    ]
    require_all(unit_text, terms, "admitted Indonesian terminology")
    require(not re.search(r"\bkorantai simplicial\b", unit_text, re.IGNORECASE), "superseded term 'korantai simplicial' remains")
    for prefix in ("mcheck", "hint", "sol"):
        observed = re.findall(fr"#o012-rbt-l25-{prefix}-(\d{{3}})", unit_text)
        require(observed == [f"{n:03d}" for n in range(1, 7)], f"{prefix} mastery sequence mismatch")
    passed("language_and_mastery", "admitted id-ID terminology; six exact problem/hint/full-solution triples")

    require_all(
        audit_text,
        [
            "Status: source frozen; translation not yet admitted",
            SPAN_EXPECTED[1],
            "physical lines **5370–5611**",
            "Supply the omitted proof",
            "The long exact sequence proposition has no source proof",
            "source leaves the entire injectivity half",
            "Repair the proof of the Euler-characteristic proposition",
            "exact next source cursor",
        ],
        "source audit",
    )
    require_all(
        review_text,
        [
            "- P1: 0",
            "- P2: 0",
            "- P3: 0",
            "Resolved pre-admission finding",
            "UNIT025-TERM-P3-001",
            UNIT_EXPECTED[2],
            "449 MathML nodes",
            "evidence package is **PASS**",
        ],
        "independent review",
    )
    passed("audit_and_review", "source audit is exact; final review records P1=0, P2=0, P3=0 and the resolved terminology finding")

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
    require(len(dom_ids) == len(set(dom_ids)) == 60, "rendered DOM-ID census or uniqueness mismatch")
    require(EXPECTED_IDS.issubset(set(dom_ids)), "rendered HTML lost one or more stable IDs")
    fragment_ids = [html_lib.unescape(value) for value in re.findall(r'\bhref="#([^"]+)"', html_text)]
    unresolved = sorted(set(fragment_ids) - set(dom_ids))
    require(fragment_ids == ["o012-rbt-l25-exa-001"] and not unresolved, "fragment-link topology mismatch")
    mathml_nodes = len(re.findall(r"<math\b", html_text))
    require(mathml_nodes == 449, f"MathML-node census mismatch: {mathml_nodes}")
    require(not re.search(r'<span class="math (?:display|inline)">', html_text), "raw-TeX math fallback remains")
    require(not re.search(r"(?is)<script\b[^>]*\bsrc\s*=|<link\b[^>]*\brel=\"stylesheet\"", html_text), "runtime dependency remains")
    passed("pandoc_html5_mathml", "pandoc 3.9.0.2; exit 0; warnings fatal; 449 MathML nodes; all IDs and same-file fragment resolve")

    verifier_data = Path(__file__).read_bytes()
    resolved_findings = [
        {
            "finding_id": "UNIT025-TERM-P3-001",
            "severity": "P3",
            "path": "source/id-ID/units/unit-025-lecture-025.md",
            "line": 56,
            "initial_observation": "reader used 'kompleks korantai simplicial relatif' instead of the admitted lane term",
            "resolution": "owning task replaced only 'simplicial' with 'simpleksial' before admission and QA was rebound",
            "reader_affected": True,
            "status": "RESOLVED_BEFORE_ADMISSION",
        }
    ]
    receipt = {
        "schema_version": "1.0",
        "qa_id": "O012-RBT-L25-QA",
        "status": "PASS",
        "source": {
            "path": str(AUTHORITY.relative_to(ROOT)).replace("\\", "/"),
            "commit": COMMIT,
            "line_start": 5370,
            "line_end": 5611,
            "bytes": SOURCE_EXPECTED[0],
            "lines": SOURCE_EXPECTED[1],
            "sha256": SOURCE_EXPECTED[2],
            "span_bytes": SPAN_EXPECTED[0],
            "span_sha256": SPAN_EXPECTED[1],
            "source_census": source_census,
            "next_line": 5612,
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
            "restored_degree_zero_relative_cochain": True,
            "typed_two_point_restriction": True,
            "typed_five_lemma_b_prime": True,
            "repaired_euler_rank_nullity": True,
            "restored_closing_bounded_complex_formula": True,
            "admitted_simpleksial_terminology": True,
        },
        "proof_closure": {
            "skeleton_stability": True,
            "relative_long_exact_sequence": True,
            "five_lemma_surjectivity": True,
            "five_lemma_injectivity": True,
            "euler_characteristic": True,
            "mastery_solution_triples": 6,
        },
        "rendering": {
            "pandoc": version,
            "target": "HTML5 native MathML",
            "mathml_nodes": mathml_nodes,
            "runtime_fallback": False,
            "same_file_fragment": "o012-rbt-l25-exa-001",
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
