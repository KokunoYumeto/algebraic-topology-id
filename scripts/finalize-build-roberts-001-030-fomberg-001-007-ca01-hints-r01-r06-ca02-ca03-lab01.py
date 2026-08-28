#!/usr/bin/env python3
"""Finalize the deterministic Lab 1 reader after visual and browser QA.

This bounded finalizer never rebuilds or changes a reader. It binds the exact
source, execution, append-only backend, deterministic reader, visual, and
browser evidence into one no-overwrite build receipt for the v0.31.3 gate.
"""

from __future__ import annotations

import csv
import json
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from pypdf import PdfReader


LANE = Path(__file__).resolve().parents[1]
TOKEN = "ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01"
SLUG = "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"

DRAFT_REL = f"qa/{TOKEN}_BUILD_DRAFT.json"
TARGET_REL = f"qa/{TOKEN}_BUILD_RECEIPT.json"
VISUAL_REL = f"qa/{TOKEN}_VISUAL_QA.md"
RENDER_REL = f"qa/{TOKEN}_RENDER_INVENTORY.csv"
BROWSER_REL = f"qa/{TOKEN}_BROWSER_QA.json"
HTML_REL = f"output/html/{SLUG}/index.html"
PDF_REL = f"output/pdf/topologi-aljabar-{SLUG}-id.pdf"
MANIFEST_REL = f"output/ARTIFACT_MANIFEST_{TOKEN}.csv"
LAB_QA_REL = "qa/COMPUTATION_LAB_001_QA.json"
BACKEND_REL = "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_001_CUMULATIVE_RECEIPT.json"
PROOF_REL = "qa/PROOF_REPAIR_CENSUS.json"
BUILDER_REL = f"scripts/build-{SLUG}.py"
FINALIZER_REL = f"scripts/finalize-build-{SLUG}.py"

