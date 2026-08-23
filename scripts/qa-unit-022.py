#!/usr/bin/env python3
"""Fail-closed, source-bounded QA for Roberts Lecture 22.

The verifier reads only the frozen Roberts authority, the Unit 22 reader, and
the explicitly named Unit 22 controls. It never scans the workspace and writes
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
UNIT = ROOT / "source" / "id-ID" / "units" / "unit-022-lecture-022.md"
SOURCE = ROOT / "authority" / "upstream" / (
    "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
) / "Notes.tex"
TERMS = ROOT / "00_control" / "TERMINOLOGY.csv"
ADVERSE = ROOT / "00_control" / "ADVERSE_LEDGER.csv"
AUDIT = ROOT / "qa" / "UNIT_022_SOURCE_AUDIT.md"
REVIEW = ROOT / "qa" / "UNIT_022_INDEPENDENT_REVIEW.md"
HANDOFF = ROOT / "qa" / "UNIT_022_TRANSLATION_HANDOFF.md"
OUTPUT = ROOT / "qa" / "UNIT_022_QA.json"

UPSTREAM_COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
SOURCE_BYTES = 331_447
SOURCE_LINES = 6_368
SOURCE_SHA256 = "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7"
LINE_START = 4501
LINE_END = 4938
NEXT_LINE = 4939
SPAN_BYTES = 20_585
SPAN_SHA256 = "86275c590cfcdf8519d3ce8d077fc48619bb94c3fdf039ca805ae4b7df995b7f"
RAW_BYTES = 20_668
RAW_SHA256 = "de8b63537d295d5a6d85591be81863ae4416a14323b13b1517153465f0cb9a12"

# This identity is rebound after the independent mathematical review. Any
# later reader mutation must deliberately update all three Unit 22 controls.
UNIT_BYTES = 44_066
UNIT_LINES = 1_349
UNIT_SHA256 = "0857e51568d77c811d5d79255ac75bfddc87a04b27356ae457d4e66eeffb7d0d"


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
        "xypic": r"\\xymatrix(?:nocompile)?",
        "label": r"\\label\{",
        "ref": r"\\ref\{",
        "display": r"\\\[",
        "align_star": r"\\begin\{align\*\}",
        "align": r"\\begin\{align\}",
        "cases": r"\\begin\{cases\}",
        "enumerate": r"\\begin\{enumerate\}",
        "center": r"\\begin\{center\}",
    }
    return {
        name: len(re.findall(pattern, active))
        for name, pattern in patterns.items()
    }


def expected_ids() -> set[str]:
    return {
        "o012-rbt-l22-notice",
        "o012-rbt-l22",
        "o012-rbt-l22-mastery",
        *{f"o012-rbt-l22-s{i:02d}" for i in range(1, 6)},
        *{f"o012-rbt-l22-def-{i:03d}" for i in range(1, 7)},
        *{f"o012-rbt-l22-exa-{i:03d}" for i in range(1, 12)},
        *{f"o012-rbt-l22-lem-{i:03d}" for i in range(1, 6)},
        *{f"o012-rbt-l22-proof-{i:03d}" for i in range(1, 4)},
        *{f"o012-rbt-l22-rem-{i:03d}" for i in range(1, 4)},
        *{f"o012-rbt-l22-margin-{i:03d}" for i in range(1, 6)},
        *{f"o012-rbt-l22-fig-{i:03d}" for i in range(1, 6)},
        *{f"o012-rbt-l22-audit-{i:03d}" for i in range(1, 11)},
        *{f"o012-rbt-l22-mcheck-{i:03d}" for i in range(1, 7)},
        *{f"o012-rbt-l22-hint-{i:03d}" for i in range(1, 7)},
        *{f"o012-rbt-l22-sol-{i:03d}" for i in range(1, 7)},
        "o012-rbt-l22-boundary-001",
    }


def block_counts(text: str) -> dict[str, int]:
    kinds = (
        "definition", "example", "lemma", "proof", "remark", "source-margin",
        "figure", "source-audit", "exercise", "hint", "solution", "boundary",
    )
    found = re.findall(
        r"^:::\s*\{\.((?:" + "|".join(kinds) + r"))\s+#o012-rbt-l22\b",
        text,
        flags=re.MULTILINE,
    )
    return dict(sorted(Counter(found).items()))


def block_payloads(text: str, kind: str) -> dict[str, str]:
    pattern = re.compile(
        rf"^:::\s*\{{\.{re.escape(kind)}\s+#(o012-rbt-l22-[^\s}}]+)[^}}]*\}}\s*\n"
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
        len(span_lines) == 438
        and len(span.encode()) == SPAN_BYTES
        and digest(span.encode()) == SPAN_SHA256
        and len(raw_witness.encode()) == RAW_BYTES
        and digest(raw_witness.encode()) == RAW_SHA256
        and r"\lecturenum{22}" in span_lines[0]
        and r"\lecturenum{23}" in lines[NEXT_LINE - 1]
        and not any(
            span.count(rf"\begin{{{env}}}") != span.count(rf"\end{{{env}}}")
            for env in ("definition", "example", "lemma", "proof", "rem")
        )
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
        "example": 11,
        "exercise": 0,
        "definition": 6,
        "lemma": 5,
        "proof": 3,
        "remark": 3,
        "construction": 0,
        "margin": 5,
        "tikz": 2,
        "xypic": 3,
        "label": 2,
        "ref": 1,
        "display": 8,
        "align_star": 4,
        "align": 0,
        "cases": 1,
        "enumerate": 0,
        "center": 1,
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

    odd_dollar_lines = []
    for index, line in enumerate(lines, start=1):
        dollars = len(re.findall(r"(?<!\\)\$", line))
        if dollars % 2:
            odd_dollar_lines.append(index)
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
    math_ok = not odd_dollar_lines and not bare_square and not malformed_math
    add(
        checks,
        "math_portability",
        "PASS" if math_ok else "FAIL",
        "all dollar delimiters are line-local; no bare proof closure, malformed qquad, or literal Unicode Greek in math"
        if math_ok
        else f"odd={odd_dollar_lines}; bare_square={bare_square}; malformed={malformed_math}",
    )

    required = (
        "Unit 22:",
        UPSTREAM_COMMIT,
        "Notes.tex baris 4501--4938",
        "baris 4939",
        "CC BY 4.0",
        "David Michael Roberts",
        "OpenAI Codex gpt-5.6-sol, Ultra",
        "tidak disponsori",
        "himpunan-$\\Delta$",
        "kompleks korantai simpleksial",
        "fungtor kontravarian",
        "perubahan koefisien",
        "bilangan Betti",
        "koefisien torsi",
        "homeomorfisma",
    )
    missing = [needle for needle in required if needle not in text]
    add(
        checks,
        "provenance_and_terminology",
        "PASS" if not missing else "FAIL",
        "source range, author, rights, non-endorsement, model, and admitted terms present"
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

    ids = re.findall(r"#(o012-rbt-l22(?:-[a-z0-9-]+)?)(?=[}\s])", text)
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
        "definition": 6,
        "example": 11,
        "exercise": 6,
        "figure": 5,
        "hint": 6,
        "lemma": 5,
        "proof": 3,
        "remark": 3,
        "solution": 6,
        "source-audit": 10,
        "source-margin": 5,
    }
    add(
        checks,
        "structural_inventory",
        "PASS" if observed == expected else "FAIL",
        json.dumps(observed, sort_keys=True)
        if observed == expected
        else f"observed={observed}; expected={expected}",
    )

    labels = re.findall(r'data-source-label="([^"]+)"', text)
    label_ok = labels == ["eg:infinite_cylinder", "eg:name_of_simplex"]
    add(
        checks,
        "source_labels_and_reference",
        "PASS" if label_ok and "Contoh 22.4" in text else "FAIL",
        "both source labels and the active cylinder reference are preserved"
        if label_ok and "Contoh 22.4" in text
        else f"labels={labels}",
    )

    figures = re.findall(
        r'^:::\s*\{\.figure\s+#(o012-rbt-l22-fig-\d{3})\s+data-source-format="([^"]+)"',
        text,
        re.MULTILINE,
    )
    access_ok = (
        len(figures) == 5
        and {item for item, _ in figures}
        == {f"o012-rbt-l22-fig-{i:03d}" for i in range(1, 6)}
        and Counter(fmt for _, fmt in figures)
        == Counter({"tikz": 2, "xypic": 3})
        and text.count("**Diagram 22.") == 5
        and text.count("{.source-margin #o012-rbt-l22-margin-") == 5
        and not re.search(
            r"\\xymatrix|\\begin\{tikzpicture\}|\\marginnote|\\begin\{center\}",
            text,
        )
        and "data insidensi" in text
        and "komutatif" in text
    )
    add(
        checks,
        "accessibility_reflow",
        "PASS" if access_ok else "FAIL",
        "two TikZ and three Xy-pic relationships are semantic figures; five margins are in reading order"
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
            if key.startswith(f"o012-rbt-l22-{prefix}-")
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
                rf'^:::\s*\{{\.{kind}\s+#o012-rbt-l22-{prefix}-\d{{3}}\s+data-origin="edition-original"\}}',
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
        "setelah memilih $x\\in X_2$",
        "f_{2i}&e_{2i}&e_{1,i+1}&e_{3i}",
        "|\\operatorname{id}|=\\operatorname{id}",
        "berdimensi tak hingga bila",
        "d_{i,Y}^n\\circ f_n",
        "\\lambda_S\\colon\\Delta^k\\longrightarrow\\Delta^n",
        "\\sum_{i=0}^{n+1}(-1)^i g\\circ d_i^{n+1}",
        "0\\leq i<j\\leq n+2",
        "\\delta_{n,X}f_n^*g",
        "Jika $R$ Noetherian",
        "produk salinan $R$",
        "kompleks **korantai simpleksial**",
        "Jika $X_\\bullet$ berhingga",
        "fakta geometrik standar",
        "$\\mathbb R$ datar",
    )
    missing = [needle for needle in required if needle not in text]
    reader_text = re.sub(
        r"^:::\s*\{\.source-audit[^\n]*\}\s*\n.*?^:::\s*$",
        "",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    forbidden = (
        "singe edge",
        "cyclicly",
        "defintion",
        "defintitions",
        "relisation",
        "combinatrial",
        "calulate",
        "kompleks korantai *singular*",
        "isomorfisme",
        "\\sum_{i=0}^n (-1)^i",
    )
    found = [needle for needle in forbidden if needle in reader_text]
    ok = not missing and not found
    add(
        checks,
        "mathematical_and_language_repairs",
        "PASS" if ok else "FAIL",
        "simplex names, typed relations, all-face differential, Noetherian/product semantics, coefficient qualifications, and source corrections present"
        if ok
        else f"missing={missing}; forbidden={found}",
    )


def check_controls(checks: list[dict[str, str]]) -> None:
    audit = AUDIT.read_text(encoding="utf-8")
    review = REVIEW.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")
    controls_ok = (
        ("4501–4938" in audit or "4501-4938" in audit)
        and SPAN_SHA256 in audit
        and "11 `example` environments" in audit
        and "Final snapshot" in review
        and UNIT_SHA256 in review
        and "P1: 0" in review
        and "P2: 0" in review
        and "P3: 0" in review
        and UNIT_SHA256 in handoff
        and "438 LF-normalized" in handoff
        and not privacy_markers(audit + review + handoff)
    )
    add(
        checks,
        "source_review_handoff_binding",
        "PASS" if controls_ok else "FAIL",
        "audit, review, and handoff bind the final Unit 22 hash"
        if controls_ok
        else "one or more Unit 22 controls are stale or incomplete",
    )

    terms = TERMS.read_text(encoding="utf-8")
    adverse = ADVERSE.read_text(encoding="utf-8")
    term_ok = all(f"O012-TERM-{i:04d}" in terms for i in range(293, 301))
    adverse_ok = all(f"O012-ADV-{i:04d}" in adverse for i in range(298, 312))
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
        "TERM tail=300; ADV tail=311; Unit 22 controls present"
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
            "qa_id": "O012-RBT-L22-QA",
            "status": "FAIL",
            "checks": checks,
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1
    add(checks, "required_files", "PASS", "all bounded Unit 22 inputs exist")

    source_read = read_utf8(SOURCE)
    unit_read = read_utf8(UNIT)
    if source_read is None or unit_read is None:
        add(checks, "encoding", "FAIL", "source or unit is not readable UTF-8")
        print(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "qa_id": "O012-RBT-L22-QA",
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
        "qa_id": "O012-RBT-L22-QA",
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
