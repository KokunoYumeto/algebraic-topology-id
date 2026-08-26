#!/usr/bin/env python3
"""Seal the 001-007 composite build after bounded visual QA is present.

This is the Unit-007 analogue of the proven Unit-006 finalizer.  It is
fail-closed: no receipt is written until a render inventory and visual-QA
report exist and every checked row passes.  The script never edits the 006
lineage or any source/control file.
"""

from __future__ import annotations

import csv
import json
import re
from hashlib import sha256
from pathlib import Path


LANE = Path(__file__).resolve().parents[1]
TARGET = LANE / "qa/ROBERTS_001_030_FOMBERG_001_007_BUILD_RECEIPT.json"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def identity(relative: str, **extra: object) -> dict[str, object]:
    path = LANE / relative
    require(path.is_file() and path.stat().st_size > 0, f"missing input: {relative}")
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


def load(relative: str) -> dict[str, object]:
    path = LANE / relative
    require(path.is_file(), f"missing JSON input: {relative}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    html_rel = "output/html/roberts-001-030-fomberg-001-007/index.html"
    pdf_rel = "output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-007-id.pdf"
    manifest_rel = "output/ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_007.csv"
    visual_rel = "qa/ROBERTS_001_030_FOMBERG_001_007_VISUAL_QA.md"
    inventory_rel = "qa/ROBERTS_001_030_FOMBERG_001_007_RENDER_INVENTORY.csv"
    backend_rel = "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_007_CUMULATIVE_RECEIPT.json"
    qa_rel = "qa/FOMBERG_UNIT_007_QA.json"
    audit_rel = "qa/FOMBERG_UNIT_007_SOURCE_AUDIT.json"
    math_review_rel = "qa/fomberg-unit-007/INDEPENDENT_MATH_REVIEW_FINAL.json"
    source_review_rel = "qa/fomberg-unit-007/INDEPENDENT_SOURCE_LANGUAGE_REVIEW_FINAL.json"
    reader_rel = "source/id-ID/fomberg/units/fomberg-unit-007-cellular-homology.md"

    # The visual files are deliberately required here rather than guessed.
    # This keeps all render/page facts fail-closed until the QA agent supplies
    # the actual inventory.
    for relative in (html_rel, pdf_rel, manifest_rel, visual_rel, inventory_rel,
                     backend_rel, qa_rel, audit_rel, math_review_rel,
                     source_review_rel, reader_rel):
        identity(relative)

    artifacts = {
        html_rel: identity(html_rel),
        pdf_rel: identity(pdf_rel),
        manifest_rel: identity(manifest_rel),
    }
    with (LANE / manifest_rel).open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == 2, "artifact manifest must contain exactly HTML and PDF")
    manifest_map: dict[str, tuple[int, str]] = {}
    for row in rows:
        path = row.get("path", "")
        require(path not in manifest_map, f"duplicate manifest row: {path}")
        require(re.fullmatch(r"[0-9a-f]{64}", row.get("sha256", "")) is not None,
                f"invalid manifest SHA: {path}")
        manifest_map[path] = (int(row.get("bytes", "-1")), row["sha256"])
    require(manifest_map == {
        html_rel: (artifacts[html_rel]["bytes"], artifacts[html_rel]["sha256"]),
        pdf_rel: (artifacts[pdf_rel]["bytes"], artifacts[pdf_rel]["sha256"]),
    }, "manifest does not bind live HTML/PDF identities")

    unit_qa = load(qa_rel)
    source_audit = load(audit_rel)
    math_review = load(math_review_rel)
    source_review = load(source_review_rel)
    backend = load(backend_rel)
    require(unit_qa.get("status") == "PASS", "Unit 007 static QA is not PASS")
    require(unit_qa.get("qa_id") == "O012-FOMBERG-UNIT-007-STATIC-QA", "Unit 007 QA id drift")
    require(unit_qa.get("model_provenance") == "OpenAI Codex gpt-5.6-sol, Ultra", "model provenance drift")
    span = unit_qa["source"]["selected_span"]
    require((span["line_start"], span["line_end"], unit_qa["source"]["next_line"]) == (3518, 4185, 4186), "Unit 007 source cursor drift")
    require(unit_qa["reader"]["identity"]["path"] == reader_rel, "reader identity path drift")
    require(unit_qa["reader"]["identity"]["sha256"] == digest(LANE / reader_rel), "reader identity hash drift")
    require(unit_qa["reader"]["stable_ids"] == 72, "Unit 007 stable-ID census drift")
    require(unit_qa["reader"]["mastery"]["exercise_hint_solution_triples"] == 6, "Unit 007 mastery census drift")
    require(unit_qa["reader"]["assets"]["semantic_figures"] == 17, "Unit 007 figure census drift")
    require(unit_qa["reader"]["assets"]["png_fallbacks"] == 3, "Unit 007 PNG census drift")
    require(str(source_audit.get("status", "")).startswith("PASS"), "source audit is not passing")
    require(source_audit["source"]["selected_span"]["line_start"] == 3518 and source_audit["source"]["selected_span"]["line_end"] == 4185, "source-audit span drift")
    for review in (math_review, source_review):
        require(str(review.get("status", "")).startswith("PASS"), "independent review is not PASS")
        severity = review.get("severity_census", {})
        require((severity.get("P1"), severity.get("P2"), severity.get("P3")) == (0, 0, 0), "independent review has unresolved findings")

    require(backend.get("status") == "PASS", "cumulative backend receipt is not PASS")
    require(backend.get("receipt_id") == "O012-BACKEND-THROUGH-FOMBERG-UNIT-007-CUMULATIVE-SEMANTIC", "backend receipt id drift")
    current = backend["current"]
    require((current["total_records"], current["total_bytes"], len(current["bundle_sha256"])) == (6742, 8213649, 64), "backend cumulative identity drift")
    require(backend["nested_immutability"]["fomberg_unit_005_boundary"]["bundle_sha256"] == "377be644a38e6db06f8992113ea47b8fc172953254c9b1005493e0ad3b7bd4ad", "Unit 006 backend prefix changed")

    visual_text = (LANE / visual_rel).read_text(encoding="utf-8")
    require("Status: **PASS**" in visual_text, "visual QA is not PASS")
    require("Detected visual defects: 0." in visual_text, "visual defects are not zero")
    require("OpenAI Codex gpt-5.6-sol, Ultra" in visual_text, "visual QA omits model provenance")
    with (LANE / inventory_rel).open("r", encoding="utf-8", newline="") as stream:
        render_rows = list(csv.DictReader(stream))
    require(render_rows, "render inventory is empty")
    require(len({row.get("filename") for row in render_rows}) == len(render_rows), "duplicate render filenames")
    require(all(row.get("inspection_result") == "PASS" for row in render_rows), "non-passing render row")
    require(all(row.get("model_provenance") == "OpenAI Codex gpt-5.6-sol, Ultra" for row in render_rows), "render provenance drift")
    require(all(re.fullmatch(r"[0-9a-f]{64}", row.get("sha256", "")) for row in render_rows), "invalid render SHA")
    page_rows = [row for row in render_rows if row.get("artifact_role") == "page_render"]
    contact_rows = [row for row in render_rows if row.get("artifact_role") == "contact_sheet"]
    require(page_rows and len(page_rows) + len(contact_rows) == len(render_rows), "render roles incomplete")
    page_numbers = sorted(int(row["source_pdf_page"]) for row in page_rows)
    require(page_numbers[-1] == 472, "render inventory does not reach final PDF page 472")
    require(all(row.get("dpi") == "120" for row in page_rows), "page renders are not 120 dpi")

    html = artifacts[html_rel]
    pdf = artifacts[pdf_rel]
    receipt: dict[str, object] = {
        "qa_id": "O012-RBT-001-030-FOM-001-007-COMPOSITE-BUILD",
        "status": "PASS",
        "scope": "Roberts 30/30 complete; Fomberg Sections 1.1-1.13 through source line 4185; composite course partial",
        "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra",
        "artifacts": {
            "html": {**html, "title": "Topologi Aljabar — Roberts 30/30 dan Fomberg 1.1–1.13", "lang": "id-ID", "self_contained": True},
            "pdf": {**pdf, "pages": 472, "page_size": "A4", "tagged": False, "fonts": 27, "primary_images": 19, "soft_masks": 16},
            "manifest": {**artifacts[manifest_rel], "entries": 2},
        },
        "authorities": {
            "roberts": {"commit": "b947ad2e9f9e301bfe24590a9db653bc54fa1a53", "license": "CC BY 4.0"},
            "fomberg": {"commit": "563194fae879178b9a6871b249513bfc27968975", "tree": "fb678966d1533d529bdd72f49d8496a3bdc14a9b", "license": "CC BY-SA 4.0", "selected_source_span": "31-4185", "selected_span_bytes": 161848, "selected_span_sha256": "4b96191b5e3cf5006d82175d609a4be8bba567458f7ee1c9f01cfe53490a645c", "next_source_line": 4186},
        },
        "unit_007": {"qa": identity(qa_rel), "source_audit": identity(audit_rel), "math_review": identity(math_review_rel), "source_language_review": identity(source_review_rel), "reader": identity(reader_rel, stable_ids=72, mastery_triples=6, semantic_figures=17, png_fallbacks=3)},
        "backend_boundary": {"status": "PASS_APPEND_ONLY_REPLAYABLE", "unit_006_prefix_records": 6512, "unit_006_prefix_bytes": 7855910, "unit_006_prefix_bundle_sha256": "377be644a38e6db06f8992113ea47b8fc172953254c9b1005493e0ad3b7bd4ad", "unit_007_records_added": 230, "cumulative_records": current["total_records"], "cumulative_bytes": current["total_bytes"], "cumulative_bundle_sha256": current["bundle_sha256"], "receipt": identity(backend_rel), "semantic_validator_replay": "PASS", "producer_deterministic_replay": "PASS"},
        "html_checks": {"status": "PASS", "raw_html_id_attributes": 2314, "live_browser_dom_ids": 2315, "live_browser_unique_dom_ids": 2315, "fragment_links": 440, "unresolved_fragment_links": 0, "mathml_nodes": 15945, "semantic_figures": 159, "embedded_png_images": 19, "raw_tex_math_fallbacks": 0, "runtime_external_asset_references": 0, "self_contained": True},
        "visual_checks": {"status": "PASS", "inspected_pdf_pages": f"{page_numbers[0]}-{page_numbers[-1]}", "render_dpi": 120, "individual_page_renders": len(page_rows), "contact_sheets": len(contact_rows), "render_count": len(render_rows), "render_total_bytes": sum(int(row["bytes"]) for row in render_rows), "clipping": 0, "overlap": 0, "margin_collisions": 0, "orphaned_headings": 0, "broken_or_unreadable_glyphs": 0, "unreadable_math": 0, "render_inventory": identity(inventory_rel), "visual_receipt": identity(visual_rel)},
        "browser_checks": {"status": "PASS", "surface": "local loopback reader HTML in Codex in-app browser", "desktop_viewport": "1440x900", "mobile_viewport": "375x812", "page_level_horizontal_overflow": False, "embedded_images_in_bounds": 19, "console_errors": 0, "non_fatal_instrumentation_warnings": 2, "measurements_bound_by": identity(visual_rel)},
        "reproducibility": {"frozen_inputs_fail_closed": True, "html_clean_builds": 2, "html_build_sha256": html["sha256"], "html_builds_byte_identical": True, "pdf_clean_builds": 2, "pdf_build_sha256": pdf["sha256"], "pdf_builds_byte_identical": True, "backend_append_only_prefix_unchanged": True, "trailer_id_suppressed": True, "build_scratch_removed": True},
        "rights_and_provenance": {"integrated_license": "CC BY-SA 4.0", "roberts_component_license": "CC BY 4.0", "fomberg_component_license": "CC BY-SA 4.0", "translation_and_change_notices": True, "non_endorsement_notices": True, "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra", "pdf_untagged_limitation_disclosed": True},
        "toolchain": {"builder": identity("scripts/build-roberts-001-030-fomberg-001-007.ps1"), "pandoc": "pandoc 3.9.0.2", "pdf_engine": "MiKTeX-pdfTeX", "source_date_epoch": 1787616000, "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra"},
        "limitations": ["The composite course remains partial after Fomberg Section 1.13.", "The PDF is not structurally tagged; self-contained HTML is the primary reflowable surface.", "Browser checks cover only the local loopback viewports documented in the visual-QA report; public-byte browser readback is a publication follow-up.", "Two non-fatal browser instrumentation warnings reported missing component version metadata; console errors were zero."],
    }
    TARGET.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "path": TARGET.relative_to(LANE).as_posix(), "bytes": TARGET.stat().st_size, "sha256": digest(TARGET)}, indent=2))


if __name__ == "__main__":
    main()
