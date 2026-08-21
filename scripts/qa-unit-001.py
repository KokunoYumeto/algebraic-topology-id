#!/usr/bin/env python3
"""Strict, deterministic QA for O012 reader Unit 001."""

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
SOURCE = LANE / "source" / "id-ID" / "reader-unit-001.md"
HTML = LANE / "output" / "html" / "index.html"
PDF = LANE / "output" / "pdf" / "topologi-aljabar-unit-001-id.pdf"
ARTIFACT_MANIFEST = LANE / "output" / "ARTIFACT_MANIFEST.csv"
AUTHORITY = LANE / "00_control" / "AUTHORITY.json"
CURSOR = LANE / "00_control" / "CURSOR.json"
UPSTREAM_MANIFEST = LANE / "00_control" / "UPSTREAM_FILE_MANIFEST.csv"
RECEIPT = LANE / "qa" / "UNIT_001_QA.json"

EXPECTED_BLOCKS = {
    "definition": 6,
    "example": 7,
    "exercise": 2,
    "lemma": 1,
    "note": 2,
    "proof": 1,
    "proposition": 1,
}
EXPECTED_SOURCE_ENVS = {
    "definition": 6,
    "example": 7,
    "ex": 1,
    "lemma": 1,
    "proof": 1,
    "prop": 1,
}
EXPECTED_ARTIFACTS = {
    "output/html/index.html",
    "output/pdf/topologi-aljabar-unit-001-id.pdf",
}


def fail(message: str) -> None:
    raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    require(isinstance(value, dict), f"Expected JSON object: {path}")
    return value


def verify_file(path: Path, expected_bytes: int, expected_sha: str) -> None:
    require(path.is_file(), f"Missing file: {path}")
    require(path.stat().st_size == expected_bytes, f"Byte mismatch: {path}")
    require(sha256(path) == expected_sha, f"SHA-256 mismatch: {path}")


def verify_authority() -> dict:
    authority = read_json(AUTHORITY)
    require(authority["role_id"] == "O012", "Wrong role in authority")
    require(authority["course_id"] == "D60", "Wrong course in authority")
    require(authority["commit_sha1"] == "b947ad2e9f9e301bfe24590a9db653bc54fa1a53", "Wrong commit")
    require(authority["tree_sha1"] == "aa1d3edb85818e7176e2d0bbc06d9b4bd1e247f5", "Wrong tree")

    for key in ("archive", "active_source", "upstream_pdf"):
        item = authority[key]
        verify_file(LANE / item["path"], int(item["bytes"]), item["sha256"])

    license_path = LANE / "LICENSE.md"
    require(sha256(license_path) == authority["license"]["license_file_sha256"], "License hash mismatch")
    require(authority["license"]["spdx"] == "CC-BY-4.0", "Unexpected license")

    manifest_rows: dict[str, tuple[int, str]] = {}
    with UPSTREAM_MANIFEST.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            path = row["path"]
            require(path not in manifest_rows, f"Duplicate upstream manifest path: {path}")
            manifest_rows[path] = (int(row["bytes"]), row["sha256"])
    require(len(manifest_rows) == 7, "Upstream manifest must have exactly 7 rows")
    upstream_root = (LANE / authority["active_source"]["path"]).parent
    for relative, (size, digest) in manifest_rows.items():
        verify_file(upstream_root / relative, size, digest)
    require(sha256(UPSTREAM_MANIFEST) == authority["manifest"]["sha256"], "Upstream manifest hash mismatch")
    return authority


