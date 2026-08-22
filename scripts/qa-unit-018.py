#!/usr/bin/env python3
"""Bounded structural/source QA for O012 Roberts Lecture 18."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "source" / "id-ID" / "units" / "unit-018-lecture-018.md"
SOURCE = (
    ROOT
    / "authority"
    / "upstream"
    / "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
    / "Notes.tex"
)
TERMS = ROOT / "00_control" / "TERMINOLOGY.csv"
ADVERSE = ROOT / "00_control" / "ADVERSE_LEDGER.csv"
AUDIT = ROOT / "qa" / "UNIT_018_SOURCE_AUDIT.md"
REVIEW = ROOT / "qa" / "UNIT_018_INDEPENDENT_REVIEW.md"
OUTPUT = ROOT / "qa" / "UNIT_018_QA.json"

SOURCE_SHA256 = "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fail(checks: list[dict], name: str, detail: str) -> None:
    checks.append({"check": name, "status": "FAIL", "detail": detail})


def passed(checks: list[dict], name: str, detail: str) -> None:
    checks.append({"check": name, "status": "PASS", "detail": detail})


def main() -> int:
    checks: list[dict] = []
    required = [UNIT, SOURCE, TERMS, ADVERSE, AUDIT, REVIEW]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        fail(checks, "required_files", "missing: " + ", ".join(missing))
        payload = {"status": "FAIL", "checks": checks}
        OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(payload, indent=2))
        return 1
    passed(checks, "required_files", "all six bounded inputs exist")

    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_lines = source_text.splitlines()
    digest = sha256(source_bytes)
    if digest == SOURCE_SHA256 and len(source_lines) == 6368:
        passed(checks, "source_identity", f"6368 lines; SHA-256 {digest}")
    else:
        fail(
            checks,
            "source_identity",
            f"{len(source_lines)} lines; SHA-256 {digest}; expected 6368/{SOURCE_SHA256}",
        )

    span = source_lines[3481:3677]
    boundary_ok = (
        len(span) == 196
        and r"The\lecturenum{18} assignment" in span[0]
        and span[-1] == ""
        and r"\lecturenum{19}" in source_lines[3677]
    )
    if boundary_ok:
        passed(checks, "source_boundary", "Notes.tex:3482-3677; Lecture 19 at 3678")
    else:
        fail(checks, "source_boundary", "exact line markers or 196-line span changed")

    unit_bytes = UNIT.read_bytes()
    try:
        unit_text = unit_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(checks, "encoding", str(exc))
        unit_text = unit_bytes.decode("utf-8", errors="replace")
    else:
        if b"\r" in unit_bytes or not unit_bytes.endswith(b"\n"):
            fail(checks, "encoding", "expected UTF-8 LF with final newline and no CR bytes")
        else:
            passed(checks, "encoding", "UTF-8; LF only; final newline present")

    header_needles = [
        'title: "Topologi Aljabar"',
        "Unit 18:",
        "lang: id-ID",
        "CC BY 4.0",
        "OpenAI Codex gpt-5.6-sol, Ultra",
        "Notes.tex baris 3482--3677",
        "baris 3678",
    ]
    absent = [needle for needle in header_needles if needle not in unit_text]
    if absent:
        fail(checks, "provenance_header", "missing: " + "; ".join(absent))
    else:
        passed(checks, "provenance_header", "source span, rights, model, and boundary disclosed")

    ids = re.findall(
        r"\{[^}\n]*#(o012-rbt-l18(?:-[a-z0-9-]+)?)[^}\n]*\}",
        unit_text,
    )
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    required_ids = {
        "o012-rbt-l18-notice",
        "o012-rbt-l18",
        "o012-rbt-l18-mastery",
        "o012-rbt-l18-thm-001",
        *{f"o012-rbt-l18-s{i:02d}" for i in range(1, 9)},
        *{f"o012-rbt-l18-ex-{i:03d}" for i in range(1, 11)},
        *{f"o012-rbt-l18-rem-{i:03d}" for i in range(1, 7)},
        *{f"o012-rbt-l18-prop-{i:03d}" for i in range(1, 3)},
        *{f"o012-rbt-l18-lem-{i:03d}" for i in range(1, 3)},
        *{f"o012-rbt-l18-def-{i:03d}" for i in range(1, 3)},
        *{f"o012-rbt-l18-mcheck-{i:03d}" for i in range(1, 7)},
        *{f"o012-rbt-l18-hint-{i:03d}" for i in range(1, 7)},
        *{f"o012-rbt-l18-sol-{i:03d}" for i in range(1, 7)},
    }
    missing_ids = sorted(required_ids - set(ids))
    if duplicates or missing_ids:
        fail(
            checks,
            "stable_ids",
            f"duplicates={duplicates}; missing={missing_ids}; observed={len(ids)}",
        )
    else:
        passed(checks, "stable_ids", f"{len(ids)} unique IDs; required inventory present")

    pandoc = shutil.which("pandoc")
    if pandoc is None:
        fail(checks, "pandoc_structural_ids", "pandoc is unavailable")
    else:
        parsed = subprocess.run(
            [pandoc, str(UNIT), "--to=html5"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        structural_missing = sorted(
            item for item in set(ids) if f'id="{item}"' not in parsed.stdout
        )
        literal_margin_ids = re.findall(
            r"^\{#(o012-rbt-l18-margin-\d{3})\}\s*$",
            unit_text,
            flags=re.MULTILINE,
        )
        if parsed.returncode or structural_missing or literal_margin_ids:
            fail(
                checks,
                "pandoc_structural_ids",
                "returncode={} missing={} literal_margin_ids={} stderr={}".format(
                    parsed.returncode,
                    structural_missing,
                    literal_margin_ids,
                    parsed.stderr.strip(),
                ),
            )
        else:
            passed(
                checks,
                "pandoc_structural_ids",
                f"all {len(set(ids))} textual declarations are structural Pandoc IDs",
            )

    active_span = "\n".join(line for line in span if not line.lstrip().startswith("%"))
    source_objects = {
        "proposition": len(re.findall(r"\\begin\{prop\}", active_span)),
        "lemma": len(re.findall(r"\\begin\{lemma\}", active_span)),
        "theorem": len(re.findall(r"\\begin\{theorem\}", active_span)),
        "definition": len(re.findall(r"\\begin\{definition\}", active_span)),
        "example": len(re.findall(r"\\begin\{example\}", active_span)),
        "remark": len(re.findall(r"\\begin\{rem\}", active_span)),
        "exercise": len(re.findall(r"\\begin\{(?:ex|q)\}", active_span)),
        "margin": len(re.findall(r"\\marginnote", active_span)),
    }
    expected_objects = {
        "proposition": 2,
        "lemma": 2,
        "theorem": 1,
        "definition": 2,
        "example": 10,
        "remark": 6,
        "exercise": 0,
        "margin": 5,
    }
    if source_objects == expected_objects:
        passed(checks, "source_census", json.dumps(source_objects, sort_keys=True))
    else:
        fail(
            checks,
            "source_census",
            f"observed={source_objects}; expected={expected_objects}",
        )

    mastery = {
        "exercise_blocks": len(
            re.findall(
                r':::\s*\{\.exercise #o012-rbt-l18-mcheck-\d{3} data-origin="edition-original"\}',
                unit_text,
            )
        ),
        "hints": len(
            re.findall(
                r':::\s*\{\.hint #o012-rbt-l18-hint-\d{3} data-origin="edition-original"\}',
                unit_text,
            )
        ),
        "solutions": len(
            re.findall(
                r':::\s*\{\.solution #o012-rbt-l18-sol-\d{3} data-origin="edition-original"\}',
                unit_text,
            )
        ),
    }
    if mastery == {"exercise_blocks": 6, "hints": 6, "solutions": 6}:
        passed(checks, "mastery_closure", json.dumps(mastery, sort_keys=True))
    else:
        fail(checks, "mastery_closure", json.dumps(mastery, sort_keys=True))

    reader_text = re.sub(
        r":::\s*\{\.source-audit[^}]*\}.*?\n:::\s*",
        "",
        unit_text,
        flags=re.DOTALL,
    )
    forbidden = {
        r"\\xymatrix": "positional Xy-pic remains",
        r"\\marginnote": "margin-only content remains",
        "funktor": "deprecated Indonesian variant remains",
        "homomorfisme": "deprecated morfisme-family variant remains",
        "isomorfisme": "deprecated morfisme-family variant remains",
        "trivialiasi": "misspelled trivialisasi remains",
        "naturalisasi": "use naturalitas for naturality",
        "homotopi bertitik-ujung": "use explicit endpoint-preserving terminology",
        "modul-$R$": "use modul atas R",
        "lima suku yang relevan": "display contains only four terms",
        r"\pi_1(X,x)\to\pi_n(Y,y)": "source type error remains",
        r"F=\pi^{-1}(F)": "pointed-fibre type error remains",
        r"\pi_1(X,x)/q_*": "unsided source quotient remains",
        "membuat $\\delta$ injektif sebagai": "pointed-set exactness was misused as injectivity",
    }
    hits = {needle: label for needle, label in forbidden.items() if needle in reader_text}
    if hits:
        fail(checks, "forbidden_regressions", json.dumps(hits, ensure_ascii=False))
    else:
        passed(checks, "forbidden_regressions", "no known type, terminology, or layout regression")

    required_math = [
        r"\lVert\mathbf",
        r"\pi_n(X,x)\to\pi_n(Y,y)",
        r"T_h(f_*[\alpha])=g_*[\alpha]",
        r"\operatorname{pr}_1",
        r"\mathbb{CP}^1\cong S^2",
        r"H\backslash G",
        r"i_*^{-1}([p])",
        r"\delta\colon G",
        r"\pi_{25}(S^6)",
        r"H=q_*\pi_1(S^m)=1",
        "pengangkatan homotopi relatif",
        "SLSC menurut konvensi mata kuliah",
        r"T_{\gamma_0}=T_{\gamma_1}",
        "modul atas $R$",
        "*fibre bundle*",
        "garis projektif kompleks",
        "koordinat homogen",
        "bundel Hopf kompleks",
        "bundel Hopf kuaternionik",
    ]
    absent_math = [needle for needle in required_math if needle not in unit_text]
    if absent_math:
        fail(checks, "required_repairs", "missing: " + "; ".join(absent_math))
    else:
        passed(checks, "required_repairs", "typed, handed, and source-gap repairs present")

    quantified_objects = len(re.findall(r"Tetapkan\s+\$n\\geq1\$", unit_text))
    margin_divs = set(
        re.findall(
            r'^::: \{\.source-margin #(o012-rbt-l18-margin-\d{3})\}\s*$',
            unit_text,
            flags=re.MULTILINE,
        )
    )
    expected_margin_divs = {f"o012-rbt-l18-margin-{i:03d}" for i in range(1, 6)}
    if quantified_objects >= 5 and margin_divs == expected_margin_divs:
        passed(
            checks,
            "independent_review_repairs",
            f"n-range declarations={quantified_objects}; five attributed source-margin divs",
        )
    else:
        fail(
            checks,
            "independent_review_repairs",
            f"n-range declarations={quantified_objects}; margin_divs={sorted(margin_divs)}",
        )

    review_text = REVIEW.read_text(encoding="utf-8")
    unit_digest = sha256(unit_bytes)
    review_needles = [
        f"Final snapshot: {len(unit_bytes):,} bytes, {len(unit_text.splitlines()):,} lines, SHA-256",
        f"`{unit_digest}`",
        "- P1: 0",
        "- P2: 0",
        "- P3: 0",
        "all 67 unique textual ID declarations are structural IDs",
    ]
    absent_review = [needle for needle in review_needles if needle not in review_text]
    if absent_review:
        fail(checks, "independent_review_binding", "missing: " + "; ".join(absent_review))
    else:
        passed(
            checks,
            "independent_review_binding",
            f"P1/P2/P3 zero; bound to Unit SHA-256 {unit_digest}",
        )

    term_text = TERMS.read_text(encoding="utf-8")
    adverse_text = ADVERSE.read_text(encoding="utf-8")
    term_ids = re.findall(r"O012-TERM-(\d{4})", term_text)
    adverse_ids = re.findall(r"O012-ADV-(\d{4})", adverse_text)
    terms_ok = (
        term_ids
        and term_ids[-1] == "0274"
        and len(term_ids) == len(set(term_ids))
        and all(int(b) == int(a) + 1 for a, b in zip(term_ids, term_ids[1:]))
    )
    adverse_ok = (
        adverse_ids
        and adverse_ids[-1] == "0257"
        and len(adverse_ids) == len(set(adverse_ids))
        and all(int(b) == int(a) + 1 for a, b in zip(adverse_ids, adverse_ids[1:]))
    )
    if terms_ok and adverse_ok:
        passed(checks, "ledger_contiguity", "terminology through 0274; adverse through 0257")
    else:
        fail(
            checks,
            "ledger_contiguity",
            f"term_tail={term_ids[-1:]}; adverse_tail={adverse_ids[-1:]}",
        )

    status = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    payload = {
        "schema_version": "1.0",
        "qa_id": "O012-RBT-L18-QA",
        "status": status,
        "source": {
            "path": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "commit": "b947ad2e9f9e301bfe24590a9db653bc54fa1a53",
            "line_start": 3482,
            "line_end": 3677,
            "sha256": digest,
        },
        "unit": {
            "path": str(UNIT.relative_to(ROOT)).replace("\\", "/"),
            "bytes": len(unit_bytes),
            "lines": len(unit_text.splitlines()),
            "sha256": sha256(unit_bytes),
            "stable_ids": len(ids),
        },
        "checks": checks,
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
