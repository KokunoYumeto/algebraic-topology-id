#!/usr/bin/env python3
"""Finalize the deterministic Lab 3 reader after visual and browser QA.

This bounded finalizer never rebuilds or changes a reader. It binds the exact
source, execution, append-only backend, deterministic reader, visual, and
browser evidence into one no-overwrite build receipt for the successor gate.
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
TOKEN = "ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03"
SLUG = "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
PRIOR_PAGES = 529
PRIOR_OUTLINE = 451
PRIOR_NAMED = 3_105
LAB_STABLE_IDS = 25
LAB_HEADINGS = 18
LAB_TASKS = 6

DRAFT_REL = f"qa/{TOKEN}_BUILD_DRAFT.json"
TARGET_REL = f"qa/{TOKEN}_BUILD_RECEIPT.json"
VISUAL_REL = f"qa/{TOKEN}_VISUAL_QA.md"
RENDER_REL = f"qa/{TOKEN}_RENDER_INVENTORY.csv"
BROWSER_REL = f"qa/{TOKEN}_BROWSER_QA.json"
HTML_REL = f"output/html/{SLUG}/index.html"
PDF_REL = f"output/pdf/topologi-aljabar-{SLUG}-id.pdf"
MANIFEST_REL = f"output/ARTIFACT_MANIFEST_{TOKEN}.csv"
LAB_QA_REL = "qa/COMPUTATION_LAB_003_QA.json"
BACKEND_REL = "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_003_CUMULATIVE_RECEIPT.json"
PROOF_REL = "qa/PROOF_REPAIR_CENSUS.json"
BUILDER_REL = f"scripts/build-{SLUG}.py"
MERGER_REL = "scripts/merge-computation-lab-003.py"
FINALIZER_REL = f"scripts/finalize-build-{SLUG}.py"
RENDER_DIR_REL = "tmp/pdfs/lab03-visual-qa"
PRIOR_HTML_REL = "output/html/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02/index.html"
PRIOR_PDF_REL = "output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-id.pdf"

SOURCE_RELS = [
    "source/id-ID/labs/computation-lab-003-cellular-boundaries-degree.md",
    "source/id-ID/labs/o012_d60_lab03_cellular_degree.py",
    "source/id-ID/labs/test_o012_d60_lab03_cellular_degree.py",
    "source/id-ID/labs/expected-output-lab03.txt",
]

EXPECTED = {
    LAB_QA_REL: (4_534, "a13bc301036c0d2cbfb6c92ab1423d2c2ca09a503bfa2a830a62832a0c4bf12f"),
    BACKEND_REL: (10_047, "7ee69a9291368d407e38de4c63440d599b5cd13ec5fc288f5468084bc7774c80"),
    SOURCE_RELS[0]: (19_453, "4c3d88ec7d28d14fd1594c59262a50923efbad3082d7796d947661c7012bdf27"),
    SOURCE_RELS[1]: (15_641, "2ef4f077a902459b93dcdaef6db1c608e97c89d64b8dacbb8cb378367150009e"),
    SOURCE_RELS[2]: (8_217, "c1bbe85ff16a76d2ea55dfcb0686d016b52634aa33687e6dd3f9ba4baf568159"),
    SOURCE_RELS[3]: (1_201, "0ac6d4c262eb8088050b3562025e7156dd329832f8cb13b0fd57e4b7f6fe8381"),
    BUILDER_REL: (33_753, "6c05b72eb7ba66393b9f484607c93b1b908151051f361c10696927b90a6eccd4"),
    MERGER_REL: (10_292, "f9b9a2d11131153a15f28d1a763a8d5b17f4c6fca7c8eef93cfcea13feb8512c"),
    PRIOR_HTML_REL: (15_615_104, "d0c6afddfa92759d475258bf08f20ea4019eccf72b7554128b2b938bd247b375"),
    PRIOR_PDF_REL: (9_507_127, "1bad03f9ba031ba91967a0a0ac2af6d15a0f768882cd541fe26dcbe26c4edd0b"),
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


def count_outline(items: list[Any]) -> int:
    total = 0
    for item in items:
        if isinstance(item, list):
            total += count_outline(item)
        else:
            total += 1
    return total


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
            # Pandoc puts explicit heading identifiers on the generated
            # section wrappers, not on their h1/h2 children.
            if tag.lower() == "section" and str(ident).startswith("o012-d60-lab03"):
                self.lab_headings += 1
        classes = set(str(values.get("class") or "").split())
        if "exercise" in classes and ident and str(ident).startswith("o012-d60-lab03-task-"):
            self.lab_tasks += 1
        href = values.get("href")
        if href and href.startswith("#") and len(href) > 1:
            self.fragments.append(href[1:])
        if tag.lower() == "math":
            self.math_nodes += 1


def verify_sources_and_backend() -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    sources = [exact_identity(rel) for rel in SOURCE_RELS]
    lab = load(LAB_QA_REL)
    checks = lab.get("checks", {})
    require(
        lab.get("status") == "PASS"
        and lab.get("receipt_kind") == "computation_laboratory_source_execution_review_closure"
        and lab.get("laboratory_id") == "D60-LAB03"
        and lab.get("edition_unit_id") == "O012-ORIG-LAB03"
        and lab.get("course_route_unit_ids") == ["D60-R12", "D60-R14"]
        and lab.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0}
        and checks.get("two_test_runs_6_of_6") == "PASS"
        and checks.get("two_program_runs_byte_identical") == "PASS"
        and checks.get("expected_output_exact") == "PASS"
        and checks.get("independent_code") == "PASS"
        and checks.get("independent_mathematics") == "PASS"
        and checks.get("independent_source_language") == "PASS"
        and checks.get("stable_ids_25_unique") == "PASS"
        and checks.get("tasks_6_with_hint_and_complete_solution") == "PASS"
        and checks.get("route_scope_D60_R12_R14") == "PASS"
        and checks.get("rights_origin_provenance_non_endorsement") == "PASS",
        "Lab 3 source/execution/review closure mismatch",
    )
    for expected in sources:
        require(
            any(all(row.get(key) == expected[key] for key in ("path", "bytes", "sha256")) for row in lab["inputs"]),
            f"Lab QA does not bind {expected['path']}",
        )

    backend = load(BACKEND_REL)
    prefix, delta, final = backend.get("immutable_prefix", {}), backend.get("delta", {}), backend.get("cumulative", {})
    require(
        backend.get("status") == "PASS"
        and backend.get("receipt_kind") == "cumulative_backend_boundary"
        and backend.get("laboratory_id") == "D60-LAB03"
        and backend.get("edition_unit_id") == "O012-ORIG-LAB03"
        and prefix.get("preserved_exactly") is True
        and (prefix.get("records"), prefix.get("bytes"), prefix.get("bundle_sha256"))
        == (7_546, 9_122_755, "ac3a0377861ed2b728f9c7473579fdd4febe43e454a92f3ea06451e13d46c8f8")
        and (delta.get("records"), delta.get("bytes"), delta.get("bundle_sha256"))
        == (148, 157_630, "44e8ec3a65f35da9a20d1fd589536a7758e39807baf92240ef4d4e597b6fc827")
        and (final.get("records"), final.get("bytes"), final.get("bundle_sha256"))
        == (7_694, 9_280_385, "cddd65499da547e0c4f01b8a880f68d1c3d314c078a9179528e4a28b2c5f65a2")
        and final.get("computation_laboratories_complete") == 3
        and final.get("computation_laboratories_required") == 4
        and backend.get("replay", {}).get("status") == "PASS"
        and backend.get("replay", {}).get("temporary_replay_removed") is True
        and backend.get("semantic_checks", {}).get("append_only_ready") == "PASS"
        and backend.get("semantic_checks", {}).get("stable_ids") == LAB_STABLE_IDS
        and backend.get("semantic_checks", {}).get("tasks") == LAB_TASKS
        and backend.get("semantic_checks", {}).get("dependency_scope") == "D60-R12_and_D60-R14",
        "Lab 3 append-only backend closure mismatch",
    )
    require(all(row.get("prefix_preserved") is True and row.get("suffix_exact") is True for row in backend.get("files", [])), "backend file-prefix replay mismatch")
    return lab, backend, sources


def verify_reader() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], HtmlInventory]:
    draft = load(DRAFT_REL)
    require(draft.get("status") == "PASS_DETERMINISTIC_BUILD_PENDING_VISUAL_BROWSER_QA" and draft.get("model_provenance") == MODEL, "draft status/provenance mismatch")
    html_id, pdf_id, manifest_id = identity(HTML_REL), identity(PDF_REL), identity(MANIFEST_REL)
    bind(draft.get("html", {}), html_id, "draft HTML")
    bind(draft.get("pdf", {}), pdf_id, "draft PDF")
    bind(draft.get("manifest", {}), manifest_id, "draft manifest")
    bind(draft.get("qa", {}), exact_identity(LAB_QA_REL), "draft Lab QA")
    bind(draft.get("backend_receipt", {}), exact_identity(BACKEND_REL), "draft backend")
    toolchain = draft.get("toolchain_inputs", {})
    bind(toolchain.get("builder", {}), exact_identity(BUILDER_REL), "draft builder")
    bind(toolchain.get("merger", {}), exact_identity(MERGER_REL), "draft merger")

    source_rows = draft.get("sources", [])
    for expected in (exact_identity(rel) for rel in SOURCE_RELS):
        require(any(all(row.get(key) == expected[key] for key in ("path", "bytes", "sha256")) for row in source_rows), f"draft source binding missing: {expected['path']}")

    frozen = draft.get("frozen_predecessor", {})
    prior_html = exact_identity(PRIOR_HTML_REL)
    prior_pdf = exact_identity(PRIOR_PDF_REL)
    require(
        (frozen.get("html_bytes"), frozen.get("html_sha256")) == (prior_html["bytes"], prior_html["sha256"])
        and (frozen.get("pdf_bytes"), frozen.get("pdf_sha256"), frozen.get("pdf_pages")) == (prior_pdf["bytes"], prior_pdf["sha256"], PRIOR_PAGES)
        and frozen.get("html_exact_reconstruction") is True
        and frozen.get("pdf_extracted_text_prefix_identical") is True
        and frozen.get("pdf_outline_exact_prefix") is True
        and frozen.get("pdf_named_destinations_preserved") is True
        and isinstance(frozen.get("pdf_page_structure_aggregate_sha256"), str)
        and len(frozen["pdf_page_structure_aggregate_sha256"]) == 64,
        "frozen predecessor proof mismatch",
    )

    with path(MANIFEST_REL).open("r", encoding="utf-8", newline="") as handle:
        manifest_rows = list(csv.DictReader(handle))
    require(len(manifest_rows) == 2, "artifact manifest entry census mismatch")
    for artifact in (html_id, pdf_id):
        require(
            any(row.get("path") == artifact["path"] and int(row.get("bytes", -1)) == artifact["bytes"] and row.get("sha256") == artifact["sha256"] for row in manifest_rows),
            f"artifact manifest does not bind {artifact['path']}",
        )

    html_text = path(HTML_REL).read_text(encoding="utf-8")
    inv = HtmlInventory()
    inv.feed(html_text)
    lab_ids = [ident for ident in inv.ids if ident.startswith("o012-d60-lab03")]
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
    require(
        "<script src=" not in html_text
        and "<link rel=" not in html_text
        and "pre { max-width: 100%; overflow-x: auto; white-space: pre; }" in html_text
        and "max-width: 58rem;" in html_text
        and "margin: 0 auto;" in html_text
        and "@media (max-width: 700px)" in html_text,
        "HTML self-contained centered/reflowing shell gate failed",
    )

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
    semantic = browser.get("semantic_and_binding_checks", {})
    mobile = browser.get("mobile", {})
    navigation = browser.get("navigation_and_keyboard", {})
    code_scroll = mobile.get("code_blocks_requiring_local_scroll")
    math_scroll = mobile.get("wide_display_math_nodes")
    predecessor_tables = mobile.get("predecessor_wide_table_containers")
    require(
        browser.get("status") == "PASS"
        and browser.get("desktop", {}).get("page_level_horizontal_overflow") is False
        and mobile.get("page_level_horizontal_overflow") is False
        and isinstance(code_scroll, int)
        and code_scroll > 0
        and code_scroll == mobile.get("code_blocks_with_overflow_x_auto")
        and isinstance(math_scroll, int)
        and math_scroll >= 0
        and math_scroll == mobile.get("wide_display_math_nodes_with_overflow_x_auto")
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
        and isinstance(semantic.get("laboratory_mathml_nodes"), int)
        and semantic.get("laboratory_mathml_nodes") > 0
        and semantic.get("document_mathml_nodes") == inv.math_nodes
        and navigation.get("toc_lab03_link_count") == 1
        and navigation.get("toc_lab03_activation") == "PASS"
        and navigation.get("activated_hash") == "#o012-d60-lab03"
        and navigation.get("keyboard_focus", {}).get("status") == "PASS"
        and browser.get("console", {}).get("errors") == browser["console"].get("warnings") == 0
        and browser.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0},
        "browser QA closure mismatch",
    )
    browser_counts = {
        "code_local_scrollers": code_scroll,
        "math_local_scrollers": math_scroll,
        "predecessor_table_local_scrollers": predecessor_tables,
    }
    return identity(VISUAL_REL), identity(RENDER_REL), identity(BROWSER_REL), browser_counts, expected_pages, render_bytes


def main() -> None:
    target = path(TARGET_REL)
    require(not target.exists(), f"refusing to overwrite final receipt: {TARGET_REL}")
    lab, backend, sources = verify_sources_and_backend()
    draft, html_id, pdf_id, manifest_id, inv = verify_reader()
    visual_id, render_id, browser_id, browser_counts, visual_pages, render_bytes = verify_visual_browser(pdf_id["pages"], inv)
    proof = load(PROOF_REL)
    appended_pages = pdf_id["pages"] - PRIOR_PAGES
    receipt = {
        "qa_id": "O012-RBT-001-030-FOM-001-007-CA01-HINTS-R01-R06-CA02-CA03-LAB01-LAB02-LAB03-COMPOSITE-BUILD",
        "status": "PASS",
        "scope": "Roberts 30/30; Fomberg Sections 1.1-1.13; D60-CA01/02/03; ordinary mastery 84/84; solution-bearing mastery 108/108; computation Labs 1-3 complete; Lab 4, proof-metadata closure, and capstone pending",
        "model_provenance": MODEL,
        "deterministic_build_draft": identity(DRAFT_REL),
        "sources": sources,
        "source_execution_review": {"status": lab["status"], "receipt": exact_identity(LAB_QA_REL), "routes": ["D60-R12", "D60-R14"], "tasks": LAB_TASKS, "tests": 6, "stable_ids": LAB_STABLE_IDS, "headings": LAB_HEADINGS, "severity_census": lab["severity_census"]},
        "html": {**html_id, "title": "Topologi Aljabar — Roberts 30/30, Fomberg 1.1–1.13, Asesmen Kumulatif 1–3, dan Laboratorium Komputasi 1–3", "lang": "id-ID", "self_contained": True},
        "pdf": {**pdf_id, "page_size": "A4", "tagged": False},
        "manifest": {**manifest_id, "entries": 2},
        "backend_boundary": {"status": "PASS_APPEND_ONLY_REPLAYABLE", "receipt": exact_identity(BACKEND_REL), "immutable_prefix_records": 7_546, "records_added": 148, "cumulative_records": 7_694, "cumulative_bytes": 9_280_385, "cumulative_bundle_sha256": backend["cumulative"]["bundle_sha256"], "laboratories_complete": 3, "laboratories_required": 4},
        "html_checks": {"status": "PASS", "serialized_dom_ids": len(inv.ids), "live_browser_dom_ids": len(inv.ids) + 1, "fragment_links": len(inv.fragments), "unresolved_fragment_links": 0, "mathml_nodes": inv.math_nodes, "stable_ids_added": LAB_STABLE_IDS, "headings_added": LAB_HEADINGS, "tasks_added": LAB_TASKS, "self_contained": True, "centered_reflow": True},
        "pdf_checks": {"status": "PASS", "pages": pdf_id["pages"], "appended_lab_pages": appended_pages, "bounded_pages_checked": len(visual_pages), "all_bounded_pages_a4_nonempty": True, "fonts": draft["pdf"]["fonts"], "all_fonts_embedded_subset_tounicode": True, "stable_id_destinations_added": LAB_STABLE_IDS, "outline_entries_added": LAB_HEADINGS},
        "reproducibility": {"frozen_inputs_fail_closed": True, "html_clean_writes": 2, "pdf_appendix_clean_builds": 2, "merged_pdf_clean_builds": 2, "merged_pdf_builds_byte_identical": True, "predecessor_html_exact_reconstruction": True, "predecessor_pdf_extracted_text_prefix_identical": True, "predecessor_pdf_pages_structurally_preserved": PRIOR_PAGES, "predecessor_pdf_page_structure_aggregate_sha256": draft["frozen_predecessor"]["pdf_page_structure_aggregate_sha256"], "source_date_epoch": draft["source_date_epoch"]},
        "toolchain": {"builder": exact_identity(BUILDER_REL), "merger": exact_identity(MERGER_REL), "finalizer": identity(FINALIZER_REL), "pandoc": draft["pandoc"], "pypdf": draft["pypdf"], "model_provenance": MODEL},
        "visual_checks": {"status": "PASS", "visual_receipt": visual_id, "render_inventory": render_id, "pages_inspected": visual_pages, "render_count": len(visual_pages), "render_bytes": render_bytes, "severity_census": {"P1": 0, "P2": 0, "P3": 0}},
        "browser_checks": {"status": "PASS", "browser_receipt": browser_id, "desktop": "PASS", "mobile": "PASS", "offline": "PASS", **browser_counts, "unexpected_local_overflow_nodes": 0, "unresolved_fragment_links": 0, "runtime_external_asset_references": 0, "console_errors": 0, "console_warnings": 0, "severity_census": {"P1": 0, "P2": 0, "P3": 0}},
        "remaining": {"computation_labs": ["D60-LAB04"], "proof_metadata_status": proof.get("status"), "capstone": "pending"},
        "limitations": [
            "The composite course remains partial: computation Lab 4, the cross-invariant capstone, and the recorded proof-metadata closure remain.",
            "The PDF remains untagged; the self-contained native-MathML HTML is the primary reflowable surface.",
            "Public-byte readback is a post-publication transaction and is not claimed by this local build receipt.",
        ],
    }
    target.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", **identity(TARGET_REL)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