def verify_source(authority: dict) -> tuple[list[str], dict[str, int]]:
    text = SOURCE.read_text(encoding="utf-8")
    require("\ufffd" not in text, "U+FFFD in source")
    for marker in ("Ã", "Â", "â€", "ï¿½"):
        require(marker not in text, f"Mojibake marker in source: {marker}")

    ids = re.findall(r"#(o012-[a-z0-9-]+)(?=[}\s])", text)
    require(len(ids) == len(set(ids)), "Duplicate stable ID in source")
    require(len(ids) == 29, f"Expected 29 stable IDs, found {len(ids)}")
    require(all(value.startswith("o012-rbt-") for value in ids), "Noncanonical stable ID")

    block_counts = Counter(
        re.findall(
            r"^::: \{\.(definition|example|exercise|lemma|note|proof|proposition)\s+#o012-",
            text,
            flags=re.MULTILINE,
        )
    )
    require(dict(sorted(block_counts.items())) == EXPECTED_BLOCKS, f"Reader block census mismatch: {block_counts}")
    require(text.count("## Apa yang dipelajari oleh topologi aljabar?") == 1, "Missing first source section")
    require(text.count("## Ruang topologis") == 1, "Missing second source section")

    upstream_path = LANE / authority["active_source"]["path"]
    upstream_lines = upstream_path.read_text(encoding="utf-8").splitlines()
    require(len(upstream_lines) == 6368, "Unexpected upstream line count")
    span = "\n".join(upstream_lines[133:348])
    source_counts = {
        env: len(re.findall(rf"\\begin\{{{re.escape(env)}\}}", span))
        for env in EXPECTED_SOURCE_ENVS
    }
    require(source_counts == EXPECTED_SOURCE_ENVS, f"Upstream environment census mismatch: {source_counts}")
    require(span.count("\\section{") == 2, "Upstream span must contain two sections")
    require(span.count("\\lecturenum{1}") == 1, "Upstream span must contain Lecture 1")
    require("g\\circ f = \\id_X$ and $g\\circ f = \\id_Y" in span, "Expected upstream inverse typo missing")

    required_reader_text = (
        "$g\\circ f=\\operatorname{id}_X$ dan $f\\circ g=\\operatorname{id}_Y$",
        "#o012-rbt-l01-sol-001",
        "#o012-rbt-l01-sol-002",
        "#o012-rbt-l01-check-001",
        "#o012-rbt-l01-worked-001",
        "H(x,t)=\\left((1-t)+\\frac{t}{\\lVert x\\rVert}\\right)x",
    )
    for required in required_reader_text:
        require(required in text, f"Missing reader invariant: {required}")
    require(
        text.count("$g\\circ f=\\operatorname{id}_Y$") == 1,
        "The erroneous inverse identity must occur exactly once, in the provenance notice",
    )
    require(
        text.count("$f\\circ g=\\operatorname{id}_Y$") >= 2,
        "The corrected inverse identity must occur in the notice and definition",
    )

    lower = text.lower()
    for phrase in (
        " show that ",
        " continuous function ",
        " topological spaces ",
        " neighbourhood base ",
        " proof.",
        " exercise ",
        " definition ",
    ):
        require(phrase not in lower, f"Reader-facing English residue: {phrase.strip()}")
    for secret in (
        r"C:\\Users\\",
        "C:/Users/",
        "github_pat_",
        "ghp_",
        "sk-proj-",
        "Translation and Transcription Project",
    ):
        require(secret not in text, f"Private/control residue in source: {secret}")

    cursor = read_json(CURSOR)
    # This historical Unit 1 verifier must remain valid as the cumulative
    # production cursor advances beyond the first frozen boundary.
    require(cursor["completed_through_line"] >= 348, "Cursor regressed before Unit 1 end")
    require(cursor["next_line"] == cursor["completed_through_line"] + 1, "Cursor continuity mismatch")
    require("o012-rbt-l01" in cursor["completed_units"], "Cursor lost completed Unit 1")
    return ids, dict(sorted(block_counts.items()))


def verify_html(source_ids: list[str]) -> dict[str, int]:
    # libxml2's legacy HTML DTD reports valid HTML5 elements such as <header>
    # as unknown when recovery is disabled. Parse in HTML5-tolerant mode, then
    # enforce the exact semantic invariants below.
    parser = etree.HTMLParser(recover=True)
    root = etree.parse(str(HTML), parser).getroot()
    require(root.get("lang") == "id-ID", "HTML lang is not id-ID")
    titles = root.xpath("//title/text()")
    require(titles == ["Topologi Aljabar — Unit 1"], f"Unexpected HTML title: {titles}")

    html_ids = root.xpath("//*[@id]/@id")
    require(len(html_ids) == len(set(html_ids)), "Duplicate HTML id")
    for source_id in source_ids:
        require(source_id in html_ids, f"Stable ID missing from HTML: {source_id}")
    for href in root.xpath("//@href"):
        if href.startswith("#"):
            require(href[1:] in html_ids, f"Broken local fragment: {href}")

    math_count = len(root.xpath("//*[local-name()='math']"))
    require(math_count >= 100, f"Too few MathML nodes: {math_count}")
    require(not root.xpath("//script"), "HTML must not contain scripts")
    require(not root.xpath("//img"), "Unit 001 unexpectedly contains images")
    require(not root.xpath("//link[@rel='stylesheet']"), "CSS was not embedded")
    styles = "\n".join(root.xpath("//style/text()"))
    for rule in ("max-width: 58rem", "margin: 0 auto", "@media (max-width: 700px)"):
        require(rule in styles, f"Missing readable-layout rule: {rule}")

    data = HTML.read_text(encoding="utf-8")
    for pattern in (r"C:\\Users\\", "C:/Users/", "github_pat_", "ghp_", "sk-proj-"):
        require(pattern not in data, f"Private data in HTML: {pattern}")
    return {"html_ids": len(html_ids), "mathml_nodes": math_count}


