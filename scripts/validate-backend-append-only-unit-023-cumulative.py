#!/usr/bin/env python3
"""Independent validator for the cumulative Units 001--023 backend append."""
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
    "artifacts.jsonl": (119, 93962, "a439fbb383c0082b68f9ebee1ec988b92f910e595992bbe23a97c1844ab0c9a9"),
    "assets.jsonl": (25, 15447, "752dfa957041664a1b3f32acdcf996511164d5c17ba6aa34619a100651dad3b1"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (312, 98079, "6fadff806dab54588f4984dd44ec745152841dbf44416ea881d9414f6b535830"),
    "corrections.jsonl": (313, 306801, "a0545c84efadc062f181356f9fa508b0da5f9077f52702da0750e3165c0b6244"),
    "qa.jsonl": (107, 60615, "6c6a5c890596eb883daf5b30ddb3ed1ffc287fa91aca6eaa45312225a75e0a13"),
    "relations.jsonl": (331, 134073, "d85e492b275093cb807fa2ca407bca56c0ec758c1f5e7df2f2f0babc4baf8a30"),
    "rights.jsonl": (62, 56383, "b3d975821a277ec640297ce75cb44e2c6dd18383eff876361b1952a51449b7ff"),
    "segments.jsonl": (956, 1193838, "1851199865ae823a7f155f1a33590290cafccb0f1cafe37d429fb7072a2d84c0"),
    "terms.jsonl": (305, 188007, "16ac428e76df5de2a97f475c9a80c7e63278bc57a15720047785e4ad217e82a9"),
    "units.jsonl": (979, 1274986, "e66891050013b595dbe972bee0d7ba3b88689a8a6a06a2c2885919194df036c9"),
}
APPEND_COUNTS = {"artifacts.jsonl": 6, "assets.jsonl": 0, "authority.jsonl": 0,
                 "concepts.jsonl": 0, "corrections.jsonl": 0, "qa.jsonl": 2,
                 "relations.jsonl": 6, "rights.jsonl": 1, "segments.jsonl": 0,
                 "terms.jsonl": 0, "units.jsonl": 0}