EXPECTED = {
    DRAFT_REL: (40_536, "dadc4c988bc8e14a0738c95b5493bc34de068f476025238c8803c32baafa4bfe"),
    HTML_REL: (15_389_821, "bb0cf484271370878508a6b774e442ee57aaf82b1a3bbca1bed086729360f7ff"),
    PDF_REL: (9_193_942, "722fa7f6c3aa20d1a4c52257d3127fa500bbaf6aad66f64d62177718cd53d128"),
    MANIFEST_REL: (357, "cbb39a0f0a7b4831fa5eaa2e9b3beb6fc5fa15379ec322f2abb8279fa2b7d824"),
    LAB_QA_REL: (4_258, "75dede0eaa0edbb22c75470dc641bdd10f95aac57c05331171ace4ac9e68aa2b"),
    BACKEND_REL: (9_727, "90f445294eea58aca5bcebe6acaff7293251b21e32aa25f3b62705e64cf8ab74"),
    "source/id-ID/labs/computation-lab-001-monodromy-presentations.md": (12_275, "165e2f9ba587714fb32a2f5a6432920a36493ebc6902d580f55df9c8ab4c65c4"),
    "source/id-ID/labs/o012_d60_lab01_monodromy.py": (8_818, "a9c8875aeb2642921a2d152cd0ed316c6c67969a466240ada9836d3c42252628"),
    "source/id-ID/labs/test_o012_d60_lab01_monodromy.py": (3_032, "ae30ca6604b2a96b12c7df125fdcaa6deea00a9e4594f6b161d7d4785d9b949b"),
    "source/id-ID/labs/expected-output-lab01.txt": (478, "ddaa8015f314e53895c311e12be4d2d1dcaa1fa3f20def4ee112f28077a38717"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def path(relative: str) -> Path:
    candidate = (LANE / relative).resolve()
    require(LANE.resolve() in candidate.parents, f"path escaped lane: {relative}")
    return candidate


def digest(file: Path) -> str:
    return sha256(file.read_bytes()).hexdigest()


def identity(relative: str) -> dict[str, Any]:
    file = path(relative)
    require(file.is_file() and file.stat().st_size > 0, f"missing input: {relative}")
    return {"path": relative, "bytes": file.stat().st_size, "sha256": digest(file)}


def exact_identity(relative: str) -> dict[str, Any]:
    actual = identity(relative)
    size, checksum = EXPECTED[relative]
    require((actual["bytes"], actual["sha256"]) == (size, checksum), f"identity drift: {relative}")
    return actual


def load(relative: str) -> dict[str, Any]:
    return json.loads(path(relative).read_text(encoding="utf-8"))


def bind(row: dict[str, Any], expected: dict[str, Any], label: str) -> None:
    for key in ("path", "bytes", "sha256"):
        require(row.get(key) == expected[key], f"{label} {key} mismatch")


class HtmlInventory(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.fragments: list[str] = []
        self.math_nodes = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(str(values["id"]))
        href = values.get("href")
        if href and href.startswith("#") and len(href) > 1:
            self.fragments.append(href[1:])
        if tag.lower() == "math":
            self.math_nodes += 1


def verify_sources_and_backend() -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    sources = [exact_identity(rel) for rel in list(EXPECTED)[6:]]
    lab = load(LAB_QA_REL)
    require(
        lab.get("status") == "PASS"
        and lab.get("laboratory_id") == "D60-LAB01"
        and lab.get("edition_unit_id") == "O012-ORIG-LAB01"
        and lab.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0}
        and lab.get("checks", {}).get("two_test_runs_6_of_6") == "PASS"
        and lab["checks"].get("expected_output_exact") == "PASS"
        and lab["checks"].get("independent_mathematics") == "PASS"
        and lab["checks"].get("independent_source_language") == "PASS",
        "Lab 1 source/execution/review closure mismatch",
    )
    for expected in sources:
        require(any(all(row.get(k) == expected[k] for k in ("path", "bytes", "sha256")) for row in lab["inputs"]), f"Lab QA does not bind {expected['path']}")
    backend = load(BACKEND_REL)
    prefix, delta, final = backend.get("immutable_prefix", {}), backend.get("delta", {}), backend.get("cumulative", {})
    require(
        backend.get("status") == "PASS"
        and prefix.get("preserved_exactly") is True
        and (prefix.get("records"), prefix.get("bytes"), prefix.get("bundle_sha256")) == (7273, 8_840_132, "97edc6371a0bf670ebdaaa4fab8618ec138ae25c4bf54ca9172139934ba0b464")
        and (delta.get("records"), delta.get("bytes")) == (131, 135_568)
        and (final.get("records"), final.get("bytes"), final.get("bundle_sha256")) == (7404, 8_975_700, "4740eb2ff83b4f9df3c0d90c2426ff77e652b23cad0bbe7763c54ebdefa60b4b")
        and final.get("computation_laboratories_complete") == 1
        and backend.get("replay", {}).get("status") == "PASS"
        and backend.get("semantic_checks", {}).get("append_only_ready") == "PASS",
        "Lab 1 append-only backend closure mismatch",
    )
    require(all(row.get("prefix_preserved") is True and row.get("suffix_exact") is True for row in backend.get("files", [])), "backend file-prefix replay mismatch")
    return lab, backend, sources


def verify_reader() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], int]:
    draft = load(DRAFT_REL)
    require(draft.get("status") == "PASS_DETERMINISTIC_BUILD_PENDING_VISUAL_BROWSER_QA" and draft.get("model_provenance") == MODEL, "draft status/provenance mismatch")
    html_id, pdf_id, manifest_id = exact_identity(HTML_REL), exact_identity(PDF_REL), exact_identity(MANIFEST_REL)
    bind(draft.get("html", {}), html_id, "draft HTML")
    bind(draft.get("pdf", {}), pdf_id, "draft PDF")
    bind(draft.get("manifest", {}), manifest_id, "draft manifest")
    require(draft["html"].get("dom_ids") == 2818 and draft["html"].get("fragment_links") == 846 and draft["html"].get("stable_ids_added") == 24 and draft["html"].get("tasks_added") == 6, "draft HTML census mismatch")
    require(draft["pdf"].get("pages") == 511 and draft["pdf"].get("appendix_pages") == 10 and draft["pdf"].get("stable_id_destinations_added") == 24 and draft["pdf"].get("outline_entries_added") == 17, "draft PDF census mismatch")
    require(draft["pdf"].get("all_fonts_embedded_subset_tounicode") is True and draft["pdf"].get("deterministic_merged_builds") == 2, "draft reproducibility/font gate failed")
    html_text = path(HTML_REL).read_text(encoding="utf-8")
    inv = HtmlInventory(); inv.feed(html_text)
    require(len(inv.ids) == len(set(inv.ids)) == 2818 and len(inv.fragments) == 846 and not (set(inv.fragments) - set(inv.ids)), "serialized HTML ID/link gate failed")
    require("<script src=" not in html_text and "<link rel=" not in html_text, "HTML is not self-contained")
    reader = PdfReader(str(path(PDF_REL)))
    require(len(reader.pages) == 511, "live PDF page count mismatch")
    for page_number in range(500, 511):
        page = reader.pages[page_number]
        require(abs(float(page.mediabox.width) - 595.276) < 0.5 and abs(float(page.mediabox.height) - 841.89) < 0.5, f"non-A4 page: {page_number + 1}")
        require((page.extract_text() or "").strip(), f"empty page: {page_number + 1}")
    return draft, html_id, {**pdf_id, "pages": 511}, manifest_id, inv.math_nodes


