#!/usr/bin/env python3
"""Append the verified cumulative Units 001--025 build boundary.

The complete 3,896-record Unit 25 semantic backend is immutable. This
producer verifies that exact prefix and all seven build witnesses before
adding only cumulative artifact, QA, relation, and final-rights records.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
import re
from pathlib import Path
from typing import Any

LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
SCHEMA = "curriculum.interop"
VERSION = "0.1.0"
WORKFLOW = "o012-d60-id-reader-production"
STAMP = "2026-08-24T00:00:00Z"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
ROOT = "unit:o012-rbt-u025"
SOURCE_RIGHTS = "rights:o012-units-001-025-composite-cc-by-4.0"
FINAL_RIGHTS = "rights:o012-units-001-025-composite-cc-by-4.0-final-df72"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX = {
    "artifacts.jsonl": (138, 109709, "bab1f9ba40f5114ad42692947e23c485f59e66d8be22f83690c0784a51d9eb9f"),
    "assets.jsonl": (27, 16679, "aa569a900426a9e2cfd56777f3e52f07b35a1a72f211847bafd71ec638043462"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (325, 102250, "0ce28594cd511c1a20aff74053b7c74c6c4c6a0505c7c8c5804dd7acd2dae77d"),
    "corrections.jsonl": (332, 327054, "40791f1db8da9ba81083bad0bb4ac183094c3151b9007bb34e5fc637a1790893"),
    "qa.jsonl": (117, 66127, "743c34c79a2dde2e8595737821bd9ade984cf9cb8610eede028bcdfaaf25bc3b"),
    "relations.jsonl": (390, 158960, "a21a397f9f29c38b4ac424895a2f7f98ad6b9723e37ec47e1bf7dae213f57182"),
    "rights.jsonl": (70, 64323, "a09f281a39c910c4aaff1e10bbc1536a03f14489f68a98681f218f56ad06c453"),
    "segments.jsonl": (1075, 1428116, "d47404ea94dfa7347fbf6f6e0e0e8c5f4fb60e2634c066b87967a4468fff644a"),
    "terms.jsonl": (318, 197648, "dda9013d863bc39ec81f9936167ad24d0cfa2ebba6de0aa2c768743dc09b8503"),
    "units.jsonl": (1100, 1522772, "7fe9d4abfae9389db7cb99240b553d62b66144086c3f2097e9f64d5b2fe14318"),
}
PREFIX_RECORDS = 3896
PREFIX_BYTES = 3996359
PREFIX_BUNDLE = "55372b9c2853fa479e731c73c407b234ad2f1219e07efbedbad2a99f1e2abf47"
BUILD_ID = "qa:o012-units-001-025-build"
VISUAL_ID = "qa:o012-units-001-025-visual"
MANIFEST_ID = "artifact:o012-units-001-025-manifest"
BUILD_RECEIPT_PATH = "qa/UNITS_001_025_BUILD_RECEIPT.json"
VISUAL_RECEIPT_PATH = "qa/UNITS_001_025_VISUAL_QA.md"
INVENTORY_PATH = "qa/UNITS_001_025_RENDER_INVENTORY.csv"
MANIFEST_PATH = "output/ARTIFACT_MANIFEST_UNITS_001_025.csv"
EXPECTED_PAGES = 298
EXPECTED_RENDER_PAGES = [1, 286, *range(287, 299)]

# ident -> (path, bytes, sha256, media type, state, QA ids, manifest id)
ARTIFACTS: dict[str, tuple[str, int, str, str, str, list[str], str | None]] = {
    "artifact:o012-units-001-025-build-script": (
        "scripts/build-units-001-025.ps1", 21986,
        "d346b18845f8fc9314ae588fc7877d38275110ab23c60f10b7bad649bc3371c2",
        "text/plain; charset=utf-8", "source_frozen", [BUILD_ID], None),
    "artifact:o012-units-001-025-html": (
        "output/html/units-001-025/index.html", 4112563,
        "38cd8437f3b4235ac6269f4e3365123fa06485269d35a424ad4f5ddd589025c1",
        "text/html; charset=utf-8", "built", [BUILD_ID], MANIFEST_ID),
    "artifact:o012-units-001-025-pdf": (
        "output/pdf/topologi-aljabar-unit-001-025-id.pdf", 1972209,
        "581d62162633a6624687517c5cf1595f5fc02a2701c2222b279711e0520b9a3f",
        "application/pdf", "built", [BUILD_ID, VISUAL_ID], MANIFEST_ID),
    MANIFEST_ID: (
        MANIFEST_PATH, 249,
        "37175a8d7023bf394c50c4809122b1f3244b5d0b1b95a3b724bdb2ff184ab142",
        "text/csv; charset=utf-8", "built", [BUILD_ID], None),
    "artifact:o012-units-001-025-build-receipt": (
        BUILD_RECEIPT_PATH, 7729,
        "dd2fa5b52ed84ac939c33cfa5b9f68be4b904b014321abcb54c2ae664d0f9727",
        "application/json", "built", [BUILD_ID], None),
    "artifact:o012-units-001-025-visual-receipt": (
        VISUAL_RECEIPT_PATH, 4804,
        "ae49496b676472f6c69a3468cc76c323c45905ce7ed86a048ce11556079137a3",
        "text/markdown; charset=utf-8", "visually_checked", [VISUAL_ID], None),
    "artifact:o012-units-001-025-render-inventory": (
        INVENTORY_PATH, 2731,
        "a55ff205e621fbc750baaf086fa18883c72dba5bdfe1f66e4554247d22fdc12f",
        "text/csv; charset=utf-8", "visually_checked", [VISUAL_ID], None),
}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8") + b"\n"


def common(kind: str, ident: str) -> dict[str, Any]:
    return {"entity_type": kind, "id": ident, "schema": SCHEMA,
            "schema_version": VERSION, "status": "active", "supersedes": None,
            "timestamp": STAMP, "workflow": WORKFLOW}


def load_generic():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_u025_build", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_artifacts() -> dict[str, Any]:
    for _ident, (relative, size, expected, _media, _state, _qas, _manifest) in ARTIFACTS.items():
        raw = (LANE / relative).read_bytes()
        if len(raw) != size or digest(raw) != expected:
            raise SystemExit(f"cumulative artifact mismatch: {relative}")
    if (LANE / "output/units-001-025-manifest.sha256").exists():
        raise SystemExit("unexpected supplied-path manifest appeared; bind the receipt-declared CSV")
    receipt = json.loads((LANE / BUILD_RECEIPT_PATH).read_text(encoding="utf-8"))
    source = receipt.get("source_authority", {})
    toolchain = receipt.get("toolchain", {})
    reproducibility = receipt.get("reproducibility", {})
    if (receipt.get("status") != "PASS"
            or source.get("cumulative_source_span") != "134-5611"
            or source.get("next_source_line") != 5612
            or source.get("unit_025_span") != "5370-5611"
            or source.get("unit_025_span_bytes") != 12732
            or source.get("unit_025_span_sha256") !=
            "d05781ae58b1b6fd6174d030e52ca9ee6a08048be96f7c103e5be8de473b60b0"
            or source.get("unit_025_sha256") !=
            "df72add4e57236b51ff7d2a0c99af4b65299365874163cb334be5d0988c0f769"
            or toolchain.get("builder_sha256") != ARTIFACTS[
                "artifact:o012-units-001-025-build-script"][2]
            or toolchain.get("model_provenance") != MODEL
            or not reproducibility.get("html_two_builds_byte_identical")
            or not reproducibility.get("pdf_two_builds_byte_identical")
            or not reproducibility.get(
                "source_baseline_authority_and_unit_025_evidence_fail_closed")
            or not reproducibility.get("pandoc_html_warnings_are_fatal")
            or not reproducibility.get(
                "transient_html_macro_normalization_does_not_modify_sources")):
        raise SystemExit("cumulative build receipt binding/reproducibility mismatch")
    declared = receipt.get("artifacts", {})
    for key, ident in {
        "html": "artifact:o012-units-001-025-html",
        "pdf": "artifact:o012-units-001-025-pdf", "manifest": MANIFEST_ID,
    }.items():
        spec = ARTIFACTS[ident]
        if ((declared.get(key, {}).get("path"), declared.get(key, {}).get("bytes"),
             declared.get(key, {}).get("sha256")) != (spec[0], spec[1], spec[2])):
            raise SystemExit(f"build receipt {key} identity mismatch")
    html = receipt.get("html_checks", {})
    pdf = declared.get("pdf", {})
    browser = receipt.get("browser_checks", {})
    if (pdf.get("pages") != EXPECTED_PAGES or pdf.get("unit_025_pages") != "287-298"
            or pdf.get("page_size") != "A4" or pdf.get("catalog_lang") != "id-ID"
            or pdf.get("tagged") is not False
            or not pdf.get("all_fonts_embedded_subset_tounicode")
            or html.get("unique_dom_ids") != 1361
            or html.get("fragment_links") != 296
            or html.get("mathml_nodes") != 10118
            or html.get("semantic_figures") != 62
            or html.get("raw_tex_math_fallbacks") != 0
            or html.get("missing_unit_025_ids") != 0
            or html.get("unit_025_ids") != 59
            or html.get("unresolved_fragment_links") != 0
            or html.get("runtime_external_dependencies") != 0
            or not html.get("responsive_mobile_reflow")
            or browser.get("final_result") != "PASS"
            or browser.get("desktop", {}).get("uncontained_overflow_elements") != 0
            or browser.get("mobile", {}).get("uncontained_overflow_elements") != 0):
        raise SystemExit("cumulative HTML/PDF/browser gate mismatch")
    visual = (LANE / VISUAL_RECEIPT_PATH).read_text(encoding="utf-8")
    if ("Status: **PASS**" not in visual or MODEL not in visual
            or "pages **1, 286, and 287-298**" not in visual
            or "honestly **untagged**" not in visual):
        raise SystemExit("visual receipt is not the expected PASS/page boundary")
    inventory_raw = (LANE / INVENTORY_PATH).read_text(encoding="utf-8-sig")
    inventory_rows = list(csv.DictReader(io.StringIO(inventory_raw)))
    if (not inventory_rows
            or list(inventory_rows[0]) != ["pdf_page", "coverage", "render_name", "dpi",
                                          "width_px", "height_px", "render_bytes",
                                          "render_sha256"]
            or [int(row["pdf_page"]) for row in inventory_rows] != EXPECTED_RENDER_PAGES
            or any((row["dpi"], row["width_px"], row["height_px"]) !=
                   ("144", "1191", "1684") for row in inventory_rows)
            or any(not re.fullmatch(r"[0-9a-f]{64}", row["render_sha256"])
                   for row in inventory_rows)):
        raise SystemExit("render inventory content mismatch")
    manifest = (LANE / MANIFEST_PATH).read_text(encoding="utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(manifest)))
    expected_rows = {
        (ARTIFACTS["artifact:o012-units-001-025-html"][0],
         str(ARTIFACTS["artifact:o012-units-001-025-html"][1]),
         ARTIFACTS["artifact:o012-units-001-025-html"][2]),
        (ARTIFACTS["artifact:o012-units-001-025-pdf"][0],
         str(ARTIFACTS["artifact:o012-units-001-025-pdf"][1]),
         ARTIFACTS["artifact:o012-units-001-025-pdf"][2]),
    }
    if (not rows or list(rows[0]) != ["path", "bytes", "sha256"]
            or {(row["path"], row["bytes"], row["sha256"]) for row in rows} != expected_rows):
        raise SystemExit("cumulative manifest content mismatch")
    return receipt


def main() -> int:
    receipt = verify_artifacts()
    raws: dict[str, bytes] = {}
    tables: dict[str, list[dict[str, Any]]] = {}
    all_ids: set[str] = set()
    bundle = hashlib.sha256()
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        count, size, expected = PREFIX[name]
        lines = raw.splitlines(keepends=True)
        if (len(raw), digest(raw), len(lines)) != (size, expected, count):
            raise SystemExit(f"immutable Unit 25 semantic prefix mismatch: {name}")
        if b"\r" in raw or not raw.endswith(b"\n"):
            raise SystemExit(f"invalid prefix newline form: {name}")
        parsed: list[dict[str, Any]] = []
        for number, line in enumerate(lines, 1):
            obj = json.loads(line.decode("utf-8"))
            if canon(obj) != line or not isinstance(obj.get("id"), str):
                raise SystemExit(f"noncanonical prefix record: {name}:{number}")
            if obj["id"] in all_ids:
                raise SystemExit(f"duplicate prefix ID: {obj['id']}")
            all_ids.add(obj["id"])
            parsed.append(obj)
        raws[name] = raw
        tables[name] = parsed
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(raw)
    if (len(all_ids) != PREFIX_RECORDS
            or sum(len(raw) for raw in raws.values()) != PREFIX_BYTES
            or bundle.hexdigest() != PREFIX_BUNDLE
            or ROOT not in all_ids or SOURCE_RIGHTS not in all_ids):
        raise SystemExit("Unit 25 semantic prefix bundle/root/rights mismatch")

    additions: dict[str, list[dict[str, Any]]] = {name: [] for name in FILES}
    pending: set[str] = set()

    def add(name: str, obj: dict[str, Any]) -> None:
        if obj["id"] in all_ids or obj["id"] in pending:
            raise SystemExit(f"duplicate appended ID: {obj['id']}")
        pending.add(obj["id"])
        additions[name].append(obj)

    rights = common("rights", FINAL_RIGHTS)
    rights.update({
        "attribution": "Cumulative Roberts Units 001-025 Indonesian reader and deterministic build artifacts.",
        "change_notice": "Verified cumulative HTML/PDF build boundary; component-level rights and attribution records remain controlling.",
        "component_scope": [f"unit:o012-rbt-u{number:03d}" for number in range(1, 26)],
        "license_expression": "CC-BY-4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "non_endorsement": "Independent edition; no source-author endorsement.",
        "supersedes": SOURCE_RIGHTS,
        "third_party_status": "Component-scoped rights records control.",
    })
    add("rights.jsonl", rights)
    toolchain = receipt.get("toolchain", {})
    toolchain_note = ("Deterministic Units 001-025 builder; "
                      f"{toolchain.get('pandoc')}; PDF engine {toolchain.get('pdf_engine')}; "
                      f"Poppler {toolchain.get('poppler')}; {MODEL}.")
    for ident, (relative, size, sha, media, state, qas, manifest) in ARTIFACTS.items():
        artifact = common("artifact", ident)
        artifact.update({"bytes": size, "locale": "id-ID",
                         "manifest_artifact_id": manifest, "media_type": media,
                         "path": relative, "qa_event_ids": qas,
                         "rights_component_id": FINAL_RIGHTS, "sha256": sha,
                         "toolchain": toolchain_note, "translation_state": state,
                         "unit_id": ROOT})
        add("artifacts.jsonl", artifact)
    build = common("qa_event", BUILD_ID)
    build.update({
        "note": "Cumulative Units 001-025 HTML and PDF passed fail-closed inputs, two-build byte identity, exact manifest, offline HTML, MathML, fragment, responsive reflow, font, privacy, and source-binding gates.",
        "qa_type": "build", "result": "passed", "unit_id": ROOT,
        "witness_artifact_ids": [
            "artifact:o012-units-001-025-build-script",
            "artifact:o012-units-001-025-html",
            "artifact:o012-units-001-025-pdf", MANIFEST_ID,
            "artifact:o012-units-001-025-build-receipt"],
    })
    add("qa.jsonl", build)
    visual = common("qa_event", VISUAL_ID)
    visual.update({
        "note": "Complete Unit 25 span plus title and transition visual QA passed for the 298-page A4 PDF and responsive HTML; inventory fixes every inspected render identity.",
        "qa_type": "visual", "result": "passed", "unit_id": ROOT,
        "witness_artifact_ids": ["artifact:o012-units-001-025-pdf",
                                 "artifact:o012-units-001-025-visual-receipt",
                                 "artifact:o012-units-001-025-render-inventory"],
    })
    add("qa.jsonl", visual)

    def relation(ident: str, source: str, kind: str, target: str, note: str) -> None:
        record = common("relation", ident)
        record.update({"from_id": source, "note": note,
                       "relation_type": kind, "to_id": target})
        add("relations.jsonl", record)
    relation("relation:boundary:o012-units-001-025-build", FINAL_RIGHTS, "contains",
             "artifact:o012-units-001-025-pdf",
             "Final cumulative Units 001-025 build boundary points to the verified PDF reader.")
    relation("relation:contains:o012-units-001-025-manifest:html", MANIFEST_ID, "contains",
             "artifact:o012-units-001-025-html", "Manifest entry for the cumulative HTML reader.")
    relation("relation:contains:o012-units-001-025-manifest:pdf", MANIFEST_ID, "contains",
             "artifact:o012-units-001-025-pdf", "Manifest entry for the cumulative PDF reader.")
    relation("relation:depends-on:o012-units-001-025-build:builder", BUILD_ID, "depends-on",
             "artifact:o012-units-001-025-build-script",
             "The cumulative build QA depends on the frozen deterministic builder.")
    relation("relation:qa:o012-units-001-025-build", BUILD_ID, "illustrates",
             "artifact:o012-units-001-025-build-receipt",
             "Build QA event is witnessed by its exact receipt.")
    relation("relation:qa:o012-units-001-025-visual", VISUAL_ID, "illustrates",
             "artifact:o012-units-001-025-visual-receipt",
             "Visual QA event is witnessed by its exact receipt.")
    relation("relation:qa:o012-units-001-025-render-inventory", VISUAL_ID, "illustrates",
             "artifact:o012-units-001-025-render-inventory",
             "Visual QA event is bounded by the exact inspected-page render inventory.")

    merged = [record for name in FILES for record in tables[name]] + [
        record for name in FILES for record in additions[name]]
    if len({record["id"] for record in merged}) != len(merged):
        raise SystemExit("global ID collision in proposed backend")
    generic = load_generic()
    by_id = {record["id"]: record for record in merged}
    generic.validate_shapes(merged)
    generic.validate_references(merged, by_id)
    generic.validate_artifact_manifests(merged, LANE)
    outputs: dict[str, bytes] = {}
    for name in FILES:
        if (BACKEND / name).read_bytes() != raws[name]:
            raise SystemExit(f"semantic prefix changed before write: {name}")
        suffix = b"".join(canon(obj) for obj in sorted(
            additions[name], key=lambda obj: obj["id"]))
        outputs[name] = raws[name] + suffix
    for name in FILES:
        (BACKEND / name).write_bytes(outputs[name])
    final_bundle = hashlib.sha256()
    delta = {name: len(additions[name]) for name in FILES}
    for name in FILES:
        final_bundle.update(name.encode()); final_bundle.update(b"\0"); final_bundle.update(outputs[name])
    print("Cumulative Units 001-025 backend append: PASS")
    print("new_records_by_file=" + json.dumps(delta, sort_keys=True))
    print(f"new_records={sum(delta.values())}")
    print(f"total_records={sum(PREFIX[name][0] + delta[name] for name in FILES)}")
    print(f"backend_bytes={sum(len(raw) for raw in outputs.values())}")
    print(f"backend_bundle_sha256={final_bundle.hexdigest()}")
    for name in FILES:
        print(f"file={name} records={PREFIX[name][0] + delta[name]} "
              f"bytes={len(outputs[name])} sha256={digest(outputs[name])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
