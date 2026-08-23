#!/usr/bin/env python3
"""Append the verified cumulative Units 001--021 build boundary.

The complete 3,096-record Unit 021 source backend is an immutable prefix.
This producer freezes the deterministic builder, HTML/PDF readers, manifest,
build receipt, and visual receipt before it appends canonical sorted JSONL
records. It fails before every write if any authority or prefix byte differs.
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
ROOT = "unit:o012-rbt-u021"
SOURCE_RIGHTS = "rights:o012-units-001-021-composite-cc-by-4.0"
FINAL_RIGHTS = "rights:o012-units-001-021-composite-cc-by-4.0-final-47fa"
FILES = (
    "artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
    "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
    "segments.jsonl", "terms.jsonl", "units.jsonl",
)
PREFIX = {
    "artifacts.jsonl": (100, 78379, "f52ad11802bb22255344b1a01b35378a69f6d4eb26cfae3e1abe4890082a85bd"),
    "assets.jsonl": (23, 14215, "623f8d7948504405fb8f57379987136e5f89297f0152f3eb9408cab6a3ed153c"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (289, 90816, "b05d4ec9646338ea76991eb08d5a260a087699a76d51fde507b0c5583b5921bb"),
    "corrections.jsonl": (288, 280684, "7c06a04c7072051d28879297291d37bccca70c132339c8226e889701dc1de835"),
    "qa.jsonl": (97, 55033, "621ec0d75a3307b8acec242220c0fc39c06a4c978c89378405b4f9661f569c79"),
    "relations.jsonl": (278, 111666, "a262f8db2f816e7a1155b5749e1b18199bb1d62b7e232e9e8ee9ba365e3dbc3d"),
    "rights.jsonl": (54, 48609, "f217f667ddb845de00ce819f6facefdef0247305968d209d4b2422cdb25108b0"),
    "segments.jsonl": (830, 982695, "e3fc479798493bad011f36e302cd4da7b0daa48f45252d7095dc10adc50b3530"),
    "terms.jsonl": (282, 171661, "f6bb58da10c5970087c4ff2074b25163a3a3bd6e0f820f9df0782a4e00490deb"),
    "units.jsonl": (851, 1050067, "7851c5a529337802a6eb62f7aa51d107c38e18ecf8299fcfc86d6dc5b87c46a6"),
}
PREFIX_BUNDLE = "84920281207fc4088aa4f1f812d78333fd530e9f157eeebaa3b09cbfb53b431d"
BUILD_ID = "qa:o012-units-001-021-build"
VISUAL_ID = "qa:o012-units-001-021-visual"
MANIFEST_ID = "artifact:o012-units-001-021-manifest"
ARTIFACTS = {
    "artifact:o012-units-001-021-build-script": (
        "scripts/build-units-001-021.ps1", 17129,
        "f0678ae5af4d08059747106a9711a3a63139dc3782a36de28d2041643e075eec",
        "text/plain; charset=utf-8", "source_frozen", [BUILD_ID], None),
    "artifact:o012-units-001-021-html": (
        "output/html/units-001-021/index.html", 3306661,
        "aec7e94d3697a7feeae87134da983c59faaf29dc8d961bca28b6bfa9c53cdfa6",
        "text/html; charset=utf-8", "built", [BUILD_ID], MANIFEST_ID),
    "artifact:o012-units-001-021-pdf": (
        "output/pdf/topologi-aljabar-unit-001-021-id.pdf", 1645350,
        "aee3f74109bafd1614d01d6593b8b2edbcbfdbf3b841b6beee878a01d7ddec16",
        "application/pdf", "built", [BUILD_ID, VISUAL_ID], MANIFEST_ID),
    MANIFEST_ID: (
        "output/ARTIFACT_MANIFEST_UNITS_001_021.csv", 249,
        "40386b62066854272e8902c1f2c886a78de2c98f0dce845cbf6179c845bf1498",
        "text/csv; charset=utf-8", "built", [BUILD_ID], None),
    "artifact:o012-units-001-021-build-receipt": (
        "qa/UNITS_001_021_BUILD_RECEIPT.json", 3850,
        "e3afdb61c3787eac1b84601609a89eadb34e9eee5b9c5481ba18c5e441a51032",
        "application/json", "built", [BUILD_ID], None),
    "artifact:o012-units-001-021-visual-receipt": (
        "qa/UNITS_001_021_VISUAL_QA.md", 3350,
        "f42bc668ab68a3f05993ac4d56a565160f4a94a417f656dd3f29f1e12475c6fa",
        "text/markdown; charset=utf-8", "visually_checked", [VISUAL_ID], None),
}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(
        obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8") + b"\n"


def common(kind: str, ident: str) -> dict[str, Any]:
    return {
        "entity_type": kind, "id": ident, "schema": SCHEMA,
        "schema_version": VERSION, "status": "active", "supersedes": None,
        "timestamp": STAMP, "workflow": WORKFLOW,
    }


def load_generic():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_validator", path)
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
    receipt = json.loads(
        (LANE / "qa/UNITS_001_021_BUILD_RECEIPT.json").read_text(encoding="utf-8")
    )
    if receipt.get("status") != "PASS":
        raise SystemExit("cumulative build receipt is not PASS")
    if receipt.get("source_authority", {}).get("unit_021_sha256") != (
        "47fa3994dc59370fc464e9d150d62512a4602a3cffa5996f1027f93a427e0eec"
    ):
        raise SystemExit("build receipt is not bound to final Unit 021")
    if receipt.get("toolchain", {}).get("builder_sha256") != (
        "f0678ae5af4d08059747106a9711a3a63139dc3782a36de28d2041643e075eec"
    ):
        raise SystemExit("build receipt builder identity mismatch")
    reproducibility = receipt.get("reproducibility", {})
    if not (reproducibility.get("html_two_builds_byte_identical")
            and reproducibility.get("pdf_two_builds_byte_identical")
            and reproducibility.get("source_and_baseline_inputs_fail_closed")):
        raise SystemExit("build receipt reproducibility gate failed")
    declared = receipt.get("artifacts", {})
    expected = {
        "html": (3306661, "aec7e94d3697a7feeae87134da983c59faaf29dc8d961bca28b6bfa9c53cdfa6"),
        "pdf": (1645350, "aee3f74109bafd1614d01d6593b8b2edbcbfdbf3b841b6beee878a01d7ddec16"),
        "manifest": (249, "40386b62066854272e8902c1f2c886a78de2c98f0dce845cbf6179c845bf1498"),
    }
    for key, (size, sha) in expected.items():
        if (declared.get(key, {}).get("bytes"), declared.get(key, {}).get("sha256")) != (size, sha):
            raise SystemExit(f"build receipt {key} identity mismatch")
    if declared.get("pdf", {}).get("pages") != 246:
        raise SystemExit("build receipt PDF page count is not 246")
    visual = (LANE / "qa/UNITS_001_021_VISUAL_QA.md").read_text(encoding="utf-8")
    if "Status: **PASS**" not in visual or "246 A4 pages" not in visual:
        raise SystemExit("visual receipt is not the expected PASS/246-page boundary")
    manifest = (LANE / "output/ARTIFACT_MANIFEST_UNITS_001_021.csv").read_text(
        encoding="utf-8-sig"
    )
    rows = list(csv.DictReader(io.StringIO(manifest)))
    expected_rows = {
        ("output/html/units-001-021/index.html", "3306661",
         "aec7e94d3697a7feeae87134da983c59faaf29dc8d961bca28b6bfa9c53cdfa6"),
        ("output/pdf/topologi-aljabar-unit-001-021-id.pdf", "1645350",
         "aee3f74109bafd1614d01d6593b8b2edbcbfdbf3b841b6beee878a01d7ddec16"),
    }
    if (rows and list(rows[0]) != ["path", "bytes", "sha256"]) or {
        (row["path"], row["bytes"], row["sha256"]) for row in rows
    } != expected_rows:
        raise SystemExit("cumulative manifest content mismatch")


def main() -> int:
    verify_artifacts()
    raws: dict[str, bytes] = {}
    tables: dict[str, list[dict[str, Any]]] = {}
    prefix_bundle = hashlib.sha256()
    all_ids: set[str] = set()
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        count, size, expected = PREFIX[name]
        lines = raw.splitlines(keepends=True)
        if (len(raw), digest(raw), len(lines)) != (size, expected, count):
            raise SystemExit(f"immutable Unit 021 prefix mismatch: {name}")
        if b"\r" in raw or not raw.endswith(b"\n"):
            raise SystemExit(f"invalid historical newline form: {name}")
        parsed: list[dict[str, Any]] = []
        for number, line in enumerate(lines, 1):
            obj = json.loads(line.decode("utf-8"))
            if canon(obj) != line or not isinstance(obj.get("id"), str):
                raise SystemExit(f"noncanonical historical record: {name}:{number}")
            if obj["id"] in all_ids:
                raise SystemExit(f"duplicate historical ID: {obj['id']}")
            all_ids.add(obj["id"])
            parsed.append(obj)
        raws[name] = raw
        tables[name] = parsed
        prefix_bundle.update(name.encode("utf-8"))
        prefix_bundle.update(b"\0")
        prefix_bundle.update(raw)
    if prefix_bundle.hexdigest() != PREFIX_BUNDLE:
        raise SystemExit("immutable Unit 021 prefix bundle mismatch")
    if ROOT not in all_ids or SOURCE_RIGHTS not in all_ids:
        raise SystemExit("Unit 021 root or source-stage cumulative rights missing")

    additions: dict[str, list[dict[str, Any]]] = {name: [] for name in FILES}
    pending: set[str] = set()

    def add(name: str, obj: dict[str, Any]) -> None:
        if obj["id"] in all_ids or obj["id"] in pending:
            raise SystemExit(f"duplicate appended ID: {obj['id']}")
        pending.add(obj["id"])
        additions[name].append(obj)

    rights = common("rights", FINAL_RIGHTS)
    rights.update({
        "attribution": "Cumulative Roberts Units 001-021 Indonesian reader and deterministic build artifacts.",
        "change_notice": "Verified cumulative HTML/PDF build boundary; component-level rights and attribution records remain controlling.",
        "component_scope": [f"unit:o012-rbt-u{number:03d}" for number in range(1, 22)],
        "license_expression": "CC-BY-4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "non_endorsement": "Independent edition; no source-author endorsement.",
        "supersedes": SOURCE_RIGHTS,
        "third_party_status": "Component-scoped rights records control.",
    })
    add("rights.jsonl", rights)

    toolchain = (
        "Deterministic Units 001-021 builder; Pandoc 3.9.0.2; MiKTeX "
        "pdfTeX-1.40.29; SOURCE_DATE_EPOCH=1787443200."
    )
    for ident, (relative, size, sha, media, state, qas, manifest) in ARTIFACTS.items():
        artifact = common("artifact", ident)
        artifact.update({
            "bytes": size, "locale": "id-ID", "manifest_artifact_id": manifest,
            "media_type": media, "path": relative, "qa_event_ids": qas,
            "rights_component_id": FINAL_RIGHTS, "sha256": sha,
            "toolchain": toolchain, "translation_state": state, "unit_id": ROOT,
        })
        add("artifacts.jsonl", artifact)

    build = common("qa_event", BUILD_ID)
    build.update({
        "note": "Cumulative Units 001-021 HTML and PDF passed fail-closed inputs, two-build byte identity, exact manifest, offline HTML, MathML, fragment, font, and privacy gates.",
        "qa_type": "build", "result": "passed", "unit_id": ROOT,
        "witness_artifact_ids": [
            "artifact:o012-units-001-021-build-script",
            "artifact:o012-units-001-021-html",
            "artifact:o012-units-001-021-pdf",
            MANIFEST_ID,
            "artifact:o012-units-001-021-build-receipt",
        ],
    })
    add("qa.jsonl", build)
    visual = common("qa_event", VISUAL_ID)
    visual.update({
        "note": "Representative visual QA passed on seven pages of the 246-page A4 PDF after the recorded builder-only multiline-link repair; no inspected clipping, overlap, broken glyph, or positional-figure dependence.",
        "qa_type": "visual", "result": "passed", "unit_id": ROOT,
        "witness_artifact_ids": [
            "artifact:o012-units-001-021-pdf",
            "artifact:o012-units-001-021-visual-receipt",
        ],
    })
    add("qa.jsonl", visual)

    def relation(ident: str, source: str, kind: str, target: str, note: str) -> None:
        record = common("relation", ident)
        record.update({"from_id": source, "note": note,
                       "relation_type": kind, "to_id": target})
        add("relations.jsonl", record)

    relation("relation:boundary:o012-units-001-021-build", FINAL_RIGHTS, "contains",
             "artifact:o012-units-001-021-pdf",
             "Final cumulative Units 001-021 build boundary points to the verified PDF reader.")
    relation("relation:contains:o012-units-001-021-manifest:html", MANIFEST_ID, "contains",
             "artifact:o012-units-001-021-html", "Manifest entry for the cumulative HTML reader.")
    relation("relation:contains:o012-units-001-021-manifest:pdf", MANIFEST_ID, "contains",
             "artifact:o012-units-001-021-pdf", "Manifest entry for the cumulative PDF reader.")
    relation("relation:depends-on:o012-units-001-021-build:builder", BUILD_ID, "depends-on",
             "artifact:o012-units-001-021-build-script",
             "The cumulative build QA depends on the frozen deterministic builder.")
    relation("relation:qa:o012-units-001-021-build", BUILD_ID, "illustrates",
             "artifact:o012-units-001-021-build-receipt",
             "Build QA event is witnessed by its exact receipt.")
    relation("relation:qa:o012-units-001-021-visual", VISUAL_ID, "illustrates",
             "artifact:o012-units-001-021-visual-receipt",
             "Visual QA event is witnessed by its exact receipt.")

    merged_records = [record for name in FILES for record in tables[name]] + [
        record for name in FILES for record in additions[name]
    ]
    merged_ids = {record["id"] for record in merged_records}
    if len(merged_ids) != len(merged_records):
        raise SystemExit("global ID collision in proposed backend")
    generic = load_generic()
    generic.validate_shapes(merged_records)
    generic.validate_references(merged_records, {record["id"]: record for record in merged_records})

    output: dict[str, bytes] = {}
    for name in FILES:
        if (BACKEND / name).read_bytes() != raws[name]:
            raise SystemExit(f"historical prefix changed before write: {name}")
        suffix = b"".join(canon(obj) for obj in sorted(additions[name], key=lambda obj: obj["id"]))
        output[name] = raws[name] + suffix
    for name in FILES:
        (BACKEND / name).write_bytes(output[name])

    bundle = hashlib.sha256()
    for name in FILES:
        bundle.update(name.encode("utf-8"))
        bundle.update(b"\0")
        bundle.update(output[name])
    delta = {name: len(additions[name]) for name in FILES}
    print("Cumulative Units 001-021 backend append: PASS")
    print("new_records_by_file=" + json.dumps(delta, sort_keys=True))
    print(f"new_records={sum(delta.values())}")
    print(f"backend_bytes={sum(len(raw) for raw in output.values())}")
    print(f"backend_bundle_sha256={bundle.hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
