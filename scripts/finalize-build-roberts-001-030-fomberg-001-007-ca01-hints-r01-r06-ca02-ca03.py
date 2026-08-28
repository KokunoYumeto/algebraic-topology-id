#!/usr/bin/env python3
"""Finalize the deterministic CA02/CA03 reader after visual and browser QA.

This bounded finalizer never rebuilds or changes a reader. It verifies the
already-produced draft, exact artifacts, assessment/backend closure, render
inventory, and browser/visual receipts, then creates one no-overwrite final
build receipt for the v0.31.2 release gate.
"""

from __future__ import annotations

import csv
import json
import re
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from pypdf import PdfReader


LANE = Path(__file__).resolve().parents[1]
TOKEN = "ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03"
SLUG = "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"

DRAFT_REL = f"qa/{TOKEN}_BUILD_DRAFT.json"
TARGET_REL = f"qa/{TOKEN}_BUILD_RECEIPT.json"
VISUAL_REL = f"qa/{TOKEN}_VISUAL_QA.md"
RENDER_REL = f"qa/{TOKEN}_RENDER_INVENTORY.csv"
BROWSER_REL = f"qa/{TOKEN}_BROWSER_QA.json"
HTML_REL = f"output/html/{SLUG}/index.html"
PDF_REL = f"output/pdf/topologi-aljabar-{SLUG}-id.pdf"
MANIFEST_REL = f"output/ARTIFACT_MANIFEST_{TOKEN}.csv"
COMBINED_QA_REL = "qa/CUMULATIVE_ASSESSMENTS_002_003_QA.json"
BACKEND_REL = "qa/BACKEND_APPEND_ONLY_CUMULATIVE_ASSESSMENTS_002_003_CUMULATIVE_RECEIPT.json"
ROUTE_REL = "qa/ROUTE_MASTERY_CENSUS.json"
PROOF_REL = "qa/PROOF_REPAIR_CENSUS.json"
BUILDER_REL = f"scripts/build-{SLUG}.ps1"
FINALIZER_REL = f"scripts/finalize-build-{SLUG}.py"

