#!/usr/bin/env python3
"""Fail-closed, source-bounded QA for Roberts Lecture 21.

The verifier reads only the frozen Roberts authority, the Unit 21 reader, and
the small set of named lane controls. It never scans the workspace and writes
the receipt only after every gate passes.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "source" / "id-ID" / "units" / "unit-021-lecture-021.md"
SOURCE = ROOT / "authority" / "upstream" / (
    "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
) / "Notes.tex"
TERMS = ROOT / "00_control" / "TERMINOLOGY.csv"
ADVERSE = ROOT / "00_control" / "ADVERSE_LEDGER.csv"
AUDIT = ROOT / "qa" / "UNIT_021_SOURCE_AUDIT.md"
REVIEW = ROOT / "qa" / "UNIT_021_INDEPENDENT_REVIEW.md"
HANDOFF = ROOT / "qa" / "UNIT_021_TRANSLATION_HANDOFF.md"
OUTPUT = ROOT / "qa" / "UNIT_021_QA.json"

UPSTREAM_COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
SOURCE_BYTES = 331_447
SOURCE_LINES = 6_368
SOURCE_SHA256 = "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7"
LINE_START = 4346
LINE_END = 4500
NEXT_LINE = 4501
SPAN_BYTES = 7_267
SPAN_SHA256 = "281ba27f0f52f35fd9842954c223546e84ce1a0909ee84c14b2081c38c11f150"
RAW_BYTES = 7_359
RAW_SHA256 = "8a3ab990ae87087dd259340b08cdb7ddb95068a5b9859de66f7e002115307e6f"

# Captured only after the translation, mathematical review, and terminology
# pass were complete. Any later reader mutation must deliberately update every
# bound Unit 21 control.
UNIT_BYTES = 26_237
UNIT_LINES = 786
UNIT_SHA256 = "47fa3994dc59370fc464e9d150d62512a4602a3cffa5996f1027f93a427e0eec"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def add(checks: list[dict[str, str]], name: str, status: str, detail: str) -> None:
    checks.append({"check": name, "status": status, "detail": detail})


def read_utf8(path: Path) -> tuple[bytes, str] | None:
    try:
        raw = path.read_bytes()
        return raw, raw.decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def privacy_markers(text: str) -> list[str]:
    low = text.lower()
    markers = {
        "windows-user-path": "c:/users/",
        "github-token": "github_pat_",
        "github-classic-token": "ghp_",
        "gitlab-token": "glpat-",
        "openai-token": "sk-proj-",
        "bearer-token": "bearer ",
        "access-token": "access_token",
        "api-token": "api_token",
    }
    return [name for name, marker in markers.items() if marker in low]


def source_census(span: str) -> dict[str, int]:
    active = "\n".join(
        line for line in span.splitlines() if not line.lstrip().startswith("%")
    )
    patterns = {
        "example": r"\\begin\{example\}",
        "exercise": r"\\begin\{ex\}",
        "definition": r"\\begin\{definition\}",
        "lemma": r"\\begin\{lemma\}",
        "proof": r"\\begin\{proof\}",
        "remark": r"\\begin\{rem\}",
        "construction": r"\\begin\{(?:constr|construction)\}",
        "margin": r"\\marginnote",
        "tikz": r"\\begin\{tikzpicture\}",
        "label": r"\\label\{",
        "display": r"\\\[",
        "align_star": r"\\begin\{align\*\}",
        "align": r"\\begin\{align\}",
        "cases": r"\\begin\{cases\}",
        "enumerate": r"\\begin\{enumerate\}",
    }
    return {
        name: len(re.findall(pattern, active))
        for name, pattern in patterns.items()
    }


def expected_ids() -> set[str]:
    return {
        "o012-rbt-l21-notice",
        "o012-rbt-l21",
        "o012-rbt-l21-mastery",
        *{f"o012-rbt-l21-s{i:02d}" for i in range(1, 5)},
        "o012-rbt-l21-rem-001",
        *{f"o012-rbt-l21-constr-{i:03d}" for i in range(1, 3)},
        *{f"o012-rbt-l21-def-{i:03d}" for i in range(1, 4)},
        *{f"o012-rbt-l21-exa-{i:03d}" for i in range(1, 5)},
        *{f"o012-rbt-l21-margin-{i:03d}" for i in range(1, 5)},
        *{f"o012-rbt-l21-fig-{i:03d}" for i in range(1, 3)},
        *{f"o012-rbt-l21-audit-{i:03d}" for i in range(1, 6)},
        *{f"o012-rbt-l21-mcheck-{i:03d}" for i in range(1, 7)},
        *{f"o012-rbt-l21-hint-{i:03d}" for i in range(1, 7)},
        *{f"o012-rbt-l21-sol-{i:03d}" for i in range(1, 7)},
        "o012-rbt-l21-boundary-001",
    }


def block_counts(text: str) -> dict[str, int]:
    kinds = (
        "remark", "construction", "definition", "example", "source-margin",
        "figure", "source-audit", "exercise", "hint", "solution", "boundary",
    )
    found = re.findall(
        r"^:::\s*\{\.((?:" + "|".join(kinds) + r"))\s+#o012-rbt-l21\b",
        text,
        flags=re.MULTILINE,
    )
    return dict(sorted(Counter(found).items()))


def block_payloads(text: str, kind: str) -> dict[str, str]:
    pattern = re.compile(
        rf"^:::\s*\{{\.{re.escape(kind)}\s+#(o012-rbt-l21-[^\s}}]+)[^}}]*\}}\s*\n"
        r"(.*?)(?=^:::\s*$)",
        flags=re.MULTILINE | re.DOTALL,
    )
    return {match.group(1): match.group(2) for match in pattern.finditer(text)}


def check_source(checks: list[dict[str, str]], raw: bytes, text: str) -> None:
    lines = text.splitlines()
    identity_ok = (
        len(raw) == SOURCE_BYTES
        and len(lines) == SOURCE_LINES
        and digest(raw) == SOURCE_SHA256
    )
    add(
        checks,
        "source_identity",
        "PASS" if identity_ok else "FAIL",
        f"Notes.tex {len(raw):,} bytes/{len(lines):,} lines; SHA-256 {digest(raw)}",
    )

    span_lines = lines[LINE_START - 1 : LINE_END]
    span = "\n".join(span_lines)
    raw_witness = "\n".join(lines[LINE_START - 1 : NEXT_LINE])
    boundary_ok = (
        len(span_lines) == 155
        and len(span.encode()) == SPAN_BYTES
        and digest(span.encode()) == SPAN_SHA256
        and len(raw_witness.encode()) == RAW_BYTES
        and digest(raw_witness.encode()) == RAW_SHA256
        and span_lines[0] == r"\begin{rem}"
        and r"\lecturenum{21}" in span_lines[1]
        and r"\lecturenum{22}" in lines[NEXT_LINE - 1]
        and not re.search(r"\\begin\{(?:rem|constr|construction|definition|example)\}[^\n]*\Z", span)
    )
    add(
        checks,
        "source_boundary",
        "PASS" if boundary_ok else "FAIL",
        f"Notes.tex:{LINE_START}-{LINE_END}; next marker line {NEXT_LINE}; span SHA-256 {SPAN_SHA256}"
        if boundary_ok
        else f"span={len(span.encode())}/{digest(span.encode())}; witness={len(raw_witness.encode())}/{digest(raw_witness.encode())}",
    )

    observed = source_census(span)
    expected = {
        "example": 4,
        "exercise": 0,
        "definition": 3,
        "lemma": 0,
        "proof": 0,
        "remark": 1,
        "construction": 2,
        "margin": 4,
        "tikz": 2,
        "label": 1,
        "display": 5,
        "align_star": 1,
        "align": 0,
        "cases": 2,
        "enumerate": 1,
    }
    add(
        checks,
        "source_census",
        "PASS" if observed == expected else "FAIL",
        json.dumps(observed, sort_keys=True)
        if observed == expected
        else f"observed={observed}; expected={expected}",
    )


def check_unit(checks: list[dict[str, str]], raw: bytes, text: str) -> list[str]:
    lines = text.splitlines()
    identity = (
        len(raw) == UNIT_BYTES
        and len(lines) == UNIT_LINES
        and digest(raw) == UNIT_SHA256
        and b"\r" not in raw
        and raw.endswith(b"\n")
    )
    add(
        checks,
        "unit_identity_encoding",
        "PASS" if identity else "FAIL",
        f"{len(raw):,} bytes/{len(lines):,} LF lines; SHA-256 {digest(raw)}",
    )

    bare_square = [
        index
        for index, line in enumerate(lines, start=1)
        if re.search(r"(?<!\$)\\square\$", line)
    ]
    malformed_math = [
        index
        for index, line in enumerate(lines, start=1)
        if "\\nqquad" in line or re.search(r"\$[^$]*[δΔΣ][^$]*\$", line)
    ]
    math_ok = not bare_square and not malformed_math
    add(
        checks,
        "math_portability",
        "PASS" if math_ok else "FAIL",
        "no bare proof closure, malformed qquad, or literal Unicode Greek inside math"
        if math_ok
        else f"bare_square={bare_square}; malformed_math={malformed_math}",
    )

    required = (
        "Unit 21:",
        UPSTREAM_COMMIT,
        "Notes.tex baris 4346--4500",
        "baris 4501",
        "CC BY 4.0",
        "David Michael Roberts",
        "OpenAI Codex gpt-5.6-sol, Ultra",
        "tidak disponsori",
        "realisasi geometrik",
        "Simpleks-$n$ standar",
        "triangulasi",
        "homeomorfisma",
    )
    missing = [needle for needle in required if needle not in text]
    add(
        checks,
        "provenance_and_terminology",
        "PASS" if not missing else "FAIL",
        "source range, author, license, non-endorsement, model, and admitted terms present"
        if not missing
        else f"missing={missing}",
    )

    private = privacy_markers(text)
    add(
        checks,
        "privacy",
        "PASS" if not private else "FAIL",
        "no credential or local-user-path markers" if not private else str(private),
    )

    ids = re.findall(r"#(o012-rbt-l21(?:-[a-z0-9-]+)?)(?=[}\s])", text)
    unique = set(ids)
    wanted = expected_ids()
    id_ok = len(ids) == len(unique) == len(wanted) and unique == wanted
    add(
        checks,
        "stable_ids",
        "PASS" if id_ok else "FAIL",
        f"{len(unique)} unique IDs"
        if id_ok
        else f"observed={len(ids)} unique={len(unique)} missing={sorted(wanted-unique)} unexpected={sorted(unique-wanted)}",
    )

    observed = block_counts(text)
    expected = {
        "boundary": 1,
        "construction": 2,
        "definition": 3,
        "example": 4,
        "exercise": 6,
        "figure": 2,
        "hint": 6,
        "remark": 1,
        "solution": 6,
        "source-audit": 5,
        "source-margin": 4,
    }
    add(
        checks,
        "structural_inventory",
        "PASS" if observed == expected else "FAIL",
        json.dumps(observed, sort_keys=True)
        if observed == expected
        else f"observed={observed}; expected={expected}",
    )

    label_ok = text.count('data-source-label="eg:join_interval_geom_real"') == 1
    add(
        checks,
        "source_label",
        "PASS" if label_ok else "FAIL",
        "the one active source label is preserved exactly"
        if label_ok
        else "source label missing or duplicated",
    )

    figures = re.findall(
        r'^:::\s*\{\.figure\s+#(o012-rbt-l21-fig-\d{3})\s+data-source-format="([^"]+)"',
        text,
        re.MULTILINE,
    )
    access_ok = (
        len(figures) == 2
        and {item for item, _ in figures}
        == {"o012-rbt-l21-fig-001", "o012-rbt-l21-fig-002"}
        and Counter(fmt for _, fmt in figures) == Counter({"tikz": 2})
        and text.count("**Diagram 21.") == 2
        and text.count("{.source-margin #o012-rbt-l21-margin-") == 4
        and not re.search(r"\\xymatrix|\\begin\{tikzpicture\}|\\marginnote", text)
        and "ruang ambien" in text
        and "titik sudut" in text
    )
    add(
        checks,
        "accessibility_reflow",
        "PASS" if access_ok else "FAIL",
        "two centered semantic TikZ replacements and four reading-order margins"
        if access_ok
        else f"figures={figures}",
    )
    return ids


def check_pandoc(checks: list[dict[str, str]], ids: list[str]) -> None:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        add(checks, "pandoc_structural_ids", "FAIL", "pandoc unavailable")
        return
    result = subprocess.run(
        [pandoc, str(UNIT), "--to=html5", "--mathjax"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    missing = sorted({item for item in ids if f'id="{item}"' not in result.stdout})
    ok = result.returncode == 0 and not result.stderr.strip() and not missing
    add(
        checks,
        "pandoc_structural_ids",
        "PASS" if ok else "FAIL",
        f"all {len(set(ids))} IDs survive Pandoc; exit 0; no warnings"
        if ok
        else f"exit={result.returncode}; missing={missing}; stderr={result.stderr.strip()}",
    )


def check_mastery(checks: list[dict[str, str]], text: str) -> None:
    expected = {f"{i:03d}" for i in range(1, 7)}
    prefixes = {"exercise": "mcheck", "hint": "hint", "solution": "sol"}
    payloads = {
        kind: {
            key: value
            for key, value in block_payloads(text, kind).items()
            if key.startswith(f"o012-rbt-l21-{prefix}-")
        }
        for kind, prefix in prefixes.items()
    }
    suffixes = {
        kind: {key.rsplit("-", 1)[-1] for key in values}
        for kind, values in payloads.items()
    }
    origins = {
        kind: len(
            re.findall(
                rf'^:::\s*\{{\.{kind}\s+#o012-rbt-l21-{prefix}-\d{{3}}\s+data-origin="edition-original"\}}',
                text,
                re.MULTILINE,
            )
        )
        for kind, prefix in prefixes.items()
    }
    nonempty = all(
        len(body.strip()) >= 120
        for values in payloads.values()
        for body in values.values()
    )
    ok = (
        all(len(values) == 6 for values in payloads.values())
        and all(value == expected for value in suffixes.values())
        and origins == {"exercise": 6, "hint": 6, "solution": 6}
        and nonempty
    )
    add(
        checks,
        "mastery_closure",
        "PASS" if ok else "FAIL",
        "six edition-original problem/hint/full-solution triples"
        if ok
        else f"payloads={list(map(len, payloads.values()))}; suffixes={suffixes}; origins={origins}",
    )


def check_repairs(checks: list[dict[str, str]], text: str) -> None:
    required = (
        "n<0\\text{ atau }n>2",
        "(e,\\partial_i(\\ast))\\sim(d_i(e),\\ast)",
        "(v_0,v_1)\\in\\mathbb R^2",
        "ortan **nonnegatif**",
        "x\\in X_n",
        "\\mathbf v\\in\\Delta^{n-1}",
        "1\\leq n\\leq2",
        "\\tau\\colon\\Sigma\\xrightarrow{\\ \\cong\\ }|X_\\bullet|",
        "fakta geometrik standar",
        "contoh tandingan",
    )
    missing = [needle for needle in required if needle not in text]
    reader_text = re.sub(
        r"^:::\s*\{\.source-audit[^\n]*\}\s*\n.*?^:::\s*$",
        "",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    forbidden = (
        "superceded",
        "imporantly",
        "how do so",
        "dengan ortan positif di $\\mathbb R^3$",
        "isomorfisme",
        "kontraindikasi",
    )
    found = [needle for needle in forbidden if needle in reader_text]
    ok = not missing and not found
    add(
        checks,
        "mathematical_and_language_repairs",
        "PASS" if ok else "FAIL",
        "degree range, typed quotients, simplex boundary, black boxes, and language repairs present"
        if ok
        else f"missing={missing}; forbidden={found}",
    )


def check_controls(checks: list[dict[str, str]]) -> None:
    audit = AUDIT.read_text(encoding="utf-8")
    review = REVIEW.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")
    controls_ok = (
        ("4346–4500" in audit or "4346-4500" in audit)
        and SPAN_SHA256 in audit
        and "4 `example` environments" in audit
        and "Final snapshot" in review
        and UNIT_SHA256 in review
        and "P1: 0" in review
        and "P2: 0" in review
        and "P3: 0" in review
        and UNIT_SHA256 in handoff
        and "155 LF-normalized" in handoff
        and not privacy_markers(audit + review + handoff)
    )
    add(
        checks,
        "source_review_handoff_binding",
        "PASS" if controls_ok else "FAIL",
        "audit, review, and handoff bind the final Unit 21 hash"
        if controls_ok
        else "one or more Unit 21 controls are stale or incomplete",
    )

    terms = TERMS.read_text(encoding="utf-8")
    adverse = ADVERSE.read_text(encoding="utf-8")
    term_ok = all(f"O012-TERM-{i:04d}" in terms for i in range(290, 293))
    adverse_ok = all(f"O012-ADV-{i:04d}" in adverse for i in range(290, 298))
    term_ids = [int(item) for item in re.findall(r"O012-TERM-(\d{4})", terms)]
    adv_ids = [int(item) for item in re.findall(r"O012-ADV-(\d{4})", adverse)]
    contiguous = (
        term_ids == list(range(1, max(term_ids) + 1))
        and adv_ids == list(range(1, max(adv_ids) + 1))
    )
    ok = term_ok and adverse_ok and contiguous
    add(
        checks,
        "terminology_and_ledger",
        "PASS" if ok else "FAIL",
        "TERM tail=292; ADV tail=297; Unit 21 controls present"
        if ok
        else "ledger or glossary controls are incomplete or noncontiguous",
    )


def main() -> int:
    checks: list[dict[str, str]] = []
    required = (UNIT, SOURCE, TERMS, ADVERSE, AUDIT, REVIEW, HANDOFF)
    missing = [
        str(path.relative_to(ROOT)).replace("\\", "/")
        for path in required
        if not path.is_file()
    ]
    if missing:
        add(checks, "required_files", "FAIL", "missing: " + "; ".join(missing))
        result = {
            "schema_version": "1.0",
            "qa_id": "O012-RBT-L21-QA",
            "status": "FAIL",
            "checks": checks,
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1
    add(checks, "required_files", "PASS", "all bounded Unit 21 inputs exist")

    source_read = read_utf8(SOURCE)
    unit_read = read_utf8(UNIT)
    if source_read is None or unit_read is None:
        add(checks, "encoding", "FAIL", "source or unit is not readable UTF-8")
        print(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "qa_id": "O012-RBT-L21-QA",
                    "status": "FAIL",
                    "checks": checks,
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 1

    source_raw, source_text = source_read
    unit_raw, unit_text = unit_read
    check_source(checks, source_raw, source_text)
    ids = check_unit(checks, unit_raw, unit_text)
    check_pandoc(checks, ids)
    check_mastery(checks, unit_text)
    check_repairs(checks, unit_text)
    check_controls(checks)
    status = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    result = {
        "schema_version": "1.0",
        "qa_id": "O012-RBT-L21-QA",
        "status": status,
        "source": {
            "path": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "commit": UPSTREAM_COMMIT,
            "line_start": LINE_START,
            "line_end": LINE_END,
            "bytes": len(source_raw),
            "sha256": digest(source_raw),
            "span_bytes": SPAN_BYTES,
            "span_sha256": SPAN_SHA256,
            "raw_through_next_marker_bytes": RAW_BYTES,
            "raw_through_next_marker_sha256": RAW_SHA256,
        },
        "unit": {
            "path": str(UNIT.relative_to(ROOT)).replace("\\", "/"),
            "bytes": len(unit_raw),
            "lines": len(unit_text.splitlines()),
            "sha256": digest(unit_raw),
            "stable_ids": len(set(ids)),
        },
        "checks": checks,
        "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra",
    }
    if status == "PASS":
        OUTPUT.write_text(
            json.dumps(result, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
