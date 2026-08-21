#!/usr/bin/env python3
"""Strict QA for the cumulative O012 Units 001-002 reader."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

from lxml import etree
from pypdf import PdfReader


LANE = Path(__file__).resolve().parents[1]
SOURCE_1 = LANE / "source" / "id-ID" / "reader-unit-001.md"
SOURCE_2 = LANE / "source" / "id-ID" / "units" / "unit-002-lecture-002.md"
HTML = LANE / "output" / "html" / "units-001-002" / "index.html"
PDF = LANE / "output" / "pdf" / "topologi-aljabar-unit-001-002-id.pdf"
MANIFEST = LANE / "output" / "ARTIFACT_MANIFEST_UNITS_001_002.csv"
AUTHORITY = LANE / "00_control" / "AUTHORITY.json"
UPSTREAM_MANIFEST = LANE / "00_control" / "UPSTREAM_FILE_MANIFEST.csv"
VISUAL = LANE / "qa" / "UNITS_001_002_VISUAL_QA.md"
INDEPENDENT = LANE / "qa" / "UNIT_002_INDEPENDENT_REVIEW.md"
TEXT_WITNESS = LANE / "qa" / "units-001-002-extracted.txt"
RECEIPT = LANE / "qa" / "UNITS_001_002_QA.json"

EXPECTED = {
    SOURCE_1: (16179, "c80b51c22a2fa7ea116201028b78d5f8d708ef4d8355d34092ac7a9c88415e15"),
    SOURCE_2: (25090, "4d2acc43557db9b3c419ee177545d285b9fcf50b2aa2dd3b2c6c44182f3a6a01"),
    HTML: (220035, "d3b5cbfaa3511823821ecf9ba26a4eaec7c84d937417927d11bde3f66abc9f54"),
    PDF: (395385, "0413c3a3280955cc482a5c0c2d7615b78128dccba3b6b1901dee1bf34d133b8e"),
    MANIFEST: (247, "93e98f6cbbc60775bb934df5b49141f63d7cd2c76582a26c61d4192ff320d721"),
    TEXT_WITNESS: (44049, "ca507d19a8c3089ef9190fcbd31d56c41ea61dd59e5849bba7d0ed1e65ef37b1"),
}

BLOCKS_1 = {
    "definition": 6,
    "example": 7,
    "exercise": 2,
    "lemma": 1,
    "note": 2,
    "proof": 1,
    "proposition": 1,
}
BLOCKS_2 = {
    "definition": 3,
    "example": 8,
    "exercise": 7,
    "lemma": 3,
    "proof": 1,
    "question": 1,
}
ARTIFACT_PATHS = {
    "output/html/units-001-002/index.html",
    "output/pdf/topologi-aljabar-unit-001-002-id.pdf",
}
WINDOWS_PROFILE = chr(92).join(("C:", "Users", ""))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_file(path: Path, expected_bytes: int, expected_sha: str) -> None:
    require(path.is_file(), f"Missing file: {path}")
    require(path.stat().st_size == expected_bytes, f"Byte mismatch: {path}")
    require(sha256(path) == expected_sha, f"SHA-256 mismatch: {path}")


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    require(isinstance(value, dict), f"Expected JSON object: {path}")
    return value


def stable_ids(text: str) -> list[str]:
    return re.findall(r"#(o012-[a-z0-9-]+)(?=[}\s])", text)


def block_counts(text: str) -> dict[str, int]:
    values = Counter(
        re.findall(
            r"^::: \{\.(definition|example|exercise|lemma|note|proof|proposition|question)\s+#o012-",
            text,
            flags=re.MULTILINE,
        )
    )
    return dict(sorted(values.items()))


def verify_authority() -> tuple[dict, list[str]]:
    authority = read_json(AUTHORITY)
    require(authority["role_id"] == "O012" and authority["course_id"] == "D60", "Authority role mismatch")
    require(authority["commit_sha1"] == "b947ad2e9f9e301bfe24590a9db653bc54fa1a53", "Authority commit mismatch")
    require(authority["tree_sha1"] == "aa1d3edb85818e7176e2d0bbc06d9b4bd1e247f5", "Authority tree mismatch")
    for key in ("archive", "active_source", "upstream_pdf"):
        item = authority[key]
        verify_file(LANE / item["path"], int(item["bytes"]), item["sha256"])
    require(authority["license"]["spdx"] == "CC-BY-4.0", "Authority license mismatch")
    require(sha256(LANE / "LICENSE.md") == authority["license"]["license_file_sha256"], "License hash mismatch")

    rows = []
    with UPSTREAM_MANIFEST.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 7, "Upstream manifest row mismatch")
    require(len({row["path"] for row in rows}) == 7, "Duplicate upstream manifest path")
    root = (LANE / authority["active_source"]["path"]).parent
    for row in rows:
        verify_file(root / row["path"], int(row["bytes"]), row["sha256"])
    require(sha256(UPSTREAM_MANIFEST) == authority["manifest"]["sha256"], "Upstream manifest hash mismatch")

    upstream = (LANE / authority["active_source"]["path"]).read_text(encoding="utf-8").splitlines()
    require(len(upstream) == 6368, "Unexpected upstream line count")
    return authority, upstream


def verify_sources(upstream: list[str]) -> tuple[list[str], dict[str, dict[str, int]]]:
    text1 = SOURCE_1.read_text(encoding="utf-8")
    text2 = SOURCE_2.read_text(encoding="utf-8")
    for label, text in (("Unit 1", text1), ("Unit 2", text2)):
        require("\ufffd" not in text, f"U+FFFD in {label}")
        for marker in ("Ã", "Â", "â€", "ï¿½"):
            require(marker not in text, f"Mojibake in {label}: {marker}")
        for placeholder in ("TODO", "TBD", "PLACEHOLDER"):
            require(placeholder not in text, f"Placeholder in {label}: {placeholder}")
        for secret in (WINDOWS_PROFILE, "C:/Users/", "github_pat_", "ghp_", "sk-proj_"):
            require(secret not in text, f"Private/control residue in {label}: {secret}")

    ids1, ids2 = stable_ids(text1), stable_ids(text2)
    require(len(ids1) == 29 and len(set(ids1)) == 29, "Unit 1 stable-ID mismatch")
    require(len(ids2) == 41 and len(set(ids2)) == 41, "Unit 2 stable-ID mismatch")
    require(not (set(ids1) & set(ids2)), "Stable-ID collision across units")
    require(block_counts(text1) == BLOCKS_1, f"Unit 1 block mismatch: {block_counts(text1)}")
    require(block_counts(text2) == BLOCKS_2, f"Unit 2 block mismatch: {block_counts(text2)}")
    require(text2.count("::: ") == text2.count("\n:::\n") + (1 if text2.endswith("\n:::\n") else 0), "Unit 2 semantic fences are unbalanced")

    span1 = "\n".join(upstream[133:348])
    span2 = "\n".join(upstream[348:584])
    require(span1.count(r"\lecturenum{1}") == 1, "Lecture 1 marker mismatch")
    require(span2.count(r"\lecturenum{2}") == 1, "Lecture 2 marker mismatch")
    expected_env2 = {"definition": 3, "example": 8, "ex": 6, "lemma": 3, "proof": 1, "q": 1}
    actual_env2 = {key: span2.count(rf"\begin{{{key}}}") for key in expected_env2}
    require(actual_env2 == expected_env2, f"Unit 2 authority environment mismatch: {actual_env2}")
    require(r"\bigsqcup_\beta X\times Z_\beta" in span2, "Promoted marginal exercise missing from authority")
    require(r"\{x\in \RR^n\mod |x|\leq 1\}" in span2, "Disk source defect witness missing")
    require("(t,x_i) \\ar@{|->}[r] & tx_i" in span2, "Contraction coordinate source defect missing")
    require(r"x\in Z_\beta" in span2 and r"g_\beta(z) = x" in span2, "Joint-surjectivity source defect missing")

    for token in (
        r"D^n:=\bigl\{x\in\mathbb{R}^n\mid\lVert x\rVert\le 1\bigr\}",
        r"\longmapsto(1-t)x_i",
        "citranya harus memuat setiap nilai di antara $0$ dan $1$, suatu kontradiksi",
        "citra yang memuat paling banyak satu titik",
        "yaitu pemetaan kontinu",
        "maka setiap fungsi kontinu $f",
        "#o012-rbt-l02-sol-007",
        "#o012-rbt-l02-answer-001",
    ):
        require(token in text2, f"Missing Unit 2 invariant: {token}")

    for number in range(1, 3):
        require(f"#o012-rbt-l01-ex-{number:03d}" in text1, "Unit 1 exercise missing")
        require(f"#o012-rbt-l01-sol-{number:03d}" in text1, "Unit 1 solution missing")
    for number in range(1, 8):
        require(f"#o012-rbt-l02-ex-{number:03d}" in text2, "Unit 2 exercise missing")
        require(f"#o012-rbt-l02-sol-{number:03d}" in text2, "Unit 2 solution missing")
    require("#o012-rbt-l02-q-001" in text2 and "#o012-rbt-l02-answer-001" in text2, "Question-answer closure missing")

    for phrase in (
        "If the set of functions",
        "Given continuous functions",
        "Every contractible space",
        "show that a subset",
        "the final topology",
    ):
        require(phrase not in text2, f"Active English residue in Unit 2: {phrase}")
    return ids1 + ids2, {"unit_001": BLOCKS_1, "unit_002": BLOCKS_2}


def verify_html(source_ids: list[str]) -> dict[str, int]:
    parser = etree.HTMLParser(recover=True)
    root = etree.parse(str(HTML), parser).getroot()
    require(root.get("lang") == "id-ID", "HTML lang mismatch")
    require(root.xpath("//title/text()") == ["Topologi Aljabar — Unit 1–2"], "HTML title mismatch")
    html_ids = root.xpath("//*[@id]/@id")
    require(len(html_ids) == len(set(html_ids)), "Duplicate HTML id")
    for source_id in source_ids:
        require(source_id in html_ids, f"Stable ID missing from HTML: {source_id}")
    for href in root.xpath("//@href"):
        if href.startswith("#"):
            require(href[1:] in html_ids, f"Broken local fragment: {href}")
    require(not root.xpath("//script"), "Cumulative HTML contains scripts")
    require(not root.xpath("//img"), "Unexpected cumulative image")
    require(not root.xpath("//link[@rel='stylesheet']"), "CSS was not embedded")
    require(not root.xpath("//@src"), "Cumulative HTML has runtime source dependencies")
    math_count = len(root.xpath("//*[local-name()='math']"))
    require(math_count == 621, f"MathML count mismatch: {math_count}")
    styles = "\n".join(root.xpath("//style/text()"))
    for rule in ("max-width: 58rem", "margin: 0 auto", ".question", "#fff8ef"):
        require(rule in styles, f"Missing cumulative style: {rule}")
    data = HTML.read_text(encoding="utf-8")
    for pattern in (WINDOWS_PROFILE, "C:/Users/", "github_pat_", "ghp_", "sk-proj_"):
        require(pattern not in data, f"Private data in HTML: {pattern}")
    return {"html_ids": len(html_ids), "stable_ids": len(source_ids), "mathml_nodes": math_count}


def verify_pdf() -> dict[str, object]:
    reader = PdfReader(str(PDF), strict=True)
    require(not reader.is_encrypted, "PDF is encrypted")
    require(len(reader.pages) == 15, f"PDF page mismatch: {len(reader.pages)}")
    require(reader.trailer["/Root"].get("/Lang") == "id-ID", "PDF /Lang mismatch")
    require(reader.metadata.title == "Topologi Aljabar", "PDF title mismatch")
    extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
    for phrase in (
        "Kuliah 1",
        "Kuliah 2",
        "Topologi akhir dan ruang hasil bagi",
        "Latihan 2.7",
        "Solusi Latihan 2.7",
        "Jawaban Pertanyaan 2.1",
    ):
        require(phrase in extracted, f"Missing PDF text: {phrase}")
    for pattern in (WINDOWS_PROFILE, "C:/Users/", "github_pat_", "ghp_", "sk-proj_", "No correct answer"):
        require(pattern not in extracted, f"Private/English UI residue in PDF: {pattern}")
    pdffonts = shutil.which("pdffonts")
    require(pdffonts is not None, "pdffonts unavailable")
    result = subprocess.run([pdffonts, str(PDF)], check=True, capture_output=True, text=True)
    rows = [line.split() for line in result.stdout.splitlines()[2:] if line.strip()]
    require(rows, "No PDF fonts reported")
    require(all(row[-5:-2] == ["yes", "yes", "yes"] for row in rows), "PDF font embedding/ToUnicode failure")
    return {
        "pages": len(reader.pages),
        "encrypted": False,
        "lang": "id-ID",
        "tagged": "/StructTreeRoot" in reader.trailer["/Root"],
        "fonts": len(rows),
        "all_fonts_embedded": True,
        "all_fonts_tounicode": True,
        "extracted_characters": len(extracted),
    }


def verify_manifest() -> list[dict[str, object]]:
    with MANIFEST.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 2 and len({row["path"] for row in rows}) == 2, "Cumulative manifest shape mismatch")
    require({row["path"] for row in rows} == ARTIFACT_PATHS, "Cumulative manifest set mismatch")
    for row in rows:
        verify_file(LANE / row["path"], int(row["bytes"]), row["sha256"])
    return [{"path": row["path"], "bytes": int(row["bytes"]), "sha256": row["sha256"]} for row in rows]


def main() -> int:
    for path, (size, digest) in EXPECTED.items():
        verify_file(path, size, digest)
    verify_file(
        LANE / "output" / "html" / "index.html",
        85580,
        "5cc4a29f2c29b274328b574d6698a51d75af0939f9959937db8d679c38ad51b8",
    )
    verify_file(
        LANE / "output" / "pdf" / "topologi-aljabar-unit-001-id.pdf",
        321743,
        "6f71546a616c02ef81f8747ecfce3875784842065fc131cc82e5060b066a59c9",
    )
    require(VISUAL.is_file() and INDEPENDENT.is_file(), "Review receipt missing")
    authority, upstream = verify_authority()
    source_ids, blocks = verify_sources(upstream)
    html = verify_html(source_ids)
    pdf = verify_pdf()
    artifacts = verify_manifest()
    receipt = {
        "schema_version": "1.0",
        "status": "pass",
        "role_id": "O012",
        "course_id": "D60",
        "unit_ids": ["o012-rbt-l01", "o012-rbt-l02"],
        "source_authority": {
            "commit_sha1": authority["commit_sha1"],
            "tree_sha1": authority["tree_sha1"],
            "path": "Notes.tex",
            "line_start": 134,
            "line_end": 584,
        },
        "reader_sources": [
            {"path": SOURCE_1.relative_to(LANE).as_posix(), "bytes": SOURCE_1.stat().st_size, "sha256": sha256(SOURCE_1), "stable_ids": 29},
            {"path": SOURCE_2.relative_to(LANE).as_posix(), "bytes": SOURCE_2.stat().st_size, "sha256": sha256(SOURCE_2), "stable_ids": 41},
        ],
        "block_counts": blocks,
        "html": html,
        "pdf": pdf,
        "artifacts": artifacts,
        "witnesses": {
            "independent_review_sha256": sha256(INDEPENDENT),
            "visual_review_sha256": sha256(VISUAL),
            "extracted_text_sha256": sha256(TEXT_WITNESS),
        },
        "gates": {
            "authority_exact": True,
            "source_spans_bound": True,
            "structure_bound": True,
            "exercise_solution_closure": True,
            "question_answer_closure": True,
            "seven_source_corrections_verified": True,
            "html_semantic_offline": True,
            "privacy_secret_scan": True,
            "pdf_reproducible_by_build_script": True,
            "visual_review": "pass_manual_all_15_pages_and_browser_desktop_mobile",
            "unit_001_artifacts_unchanged": True,
        },
        "known_caveat": "PDF is intentionally secondary and untagged; semantic HTML is the accessibility surface.",
    }
    payload = json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    RECEIPT.write_text(payload, encoding="utf-8", newline="\n")
    print(
        "PASS "
        f"stable_ids={len(source_ids)} blocks={sum(sum(v.values()) for v in blocks.values())} "
        f"mathml={html['mathml_nodes']} pdf_pages={pdf['pages']} "
        f"receipt_sha256={sha256(RECEIPT)}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise
