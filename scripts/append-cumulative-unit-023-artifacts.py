#!/usr/bin/env python3
"""Append the verified cumulative Units 001--023 build boundary.

The complete 3,513-record Unit 23 semantic backend is immutable.  This
producer verifies that exact prefix and all six frozen build witnesses before
adding only cumulative artifact, QA, relation, and final-rights records.
"""
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
SCHEMA = "curriculum.interop"
VERSION = "0.1.0"
WORKFLOW = "o012-d60-id-reader-production"
STAMP = "2026-08-24T00:00:00Z"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
ROOT = "unit:o012-rbt-u023"
SOURCE_RIGHTS = "rights:o012-units-001-023-composite-cc-by-4.0"
FINAL_RIGHTS = "rights:o012-units-001-023-composite-cc-by-4.0-final-6f05"
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
PREFIX_RECORDS = 3513
PREFIX_BYTES = 3424912
PREFIX_BUNDLE = "2b31536824cea66fc186bd653354eea4eea45f9c68da7992a45d037c782672dc"
BUILD_ID = "qa:o012-units-001-023-build"
VISUAL_ID = "qa:o012-units-001-023-visual"
MANIFEST_ID = "artifact:o012-units-001-023-manifest"
BUILD_RECEIPT_PATH = "qa/UNITS_001_023_BUILD_RECEIPT.json"
VISUAL_RECEIPT_PATH = "qa/UNITS_001_023_VISUAL_QA.md"
EXPECTED_PAGES = 273

