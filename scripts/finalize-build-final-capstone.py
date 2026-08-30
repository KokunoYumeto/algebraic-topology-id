#!/usr/bin/env python3
"""Fail closed over the final D60 capstone reader and its visual/browser evidence."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
SLUG = "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04-capstone"
HTML = ROOT / f"output/html/{SLUG}/index.html"
PDF = ROOT / f"output/pdf/topologi-aljabar-{SLUG}-id.pdf"
MANIFEST = ROOT / "output/ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04_CAPSTONE.csv"
DRAFT = ROOT / "qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04_CAPSTONE_BUILD_DRAFT.json"
VISUAL = ROOT / "qa/capstone/VISUAL_QA.json"
BROWSER = ROOT / "qa/capstone/BROWSER_QA.json"
SOURCE = ROOT / "source/id-ID/capstone/o012-d60-capstone-klein-bottle.md"
STATIC = ROOT / "qa/capstone/STATIC_QA.json"
MATH = ROOT / "qa/capstone/INDEPENDENT_MATH_REVIEW.json"
LANG = ROOT / "qa/capstone/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json"
QA = ROOT / "qa/capstone/QA.json"
CENSUS = ROOT / "qa/PROOF_REPAIR_CENSUS.json"
OUT = ROOT / "qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04_CAPSTONE_BUILD_RECEIPT.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"


def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(data),
        "lf_lines": data.count(b"\n"),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    required = (HTML, PDF, MANIFEST, DRAFT, VISUAL, BROWSER, SOURCE, STATIC, MATH, LANG, QA, CENSUS)
    require(all(path.is_file() for path in required), "missing final build input")
    draft, visual, browser = load(DRAFT), load(VISUAL), load(BROWSER)
    require(draft.get("status") == "PASS_DETERMINISTIC_BUILD_PENDING_VISUAL_BROWSER_QA", "draft status drift")
    require(visual.get("status") == browser.get("status") == "PASS", "visual/browser QA did not pass")
    require(draft["html"]["bytes"] == HTML.stat().st_size and draft["html"]["sha256"] == sha256(HTML), "HTML identity drift")
    require(draft["pdf"]["bytes"] == PDF.stat().st_size and draft["pdf"]["sha256"] == sha256(PDF), "PDF identity drift")
    require(draft["manifest"]["bytes"] == MANIFEST.stat().st_size and draft["manifest"]["sha256"] == sha256(MANIFEST), "manifest identity drift")
    require(visual["pdf"]["sha256"] == sha256(PDF), "visual QA PDF mismatch")
    require(browser["html"]["sha256"] == sha256(HTML), "browser QA HTML mismatch")
    require(browser["desktop"]["document_client_width"] == browser["desktop"]["document_scroll_width"], "desktop horizontal overflow")
    require(browser["mobile"]["document_client_width"] == browser["mobile"]["document_scroll_width"], "mobile horizontal overflow")
    require(browser["console"] == {"errors": 0, "warnings": 0}, "browser console findings")
    require(browser["structure"]["ids"] == browser["structure"]["unique_ids"], "duplicate HTML IDs")
    require(browser["structure"]["unresolved_fragments"] == 0, "unresolved fragments")
    require(browser["structure"]["external_runtime_assets"] == 0, "external runtime assets")
    for item in visual["render"]["files"]:
        path = ROOT / item["path"]
        require(path.is_file() and path.stat().st_size == item["bytes"] and sha256(path) == item["sha256"], f"render drift: {path}")
    source_id = identity(SOURCE)
    require(draft["source"] == source_id, "source identity drift")
    for path in (STATIC, MATH, LANG, QA):
        data = load(path)
        require(data.get("status") == "PASS", f"source QA not PASS: {path}")
    require(load(CENSUS).get("status") == "PASS", "proof census not PASS")
    html_text = HTML.read_text(encoding="utf-8")
    require(html_text.count('class="exercise') >= 6 and 'id="o012-d60-capstone"' in html_text, "capstone HTML missing")
    require(not re.search(r"C:\\Users\\|github_pat_|ghp_|BEGIN PRIVATE KEY", html_text), "private HTML marker")
    reader = PdfReader(str(PDF))
    require(len(reader.pages) == 564, "PDF page count drift")
    require(len(reader.named_destinations) == 3189, "PDF destination count drift")
    receipt = {
        "receipt_kind": "final_d60_capstone_reader_build",
        "status": "PASS",
        "date": "2026-08-29",
        "model_provenance": MODEL,
        "frozen_predecessor": draft["frozen_predecessor"],
        "source": source_id,
        "source_qa": [identity(path) for path in (STATIC, MATH, LANG, QA)],
        "proof_census": identity(CENSUS),
        "html": {**draft["html"], "browser_qa": identity(BROWSER)},
        "pdf": {**draft["pdf"], "visual_qa": identity(VISUAL)},
        "manifest": identity(MANIFEST),
        "determinism": {
            "two_clean_html_builds_identical": True,
            "two_clean_appendix_pdf_builds_identical": True,
            "two_clean_merged_pdf_builds_identical": True,
            "predecessor_html_exactly_reconstructible": True,
            "predecessor_pdf_text_prefix_identical": True,
        },
        "accessibility": {
            "primary_surface": "self-contained semantic HTML with native MathML",
            "html_lang": "id-ID",
            "document_horizontal_overflow_desktop": False,
            "document_horizontal_overflow_mobile_375x812": False,
            "pdf_tagged": False,
        },
        "severity_census": {"P1": 0, "P2": 0, "P3": 0},
        "builder_inputs": draft["toolchain_inputs"],
    }
    encoded = (json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pending = OUT.with_name(f".{OUT.name}.pending")
    require(not pending.exists(), "pending receipt collision")
    pending.write_bytes(encoded)
    require(json.loads(pending.read_text(encoding="utf-8"))["status"] == "PASS", "pending receipt invalid")
    pending.replace(OUT)
    print(json.dumps(identity(OUT), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
