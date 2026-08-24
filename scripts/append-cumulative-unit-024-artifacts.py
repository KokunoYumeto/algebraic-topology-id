#!/usr/bin/env python3
"""Append the verified cumulative Units 001--024 build boundary.

The complete 3,706-record Unit 24 semantic backend is immutable. This
producer verifies that exact prefix and all seven frozen build witnesses
before adding only cumulative artifact, QA, relation, and final-rights records.
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
ROOT = "unit:o012-rbt-u024"
SOURCE_RIGHTS = "rights:o012-units-001-024-composite-cc-by-4.0"
FINAL_RIGHTS = "rights:o012-units-001-024-composite-cc-by-4.0-final-993a"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX = {
    "artifacts.jsonl": (128, 101337, "4bff9b72daf44201c97a7e3c3896e43d0174e79d040b0b88b9d4e31b828139c3"),
    "assets.jsonl": (26, 16063, "60d4f100505e27b28bc0642c8849dbc1842926d971642f2210c3a392e3f73eb4"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (319, 100311, "342c1cabc894a64d766dee238ded0a923ef655930421ddfe4d5fcf7f4569c17f"),
    "corrections.jsonl": (322, 316453, "acb12d317419c4df9f43e3743daa4001bf2a99a70c8ca4f55388401a211a488b"),
    "qa.jsonl": (112, 63331, "0c7af567ccfe67c0db7611f889511c8ede1730e3da339d04388ca87b835c9349"),
    "relations.jsonl": (361, 146819, "393554493bb45b01fe93045639ad8f6cf0ca65fc324adf87e3219d71a824985e"),
    "rights.jsonl": (66, 60332, "328bf2f3c0e1504d59150ef25af16e8e9de68a71e5f7eda9fcf2e154c3a5cd77"),
    "segments.jsonl": (1016, 1313231, "09210c2eaee49c9937ba555f1b18b26332c14297adbd70bcd17830b5ac75e620"),
    "terms.jsonl": (312, 193238, "68e6b19d70650fae488bf4ab7676dbc8e3d9efb1fb1b46de10a0169caafb1665"),
    "units.jsonl": (1040, 1401068, "ca605764e55f79126ac83d3313dd2d7a72626f4b3906573c7bc51ca9a3f1b95d"),
}
PREFIX_RECORDS = 3706
PREFIX_BYTES = 3714904
PREFIX_BUNDLE = "b0a182615e96995b6afa9ad0d8b25f221b9ad6fb58feca01b284b08211db1066"
BUILD_ID = "qa:o012-units-001-024-build"
VISUAL_ID = "qa:o012-units-001-024-visual"
MANIFEST_ID = "artifact:o012-units-001-024-manifest"
BUILD_RECEIPT_PATH = "qa/UNITS_001_024_BUILD_RECEIPT.json"
VISUAL_RECEIPT_PATH = "qa/UNITS_001_024_VISUAL_QA.md"
INVENTORY_PATH = "qa/UNITS_001_024_RENDER_INVENTORY.csv"
EXPECTED_PAGES = 286
EXPECTED_RENDER_PAGES = [1, 273, *range(274, 287)]

# ident -> (path, bytes, sha256, media type, state, QA ids, manifest id)
ARTIFACTS: dict[str, tuple[str, int, str, str, str, list[str], str | None]] = {
    "artifact:o012-units-001-024-build-script": (
        "scripts/build-units-001-024.ps1", 21976,
        "8e62da597b783f56e0a9174a7822ee453de6de8be01fc5493cb2ab93c41a3c44",
        "text/plain; charset=utf-8", "source_frozen", [BUILD_ID], None),
    "artifact:o012-units-001-024-html": (
        "output/html/units-001-024/index.html", 3927104,
        "28a84406de9e196070965920a7f7937177197977f9ddf118f0f8b07d464cbf0f",
        "text/html; charset=utf-8", "built", [BUILD_ID], MANIFEST_ID),
    "artifact:o012-units-001-024-pdf": (
        "output/pdf/topologi-aljabar-unit-001-024-id.pdf", 1907368,
        "5189b04f2f28d7e8192c16e8ef070e23bbf98085d150d1f2124d15c071ccf9b8",
        "application/pdf", "built", [BUILD_ID, VISUAL_ID], MANIFEST_ID),
    MANIFEST_ID: (
        "output/ARTIFACT_MANIFEST_UNITS_001_024.csv", 249,
        "23d2b33dd8eb08ba82bb020e3607abbf24925d79e774ca177be228656800a0ff",
        "text/csv; charset=utf-8", "built", [BUILD_ID], None),
    "artifact:o012-units-001-024-build-receipt": (
        BUILD_RECEIPT_PATH, 7560,
        "a050b3d282d43033ccdd7565bc6ee301eee6c30014ef6d8b84c5ec490406129a",
        "application/json", "built", [BUILD_ID], None),
    "artifact:o012-units-001-024-visual-receipt": (
        VISUAL_RECEIPT_PATH, 4928,
        "7aff942b47ec489a56923879aee189fc3911e0eded232a511de66aff8ee01a27",
        "text/markdown; charset=utf-8", "visually_checked", [VISUAL_ID], None),
    "artifact:o012-units-001-024-render-inventory": (
        INVENTORY_PATH, 2659,
        "1d9554d98de7d4751fc7ee2d1b5a6cb45edb580e62226b030aea389dff9de683",
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
    spec = importlib.util.spec_from_file_location("o012_generic_u024_build", path)
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
    receipt = json.loads((LANE / BUILD_RECEIPT_PATH).read_text(encoding="utf-8"))
    source = receipt.get("source_authority", {})
    toolchain = receipt.get("toolchain", {})
    reproducibility = receipt.get("reproducibility", {})
    if (receipt.get("status") != "PASS"
            or source.get("cumulative_source_span") != "134-5369"
            or source.get("next_source_line") != 5370
            or source.get("unit_024_span") != "5113-5369"
            or source.get("unit_024_span_bytes") != 12837
            or source.get("unit_024_span_sha256") !=
            "b2128930a56a0a8c04c327a397e72e21b215ffe742bb684e8dd166f0e04b0aea"
            or source.get("unit_024_sha256") !=
            "993ad0c3493caff6bd15ab2bcf435f6cbb1f49ed9a1e11bc1009d649ae2d3647"
            or toolchain.get("builder_sha256") != ARTIFACTS[
                "artifact:o012-units-001-024-build-script"][2]
            or toolchain.get("model_provenance") != MODEL
            or not reproducibility.get("html_two_builds_byte_identical")
            or not reproducibility.get("pdf_two_builds_byte_identical")
            or not reproducibility.get(
                "source_baseline_authority_and_unit_024_evidence_fail_closed")
            or not reproducibility.get("pandoc_html_warnings_are_fatal")
            or not reproducibility.get("responsive_fix_rebuilt_before_final_identity")):
        raise SystemExit("cumulative build receipt binding/reproducibility mismatch")
    declared = receipt.get("artifacts", {})
    for key, ident in {
        "html": "artifact:o012-units-001-024-html",
        "pdf": "artifact:o012-units-001-024-pdf", "manifest": MANIFEST_ID,
    }.items():
        spec = ARTIFACTS[ident]
        if (declared.get(key, {}).get("bytes"), declared.get(key, {}).get("sha256")) != (spec[1], spec[2]):
            raise SystemExit(f"build receipt {key} identity mismatch")
    html = receipt.get("html_checks", {})
    pdf = declared.get("pdf", {})
    if (pdf.get("pages") != EXPECTED_PAGES or pdf.get("unit_024_pages") != "274-286"
            or html.get("raw_tex_math_fallbacks") != 0
            or html.get("missing_unit_024_ids") != 0
            or html.get("unit_024_ids") != 60
            or html.get("unresolved_fragment_links") != 0
            or html.get("runtime_external_dependencies") != 0
            or not html.get("responsive_mobile_reflow")):
        raise SystemExit("cumulative structural/PDF gate mismatch")
    visual = (LANE / VISUAL_RECEIPT_PATH).read_text(encoding="utf-8")
    if ("Status: **PASS**" not in visual or MODEL not in visual
            or "pages **1, 273, and 274-286**" not in visual):
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
    manifest = (LANE / ARTIFACTS[MANIFEST_ID][0]).read_text(encoding="utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(manifest)))
    expected_rows = {
        (ARTIFACTS["artifact:o012-units-001-024-html"][0],
         str(ARTIFACTS["artifact:o012-units-001-024-html"][1]),
         ARTIFACTS["artifact:o012-units-001-024-html"][2]),
        (ARTIFACTS["artifact:o012-units-001-024-pdf"][0],
         str(ARTIFACTS["artifact:o012-units-001-024-pdf"][1]),
         ARTIFACTS["artifact:o012-units-001-024-pdf"][2]),
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
            raise SystemExit(f"immutable Unit 24 semantic prefix mismatch: {name}")
        if b"\r" in raw or not raw.endswith(b"\n"):
            raise SystemExit(f"invalid prefix newline form: {name}")
        parsed: list[dict[str, Any]] = []
        for number, line in enumerate(lines, 1):
            obj = json.loads(line.decode("utf-8"))
            if canon(obj) != line or not isinstance(obj.get("id"), str):
                raise SystemExit(f"noncanonical prefix record: {name}:{number}")
            if obj["id"] in all_ids:
                raise SystemExit(f"duplicate prefix ID: {obj['id']}")
            all_ids.add(obj["id"]); parsed.append(obj)
        raws[name] = raw; tables[name] = parsed
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(raw)
    if (len(all_ids) != PREFIX_RECORDS
            or sum(len(raw) for raw in raws.values()) != PREFIX_BYTES
            or bundle.hexdigest() != PREFIX_BUNDLE
            or ROOT not in all_ids or SOURCE_RIGHTS not in all_ids):
        raise SystemExit("Unit 24 semantic prefix bundle/root/rights mismatch")

    additions: dict[str, list[dict[str, Any]]] = {name: [] for name in FILES}
    pending: set[str] = set()

    def add(name: str, obj: dict[str, Any]) -> None:
        if obj["id"] in all_ids or obj["id"] in pending:
            raise SystemExit(f"duplicate appended ID: {obj['id']}")
        pending.add(obj["id"]); additions[name].append(obj)

    rights = common("rights", FINAL_RIGHTS)
    rights.update({
        "attribution": "Cumulative Roberts Units 001-024 Indonesian reader and deterministic build artifacts.",
        "change_notice": "Verified cumulative HTML/PDF build boundary; component-level rights and attribution records remain controlling.",
        "component_scope": [f"unit:o012-rbt-u{number:03d}" for number in range(1, 25)],
        "license_expression": "CC-BY-4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "non_endorsement": "Independent edition; no source-author endorsement.",
        "supersedes": SOURCE_RIGHTS,
        "third_party_status": "Component-scoped rights records control.",
    })
    add("rights.jsonl", rights)
    toolchain = receipt.get("toolchain", {})
    toolchain_note = ("Deterministic Units 001-024 builder; "
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
        "note": "Cumulative Units 001-024 HTML and PDF passed fail-closed inputs, two-build byte identity, exact manifest, offline HTML, MathML, fragment, responsive reflow, font, privacy, and source-binding gates.",
        "qa_type": "build", "result": "passed", "unit_id": ROOT,
        "witness_artifact_ids": [
            "artifact:o012-units-001-024-build-script",
            "artifact:o012-units-001-024-html",
            "artifact:o012-units-001-024-pdf", MANIFEST_ID,
            "artifact:o012-units-001-024-build-receipt"],
    })
    add("qa.jsonl", build)
    visual = common("qa_event", VISUAL_ID)
    visual.update({
        "note": "Complete Unit 24 span plus title and transition visual QA passed for the 286-page A4 PDF and responsive HTML; inventory fixes every inspected render identity.",
        "qa_type": "visual", "result": "passed", "unit_id": ROOT,
        "witness_artifact_ids": ["artifact:o012-units-001-024-pdf",
                                 "artifact:o012-units-001-024-visual-receipt",
                                 "artifact:o012-units-001-024-render-inventory"],
    })
    add("qa.jsonl", visual)

    def relation(ident: str, source: str, kind: str, target: str, note: str) -> None:
        record = common("relation", ident)
        record.update({"from_id": source, "note": note,
                       "relation_type": kind, "to_id": target})
        add("relations.jsonl", record)
    relation("relation:boundary:o012-units-001-024-build", FINAL_RIGHTS, "contains",
             "artifact:o012-units-001-024-pdf",
             "Final cumulative Units 001-024 build boundary points to the verified PDF reader.")
    relation("relation:contains:o012-units-001-024-manifest:html", MANIFEST_ID, "contains",
             "artifact:o012-units-001-024-html", "Manifest entry for the cumulative HTML reader.")
    relation("relation:contains:o012-units-001-024-manifest:pdf", MANIFEST_ID, "contains",
             "artifact:o012-units-001-024-pdf", "Manifest entry for the cumulative PDF reader.")
    relation("relation:depends-on:o012-units-001-024-build:builder", BUILD_ID, "depends-on",
             "artifact:o012-units-001-024-build-script",
             "The cumulative build QA depends on the frozen deterministic builder.")
    relation("relation:qa:o012-units-001-024-build", BUILD_ID, "illustrates",
             "artifact:o012-units-001-024-build-receipt",
             "Build QA event is witnessed by its exact receipt.")
    relation("relation:qa:o012-units-001-024-visual", VISUAL_ID, "illustrates",
             "artifact:o012-units-001-024-visual-receipt",
             "Visual QA event is witnessed by its exact receipt.")
    relation("relation:qa:o012-units-001-024-render-inventory", VISUAL_ID, "illustrates",
             "artifact:o012-units-001-024-render-inventory",
             "Visual QA event is bounded by the exact inspected-page render inventory.")

    merged = [record for name in FILES for record in tables[name]] + [
        record for name in FILES for record in additions[name]]
    if len({record["id"] for record in merged}) != len(merged):
        raise SystemExit("global ID collision in proposed backend")
    generic = load_generic()
    generic.validate_shapes(merged)
    generic.validate_references(merged, {record["id"]: record for record in merged})
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
    print("Cumulative Units 001-024 backend append: PASS")
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
