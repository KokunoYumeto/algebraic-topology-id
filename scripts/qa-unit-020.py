#!/usr/bin/env python3
"""Fail-closed, source-bounded QA for Roberts Lecture 20.

The verifier reads only the frozen Roberts authority, the Unit 20 reader, and
the small set of named lane controls.  It never scans the workspace and only
writes the receipt after every gate passes.
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
UNIT = ROOT / "source" / "id-ID" / "units" / "unit-020-lecture-020.md"
SOURCE = ROOT / "authority" / "upstream" / (
    "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
) / "Notes.tex"
TERMS = ROOT / "00_control" / "TERMINOLOGY.csv"
ADVERSE = ROOT / "00_control" / "ADVERSE_LEDGER.csv"
AUDIT = ROOT / "qa" / "UNIT_020_SOURCE_AUDIT.md"
REVIEW = ROOT / "qa" / "UNIT_020_INDEPENDENT_REVIEW.md"
HANDOFF = ROOT / "qa" / "UNIT_020_TRANSLATION_HANDOFF.md"
OUTPUT = ROOT / "qa" / "UNIT_020_QA.json"

UPSTREAM_COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
SOURCE_BYTES = 331_447
SOURCE_LINES = 6_368
SOURCE_SHA256 = "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7"
LINE_START = 3948
LINE_END = 4345
NEXT_LINE = 4346
SPAN_BYTES = 17_645
SPAN_SHA256 = "1fa7d0ea4ecd567ae8975da5b9b41495a1757913942102f223d1234168366e88"
RAW_BYTES = 17_657
RAW_SHA256 = "6af488776f936d7a3ef17a30a8af94e6955df91e3a3057b92b048e1b38ca1917"

# This identity was captured after the terminology and TeX repairs were
# applied and remained stable across an independent second read.
UNIT_BYTES = 45_780
UNIT_LINES = 1_425
UNIT_SHA256 = "b2592d9dd11d1e805ff2995f96604de35c5454bf2a1e5008163ec5a266d7ea50"


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
    active = "\n".join(line for line in span.splitlines() if not line.lstrip().startswith("%"))
    patterns = {
        "example": r"\\begin\{example\}",
        "exercise": r"\\begin\{ex\}",
        "definition": r"\\begin\{definition\}",
        "lemma": r"\\begin\{lemma\}",
        "proof": r"\\begin\{proof\}",
        "remark": r"\\begin\{rem\}",
        "margin": r"\\marginnote",
        "tikz": r"\\begin\{tikzpicture\}",
        "label": r"\\label\{",
        "display": r"\\\[",
        "align_star": r"\\begin\{align\*\}",
        "align": r"\\begin\{align\}",
        "cases": r"\\begin\{cases\}",
    }
    return {name: len(re.findall(pattern, active)) for name, pattern in patterns.items()}


def expected_ids() -> set[str]:
    return {
        "o012-rbt-l20-notice",
        "o012-rbt-l20",
        "o012-rbt-l20-mastery",
        "o012-rbt-l20-s01", "o012-rbt-l20-s02", "o012-rbt-l20-s04",
        *{f"o012-rbt-l20-def-{i:03d}" for i in range(1, 3)},
        *{f"o012-rbt-l20-exa-{i:03d}" for i in range(1, 9)},
        *{f"o012-rbt-l20-ex-{i:03d}" for i in range(1, 5)},
        *{f"o012-rbt-l20-lem-{i:03d}" for i in range(1, 3)},
        *{f"o012-rbt-l20-rem-{i:03d}" for i in range(1, 5)},
        *{f"o012-rbt-l20-proof-{i:03d}" for i in range(1, 3)},
        *{f"o012-rbt-l20-margin-{i:03d}" for i in range(1, 12)},
        *{f"o012-rbt-l20-audit-{i:03d}" for i in range(1, 9)},
        *{f"o012-rbt-l20-fig-{i:03d}" for i in range(1, 8)},
        *{f"o012-rbt-l20-mcheck-{i:03d}" for i in range(1, 7)},
        *{f"o012-rbt-l20-hint-{i:03d}" for i in range(1, 7)},
        *{f"o012-rbt-l20-sol-{i:03d}" for i in range(1, 7)},
        "o012-rbt-l20-boundary-001",
    }


def block_counts(text: str) -> dict[str, int]:
    kinds = (
        "definition", "example", "lemma", "remark", "proof", "source-margin",
        "source-audit", "figure", "exercise", "hint", "solution", "boundary",
    )
    found = re.findall(
        r"^:::\s*\{\.((?:" + "|".join(kinds) + r"))\s+#o012-rbt-l20\b",
        text,
        flags=re.MULTILINE,
    )
    return dict(sorted(Counter(found).items()))


def block_payloads(text: str, kind: str) -> dict[str, str]:
    pattern = re.compile(
        rf"^:::\s*\{{\.{re.escape(kind)}\s+#(o012-rbt-l20-[^\s}}]+)[^}}]*\}}\s*\n"
        r"(.*?)(?=^:::\s*$)",
        flags=re.MULTILINE | re.DOTALL,
    )
    return {match.group(1): match.group(2) for match in pattern.finditer(text)}


def check_source(checks: list[dict[str, str]], raw: bytes, text: str) -> None:
    lines = text.splitlines()
    if len(raw) == SOURCE_BYTES and len(lines) == SOURCE_LINES and digest(raw) == SOURCE_SHA256:
        add(checks, "source_identity", "PASS", f"Notes.tex {len(raw):,} bytes/{len(lines):,} lines; SHA-256 {digest(raw)}")
    else:
        add(checks, "source_identity", "FAIL", f"observed {len(raw)}/{len(lines)}/{digest(raw)}")

    span_lines = lines[LINE_START - 1 : LINE_END]
    span = "\n".join(span_lines)
    raw_span = "\n".join(lines[LINE_START - 1 : NEXT_LINE])
    boundary_ok = (
        len(span_lines) == 398
        and len(span.encode()) == SPAN_BYTES
        and digest(span.encode()) == SPAN_SHA256
        and len(raw_span.encode()) == RAW_BYTES
        and digest(raw_span.encode()) == RAW_SHA256
        and r"\lecturenum{20}" in span_lines[0]
        and r"\lecturenum{21}" in lines[NEXT_LINE]
    )
    if boundary_ok:
        add(checks, "source_boundary", "PASS", f"Notes.tex:{LINE_START}-{LINE_END}; deferred line {NEXT_LINE}; span SHA-256 {SPAN_SHA256}")
    else:
        add(checks, "source_boundary", "FAIL", f"span={len(span.encode())}/{digest(span.encode())}; raw={len(raw_span.encode())}/{digest(raw_span.encode())}")

    observed = source_census(span)
    expected = {"example": 8, "exercise": 4, "definition": 2, "lemma": 2,
                "proof": 2, "remark": 4, "margin": 11, "tikz": 7, "label": 6,
                "display": 8, "align_star": 2, "align": 1, "cases": 3}
    add(checks, "source_census", "PASS" if observed == expected else "FAIL",
        json.dumps(observed, sort_keys=True) if observed == expected else f"observed={observed}; expected={expected}")


def check_unit(checks: list[dict[str, str]], raw: bytes, text: str) -> list[str]:
    lines = text.splitlines()
    identity = len(raw) == UNIT_BYTES and len(lines) == UNIT_LINES and digest(raw) == UNIT_SHA256 and b"\r" not in raw and raw.endswith(b"\n")
    add(checks, "unit_identity_encoding", "PASS" if identity else "FAIL",
        f"{len(raw):,} bytes/{len(lines):,} LF lines; SHA-256 {digest(raw)}")

    required = (
        "Unit 20:", UPSTREAM_COMMIT, "Notes.tex baris 3948--4346", "baris 4347",
        "CC BY 4.0", "David Michael Roberts", "OpenAI Codex gpt-5.6-sol, Ultra",
        "tidak disponsori", "isomorfisma",
    )
    missing = [needle for needle in required if needle not in text]
    add(checks, "provenance_and_terminology", "PASS" if not missing else "FAIL",
        "source range, author, license, non-endorsement, model, and glossary forms present" if not missing else f"missing={missing}")

    private = privacy_markers(text)
    add(checks, "privacy", "PASS" if not private else "FAIL", "no credential/path markers" if not private else str(private))

    ids = re.findall(r"#(o012-rbt-l20(?:-[a-z0-9-]+)?)(?=[}\s])", text)
    unique = set(ids)
    wanted = expected_ids()
    id_ok = len(ids) == len(unique) == len(wanted) and unique == wanted
    add(checks, "stable_ids", "PASS" if id_ok else "FAIL",
        f"{len(unique)} unique IDs" if id_ok else f"observed={len(ids)} unique={len(unique)} missing={sorted(wanted-unique)} unexpected={sorted(unique-wanted)}")

    observed = block_counts(text)
    expected = {"boundary": 1, "definition": 2, "example": 8, "exercise": 10,
                "figure": 7, "hint": 6, "lemma": 2, "proof": 2, "remark": 4,
                "solution": 6, "source-audit": 8, "source-margin": 11}
    add(checks, "structural_inventory", "PASS" if observed == expected else "FAIL",
        json.dumps(observed, sort_keys=True) if observed == expected else f"observed={observed}; expected={expected}")

    # The four source ex environments yield ten Markdown exercise blocks only
    # because the first source exercise has two enumerated prompts; the six
    # edition-original mastery triples are separately checked below.
    figures = re.findall(r"^:::\s*\{\.figure\s+#(o012-rbt-l20-fig-\d{3})\s+data-source-format=\"([^\"]+)\"", text, re.MULTILINE)
    formats = Counter(fmt for _, fmt in figures)
    access_ok = (
        len(figures) == 7 and {i for i, _ in figures} == {f"o012-rbt-l20-fig-{i:03d}" for i in range(1, 8)}
        and formats == Counter({"tikz": 7})
        and not re.search(r"\\xymatrix|\\begin\{tikzpicture\}|\\marginnote", text)
        and text.count("**Diagram 20.") == 7
        and "tanpa mengandalkan arsiran" in text
    )
    add(checks, "accessibility_reflow", "PASS" if access_ok else "FAIL", "seven centered semantic figures; no raw positional source commands" if access_ok else f"figures={figures}")

    return ids


def check_pandoc(checks: list[dict[str, str]], ids: list[str]) -> None:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        add(checks, "pandoc_structural_ids", "FAIL", "pandoc unavailable")
        return
    result = subprocess.run([pandoc, str(UNIT), "--to=html5", "--mathjax"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    missing = sorted({item for item in ids if f'id="{item}"' not in result.stdout})
    ok = result.returncode == 0 and not result.stderr.strip() and not missing
    add(checks, "pandoc_structural_ids", "PASS" if ok else "FAIL", f"all {len(set(ids))} IDs survive Pandoc; exit 0; no warnings" if ok else f"exit={result.returncode}; missing={missing}; stderr={len(result.stderr.encode())}")


def check_mastery(checks: list[dict[str, str]], text: str) -> None:
    expected = {f"{i:03d}" for i in range(1, 7)}
    payloads = {kind: block_payloads(text, kind) for kind in ("exercise", "hint", "solution")}
    prefixes = {"exercise": "mcheck", "hint": "hint", "solution": "sol"}
    suffixes = {kind: {key.rsplit("-", 1)[-1] for key in values if key.startswith(f"o012-rbt-l20-{prefixes[kind]}-")} for kind, values in payloads.items()}
    # Source exercises are also `.exercise` blocks; mastery closure is the
    # six explicitly edition-original `mcheck` triples only.
    payloads["exercise"] = {key: value for key, value in payloads["exercise"].items() if "-mcheck-" in key}
    origins = {kind: len(re.findall(rf"^:::\s*\{{\.{kind}\s+#o012-rbt-l20-{prefixes[kind]}-\d{{3}}\s+data-origin=\"edition-original\"\}}", text, re.MULTILINE)) for kind in prefixes}
    nonempty = all(len(body.strip()) >= 120 for values in payloads.values() for body in values.values())
    ok = all(len(values) == 6 for values in payloads.values()) and all(value == expected for value in suffixes.values()) and origins == {"exercise": 6, "hint": 6, "solution": 6} and nonempty
    add(checks, "mastery_closure", "PASS" if ok else "FAIL", "six problem/hint/full-solution triples" if ok else f"payloads={list(map(len,payloads.values()))}; suffixes={suffixes}; origins={origins}")


def check_repairs(checks: list[dict[str, str]], text: str) -> None:
    required = (
        "M=D^{\\mathsf T}", "\\mathbb Z(\\underline A+\\underline B+\\underline C)",
        "\\Psi(y)=(y_d+y_a+y_b+y_c,\\;y_e-y_a-y_b)",
        "\\operatorname{coker}\\delta\\cong\\mathbb Z^2",
        "\\operatorname{coker}\\delta_1\\cong\\mathbb Z/2\\mathbb Z",
        "H^2\\cong\\mathbb Z/2\\mathbb Z", "\\qquad",
        "Mike Hopkins", "target dikurangi sumber", "isomorfisma",
    )
    missing = [needle for needle in required if needle not in text]
    reader_text = re.sub(r"^:::\s*\{\.source-audit[^\n]*\}\s*\n.*?^:::\s*$", "", text, flags=re.MULTILINE | re.DOTALL)
    forbidden = ("isomorfisme", "\\nqquad", "0\\ZZ^4", "koset kanan", "simplicty", "explicity", "from from")
    found = [needle for needle in forbidden if needle in reader_text]
    ok = not missing and not found
    add(checks, "mathematical_and_language_repairs", "PASS" if ok else "FAIL", "matrix signs, Klein Smith form, TeX, terminology, and source corrections present" if ok else f"missing={missing}; forbidden={found}")


def check_controls(checks: list[dict[str, str]], text: str) -> None:
    audit = AUDIT.read_text(encoding="utf-8")
    review = REVIEW.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")
    controls_ok = (
        ("3948–4345" in audit or "3948-4345" in audit) and SPAN_SHA256 in audit and "8 `example` environments" in audit
        and "Final snapshot" in review and UNIT_SHA256 in review and "P1: 0" in review and "P2: 0" in review and "P3: 0" in review
        and UNIT_SHA256 in handoff and "398 LF-normalized lines" in handoff
        and not privacy_markers(audit + review + handoff)
    )
    add(checks, "source_review_handoff_binding", "PASS" if controls_ok else "FAIL", "audit, independent review, and handoff bind the final Unit 20 hash" if controls_ok else "one or more controls are stale or incomplete")

    terms = TERMS.read_text(encoding="utf-8")
    adverse = ADVERSE.read_text(encoding="utf-8")
    term_ok = "O012-TERM-0288" in terms and "O012-TERM-0289" in terms
    term_ids = [int(x) for x in re.findall(r"O012-TERM-(\d{4})", terms)]
    adv_ids = [int(x) for x in re.findall(r"O012-ADV-(\d{4})", adverse)]
    contig = term_ids == list(range(1, max(term_ids) + 1)) and adv_ids == list(range(1, max(adv_ids) + 1))
    add(checks, "terminology_and_ledger", "PASS" if term_ok and contig else "FAIL", f"TERM tail={max(term_ids)}; ADV tail={max(adv_ids)}; new controls present" if term_ok and contig else "ledger or glossary controls incomplete")


def main() -> int:
    checks: list[dict[str, str]] = []
    required = (UNIT, SOURCE, TERMS, ADVERSE, AUDIT, REVIEW, HANDOFF)
    missing = [str(path.relative_to(ROOT)).replace("\\", "/") for path in required if not path.is_file()]
    if missing:
        add(checks, "required_files", "FAIL", "missing: " + "; ".join(missing))
        result = {"schema_version": "1.0", "qa_id": "O012-RBT-L20-QA", "status": "FAIL", "checks": checks}
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1
    add(checks, "required_files", "PASS", "all bounded Unit 20 inputs exist")
    source_read = read_utf8(SOURCE)
    unit_read = read_utf8(UNIT)
    if source_read is None or unit_read is None:
        add(checks, "encoding", "FAIL", "source or unit is not readable UTF-8")
        print(json.dumps({"schema_version": "1.0", "qa_id": "O012-RBT-L20-QA", "status": "FAIL", "checks": checks}, indent=2))
        return 1
    source_raw, source_text = source_read
    unit_raw, unit_text = unit_read
    check_source(checks, source_raw, source_text)
    ids = check_unit(checks, unit_raw, unit_text)
    check_pandoc(checks, ids)
    check_mastery(checks, unit_text)
    check_repairs(checks, unit_text)
    check_controls(checks, unit_text)
    status = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    result = {
        "schema_version": "1.0", "qa_id": "O012-RBT-L20-QA", "status": status,
        "source": {"path": str(SOURCE.relative_to(ROOT)).replace("\\", "/"), "commit": UPSTREAM_COMMIT, "line_start": LINE_START, "line_end": LINE_END, "bytes": len(source_raw), "sha256": digest(source_raw), "span_bytes": SPAN_BYTES, "span_sha256": SPAN_SHA256, "raw_pre_marker_bytes": RAW_BYTES, "raw_pre_marker_sha256": RAW_SHA256},
        "unit": {"path": str(UNIT.relative_to(ROOT)).replace("\\", "/"), "bytes": len(unit_raw), "lines": len(unit_text.splitlines()), "sha256": digest(unit_raw), "stable_ids": len(ids)},
        "checks": checks,
        "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra",
    }
    if status == "PASS":
        OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
