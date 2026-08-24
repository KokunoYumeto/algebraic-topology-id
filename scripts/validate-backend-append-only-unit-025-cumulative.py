#!/usr/bin/env python3
"""Independent validator for the cumulative Units 001--025 backend append.

The validator proves three nested byte boundaries: the immutable Units 001--024
cumulative backend, the exact Unit 25 semantic suffix, and the final 17-record
Unit 25 cumulative build suffix.  It does not import the producing script.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")

UNIT24 = {
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
SEMANTIC = {
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
FINAL = {
    "artifacts.jsonl": (145, 115514, "ac0633eb616f2d0bd412bfb076a482d6ef6a402683d35da67bf6c1ed290ea40e"),
    "assets.jsonl": (27, 16679, "aa569a900426a9e2cfd56777f3e52f07b35a1a72f211847bafd71ec638043462"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (325, 102250, "0ce28594cd511c1a20aff74053b7c74c6c4c6a0505c7c8c5804dd7acd2dae77d"),
    "corrections.jsonl": (332, 327054, "40791f1db8da9ba81083bad0bb4ac183094c3151b9007bb34e5fc637a1790893"),
    "qa.jsonl": (119, 67471, "7b90c07af1561b6356a3249f396a97aaf10265989f4d7ba2b1493f87bac60b93"),
    "relations.jsonl": (397, 162048, "62f67c2ede76bcd24e9ad87db7968dd92649aba6e284c4829042941dd7ea8a50"),
    "rights.jsonl": (71, 65630, "7e54a0f51dd951aecadbc3767173308dc02c12ada6c121b9703c9ec2fb7f2ac7"),
    "segments.jsonl": (1075, 1428116, "d47404ea94dfa7347fbf6f6e0e0e8c5f4fb60e2634c066b87967a4468fff644a"),
    "terms.jsonl": (318, 197648, "dda9013d863bc39ec81f9936167ad24d0cfa2ebba6de0aa2c768743dc09b8503"),
    "units.jsonl": (1100, 1522772, "7fe9d4abfae9389db7cb99240b553d62b66144086c3f2097e9f64d5b2fe14318"),
}
UNIT24_TOTAL = (3723, 3726427, "ffa8c7cb45b6d8170d7bc83df24ec487fd0c2777297b55eff2d5e7b3ae63fe25")
SEMANTIC_TOTAL = (3896, 3996359, "55372b9c2853fa479e731c73c407b234ad2f1219e07efbedbad2a99f1e2abf47")
FINAL_TOTAL = (3913, 4007903, "8b50629f25c5fcbedb6d5547f8f7151c622aa90e04f71583008bd176058a4f78")
SEMANTIC_DELTA = {
    "artifacts.jsonl": 3, "assets.jsonl": 1, "authority.jsonl": 0,
    "concepts.jsonl": 6, "corrections.jsonl": 10, "qa.jsonl": 3,
    "relations.jsonl": 22, "rights.jsonl": 3, "segments.jsonl": 59,
    "terms.jsonl": 6, "units.jsonl": 60,
}
BUILD_DELTA = {
    "artifacts.jsonl": 7, "assets.jsonl": 0, "authority.jsonl": 0,
    "concepts.jsonl": 0, "corrections.jsonl": 0, "qa.jsonl": 2,
    "relations.jsonl": 7, "rights.jsonl": 1, "segments.jsonl": 0,
    "terms.jsonl": 0, "units.jsonl": 0,
}
FINAL_RIGHTS = "rights:o012-units-001-025-composite-cc-by-4.0-final-df72"
SOURCE_RIGHTS = "rights:o012-units-001-025-composite-cc-by-4.0"
BUILD_ID = "qa:o012-units-001-025-build"
VISUAL_ID = "qa:o012-units-001-025-visual"
MANIFEST_ID = "artifact:o012-units-001-025-manifest"
MANIFEST_PATH = "output/ARTIFACT_MANIFEST_UNITS_001_025.csv"
SEMANTIC_RECEIPT = "qa/BACKEND_APPEND_ONLY_UNIT_025_RECEIPT.json"

ARTIFACTS = {
    "artifact:o012-units-001-025-build-script": ("scripts/build-units-001-025.ps1", 21986, "d346b18845f8fc9314ae588fc7877d38275110ab23c60f10b7bad649bc3371c2"),
    "artifact:o012-units-001-025-html": ("output/html/units-001-025/index.html", 4112563, "38cd8437f3b4235ac6269f4e3365123fa06485269d35a424ad4f5ddd589025c1"),
    "artifact:o012-units-001-025-pdf": ("output/pdf/topologi-aljabar-unit-001-025-id.pdf", 1972209, "581d62162633a6624687517c5cf1595f5fc02a2701c2222b279711e0520b9a3f"),
    MANIFEST_ID: (MANIFEST_PATH, 249, "37175a8d7023bf394c50c4809122b1f3244b5d0b1b95a3b724bdb2ff184ab142"),
    "artifact:o012-units-001-025-build-receipt": ("qa/UNITS_001_025_BUILD_RECEIPT.json", 7729, "dd2fa5b52ed84ac939c33cfa5b9f68be4b904b014321abcb54c2ae664d0f9727"),
    "artifact:o012-units-001-025-visual-receipt": ("qa/UNITS_001_025_VISUAL_QA.md", 4804, "ae49496b676472f6c69a3468cc76c323c45905ce7ed86a048ce11556079137a3"),
    "artifact:o012-units-001-025-render-inventory": ("qa/UNITS_001_025_RENDER_INVENTORY.csv", 2731, "a55ff205e621fbc750baaf086fa18883c72dba5bdfe1f66e4554247d22fdc12f"),
}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8") + b"\n"


def load_generic():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_u025_cumulative", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_suffix(raw: bytes, expected_count: int, name: str, label: str) -> list[dict[str, Any]]:
    lines = raw.splitlines(keepends=True)
    if len(lines) != expected_count or b"\r" in raw:
        raise SystemExit(f"{name}: {label} count/newline mismatch")
    objects: list[dict[str, Any]] = []
    ids: list[str] = []
    for line in lines:
        obj = json.loads(line.decode("utf-8"))
        if canon(obj) != line:
            raise SystemExit(f"{name}: noncanonical {label} record")
        objects.append(obj)
        ids.append(obj["id"])
    if ids != sorted(ids) or len(ids) != len(set(ids)):
        raise SystemExit(f"{name}: {label} suffix is not sorted/unique")
    return objects


def verify_witnesses(by_id: dict[str, dict[str, Any]]) -> None:
    if (LANE / "output/units-001-025-manifest.sha256").exists():
        raise SystemExit("unexpected non-authoritative supplied manifest path exists")
    for ident, (path, size, sha) in ARTIFACTS.items():
        raw = (LANE / path).read_bytes()
        record = by_id[ident]
        if (len(raw), digest(raw)) != (size, sha):
            raise SystemExit(f"cumulative witness identity mismatch: {path}")
        if (record["path"], record["bytes"], record["sha256"],
                record["rights_component_id"]) != (path, size, sha, FINAL_RIGHTS):
            raise SystemExit(f"backend artifact binding mismatch: {ident}")
    manifest = list(csv.DictReader(io.StringIO(
        (LANE / MANIFEST_PATH).read_text(encoding="utf-8-sig"))))
    expected = {
        (ARTIFACTS["artifact:o012-units-001-025-html"][0],
         str(ARTIFACTS["artifact:o012-units-001-025-html"][1]),
         ARTIFACTS["artifact:o012-units-001-025-html"][2]),
        (ARTIFACTS["artifact:o012-units-001-025-pdf"][0],
         str(ARTIFACTS["artifact:o012-units-001-025-pdf"][1]),
         ARTIFACTS["artifact:o012-units-001-025-pdf"][2]),
    }
    if {(row["path"], row["bytes"], row["sha256"]) for row in manifest} != expected:
        raise SystemExit("cumulative manifest rows mismatch")
    receipt = json.loads((LANE / "qa/UNITS_001_025_BUILD_RECEIPT.json").read_text(encoding="utf-8"))
    html = receipt.get("html_checks", {})
    pdf = receipt.get("artifacts", {}).get("pdf", {})
    browser = receipt.get("browser_checks", {})
    reproducibility = receipt.get("reproducibility", {})
    if (receipt.get("status") != "PASS"
            or receipt.get("source_authority", {}).get("next_source_line") != 5612
            or not reproducibility.get("html_two_builds_byte_identical")
            or not reproducibility.get("pdf_two_builds_byte_identical")
            or html.get("unique_dom_ids") != 1361
            or html.get("fragment_links") != 296
            or html.get("mathml_nodes") != 10118
            or html.get("semantic_figures") != 62
            or html.get("raw_tex_math_fallbacks") != 0
            or html.get("runtime_external_dependencies") != 0
            or pdf.get("pages") != 298 or pdf.get("page_size") != "A4"
            or pdf.get("catalog_lang") != "id-ID" or pdf.get("tagged") is not False
            or not pdf.get("all_fonts_embedded_subset_tounicode")
            or browser.get("final_result") != "PASS"
            or browser.get("desktop", {}).get("uncontained_overflow_elements") != 0
            or browser.get("mobile", {}).get("uncontained_overflow_elements") != 0):
        raise SystemExit("cumulative receipt fact closure mismatch")
    visual = (LANE / "qa/UNITS_001_025_VISUAL_QA.md").read_text(encoding="utf-8")
    if ("Status: **PASS**" not in visual or MODEL not in visual
            or "pages **1, 286, and 287-298**" not in visual):
        raise SystemExit("visual receipt content mismatch")
    inventory = list(csv.DictReader(io.StringIO(
        (LANE / "qa/UNITS_001_025_RENDER_INVENTORY.csv").read_text(encoding="utf-8-sig"))))
    expected_pages = [1, 286, *range(287, 299)]
    if ([int(row["pdf_page"]) for row in inventory] != expected_pages
            or any((row["dpi"], row["width_px"], row["height_px"]) !=
                   ("144", "1191", "1684") for row in inventory)
            or any(not re.fullmatch(r"[0-9a-f]{64}", row["render_sha256"])
                   for row in inventory)):
        raise SystemExit("render inventory closure mismatch")


def main() -> int:
    u24_bundle = hashlib.sha256()
    semantic_bundle = hashlib.sha256()
    final_bundle = hashlib.sha256()
    semantic_suffix: dict[str, list[dict[str, Any]]] = {}
    build_suffix: dict[str, list[dict[str, Any]]] = {}
    final_objects: list[dict[str, Any]] = []
    seen: set[str] = set()
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        if (len(raw), len(raw.splitlines()), digest(raw)) != (
                FINAL[name][1], FINAL[name][0], FINAL[name][2]):
            raise SystemExit(f"{name}: final cumulative identity mismatch")
        u24 = raw[:UNIT24[name][1]]
        semantic = raw[:SEMANTIC[name][1]]
        if (len(u24.splitlines()), digest(u24)) != (UNIT24[name][0], UNIT24[name][2]):
            raise SystemExit(f"{name}: Unit 24 cumulative prefix changed")
        if (len(semantic.splitlines()), digest(semantic)) != (SEMANTIC[name][0], SEMANTIC[name][2]):
            raise SystemExit(f"{name}: Unit 25 semantic boundary changed")
        semantic_suffix[name] = parse_suffix(
            raw[UNIT24[name][1]:SEMANTIC[name][1]], SEMANTIC_DELTA[name], name,
            "Unit 25 semantic")
        build_suffix[name] = parse_suffix(
            raw[SEMANTIC[name][1]:], BUILD_DELTA[name], name, "Unit 25 cumulative")
        for line in raw.decode("utf-8").splitlines():
            obj = json.loads(line)
            if obj["id"] in seen:
                raise SystemExit(f"global duplicate ID: {obj['id']}")
            seen.add(obj["id"])
            final_objects.append(obj)
        u24_bundle.update(name.encode()); u24_bundle.update(b"\0"); u24_bundle.update(u24)
        semantic_bundle.update(name.encode()); semantic_bundle.update(b"\0"); semantic_bundle.update(semantic)
        final_bundle.update(name.encode()); final_bundle.update(b"\0"); final_bundle.update(raw)
    if (sum(UNIT24[name][0] for name in FILES), sum(UNIT24[name][1] for name in FILES),
            u24_bundle.hexdigest()) != UNIT24_TOTAL:
        raise SystemExit("Unit 24 cumulative bundle mismatch")
    if (sum(SEMANTIC[name][0] for name in FILES), sum(SEMANTIC[name][1] for name in FILES),
            semantic_bundle.hexdigest()) != SEMANTIC_TOTAL:
        raise SystemExit("Unit 25 semantic bundle mismatch")
    if (len(seen), sum(FINAL[name][1] for name in FILES),
            final_bundle.hexdigest()) != FINAL_TOTAL:
        raise SystemExit("Unit 25 cumulative bundle mismatch")

    by_id = {obj["id"]: obj for obj in final_objects}
    generic = load_generic()
    generic.validate_shapes(final_objects)
    generic.validate_references(final_objects, by_id)
    generic.validate_artifact_manifests(final_objects, LANE)

    semantic_receipt_raw = (LANE / SEMANTIC_RECEIPT).read_bytes()
    if (len(semantic_receipt_raw) != 6957
            or digest(semantic_receipt_raw) != "7814c3586ab5e25989ddbed45ab8569d8406fb9022c5fa52e74e5b8b1aef37aa"):
        raise SystemExit("Unit 25 semantic receipt identity mismatch")
    semantic_receipt = json.loads(semantic_receipt_raw)
    if (semantic_receipt["status"] != "PASS"
            or semantic_receipt["immutability"]["prefix_bundle_sha256"] != UNIT24_TOTAL[2]
            or semantic_receipt["current"]["bundle_sha256"] != SEMANTIC_TOTAL[2]
            or semantic_receipt["append"]["records_by_file"] != SEMANTIC_DELTA
            or semantic_receipt["closure"]["resolved_terminology_finding"]["finding_id"] !=
            "UNIT025-TERM-P3-001"):
        raise SystemExit("Unit 25 semantic receipt binding mismatch")
    semantic_types = Counter(obj["entity_type"] for name in FILES for obj in semantic_suffix[name])
    if semantic_types != Counter({"unit": 60, "segment": 59, "relation": 22,
                                  "correction": 10, "concept": 6, "term": 6,
                                  "artifact": 3, "qa_event": 3, "rights": 3,
                                  "asset": 1}):
        raise SystemExit("Unit 25 semantic suffix census mismatch")
    if {obj.get("adverse_ledger_id") for obj in semantic_suffix["corrections.jsonl"]} != {
            f"O012-ADV-{number:04d}" for number in range(332, 342)}:
        raise SystemExit("Unit 25 semantic correction tail mismatch")
    if {obj.get("terminology_control_id") for obj in semantic_suffix["terms.jsonl"]} != {
            f"O012-TERM-{number:04d}" for number in range(323, 329)}:
        raise SystemExit("Unit 25 semantic term tail mismatch")

    build_types = Counter(obj["entity_type"] for name in FILES for obj in build_suffix[name])
    if build_types != Counter({"artifact": 7, "qa_event": 2, "relation": 7, "rights": 1}):
        raise SystemExit("Unit 25 cumulative suffix census mismatch")
    expected_artifact_ids = set(ARTIFACTS)
    if {obj["id"] for obj in build_suffix["artifacts.jsonl"]} != expected_artifact_ids:
        raise SystemExit("Unit 25 cumulative artifact ID mismatch")
    if {obj["id"] for obj in build_suffix["qa.jsonl"]} != {BUILD_ID, VISUAL_ID}:
        raise SystemExit("Unit 25 cumulative QA ID mismatch")
    expected_relation_ids = {
        "relation:boundary:o012-units-001-025-build",
        "relation:contains:o012-units-001-025-manifest:html",
        "relation:contains:o012-units-001-025-manifest:pdf",
        "relation:depends-on:o012-units-001-025-build:builder",
        "relation:qa:o012-units-001-025-build",
        "relation:qa:o012-units-001-025-visual",
        "relation:qa:o012-units-001-025-render-inventory",
    }
    if {obj["id"] for obj in build_suffix["relations.jsonl"]} != expected_relation_ids:
        raise SystemExit("Unit 25 cumulative relation ID mismatch")
    rights = by_id[FINAL_RIGHTS]
    if (rights["supersedes"] != SOURCE_RIGHTS
            or rights["component_scope"] != [f"unit:o012-rbt-u{number:03d}" for number in range(1, 26)]
            or rights["license_expression"] != "CC-BY-4.0"):
        raise SystemExit("Unit 25 final rights mismatch")
    for ident in (BUILD_ID, VISUAL_ID):
        if by_id[ident]["result"] != "passed" or by_id[ident]["unit_id"] != "unit:o012-rbt-u025":
            raise SystemExit(f"Unit 25 cumulative QA event mismatch: {ident}")
    verify_witnesses(by_id)

    print("Cumulative Units 001-025 append-only backend validation: PASS")
    print(f"unit24_prefix_records={UNIT24_TOTAL[0]}")
    print(f"unit24_prefix_bytes={UNIT24_TOTAL[1]}")
    print(f"unit24_prefix_bundle_sha256={UNIT24_TOTAL[2]}")
    print(f"unit25_semantic_records={SEMANTIC_TOTAL[0]}")
    print(f"unit25_semantic_bytes={SEMANTIC_TOTAL[1]}")
    print(f"unit25_semantic_bundle_sha256={SEMANTIC_TOTAL[2]}")
    print("cumulative_records_added=17")
    print("cumulative_records_by_file=" + json.dumps(BUILD_DELTA, sort_keys=True))
    print(f"final_records={FINAL_TOTAL[0]}")
    print(f"final_bytes={FINAL_TOTAL[1]}")
    print(f"final_bundle_sha256={FINAL_TOTAL[2]}")
    print("manifest_path_correction=output/ARTIFACT_MANIFEST_UNITS_001_025.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