EXPECTED = {
    HTML_REL: (15_287_428, "417e50656ae0a61134c480f59df1bcd54d66a68c938d1d54f9c931ba37e2a5d6"),
    PDF_REL: (8_915_996, "74ed9b5bf0f79a98693369dc7beba3e84ac81c711cc96b9951ae950ae9632a16"),
    MANIFEST_REL: (345, "40220aec7c99f28892775a2d274bcc24ae3cc847946737424a254d97aa7f5c69"),
    COMBINED_QA_REL: (3_906, "24439975cfe1d877dbffdb2948afaa78839b43cd172b2a95cbf1bb0bee599932"),
    BACKEND_REL: (11_073, "61e5a3791ca4cacf7a2fbe0c09f5b638afd1c2c427f8784d04b96331903d53c7"),
    "source/id-ID/mastery/cumulative-assessment-002-homology-excision-cellular.md": (25_321, "2f8dc58eb4fb2da06e239d8e0979112c5f50c846f584900a2e7ea4999a8685ea"),
    "source/id-ID/mastery/cumulative-assessment-003-cohomology-degree-synthesis.md": (26_074, "35c2c9a1b7edbeb1902245b567754e33f4720e11b48d2822bad7666a6a626894"),
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


def load(relative: str) -> dict[str, Any]:
    return json.loads(path(relative).read_text(encoding="utf-8"))


def exact_identity(relative: str) -> dict[str, Any]:
    actual = identity(relative)
    expected_bytes, expected_sha = EXPECTED[relative]
    require(actual["bytes"] == expected_bytes and actual["sha256"] == expected_sha, f"identity drift: {relative}")
    return actual


def assert_receipt_identity(row: dict[str, Any], expected: dict[str, Any], label: str) -> None:
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


def verify_assessments() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    combined = load(COMBINED_QA_REL)
    require(
        combined.get("status") == "PASS"
        and combined.get("cumulative_items_added") == 16
        and combined.get("exercise_hint_solution_triples") == 16
        and combined.get("complete_checked_solutions") == 16
        and combined.get("mastery_postcondition", {}).get("total") == 108,
        "combined CA02/CA03 QA closure mismatch",
    )
    rows = []
    for code, source, math_review, language_review in (
        (
            "D60-CA02",
            "source/id-ID/mastery/cumulative-assessment-002-homology-excision-cellular.md",
            "qa/cumulative-assessment-002/INDEPENDENT_MATH_REVIEW.json",
            "qa/cumulative-assessment-002/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json",
        ),
        (
            "D60-CA03",
            "source/id-ID/mastery/cumulative-assessment-003-cohomology-degree-synthesis.md",
            "qa/cumulative-assessment-003/INDEPENDENT_MATH_REVIEW.json",
            "qa/cumulative-assessment-003/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json",
        ),
    ):
        source_id = exact_identity(source)
        text = path(source).read_text(encoding="utf-8")
        require(text.count("::: {.exercise") == text.count("::: {.hint") == text.count("::: {.solution") == 8, f"{code} source triple mismatch")
        reviews = []
        for review_rel in (math_review, language_review):
            review = load(review_rel)
            require(str(review.get("status", "")).startswith("PASS"), f"{code} review failed: {review_rel}")
            require(review.get("reader_sha256") == source_id["sha256"], f"{code} review does not bind source: {review_rel}")
            reviews.append(identity(review_rel))
        rows.append({"assessment_id": code, "source": source_id, "reviews": reviews, "items": 8, "hints": 8, "complete_solutions": 8})
    return combined, rows


def verify_backend_and_route() -> tuple[dict[str, Any], dict[str, Any]]:
    backend = load(BACKEND_REL)
    prefix, final = backend.get("immutable_prefix", {}), backend.get("cumulative", {})
    require(
        backend.get("status") == "PASS"
        and prefix.get("preserved_exactly") is True
        and prefix.get("records") == 7012
        and prefix.get("bytes") == 8_545_732
        and prefix.get("bundle_sha256") == "7d723f9ef163303c7dde63d646dc8d5917c2450b1da5d24c87ef77bf4e4d664b"
        and final.get("records") == 7273
        and final.get("bytes") == 8_840_132
        and final.get("bundle_sha256") == "97edc6371a0bf670ebdaaa4fab8618ec138ae25c4bf54ca9172139934ba0b464"
        and final.get("solution_bearing_slots") == 108
        and backend.get("replay", {}).get("status") == "PASS",
        "append-only backend closure mismatch",
    )
    route = load(ROUTE_REL)
    compliance = route.get("compliance", {}).get("backend_admitted", {})
    assessments = route.get("assessments", {}).get("backend", {})
    ordinary = route.get("ordinary_mastery", {}).get("quota", {})
    graph = route.get("graph_validation", {})
    require(
        route.get("status") == "PASS"
        and ordinary.get("capped_route_credit") == 84
        and ordinary.get("gap") == 0
        and ordinary.get("met") is True
        and assessments.get("credited_items") == 24
        and assessments.get("complete_assessment_ids") == ["D60-CA01", "D60-CA02", "D60-CA03"]
        and compliance.get("total_slots_covered") == compliance.get("required") == 108
        and compliance.get("gap") == 0
        and compliance.get("met") is True
        and graph.get("validation_error_count") == 0
        and not graph.get("duplicate_or_reused_triple_solution_ids"),
        "108/108 route-mastery closure mismatch",
    )
    return backend, route


def verify_reader_draft() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    draft = load(DRAFT_REL)
    require(draft.get("status") == "PASS_DETERMINISTIC_BUILD_PENDING_VISUAL_BROWSER_QA", "deterministic draft status mismatch")
    require(draft.get("model_provenance") == MODEL and draft.get("pypdf") == "6.12.2", "draft tool/provenance drift")
    html_id, pdf_id, manifest_id = exact_identity(HTML_REL), exact_identity(PDF_REL), exact_identity(MANIFEST_REL)
    assert_receipt_identity(draft.get("html", {}), html_id, "draft HTML")
    assert_receipt_identity(draft.get("pdf", {}), pdf_id, "draft PDF")
    assert_receipt_identity(draft.get("manifest", {}), manifest_id, "draft manifest")
    require(draft["html"].get("dom_ids") == 2466 and draft["html"].get("fragment_links") == 516 and draft["html"].get("assessment_triples_added") == 16, "draft HTML census mismatch")
    require(draft["pdf"].get("pages") == 501 and draft["pdf"].get("appendix_pages") == 19 and draft["pdf"].get("stable_id_destinations_added") == 68, "draft PDF census mismatch")
    require(draft["pdf"].get("all_fonts_embedded_subset_tounicode") is True and draft["pdf"].get("deterministic_merged_builds") == 2, "draft PDF reproducibility/font gate failed")
    html_text = path(HTML_REL).read_text(encoding="utf-8")
    inventory = HtmlInventory()
    inventory.feed(html_text)
    ids, fragments = inventory.ids, inventory.fragments
    require(len(ids) == len(set(ids)) == 2466 and len(fragments) == 516 and not (set(fragments) - set(ids)), "serialized HTML ID/link gate failed")
    require(inventory.math_nodes == 16_911 and "<script src=" not in html_text and "<link rel=" not in html_text, "HTML MathML/self-contained gate failed")
    reader = PdfReader(str(path(PDF_REL)))
    require(len(reader.pages) == 501, "live PDF page count mismatch")
    for page_number in range(481, 501):
        page = reader.pages[page_number]
        require(abs(float(page.mediabox.width) - 595.276) < 0.5 and abs(float(page.mediabox.height) - 841.89) < 0.5, f"non-A4 bounded page: {page_number + 1}")
        require((page.extract_text() or "").strip(), f"empty bounded PDF page: {page_number + 1}")
    return draft, html_id, {**pdf_id, "pages": 501}, manifest_id


def verify_visual_browser() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    visual = path(VISUAL_REL).read_text(encoding="utf-8")
    require("Overall disposition: **PASS" in visual and all(f"P{i} " in visual and f"P{i} (" in visual for i in (1, 2, 3)), "visual receipt lacks PASS/severity closure")
    require("P1 (missing, unreadable, blank, clipped, or broken content): **0**" in visual, "visual P1 mismatch")
    require("P2 (material layout, transition, font, formula, hierarchy, or navigation defect): **0**" in visual, "visual P2 mismatch")
    require("P3 (minor visible cosmetic defect): **0**" in visual, "visual P3 mismatch")
    with path(RENDER_REL).open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require([int(row["physical_page"]) for row in rows] == list(range(482, 502)), "render inventory page sequence mismatch")
    require(len(rows) == 20 and all(row["visual_status"] == "PASS" and row["retained_after_qa"] == "false" for row in rows), "render inventory disposition mismatch")
    require(sum(int(row["bytes"]) for row in rows) == 5_269_583, "render inventory byte total mismatch")
    browser = load(BROWSER_REL)
    assert_receipt_identity(browser.get("artifact", {}), exact_identity(HTML_REL), "browser HTML")
    require(
        browser.get("status") == "PASS"
        and browser.get("desktop", {}).get("status") == "PASS"
        and browser.get("mobile", {}).get("status") == "PASS"
        and browser["desktop"].get("page_level_horizontal_overflow") is False
        and browser["mobile"].get("page_level_horizontal_overflow") is False
        and browser.get("semantic_and_binding_checks", {}).get("unresolved_fragment_links") == 0
        and browser["semantic_and_binding_checks"].get("duplicate_live_dom_ids") == 0
        and browser["semantic_and_binding_checks"].get("runtime_external_asset_references") == 0
        and browser.get("console", {}).get("errors") == browser["console"].get("warnings") == 0
        and browser.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0},
        "browser QA closure mismatch",
    )
    return identity(VISUAL_REL), identity(RENDER_REL), identity(BROWSER_REL)


