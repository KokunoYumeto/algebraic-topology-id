#!/usr/bin/env python3
"""Append the verified cumulative Units 001--022 build boundary.

The complete 3,322-record Unit 22 semantic backend is immutable.  This
producer verifies that exact prefix and all six build witnesses before adding
only cumulative artifact, QA, relation, and final-rights records.
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
STAMP = "2026-08-23T00:00:00Z"
ROOT = "unit:o012-rbt-u022"
SOURCE_RIGHTS = "rights:o012-units-001-022-composite-cc-by-4.0"
FINAL_RIGHTS = "rights:o012-units-001-022-composite-cc-by-4.0-final-0857"
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
PREFIX_BUNDLE = "2329606117578210ce927123ec01639390f2e493fcc995899606eaa38996f2bc"
BUILD_ID = "qa:o012-units-001-022-build"
VISUAL_ID = "qa:o012-units-001-022-visual"
MANIFEST_ID = "artifact:o012-units-001-022-manifest"
ARTIFACTS = {
    "artifact:o012-units-001-022-build-script": (
        "scripts/build-units-001-022.ps1", 18956,
        "6d3ada82dbc5afbcec8b394c64694e392ceae55db165a8363d88b8c57b1464b7",
        "text/plain; charset=utf-8", "source_frozen", [BUILD_ID], None),
    "artifact:o012-units-001-022-html": (
        "output/html/units-001-022/index.html", 3520527,
        "15938aac7515e4ad7de66f8cf2d825744f9eb08b654165b835bfeace31aef8f4",
        "text/html; charset=utf-8", "built", [BUILD_ID], MANIFEST_ID),
    "artifact:o012-units-001-022-pdf": (
        "output/pdf/topologi-aljabar-unit-001-022-id.pdf", 1728316,
        "5dabcbdc98fdc7203ca2fe4f42aff86b9e3cb761136f676e0dd43b350768fb77",
        "application/pdf", "built", [BUILD_ID, VISUAL_ID], MANIFEST_ID),
    MANIFEST_ID: (
        "output/ARTIFACT_MANIFEST_UNITS_001_022.csv", 249,
        "3a79a520d0281504edd2449fdfd13c5a874ec675f8187a9e6cb516a760ef35c8",
        "text/csv; charset=utf-8", "built", [BUILD_ID], None),
    "artifact:o012-units-001-022-build-receipt": (
        "qa/UNITS_001_022_BUILD_RECEIPT.json", 5315,
        "347569120a698d2738472fb6d194fa6109f8b638b9e16b08c473fc9e793312b5",
        "application/json", "built", [BUILD_ID], None),
    "artifact:o012-units-001-022-visual-receipt": (
        "qa/UNITS_001_022_VISUAL_QA.md", 4747,
        "35a5b00b6bdda6b77041ff568f14c91702818be3f939d9e3df36829ae168251b",
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
    spec = importlib.util.spec_from_file_location("o012_generic_validator_u022_build", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_artifacts() -> None:
    for _ident, (relative, size, expected, _media, _state, _qas, _manifest) in ARTIFACTS.items():
        raw = (LANE / relative).read_bytes()
        if len(raw) != size or digest(raw) != expected:
            raise SystemExit(f"cumulative artifact mismatch: {relative}")
    receipt = json.loads((LANE / "qa/UNITS_001_022_BUILD_RECEIPT.json").read_text(
        encoding="utf-8"))
    source = receipt.get("source_authority", {})
    toolchain = receipt.get("toolchain", {})
    reproducibility = receipt.get("reproducibility", {})
    if (receipt.get("status") != "PASS"
            or source.get("unit_022_span") != "4501-4938"
            or source.get("unit_022_span_bytes") != 20585
            or source.get("unit_022_span_sha256") !=
            "86275c590cfcdf8519d3ce8d077fc48619bb94c3fdf039ca805ae4b7df995b7f"
            or source.get("unit_022_sha256") !=
            "0857e51568d77c811d5d79255ac75bfddc87a04b27356ae457d4e66eeffb7d0d"
            or toolchain.get("builder_sha256") !=
            "6d3ada82dbc5afbcec8b394c64694e392ceae55db165a8363d88b8c57b1464b7"
            or toolchain.get("model_provenance") != "OpenAI Codex gpt-5.6-sol, Ultra"
            or not reproducibility.get("html_two_builds_byte_identical")
            or not reproducibility.get("pdf_two_builds_byte_identical")
            or not reproducibility.get("source_and_baseline_inputs_fail_closed")):
        raise SystemExit("cumulative build receipt binding/reproducibility mismatch")
    expected = {
        "html": (3520527, "15938aac7515e4ad7de66f8cf2d825744f9eb08b654165b835bfeace31aef8f4"),
        "pdf": (1728316, "5dabcbdc98fdc7203ca2fe4f42aff86b9e3cb761136f676e0dd43b350768fb77"),
        "manifest": (249, "3a79a520d0281504edd2449fdfd13c5a874ec675f8187a9e6cb516a760ef35c8"),
    }
    declared = receipt.get("artifacts", {})
    for key, identity in expected.items():
        if (declared.get(key, {}).get("bytes"), declared.get(key, {}).get("sha256")) != identity:
            raise SystemExit(f"build receipt {key} identity mismatch")
    if (declared.get("pdf", {}).get("pages") != 261
            or receipt.get("html_checks", {}).get("raw_tex_math_fallbacks") != 0
            or receipt.get("html_checks", {}).get("missing_unit_022_ids") != 0):
        raise SystemExit("cumulative structural/PDF gate mismatch")
    visual = (LANE / "qa/UNITS_001_022_VISUAL_QA.md").read_text(encoding="utf-8")
    if ("Status: **PASS**" not in visual or "261 A4 pages" not in visual
            or "OpenAI Codex gpt-5.6-sol, Ultra" not in visual):
        raise SystemExit("visual receipt is not expected PASS/261-page boundary")
    manifest = (LANE / "output/ARTIFACT_MANIFEST_UNITS_001_022.csv").read_text(
        encoding="utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(manifest)))
    expected_rows = {
        ("output/html/units-001-022/index.html", "3520527",
         "15938aac7515e4ad7de66f8cf2d825744f9eb08b654165b835bfeace31aef8f4"),
        ("output/pdf/topologi-aljabar-unit-001-022-id.pdf", "1728316",
         "5dabcbdc98fdc7203ca2fe4f42aff86b9e3cb761136f676e0dd43b350768fb77"),
    }
    if (not rows or list(rows[0]) != ["path", "bytes", "sha256"] or
            {(row["path"], row["bytes"], row["sha256"]) for row in rows} != expected_rows):
        raise SystemExit("cumulative manifest content mismatch")


def main() -> int:
    verify_artifacts()
    raws: dict[str, bytes] = {}
    tables: dict[str, list[dict[str, Any]]] = {}
    all_ids: set[str] = set()
    bundle = hashlib.sha256()
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        count, size, expected = PREFIX[name]
        lines = raw.splitlines(keepends=True)
        if (len(raw), digest(raw), len(lines)) != (size, expected, count):
            raise SystemExit(f"immutable Unit 22 semantic prefix mismatch: {name}")
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
    if bundle.hexdigest() != PREFIX_BUNDLE or ROOT not in all_ids or SOURCE_RIGHTS not in all_ids:
        raise SystemExit("Unit 22 semantic prefix bundle/root/rights mismatch")

    additions: dict[str, list[dict[str, Any]]] = {name: [] for name in FILES}
    pending: set[str] = set()
    def add(name: str, obj: dict[str, Any]) -> None:
        if obj["id"] in all_ids or obj["id"] in pending:
            raise SystemExit(f"duplicate appended ID: {obj['id']}")
        pending.add(obj["id"]); additions[name].append(obj)

    rights = common("rights", FINAL_RIGHTS)
    rights.update({
        "attribution": "Cumulative Roberts Units 001-022 Indonesian reader and deterministic build artifacts.",
        "change_notice": "Verified cumulative HTML/PDF build boundary; component-level rights and attribution records remain controlling.",
        "component_scope": [f"unit:o012-rbt-u{number:03d}" for number in range(1, 23)],
        "license_expression": "CC-BY-4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "non_endorsement": "Independent edition; no source-author endorsement.",
        "supersedes": SOURCE_RIGHTS,
        "third_party_status": "Component-scoped rights records control.",
    })
    add("rights.jsonl", rights)
    toolchain = ("Deterministic Units 001-022 builder; Pandoc 3.9.0.2; MiKTeX "
                 "pdfTeX-1.40.29; SOURCE_DATE_EPOCH=1787443200; "
                 "OpenAI Codex gpt-5.6-sol, Ultra.")
    for ident, (relative, size, sha, media, state, qas, manifest) in ARTIFACTS.items():
        artifact = common("artifact", ident)
        artifact.update({"bytes": size, "locale": "id-ID",
                         "manifest_artifact_id": manifest, "media_type": media,
                         "path": relative, "qa_event_ids": qas,
                         "rights_component_id": FINAL_RIGHTS, "sha256": sha,
                         "toolchain": toolchain, "translation_state": state,
                         "unit_id": ROOT})
        add("artifacts.jsonl", artifact)
    build = common("qa_event", BUILD_ID)
    build.update({
        "note": "Cumulative Units 001-022 HTML and PDF passed fail-closed inputs, two-build byte identity, exact manifest, offline HTML, MathML, fragment, font, privacy, and source-binding gates.",
        "qa_type": "build", "result": "passed", "unit_id": ROOT,
        "witness_artifact_ids": [
            "artifact:o012-units-001-022-build-script",
            "artifact:o012-units-001-022-html",
            "artifact:o012-units-001-022-pdf", MANIFEST_ID,
            "artifact:o012-units-001-022-build-receipt"],
    })
    add("qa.jsonl", build)
    visual = common("qa_event", VISUAL_ID)
    visual.update({
        "note": "Representative visual QA passed on ten pages of the 261-page A4 PDF after the recorded HTML-only semantic-diagram MathML repair; no inspected clipping, overlap, broken glyph, or positional-figure dependence.",
        "qa_type": "visual", "result": "passed", "unit_id": ROOT,
        "witness_artifact_ids": ["artifact:o012-units-001-022-pdf",
                                 "artifact:o012-units-001-022-visual-receipt"],
    })
    add("qa.jsonl", visual)

    def relation(ident: str, source: str, kind: str, target: str, note: str) -> None:
        record = common("relation", ident)
        record.update({"from_id": source, "note": note,
                       "relation_type": kind, "to_id": target})
        add("relations.jsonl", record)
    relation("relation:boundary:o012-units-001-022-build", FINAL_RIGHTS, "contains",
             "artifact:o012-units-001-022-pdf",
             "Final cumulative Units 001-022 build boundary points to the verified PDF reader.")
    relation("relation:contains:o012-units-001-022-manifest:html", MANIFEST_ID, "contains",
             "artifact:o012-units-001-022-html", "Manifest entry for the cumulative HTML reader.")
    relation("relation:contains:o012-units-001-022-manifest:pdf", MANIFEST_ID, "contains",
             "artifact:o012-units-001-022-pdf", "Manifest entry for the cumulative PDF reader.")
    relation("relation:depends-on:o012-units-001-022-build:builder", BUILD_ID, "depends-on",
             "artifact:o012-units-001-022-build-script",
             "The cumulative build QA depends on the frozen deterministic builder.")
    relation("relation:qa:o012-units-001-022-build", BUILD_ID, "illustrates",
             "artifact:o012-units-001-022-build-receipt",
             "Build QA event is witnessed by its exact receipt.")
    relation("relation:qa:o012-units-001-022-visual", VISUAL_ID, "illustrates",
             "artifact:o012-units-001-022-visual-receipt",
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
    for name in FILES:
        final_bundle.update(name.encode()); final_bundle.update(b"\0"); final_bundle.update(outputs[name])
    delta = {name: len(additions[name]) for name in FILES}
    print("Cumulative Units 001-022 backend append: PASS")
    print("new_records_by_file=" + json.dumps(delta, sort_keys=True))
    print(f"new_records={sum(delta.values())}")
    print(f"total_records={sum(PREFIX[name][0] + delta[name] for name in FILES)}")
    print(f"backend_bytes={sum(len(raw) for raw in outputs.values())}")
    print(f"backend_bundle_sha256={final_bundle.hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
