#!/usr/bin/env python3
"""Fail-closed bounded QA for the O012 Roberts Lecture 19 reader unit.

This verifier is deliberately local and source-bounded.  It writes the QA
receipt only after every check succeeds; a failed or incomplete unit therefore
cannot replace an earlier receipt with a misleading ``PASS`` or partial
record.
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
UNIT = ROOT / "source" / "id-ID" / "units" / "unit-019-lecture-019.md"
SOURCE = (
    ROOT
    / "authority"
    / "upstream"
    / "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
    / "Notes.tex"
)
TERMS = ROOT / "00_control" / "TERMINOLOGY.csv"
ADVERSE = ROOT / "00_control" / "ADVERSE_LEDGER.csv"
AUDIT = ROOT / "qa" / "UNIT_019_SOURCE_AUDIT.md"
REVIEW = ROOT / "qa" / "UNIT_019_INDEPENDENT_REVIEW.md"
OUTPUT = ROOT / "qa" / "UNIT_019_QA.json"

UPSTREAM_COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
SOURCE_BYTES = 331_447
SOURCE_LINES = 6_368
SOURCE_SHA256 = "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7"
SOURCE_LINE_START = 3678
SOURCE_LINE_END = 3947
SOURCE_NEXT_LINE = 3948
SOURCE_SPAN_BYTES = 16_723
SOURCE_SPAN_SHA256 = "15feb1cca535c90df280e232ce23cb44719a4cf863c6ee17f8c29da5c4f462ab"

UNIT_BYTES = 57_277
UNIT_LINES = 1_865
UNIT_SHA256 = "ba34773d63e4dc70fccdf4fa19fbdc8a397062a4bc359978f3261a70ff64f98c"


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_file(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def add(checks: list[dict[str, str]], name: str, status: str, detail: str) -> None:
    checks.append({"check": name, "status": status, "detail": detail})


def passed(checks: list[dict[str, str]], name: str, detail: str) -> None:
    add(checks, name, "PASS", detail)


def failed(checks: list[dict[str, str]], name: str, detail: str) -> None:
    add(checks, name, "FAIL", detail)


def expected_ids() -> set[str]:
    """Return the complete, deliberately frozen Unit 019 ID inventory."""

    return {
        "o012-rbt-l19-notice",
        "o012-rbt-l19",
        "o012-rbt-l19-mastery",
        *{f"o012-rbt-l19-s{i:02d}" for i in range(1, 8)},
        *{f"o012-rbt-l19-def-{i:03d}" for i in range(1, 7)},
        *{f"o012-rbt-l19-ex-{i:03d}" for i in range(1, 13)},
        *{f"o012-rbt-l19-lem-{i:03d}" for i in range(1, 3)},
        "o012-rbt-l19-rem-001",
        "o012-rbt-l19-proof-001",
        *{f"o012-rbt-l19-margin-{i:03d}" for i in range(1, 14)},
        *{f"o012-rbt-l19-audit-{i:03d}" for i in range(1, 10)},
        *{f"o012-rbt-l19-fig-{i:03d}" for i in range(1, 7)},
        *{f"o012-rbt-l19-mcheck-{i:03d}" for i in range(1, 7)},
        *{f"o012-rbt-l19-hint-{i:03d}" for i in range(1, 7)},
        *{f"o012-rbt-l19-sol-{i:03d}" for i in range(1, 7)},
    }


def source_census(source_span: str) -> dict[str, int]:
    active = "\n".join(
        line for line in source_span.splitlines() if not line.lstrip().startswith("%")
    )
    return {
        "definition": len(re.findall(r"\\begin\{definition\}", active)),
        "example": len(re.findall(r"\\begin\{example\}", active)),
        "lemma": len(re.findall(r"\\begin\{lemma\}", active)),
        "remark": len(re.findall(r"\\begin\{rem\}", active)),
        "proof": len(re.findall(r"\\begin\{proof\}", active)),
        "margin": len(re.findall(r"\\marginnote", active)),
        "display": len(re.findall(r"\\\[", active)),
        "align": len(re.findall(r"\\begin\{align\*\}", active)),
        "xymatrix": len(re.findall(r"\\xymatrix", active)),
        "tikz": len(re.findall(r"\\begin\{tikzpicture\}", active)),
        "label": len(re.findall(r"\\label\{", active)),
    }


def markdown_block_counts(text: str) -> dict[str, int]:
    kinds = (
        "definition",
        "example",
        "lemma",
        "remark",
        "proof",
        "source-margin",
        "source-audit",
        "figure",
        "exercise",
        "hint",
        "solution",
    )
    return dict(
        sorted(
            Counter(
                re.findall(
                    r"^:::\s*\{\.((?:" + "|".join(kinds) + r"))\s+#o012-rbt-l19\b",
                    text,
                    flags=re.MULTILINE,
                )
            ).items()
        )
    )


def privacy_markers(text: str) -> list[str]:
    """Find credential/path markers without echoing their values."""

    low = text.lower()
    patterns = {
        "home-path": str(Path.home()).replace("\\", "/").lower(),
        "windows-user-path": r"c:/users/",
        "github-token": r"github_pat_",
        "github-classic-token": r"ghp_",
        "gitlab-token": r"glpat-",
        "openai-token": r"sk-proj-",
        "bearer-token": r"bearer ",
        "access-token": r"access_token",
        "api-token": r"api_token",
        "secret-key": r"secret_key",
    }
    return [name for name, marker in patterns.items() if marker in low]


def read_utf8(path: Path) -> tuple[bytes, str] | None:
    try:
        raw = path.read_bytes()
        return raw, raw.decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def check_source(
    checks: list[dict[str, str]], source_raw: bytes, source_text: str
) -> str:
    lines = source_text.splitlines()
    digest = digest_bytes(source_raw)
    source_ok = (
        len(source_raw) == SOURCE_BYTES
        and len(lines) == SOURCE_LINES
        and digest == SOURCE_SHA256
    )
    if source_ok:
        passed(
            checks,
            "source_identity",
            f"Notes.tex {len(source_raw):,} bytes/{len(lines):,} lines; SHA-256 {digest}",
        )
    else:
        failed(
            checks,
            "source_identity",
            f"observed {len(source_raw):,} bytes/{len(lines):,} lines/{digest}; "
            f"expected {SOURCE_BYTES:,}/{SOURCE_LINES:,}/{SOURCE_SHA256}",
        )

    span_lines = lines[SOURCE_LINE_START - 1 : SOURCE_LINE_END]
    span = "\n".join(span_lines)
    span_digest = digest_bytes(span.encode("utf-8"))
    boundary_ok = (
        len(span_lines) == SOURCE_LINE_END - SOURCE_LINE_START + 1
        and len(span.encode("utf-8")) == SOURCE_SPAN_BYTES
        and span_digest == SOURCE_SPAN_SHA256
        and r"\lecturenum{19}" in span_lines[0]
        and span_lines[-1] == ""
        and r"\lecturenum{20}" in lines[SOURCE_NEXT_LINE - 1]
    )
    if boundary_ok:
        passed(
            checks,
            "source_boundary",
            f"Notes.tex:{SOURCE_LINE_START}-{SOURCE_LINE_END}; "
            f"next Lecture 20 at {SOURCE_NEXT_LINE}; span SHA-256 {span_digest}",
        )
    else:
        failed(
            checks,
            "source_boundary",
            f"span lines={len(span_lines)} bytes={len(span.encode('utf-8'))} "
            f"SHA-256={span_digest}; expected {SOURCE_SPAN_BYTES}/{SOURCE_SPAN_SHA256}",
        )

    observed = source_census(span)
    expected = {
        "definition": 6,
        "example": 12,
        "lemma": 2,
        "remark": 1,
        "proof": 1,
        "margin": 13,
        "display": 15,
        "align": 1,
        "xymatrix": 4,
        "tikz": 2,
        "label": 2,
    }
    if observed == expected:
        passed(checks, "source_census", json.dumps(observed, sort_keys=True))
    else:
        failed(
            checks,
            "source_census",
            f"observed={json.dumps(observed, sort_keys=True)}; "
            f"expected={json.dumps(expected, sort_keys=True)}",
        )
    return span


def check_unit(
    checks: list[dict[str, str]], unit_raw: bytes, unit_text: str
) -> list[str]:
    digest = digest_bytes(unit_raw)
    lines = unit_text.splitlines()
    encoding_ok = b"\r" not in unit_raw and unit_raw.endswith(b"\n")
    identity_ok = (
        len(unit_raw) == UNIT_BYTES
        and len(lines) == UNIT_LINES
        and digest == UNIT_SHA256
        and encoding_ok
    )
    if identity_ok:
        passed(
            checks,
            "unit_identity_encoding",
            f"{len(unit_raw):,} bytes/{len(lines):,} lines; UTF-8 LF; SHA-256 {digest}",
        )
    else:
        failed(
            checks,
            "unit_identity_encoding",
            f"observed {len(unit_raw):,} bytes/{len(lines):,} lines/{digest}; "
            f"UTF-8-LF={encoding_ok}; expected {UNIT_BYTES:,}/{UNIT_LINES:,}/{UNIT_SHA256}",
        )

    required_header = (
        'title: "Topologi Aljabar"',
        "Unit 19:",
        "lang: id-ID",
        "CC BY 4.0",
        "David Michael Roberts",
        UPSTREAM_COMMIT,
        "Notes.tex baris 3678--3947",
        "baris 3948",
        "OpenAI Codex gpt-5.6-sol, Ultra",
    )
    missing = [needle for needle in required_header if needle not in unit_text]
    if not re.search(r"Creative Commons Attribution\s+4\.0", unit_text):
        missing.append("Creative Commons Attribution 4.0")
    no_endorsement = bool(
        re.search(r"tidak\s+(?:disponsori|didukung|disahkan)|status resmi", unit_text, re.I)
    )
    if not missing and no_endorsement:
        passed(
            checks,
            "provenance_header",
            "source range, commit, author, CC BY 4.0, non-endorsement, and model disclosed",
        )
    else:
        if not no_endorsement:
            missing.append("non-endorsement statement")
        failed(checks, "provenance_header", "missing: " + "; ".join(missing))

    markers = privacy_markers(unit_text)
    if markers:
        failed(checks, "privacy", "private path or credential marker(s): " + ", ".join(markers))
    else:
        passed(checks, "privacy", "no local-user path, personal credential, or token marker")

    ids = re.findall(r"#(o012-rbt-l19(?:-[a-z0-9-]+)?)(?=[}\s])", unit_text)
    unique_ids = set(ids)
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    wanted = expected_ids()
    if len(ids) == 78 and len(unique_ids) == 78 and not duplicates and unique_ids == wanted:
        passed(checks, "stable_ids", "78 unique IDs; complete frozen Unit 019 inventory")
    else:
        failed(
            checks,
            "stable_ids",
            f"observed={len(ids)} unique={len(unique_ids)} duplicates={duplicates}; "
            f"missing={sorted(wanted - unique_ids)}; unexpected={sorted(unique_ids - wanted)}",
        )

    blocks = markdown_block_counts(unit_text)
    expected_blocks = {
        "definition": 6,
        "example": 12,
        "exercise": 6,
        "figure": 6,
        "hint": 6,
        "lemma": 2,
        "proof": 1,
        "remark": 1,
        "solution": 6,
        "source-audit": 9,
        "source-margin": 13,
    }
    if blocks == expected_blocks:
        passed(checks, "structural_inventory", json.dumps(blocks, sort_keys=True))
    else:
        failed(
            checks,
            "structural_inventory",
            f"observed={json.dumps(blocks, sort_keys=True)}; "
            f"expected={json.dumps(expected_blocks, sort_keys=True)}",
        )

    labels = re.findall(r'data-source-label="([^"]+)"', unit_text)
    formats = re.findall(r'data-source-format="([^"]+)"', unit_text)
    format_counts = Counter(formats)
    figures = re.findall(
        r"^:::\s*\{\.figure\s+#(o012-rbt-l19-fig-\d{3})\s+data-source-format=\"([^\"]+)\"\}",
        unit_text,
        flags=re.MULTILINE,
    )
    figure_ids = {item[0] for item in figures}
    figure_access_ok = (
        len(labels) == 2
        and len(set(labels)) == 2
        and len(figures) == 6
        and figure_ids == {f"o012-rbt-l19-fig-{i:03d}" for i in range(1, 7)}
        and format_counts == Counter({"xymatrix": 4, "tikz": 2})
        and not re.search(r"\\xymatrix|\\begin\{tikzpicture\}|\\draw(?:\s|\[)", unit_text)
        and unit_text.count("**Diagram 19.") == 6
        and "setiap objek, arah, serta label panah" in unit_text
        and "tanpa memakai warna atau posisi sebagai kode" in unit_text
    )
    if figure_access_ok:
        passed(
            checks,
            "accessibility_reflow",
            "six centered semantic figures (4 Xy-pic/2 TikZ), two source labels, no positional commands",
        )
    else:
        failed(
            checks,
            "accessibility_reflow",
            f"labels={len(labels)} formats={dict(format_counts)} figures={len(figures)} "
            "or semantic/no-raw-command requirements failed",
        )
    return ids


def check_pandoc(checks: list[dict[str, str]], unit: Path, ids: list[str]) -> None:
    pandoc = shutil.which("pandoc")
    if pandoc is None:
        failed(checks, "pandoc_structural_ids", "pandoc is unavailable")
        return
    result = subprocess.run(
        [pandoc, str(unit), "--to=html5", "--mathjax"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    missing = sorted({item for item in ids if f'id="{item}"' not in result.stdout})
    if result.returncode == 0 and not result.stderr.strip() and not missing:
        passed(
            checks,
            "pandoc_structural_ids",
            f"all {len(set(ids))} IDs survive Pandoc; exit 0; no warnings",
        )
    else:
        failed(
            checks,
            "pandoc_structural_ids",
            f"exit={result.returncode}; missing={missing}; stderr_bytes={len(result.stderr.encode('utf-8'))}",
        )


def block_payloads(text: str, kind: str) -> dict[str, str]:
    pattern = re.compile(
        rf"^:::\s*\{{\.{re.escape(kind)}\s+#(o012-rbt-l19-[^\s}}]+)[^}}]*\}}\s*\n(.*?)(?=^:::\s*$)",
        flags=re.MULTILINE | re.DOTALL,
    )
    return {match.group(1): match.group(2) for match in pattern.finditer(text)}


def check_mastery(checks: list[dict[str, str]], unit_text: str) -> None:
    expected = {f"{i:03d}" for i in range(1, 7)}
    payloads = {
        kind: block_payloads(unit_text, kind) for kind in ("exercise", "hint", "solution")
    }
    id_prefix = {"exercise": "mcheck", "hint": "hint", "solution": "sol"}
    suffixes = {
        kind: {
            key.rsplit("-", 1)[-1]
            for key in value
            if key.startswith(f"o012-rbt-l19-{id_prefix[kind]}-")
        }
        for kind, value in payloads.items()
    }
    origin_counts = {
        kind: len(
            re.findall(
                rf"^:::\s*\{{\.{kind}\s+#o012-rbt-l19-{id_prefix[kind]}-\d{{3}}\s+data-origin=\"edition-original\"\}}",
                unit_text,
                flags=re.MULTILINE,
            )
        )
        for kind in ("exercise", "hint", "solution")
    }
    nonempty = all(len(body.strip()) >= 120 for value in payloads.values() for body in value.values())
    triples_ok = (
        all(len(value) == 6 for value in payloads.values())
        and suffixes["exercise"] == expected
        and suffixes["hint"] == expected
        and suffixes["solution"] == expected
        and origin_counts == {"exercise": 6, "hint": 6, "solution": 6}
        and nonempty
    )
    if triples_ok:
        passed(checks, "mastery_closure", "six edition-original exercise/hint/complete-solution triples")
    else:
        failed(
            checks,
            "mastery_closure",
            f"block_counts={{k: len(v) for k, v in payloads.items()}} suffixes={suffixes} "
            f"origins={origin_counts} nonempty={nonempty}",
        )


def check_repairs(checks: list[dict[str, str]], unit_text: str) -> None:
    # Source-audit blocks intentionally quote the original defects.  Evaluate
    # reader-facing correction checks after removing those quoted observations.
    reader_text = re.sub(
        r"^:::\s*\{\.source-audit[^\n]*\}\s*\n.*?^:::\s*$",
        "",
        unit_text,
        flags=re.MULTILINE | re.DOTALL,
    )
    normalized = re.sub(r"\s+", " ", reader_text)
    required = {
        "right_action": ("aksi kanan", "g\\cdot h=gh", "torsor-$H$", "koset kiri"),
        "n_range": ("n\\geq3",),
        "delta_sign": (r"\times(\pm2)", r"\pm2", "pilihan generator"),
        "finite_euler": ("poliedron **berhingga**", "hipotesis", "R^S", "produk"),
        "cohomological_grading": ("kohomologis", "menaikkan derajat"),
        "complex_morphism": ("setiap persegi", "komutatif", "peta nol", "peta hasil bagi"),
        "vector_calculus": (r"U\subset\mathbb R^3", "**terbuka**", "rotor", "divergensi"),
        "de_rham_scope": ("tak teraugmentasi", "eksak pada derajat positif", "diaugmentasi"),
        "slpc_scope": ("SLPC menurut konvensi mata kuliah", "tidak berarti SLSC"),
        "graph_orientation": ("d_1(e)", "d_0(e)", "target dikurangi sumber", "pasangan terurut"),
        "semantic_direction": ("sumber", "target", "arah", "label panah"),
    }
    missing = [
        f"{name}: {', '.join(needle for needle in needles if needle not in unit_text)}"
        for name, needles in required.items()
        if any(needle not in normalized for needle in needles)
    ]
    forbidden = {
        "raw-xymatrix": r"\\xymatrix",
        "raw-tikz": r"\\begin{tikzpicture}",
        "source-coset-mislabel": "koset kanan",
        "source-range-typo": "assuming >= 3",
        "source-vertx-typo": "vertx",
        "source-acomplex-typo": "acomplex",
        "source-there-is-map": "There is map",
        "source-whose-story": "whose story",
    }
    found_forbidden = [name for name, needle in forbidden.items() if needle in reader_text]
    if not missing and not found_forbidden:
        passed(checks, "required_repairs", "handedness, correction, grading, scope, and accessibility wording present")
    else:
        failed(checks, "required_repairs", f"missing={missing}; forbidden={found_forbidden}")


def check_review_and_ledgers(
    checks: list[dict[str, str]], unit_raw: bytes, unit_text: str, review_text: str, terms_text: str, adverse_text: str
) -> None:
    unit_digest = digest_bytes(unit_raw)
    review_needles = (
        f"Final snapshot: {len(unit_raw):,} bytes, {len(unit_text.splitlines()):,} lines, SHA-256",
        f"`{unit_digest}`",
        "- P1: 0",
        "- P2: 0",
        "- P3: 0",
        "all 78 unique textual ID declarations are structural IDs",
        "Unit 19 passes the independent-review gate.",
    )
    absent = [needle for needle in review_needles if needle not in review_text]
    review_private = privacy_markers(review_text)
    if not absent and not review_private:
        passed(checks, "independent_review_binding", f"final review binds SHA-256 {unit_digest}; P1/P2/P3 zero")
    else:
        failed(checks, "independent_review_binding", f"missing={absent}; private_markers={review_private}")

    def ledger_status(text: str, prefix: str, tail: int) -> tuple[bool, list[str]]:
        ids = re.findall(rf"{re.escape(prefix)}-(\d{{4}})", text)
        ok = bool(ids) and len(ids) == len(set(ids)) and ids[-1] == f"{tail:04d}"
        ok = ok and all(int(b) == int(a) + 1 for a, b in zip(ids, ids[1:]))
        return ok, ids

    terms_ok, term_ids = ledger_status(terms_text, "O012-TERM", 287)
    adverse_ok, adverse_ids = ledger_status(adverse_text, "O012-ADV", 278)
    if terms_ok and adverse_ok:
        passed(checks, "ledger_contiguity", "TERMINOLOGY.csv through TERM0287; ADVERSE_LEDGER.csv through ADV0278")
    else:
        failed(
            checks,
            "ledger_contiguity",
            f"term_count={len(term_ids)} term_tail={term_ids[-1:]}; "
            f"adverse_count={len(adverse_ids)} adverse_tail={adverse_ids[-1:]}",
        )


def payload(checks: list[dict[str, str]], source_raw: bytes | None, unit_raw: bytes | None) -> dict:
    return {
        "schema_version": "1.0",
        "qa_id": "O012-RBT-L19-QA",
        "status": "PASS" if checks and all(item["status"] == "PASS" for item in checks) else "FAIL",
        "source": {
            "path": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "commit": UPSTREAM_COMMIT,
            "line_start": SOURCE_LINE_START,
            "line_end": SOURCE_LINE_END,
            "bytes": len(source_raw) if source_raw is not None else None,
            "sha256": digest_bytes(source_raw) if source_raw is not None else None,
        },
        "unit": {
            "path": str(UNIT.relative_to(ROOT)).replace("\\", "/"),
            "bytes": len(unit_raw) if unit_raw is not None else None,
            "lines": len(unit_raw.decode("utf-8").splitlines()) if unit_raw is not None else None,
            "sha256": digest_bytes(unit_raw) if unit_raw is not None else None,
            "stable_ids": 78,
        },
        "checks": checks,
    }


def main() -> int:
    checks: list[dict[str, str]] = []
    required = (UNIT, SOURCE, TERMS, ADVERSE, AUDIT, REVIEW)
    missing = [str(path.relative_to(ROOT)).replace("\\", "/") for path in required if not path.is_file()]
    if missing:
        failed(checks, "required_files", "missing: " + "; ".join(missing))
        result = payload(checks, None, None)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1
    passed(checks, "required_files", "all six bounded inputs exist")

    source_read = read_utf8(SOURCE)
    unit_read = read_utf8(UNIT)
    if source_read is None:
        failed(checks, "source_encoding", "Notes.tex is not readable as UTF-8")
        result = payload(checks, None, None)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1
    if unit_read is None:
        failed(checks, "unit_encoding", "Unit 019 is not readable as UTF-8")
        result = payload(checks, source_read[0], None)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1

    source_raw, source_text = source_read
    unit_raw, unit_text = unit_read
    span = check_source(checks, source_raw, source_text)
    ids = check_unit(checks, unit_raw, unit_text)
    check_pandoc(checks, UNIT, ids)
    check_mastery(checks, unit_text)
    check_repairs(checks, unit_text)

    audit_text = AUDIT.read_text(encoding="utf-8")
    review_text = REVIEW.read_text(encoding="utf-8")
    terms_text = TERMS.read_text(encoding="utf-8")
    adverse_text = ADVERSE.read_text(encoding="utf-8")
    audit_needles = (
        "physical source lines 3678--3947",
        SOURCE_SPAN_SHA256,
        "6 definitions, 12 examples, 2 lemmas, 1 remark",
        "15 `\\[...\\]` display blocks and 1 `align*` block",
        "4 inline `xymatrix` diagrams, 2 inline TikZ diagrams, 13 marginal notes, and 2 source labels",
    )
    absent_audit = [needle for needle in audit_needles if needle not in audit_text]
    if not absent_audit and not privacy_markers(audit_text):
        passed(checks, "source_audit_binding", "source audit records the frozen span and complete census")
    else:
        failed(checks, "source_audit_binding", f"missing={absent_audit}; private_markers={privacy_markers(audit_text)}")
    check_review_and_ledgers(checks, unit_raw, unit_text, review_text, terms_text, adverse_text)

    result = payload(checks, source_raw, unit_raw)
    if result["status"] == "PASS":
        OUTPUT.write_text(
            json.dumps(result, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    # Fail closed: retain any previous receipt rather than writing a failed or
    # incomplete replacement.  The caller gets the complete diagnostic on stdout.
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
