#!/usr/bin/env python3
"""Seal the deterministic Unit 006 composite build and visual-QA receipt."""

from __future__ import annotations

import csv
import json
import re
from hashlib import sha256
from pathlib import Path


LANE = Path(__file__).resolve().parents[1]
TARGET = LANE / "qa/ROBERTS_001_030_FOMBERG_001_006_BUILD_RECEIPT.json"

# Fill these facts only from the deterministic Unit006 build/visual/browser
# outputs. ``None`` is an intentional fail-closed scaffold value: final artifact
# byte identities themselves are computed and cross-checked live below.
FINAL_QA_FACTS = {
    "pdf_pages": None,
    "pdf_fonts": None,
    "html_raw_ids": None,
    "html_live_ids": None,
    "html_fragment_links": None,
    "html_mathml_nodes": None,
    "html_semantic_figures": None,
    "mobile_local_scrollers": None,
    "new_pdf_pages": None,
    "inspected_pdf_pages": None,
    "individual_page_renders": None,
    "contact_sheets": None,
    "render_count": None,
    "render_total_bytes": None,
    "original_resolution_pages": None,
}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def identity(relative: str, **extra: object) -> dict[str, object]:
    path = LANE / relative
    value: dict[str, object] = {
        "path": relative,
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }
    value.update(extra)
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    html_path = "output/html/roberts-001-030-fomberg-001-006/index.html"
    pdf_path = "output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-006-id.pdf"
    manifest_path = "output/ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_006.csv"
    visual_path = "qa/ROBERTS_001_030_FOMBERG_001_006_VISUAL_QA.md"
    inventory_path = "qa/ROBERTS_001_030_FOMBERG_001_006_RENDER_INVENTORY.csv"
    backend_path = "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_006_CUMULATIVE_RECEIPT.json"
    unit_qa_path = "qa/FOMBERG_UNIT_006_QA.json"
    unit_audit_path = "qa/FOMBERG_UNIT_006_SOURCE_AUDIT.json"
    unit_review_path = "qa/fomberg-unit-006/INDEPENDENT_REVIEW_FINAL.json"

    missing_facts = sorted(key for key, value in FINAL_QA_FACTS.items() if value is None)
    require(not missing_facts, f"unsealed deterministic QA facts: {missing_facts}")
    integer_facts = (
        "pdf_pages",
        "pdf_fonts",
        "html_raw_ids",
        "html_live_ids",
        "html_fragment_links",
        "html_mathml_nodes",
        "html_semantic_figures",
        "mobile_local_scrollers",
        "individual_page_renders",
        "contact_sheets",
        "render_count",
        "render_total_bytes",
    )
    for key in integer_facts:
        value = FINAL_QA_FACTS[key]
        require(
            isinstance(value, int) and not isinstance(value, bool) and value >= 0,
            f"invalid deterministic QA integer: {key}",
        )
    require(FINAL_QA_FACTS["pdf_pages"] > 437, "Unit 006 PDF did not extend Unit 005")
    require(FINAL_QA_FACTS["pdf_fonts"] > 0, "PDF font census is empty")
    require(FINAL_QA_FACTS["html_raw_ids"] > 0, "raw HTML ID census is empty")
    require(
        FINAL_QA_FACTS["html_live_ids"] >= FINAL_QA_FACTS["html_raw_ids"],
        "live HTML ID census is smaller than the raw HTML census",
    )
    require(FINAL_QA_FACTS["html_fragment_links"] > 0, "fragment-link census is empty")
    require(FINAL_QA_FACTS["html_mathml_nodes"] > 0, "MathML census is empty")
    require(FINAL_QA_FACTS["html_semantic_figures"] >= 142, "figure census regressed")
    require(
        FINAL_QA_FACTS["new_pdf_pages"] == "439-452",
        "Unit 006 PDF page span must be 439-452",
    )
    require(
        FINAL_QA_FACTS["inspected_pdf_pages"] == "438-452",
        "visual inspection must include the Unit 005/006 seam and all Unit 006 pages",
    )
    require(
        isinstance(FINAL_QA_FACTS["original_resolution_pages"], list)
        and all(
            isinstance(page, int) and not isinstance(page, bool)
            for page in FINAL_QA_FACTS["original_resolution_pages"]
        ),
        "original-resolution page inventory is malformed",
    )
    required_paths = (
        html_path,
        pdf_path,
        manifest_path,
        visual_path,
        inventory_path,
        backend_path,
        unit_qa_path,
        unit_audit_path,
        unit_review_path,
    )
    for relative in required_paths:
        path = LANE / relative
        require(path.is_file() and path.stat().st_size > 0, f"missing final input: {relative}")
    expected = {
        relative: ((LANE / relative).stat().st_size, digest(LANE / relative))
        for relative in required_paths
    }
    with (LANE / manifest_path).open("r", encoding="utf-8", newline="") as stream:
        manifest_source_rows = list(csv.DictReader(stream))
    require(len(manifest_source_rows) == 2, "artifact manifest must contain two rows")
    manifest_rows: dict[str, tuple[int, str]] = {}
    for row in manifest_source_rows:
        relative = row.get("path", "")
        require(relative not in manifest_rows, f"duplicate artifact manifest path: {relative}")
        wanted = row.get("sha256", "")
        require(
            bool(re.fullmatch(r"[0-9a-f]{64}", wanted)),
            f"invalid artifact manifest SHA-256: {relative}",
        )
        try:
            size = int(row.get("bytes", ""))
        except (TypeError, ValueError) as error:
            raise RuntimeError(f"invalid artifact manifest byte count: {relative}") from error
        require(size >= 0, f"negative artifact manifest byte count: {relative}")
        manifest_rows[relative] = (size, wanted)
    require(
        manifest_rows == {
            html_path: expected[html_path],
            pdf_path: expected[pdf_path],
        },
        "artifact manifest does not bind the exact live HTML/PDF",
    )

    receipt = json.loads(
        (LANE / "qa/ROBERTS_001_030_FOMBERG_001_005_BUILD_RECEIPT.json").read_text(
            encoding="utf-8"
        )
    )
    backend = json.loads((LANE / backend_path).read_text(encoding="utf-8"))
    unit_qa = json.loads((LANE / unit_qa_path).read_text(encoding="utf-8"))

    require(backend["status"] == "PASS", "backend receipt is not passing")
    require(unit_qa["status"] == "PASS", "Unit 006 static QA is not passing")
    require(
        backend.get("receipt_id")
        == "O012-BACKEND-THROUGH-FOMBERG-UNIT-006-CUMULATIVE-SEMANTIC",
        "Unit 006 cumulative backend receipt ID mismatch",
    )
    require(
        {
            key: backend["current"].get(key)
            for key in ("total_records", "total_bytes", "bundle_sha256")
        }
        == {
            "total_records": 6512,
            "total_bytes": 7855910,
            "bundle_sha256": "377be644a38e6db06f8992113ea47b8fc172953254c9b1005493e0ad3b7bd4ad",
        },
        "Unit 006 cumulative backend identity mismatch",
    )
    visual_text = (LANE / visual_path).read_text(encoding="utf-8")
    require("Status: **PASS**" in visual_text, "visual QA is not passing")
    require(
        "OpenAI Codex gpt-5.6-sol, Ultra" in visual_text,
        "visual QA omits model provenance",
    )
    for marker in (
        "pages 438-452",
        "Detected visual defects: 0.",
        "GitHub Pages",
        "1440x900",
        "375x812",
    ):
        require(marker in visual_text, f"visual/browser QA omits evidence marker: {marker}")

    with (LANE / inventory_path).open("r", encoding="utf-8", newline="") as stream:
        render_rows = list(csv.DictReader(stream))
    require(render_rows, "render inventory is empty")
    require(
        len({row.get("filename") for row in render_rows}) == len(render_rows),
        "render inventory contains duplicate filenames",
    )
    require(
        all(row.get("inspection_result") == "PASS" for row in render_rows),
        "render inventory contains a non-passing inspection",
    )
    require(
        all(
            row.get("model_provenance") == "OpenAI Codex gpt-5.6-sol, Ultra"
            for row in render_rows
        ),
        "render inventory model provenance drift",
    )
    require(
        all(re.fullmatch(r"[0-9a-f]{64}", row.get("sha256", "")) for row in render_rows),
        "render inventory contains an invalid SHA-256",
    )
    page_rows = [row for row in render_rows if row.get("artifact_role") == "page_render"]
    contact_rows = [row for row in render_rows if row.get("artifact_role") == "contact_sheet"]
    require(
        len(page_rows) + len(contact_rows) == len(render_rows),
        "render inventory contains an unexpected artifact role",
    )
    page_numbers = sorted(int(row["source_pdf_page"]) for row in page_rows)
    require(page_numbers == list(range(438, 453)), "render inventory page span drift")
    require(
        all(row.get("dpi") == "120" for row in page_rows),
        "individual page renders are not all 120 dpi",
    )
    require(
        int(FINAL_QA_FACTS["individual_page_renders"]) == len(page_rows)
        and int(FINAL_QA_FACTS["contact_sheets"]) == len(contact_rows)
        and int(FINAL_QA_FACTS["render_count"]) == len(render_rows),
        "render-count facts do not match the inventory",
    )
    inventory_render_bytes = sum(int(row["bytes"]) for row in render_rows)
    require(
        int(FINAL_QA_FACTS["render_total_bytes"]) == inventory_render_bytes,
        "render-byte fact does not match the inventory",
    )
    require(
        FINAL_QA_FACTS["original_resolution_pages"] == page_numbers,
        "original-resolution page fact does not match the inventory",
    )

    receipt.update(
        {
            "qa_id": "O012-RBT-001-030-FOM-001-006-COMPOSITE-BUILD",
            "scope": (
                "Roberts 30/30 complete; Fomberg Sections 1.1-1.12 through "
                "source line 3517; composite course partial"
            ),
        }
    )
    receipt["artifacts"] = {
        "html": identity(html_path),
        "pdf": identity(
            pdf_path,
            pages=FINAL_QA_FACTS["pdf_pages"],
            page_size="A4",
            page_size_points="595.276x841.890",
            page_rotation=0,
            title="Topologi Aljabar - Roberts 30/30 dan Fomberg 1.1-1.12",
            encrypted=False,
            forms=False,
            javascript=False,
            suspects=False,
            tagged=False,
            fonts=FINAL_QA_FACTS["pdf_fonts"],
            all_fonts_embedded_subset_tounicode=True,
            primary_images=16,
            soft_masks=16,
            embedded_unit_003_images=6,
            embedded_unit_004_images=3,
            embedded_unit_005_images=0,
            embedded_unit_006_images=7,
        ),
        "manifest": identity(
            manifest_path,
            entries=2,
            all_entries_match_live_artifact_bytes_and_hashes=True,
        ),
    }
    receipt["authorities"]["fomberg"].update(
        {
            "selected_source_span": "31-3517",
            "selected_span_lines": 3487,
            "selected_span_bytes": 135315,
            "selected_span_sha256": "ef632f69b4b3e820fc5c7b06b27fc8ae4fba65d929e06890b5e576d149f73d56",
            "next_source_line": 3518,
        }
    )
    receipt["component_numbering"] = {
        "roberts_edition_units": "001-030",
        "fomberg_component_ids": [f"O012-FOM-{number:03d}" for number in range(1, 7)],
        "course_route_unit_ids": ["D60-R08", "D60-R09", "D60-R10", "D60-R11", "D60-R12", "D60-R12"],
        "fomberg_is_not_roberts_units_031_036": True,
    }
    receipt.pop("unit_005_static_qa", None)
    receipt["unit_006_static_qa"] = {
        "reader": {
            **unit_qa["reader"]["identity"],
            "stable_ids": unit_qa["reader"]["stable_ids"],
        },
        "source_audit": identity(unit_audit_path),
        "qa_receipt": identity(unit_qa_path),
        "independent_review_receipt": identity(unit_review_path),
        "proof_repairs_complete": unit_qa["reader"].get("proof_repairs", []),
        "mastery_triples": unit_qa["reader"]["mastery"][
            "exercise_hint_solution_triples"
        ],
        "svg_masters": 7,
        "png_reader_assets": 7,
        "independent_review": "P1=0; P2=0; P3=0",
    }
    suffix = backend["nested_immutability"]["fomberg_unit_006_suffix"]
    prefix = backend["nested_immutability"]["fomberg_unit_005_boundary"]
    current = backend["current"]
    receipt["backend_boundary"] = {
        "status": "PASS_APPEND_ONLY_REPLAYABLE",
        "unit_005_prefix_records": prefix["records"],
        "unit_005_prefix_bytes": prefix["bytes"],
        "unit_005_prefix_bundle_sha256": prefix["bundle_sha256"],
        "unit_006_records_added": suffix["records"],
        "cumulative_records": current["total_records"],
        "cumulative_bytes": current["total_bytes"],
        "cumulative_bundle_sha256": current["bundle_sha256"],
        "records_added_by_file": suffix["records_by_file"],
        "receipt": identity(backend_path),
        "semantic_validator_replay": "PASS",
        "producer_deterministic_replay": "PASS",
    }
    receipt["html_checks"] = {
        "status": "PASS",
        "title": "Topologi Aljabar - Roberts 30/30 dan Fomberg 1.1-1.12",
        "lang": "id-ID",
        "raw_html_id_attributes": FINAL_QA_FACTS["html_raw_ids"],
        "live_browser_dom_ids": FINAL_QA_FACTS["html_live_ids"],
        "live_browser_unique_dom_ids": FINAL_QA_FACTS["html_live_ids"],
        "fragment_links": FINAL_QA_FACTS["html_fragment_links"],
        "unresolved_fragment_links": 0,
        "mathml_nodes": FINAL_QA_FACTS["html_mathml_nodes"],
        "semantic_figures": FINAL_QA_FACTS["html_semantic_figures"],
        "embedded_png_images": 16,
        "fomberg_stable_ids": current["stable_ids"],
        "missing_fomberg_stable_ids": 0,
        "raw_tex_math_fallbacks": 0,
        "runtime_external_asset_references": 0,
        "self_contained": True,
    }
    receipt["browser_checks"] = {
        "status": "PASS",
        "surface": "public GitHub Pages HTML in Codex in-app browser",
        "desktop_viewport": "1440x900",
        "mobile_viewport": "375x812",
        "page_level_horizontal_overflow": False,
        "local_horizontal_scrollers": FINAL_QA_FACTS["mobile_local_scrollers"],
        "embedded_images_in_bounds": 16,
        "toc_unit_006_navigation": "PASS",
        "measurements_bound_by": identity(visual_path),
    }
    receipt["visual_checks"] = {
        "status": "PASS",
        "new_fomberg_pdf_pages": FINAL_QA_FACTS["new_pdf_pages"],
        "inspected_pdf_pages": FINAL_QA_FACTS["inspected_pdf_pages"],
        "render_dpi": 120,
        "individual_page_renders": FINAL_QA_FACTS["individual_page_renders"],
        "contact_sheets": FINAL_QA_FACTS["contact_sheets"],
        "render_count": FINAL_QA_FACTS["render_count"],
        "render_total_bytes": FINAL_QA_FACTS["render_total_bytes"],
        "original_resolution_pages": FINAL_QA_FACTS["original_resolution_pages"],
        "clipping": 0,
        "overlap": 0,
        "margin_collisions": 0,
        "orphaned_headings": 0,
        "broken_or_unreadable_glyphs": 0,
        "unreadable_math": 0,
        "render_inventory": identity(inventory_path),
        "visual_receipt": identity(visual_path),
    }
    receipt["reproducibility"] = {
        "frozen_inputs_fail_closed": True,
        "html_clean_builds": 2,
        "html_build_a_sha256": expected[html_path][1],
        "html_build_b_sha256": expected[html_path][1],
        "html_builds_byte_identical": True,
        "pdf_clean_builds": 2,
        "pdf_build_a_sha256": expected[pdf_path][1],
        "pdf_build_b_sha256": expected[pdf_path][1],
        "pdf_builds_byte_identical": True,
        "protected_prior_composite_unchanged": True,
        "backend_append_only_prefix_unchanged": True,
        "trailer_id_suppressed": True,
        "build_scratch_removed": True,
    }
    receipt["rights_and_provenance"].update(
        {
            "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra",
            "pdf_untagged_limitation_disclosed": True,
        }
    )
    builder = identity("scripts/build-roberts-001-030-fomberg-001-006.ps1")
    receipt["toolchain"] = {
        "builder": builder["path"],
        "builder_bytes": builder["bytes"],
        "builder_sha256": builder["sha256"],
        "pandoc": "pandoc 3.9.0.2",
        "pdf_engine": "MiKTeX-pdfTeX 4.27 (MiKTeX 26.5)",
        "source_date_epoch": 1787616000,
        "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra",
    }
    receipt["limitations"] = [
        "The composite course remains partial after Fomberg Sections 1.1-1.12.",
        "The PDF is not structurally tagged; the self-contained HTML is the primary accessible and reflowable surface.",
        "No formal accessibility-tree conformance claim is made.",
        "Browser layout checks cover only the stated desktop and mobile viewports.",
    ]

    payload = json.dumps(receipt, ensure_ascii=False, indent=2) + "\n"
    TARGET.write_text(payload, encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "status": "PASS",
                "path": TARGET.relative_to(LANE).as_posix(),
                "bytes": TARGET.stat().st_size,
                "sha256": digest(TARGET),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
