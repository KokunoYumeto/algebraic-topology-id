#!/usr/bin/env python3
"""Fail-closed, source-bounded QA for Roberts Lecture 23.

The verifier reads only the frozen Roberts authority, the final Unit 23
reader, and the explicitly named Unit 23 controls. It never scans the
workspace. A stale receipt is removed at startup and a new receipt is written
only when every source, mathematical, structural, accessibility, rights, and
rendering gate passes.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = Path(__file__).resolve()
UNIT = ROOT / "source" / "id-ID" / "units" / "unit-023-lecture-023.md"
SOURCE = ROOT / "authority" / "upstream" / (
    "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
) / "Notes.tex"
TERMS = ROOT / "00_control" / "TERMINOLOGY.csv"
ADVERSE = ROOT / "00_control" / "ADVERSE_LEDGER.csv"
AUDIT = ROOT / "qa" / "UNIT_023_SOURCE_AUDIT.md"
REVIEW = ROOT / "qa" / "UNIT_023_INDEPENDENT_REVIEW.md"
OUTPUT = ROOT / "qa" / "UNIT_023_QA.json"

UPSTREAM_COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
SOURCE_BYTES = 331_447
SOURCE_LINES = 6_368
SOURCE_SHA256 = "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7"
LINE_START = 4_939
LINE_END = 5_112
NEXT_LINE = 5_113
EXAMPLE_START = 5_076
EXAMPLE_END = 5_121
SPAN_BYTES = 9_776
SPAN_SHA256 = "c7256a45621ad7a435277867298e4aeb8eb584dfce066cdae3b48c4ee0e0e3f4"

UNIT_BYTES = 39_176
UNIT_LINES = 1_094
UNIT_SHA256 = "6f05ddbe6a720109797976c6929b0535f21a38353673cb42d9646a3196f56bd2"
AUDIT_BYTES = 5_254
AUDIT_SHA256 = "4777f7c14d35e5fb977955818ff7ab133ecc91adb3575867f0e97f8ff00d28b3"
REVIEW_BYTES = 3_149
REVIEW_SHA256 = "dce8f82872186285c85a42b61b1bbf8fb9fd8e809eea5bccd6367dc87958c880"

MODEL_PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def add(checks: list[dict[str, str]], name: str, passed: bool, detail: str) -> None:
    checks.append({"check": name, "status": "PASS" if passed else "FAIL", "detail": detail})


def read_utf8(path: Path) -> tuple[bytes, str] | None:
    try:
        raw = path.read_bytes()
        return raw, raw.decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def privacy_markers(text: str) -> list[str]:
    low = text.lower().replace("\\", "/")
    markers = {
        "windows-user-path": "c:/users/",
        "github-token": "github_pat_",
        "github-classic-token": "ghp_",
        "gitlab-token": "glpat-",
        "openai-token": "sk-proj-",
        "bearer-token": "bearer ",
        "access-token": "access_token",
        "api-token": "api_token",
        "zenodo-token": "zenodo token",
    }
    return [name for name, marker in markers.items() if marker in low]


def expected_ids() -> set[str]:
    return {
        "o012-rbt-l23-notice",
        "o012-rbt-l23",
        "o012-rbt-l23-mastery",
        *{f"o012-rbt-l23-s{i:02d}" for i in range(1, 5)},
        *{f"o012-rbt-l23-fig-{i:03d}" for i in range(1, 3)},
        *{f"o012-rbt-l23-audit-{i:03d}" for i in range(1, 9)},
        *{f"o012-rbt-l23-margin-{i:03d}" for i in range(1, 7)},
        "o012-rbt-l23-rem-001",
        "o012-rbt-l23-lem-001",
        *{f"o012-rbt-l23-proof-{i:03d}" for i in range(1, 5)},
        "o012-rbt-l23-cor-001",
        *{f"o012-rbt-l23-exa-{i:03d}" for i in range(1, 3)},
        *{f"o012-rbt-l23-mcheck-{i:03d}" for i in range(1, 7)},
        *{f"o012-rbt-l23-hint-{i:03d}" for i in range(1, 7)},
        *{f"o012-rbt-l23-sol-{i:03d}" for i in range(1, 7)},
        "o012-rbt-l23-boundary-001",
    }


OPEN_FENCE = re.compile(r"^(?P<indent>[ \t]*):::\s*\{(?P<attrs>[^}]*)\}\s*$")
CLOSE_FENCE = re.compile(r"^[ \t]*:::\s*$")


def parse_fences(text: str) -> tuple[list[dict[str, object]], list[str]]:
    records: list[dict[str, object]] = []
    stack: list[dict[str, object]] = []
    errors: list[str] = []
    for number, line in enumerate(text.splitlines(), start=1):
        opening = OPEN_FENCE.match(line)
        if opening:
            attrs = opening.group("attrs")
            kind_match = re.search(r"(?:^|\s)\.([a-z][a-z0-9-]*)", attrs)
            id_match = re.search(r"(?:^|\s)#(o012-rbt-l23(?:-[a-z0-9-]+)?)", attrs)
            record: dict[str, object] = {
                "start": number,
                "end": None,
                "indent": len(opening.group("indent").expandtabs(4)),
                "kind": kind_match.group(1) if kind_match else "",
                "id": id_match.group(1) if id_match else "",
                "attrs": attrs,
            }
            records.append(record)
            stack.append(record)
        elif CLOSE_FENCE.match(line):
            if not stack:
                errors.append(f"orphan closing fence at line {number}")
            else:
                stack.pop()["end"] = number
    if stack:
        errors.extend(f"unclosed fence at line {item['start']}" for item in stack)
    return records, errors


def payload(text: str, record: dict[str, object]) -> str:
    lines = text.splitlines()
    start = int(record["start"])
    end = int(record["end"] or start)
    return "\n".join(lines[start : end - 1])


def source_census(span: str) -> dict[str, int]:
    active = "\n".join(
        line for line in span.splitlines() if not line.lstrip().startswith("%")
    )
    patterns = {
        "remark_begin": r"\\begin\{rem\}",
        "remark_end": r"\\end\{rem\}",
        "lemma_begin": r"\\begin\{lemma\}",
        "lemma_end": r"\\end\{lemma\}",
        "corollary_begin": r"\\begin\{corollary\}",
        "corollary_end": r"\\end\{corollary\}",
        "example_begin": r"\\begin\{example\}",
        "example_end": r"\\end\{example\}",
        "enumerate_begin": r"\\begin\{enumerate\}",
        "enumerate_end": r"\\end\{enumerate\}",
        "enumerate_item": r"(?m)^\s*\\item\b",
        "margin": r"\\marginnote",
        "xypic": r"\\xymatrix(?:nocompile)?",
        "reference": r"\\ref\{",
        "display": r"\\\[",
        "align_star": r"\\begin\{align\*\}",
        "definition": r"\\begin\{definition\}",
        "proof": r"\\begin\{proof\}",
        "exercise": r"\\begin\{ex\}",
        "construction": r"\\begin\{(?:constr|construction)\}",
        "label": r"\\label\{",
        "citation": r"\\cite(?:\[|\{)",
        "tikz": r"\\begin\{tikzpicture\}",
        "external_graphic": r"\\includegraphics",
        "input": r"\\input(?:\s|\{)",
        "include": r"\\include(?:\s|\{)",
    }
    return {name: len(re.findall(pattern, active)) for name, pattern in patterns.items()}


def check_source(checks: list[dict[str, str]], raw: bytes, text: str) -> dict[str, int]:
    lines = text.splitlines()
    identity_ok = (
        len(raw) == SOURCE_BYTES
        and len(lines) == SOURCE_LINES
        and digest(raw) == SOURCE_SHA256
    )
    add(
        checks,
        "source_identity",
        identity_ok,
        f"Notes.tex {len(raw):,} bytes/{len(lines):,} lines; SHA-256 {digest(raw)}",
    )

    span_lines = lines[LINE_START - 1 : LINE_END]
    # The physical slice includes the terminator of its final blank line.
    span = "\n".join(span_lines) + "\n"
    span_raw = span.encode("utf-8")
    boundary_ok = (
        len(span_lines) == 174
        and len(span_raw) == SPAN_BYTES
        and digest(span_raw) == SPAN_SHA256
        and r"\lecturenum{23}" in span_lines[0]
        and lines[LINE_END - 1] == ""
        and r"\lecturenum{24}" in lines[NEXT_LINE - 1]
        and lines[EXAMPLE_START - 1].strip() == r"\begin{example}"
        and lines[EXAMPLE_END - 1].strip() == r"\end{example}"
        and r"\lecturenum{24}" not in span
    )
    add(
        checks,
        "source_boundary_and_continuation",
        boundary_ok,
        (
            f"Notes.tex:{LINE_START}-{LINE_END}; 174 physical lines; "
            f"{len(span_raw):,} LF bytes; SHA-256 {digest(span_raw)}; "
            f"Lecture 24 marker {NEXT_LINE}; example {EXAMPLE_START}-{EXAMPLE_END}"
        ),
    )

    observed = source_census(span)
    expected = {
        "remark_begin": 1,
        "remark_end": 1,
        "lemma_begin": 1,
        "lemma_end": 1,
        "corollary_begin": 1,
        "corollary_end": 1,
        "example_begin": 2,
        "example_end": 1,
        "enumerate_begin": 2,
        "enumerate_end": 2,
        "enumerate_item": 6,
        "margin": 6,
        "xypic": 2,
        "reference": 1,
        "display": 9,
        "align_star": 1,
        "definition": 0,
        "proof": 0,
        "exercise": 0,
        "construction": 0,
        "label": 0,
        "citation": 0,
        "tikz": 0,
        "external_graphic": 0,
        "input": 0,
        "include": 0,
    }
    add(
        checks,
        "source_census",
        observed == expected,
        json.dumps(observed, sort_keys=True)
        if observed == expected
        else f"observed={observed}; expected={expected}",
    )
    return observed


def check_unit_identity(checks: list[dict[str, str]], raw: bytes, text: str) -> None:
    lines = text.splitlines()
    ok = (
        len(raw) == UNIT_BYTES
        and len(lines) == UNIT_LINES
        and digest(raw) == UNIT_SHA256
        and b"\r" not in raw
        and raw.endswith(b"\n")
    )
    add(
        checks,
        "unit_identity_and_encoding",
        ok,
        f"{len(raw):,} bytes/{len(lines):,} LF lines; SHA-256 {digest(raw)}",
    )


def check_math_delimiters(checks: list[dict[str, str]], text: str) -> None:
    odd_lines: list[int] = []
    malformed: list[int] = []
    for number, line in enumerate(text.splitlines(), start=1):
        if len(re.findall(r"(?<!\\)\$", line)) % 2:
            odd_lines.append(number)
        if "\\nqquad" in line or re.search(r"(?<!\$)\\square\$", line):
            malformed.append(number)
    ok = not odd_lines and not malformed
    add(
        checks,
        "line_local_math_delimiters",
        ok,
        "every unescaped dollar delimiter is closed on its own source line"
        if ok
        else f"odd-dollar-lines={odd_lines}; malformed={malformed}",
    )


def check_provenance(checks: list[dict[str, str]], text: str) -> None:
    flat = " ".join(text.split())
    required = (
        'title: "Topologi Aljabar"',
        'subtitle: "Unit 23: Evaluasi, Gabungan Saling Lepas, dan Perekatan Korantai"',
        'lang: id-ID',
        'rights: "Materi adaptasi dan materi pendamping: CC BY 4.0;',
        "David Michael Roberts (materi sumber)",
        "© 2019 David Michael Roberts",
        UPSTREAM_COMMIT,
        "Notes.tex baris 4939--5112",
        SPAN_SHA256,
        "Creative Commons Attribution 4.0 International (CC BY 4.0)",
        "tidak disponsori, didukung, disahkan, ataupun diberi",
        MODEL_PROVENANCE,
        "kredit kontributor manusia",
    )
    missing = [needle for needle in required if needle not in flat]
    forbidden = [needle for needle in ("TTP", "Translation and Transcription Project") if needle in text]
    add(
        checks,
        "rights_provenance_and_nonendorsement",
        not missing and not forbidden,
        "author, exact source, CC BY 4.0, changes, non-endorsement, human credit, and exact model provenance present"
        if not missing and not forbidden
        else f"missing={missing}; forbidden={forbidden}",
    )

    private = privacy_markers(text)
    add(
        checks,
        "privacy",
        not private,
        "no credential or local-user-path marker" if not private else str(private),
    )


def check_structure(
    checks: list[dict[str, str]], text: str
) -> tuple[list[str], list[dict[str, object]]]:
    ids = re.findall(r"#(o012-rbt-l23(?:-[a-z0-9-]+)?)(?=[}\s])", text)
    unique = set(ids)
    wanted = expected_ids()
    id_ok = len(ids) == len(unique) == len(wanted) == 51 and unique == wanted
    add(
        checks,
        "stable_ids",
        id_ok,
        "51 occurrences, 51 unique IDs, exact expected set"
        if id_ok
        else (
            f"occurrences={len(ids)}; unique={len(unique)}; "
            f"missing={sorted(wanted-unique)}; unexpected={sorted(unique-wanted)}"
        ),
    )

    records, fence_errors = parse_fences(text)
    allowed = {
        "proof", "source-audit", "source-margin", "figure", "example",
        "exercise", "hint", "solution", "lemma", "corollary", "remark",
        "boundary",
    }
    expected_counts = {
        "proof": 4,
        "source-audit": 8,
        "source-margin": 6,
        "figure": 2,
        "example": 2,
        "exercise": 6,
        "hint": 6,
        "solution": 6,
        "lemma": 1,
        "corollary": 1,
        "remark": 1,
        "boundary": 1,
    }
    observed_counts = dict(sorted(Counter(str(item["kind"]) for item in records).items()))
    missing_attributes = [
        int(item["start"])
        for item in records
        if not item["id"] or item["kind"] not in allowed or item["end"] is None
    ]
    fence_ok = (
        not fence_errors
        and len(records) == 44
        and observed_counts == expected_counts
        and not missing_attributes
    )
    add(
        checks,
        "balanced_fences_and_inventory",
        fence_ok,
        (
            "44 balanced fenced semantic objects (indentation allowed): "
            + json.dumps(observed_counts, sort_keys=True)
        )
        if fence_ok
        else (
            f"records={len(records)}; counts={observed_counts}; "
            f"errors={fence_errors}; malformed={missing_attributes}"
        ),
    )

    by_id = {str(item["id"]): item for item in records}
    attr_errors: list[str] = []
    for index in range(1, 5):
        item = by_id.get(f"o012-rbt-l23-proof-{index:03d}")
        if not item or 'data-origin="edition-proof-closure"' not in str(item["attrs"]):
            attr_errors.append(f"proof-{index:03d}")
    for kind, prefix in (("exercise", "mcheck"), ("hint", "hint"), ("solution", "sol")):
        for index in range(1, 7):
            item = by_id.get(f"o012-rbt-l23-{prefix}-{index:03d}")
            if (
                not item
                or item["kind"] != kind
                or 'data-origin="edition-original"' not in str(item["attrs"])
            ):
                attr_errors.append(f"{kind}-{index:03d}")
    for index in range(1, 3):
        item = by_id.get(f"o012-rbt-l23-fig-{index:03d}")
        if not item or 'data-source-format="xypic"' not in str(item["attrs"]):
            attr_errors.append(f"figure-{index:03d}")
    continuation = by_id.get("o012-rbt-l23-exa-002")
    if not continuation or 'data-source-status="continues-in-lecture-024"' not in str(continuation["attrs"]):
        attr_errors.append("example-continuation")
    if 'data-proof-status="verified-by-restriction"' not in str(by_id.get("o012-rbt-l23-lem-001", {}).get("attrs", "")):
        attr_errors.append("lemma-proof-status")
    if 'data-proof-status="follows-from-lemma-23.1"' not in str(by_id.get("o012-rbt-l23-cor-001", {}).get("attrs", "")):
        attr_errors.append("corollary-proof-status")
    nested_margin = by_id.get("o012-rbt-l23-margin-002")
    if not nested_margin or int(nested_margin["indent"]) != 3:
        attr_errors.append("indented-margin-002")
    add(
        checks,
        "semantic_attributes",
        not attr_errors,
        "proof origins, mastery origins, Xy-pic provenance, proof status, and cross-lecture state are exact"
        if not attr_errors
        else f"attribute failures={attr_errors}",
    )
    return ids, records


def check_accessibility(
    checks: list[dict[str, str]], text: str, records: list[dict[str, object]]
) -> None:
    raw_commands = re.findall(
        r"\\(?:xymatrix|marginnote|includegraphics|input\{|include\{)|"
        r"\\begin\{(?:tikzpicture|center)\}",
        text,
    )
    runtime = [
        marker
        for marker in ("<script", "javascript:", "mathjax", "katex", "cdn.jsdelivr", "unpkg.com")
        if marker in text.lower()
    ]
    by_id = {str(item["id"]): item for item in records}
    figure_1 = payload(text, by_id["o012-rbt-l23-fig-001"]) if "o012-rbt-l23-fig-001" in by_id else ""
    figure_2 = payload(text, by_id["o012-rbt-l23-fig-002"]) if "o012-rbt-l23-fig-002" in by_id else ""
    semantic = (
        text.count("**Diagram 23.") == 2
        and "Kedua lintasan" in figure_1
        and "Posisi panah pada gambar tidak membawa informasi tambahan" in figure_1
        and "Panah vertikal kiri" in figure_2
        and "kedua lintasan memetakan" in figure_2
        and "| Derajat |" in text
        and "0-2-1-3-0" in text
    )
    ok = not raw_commands and not runtime and semantic
    add(
        checks,
        "accessible_semantic_reflow",
        ok,
        "two Xy-pic diagrams and six margins are semantic/read-order content; no raw diagram command or runtime fallback"
        if ok
        else f"raw={raw_commands}; runtime={runtime}; semantic={semantic}",
    )


def strip_source_audits(text: str) -> str:
    return re.sub(
        r"^[ \t]*:::\s*\{\.source-audit[^\n]*\}\s*\n.*?^[ \t]*:::\s*$",
        "",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )


def check_mathematics(checks: list[dict[str, str]], text: str) -> None:
    flat = " ".join(text.split())
    required = (
        r"C^n(X_\bullet;R)=R^{X_n}",
        r"g\longmapsto g(x)",
        r"\varepsilon_x\colon H^0(X_\bullet;R)\longrightarrow R",
        r"f^*\colon H^0(Y_\bullet;R)\longrightarrow H^0(X_\bullet;R)",
        r"\varepsilon_x\circ f^*=\varepsilon_y",
        "fungtor kontravarian",
        r"R^{P\sqcup Q}\xrightarrow{\ \cong\ }R^P\oplus R^Q",
        r"R^{\bigsqcup_{\alpha\in I}P_\alpha}",
        r"\prod_{\alpha\in I}R^{P_\alpha}",
        r"\rho_{n+1}\delta_{X\sqcup Y}^n",
        r"Z^n(A^\bullet\oplus B^\bullet)",
        r"B^n(A^\bullet\oplus B^\bullet)",
        "teori himpunan ZFC biasa",
        "aksioma pilihan",
        "subhimpunan wajar takkosong",
        r"0\leq n\leq2",
        "X:(4,6,4)",
        "U:(4,5,2)",
        "V:(4,5,2)",
        "W:(4,4,0)",
        "0-2-1-3-0",
        r"\alpha_n(g)=(g|_{U_n},g|_{V_n})",
        r"\beta_n(f,h)=f|_{W_n}-h|_{W_n}",
        r"\ker\beta_n=\operatorname{im}\alpha_n",
        r"\alpha_{n+1}(\delta_X^n g)",
        r"\beta_{n+1}(\delta_U^n f,\delta_V^n h)",
        "barisan eksak pendek kompleks korantai",
        r"X_n=U_n\cup V_n",
        "Bila $R$ bukan gelanggang nol",
        r"\widetilde R^{X/A}:=\ker(\operatorname{ev}_*)",
        r"q^*\big|_{\widetilde R^{X/A}}\colon",
        r"\widetilde R^{X/A}\xrightarrow{\ \cong\ }\ker(i^*)",
        r"A\ne\varnothing",
        r"A=\varnothing",
        r"0\longrightarrow R^X\xrightarrow{\ \operatorname{id}\ }R^X",
        "[Contoh 22.8](#o012-rbt-l22-exa-008)",
    )
    missing = [needle for needle in required if needle not in flat]
    substantive = strip_source_audits(text)
    forbidden = (
        r"R^{P\sqcup Q}\cong R^Q\oplus R^Q",
        "H^(",
        "pelekatan",
        "titik pangkal",
        "berpangkal",
        "perpanjangan nol",
        "isomorfisme",
        "funktor ",
    )
    substantive_flat = " ".join(substantive.split())
    found = [needle for needle in forbidden if needle in substantive_flat]
    add(
        checks,
        "mathematical_and_language_invariants",
        not missing and not found,
        (
            "typed evaluation/augmentation, finite sum vs arbitrary product, componentwise cohomology, "
            "tetrahedral census, gluing exactness, quotient reduction, and admitted language are present"
        )
        if not missing and not found
        else f"missing={missing}; forbidden={found}",
    )


def check_continuation(
    checks: list[dict[str, str]], text: str, records: list[dict[str, object]]
) -> None:
    by_id = {str(item["id"]): item for item in records}
    example = by_id.get("o012-rbt-l23-exa-002")
    boundary = by_id.get("o012-rbt-l23-boundary-001")
    example_text = " ".join(payload(text, example).split()) if example else ""
    boundary_text = " ".join(payload(text, boundary).split()) if boundary else ""
    required_example = (
        "Lingkungan `example` sumber yang dibuka pada",
        "Baris 5112 kosong",
        "Kuliah 24 dimulai di baris 5113",
        "baru ditutup pada baris 5121",
        "Baris 5113--5121 tidak",
    )
    required_boundary = (
        "berhenti pada Notes.tex baris 5112",
        r"penanda `\lecturenum{24}` pada baris 5113",
        "dibuka pada baris 5076",
        "baru ditutup pada baris 5121",
        "Kursor sumber berikutnya yang tepat adalah baris 5113",
    )
    missing = [needle for needle in required_example if needle not in example_text]
    missing += [needle for needle in required_boundary if needle not in boundary_text]
    leaked = "Hence,\\lecturenum{24} given a pair" in text
    add(
        checks,
        "cross_lecture_continuation",
        not missing and not leaked,
        "source example remains explicitly open; no Notes.tex:5113-5121 content is imported; cursor is 5113"
        if not missing and not leaked
        else f"missing={missing}; leaked-next-source={leaked}",
    )


def mastery_payloads(text: str, kind: str, prefix: str) -> dict[str, str]:
    pattern = re.compile(
        rf"^[ \t]*:::\s*\{{\.{re.escape(kind)}\s+#(o012-rbt-l23-{prefix}-\d{{3}})[^}}]*\}}\s*\n"
        r"(.*?)(?=^[ \t]*:::\s*$)",
        flags=re.MULTILINE | re.DOTALL,
    )
    return {match.group(1): match.group(2).strip() for match in pattern.finditer(text)}


def check_mastery(checks: list[dict[str, str]], text: str) -> None:
    sets = {
        "exercise": mastery_payloads(text, "exercise", "mcheck"),
        "hint": mastery_payloads(text, "hint", "hint"),
        "solution": mastery_payloads(text, "solution", "sol"),
    }
    expected_suffixes = {f"{index:03d}" for index in range(1, 7)}
    suffixes = {
        kind: {key.rsplit("-", 1)[-1] for key in values}
        for kind, values in sets.items()
    }
    lengths_ok = (
        all(len(value) >= 300 for value in sets["exercise"].values())
        and all(len(value) >= 150 for value in sets["hint"].values())
        and all(len(value) >= 800 for value in sets["solution"].values())
    )
    solution_requirements = {
        "001": (r"g(x)", r"C^k(X_\bullet;R)=R^{X_k}"),
        "002": (r"(\varepsilon_x\circ f^*)([g])", "invers kanan"),
        "003": ("ZFC", "pilihan serentak", r"\prod_\alpha H^n(C_\alpha)"),
        "004": (r"\ker\beta_n=\operatorname{im}\alpha_n", "surjektif"),
        "005": (r"$(4,6,4)$", "W", "0-2-1-3-0"),
        "006": (r"\ker(\operatorname{ev}_*)", r"A=\varnothing", r"\operatorname{id}"),
    }
    solution_missing: dict[str, list[str]] = {}
    for suffix, needles in solution_requirements.items():
        body = sets["solution"].get(f"o012-rbt-l23-sol-{suffix}", "")
        absent = [needle for needle in needles if needle not in body]
        if absent:
            solution_missing[suffix] = absent
    ok = (
        all(len(values) == 6 for values in sets.values())
        and all(value == expected_suffixes for value in suffixes.values())
        and lengths_ok
        and not solution_missing
    )
    add(
        checks,
        "mastery_closure",
        ok,
        "six edition-original problem/hint/full-solution triples close all six declared competencies"
        if ok
        else (
            f"counts={{{', '.join(f'{k!r}: {len(v)}' for k, v in sets.items())}}}; suffixes={suffixes}; "
            f"lengths={lengths_ok}; missing={solution_missing}"
        ),
    )


def check_controls(checks: list[dict[str, str]]) -> tuple[int, int]:
    audit_raw, audit = AUDIT.read_bytes(), AUDIT.read_text(encoding="utf-8")
    review_raw, review = REVIEW.read_bytes(), REVIEW.read_text(encoding="utf-8")
    audit_flat = " ".join(audit.split())
    review_flat = " ".join(review.split())
    audit_ok = (
        len(audit_raw) == AUDIT_BYTES
        and digest(audit_raw) == AUDIT_SHA256
        and UNIT_SHA256 in audit_flat
        and SPAN_SHA256 in audit_flat
        and "51 stable-ID occurrences and 51 unique stable IDs" in audit_flat
        and "44 identified fenced semantic objects" in audit_flat
        and "6 promoted source-margin notes" in audit_flat
        and "4 edition proof closures" in audit_flat
        and "8 source/accessibility audit records" in audit_flat
        and "2 semantic figures" in audit_flat
        and "2 `example`" in audit_flat
        and MODEL_PROVENANCE in audit_flat
    )
    review_ok = (
        len(review_raw) == REVIEW_BYTES
        and digest(review_raw) == REVIEW_SHA256
        and UNIT_SHA256 in review_flat
        and SPAN_SHA256 in review_flat
        and "P1: 0" in review_flat
        and "P2: 0" in review_flat
        and "P3: 0" in review_flat
        and "All 51 structural IDs are unique" in review_flat
        and "All 44 fenced semantic blocks are" in review_flat
        and "six margins" in review_flat
        and "465 MathML nodes" in review_flat
        and MODEL_PROVENANCE in review_flat
    )
    private = privacy_markers(audit + review)
    add(
        checks,
        "source_audit_and_independent_review",
        audit_ok and review_ok and not private,
        (
            f"audit {len(audit_raw):,}/{digest(audit_raw)}; review {len(review_raw):,}/{digest(review_raw)}; "
            "P1=P2=P3=0"
        )
        if audit_ok and review_ok and not private
        else f"audit={audit_ok}; review={review_ok}; privacy={private}",
    )

    with TERMS.open("r", encoding="utf-8", newline="") as handle:
        term_reader = csv.DictReader(handle)
        term_rows = list(term_reader)
        term_header = term_reader.fieldnames
    with ADVERSE.open("r", encoding="utf-8", newline="") as handle:
        adverse_reader = csv.DictReader(handle)
        adverse_rows = list(adverse_reader)
        adverse_header = adverse_reader.fieldnames

    expected_term_header = ["term_id", "source_term", "id_ID", "scope", "status", "note"]
    expected_adverse_header = [
        "event_id", "severity", "source_location", "observed", "action", "status", "rationale"
    ]
    term_numbers = [
        int(match.group(1))
        for row in term_rows
        if (match := re.fullmatch(r"O012-TERM-(\d{4})", row.get("term_id", "")))
    ]
    adverse_numbers = [
        int(match.group(1))
        for row in adverse_rows
        if (match := re.fullmatch(r"O012-ADV-(\d{4})", row.get("event_id", "")))
    ]
    term_map = {row.get("term_id", ""): row for row in term_rows}
    adverse_map = {row.get("event_id", ""): row for row in adverse_rows}
    expected_terms = {
        301: ("augmentation", "augmentasi"),
        302: ("augmented module", "modul teraugmentasi"),
        303: ("direct sum", "jumlah langsung"),
        304: ("product of modules", "produk modul"),
        305: ("direct product", "produk langsung"),
        306: ("restriction map", "pemetaan restriksi"),
        307: ("sub-Delta-set", "sub-himpunan-Delta"),
        308: ("pair of Delta-sets", "pasangan himpunan-Delta"),
        309: ("quotient Delta-set", "himpunan-Delta hasil bagi"),
        310: ("reduced function module", "modul fungsi tereduksi"),
        311: ("reduced cochain", "korantai tereduksi"),
        312: ("relative simplicial cochain complex", "kompleks korantai simpleksial relatif"),
        313: ("degreewise", "pada setiap derajat"),
        314: ("extension by zero", "perluasan dengan nol"),
        315: ("cocycle", "kosiklus"),
    }
    term_failures: list[str] = []
    for number, (source_term, id_term) in expected_terms.items():
        row = term_map.get(f"O012-TERM-{number:04d}")
        if not row or (row.get("source_term"), row.get("id_ID"), row.get("status")) != (
            source_term,
            id_term,
            "admitted",
        ):
            term_failures.append(f"TERM-{number:04d}")

    expected_adverse = {
        312: ("P1", "Notes.tex:4943-4951", "corrected_in_translation"),
        313: ("P1", "Notes.tex:4954-4956", "corrected_in_translation"),
        314: ("P2", "Notes.tex:4958-4959", "corrected_in_translation"),
        315: ("P1", "Notes.tex:4974-4975", "corrected_in_translation"),
        316: ("P2", "Notes.tex:5002-5006", "clarified_in_translation"),
        317: ("P1", "Notes.tex:5023-5024", "corrected_in_translation"),
        318: ("P2", "Notes.tex:5042-5061", "proof_completed_in_translation"),
        319: ("P1", "Notes.tex:5078-5087,5111", "corrected_in_translation"),
        320: ("P1", "Notes.tex:5089-5109", "proof_completed_in_translation"),
        321: ("P2", "Notes.tex:4944-4947,5045-5048,4952-4953,4974,5002,5033,5036,5078-5079", "accessibility_reflow"),
        322: ("P3", "Notes.tex:4941,4952-4953,4987,5002,5013,5050,5057", "corrected_in_translation"),
    }
    adverse_failures: list[str] = []
    for number, (severity, location, status) in expected_adverse.items():
        row = adverse_map.get(f"O012-ADV-{number:04d}")
        if not row or (row.get("severity"), row.get("source_location"), row.get("status")) != (
            severity,
            location,
            status,
        ) or any(not value for value in row.values()):
            adverse_failures.append(f"ADV-{number:04d}")

    term_max = max(term_numbers, default=0)
    adverse_max = max(adverse_numbers, default=0)
    ledger_ok = (
        term_header == expected_term_header
        and adverse_header == expected_adverse_header
        and len(term_numbers) == len(term_rows)
        and len(adverse_numbers) == len(adverse_rows)
        and term_numbers == list(range(1, term_max + 1))
        and adverse_numbers == list(range(1, adverse_max + 1))
        and term_max >= 315
        and adverse_max >= 322
        and not term_failures
        and not adverse_failures
    )
    add(
        checks,
        "terminology_and_adverse_ledgers",
        ledger_ok,
        f"contiguous TERM tail={term_max}; ADV tail={adverse_max}; Unit 23 rows exact"
        if ledger_ok
        else (
            f"headers={term_header}/{adverse_header}; tails={term_max}/{adverse_max}; "
            f"term-failures={term_failures}; adverse-failures={adverse_failures}"
        ),
    )
    return term_max, adverse_max


def check_pandoc(checks: list[dict[str, str]], ids: list[str]) -> str:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        add(checks, "pandoc_html5_mathml", False, "pandoc unavailable")
        return "unavailable"
    version_result = subprocess.run(
        [pandoc, "--version"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    version = version_result.stdout.splitlines()[0].strip() if version_result.stdout else "unknown"
    result = subprocess.run(
        [pandoc, str(UNIT), "--to=html5", "--mathml"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )
    html = result.stdout
    missing = sorted({item for item in ids if f'id="{item}"' not in html})
    math_nodes = len(re.findall(r"<math(?:\s|>)", html))
    runtime = [
        marker
        for marker in ("<script", "mathjax", "katex", "cdn.jsdelivr", "unpkg.com")
        if marker in html.lower()
    ]
    ok = (
        version_result.returncode == 0
        and result.returncode == 0
        and not result.stderr.strip()
        and not missing
        and math_nodes == 465
        and not runtime
    )
    add(
        checks,
        "pandoc_html5_mathml",
        ok,
        f"{version}; exit 0; no warnings; 51 IDs; 465 native MathML nodes; no runtime fallback"
        if ok
        else (
            f"version={version}; exit={result.returncode}; stderr={result.stderr.strip()}; "
            f"missing={missing}; math-nodes={math_nodes}; runtime={runtime}"
        ),
    )
    return version


def emit_failure(checks: list[dict[str, str]], reason: str | None = None) -> int:
    if reason:
        add(checks, "execution", False, reason)
    result = {
        "schema_version": "1.0",
        "qa_id": "O012-RBT-L23-QA",
        "status": "FAIL",
        "checks": checks,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1


def main() -> int:
    checks: list[dict[str, str]] = []
    if OUTPUT.exists():
        try:
            OUTPUT.unlink()
        except OSError as exc:
            return emit_failure(checks, f"cannot remove stale receipt: {exc}")

    required = (UNIT, SOURCE, TERMS, ADVERSE, AUDIT, REVIEW)
    missing = [
        str(path.relative_to(ROOT)).replace("\\", "/")
        for path in required
        if not path.is_file()
    ]
    if missing:
        add(checks, "required_files", False, "missing: " + "; ".join(missing))
        return emit_failure(checks)
    add(checks, "required_files", True, "all six bounded Unit 23 inputs exist")

    source_read = read_utf8(SOURCE)
    unit_read = read_utf8(UNIT)
    if source_read is None or unit_read is None:
        return emit_failure(checks, "authority source or Unit 23 reader is not readable UTF-8")

    source_raw, source_text = source_read
    unit_raw, unit_text = unit_read
    census = check_source(checks, source_raw, source_text)
    check_unit_identity(checks, unit_raw, unit_text)
    check_math_delimiters(checks, unit_text)
    check_provenance(checks, unit_text)
    ids, records = check_structure(checks, unit_text)
    check_accessibility(checks, unit_text, records)
    check_mathematics(checks, unit_text)
    check_continuation(checks, unit_text, records)
    check_mastery(checks, unit_text)
    term_tail, adverse_tail = check_controls(checks)
    pandoc_version = check_pandoc(checks, ids)

    status = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    result = {
        "schema_version": "1.0",
        "qa_id": "O012-RBT-L23-QA",
        "status": status,
        "source": {
            "path": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "commit": UPSTREAM_COMMIT,
            "line_start": LINE_START,
            "line_end": LINE_END,
            "bytes": len(source_raw),
            "lines": len(source_text.splitlines()),
            "sha256": digest(source_raw),
            "span_bytes": SPAN_BYTES,
            "span_sha256": SPAN_SHA256,
            "source_census": census,
            "next_line": NEXT_LINE,
            "cross_lecture_example_end": EXAMPLE_END,
        },
        "unit": {
            "path": str(UNIT.relative_to(ROOT)).replace("\\", "/"),
            "bytes": len(unit_raw),
            "lines": len(unit_text.splitlines()),
            "sha256": digest(unit_raw),
            "stable_ids": len(set(ids)),
            "fenced_semantic_objects": len(records),
        },
        "controls": {
            "source_audit": {
                "path": str(AUDIT.relative_to(ROOT)).replace("\\", "/"),
                "bytes": AUDIT_BYTES,
                "sha256": AUDIT_SHA256,
            },
            "independent_review": {
                "path": str(REVIEW.relative_to(ROOT)).replace("\\", "/"),
                "bytes": REVIEW_BYTES,
                "sha256": REVIEW_SHA256,
                "p1": 0,
                "p2": 0,
                "p3": 0,
            },
            "terminology_tail": term_tail,
            "adverse_ledger_tail": adverse_tail,
        },
        "rendering": {
            "pandoc": pandoc_version,
            "target": "HTML5 native MathML",
            "mathml_nodes": 465,
            "runtime_fallback": False,
        },
        "verifier": {
            "path": str(SCRIPT.relative_to(ROOT)).replace("\\", "/"),
            "sha256": digest(SCRIPT.read_bytes()),
        },
        "checks": checks,
        "model_provenance": MODEL_PROVENANCE,
    }
    if status != "PASS":
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1

    try:
        OUTPUT.write_text(
            json.dumps(result, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    except OSError as exc:
        return emit_failure(checks, f"cannot write PASS receipt: {exc}")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