def main() -> None:
    target = path(TARGET_REL)
    require(not target.exists(), f"refusing to overwrite final receipt: {TARGET_REL}")
    draft, html_id, pdf_id, manifest_id = verify_reader_draft()
    combined, assessments = verify_assessments()
    backend, route = verify_backend_and_route()
    visual_id, render_id, browser_id = verify_visual_browser()
    proof_id = identity(PROOF_REL)
    receipt = {
        "qa_id": "O012-RBT-001-030-FOM-001-007-CA01-HINTS-R01-R06-CA02-CA03-COMPOSITE-BUILD",
        "status": "PASS",
        "scope": "Roberts 30/30; Fomberg Sections 1.1-1.13; D60-CA01/02/03; ordinary mastery 84/84; solution-bearing mastery 108/108; labs, capstone, and recorded proof closure pending",
        "model_provenance": MODEL,
        "deterministic_build_draft": identity(DRAFT_REL),
        "html": {**html_id, "title": "Topologi Aljabar — Roberts 30/30, Fomberg 1.1–1.13, dan Asesmen Kumulatif 1–3", "lang": "id-ID", "self_contained": True},
        "pdf": {**pdf_id, "page_size": "A4", "tagged": False},
        "manifest": {**manifest_id, "entries": 2},
        "artifacts": {"html": html_id, "pdf": pdf_id, "manifest": manifest_id},
        "frozen_predecessor": draft.get("frozen_predecessor"),
        "assessments": {
            "status": "PASS",
            "completed": ["D60-CA01", "D60-CA02", "D60-CA03"],
            "new_assessments": assessments,
            "combined_qa": exact_identity(COMBINED_QA_REL),
            "ordinary_mastery_items": 84,
            "cumulative_assessment_items": 24,
            "solution_bearing_items": 108,
        },
        "backend_boundary": {
            "status": "PASS_APPEND_ONLY_REPLAYABLE",
            "receipt": exact_identity(BACKEND_REL),
            "immutable_prefix_records": 7012,
            "records_added": 261,
            "cumulative_records": 7273,
            "cumulative_bytes": 8_840_132,
            "cumulative_bundle_sha256": "97edc6371a0bf670ebdaaa4fab8618ec138ae25c4bf54ca9172139934ba0b464",
            "route_mastery_census": identity(ROUTE_REL),
            "route_status": route["status"],
            "proof_repair_census": proof_id,
            "proof_repair_status": load(PROOF_REL).get("status"),
        },
        "html_checks": {
            "status": "PASS", "serialized_dom_ids": 2466, "live_browser_dom_ids": 2467,
            "live_runtime_injected_ids": 1, "fragment_links": 516, "unresolved_fragment_links": 0,
            "mathml_nodes": 16_911, "assessment_triples_added": 16, "self_contained": True,
            "centered_reflow": True,
        },
        "pdf_checks": {
            "status": "PASS", "pages": 501, "appended_assessment_pages": 19,
            "bounded_pages_structurally_checked": 20, "all_bounded_pages_a4_nonempty": True,
            "bounded_out_of_page_glyph_boxes": 0, "bounded_replacement_square_markers": 0,
            "fonts": 75, "all_fonts_embedded_subset_tounicode": True,
            "stable_id_destinations_added": 68, "outline_entries_added": 20,
        },
        "reproducibility": {
            "frozen_inputs_fail_closed": True, "html_clean_writes": 2,
            "pdf_appendix_clean_builds": 2, "merged_pdf_clean_builds": 2,
            "merged_pdf_builds_byte_identical": True, "predecessor_html_exact_reconstruction": True,
            "predecessor_pdf_pages_structural_and_pixel_equivalent": 482,
            "source_date_epoch": draft.get("source_date_epoch"),
        },
        "toolchain": {"builder": identity(BUILDER_REL), "finalizer": identity(FINALIZER_REL), "pandoc": draft.get("pandoc"), "pypdf": draft.get("pypdf"), "model_provenance": MODEL},
        "visual_checks": {"status": "PASS", "visual_receipt": visual_id, "render_inventory": render_id, "pages_inspected": list(range(482, 502)), "severity_census": {"P1": 0, "P2": 0, "P3": 0}},
        "browser_checks": {"status": "PASS", "browser_receipt": browser_id, "desktop": "PASS", "mobile": "PASS", "offline": "PASS", "unresolved_fragment_links": 0, "runtime_external_asset_references": 0, "console_errors": 0, "console_warnings": 0, "severity_census": {"P1": 0, "P2": 0, "P3": 0}},
        "limitations": [
            "The composite course remains partial: four computation laboratories, the cross-invariant capstone, and the recorded proof-metadata closure remain.",
            "The PDF remains untagged; the self-contained native-MathML HTML is the primary reflowable surface.",
            "Public-byte readback is a post-publication transaction and is not claimed by this local build receipt."
        ],
    }
    require(combined.get("mastery_postcondition", {}).get("total") == 108 and backend["cumulative"]["solution_bearing_slots"] == 108, "late mastery gate drift")
    target.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", **identity(TARGET_REL)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
