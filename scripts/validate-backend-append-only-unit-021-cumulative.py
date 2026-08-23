#!/usr/bin/env python3
"""Validate the append-only cumulative Units 001--021 build boundary."""
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
APPEND_COUNTS = {
    "artifacts.jsonl": 6, "assets.jsonl": 0, "authority.jsonl": 0,
    "concepts.jsonl": 0, "corrections.jsonl": 0, "qa.jsonl": 2,
    "relations.jsonl": 6, "rights.jsonl": 1, "segments.jsonl": 0,
    "terms.jsonl": 0, "units.jsonl": 0,
}
FINAL = {
    "artifacts.jsonl": (106, 83103, "1708f7276cb28e295d578c8e4411618291c7294c8faee863c89461c63378a978"),
    "assets.jsonl": (23, 14215, "623f8d7948504405fb8f57379987136e5f89297f0152f3eb9408cab6a3ed153c"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (289, 90816, "b05d4ec9646338ea76991eb08d5a260a087699a76d51fde507b0c5583b5921bb"),
    "corrections.jsonl": (288, 280684, "7c06a04c7072051d28879297291d37bccca70c132339c8226e889701dc1de835"),
    "qa.jsonl": (99, 56340, "249c2f6110269d1daef7fff472e4fb17c2f7060b8cd39f662884fd8bba0f0145"),
    "relations.jsonl": (284, 114295, "3a1b930dbe14992819fcaeca39edb96e915641e62247a2e7ea879809a998c2e9"),
    "rights.jsonl": (55, 49832, "1dca76e63699015d393009a8ed263ea4f1adb4e9be3a9668aae8e19bdcf55524"),
    "segments.jsonl": (830, 982695, "e3fc479798493bad011f36e302cd4da7b0daa48f45252d7095dc10adc50b3530"),
    "terms.jsonl": (282, 171661, "f6bb58da10c5970087c4ff2074b25163a3a3bd6e0f820f9df0782a4e00490deb"),
    "units.jsonl": (851, 1050067, "7851c5a529337802a6eb62f7aa51d107c38e18ecf8299fcfc86d6dc5b87c46a6"),
}
BUNDLE_SHA = "cf5acacf3ad2351869297dd8d3827787377422fa30c8c1385e60833b23913db9"
ROOT = "unit:o012-rbt-u021"
SOURCE_RIGHTS = "rights:o012-units-001-021-composite-cc-by-4.0"
FINAL_RIGHTS = "rights:o012-units-001-021-composite-cc-by-4.0-final-47fa"
BUILD_ID = "qa:o012-units-001-021-build"
VISUAL_ID = "qa:o012-units-001-021-visual"
MANIFEST_ID = "artifact:o012-units-001-021-manifest"
EXPECTED_SUFFIX_IDS = {
    "artifacts.jsonl": [
        "artifact:o012-units-001-021-build-receipt",
        "artifact:o012-units-001-021-build-script",
        "artifact:o012-units-001-021-html",
        "artifact:o012-units-001-021-manifest",
        "artifact:o012-units-001-021-pdf",
        "artifact:o012-units-001-021-visual-receipt",
    ],
    "assets.jsonl": [],
    "authority.jsonl": [],
    "concepts.jsonl": [],
    "corrections.jsonl": [],
    "qa.jsonl": [BUILD_ID, VISUAL_ID],
    "relations.jsonl": [
        "relation:boundary:o012-units-001-021-build",
        "relation:contains:o012-units-001-021-manifest:html",
        "relation:contains:o012-units-001-021-manifest:pdf",
        "relation:depends-on:o012-units-001-021-build:builder",
        "relation:qa:o012-units-001-021-build",
        "relation:qa:o012-units-001-021-visual",
    ],
    "rights.jsonl": [FINAL_RIGHTS],
    "segments.jsonl": [],
    "terms.jsonl": [],
    "units.jsonl": [],
}
ARTIFACTS = {
    "artifact:o012-units-001-021-build-script": (
        "scripts/build-units-001-021.ps1", 17129,
        "f0678ae5af4d08059747106a9711a3a63139dc3782a36de28d2041643e075eec",
        None, [BUILD_ID]),
    "artifact:o012-units-001-021-html": (
        "output/html/units-001-021/index.html", 3306661,
        "aec7e94d3697a7feeae87134da983c59faaf29dc8d961bca28b6bfa9c53cdfa6",
        MANIFEST_ID, [BUILD_ID]),
    "artifact:o012-units-001-021-pdf": (
        "output/pdf/topologi-aljabar-unit-001-021-id.pdf", 1645350,
        "aee3f74109bafd1614d01d6593b8b2edbcbfdbf3b841b6beee878a01d7ddec16",
        MANIFEST_ID, [BUILD_ID, VISUAL_ID]),
    MANIFEST_ID: (
        "output/ARTIFACT_MANIFEST_UNITS_001_021.csv", 249,
        "40386b62066854272e8902c1f2c886a78de2c98f0dce845cbf6179c845bf1498",
        None, [BUILD_ID]),
    "artifact:o012-units-001-021-build-receipt": (
        "qa/UNITS_001_021_BUILD_RECEIPT.json", 3850,
        "e3afdb61c3787eac1b84601609a89eadb34e9eee5b9c5481ba18c5e441a51032",
        None, [BUILD_ID]),
    "artifact:o012-units-001-021-visual-receipt": (
        "qa/UNITS_001_021_VISUAL_QA.md", 3350,
        "f42bc668ab68a3f05993ac4d56a565160f4a94a417f656dd3f29f1e12475c6fa",
        None, [VISUAL_ID]),
}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(
        obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8") + b"\n"


def load_generic():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_validator", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    records: list[dict[str, Any]] = []
    by_file: dict[str, list[dict[str, Any]]] = {}
    raw_by_file: dict[str, bytes] = {}
    prefix_bundle = hashlib.sha256()
    final_bundle = hashlib.sha256()
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        raw_by_file[name] = raw
        final_count, final_bytes, final_sha = FINAL[name]
        lines = raw.splitlines(keepends=True)
        if (len(lines), len(raw), digest(raw)) != (final_count, final_bytes, final_sha):
            raise SystemExit(f"final backend identity mismatch: {name}")
        if b"\r" in raw or not raw.endswith(b"\n"):
            raise SystemExit(f"invalid JSONL newline form: {name}")
        prefix_count, prefix_bytes, prefix_sha = PREFIX[name]
        prefix = b"".join(lines[:prefix_count])
        if (len(prefix), digest(prefix)) != (prefix_bytes, prefix_sha):
            raise SystemExit(f"immutable 3,096-record prefix mismatch: {name}")
        suffix = lines[prefix_count:]
        if len(suffix) != APPEND_COUNTS[name]:
            raise SystemExit(f"cumulative append count mismatch: {name}")
        parsed: list[dict[str, Any]] = []
        for number, line in enumerate(lines, 1):
            obj = json.loads(line.decode("utf-8"))
            if not isinstance(obj.get("id"), str) or canon(obj) != line:
                raise SystemExit(f"noncanonical record: {name}:{number}")
            parsed.append(obj)
        ids = [obj["id"] for obj in parsed]
        if len(ids) != len(set(ids)):
            raise SystemExit(f"duplicate IDs: {name}")
        suffix_ids = ids[prefix_count:]
        if suffix_ids != sorted(suffix_ids) or suffix_ids != EXPECTED_SUFFIX_IDS[name]:
            raise SystemExit(f"unexpected or unsorted cumulative suffix: {name}")
        by_file[name] = parsed
        records.extend(parsed)
        prefix_bundle.update(name.encode("utf-8")); prefix_bundle.update(b"\0"); prefix_bundle.update(prefix)
        final_bundle.update(name.encode("utf-8")); final_bundle.update(b"\0"); final_bundle.update(raw)
    if prefix_bundle.hexdigest() != PREFIX_BUNDLE:
        raise SystemExit("immutable prefix bundle mismatch")
    if final_bundle.hexdigest() != BUNDLE_SHA:
        raise SystemExit("final backend bundle mismatch")
    by_id = {obj["id"]: obj for obj in records}
    if len(by_id) != len(records):
        raise SystemExit("duplicate global backend ID")
    generic = load_generic()
    generic.validate_shapes(records)
    generic.validate_references(records, by_id)
    generic.validate_artifact_manifests(records, LANE)

    for ident, (relative, size, sha, manifest, qas) in ARTIFACTS.items():
        raw = (LANE / relative).read_bytes()
        if (len(raw), digest(raw)) != (size, sha):
            raise SystemExit(f"cumulative artifact identity mismatch: {relative}")
        record = by_id.get(ident)
        if (record is None or record.get("path") != relative
                or record.get("bytes") != size or record.get("sha256") != sha
                or record.get("manifest_artifact_id") != manifest
                or record.get("qa_event_ids") != qas
                or record.get("rights_component_id") != FINAL_RIGHTS
                or record.get("unit_id") != ROOT):
            raise SystemExit(f"malformed cumulative artifact record: {ident}")

    manifest_text = (LANE / "output/ARTIFACT_MANIFEST_UNITS_001_021.csv").read_text(
        encoding="utf-8-sig"
    )
    rows = list(csv.DictReader(io.StringIO(manifest_text)))
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

    receipt = json.loads(
        (LANE / "qa/UNITS_001_021_BUILD_RECEIPT.json").read_text(encoding="utf-8")
    )
    if (receipt.get("status") != "PASS"
            or receipt.get("source_authority", {}).get("unit_021_sha256")
            != "47fa3994dc59370fc464e9d150d62512a4602a3cffa5996f1027f93a427e0eec"
            or receipt.get("toolchain", {}).get("builder_sha256")
            != "f0678ae5af4d08059747106a9711a3a63139dc3782a36de28d2041643e075eec"
            or receipt.get("artifacts", {}).get("pdf", {}).get("pages") != 246
            or not receipt.get("reproducibility", {}).get("html_two_builds_byte_identical")
            or not receipt.get("reproducibility", {}).get("pdf_two_builds_byte_identical")):
        raise SystemExit("cumulative build receipt content mismatch")
    visual_text = (LANE / "qa/UNITS_001_021_VISUAL_QA.md").read_text(encoding="utf-8")
    if "Status: **PASS**" not in visual_text or "246 A4 pages" not in visual_text:
        raise SystemExit("cumulative visual receipt content mismatch")

    rights = by_id.get(FINAL_RIGHTS)
    expected_scope = [f"unit:o012-rbt-u{number:03d}" for number in range(1, 22)]
    if (rights is None or rights.get("supersedes") != SOURCE_RIGHTS
            or rights.get("component_scope") != expected_scope
            or rights.get("license_expression") != "CC-BY-4.0"):
        raise SystemExit("final cumulative rights pointer mismatch")
    build = by_id.get(BUILD_ID)
    visual = by_id.get(VISUAL_ID)
    if (build is None or build.get("result") != "passed" or build.get("qa_type") != "build"
            or len(build.get("witness_artifact_ids", [])) != 5):
        raise SystemExit("cumulative build QA event mismatch")
    if (visual is None or visual.get("result") != "passed" or visual.get("qa_type") != "visual"
            or visual.get("witness_artifact_ids") != [
                "artifact:o012-units-001-021-pdf",
                "artifact:o012-units-001-021-visual-receipt",
            ]):
        raise SystemExit("cumulative visual QA event mismatch")
    expected_relations = {
        "relation:boundary:o012-units-001-021-build",
        "relation:contains:o012-units-001-021-manifest:html",
        "relation:contains:o012-units-001-021-manifest:pdf",
        "relation:depends-on:o012-units-001-021-build:builder",
        "relation:qa:o012-units-001-021-build",
        "relation:qa:o012-units-001-021-visual",
    }
    if {obj["id"] for obj in by_file["relations.jsonl"][PREFIX["relations.jsonl"][0]:]} != expected_relations:
        raise SystemExit("cumulative relation closure mismatch")

    result = {
        "status": "PASS",
        "immutable_prefix_records": 3096,
        "immutable_prefix_bytes": 2886546,
        "immutable_prefix_bundle_sha256": PREFIX_BUNDLE,
        "new_records": sum(APPEND_COUNTS.values()),
        "new_records_by_file": APPEND_COUNTS,
        "total_records": sum(count for count, _size, _sha in FINAL.values()),
        "backend_bytes": sum(size for _count, size, _sha in FINAL.values()),
        "backend_bundle_sha256": BUNDLE_SHA,
        "per_file": {
            name: {"records": FINAL[name][0], "bytes": FINAL[name][1],
                   "sha256": FINAL[name][2]} for name in FILES
        },
        "pdf_pages": 246,
        "rights_component_id": FINAL_RIGHTS,
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