# ident -> (path, bytes, sha256, media_type, state, qa_ids, manifest_id)
ARTIFACTS: dict[str, tuple[str, int, str, str, str, list[str], str | None]] = {
    "artifact:o012-units-001-023-build-script": (
        "scripts/build-units-001-023.ps1", 19688,
        "2fd88a027775678ec359037923df604ecb2444e527ba8bda61731f68a6691f88",
        "text/plain; charset=utf-8", "source_frozen", [BUILD_ID], None),
    "artifact:o012-units-001-023-html": (
        "output/html/units-001-023/index.html", 3707037,
        "536fbe19e295424d12198bf1b221be3e2f0170f87fa810a9125bcca9f742264b",
        "text/html; charset=utf-8", "built", [BUILD_ID], MANIFEST_ID),
    "artifact:o012-units-001-023-pdf": (
        "output/pdf/topologi-aljabar-unit-001-023-id.pdf", 1801983,
        "e51aa739eefaa12f4b1d7a4fe99073c525775f113aa62e4506395a01fe1fcbaf",
        "application/pdf", "built", [BUILD_ID, VISUAL_ID], MANIFEST_ID),
    MANIFEST_ID: (
        "output/ARTIFACT_MANIFEST_UNITS_001_023.csv", 249,
        "f12629f0929eeec100c6fc769c239c64bcc1fb72283be4abee9daec691561f34",
        "text/csv; charset=utf-8", "built", [BUILD_ID], None),
    "artifact:o012-units-001-023-build-receipt": (
        "qa/UNITS_001_023_BUILD_RECEIPT.json", 5775,
        "a09fde0e147756c35fe4ba9ff5a212625bdbe96d19400409b14214e67afb4cf8",
        "application/json", "built", [BUILD_ID], None),
    "artifact:o012-units-001-023-visual-receipt": (
        "qa/UNITS_001_023_VISUAL_QA.md", 4278,
        "784bc1b77b65e3e91c1de34a2e14d42a2202861a04e24f8eb3c130f480dbd35e",
        "text/markdown; charset=utf-8", "visually_checked", [VISUAL_ID], None),
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
    spec = importlib.util.spec_from_file_location("o012_generic_u023_build", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
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


def verify_artifacts() -> dict[str, Any]:
    if set(ARTIFACTS) != expected_artifact_ids() or EXPECTED_PAGES <= 0:
        raise SystemExit("cumulative Unit 23 artifact identities are not admitted")
    for _ident, (relative, size, expected, _media, _state, _qas, _manifest) in ARTIFACTS.items():
        raw = (LANE / relative).read_bytes()
        if len(raw) != size or digest(raw) != expected:
            raise SystemExit(f"cumulative artifact mismatch: {relative}")
    receipt = json.loads((LANE / BUILD_RECEIPT_PATH).read_text(encoding="utf-8"))
    source = receipt.get("source_authority", {})
    toolchain = receipt.get("toolchain", {})
    reproducibility = receipt.get("reproducibility", {})
    builder_sha = ARTIFACTS["artifact:o012-units-001-023-build-script"][2]
    if (receipt.get("status") != "PASS"
            or source.get("unit_023_span") != "4939-5112"
            or source.get("unit_023_span_bytes") != 9776
            or source.get("unit_023_span_sha256") !=
            "c7256a45621ad7a435277867298e4aeb8eb584dfce066cdae3b48c4ee0e0e3f4"
            or source.get("unit_023_sha256") !=
            "6f05ddbe6a720109797976c6929b0535f21a38353673cb42d9646a3196f56bd2"
            or toolchain.get("builder_sha256") != builder_sha
            or toolchain.get("model_provenance") != MODEL
            or not reproducibility.get("html_two_builds_byte_identical")
            or not reproducibility.get("pdf_two_builds_byte_identical")
            or not reproducibility.get("source_baseline_and_unit_023_evidence_fail_closed")):
        raise SystemExit("cumulative build receipt binding/reproducibility mismatch")
    declared = receipt.get("artifacts", {})
    artifact_keys = {
        "html": "artifact:o012-units-001-023-html",
        "pdf": "artifact:o012-units-001-023-pdf",
        "manifest": MANIFEST_ID,
    }
    for key, ident in artifact_keys.items():
        spec = ARTIFACTS[ident]
        if (declared.get(key, {}).get("bytes"), declared.get(key, {}).get("sha256")) != (spec[1], spec[2]):
            raise SystemExit(f"build receipt {key} identity mismatch")
    html_checks = receipt.get("html_checks", {})
    if (declared.get("pdf", {}).get("pages") != EXPECTED_PAGES
            or html_checks.get("raw_tex_math_fallbacks") != 0
            or html_checks.get("missing_unit_023_ids") != 0
            or html_checks.get("unit_023_ids") != 51):
        raise SystemExit("cumulative structural/PDF gate mismatch")
    visual = (LANE / VISUAL_RECEIPT_PATH).read_text(encoding="utf-8")
    if ("Status: **PASS**" not in visual or MODEL not in visual
            or str(EXPECTED_PAGES) not in visual):
        raise SystemExit("visual receipt is not the expected PASS/page boundary")
    manifest_path = ARTIFACTS[MANIFEST_ID][0]
    manifest = (LANE / manifest_path).read_text(encoding="utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(manifest)))
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
            raise SystemExit(f"immutable Unit 23 semantic prefix mismatch: {name}")
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
    if (sum(item[0] for item in PREFIX.values()) != PREFIX_RECORDS
            or sum(item[1] for item in PREFIX.values()) != PREFIX_BYTES
            or bundle.hexdigest() != PREFIX_BUNDLE
            or ROOT not in all_ids or SOURCE_RIGHTS not in all_ids):
        raise SystemExit("Unit 23 semantic prefix bundle/root/rights mismatch")

    additions: dict[str, list[dict[str, Any]]] = {name: [] for name in FILES}
    pending: set[str] = set()

    def add(name: str, obj: dict[str, Any]) -> None:
        if obj["id"] in all_ids or obj["id"] in pending:
            raise SystemExit(f"duplicate appended ID: {obj['id']}")
        pending.add(obj["id"]); additions[name].append(obj)

    rights = common("rights", FINAL_RIGHTS)
    rights.update({
        "attribution": "Cumulative Roberts Units 001-023 Indonesian reader and deterministic build artifacts.",
        "change_notice": "Verified cumulative HTML/PDF build boundary; component-level rights and attribution records remain controlling.",
        "component_scope": [f"unit:o012-rbt-u{number:03d}" for number in range(1, 24)],
        "license_expression": "CC-BY-4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "non_endorsement": "Independent edition; no source-author endorsement.",
        "supersedes": SOURCE_RIGHTS,
        "third_party_status": "Component-scoped rights records control.",
    })
    add("rights.jsonl", rights)
    toolchain = receipt.get("toolchain", {})
    toolchain_note = ("Deterministic Units 001-023 builder; "
                      f"{toolchain.get('pandoc', 'Pandoc version recorded in build receipt')}; "
                      f"PDF engine {toolchain.get('pdf_engine', 'recorded in build receipt')}; "
                      f"{MODEL}.")
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
        "note": "Cumulative Units 001-023 HTML and PDF passed fail-closed inputs, two-build byte identity, exact manifest, offline HTML, MathML, fragment, font, privacy, and source-binding gates.",
        "qa_type": "build", "result": "passed", "unit_id": ROOT,
        "witness_artifact_ids": [
            "artifact:o012-units-001-023-build-script",
            "artifact:o012-units-001-023-html",
            "artifact:o012-units-001-023-pdf", MANIFEST_ID,
            "artifact:o012-units-001-023-build-receipt"],
    })
    add("qa.jsonl", build)
    visual = common("qa_event", VISUAL_ID)
    visual.update({
        "note": f"Representative visual QA passed for the {EXPECTED_PAGES}-page A4 PDF; no recorded clipping, overlap, broken glyph, or positional-only mathematical dependency.",
        "qa_type": "visual", "result": "passed", "unit_id": ROOT,
        "witness_artifact_ids": ["artifact:o012-units-001-023-pdf",
                                 "artifact:o012-units-001-023-visual-receipt"],
    })
    add("qa.jsonl", visual)

    def relation(ident: str, source: str, kind: str, target: str, note: str) -> None:
        record = common("relation", ident)
        record.update({"from_id": source, "note": note,
                       "relation_type": kind, "to_id": target})
        add("relations.jsonl", record)
    relation("relation:boundary:o012-units-001-023-build", FINAL_RIGHTS, "contains",
             "artifact:o012-units-001-023-pdf",
             "Final cumulative Units 001-023 build boundary points to the verified PDF reader.")
    relation("relation:contains:o012-units-001-023-manifest:html", MANIFEST_ID, "contains",
             "artifact:o012-units-001-023-html", "Manifest entry for the cumulative HTML reader.")
    relation("relation:contains:o012-units-001-023-manifest:pdf", MANIFEST_ID, "contains",
             "artifact:o012-units-001-023-pdf", "Manifest entry for the cumulative PDF reader.")
    relation("relation:depends-on:o012-units-001-023-build:builder", BUILD_ID, "depends-on",
             "artifact:o012-units-001-023-build-script",
             "The cumulative build QA depends on the frozen deterministic builder.")
    relation("relation:qa:o012-units-001-023-build", BUILD_ID, "illustrates",
             "artifact:o012-units-001-023-build-receipt",
             "Build QA event is witnessed by its exact receipt.")
    relation("relation:qa:o012-units-001-023-visual", VISUAL_ID, "illustrates",
             "artifact:o012-units-001-023-visual-receipt",
             "Visual QA event is witnessed by its exact receipt.")

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
    print("Cumulative Units 001-023 backend append: PASS")
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