def verify_visual_browser() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    visual = path(VISUAL_REL).read_text(encoding="utf-8")
    for line in (
        "P1 (missing, unreadable, blank, clipped, or broken content): **0**",
        "P2 (material layout, transition, font, formula, hierarchy, or navigation defect): **0**",
        "P3 (minor visible cosmetic defect): **0**",
        "Overall disposition: **PASS",
    ):
        require(line in visual, f"visual closure missing: {line}")
    with path(RENDER_REL).open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require([int(row["physical_page"]) for row in rows] == list(range(501, 512)), "render page sequence mismatch")
    require(len(rows) == 11 and sum(int(row["bytes"]) for row in rows) == 2_783_469, "render inventory count/bytes mismatch")
    require(all(row["visual_status"] == "PASS" and row["retained_after_qa"] == "false" for row in rows), "render disposition mismatch")
    browser = load(BROWSER_REL)
    bind(browser.get("artifact", {}), exact_identity(HTML_REL), "browser HTML")
    semantic = browser.get("semantic_and_binding_checks", {})
    require(
        browser.get("status") == "PASS"
        and browser.get("desktop", {}).get("page_level_horizontal_overflow") is False
        and browser.get("mobile", {}).get("page_level_horizontal_overflow") is False
        and browser["mobile"].get("code_blocks_requiring_local_scroll") == browser["mobile"].get("code_blocks_with_overflow_x_auto") == 4
        and semantic.get("duplicate_live_dom_ids") == 0
        and semantic.get("unresolved_fragment_links") == 0
        and semantic.get("runtime_external_asset_references") == 0
        and semantic.get("laboratory_tasks") == 6
        and browser.get("navigation_and_keyboard", {}).get("toc_lab01_activation") == "PASS"
        and browser["navigation_and_keyboard"].get("keyboard_focus", {}).get("status") == "PASS"
        and browser.get("console", {}).get("errors") == browser["console"].get("warnings") == 0
        and browser.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0},
        "browser QA closure mismatch",
    )
    return identity(VISUAL_REL), identity(RENDER_REL), identity(BROWSER_REL)


