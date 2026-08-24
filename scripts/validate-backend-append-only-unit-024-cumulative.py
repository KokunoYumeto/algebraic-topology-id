#!/usr/bin/env python3
"""Independent validator for the cumulative Units 001--024 backend append."""
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
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
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
APPEND_COUNTS = {
    "artifacts.jsonl": 7, "assets.jsonl": 0, "authority.jsonl": 0,
    "concepts.jsonl": 0, "corrections.jsonl": 0, "qa.jsonl": 2,
    "relations.jsonl": 7, "rights.jsonl": 1, "segments.jsonl": 0,
    "terms.jsonl": 0, "units.jsonl": 0,
}
FINAL = {
    "artifacts.jsonl": (135, 107142, "6e0bee128eb762523c603ae31c2578325f171d61fbcd15ac6c861be6486917b5"),
    "assets.jsonl": (26, 16063, "60d4f100505e27b28bc0642c8849dbc1842926d971642f2210c3a392e3f73eb4"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (319, 100311, "342c1cabc894a64d766dee238ded0a923ef655930421ddfe4d5fcf7f4569c17f"),
    "corrections.jsonl": (322, 316453, "acb12d317419c4df9f43e3743daa4001bf2a99a70c8ca4f55388401a211a488b"),
    "qa.jsonl": (114, 64675, "87e517a10dc7b2295b469770c72ef7aef3f9cef87a6e88e1499eaa249590af45"),
    "relations.jsonl": (368, 149907, "77b3123aff933914316dc636ab0190916f8d922f4900ef5f6b3b79106148b268"),
    "rights.jsonl": (67, 61618, "1e31593a6d4004633f9b27581924ed24a4ab40f11b817df22a9298116eeeb185"),
    "segments.jsonl": (1016, 1313231, "09210c2eaee49c9937ba555f1b18b26332c14297adbd70bcd17830b5ac75e620"),
    "terms.jsonl": (312, 193238, "68e6b19d70650fae488bf4ab7676dbc8e3d9efb1fb1b46de10a0169caafb1665"),
    "units.jsonl": (1040, 1401068, "ca605764e55f79126ac83d3313dd2d7a72626f4b3906573c7bc51ca9a3f1b95d"),
}
PREFIX_RECORDS = 3706
PREFIX_BYTES = 3714904
PREFIX_BUNDLE = "b0a182615e96995b6afa9ad0d8b25f221b9ad6fb58feca01b284b08211db1066"
FINAL_BUNDLE = "ffa8c7cb45b6d8170d7bc83df24ec487fd0c2777297b55eff2d5e7b3ae63fe25"
ROOT = "unit:o012-rbt-u024"
SOURCE_RIGHTS = "rights:o012-units-001-024-composite-cc-by-4.0"
FINAL_RIGHTS = "rights:o012-units-001-024-composite-cc-by-4.0-final-993a"
BUILD_ID = "qa:o012-units-001-024-build"
VISUAL_ID = "qa:o012-units-001-024-visual"
MANIFEST_ID = "artifact:o012-units-001-024-manifest"
BUILD_RECEIPT_PATH = "qa/UNITS_001_024_BUILD_RECEIPT.json"
VISUAL_RECEIPT_PATH = "qa/UNITS_001_024_VISUAL_QA.md"
INVENTORY_PATH = "qa/UNITS_001_024_RENDER_INVENTORY.csv"
EXPECTED_PAGES = 286
EXPECTED_RENDER_PAGES = [1, 273, *range(274, 287)]
ARTIFACTS: dict[str, tuple[str, int, str]] = {
    "artifact:o012-units-001-024-build-script": (
        "scripts/build-units-001-024.ps1", 21976,
        "8e62da597b783f56e0a9174a7822ee453de6de8be01fc5493cb2ab93c41a3c44"),
    "artifact:o012-units-001-024-html": (
        "output/html/units-001-024/index.html", 3927104,
        "28a84406de9e196070965920a7f7937177197977f9ddf118f0f8b07d464cbf0f"),
    "artifact:o012-units-001-024-pdf": (
        "output/pdf/topologi-aljabar-unit-001-024-id.pdf", 1907368,
        "5189b04f2f28d7e8192c16e8ef070e23bbf98085d150d1f2124d15c071ccf9b8"),
    MANIFEST_ID: (
        "output/ARTIFACT_MANIFEST_UNITS_001_024.csv", 249,
        "23d2b33dd8eb08ba82bb020e3607abbf24925d79e774ca177be228656800a0ff"),
    "artifact:o012-units-001-024-build-receipt": (
        BUILD_RECEIPT_PATH, 7560,
        "a050b3d282d43033ccdd7565bc6ee301eee6c30014ef6d8b84c5ec490406129a"),
    "artifact:o012-units-001-024-visual-receipt": (
        VISUAL_RECEIPT_PATH, 4928,
        "7aff942b47ec489a56923879aee189fc3911e0eded232a511de66aff8ee01a27"),
    "artifact:o012-units-001-024-render-inventory": (
        INVENTORY_PATH, 2659,
        "1d9554d98de7d4751fc7ee2d1b5a6cb45edb580e62226b030aea389dff9de683"),
}
RELATION_IDS = {
    "relation:boundary:o012-units-001-024-build",
    "relation:contains:o012-units-001-024-manifest:html",
    "relation:contains:o012-units-001-024-manifest:pdf",
    "relation:depends-on:o012-units-001-024-build:builder",
    "relation:qa:o012-units-001-024-build",
    "relation:qa:o012-units-001-024-visual",
    "relation:qa:o012-units-001-024-render-inventory",
}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8") + b"\n"


def load_generic():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_u024_cumulative", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    records: list[dict[str, Any]] = []
    by_file: dict[str, list[dict[str, Any]]] = {}
    raw_by_file: dict[str, bytes] = {}
    suffix_ids: dict[str, list[str]] = {}
    prefix_bundle = hashlib.sha256()
    for name in FILES:
        raw = (BACKEND / name).read_bytes(); raw_by_file[name] = raw
        final_count, final_bytes, final_sha = FINAL[name]
        if (len(raw), len(raw.splitlines()), digest(raw)) != (final_bytes, final_count, final_sha):
            raise SystemExit(f"{name}: final identity mismatch")
        lines = raw.splitlines(keepends=True)
        if b"\r" in raw or not raw.endswith(b"\n"):
            raise SystemExit(f"{name}: invalid newline form")
        prefix_count, prefix_bytes, prefix_sha = PREFIX[name]
        prefix = b"".join(lines[:prefix_count])
        if len(prefix) != prefix_bytes or digest(prefix) != prefix_sha:
            raise SystemExit(f"{name}: semantic prefix mismatch")
        prefix_bundle.update(name.encode()); prefix_bundle.update(b"\0"); prefix_bundle.update(prefix)
        suffix = lines[prefix_count:]
        if len(suffix) != APPEND_COUNTS[name]:
            raise SystemExit(f"{name}: cumulative append count mismatch")
        parsed: list[dict[str, Any]] = []
        for number, line in enumerate(lines, 1):
            obj = json.loads(line.decode("utf-8"))
            if not isinstance(obj.get("id"), str) or canon(obj) != line:
                raise SystemExit(f"{name}:{number}: noncanonical record")
            parsed.append(obj)
        ids = [obj["id"] for obj in parsed]
        if len(ids) != len(set(ids)):
            raise SystemExit(f"{name}: duplicate IDs")
        appended = ids[prefix_count:]
        if appended != sorted(appended):
            raise SystemExit(f"{name}: suffix order mismatch")
        suffix_ids[name] = appended; by_file[name] = parsed; records.extend(parsed)
    if (sum(item[0] for item in PREFIX.values()) != PREFIX_RECORDS
            or sum(item[1] for item in PREFIX.values()) != PREFIX_BYTES
            or prefix_bundle.hexdigest() != PREFIX_BUNDLE
            or sum(APPEND_COUNTS.values()) != 17):
        raise SystemExit("semantic prefix/count bundle mismatch")
    by_id = {obj["id"]: obj for obj in records}
    if len(by_id) != len(records):
        raise SystemExit("global duplicate backend ID")
    generic = load_generic()
    generic.validate_shapes(records)
    generic.validate_references(records, by_id)
    generic.validate_artifact_manifests(records, LANE)

    if set(suffix_ids["artifacts.jsonl"]) != set(ARTIFACTS):
        raise SystemExit("cumulative artifact suffix mismatch")
    if set(suffix_ids["qa.jsonl"]) != {BUILD_ID, VISUAL_ID}:
        raise SystemExit("cumulative QA suffix mismatch")
    if set(suffix_ids["relations.jsonl"]) != RELATION_IDS:
        raise SystemExit("cumulative relation suffix mismatch")
    if suffix_ids["rights.jsonl"] != [FINAL_RIGHTS]:
        raise SystemExit("cumulative rights suffix mismatch")
    for name in FILES:
        if name not in {"artifacts.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl"} and suffix_ids[name]:
            raise SystemExit(f"out-of-scope cumulative mutation: {name}")

    for ident, (relative, size, expected_sha) in ARTIFACTS.items():
        raw = (LANE / relative).read_bytes(); record = by_id.get(ident)
        if (len(raw) != size or digest(raw) != expected_sha or not record
                or record["path"] != relative or record["bytes"] != size
                or record["sha256"] != expected_sha
                or record["rights_component_id"] != FINAL_RIGHTS
                or record["unit_id"] != ROOT or MODEL not in record["toolchain"]):
            raise SystemExit(f"cumulative artifact binding mismatch: {ident}")
    receipt = json.loads((LANE / BUILD_RECEIPT_PATH).read_text(encoding="utf-8"))
    source = receipt.get("source_authority", {})
    html = receipt.get("html_checks", {})
    pdf = receipt.get("artifacts", {}).get("pdf", {})
    if (receipt.get("status") != "PASS"
            or source.get("cumulative_source_span") != "134-5369"
            or source.get("next_source_line") != 5370
            or source.get("unit_024_sha256") !=
            "993ad0c3493caff6bd15ab2bcf435f6cbb1f49ed9a1e11bc1009d649ae2d3647"
            or source.get("unit_024_span_sha256") !=
            "b2128930a56a0a8c04c327a397e72e21b215ffe742bb684e8dd166f0e04b0aea"
            or receipt.get("toolchain", {}).get("builder_sha256") != ARTIFACTS[
                "artifact:o012-units-001-024-build-script"][2]
            or receipt.get("toolchain", {}).get("model_provenance") != MODEL
            or pdf.get("pages") != EXPECTED_PAGES or pdf.get("unit_024_pages") != "274-286"
            or html.get("unit_024_ids") != 60 or html.get("missing_unit_024_ids") != 0
            or html.get("raw_tex_math_fallbacks") != 0
            or html.get("unresolved_fragment_links") != 0
            or html.get("runtime_external_dependencies") != 0
            or not html.get("responsive_mobile_reflow")):
        raise SystemExit("build receipt semantic/QA binding mismatch")
    reproducibility = receipt.get("reproducibility", {})
    if not all(reproducibility.get(key) for key in (
            "html_two_builds_byte_identical", "pdf_two_builds_byte_identical",
            "source_baseline_authority_and_unit_024_evidence_fail_closed",
            "pandoc_html_warnings_are_fatal",
            "responsive_fix_rebuilt_before_final_identity")):
        raise SystemExit("build reproducibility gate mismatch")

    manifest_text = (LANE / ARTIFACTS[MANIFEST_ID][0]).read_text(encoding="utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(manifest_text)))
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
        raise SystemExit("manifest row closure mismatch")
    visual = (LANE / VISUAL_RECEIPT_PATH).read_text(encoding="utf-8")
    if ("Status: **PASS**" not in visual or MODEL not in visual
            or "pages **1, 273, and 274-286**" not in visual):
        raise SystemExit("visual receipt gate mismatch")
    inventory_text = (LANE / INVENTORY_PATH).read_text(encoding="utf-8-sig")
    inventory = list(csv.DictReader(io.StringIO(inventory_text)))
    if (not inventory
            or list(inventory[0]) != ["pdf_page", "coverage", "render_name", "dpi",
                                      "width_px", "height_px", "render_bytes", "render_sha256"]
            or [int(row["pdf_page"]) for row in inventory] != EXPECTED_RENDER_PAGES
            or any((row["dpi"], row["width_px"], row["height_px"]) !=
                   ("144", "1191", "1684") for row in inventory)
            or any(not re.fullmatch(r"[0-9a-f]{64}", row["render_sha256"])
                   for row in inventory)):
        raise SystemExit("render inventory gate mismatch")

    rights = by_id[FINAL_RIGHTS]
    if (rights["supersedes"] != SOURCE_RIGHTS
            or rights["component_scope"] != [
                f"unit:o012-rbt-u{number:03d}" for number in range(1, 25)]
            or rights["license_expression"] != "CC-BY-4.0"):
        raise SystemExit("final built-rights pointer mismatch")
    if by_id[BUILD_ID]["result"] != "passed" or by_id[VISUAL_ID]["result"] != "passed":
        raise SystemExit("cumulative QA events not passed")
    if set(by_id[BUILD_ID]["witness_artifact_ids"]) != {
            "artifact:o012-units-001-024-build-script",
            "artifact:o012-units-001-024-html",
            "artifact:o012-units-001-024-pdf", MANIFEST_ID,
            "artifact:o012-units-001-024-build-receipt"}:
        raise SystemExit("build QA witness closure mismatch")
    if set(by_id[VISUAL_ID]["witness_artifact_ids"]) != {
            "artifact:o012-units-001-024-pdf",
            "artifact:o012-units-001-024-visual-receipt",
            "artifact:o012-units-001-024-render-inventory"}:
        raise SystemExit("visual QA witness closure mismatch")
    if (by_id["relation:qa:o012-units-001-024-render-inventory"]["to_id"] !=
            "artifact:o012-units-001-024-render-inventory"):
        raise SystemExit("render inventory relation mismatch")

    bundle = hashlib.sha256()
    for name in FILES:
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(raw_by_file[name])
    if bundle.hexdigest() != FINAL_BUNDLE:
        raise SystemExit("final backend bundle mismatch")
    output = {
        "status": "PASS", "prefix_records": PREFIX_RECORDS,
        "prefix_bytes": PREFIX_BYTES, "prefix_bundle_sha256": PREFIX_BUNDLE,
        "prefix_preserved_byte_for_byte": True,
        "new_records": sum(APPEND_COUNTS.values()), "total_records": len(records),
        "backend_bytes": sum(len(raw) for raw in raw_by_file.values()),
        "backend_bundle_sha256": bundle.hexdigest(),
        "records_added_by_file": APPEND_COUNTS,
        "records": {name: len(by_file[name]) for name in FILES},
        "per_file_bytes": {name: len(raw_by_file[name]) for name in FILES},
        "per_file_sha256": {name: digest(raw_by_file[name]) for name in FILES},
        "artifacts": {ident: {"path": spec[0], "bytes": spec[1], "sha256": spec[2]}
                      for ident, spec in ARTIFACTS.items()},
        "pdf_pages": EXPECTED_PAGES, "render_inventory_rows": len(inventory),
    }
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
