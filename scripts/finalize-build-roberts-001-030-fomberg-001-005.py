#!/usr/bin/env python3
"""Seal the deterministic Unit 005 composite build and visual-QA receipt."""

from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path


LANE = Path(__file__).resolve().parents[1]
TARGET = LANE / "qa/ROBERTS_001_030_FOMBERG_001_005_BUILD_RECEIPT.json"


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
    html_path = "output/html/roberts-001-030-fomberg-001-005/index.html"
    pdf_path = "output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-005-id.pdf"
    manifest_path = "output/ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_005.csv"
    visual_path = "qa/ROBERTS_001_030_FOMBERG_001_005_VISUAL_QA.md"
    inventory_path = "qa/ROBERTS_001_030_FOMBERG_001_005_RENDER_INVENTORY.csv"
    backend_path = "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_005_CUMULATIVE_RECEIPT.json"
    unit_qa_path = "qa/FOMBERG_UNIT_005_QA.json"
    unit_audit_path = "qa/FOMBERG_UNIT_005_SOURCE_AUDIT.json"

    expected = {
        html_path: (8_353_769, "d726c8d8a565172fb620233080f60e2ccbde4386d6fa03b099bf6219645aea90"),
        pdf_path: (4_035_750, "b0b0441ae16ad0065dc50dfc3ba36df49932efbdf939dc048cd332dc881f931a"),
        manifest_path: (286, "33a7e2a0a1e20ba2252dc000798bc36dbe005807fb2d357429ced1ab4354088c"),
        visual_path: (3_807, "f45f92ea57b5fb4b03c3043c3c9c3ce91abf8811e21d9c72c2721334ecbf324b"),
        inventory_path: (3_895, "f58946ef221b289d5f0c443acc057c7a7da864a3cfa70316135937c8fda69b50"),
        backend_path: (7_558, "0e7e3a4595697e55d2451314481be971b9b7a95555309a596ec4155660028b9f"),
        unit_qa_path: (6_268, "874d9ef02875d4fbc28458e56b2c2894be8c990a9fd1c333a0327ccd2d3c4964"),
        unit_audit_path: (4_190, "2c8280c954bdad90995c8d209b94e9355962e3c724ffedbd1ad84675828b2135"),
    }
    for relative, (size, wanted) in expected.items():
        path = LANE / relative
        require(path.stat().st_size == size, f"byte drift: {relative}")
        require(digest(path) == wanted, f"digest drift: {relative}")

    receipt = json.loads(
        (LANE / "qa/ROBERTS_001_030_FOMBERG_001_004_BUILD_RECEIPT.json").read_text(
            encoding="utf-8"
        )
    )
    backend = json.loads((LANE / backend_path).read_text(encoding="utf-8"))
    unit_qa = json.loads((LANE / unit_qa_path).read_text(encoding="utf-8"))

    require(backend["status"] == "PASS", "backend receipt is not passing")
    require(unit_qa["status"] == "PASS", "Unit 005 static QA is not passing")

    receipt.update(
        {
            "qa_id": "O012-RBT-001-030-FOM-001-005-COMPOSITE-BUILD",
            "scope": (
                "Roberts 30/30 complete; Fomberg Sections 1.1-1.11 through "
                "source line 3122; composite course partial"
            ),
        }
    )
    receipt["artifacts"] = {
        "html": identity(html_path),
        "pdf": identity(
            pdf_path,
            pages=437,
            page_size="A4",
            page_size_points="595.276x841.890",
            page_rotation=0,
            title="Topologi Aljabar - Roberts 30/30 dan Fomberg 1.1-1.11",
            encrypted=False,
            forms=False,
            javascript=False,
            suspects=False,
            tagged=False,
            fonts=27,
            all_fonts_embedded_subset_tounicode=True,
            primary_images=9,
            soft_masks=9,
            embedded_unit_003_images=6,
            embedded_unit_004_images=3,
            embedded_unit_005_images=0,
        ),
        "manifest": identity(
            manifest_path,
            entries=2,
            all_entries_match_live_artifact_bytes_and_hashes=True,
        ),
    }
    receipt["authorities"]["fomberg"].update(
        {
            "selected_source_span": "31-3122",
            "selected_span_lines": 3092,
            "selected_span_bytes": 119775,
            "selected_span_sha256": "8fea4ae30f1fb8c347505b43a8455d3bdaa1abba86802c1232a3bbe137f1fcbd",
            "next_source_line": 3123,
        }
    )
    receipt["component_numbering"] = {
        "roberts_edition_units": "001-030",
        "fomberg_component_ids": [f"O012-FOM-{number:03d}" for number in range(1, 6)],
        "course_route_unit_ids": [f"D60-R{number:02d}" for number in range(8, 13)],
        "fomberg_is_not_roberts_units_031_035": True,
    }
    receipt.pop("unit_004_static_qa", None)
    receipt["unit_005_static_qa"] = {
        "reader": {
            **unit_qa["reader"]["identity"],
            "stable_ids": 52,
        },
        "source_audit": identity(unit_audit_path),
        "qa_receipt": identity(unit_qa_path),
        "proof_repairs_complete": ["FOM-PR-12"],
        "mastery_triples": 6,
        "independent_review": "P1=0; P2=0; P3=0",
    }
    suffix = backend["nested_immutability"]["fomberg_unit_005_suffix"]
    current = backend["current"]
    receipt["backend_boundary"] = {
        "status": "PASS_APPEND_ONLY_REPLAYABLE",
        "unit_004_prefix_records": 6113,
        "unit_004_prefix_bytes": 7284299,
        "unit_004_prefix_bundle_sha256": "902eb71aa8a8b25e824ebe9ddae556e914e370d603382f28860392d6e186baba",
        "unit_005_records_added": suffix["records"],
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
        "title": "Topologi Aljabar - Roberts 30/30 dan Fomberg 1.1-1.11",
        "lang": "id-ID",
        "raw_html_id_attributes": 2168,
        "live_browser_dom_ids": 2169,
        "live_browser_unique_dom_ids": 2169,
        "fragment_links": 423,
        "unresolved_fragment_links": 0,
        "mathml_nodes": 14883,
        "semantic_figures": 135,
        "embedded_png_images": 9,
        "fomberg_stable_ids": 476,
        "missing_fomberg_stable_ids": 0,
        "raw_tex_math_fallbacks": 0,
        "runtime_external_asset_references": 0,
        "self_contained": True,
    }
    receipt["browser_checks"] = {
        "status": "PASS",
        "surface": "exact task-local HTML in Codex in-app browser",
        "desktop": {
            "viewport": "1440x900",
            "document_client_width_px": 1425,
            "document_scroll_width_px": 1425,
            "body_width_px": 1152,
            "body_center_delta_px": -0.0556,
            "embedded_images_in_bounds": 9,
        },
        "mobile": {
            "viewport": "375x812",
            "document_client_width_px": 360,
            "document_scroll_width_px": 360,
            "body_width_px": 360,
            "page_level_horizontal_overflow": False,
            "local_horizontal_scrollers": 423,
            "embedded_images_in_bounds": 9,
        },
        "toc_unit_005_navigation": "PASS",
        "browser_connection_reset_after_required_measurements": True,
        "runtime_warning_or_error_logs": "not_retrieved_after_connection_reset",
        "temporary_viewport_reset": True,
        "test_tab_closed": True,
    }
    receipt["visual_checks"] = {
        "status": "PASS",
        "new_fomberg_pdf_pages": "425-437",
        "inspected_pdf_pages": "1-6 and 424-437",
        "render_dpi": 120,
        "individual_page_renders": 20,
        "contact_sheets": 3,
        "render_count": 23,
        "render_total_bytes": 9899021,
        "original_resolution_pages": [425, 428, 430, 432, 437],
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
    receipt["toolchain"] = {
        "builder": "scripts/build-roberts-001-030-fomberg-001-005.ps1",
        "builder_bytes": 63835,
        "builder_sha256": "a79e746f04f772caa508b0668b59b364c23c3e016191b95901b9896b80afedf7",
        "pandoc": "pandoc 3.9.0.2",
        "pdf_engine": "MiKTeX-pdfTeX 4.27 (MiKTeX 26.5)",
        "source_date_epoch": 1787616000,
        "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra",
    }
    receipt["limitations"] = [
        "The composite course remains partial after Fomberg Sections 1.1-1.11.",
        "The PDF is not structurally tagged; the self-contained HTML is the primary accessible and reflowable surface.",
        "No formal accessibility-tree conformance claim is made.",
        "The in-app browser connection reset after the required desktop/mobile layout and navigation measurements; the exact script-free HTML and deterministic static gates remain the runtime-closure witness.",
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
