#!/usr/bin/env python3
"""Independent validator for the cumulative Units 001--022 backend append."""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
from typing import Any

LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX = {
    "artifacts.jsonl": (110, 86473, "5d16598495a6df0a0855f6c413cc78def50cf653d30c6699bcef5b5455cb72ea"),
    "assets.jsonl": (24, 14831, "69020caaf45628941c57ee5cf58f3c11a31505c3416ec9d65c9ac82b47ba97aa"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (297, 93358, "2e8f93bfa8b7622960716b8a6bd33811c630c877696c5cbf031cb14eadfa110b"),
    "corrections.jsonl": (302, 295241, "718a14732930b546a3c38bf2e131d23066b2f90f09d4dd80a781294296f5cbc6"),
    "qa.jsonl": (102, 57849, "86591e4710dcf61a1cc29c1ad94187b5d4bd362f4df8d9e7d63ac14bbb88dfaf"),
    "relations.jsonl": (303, 122094, "8c28ab28cfbe752f32c95746355dde648fa7b005d0f1d4550c3933e1d804fa28"),
    "rights.jsonl": (58, 52476, "2aaf92fd5c0853ddaea495ca7e3a20caba6de445193d9f5888e38523bc359434"),
    "segments.jsonl": (905, 1094552, "491b68e826f0221353d7a7782515be769fc8048e468bba5937c797ca0390bb8c"),
    "terms.jsonl": (290, 177339, "bf1c79fc4bbaf0a9bd71545f4d69d9dc36dcb728f23710ad33a9bf9791421695"),
    "units.jsonl": (927, 1169478, "56fdf925d6e547b4a936d4ac7fb483cdbd9d845ac292989a7162efae108fcf8f"),
}
APPEND_COUNTS = {"artifacts.jsonl": 6, "assets.jsonl": 0, "authority.jsonl": 0,
                 "concepts.jsonl": 0, "corrections.jsonl": 0, "qa.jsonl": 2,
                 "relations.jsonl": 6, "rights.jsonl": 1, "segments.jsonl": 0,
                 "terms.jsonl": 0, "units.jsonl": 0}
FINAL = {
    "artifacts.jsonl": (116, 91395, "05a9525a470df9a106ad785a026b45f8913c1dfc40d363eff12df5cea3d0a58e"),
    "assets.jsonl": (24, 14831, "69020caaf45628941c57ee5cf58f3c11a31505c3416ec9d65c9ac82b47ba97aa"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (297, 93358, "2e8f93bfa8b7622960716b8a6bd33811c630c877696c5cbf031cb14eadfa110b"),
    "corrections.jsonl": (302, 295241, "718a14732930b546a3c38bf2e131d23066b2f90f09d4dd80a781294296f5cbc6"),
    "qa.jsonl": (104, 59176, "b8c439539b4bd566bb3b46423e19ab925f2cbcb8075a77b5df6a76ba7b9cf516"),
    "relations.jsonl": (309, 124723, "2d58a794206f07915c18c98c220e143354429c57d14bc93f27eb1806a2277ab6"),
    "rights.jsonl": (59, 53720, "f734f3649cc4e8a40ec7d63bd92843c1d04cf835d46f9fcef9224168a9142bd2"),
    "segments.jsonl": (905, 1094552, "491b68e826f0221353d7a7782515be769fc8048e468bba5937c797ca0390bb8c"),
    "terms.jsonl": (290, 177339, "bf1c79fc4bbaf0a9bd71545f4d69d9dc36dcb728f23710ad33a9bf9791421695"),
    "units.jsonl": (927, 1169478, "56fdf925d6e547b4a936d4ac7fb483cdbd9d845ac292989a7162efae108fcf8f"),
}
PREFIX_BUNDLE = "2329606117578210ce927123ec01639390f2e493fcc995899606eaa38996f2bc"
FINAL_BUNDLE = "38b98ca6258133036ded9e3cb72894f4181d4b6faa46af9e96a2128ab25c9df2"
ROOT = "unit:o012-rbt-u022"
SOURCE_RIGHTS = "rights:o012-units-001-022-composite-cc-by-4.0"
FINAL_RIGHTS = "rights:o012-units-001-022-composite-cc-by-4.0-final-0857"
BUILD_ID = "qa:o012-units-001-022-build"
VISUAL_ID = "qa:o012-units-001-022-visual"
MANIFEST_ID = "artifact:o012-units-001-022-manifest"
ARTIFACTS = {
    "artifact:o012-units-001-022-build-script": (
        "scripts/build-units-001-022.ps1", 18956,
        "6d3ada82dbc5afbcec8b394c64694e392ceae55db165a8363d88b8c57b1464b7"),
    "artifact:o012-units-001-022-html": (
        "output/html/units-001-022/index.html", 3520527,
        "15938aac7515e4ad7de66f8cf2d825744f9eb08b654165b835bfeace31aef8f4"),
    "artifact:o012-units-001-022-pdf": (
        "output/pdf/topologi-aljabar-unit-001-022-id.pdf", 1728316,
        "5dabcbdc98fdc7203ca2fe4f42aff86b9e3cb761136f676e0dd43b350768fb77"),
    MANIFEST_ID: (
        "output/ARTIFACT_MANIFEST_UNITS_001_022.csv", 249,
        "3a79a520d0281504edd2449fdfd13c5a874ec675f8187a9e6cb516a760ef35c8"),
    "artifact:o012-units-001-022-build-receipt": (
        "qa/UNITS_001_022_BUILD_RECEIPT.json", 5315,
        "347569120a698d2738472fb6d194fa6109f8b638b9e16b08c473fc9e793312b5"),
    "artifact:o012-units-001-022-visual-receipt": (
        "qa/UNITS_001_022_VISUAL_QA.md", 4747,
        "35a5b00b6bdda6b77041ff568f14c91702818be3f939d9e3df36829ae168251b"),
}
RELATION_IDS = {
    "relation:boundary:o012-units-001-022-build",
    "relation:contains:o012-units-001-022-manifest:html",
    "relation:contains:o012-units-001-022-manifest:pdf",
    "relation:depends-on:o012-units-001-022-build:builder",
    "relation:qa:o012-units-001-022-build",
    "relation:qa:o012-units-001-022-visual",
}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8") + b"\n"


def load_generic():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_validator_u022_cumulative", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic validator")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
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
    if prefix_bundle.hexdigest() != PREFIX_BUNDLE:
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
                or record["unit_id"] != ROOT
                or "OpenAI Codex gpt-5.6-sol, Ultra" not in record["toolchain"]):
            raise SystemExit(f"cumulative artifact binding mismatch: {ident}")
    receipt = json.loads((LANE / "qa/UNITS_001_022_BUILD_RECEIPT.json").read_text(
        encoding="utf-8"))
    if (receipt.get("status") != "PASS"
            or receipt.get("source_authority", {}).get("unit_022_sha256") !=
            "0857e51568d77c811d5d79255ac75bfddc87a04b27356ae457d4e66eeffb7d0d"
            or receipt.get("source_authority", {}).get("unit_022_span_sha256") !=
            "86275c590cfcdf8519d3ce8d077fc48619bb94c3fdf039ca805ae4b7df995b7f"
            or receipt.get("toolchain", {}).get("builder_sha256") != ARTIFACTS[
                "artifact:o012-units-001-022-build-script"][2]
            or receipt.get("artifacts", {}).get("pdf", {}).get("pages") != 261
            or receipt.get("html_checks", {}).get("unit_022_ids") != 75
            or receipt.get("html_checks", {}).get("raw_tex_math_fallbacks") != 0
            or receipt.get("toolchain", {}).get("model_provenance") !=
            "OpenAI Codex gpt-5.6-sol, Ultra"):
        raise SystemExit("build receipt semantic/QA binding mismatch")
    reproducibility = receipt["reproducibility"]
    if not all(reproducibility.get(key) for key in (
            "html_two_builds_byte_identical", "pdf_two_builds_byte_identical",
            "source_and_baseline_inputs_fail_closed", "pandoc_html_warnings_are_fatal")):
        raise SystemExit("build reproducibility gate mismatch")
    manifest_text = (LANE / ARTIFACTS[MANIFEST_ID][0]).read_text(encoding="utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(manifest_text)))
    expected_rows = {
        (ARTIFACTS["artifact:o012-units-001-022-html"][0], "3520527",
         ARTIFACTS["artifact:o012-units-001-022-html"][2]),
        (ARTIFACTS["artifact:o012-units-001-022-pdf"][0], "1728316",
         ARTIFACTS["artifact:o012-units-001-022-pdf"][2]),
    }
    if (not rows or list(rows[0]) != ["path", "bytes", "sha256"] or
            {(row["path"], row["bytes"], row["sha256"]) for row in rows} != expected_rows):
        raise SystemExit("manifest row closure mismatch")
    visual = (LANE / ARTIFACTS["artifact:o012-units-001-022-visual-receipt"][0]).read_text(
        encoding="utf-8")
    if ("Status: **PASS**" not in visual or "261 A4 pages" not in visual
            or "OpenAI Codex gpt-5.6-sol, Ultra" not in visual):
        raise SystemExit("visual receipt gate mismatch")

    rights = by_id[FINAL_RIGHTS]
    if (rights["supersedes"] != SOURCE_RIGHTS
            or rights["component_scope"] != [
                f"unit:o012-rbt-u{number:03d}" for number in range(1, 23)]
            or rights["license_expression"] != "CC-BY-4.0"):
        raise SystemExit("final built-rights pointer mismatch")
    if by_id[BUILD_ID]["result"] != "passed" or by_id[VISUAL_ID]["result"] != "passed":
        raise SystemExit("cumulative QA events not passed")
    if set(by_id[BUILD_ID]["witness_artifact_ids"]) != {
            "artifact:o012-units-001-022-build-script",
            "artifact:o012-units-001-022-html",
            "artifact:o012-units-001-022-pdf", MANIFEST_ID,
            "artifact:o012-units-001-022-build-receipt"}:
        raise SystemExit("build QA witness closure mismatch")
    if set(by_id[VISUAL_ID]["witness_artifact_ids"]) != {
            "artifact:o012-units-001-022-pdf",
            "artifact:o012-units-001-022-visual-receipt"}:
        raise SystemExit("visual QA witness closure mismatch")

    bundle = hashlib.sha256()
    for name in FILES:
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(raw_by_file[name])
    if bundle.hexdigest() != FINAL_BUNDLE:
        raise SystemExit("final backend bundle mismatch")
    output = {
        "status": "PASS", "prefix_records": 3322, "prefix_bytes": 3166412,
        "prefix_bundle_sha256": PREFIX_BUNDLE, "prefix_preserved_byte_for_byte": True,
        "new_records": sum(APPEND_COUNTS.values()), "total_records": len(records),
        "backend_bytes": sum(len(raw) for raw in raw_by_file.values()),
        "backend_bundle_sha256": bundle.hexdigest(),
        "records_added_by_file": APPEND_COUNTS,
        "records": {name: len(by_file[name]) for name in FILES},
        "per_file_bytes": {name: len(raw_by_file[name]) for name in FILES},
        "per_file_sha256": {name: digest(raw_by_file[name]) for name in FILES},
        "artifacts": {ident: {"path": spec[0], "bytes": spec[1], "sha256": spec[2]}
                      for ident, spec in ARTIFACTS.items()},
    }
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