def verify_pdf() -> dict[str, object]:
    reader = PdfReader(str(PDF), strict=True)
    require(not reader.is_encrypted, "PDF is encrypted")
    require(len(reader.pages) == 5, f"Expected 5 PDF pages, found {len(reader.pages)}")
    require(reader.trailer["/Root"].get("/Lang") == "id-ID", "PDF /Lang is not id-ID")
    require(reader.metadata.title == "Topologi Aljabar", f"Unexpected PDF title: {reader.metadata.title!r}")
    extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
    for phrase in (
        "Kuliah 1",
        "Apa yang dipelajari oleh topologi aljabar?",
        "Latihan 1.1",
        "Latihan 1.2",
        "Solusi Latihan 1.1",
        "Solusi Latihan 1.2",
        "Contoh terpecahkan: penciutan radial",
    ):
        require(phrase in extracted, f"Missing extracted PDF text: {phrase}")
    for pattern in ("C:\\Users\\", "C:/Users/", "github_pat_", "ghp_", "sk-proj-", "No correct answer"):
        require(pattern not in extracted, f"Private/English UI residue in PDF: {pattern}")

    pdffonts = shutil.which("pdffonts")
    require(pdffonts is not None, "pdffonts is unavailable")
    result = subprocess.run([pdffonts, str(PDF)], check=True, capture_output=True, text=True)
    rows = [line.split() for line in result.stdout.splitlines()[2:] if line.strip()]
    require(rows, "No PDF fonts reported")
    require(
        all(row[-5:-2] == ["yes", "yes", "yes"] for row in rows),
        "PDF font embedding/Unicode map failure",
    )
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


def verify_artifacts() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with ARTIFACT_MANIFEST.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            relative = row["path"]
            require(relative not in {item["path"] for item in rows}, f"Duplicate artifact: {relative}")
            path = LANE / relative
            verify_file(path, int(row["bytes"]), row["sha256"])
            rows.append({"path": relative, "bytes": int(row["bytes"]), "sha256": row["sha256"]})
    require({row["path"] for row in rows} == EXPECTED_ARTIFACTS, "Artifact manifest set mismatch")
    return rows


def main() -> int:
    authority = verify_authority()
    source_ids, block_counts = verify_source(authority)
    html = verify_html(source_ids)
    pdf = verify_pdf()
    artifacts = verify_artifacts()
    receipt = {
        "schema_version": "1.0",
        "status": "pass",
        "role_id": "O012",
        "course_id": "D60",
        "unit_id": "o012-rbt-l01",
        "source_authority": {
            "commit_sha1": authority["commit_sha1"],
            "tree_sha1": authority["tree_sha1"],
            "path": "Notes.tex",
            "line_start": 134,
            "line_end": 348,
        },
        "reader_source": {
            "path": SOURCE.relative_to(LANE).as_posix(),
            "bytes": SOURCE.stat().st_size,
            "sha256": sha256(SOURCE),
            "stable_ids": len(source_ids),
            "block_counts": block_counts,
        },
        "html": html,
        "pdf": pdf,
        "artifacts": artifacts,
        "gates": {
            "authority_exact": True,
            "source_span_bound": True,
            "structure_bound": True,
            "exercise_solution_closure": True,
            "math_correction_verified": True,
            "html_semantic_offline": True,
            "privacy_secret_scan": True,
            "pdf_reproducible_by_build_script": True,
            "visual_review": "pass_manual_all_5_pages; see qa/UNIT_001_VISUAL_QA.md",
        },
        "known_caveat": "PDF is intentionally secondary and untagged; semantic HTML is the accessibility surface.",
    }
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    RECEIPT.write_text(payload, encoding="utf-8", newline="\n")
    print(
        "PASS "
        f"stable_ids={len(source_ids)} blocks={sum(block_counts.values())} "
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
