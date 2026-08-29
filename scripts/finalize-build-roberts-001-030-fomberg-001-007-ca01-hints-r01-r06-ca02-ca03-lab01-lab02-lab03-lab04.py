#!/usr/bin/env python3
"""Finalize the deterministic Lab 4 reader after visual and browser QA.

The finalizer never rebuilds or changes a reader. It binds exact source,
execution, append-only backend, deterministic reader, visual, and browser
evidence into one no-overwrite receipt. The Lab 4 QA/backend identities must
be supplied explicitly at runtime.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from pypdf import PdfReader


LANE = Path(__file__).resolve().parents[1]
TOKEN = "ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04"
PRIOR_SLUG = "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03"
SLUG = PRIOR_SLUG + "-lab04"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
PRIOR_PAGES = 545
PRIOR_OUTLINE = 469
PRIOR_NAMED = 3_130
LAB_STABLE_IDS = 25
LAB_HEADINGS = 18
LAB_TASKS = 6
ROUTES = ["D60-R04", "D60-R05", "D60-R12", "D60-R13", "D60-R14"]
BACKEND_PREFIX = (7_694, 9_280_385, "cddd65499da547e0c4f01b8a880f68d1c3d314c078a9179528e4a28b2c5f65a2")

DRAFT_REL = f"qa/{TOKEN}_BUILD_DRAFT.json"
TARGET_REL = f"qa/{TOKEN}_BUILD_RECEIPT.json"
VISUAL_REL = f"qa/{TOKEN}_VISUAL_QA.md"
RENDER_REL = f"qa/{TOKEN}_RENDER_INVENTORY.csv"
BROWSER_REL = f"qa/{TOKEN}_BROWSER_QA.json"
HTML_REL = f"output/html/{SLUG}/index.html"
PDF_REL = f"output/pdf/topologi-aljabar-{SLUG}-id.pdf"
MANIFEST_REL = f"output/ARTIFACT_MANIFEST_{TOKEN}.csv"
LAB_QA_REL = "qa/COMPUTATION_LAB_004_QA.json"
BACKEND_REL = "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_004_CUMULATIVE_RECEIPT.json"
PROOF_REL = "qa/PROOF_REPAIR_CENSUS.json"
BUILDER_REL = f"scripts/build-{SLUG}.py"
MERGER_REL = "scripts/merge-computation-lab-004.py"
FINALIZER_REL = f"scripts/finalize-build-{SLUG}.py"
RENDER_DIR_REL = "tmp/pdfs/lab04-visual-qa"
PRIOR_HTML_REL = f"output/html/{PRIOR_SLUG}/index.html"
PRIOR_PDF_REL = f"output/pdf/topologi-aljabar-{PRIOR_SLUG}-id.pdf"
SOURCE_RELS = [
    "source/id-ID/labs/computation-lab-004-cross-invariant-comparison.md",
    "source/id-ID/labs/o012_d60_lab04_cross_invariants.py",
    "source/id-ID/labs/test_o012_d60_lab04_cross_invariants.py",
    "source/id-ID/labs/expected-output-lab04.txt",
]
EXPECTED_PREDECESSOR = {
    PRIOR_HTML_REL: (15_828_588, "c221955503cec820c7581c740a038ac1774999ac6a6014f8d0783da2cd08bf0d"),
    PRIOR_PDF_REL: (9_836_725, "b26b670db97facc9f5ab389eed69cf1f8b03f70e6047eacbd2bfa68c849ccd0d"),
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


def exact_predecessor(relative: str) -> dict[str, Any]:
    actual = identity(relative)
    require((actual["bytes"], actual["sha256"]) == EXPECTED_PREDECESSOR[relative], f"identity drift: {relative}")
    return actual


def exact_runtime(relative: str, size: int, checksum: str, label: str) -> dict[str, Any]:
    require(size > 0 and re.fullmatch(r"[0-9a-f]{64}", checksum) is not None, f"invalid runtime identity: {label}")
    actual = identity(relative)
    require((actual["bytes"], actual["sha256"]) == (size, checksum), f"runtime identity drift: {label}")
    return actual


def load(relative: str) -> dict[str, Any]:
    return json.loads(path(relative).read_text(encoding="utf-8"))


def bind(row: dict[str, Any], expected: dict[str, Any], label: str) -> None:
    for key in ("path", "bytes", "sha256"):
        require(row.get(key) == expected[key], f"{label} {key} mismatch")


def count_outline(items: list[Any]) -> int:
    return sum(count_outline(item) if isinstance(item, list) else 1 for item in items)


class HtmlInventory(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.fragments: list[str] = []
        self.math_nodes = 0
        self.lab_headings = 0
        self.lab_tasks = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        ident = values.get("id")
        if ident:
            self.ids.append(str(ident))
            if tag.lower() == "section" and str(ident).startswith("o012-d60-lab04"):
                self.lab_headings += 1
        classes = set(str(values.get("class") or "").split())
        if "exercise" in classes and ident and str(ident).startswith("o012-d60-lab04-task-"):
            self.lab_tasks += 1
        href = values.get("href")
        if href and href.startswith("#") and len(href) > 1:
            self.fragments.append(href[1:])
        if tag.lower() == "math":
            self.math_nodes += 1


def runtime_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--lab-qa-bytes", required=True, type=int)
    parser.add_argument("--lab-qa-sha256", required=True)
    parser.add_argument("--backend-receipt-bytes", required=True, type=int)
    parser.add_argument("--backend-receipt-sha256", required=True)
    parser.add_argument("--backend-cumulative-records", required=True, type=int)
    parser.add_argument("--backend-cumulative-bytes", required=True, type=int)
    parser.add_argument("--backend-cumulative-sha256", required=True)


def verify_sources_and_backend(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    lab_identity = exact_runtime(LAB_QA_REL, args.lab_qa_bytes, args.lab_qa_sha256, "Lab 4 QA")
    backend_identity = exact_runtime(BACKEND_REL, args.backend_receipt_bytes, args.backend_receipt_sha256, "Lab 4 backend receipt")
    require(args.backend_cumulative_records > BACKEND_PREFIX[0] and args.backend_cumulative_bytes > BACKEND_PREFIX[1], "backend cumulative boundary did not advance")
    require(re.fullmatch(r"[0-9a-f]{64}", args.backend_cumulative_sha256) is not None, "invalid backend cumulative SHA-256")
    sources = [identity(relative) for relative in SOURCE_RELS]
    lab = load(LAB_QA_REL)
    checks = lab.get("checks", {})
    require(
        lab.get("status") == "PASS"
        and lab.get("receipt_kind") == "computation_laboratory_source_execution_review_closure"
        and lab.get("laboratory_id") == "D60-LAB04"
        and lab.get("edition_unit_id") == "O012-ORIG-LAB04"
        and lab.get("course_route_unit_ids") == ROUTES
        and lab.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0}
        and checks.get("two_test_runs_6_of_6") == "PASS"
        and checks.get("two_program_runs_byte_identical") == "PASS"
        and checks.get("expected_output_exact") == "PASS"
        and checks.get("independent_code") == "PASS"
        and checks.get("independent_mathematics") == "PASS"
        and checks.get("independent_source_language") == "PASS"
        and checks.get("stable_ids_25_unique") == "PASS"
        and checks.get("tasks_6_with_hint_and_complete_solution") == "PASS"
        and checks.get("route_scope_D60_R04_R05_R12_R13_R14") == "PASS"
        and checks.get("rights_origin_provenance_non_endorsement") == "PASS",
        "Lab 4 source/execution/review closure mismatch",
    )
    for expected in sources:
        require(any(all(row.get(key) == expected[key] for key in ("path", "bytes", "sha256")) for row in lab.get("inputs", [])), f"Lab QA does not bind {expected['path']}")

    backend = load(BACKEND_REL)
    prefix, final, replay = backend.get("immutable_prefix", {}), backend.get("cumulative", {}), backend.get("replay", {})
    semantic = backend.get("semantic_checks", {})
    expected_final = (args.backend_cumulative_records, args.backend_cumulative_bytes, args.backend_cumulative_sha256)
    require(
        backend.get("status") == "PASS"
        and backend.get("receipt_kind") == "cumulative_backend_boundary"
        and backend.get("laboratory_id") == "D60-LAB04"
        and backend.get("edition_unit_id") == "O012-ORIG-LAB04"
        and prefix.get("preserved_exactly") is True
        and (prefix.get("records"), prefix.get("bytes"), prefix.get("bundle_sha256")) == BACKEND_PREFIX
        and (final.get("records"), final.get("bytes"), final.get("bundle_sha256")) == expected_final
        and final.get("computation_laboratories_complete") == 4
        and final.get("computation_laboratories_required") == 4
        and replay.get("status") == "PASS"
        and replay.get("temporary_replay_removed") is True
        and (replay.get("final", {}).get("records"), replay.get("final", {}).get("bytes"), replay.get("final", {}).get("bundle_sha256")) == expected_final
        and semantic.get("append_only_ordering") == "PASS"
        and semantic.get("independent_semantics") == "PASS"
        and semantic.get("relation_reference_integrity") == "PASS"
        and semantic.get("records_added") == args.backend_cumulative_records - BACKEND_PREFIX[0]
        and semantic.get("stable_ids") == LAB_STABLE_IDS
        and semantic.get("tasks") == LAB_TASKS,
        "Lab 4 append-only backend closure mismatch",
    )
    backend_files = backend.get("files", [])
    require(
        isinstance(backend_files, list)
        and len(backend_files) == 11
        and all(row.get("prefix_preserved") is True and row.get("suffix_exact") is True for row in backend_files),
        "backend file-prefix replay mismatch",
    )
    require(lab_identity["path"] == LAB_QA_REL and backend_identity["path"] == BACKEND_REL, "runtime receipt path binding drift")
    return lab, backend, sources


def verify_reader(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], HtmlInventory]:
    draft = load(DRAFT_REL)
    require(draft.get("status") == "PASS_DETERMINISTIC_BUILD_PENDING_VISUAL_BROWSER_QA" and draft.get("model_provenance") == MODEL, "draft status/provenance mismatch")
    html_id, pdf_id, manifest_id = identity(HTML_REL), identity(PDF_REL), identity(MANIFEST_REL)
    bind(draft.get("html", {}), html_id, "draft HTML")
    bind(draft.get("pdf", {}), pdf_id, "draft PDF")
    bind(draft.get("manifest", {}), manifest_id, "draft manifest")
    lab_id = exact_runtime(LAB_QA_REL, args.lab_qa_bytes, args.lab_qa_sha256, "Lab 4 QA")
    backend_id = exact_runtime(BACKEND_REL, args.backend_receipt_bytes, args.backend_receipt_sha256, "Lab 4 backend receipt")
    bind(draft.get("qa", {}), lab_id, "draft Lab QA")
    bind(draft.get("backend_receipt", {}), backend_id, "draft backend")
    runtime = draft.get("runtime_boundary_bindings", {})
    bind(runtime.get("lab_qa", {}), lab_id, "draft runtime Lab QA")
    bind(runtime.get("backend_receipt", {}), backend_id, "draft runtime backend")
    require(runtime.get("backend_cumulative") == {"records": args.backend_cumulative_records, "bytes": args.backend_cumulative_bytes, "bundle_sha256": args.backend_cumulative_sha256}, "draft runtime cumulative binding mismatch")
    toolchain = draft.get("toolchain_inputs", {})
    bind(toolchain.get("builder", {}), identity(BUILDER_REL), "draft builder")
    bind(toolchain.get("merger", {}), identity(MERGER_REL), "draft merger")
    for expected in (identity(relative) for relative in SOURCE_RELS):
        require(any(all(row.get(key) == expected[key] for key in ("path", "bytes", "sha256")) for row in draft.get("sources", [])), f"draft source binding missing: {expected['path']}")

    frozen = draft.get("frozen_predecessor", {})
    prior_html, prior_pdf = exact_predecessor(PRIOR_HTML_REL), exact_predecessor(PRIOR_PDF_REL)
    require(
        (frozen.get("html_bytes"), frozen.get("html_sha256")) == (prior_html["bytes"], prior_html["sha256"])
        and (frozen.get("pdf_bytes"), frozen.get("pdf_sha256"), frozen.get("pdf_pages")) == (prior_pdf["bytes"], prior_pdf["sha256"], PRIOR_PAGES)
        and frozen.get("html_exact_reconstruction") is True
        and frozen.get("pdf_extracted_text_prefix_identical") is True
        and frozen.get("pdf_outline_exact_prefix") is True
        and frozen.get("pdf_named_destinations_preserved") is True
        and re.fullmatch(r"[0-9a-f]{64}", str(frozen.get("pdf_page_structure_aggregate_sha256", ""))) is not None,
        "frozen predecessor proof mismatch",
    )
    with path(MANIFEST_REL).open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 2, "artifact manifest entry census mismatch")
    for artifact in (html_id, pdf_id):
        require(any(row.get("path") == artifact["path"] and int(row.get("bytes", -1)) == artifact["bytes"] and row.get("sha256") == artifact["sha256"] for row in rows), f"artifact manifest does not bind {artifact['path']}")

    html_text = path(HTML_REL).read_text(encoding="utf-8")
    inv = HtmlInventory()
    inv.feed(html_text)
    lab_ids = [ident for ident in inv.ids if ident.startswith("o012-d60-lab04")]
    require(
        len(inv.ids) == len(set(inv.ids)) == draft["html"].get("dom_ids")
        and len(inv.fragments) == draft["html"].get("fragment_links")
        and not (set(inv.fragments) - set(inv.ids))
        and len(lab_ids) == len(set(lab_ids)) == LAB_STABLE_IDS + 1
        and inv.lab_headings == LAB_HEADINGS
        and inv.lab_tasks == LAB_TASKS
        and draft["html"].get("stable_ids_added") == LAB_STABLE_IDS
        and draft["html"].get("tasks_added") == LAB_TASKS,
        "serialized HTML census/binding gate failed",
    )
    require("<script src=" not in html_text and "<link rel=" not in html_text and "pre { max-width: 100%; overflow-x: auto; white-space: pre; }" in html_text and "max-width: 58rem;" in html_text and "margin: 0 auto;" in html_text and "@media (max-width: 700px)" in html_text, "HTML self-contained centered/reflowing shell gate failed")

    reader = PdfReader(str(path(PDF_REL)))
    pages = len(reader.pages)
    appendix_pages = pages - PRIOR_PAGES
    require(
        pages == draft["pdf"].get("pages")
        and appendix_pages == draft["pdf"].get("appendix_pages")
        and appendix_pages > 0
        and count_outline(reader.outline) == draft["pdf"].get("outline_entries") == PRIOR_OUTLINE + LAB_HEADINGS
        and len(reader.named_destinations) == draft["pdf"].get("named_destinations") == PRIOR_NAMED + LAB_STABLE_IDS
        and draft["pdf"].get("stable_id_destinations_added") == LAB_STABLE_IDS
        and draft["pdf"].get("outline_entries_added") == LAB_HEADINGS
        and draft["pdf"].get("all_fonts_embedded_subset_tounicode") is True
        and draft["pdf"].get("trailer_id_suppressed") is True
        and draft["pdf"].get("deterministic_appendix_builds") == draft["pdf"].get("deterministic_merged_builds") == 2,
        "live PDF structure/reproducibility gate failed",
    )
    for page_number in range(PRIOR_PAGES - 1, pages):
        page = reader.pages[page_number]
        require(abs(float(page.mediabox.width) - 595.276) < 0.5 and abs(float(page.mediabox.height) - 841.89) < 0.5, f"non-A4 page: {page_number + 1}")
        require((page.extract_text() or "").strip(), f"empty page: {page_number + 1}")
    return draft, html_id, {**pdf_id, "pages": pages}, manifest_id, inv


def verify_visual_browser(final_pages: int, inv: HtmlInventory) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], list[int], int]:
    visual = path(VISUAL_REL).read_text(encoding="utf-8")
    for line in (
        "P1 (missing, unreadable, blank, clipped, or broken content): **0**",
        "P2 (material layout, transition, font, formula, hierarchy, or navigation defect): **0**",
        "P3 (minor visible cosmetic defect after correction and rerender): **0**",
        "Overall disposition: **PASS",
    ):
        require(line in visual, f"visual closure missing: {line}")
    with path(RENDER_REL).open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    expected_pages = list(range(PRIOR_PAGES, final_pages + 1))
    require([int(row["physical_page"]) for row in rows] == expected_pages, "render page sequence mismatch")
    require(len(rows) == final_pages - PRIOR_PAGES + 1, "render inventory count mismatch")
    require(all(row["visual_status"] == "PASS" and row["retained_after_qa"] == "false" for row in rows), "render disposition mismatch")
    render_bytes = sum(int(row["bytes"]) for row in rows)
    for row in rows:
        render = path(f"{RENDER_DIR_REL}/{row['render_file']}")
        require(render.is_file() and render.stat().st_size == int(row["bytes"]) and digest(render) == row["sha256"], f"render identity mismatch: {row['render_file']}")

    browser = load(BROWSER_REL)
    bind(browser.get("artifact", {}), identity(HTML_REL), "browser HTML")
    semantic, mobile = browser.get("semantic_and_binding_checks", {}), browser.get("mobile", {})
    navigation = browser.get("navigation_and_keyboard", {})
    code_scroll = mobile.get("code_blocks_requiring_local_scroll")
    math_scroll = mobile.get("wide_display_math_nodes")
    predecessor_tables = mobile.get("predecessor_wide_table_containers")
    require(
        browser.get("status") == "PASS"
        and browser.get("desktop", {}).get("page_level_horizontal_overflow") is False
        and mobile.get("page_level_horizontal_overflow") is False
        and isinstance(code_scroll, int) and code_scroll > 0 and code_scroll == mobile.get("code_blocks_with_overflow_x_auto")
        and isinstance(math_scroll, int) and math_scroll >= 0 and math_scroll == mobile.get("wide_display_math_nodes_with_overflow_x_auto")
        and predecessor_tables == mobile.get("predecessor_wide_table_containers_with_overflow_x_auto")
        and mobile.get("unexpected_local_overflow_nodes") == 0
        and semantic.get("serialized_dom_ids") == len(inv.ids)
        and semantic.get("live_browser_dom_ids") == len(inv.ids) + 1
        and semantic.get("duplicate_live_dom_ids") == 0
        and semantic.get("fragment_links") == len(inv.fragments)
        and semantic.get("unresolved_fragment_links") == 0
        and semantic.get("runtime_external_asset_references") == 0
        and semantic.get("laboratory_stable_ids") == LAB_STABLE_IDS
        and semantic.get("laboratory_root_plus_stable_ids") == LAB_STABLE_IDS + 1
        and semantic.get("laboratory_headings") == LAB_HEADINGS
        and semantic.get("laboratory_tasks") == LAB_TASKS
        and isinstance(semantic.get("laboratory_mathml_nodes"), int) and semantic.get("laboratory_mathml_nodes") > 0
        and semantic.get("document_mathml_nodes") == inv.math_nodes
        and navigation.get("toc_lab04_link_count") == 1
        and navigation.get("toc_lab04_activation") == "PASS"
        and navigation.get("activated_hash") == "#o012-d60-lab04"
        and navigation.get("keyboard_focus", {}).get("status") == "PASS"
        and browser.get("console", {}).get("errors") == browser.get("console", {}).get("warnings") == 0
        and browser.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0},
        "browser QA closure mismatch",
    )
    counts = {"code_local_scrollers": code_scroll, "math_local_scrollers": math_scroll, "predecessor_table_local_scrollers": predecessor_tables}
    return identity(VISUAL_REL), identity(RENDER_REL), identity(BROWSER_REL), counts, expected_pages, render_bytes


def main(args: argparse.Namespace) -> None:
    target = path(TARGET_REL)
    require(not target.exists(), f"refusing to overwrite final receipt: {TARGET_REL}")
    lab, backend, sources = verify_sources_and_backend(args)
    draft, html_id, pdf_id, manifest_id, inv = verify_reader(args)
    visual_id, render_id, browser_id, browser_counts, visual_pages, render_bytes = verify_visual_browser(pdf_id["pages"], inv)
    proof = load(PROOF_REL)
    receipt = {
        "qa_id": "O012-RBT-001-030-FOM-001-007-CA01-HINTS-R01-R06-CA02-CA03-LAB01-LAB02-LAB03-LAB04-COMPOSITE-BUILD",
        "status": "PASS",
        "scope": "Roberts 30/30; Fomberg Sections 1.1-1.13; D60-CA01/02/03; ordinary mastery 84/84; solution-bearing mastery 108/108; computation Labs 1-4 complete; proof-metadata closure and capstone pending",
        "model_provenance": MODEL,
        "deterministic_build_draft": identity(DRAFT_REL),
        "runtime_boundary_bindings": draft["runtime_boundary_bindings"],
        "sources": sources,
        "source_execution_review": {"status": lab["status"], "receipt": exact_runtime(LAB_QA_REL, args.lab_qa_bytes, args.lab_qa_sha256, "Lab 4 QA"), "routes": ROUTES, "tasks": LAB_TASKS, "tests": 6, "stable_ids": LAB_STABLE_IDS, "headings": LAB_HEADINGS, "severity_census": lab["severity_census"]},
        "html": {**html_id, "title": "Topologi Aljabar — Roberts 30/30, Fomberg 1.1–1.13, Asesmen Kumulatif 1–3, dan Laboratorium Komputasi 1–4", "lang": "id-ID", "self_contained": True},
        "pdf": {**pdf_id, "page_size": "A4", "tagged": False},
        "manifest": {**manifest_id, "entries": 2},
        "backend_boundary": {"status": "PASS_APPEND_ONLY_REPLAYABLE", "receipt": exact_runtime(BACKEND_REL, args.backend_receipt_bytes, args.backend_receipt_sha256, "Lab 4 backend receipt"), "immutable_prefix_records": BACKEND_PREFIX[0], "records_added": args.backend_cumulative_records - BACKEND_PREFIX[0], "cumulative_records": args.backend_cumulative_records, "cumulative_bytes": args.backend_cumulative_bytes, "cumulative_bundle_sha256": args.backend_cumulative_sha256, "laboratories_complete": 4, "laboratories_required": 4},
        "html_checks": {"status": "PASS", "serialized_dom_ids": len(inv.ids), "live_browser_dom_ids": len(inv.ids) + 1, "fragment_links": len(inv.fragments), "unresolved_fragment_links": 0, "mathml_nodes": inv.math_nodes, "stable_ids_added": LAB_STABLE_IDS, "headings_added": LAB_HEADINGS, "tasks_added": LAB_TASKS, "self_contained": True, "centered_reflow": True},
        "pdf_checks": {"status": "PASS", "pages": pdf_id["pages"], "appended_lab_pages": pdf_id["pages"] - PRIOR_PAGES, "bounded_pages_checked": len(visual_pages), "all_bounded_pages_a4_nonempty": True, "fonts": draft["pdf"]["fonts"], "all_fonts_embedded_subset_tounicode": True, "stable_id_destinations_added": LAB_STABLE_IDS, "outline_entries_added": LAB_HEADINGS},
        "reproducibility": {"frozen_inputs_fail_closed": True, "html_clean_writes": 2, "pdf_appendix_clean_builds": 2, "merged_pdf_clean_builds": 2, "merged_pdf_builds_byte_identical": True, "predecessor_html_exact_reconstruction": True, "predecessor_pdf_extracted_text_prefix_identical": True, "predecessor_pdf_pages_structurally_preserved": PRIOR_PAGES, "predecessor_pdf_page_structure_aggregate_sha256": draft["frozen_predecessor"]["pdf_page_structure_aggregate_sha256"], "source_date_epoch": draft["source_date_epoch"]},
        "toolchain": {"builder": identity(BUILDER_REL), "merger": identity(MERGER_REL), "finalizer": identity(FINALIZER_REL), "pandoc": draft["pandoc"], "pypdf": draft["pypdf"], "model_provenance": MODEL},
        "visual_checks": {"status": "PASS", "visual_receipt": visual_id, "render_inventory": render_id, "pages_inspected": visual_pages, "render_count": len(visual_pages), "render_bytes": render_bytes, "severity_census": {"P1": 0, "P2": 0, "P3": 0}},
        "browser_checks": {"status": "PASS", "browser_receipt": browser_id, "desktop": "PASS", "mobile": "PASS", "offline": "PASS", **browser_counts, "unexpected_local_overflow_nodes": 0, "unresolved_fragment_links": 0, "runtime_external_asset_references": 0, "console_errors": 0, "console_warnings": 0, "severity_census": {"P1": 0, "P2": 0, "P3": 0}},
        "remaining": {"computation_labs": [], "proof_metadata_status": proof.get("status"), "capstone": "pending"},
        "limitations": [
            "The composite course remains partial: the cross-invariant capstone and the recorded proof-metadata closure remain.",
            "The PDF remains untagged; the self-contained native-MathML HTML is the primary reflowable surface.",
            "Public-byte readback is a post-publication transaction and is not claimed by this local build receipt.",
        ],
    }
    target.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", **identity(TARGET_REL)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    runtime_args(parser)
    main(parser.parse_args())