def main() -> None:
    target = path(TARGET_REL)
    require(not target.exists(), f"refusing to overwrite final receipt: {TARGET_REL}")
    lab, backend, sources = verify_sources_and_backend()
    draft, html_id, pdf_id, manifest_id, math_nodes = verify_reader()
    visual_id, render_id, browser_id = verify_visual_browser()
    proof = load(PROOF_REL)
    receipt = {
        "qa_id": "O012-RBT-001-030-FOM-001-007-CA01-HINTS-R01-R06-CA02-CA03-LAB01-COMPOSITE-BUILD",
        "status": "PASS",
        "scope": "Roberts 30/30; Fomberg Sections 1.1-1.13; D60-CA01/02/03; ordinary mastery 84/84; solution-bearing mastery 108/108; computation Lab 1 complete; Labs 2-4, proof-metadata closure, and capstone pending",
        "model_provenance": MODEL,
        "deterministic_build_draft": exact_identity(DRAFT_REL),
        "sources": sources,
        "source_execution_review": {"status": lab["status"], "receipt": exact_identity(LAB_QA_REL), "tasks": 6, "tests": 6, "stable_ids": 24, "severity_census": lab["severity_census"]},
        "html": {**html_id, "title": "Topologi Aljabar — Roberts 30/30, Fomberg 1.1–1.13, Asesmen Kumulatif 1–3, dan Laboratorium Komputasi 1", "lang": "id-ID", "self_contained": True},
        "pdf": {**pdf_id, "page_size": "A4", "tagged": False},
        "manifest": {**manifest_id, "entries": 2},
        "backend_boundary": {"status": "PASS_APPEND_ONLY_REPLAYABLE", "receipt": exact_identity(BACKEND_REL), "immutable_prefix_records": 7273, "records_added": 131, "cumulative_records": 7404, "cumulative_bytes": 8_975_700, "cumulative_bundle_sha256": backend["cumulative"]["bundle_sha256"], "laboratories_complete": 1, "laboratories_required": 4},
        "html_checks": {"status": "PASS", "serialized_dom_ids": 2818, "live_browser_dom_ids": 2819, "fragment_links": 846, "unresolved_fragment_links": 0, "mathml_nodes": math_nodes, "stable_ids_added": 24, "tasks_added": 6, "self_contained": True, "centered_reflow": True},
        "pdf_checks": {"status": "PASS", "pages": 511, "appended_lab_pages": 10, "bounded_pages_checked": 11, "all_bounded_pages_a4_nonempty": True, "fonts": draft["pdf"]["fonts"], "all_fonts_embedded_subset_tounicode": True, "stable_id_destinations_added": 24, "outline_entries_added": 17},
        "reproducibility": {"frozen_inputs_fail_closed": True, "html_clean_writes": 2, "pdf_appendix_clean_builds": 2, "merged_pdf_clean_builds": 2, "merged_pdf_builds_byte_identical": True, "predecessor_html_exact_reconstruction": True, "predecessor_pdf_extracted_text_prefix_identical": True, "predecessor_pdf_pages_structurally_preserved": 501, "source_date_epoch": draft["source_date_epoch"]},
        "toolchain": {"builder": identity(BUILDER_REL), "finalizer": identity(FINALIZER_REL), "pandoc": draft["pandoc"], "pypdf": draft["pypdf"], "model_provenance": MODEL},
        "visual_checks": {"status": "PASS", "visual_receipt": visual_id, "render_inventory": render_id, "pages_inspected": list(range(501, 512)), "severity_census": {"P1": 0, "P2": 0, "P3": 0}},
        "browser_checks": {"status": "PASS", "browser_receipt": browser_id, "desktop": "PASS", "mobile": "PASS", "offline": "PASS", "unresolved_fragment_links": 0, "runtime_external_asset_references": 0, "console_errors": 0, "console_warnings": 0, "severity_census": {"P1": 0, "P2": 0, "P3": 0}},
        "remaining": {"computation_labs": ["D60-LAB02", "D60-LAB03", "D60-LAB04"], "proof_metadata_status": proof.get("status"), "capstone": "pending"},
        "limitations": [
            "The composite course remains partial: computation Labs 2-4, the cross-invariant capstone, and the recorded proof-metadata closure remain.",
            "The PDF remains untagged; the self-contained native-MathML HTML is the primary reflowable surface.",
            "Public-byte readback is a post-publication transaction and is not claimed by this local build receipt."
        ]
    }
    target.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", **identity(TARGET_REL)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