FINAL: dict[str, tuple[int, int, str]] = {
    "artifacts.jsonl": (125, 98770, "f8f4fc8b686554ce528bffe4ca31533d8f416ad34d9ed16b8f23b5b6d981c13c"),
    "assets.jsonl": (25, 15447, "752dfa957041664a1b3f32acdcf996511164d5c17ba6aa34619a100651dad3b1"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (312, 98079, "6fadff806dab54588f4984dd44ec745152841dbf44416ea881d9414f6b535830"),
    "corrections.jsonl": (313, 306801, "a0545c84efadc062f181356f9fa508b0da5f9077f52702da0750e3165c0b6244"),
    "qa.jsonl": (109, 61880, "3c8c741c0c50b56cd0d15b7616c3ebd3006fe368382cc14e7c50ee743eebb974"),
    "relations.jsonl": (337, 136702, "07f7ec67c251eb180f211b09da33ec165129c45646d1b08014de2f3e68b2882c"),
    "rights.jsonl": (63, 57648, "f39bd50ab5e33d7d3b0ae9063b2ed0adc9fc3986a8a034de4311876c3e810157"),
    "segments.jsonl": (956, 1193838, "1851199865ae823a7f155f1a33590290cafccb0f1cafe37d429fb7072a2d84c0"),
    "terms.jsonl": (305, 188007, "16ac428e76df5de2a97f475c9a80c7e63278bc57a15720047785e4ad217e82a9"),
    "units.jsonl": (979, 1274986, "e66891050013b595dbe972bee0d7ba3b88689a8a6a06a2c2885919194df036c9"),
}
PREFIX_RECORDS = 3513
PREFIX_BYTES = 3424912
PREFIX_BUNDLE = "2b31536824cea66fc186bd653354eea4eea45f9c68da7992a45d037c782672dc"
FINAL_BUNDLE = "0c8b27890f8423fc3224c89f2bcf60ed6cbcb9d93fabef7b53c399784f0aaaef"
ROOT = "unit:o012-rbt-u023"
SOURCE_RIGHTS = "rights:o012-units-001-023-composite-cc-by-4.0"
FINAL_RIGHTS = "rights:o012-units-001-023-composite-cc-by-4.0-final-6f05"
BUILD_ID = "qa:o012-units-001-023-build"
VISUAL_ID = "qa:o012-units-001-023-visual"
MANIFEST_ID = "artifact:o012-units-001-023-manifest"
BUILD_RECEIPT_PATH = "qa/UNITS_001_023_BUILD_RECEIPT.json"
VISUAL_RECEIPT_PATH = "qa/UNITS_001_023_VISUAL_QA.md"
EXPECTED_PAGES = 273
# ident -> (path, bytes, sha256)
ARTIFACTS: dict[str, tuple[str, int, str]] = {
    "artifact:o012-units-001-023-build-script": (
        "scripts/build-units-001-023.ps1", 19688,
        "2fd88a027775678ec359037923df604ecb2444e527ba8bda61731f68a6691f88"),
    "artifact:o012-units-001-023-html": (
        "output/html/units-001-023/index.html", 3707037,
        "536fbe19e295424d12198bf1b221be3e2f0170f87fa810a9125bcca9f742264b"),
    "artifact:o012-units-001-023-pdf": (
        "output/pdf/topologi-aljabar-unit-001-023-id.pdf", 1801983,
        "e51aa739eefaa12f4b1d7a4fe99073c525775f113aa62e4506395a01fe1fcbaf"),
    MANIFEST_ID: (
        "output/ARTIFACT_MANIFEST_UNITS_001_023.csv", 249,
        "f12629f0929eeec100c6fc769c239c64bcc1fb72283be4abee9daec691561f34"),
    "artifact:o012-units-001-023-build-receipt": (
        "qa/UNITS_001_023_BUILD_RECEIPT.json", 5775,
        "a09fde0e147756c35fe4ba9ff5a212625bdbe96d19400409b14214e67afb4cf8"),
    "artifact:o012-units-001-023-visual-receipt": (
        "qa/UNITS_001_023_VISUAL_QA.md", 4278,
        "784bc1b77b65e3e91c1de34a2e14d42a2202861a04e24f8eb3c130f480dbd35e"),
}
RELATION_IDS = {
    "relation:boundary:o012-units-001-023-build",
    "relation:contains:o012-units-001-023-manifest:html",
    "relation:contains:o012-units-001-023-manifest:pdf",
    "relation:depends-on:o012-units-001-023-build:builder",
    "relation:qa:o012-units-001-023-build",
    "relation:qa:o012-units-001-023-visual",
}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8") + b"\n"


def load_generic():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_u023_cumulative", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expected_artifact_ids() -> set[str]:
    return {
        "artifact:o012-units-001-023-build-script",
        "artifact:o012-units-001-023-html",
        "artifact:o012-units-001-023-pdf",
        MANIFEST_ID,
        "artifact:o012-units-001-023-build-receipt",
        "artifact:o012-units-001-023-visual-receipt",
    }


def main() -> int:
    if (set(FINAL) != set(FILES)
            or not re.fullmatch(r"[0-9a-f]{64}", FINAL_BUNDLE)
            or set(ARTIFACTS) != expected_artifact_ids()
            or EXPECTED_PAGES <= 0):
        raise SystemExit("cumulative Unit 23 final identities are not admitted")
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
            or prefix_bundle.hexdigest() != PREFIX_BUNDLE):
        raise SystemExit("semantic prefix bundle mismatch")
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
    html_checks = receipt.get("html_checks", {})
    if (receipt.get("status") != "PASS"
            or source.get("unit_023_sha256") !=
            "6f05ddbe6a720109797976c6929b0535f21a38353673cb42d9646a3196f56bd2"
            or source.get("unit_023_span_sha256") !=
            "c7256a45621ad7a435277867298e4aeb8eb584dfce066cdae3b48c4ee0e0e3f4"
            or receipt.get("toolchain", {}).get("builder_sha256") != ARTIFACTS[
                "artifact:o012-units-001-023-build-script"][2]
            or receipt.get("artifacts", {}).get("pdf", {}).get("pages") != EXPECTED_PAGES
            or html_checks.get("unit_023_ids") != 51
            or html_checks.get("missing_unit_023_ids") != 0
            or html_checks.get("raw_tex_math_fallbacks") != 0
            or receipt.get("toolchain", {}).get("model_provenance") != MODEL):
        raise SystemExit("build receipt semantic/QA binding mismatch")
    reproducibility = receipt.get("reproducibility", {})
    if not all(reproducibility.get(key) for key in (
            "html_two_builds_byte_identical", "pdf_two_builds_byte_identical",
            "source_baseline_and_unit_023_evidence_fail_closed",
            "pandoc_html_warnings_are_fatal")):
        raise SystemExit("build reproducibility gate mismatch")
    manifest_text = (LANE / ARTIFACTS[MANIFEST_ID][0]).read_text(encoding="utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(manifest_text)))
    expected_rows = {
        (ARTIFACTS["artifact:o012-units-001-023-html"][0],
         str(ARTIFACTS["artifact:o012-units-001-023-html"][1]),
         ARTIFACTS["artifact:o012-units-001-023-html"][2]),
        (ARTIFACTS["artifact:o012-units-001-023-pdf"][0],
         str(ARTIFACTS["artifact:o012-units-001-023-pdf"][1]),
         ARTIFACTS["artifact:o012-units-001-023-pdf"][2]),
    }
    if (not rows or list(rows[0]) != ["path", "bytes", "sha256"] or
            {(row["path"], row["bytes"], row["sha256"]) for row in rows} != expected_rows):
        raise SystemExit("manifest row closure mismatch")
    visual = (LANE / VISUAL_RECEIPT_PATH).read_text(encoding="utf-8")
    if ("Status: **PASS**" not in visual or MODEL not in visual
            or str(EXPECTED_PAGES) not in visual):
        raise SystemExit("visual receipt gate mismatch")

    rights = by_id[FINAL_RIGHTS]
    if (rights["supersedes"] != SOURCE_RIGHTS
            or rights["component_scope"] != [
                f"unit:o012-rbt-u{number:03d}" for number in range(1, 24)]
            or rights["license_expression"] != "CC-BY-4.0"):
        raise SystemExit("final built-rights pointer mismatch")
    if by_id[BUILD_ID]["result"] != "passed" or by_id[VISUAL_ID]["result"] != "passed":
        raise SystemExit("cumulative QA events not passed")
    if set(by_id[BUILD_ID]["witness_artifact_ids"]) != {
            "artifact:o012-units-001-023-build-script",
            "artifact:o012-units-001-023-html",
            "artifact:o012-units-001-023-pdf", MANIFEST_ID,
            "artifact:o012-units-001-023-build-receipt"}:
        raise SystemExit("build QA witness closure mismatch")
    if set(by_id[VISUAL_ID]["witness_artifact_ids"]) != {
            "artifact:o012-units-001-023-pdf",
            "artifact:o012-units-001-023-visual-receipt"}:
        raise SystemExit("visual QA witness closure mismatch")

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
        "pdf_pages": EXPECTED_PAGES,
    }
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
