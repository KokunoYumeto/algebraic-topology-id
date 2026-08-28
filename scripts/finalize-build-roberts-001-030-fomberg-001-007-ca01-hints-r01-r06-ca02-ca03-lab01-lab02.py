#!/usr/bin/env python3
"""Finalize the deterministic Lab 2 reader after visual and browser QA.

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
TOKEN = "ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02"
SLUG = "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"

DRAFT_REL = f"qa/{TOKEN}_BUILD_DRAFT.json"
TARGET_REL = f"qa/{TOKEN}_BUILD_RECEIPT.json"
VISUAL_REL = f"qa/{TOKEN}_VISUAL_QA.md"
RENDER_REL = f"qa/{TOKEN}_RENDER_INVENTORY.csv"
BROWSER_REL = f"qa/{TOKEN}_BROWSER_QA.json"
HTML_REL = f"output/html/{SLUG}/index.html"
PDF_REL = f"output/pdf/topologi-aljabar-{SLUG}-id.pdf"
MANIFEST_REL = f"output/ARTIFACT_MANIFEST_{TOKEN}.csv"
LAB_QA_REL = "qa/COMPUTATION_LAB_002_QA.json"
BACKEND_REL = "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_002_CUMULATIVE_RECEIPT.json"
PROOF_REL = "qa/PROOF_REPAIR_CENSUS.json"
BUILDER_REL = f"scripts/build-{SLUG}.py"
MERGER_REL = "scripts/merge-computation-lab-002.py"
FINALIZER_REL = f"scripts/finalize-build-{SLUG}.py"
RENDER_DIR_REL = "tmp/pdfs/lab02-visual-qa"

EXPECTED = {
    DRAFT_REL: (41_482, "6eefc53da04fdcde37a29baf93814234fa46abff770ab5532279dd5fc340217b"),
    HTML_REL: (15_615_104, "d0c6afddfa92759d475258bf08f20ea4019eccf72b7554128b2b938bd247b375"),
    PDF_REL: (9_507_127, "1bad03f9ba031ba91967a0a0ac2af6d15a0f768882cd541fe26dcbe26c4edd0b"),
    MANIFEST_REL: (369, "11d45714eddfecfc63a6d660f1dedac99a3ecf3d5fb36dc19961e34fb26c137c"),
    LAB_QA_REL: (4_318, "c084e575a621906ac7d8a1c6dca6f604de99b8e58a788409be17bb7392dd4319"),
    BACKEND_REL: (10_039, "8c37c03b59ba638bb7c9533f4078cd75b5500bfaa408e8b816a5bef1b5bc522b"),
    "source/id-ID/labs/computation-lab-002-chain-matrices-smith-normal-form.md": (16_529, "532a1e4dacbfb33b680fbe7251accfc16fda933ed7f49f41e836fec15e096b5b"),
    "source/id-ID/labs/o012_d60_lab02_smith_normal_form.py": (22_052, "47735d76fb1c979d78daaa068a9a32f807ebb234c2da3e5e597f75861e27ae3c"),
    "source/id-ID/labs/test_o012_d60_lab02_smith_normal_form.py": (7_891, "475872356d92f3f439ab353602c293b94db2324fe42209d30f2be6e51b13e2dc"),
    "source/id-ID/labs/expected-output-lab02.txt": (795, "965994efd39713b7591d43fab5d02bb43d200b68e67c4fa98a5b534452bb537c"),
    BUILDER_REL: (31_810, "82d881b9bd9ab6776a240c6df1b9fbdbecc584e033722c55807329a376c78164"),
    MERGER_REL: (9_480, "5b21c3598e5b2978ddd50f7de5926056011dd34f8e2d49b1f8c4eeb2411b3e88"),
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
    source_rels = [
        "source/id-ID/labs/computation-lab-002-chain-matrices-smith-normal-form.md",
        "source/id-ID/labs/o012_d60_lab02_smith_normal_form.py",
        "source/id-ID/labs/test_o012_d60_lab02_smith_normal_form.py",
        "source/id-ID/labs/expected-output-lab02.txt",
    ]
    sources = [exact_identity(rel) for rel in source_rels]
    lab = load(LAB_QA_REL)
    checks = lab.get("checks", {})
    require(
        lab.get("status") == "PASS"
        and lab.get("laboratory_id") == "D60-LAB02"
        and lab.get("edition_unit_id") == "O012-ORIG-LAB02"
        and lab.get("course_route_unit_ids") == ["D60-R08"]
        and lab.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0}
        and checks.get("two_test_runs_6_of_6") == "PASS"
        and checks.get("two_program_runs_byte_identical") == "PASS"
        and checks.get("expected_output_exact") == "PASS"
        and checks.get("independent_code") == "PASS"
        and checks.get("independent_mathematics") == "PASS"
        and checks.get("independent_source_language") == "PASS"
        and checks.get("stable_ids_25_unique") == "PASS"
        and checks.get("tasks_6_with_hint_and_complete_solution") == "PASS"
        and checks.get("rights_origin_provenance_non_endorsement") == "PASS",
        "Lab 2 source/execution/review closure mismatch",
    )
    for expected in sources:
        require(
            any(all(row.get(k) == expected[k] for k in ("path", "bytes", "sha256")) for row in lab["inputs"]),
            f"Lab QA does not bind {expected['path']}",
        )
    backend = load(BACKEND_REL)
    prefix, delta, final = backend.get("immutable_prefix", {}), backend.get("delta", {}), backend.get("cumulative", {})
    require(
        backend.get("status") == "PASS"
        and prefix.get("preserved_exactly") is True
        and (prefix.get("records"), prefix.get("bytes"), prefix.get("bundle_sha256")) == (7_404, 8_975_700, "4740eb2ff83b4f9df3c0d90c2426ff77e652b23cad0bbe7763c54ebdefa60b4b")
        and (delta.get("records"), delta.get("bytes"), delta.get("bundle_sha256")) == (142, 147_055, "48ea786c4275faed1a92e7906a68fe70151c725cb1e2d7c8e636d57dd661652c")
        and (final.get("records"), final.get("bytes"), final.get("bundle_sha256")) == (7_546, 9_122_755, "ac3a0377861ed2b728f9c7473579fdd4febe43e454a92f3ea06451e13d46c8f8")
        and final.get("computation_laboratories_complete") == 2
        and final.get("computation_laboratories_required") == 4
        and backend.get("replay", {}).get("status") == "PASS"
        and backend.get("semantic_checks", {}).get("append_only_ready") == "PASS",
        "Lab 2 append-only backend closure mismatch",
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
    require(draft["html"].get("dom_ids") == 3_632 and draft["html"].get("fragment_links") == 1_640 and draft["html"].get("stable_ids_added") == 25 and draft["html"].get("tasks_added") == 6, "draft HTML census mismatch")
    require(draft["pdf"].get("pages") == 529 and draft["pdf"].get("appendix_pages") == 18 and draft["pdf"].get("stable_id_destinations_added") == 25 and draft["pdf"].get("outline_entries_added") == 18, "draft PDF census mismatch")
    require(draft["pdf"].get("outline_entries") == 451 and draft["pdf"].get("named_destinations") == 3_105 and draft["pdf"].get("fonts") == 109, "draft PDF structure census mismatch")
    require(draft["pdf"].get("all_fonts_embedded_subset_tounicode") is True and draft["pdf"].get("trailer_id_suppressed") is True and draft["pdf"].get("deterministic_appendix_builds") == draft["pdf"].get("deterministic_merged_builds") == 2, "draft reproducibility/font gate failed")
    frozen = draft.get("frozen_predecessor", {})
    require(frozen.get("pdf_pages") == 511 and frozen.get("html_exact_reconstruction") is True and frozen.get("pdf_extracted_text_prefix_identical") is True and frozen.get("pdf_outline_exact_prefix") is True and frozen.get("pdf_named_destinations_preserved") is True and frozen.get("pdf_page_structure_aggregate_sha256") == "6b9e38839e919de425f3e333e0ee24d1c9284a2f1ac682afefbb1845369ffe9a", "frozen predecessor proof mismatch")
    html_text = path(HTML_REL).read_text(encoding="utf-8")
    inv = HtmlInventory()
    inv.feed(html_text)
    require(len(inv.ids) == len(set(inv.ids)) == 3_632 and len(inv.fragments) == 1_640 and not (set(inv.fragments) - set(inv.ids)) and inv.math_nodes == 17_155, "serialized HTML ID/link/MathML gate failed")
    require("<script src=" not in html_text and "<link rel=" not in html_text, "HTML is not self-contained")
    reader = PdfReader(str(path(PDF_REL)))
    require(len(reader.pages) == 529, "live PDF page count mismatch")
    for page_number in range(510, 529):
        page = reader.pages[page_number]
        require(abs(float(page.mediabox.width) - 595.276) < 0.5 and abs(float(page.mediabox.height) - 841.89) < 0.5, f"non-A4 page: {page_number + 1}")
        require((page.extract_text() or "").strip(), f"empty page: {page_number + 1}")
    return draft, html_id, {**pdf_id, "pages": 529}, manifest_id, inv.math_nodes


def verify_visual_browser() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
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
    require([int(row["physical_page"]) for row in rows] == list(range(511, 530)), "render page sequence mismatch")
    require(len(rows) == 19 and sum(int(row["bytes"]) for row in rows) == 4_686_166, "render inventory count/bytes mismatch")
    require(all(row["visual_status"] == "PASS" and row["retained_after_qa"] == "false" for row in rows), "render disposition mismatch")
    for row in rows:
        render = path(f"{RENDER_DIR_REL}/{row['render_file']}")
        require(render.is_file() and render.stat().st_size == int(row["bytes"]) and digest(render) == row["sha256"], f"render identity mismatch: {row['render_file']}")
    browser = load(BROWSER_REL)
    bind(browser.get("artifact", {}), exact_identity(HTML_REL), "browser HTML")
    semantic = browser.get("semantic_and_binding_checks", {})
    mobile = browser.get("mobile", {})
    navigation = browser.get("navigation_and_keyboard", {})
    require(
        browser.get("status") == "PASS"
        and browser.get("desktop", {}).get("page_level_horizontal_overflow") is False
        and mobile.get("page_level_horizontal_overflow") is False
        and mobile.get("code_blocks_requiring_local_scroll") == mobile.get("code_blocks_with_overflow_x_auto") == 4
        and mobile.get("wide_display_math_nodes") == mobile.get("wide_display_math_nodes_with_overflow_x_auto") == 3
        and mobile.get("predecessor_wide_table_containers") == mobile.get("predecessor_wide_table_containers_with_overflow_x_auto") == 1
        and mobile.get("unexpected_local_overflow_nodes") == 0
        and semantic.get("serialized_dom_ids") == 3_632
        and semantic.get("live_browser_dom_ids") == 3_633
        and semantic.get("duplicate_live_dom_ids") == 0
        and semantic.get("fragment_links") == 1_640
        and semantic.get("unresolved_fragment_links") == 0
        and semantic.get("runtime_external_asset_references") == 0
        and semantic.get("laboratory_stable_ids") == 25
        and semantic.get("laboratory_root_plus_stable_ids") == 26
        and semantic.get("laboratory_tasks") == 6
        and semantic.get("laboratory_mathml_nodes") == 83
        and semantic.get("document_mathml_nodes") == 17_155
        and navigation.get("toc_lab02_link_count") == 1
        and navigation.get("toc_lab02_activation") == "PASS"
        and navigation.get("activated_hash") == "#o012-d60-lab02"
        and navigation.get("keyboard_focus", {}).get("status") == "PASS"
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
        "qa_id": "O012-RBT-001-030-FOM-001-007-CA01-HINTS-R01-R06-CA02-CA03-LAB01-LAB02-COMPOSITE-BUILD",
        "status": "PASS",
        "scope": "Roberts 30/30; Fomberg Sections 1.1-1.13; D60-CA01/02/03; ordinary mastery 84/84; solution-bearing mastery 108/108; computation Labs 1-2 complete; Labs 3-4, proof-metadata closure, and capstone pending",
        "model_provenance": MODEL,
        "deterministic_build_draft": exact_identity(DRAFT_REL),
        "sources": sources,
        "source_execution_review": {"status": lab["status"], "receipt": exact_identity(LAB_QA_REL), "tasks": 6, "tests": 6, "stable_ids": 25, "severity_census": lab["severity_census"]},
        "html": {**html_id, "title": "Topologi Aljabar — Roberts 30/30, Fomberg 1.1–1.13, Asesmen Kumulatif 1–3, dan Laboratorium Komputasi 1–2", "lang": "id-ID", "self_contained": True},
        "pdf": {**pdf_id, "page_size": "A4", "tagged": False},
        "manifest": {**manifest_id, "entries": 2},
        "backend_boundary": {"status": "PASS_APPEND_ONLY_REPLAYABLE", "receipt": exact_identity(BACKEND_REL), "immutable_prefix_records": 7_404, "records_added": 142, "cumulative_records": 7_546, "cumulative_bytes": 9_122_755, "cumulative_bundle_sha256": backend["cumulative"]["bundle_sha256"], "laboratories_complete": 2, "laboratories_required": 4},
        "html_checks": {"status": "PASS", "serialized_dom_ids": 3_632, "live_browser_dom_ids": 3_633, "fragment_links": 1_640, "unresolved_fragment_links": 0, "mathml_nodes": math_nodes, "stable_ids_added": 25, "tasks_added": 6, "self_contained": True, "centered_reflow": True},
        "pdf_checks": {"status": "PASS", "pages": 529, "appended_lab_pages": 18, "bounded_pages_checked": 19, "all_bounded_pages_a4_nonempty": True, "fonts": draft["pdf"]["fonts"], "all_fonts_embedded_subset_tounicode": True, "stable_id_destinations_added": 25, "outline_entries_added": 18},
        "reproducibility": {"frozen_inputs_fail_closed": True, "html_clean_writes": 2, "pdf_appendix_clean_builds": 2, "merged_pdf_clean_builds": 2, "merged_pdf_builds_byte_identical": True, "predecessor_html_exact_reconstruction": True, "predecessor_pdf_extracted_text_prefix_identical": True, "predecessor_pdf_pages_structurally_preserved": 511, "predecessor_pdf_page_structure_aggregate_sha256": draft["frozen_predecessor"]["pdf_page_structure_aggregate_sha256"], "source_date_epoch": draft["source_date_epoch"]},
        "toolchain": {"builder": exact_identity(BUILDER_REL), "merger": exact_identity(MERGER_REL), "finalizer": identity(FINALIZER_REL), "pandoc": draft["pandoc"], "pypdf": draft["pypdf"], "model_provenance": MODEL},
        "visual_checks": {"status": "PASS", "visual_receipt": visual_id, "render_inventory": render_id, "pages_inspected": list(range(511, 530)), "render_count": 19, "render_bytes": 4_686_166, "severity_census": {"P1": 0, "P2": 0, "P3": 0}},
        "browser_checks": {"status": "PASS", "browser_receipt": browser_id, "desktop": "PASS", "mobile": "PASS", "offline": "PASS", "code_local_scrollers": 4, "math_local_scrollers": 3, "predecessor_table_local_scrollers": 1, "unexpected_local_overflow_nodes": 0, "unresolved_fragment_links": 0, "runtime_external_asset_references": 0, "console_errors": 0, "console_warnings": 0, "severity_census": {"P1": 0, "P2": 0, "P3": 0}},
        "remaining": {"computation_labs": ["D60-LAB03", "D60-LAB04"], "proof_metadata_status": proof.get("status"), "capstone": "pending"},
        "limitations": [
            "The composite course remains partial: computation Labs 3-4, the cross-invariant capstone, and the recorded proof-metadata closure remain.",
            "The PDF remains untagged; the self-contained native-MathML HTML is the primary reflowable surface.",
            "Public-byte readback is a post-publication transaction and is not claimed by this local build receipt.",
        ],
    }
    target.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", **identity(TARGET_REL)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
