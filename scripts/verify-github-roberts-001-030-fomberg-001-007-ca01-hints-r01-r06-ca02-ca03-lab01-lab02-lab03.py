#!/usr/bin/env python3
"""Verify a completed Lab 3 GitHub/Pages checkpoint from exact public bytes.

The Lab 3 backend is frozen below.  The final reader identities, Git commit,
and deployment are supplied as mandatory post-build inputs rather than source
placeholders.  The two historical Git commits and the complete changed-path
inventory are also frozen below.  The verifier performs no Git mutation and no
publication.  It checks the complete GitHub comparison delta, every changed
file at the commit-pinned raw endpoint, all eleven final backend files, the
deployed Lab 3 reader, the exact nine-file Zenodo checkpoint, and both public
surfaces of the frozen Lab 2 predecessor.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import os
import re
import sys
import tempfile
import urllib.parse
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / (
    "scripts/verify-github-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-"
    "ca02-ca03-lab01.py"
)
BASE_IDENTITY = (
    29_857,
    "1eb51abed9fed4bcf358db299bc3ed15b5b3c6a2ba7c7c2262f89f6fd1329354",
)
BASE_RAW = BASE.read_bytes()
if (len(BASE_RAW), hashlib.sha256(BASE_RAW).hexdigest()) != BASE_IDENTITY:
    raise RuntimeError("frozen Lab 1 GitHub verifier helper identity drift")

import importlib.util  # noqa: E402 - import follows the helper identity gate.

SPEC = importlib.util.spec_from_file_location("d60_lab03_github_verifier_base", BASE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load the frozen GitHub transport verifier")
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


SLUG = (
    "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-"
    "lab01-lab02-lab03"
)
TOKEN = (
    "ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_"
    "LAB01_LAB02_LAB03"
)
PAGES_PATH = f"output/html/{SLUG}/index.html"
PDF_PATH = f"output/pdf/topologi-aljabar-{SLUG}-id.pdf"
MANIFEST_PATH = f"output/ARTIFACT_MANIFEST_{TOKEN}.csv"
FINAL_BUILD_RECEIPT = f"qa/{TOKEN}_BUILD_RECEIPT.json"
VISUAL_RECEIPT = f"qa/{TOKEN}_VISUAL_QA.md"
BROWSER_RECEIPT = f"qa/{TOKEN}_BROWSER_QA.json"
BACKEND_RECEIPT = "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_003_CUMULATIVE_RECEIPT.json"
ZENODO_RELEASE_DIR = f"release/zenodo-{SLUG}"
ZENODO_RECEIPT_PATH = f"{ZENODO_RELEASE_DIR}/publication-receipt.json"
OUTPUT = ROOT / f"00_control/GITHUB_PUBLICATION_RECEIPT_{TOKEN}.json"
PAGES_URL = f"https://kokunoyumeto.github.io/algebraic-topology-id/{SLUG}/"

DELTA_BASE_COMMIT = "b6a175771209e3a31b047cb84af142980ca81f46"
PREDECESSOR_CONTENT_COMMIT = "8989fbd602f89d0a8d6c30bc7bac1980a74b2c99"

PREDECESSOR_PATH = (
    "output/html/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-"
    "ca02-ca03-lab01-lab02/index.html"
)
PREDECESSOR_URL = (
    "https://kokunoyumeto.github.io/algebraic-topology-id/"
    "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-"
    "lab01-lab02/"
)
PREDECESSOR_BYTES = 15_615_104
PREDECESSOR_SHA256 = "d0c6afddfa92759d475258bf08f20ea4019eccf72b7554128b2b938bd247b375"

LAB2_PREFIX = {
    "records": 7_546,
    "bytes": 9_122_755,
    "bundle_sha256": "ac3a0377861ed2b728f9c7473579fdd4febe43e454a92f3ea06451e13d46c8f8",
    "preserved_exactly": True,
}
EXPECTED_DELTA_RECORDS = {
    "artifacts.jsonl": 10,
    "assets.jsonl": 0,
    "authority.jsonl": 0,
    "concepts.jsonl": 12,
    "corrections.jsonl": 0,
    "qa.jsonl": 7,
    "relations.jsonl": 56,
    "rights.jsonl": 1,
    "segments.jsonl": 25,
    "terms.jsonl": 12,
    "units.jsonl": 25,
}
EXPECTED_DELTA_BYTES = {
    "artifacts.jsonl": 8_607,
    "assets.jsonl": 0,
    "authority.jsonl": 0,
    "concepts.jsonl": 3_992,
    "corrections.jsonl": 0,
    "qa.jsonl": 4_228,
    "relations.jsonl": 28_729,
    "rights.jsonl": 1_634,
    "segments.jsonl": 48_289,
    "terms.jsonl": 9_637,
    "units.jsonl": 52_514,
}
LAB2_FILE_PREFIXES = {
    "artifacts.jsonl": (224, 185_068, "e28ed6e26a8f9812db1e54da035dc58675cd39303138fd85b6e00e9cffb06c94"),
    "assets.jsonl": (87, 64_692, "1df40f8f6ca4f2fbfbe8a7b924a68a153713a20a4eebe1d014d8fb04669945f7"),
    "authority.jsonl": (6, 4_374, "84c622f56dbbd5ba379361245ecfe07bc79c9f4fd6b18ba21b82b5f545211869"),
    "concepts.jsonl": (501, 158_569, "20a163b753cc00f018d9a8cd8f71c6467c7dab607a3b13e8eb5532d6b04ab44c"),
    "corrections.jsonl": (564, 594_720, "bd961fad5d83e96fec6ef83caa8447e2e5f282c603fd4983d79b5b4b54049fbb"),
    "qa.jsonl": (191, 105_671, "54372bca72f81e8dab6580af8db7ab350ff6dc2717fc067f87a6a0e00200a6da"),
    "relations.jsonl": (1_160, 526_730, "96d4d3cec3e42f87e21a5b245cd92f851d9122e4de02865166ed4a9e9c53c04a"),
    "rights.jsonl": (109, 103_393, "ebfcb9d92d9c1a097df404bc16b0abfe2e1c2a02ed5a359e0f615508025f22df"),
    "segments.jsonl": (2_090, 3_432_502, "c8ee822c289168ef7895788151a0f173365ea2a3caf606e3160d8407d18bd204"),
    "terms.jsonl": (494, 329_042, "e1b94dff63d858610b1ddc48cb248b0ca99f05303964c00163718bab12ba870a"),
    "units.jsonl": (2_120, 3_617_994, "fa1b11fb7231fcb5e765126dbbdba70365b63df544b0b65dcdd60d2c6ef21a7f"),
}
LAB3_FILE_SUFFIXES = {
    "artifacts.jsonl": (10, 8_607, "b2321c465b5af28fb56f0ea10315e4a06cb355324247f10f1a894c72d000338b"),
    "assets.jsonl": (0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "authority.jsonl": (0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "concepts.jsonl": (12, 3_992, "e4821a7d3c382177f795f1a133d1ef0b8987fe891eb6e730e898579307801cbf"),
    "corrections.jsonl": (0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "qa.jsonl": (7, 4_228, "17323ccff156ad8ac1626bb9f72963530bc7efcd74a097cb465ddc721c62b014"),
    "relations.jsonl": (56, 28_729, "0b02fb3714d9642cb434e0b82603b2f24b1a3b4819bc9ad2fb411519856d44fa"),
    "rights.jsonl": (1, 1_634, "58cc5dab607f5775ca1b2b4aa4daba1378ffac828d3aea54c001a6b12c687edf"),
    "segments.jsonl": (25, 48_289, "4ff627a4fcc8f8779db107cec3dc4ba2e937ead7e4383ab5ffda853407a0bdfb"),
    "terms.jsonl": (12, 9_637, "f6aea77476b55ddc8e95b6a9d78ac740dda8471681a79b24db116576c7bd3fd4"),
    "units.jsonl": (25, 52_514, "7e4f8484ba2a99cb08f57c302e1942b760b044eba3dd909baae3a5a7f03377c3"),
}
SUPPORTING_RECEIPTS = {
    "manifest": ("qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_003_FILE_MANIFEST.csv", 2_832, 12, "863b11f109e4cdcbf245f0a812b4958b105b5e53e863bc2015d4f883ad3cab46"),
    "plan": ("qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_003_PLAN.json", 11_444, 289, "a2a36172d93efeb8628558f89c3a2db6dadee5bc354b737b4bd300d79bf4a55b"),
    "replay": ("qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_003_REPLAY_RECEIPT.json", 372, 14, "d19a4569e0a068666d4e55e8c520777d5a801b3ed5726f7e5eea6e959d759a92"),
    "semantic": ("qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_003_RECEIPT.json", 2_088, 76, "246c4a8096f1879bc2c0532689c01ba7290cf3cc993ec6fdf9366866d3e14b90"),
}
EXPECTED_CUMULATIVE_RECORDS = 7_694
EXPECTED_CHANGED_PATHS = {
    ".github/workflows/pages.yml",
    "00_control/BUILD.md",
    "00_control/CURRENT_GOAL_AND_WORKFLOW.md",
    "00_control/CURRENT_STATE.md",
    "00_control/CURSOR.json",
    "00_control/TERMINOLOGY.csv",
    "README.md",
    "backend/artifacts.jsonl",
    "backend/concepts.jsonl",
    "backend/qa.jsonl",
    "backend/relations.jsonl",
    "backend/rights.jsonl",
    "backend/segments.jsonl",
    "backend/terms.jsonl",
    "backend/units.jsonl",
    MANIFEST_PATH,
    PAGES_PATH,
    PDF_PATH,
    "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_003_CUMULATIVE_RECEIPT.json",
    "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_003_FILE_MANIFEST.csv",
    "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_003_PLAN.json",
    "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_003_RECEIPT.json",
    "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_003_REPLAY_RECEIPT.json",
    "qa/COMPUTATION_LAB_003_QA.json",
    BROWSER_RECEIPT,
    f"qa/{TOKEN}_BUILD_DRAFT.json",
    FINAL_BUILD_RECEIPT,
    f"qa/{TOKEN}_RENDER_INVENTORY.csv",
    VISUAL_RECEIPT,
    "qa/computation-lab-003/EXECUTION_RECEIPT.json",
    "qa/computation-lab-003/INDEPENDENT_CODE_REVIEW.json",
    "qa/computation-lab-003/INDEPENDENT_MATH_REVIEW.json",
    "qa/computation-lab-003/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json",
    "qa/computation-lab-003/STATIC_QA.json",
    f"{ZENODO_RELEASE_DIR}/LICENSE.md",
    f"{ZENODO_RELEASE_DIR}/PACKAGE_PREPARATION_RECEIPT.json",
    f"{ZENODO_RELEASE_DIR}/README_RELEASE.md",
    f"{ZENODO_RELEASE_DIR}/RELEASE_RIGHTS.md",
    f"{ZENODO_RELEASE_DIR}/SHA256SUMS.template",
    f"{ZENODO_RELEASE_DIR}/SOURCE_PACKAGE_README.md",
    f"{ZENODO_RELEASE_DIR}/frozen-inputs.json",
    f"{ZENODO_RELEASE_DIR}/frozen-inputs.template.json",
    f"{ZENODO_RELEASE_DIR}/metadata.json",
    f"{ZENODO_RELEASE_DIR}/publication-plan.json",
    ZENODO_RECEIPT_PATH,
    f"{ZENODO_RELEASE_DIR}/release-manifest.template.json",
    f"{ZENODO_RELEASE_DIR}/transaction.json",
    f"{ZENODO_RELEASE_DIR}/artifacts/00_TOPOLOGI_ALJABAR_ID_{TOKEN}_READER.pdf",
    f"{ZENODO_RELEASE_DIR}/artifacts/LICENSE.md",
    f"{ZENODO_RELEASE_DIR}/artifacts/README_RELEASE.md",
    f"{ZENODO_RELEASE_DIR}/artifacts/RELEASE_RIGHTS.md",
    f"{ZENODO_RELEASE_DIR}/artifacts/SHA256SUMS",
    f"{ZENODO_RELEASE_DIR}/artifacts/TOPOLOGI_ALJABAR_ID_{TOKEN}_EDITABLE_SOURCE_BACKEND.zip",
    f"{ZENODO_RELEASE_DIR}/artifacts/TOPOLOGI_ALJABAR_ID_{TOKEN}_QA_PROVENANCE.zip",
    f"{ZENODO_RELEASE_DIR}/artifacts/TOPOLOGI_ALJABAR_ID_{TOKEN}_READER.html",
    f"{ZENODO_RELEASE_DIR}/artifacts/release-manifest.json",
    f"scripts/build-{SLUG}.py",
    "scripts/extend-backend-computation-lab-003.py",
    f"scripts/finalize-build-{SLUG}.py",
    "scripts/finalize-computation-lab-003-qa.py",
    "scripts/merge-computation-lab-003.py",
    f"scripts/package-release-{SLUG}.py",
    f"scripts/publish-zenodo-{SLUG}.py",
    "scripts/qa-computation-lab-003.py",
    "scripts/validate-backend-append-only-computation-lab-003.py",
    f"scripts/verify-github-{SLUG}.py",
    "source/id-ID/labs/computation-lab-003-cellular-boundaries-degree.md",
    "source/id-ID/labs/expected-output-lab03.txt",
    "source/id-ID/labs/o012_d60_lab03_cellular_degree.py",
    "source/id-ID/labs/test_o012_d60_lab03_cellular_degree.py",
}
ACTIVE_ARGS: argparse.Namespace | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--content-commit", required=True)
    parser.add_argument("--content-tree", required=True)
    parser.add_argument("--run-id", type=int, required=True)
    parser.add_argument("--job-id", type=int, required=True)
    parser.add_argument("--deployment-id", type=int, required=True)
    parser.add_argument("--deployment-status-id", type=int, required=True)
    parser.add_argument("--zenodo-record-id", type=int, required=True)
    parser.add_argument("--zenodo-version", required=True)
    parser.add_argument("--pages-bytes", type=int, required=True)
    parser.add_argument("--pages-sha256", required=True)
    parser.add_argument("--pdf-bytes", type=int, required=True)
    parser.add_argument("--pdf-sha256", required=True)
    parser.add_argument("--manifest-bytes", type=int, required=True)
    parser.add_argument("--manifest-sha256", required=True)
    parser.add_argument("--backend-records", type=int, required=True)
    parser.add_argument("--backend-bytes", type=int, required=True)
    parser.add_argument("--backend-sha256", required=True)
    parser.add_argument("--expected-changed-files", type=int, required=True)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    for name in ("content_commit", "content_tree"):
        if re.fullmatch(r"[0-9a-f]{40}", getattr(args, name)) is None:
            parser.error(f"--{name.replace('_', '-')} must be lowercase 40-hex")
    if args.content_commit == DELTA_BASE_COMMIT:
        parser.error("--content-commit must differ from the frozen delta base")
    for name in ("pages_sha256", "pdf_sha256", "manifest_sha256", "backend_sha256"):
        if re.fullmatch(r"[0-9a-f]{64}", getattr(args, name)) is None:
            parser.error(f"--{name.replace('_', '-')} must be lowercase 64-hex")
    for name in (
        "run_id",
        "job_id",
        "deployment_id",
        "deployment_status_id",
        "zenodo_record_id",
        "pages_bytes",
        "pdf_bytes",
        "manifest_bytes",
        "backend_records",
        "backend_bytes",
    ):
        if getattr(args, name) <= 0:
            parser.error(f"--{name.replace('_', '-')} must be positive")
    if args.expected_changed_files != len(EXPECTED_CHANGED_PATHS):
        parser.error(
            "--expected-changed-files must equal the explicit Lab 3 inventory "
            f"({len(EXPECTED_CHANGED_PATHS)})"
        )
    if args.backend_records != EXPECTED_CUMULATIVE_RECORDS:
        parser.error(
            f"--backend-records must equal the proved Lab 3 census "
            f"{EXPECTED_CUMULATIVE_RECORDS}"
        )
    output = args.output if args.output.is_absolute() else ROOT / args.output
    if not output.resolve().is_relative_to(ROOT.resolve()):
        parser.error("--output must remain inside the repository")
    return args


def require_row(
    row: Any,
    *,
    path: str,
    size: int,
    digest: str,
    label: str,
) -> None:
    if not isinstance(row, dict):
        raise RuntimeError(f"{label} identity row is absent")
    actual = (row.get("path"), row.get("bytes"), row.get("sha256"))
    expected = (path, size, digest)
    if actual != expected:
        raise RuntimeError(f"{label} identity mismatch: {actual}, expected {expected}")


def configure_transport(args: argparse.Namespace) -> None:
    module.GIT_DELTA_BASE_COMMIT = DELTA_BASE_COMMIT
    module.PREDECESSOR_CONTENT_COMMIT = PREDECESSOR_CONTENT_COMMIT
    module.PAGES_URL = PAGES_URL
    module.PAGES_PATH = PAGES_PATH
    module.PAGES_BYTES = args.pages_bytes
    module.PAGES_SHA256 = args.pages_sha256
    module.PREDECESSOR_URL = PREDECESSOR_URL
    module.PREDECESSOR_PATH = PREDECESSOR_PATH
    module.PREDECESSOR_BYTES = PREDECESSOR_BYTES
    module.PREDECESSOR_SHA256 = PREDECESSOR_SHA256
    module.PDF_PATH = PDF_PATH
    module.MANIFEST_PATH = MANIFEST_PATH
    module.FINAL_BUILD_RECEIPT = FINAL_BUILD_RECEIPT
    module.VISUAL_RECEIPT = VISUAL_RECEIPT
    module.BROWSER_RECEIPT = BROWSER_RECEIPT
    module.ZENODO_RELEASE_DIR = ZENODO_RELEASE_DIR
    module.ZENODO_RECEIPT_PATH = ZENODO_RECEIPT_PATH
    module.OUTPUT = OUTPUT
    module.FIXED_LOCAL_IDENTITIES = {
        PAGES_PATH: (args.pages_bytes, args.pages_sha256, True),
        PDF_PATH: (args.pdf_bytes, args.pdf_sha256, True),
        MANIFEST_PATH: (args.manifest_bytes, args.manifest_sha256, True),
    }
    module.REQUIRED_DYNAMIC_CHANGED = set(EXPECTED_CHANGED_PATHS)
    module.ALLOWED_CHANGED_PREFIXES = ()
    module.ALLOWED_CHANGED_FILES = set(EXPECTED_CHANGED_PATHS)


def verify_backend_receipt() -> dict[str, Any]:
    if ACTIVE_ARGS is None:
        raise RuntimeError("backend verifier invoked before argument binding")
    receipt_path = module.normalized_local_path(BACKEND_RECEIPT)
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if receipt.get("status") != "PASS" or receipt.get("laboratory_id") != "D60-LAB03":
        raise RuntimeError("Lab 3 backend cumulative receipt is not PASS")
    if receipt.get("immutable_prefix") != LAB2_PREFIX:
        raise RuntimeError("Lab 3 receipt does not preserve the exact Lab 2 prefix")
    delta = receipt.get("delta", {})
    if (
        delta.get("records") != 148
        or delta.get("bytes") != 157_630
        or delta.get("bundle_sha256")
        != "44e8ec3a65f35da9a20d1fd589536a7758e39807baf92240ef4d4e597b6fc827"
        or delta.get("records_by_file") != EXPECTED_DELTA_RECORDS
        or delta.get("bytes_by_file") != EXPECTED_DELTA_BYTES
    ):
        raise RuntimeError("Lab 3 backend suffix identity/census changed")

    expected_support_rows = {
        name: {
            "path": path,
            "bytes": size,
            "lf_lines": lines,
            "sha256": digest,
        }
        for name, (path, size, lines, digest) in SUPPORTING_RECEIPTS.items()
    }
    if receipt.get("supporting_receipts") != expected_support_rows:
        raise RuntimeError("Lab 3 supporting-receipt inventory or identity changed")
    supporting: list[dict[str, Any]] = []
    for name, (path, size, lines, digest) in SUPPORTING_RECEIPTS.items():
        payload = module.normalized_local_path(path).read_bytes()
        if (len(payload), payload.count(b"\n"), module.sha256(payload)) != (
            size,
            lines,
            digest,
        ):
            raise RuntimeError(f"Lab 3 supporting receipt changed: {name}")
        supporting.append(expected_support_rows[name])
    cumulative = receipt.get("cumulative", {})
    expected_cumulative = (
        ACTIVE_ARGS.backend_records,
        ACTIVE_ARGS.backend_bytes,
        ACTIVE_ARGS.backend_sha256,
        3,
        4,
    )
    actual_cumulative = (
        cumulative.get("records"),
        cumulative.get("bytes"),
        cumulative.get("bundle_sha256"),
        cumulative.get("computation_laboratories_complete"),
        cumulative.get("computation_laboratories_required"),
    )
    if actual_cumulative != expected_cumulative:
        raise RuntimeError(
            f"Lab 3 cumulative backend identity mismatch: {actual_cumulative}, "
            f"expected {expected_cumulative}"
        )
    replay = receipt.get("replay", {})
    if (
        replay.get("status") != "PASS"
        or replay.get("exact_file_matches") != 11
        or replay.get("temporary_replay_removed") is not True
        or replay.get("final", {}).get("records") != ACTIVE_ARGS.backend_records
        or replay.get("final", {}).get("bytes") != ACTIVE_ARGS.backend_bytes
        or replay.get("final", {}).get("bundle_sha256") != ACTIVE_ARGS.backend_sha256
    ):
        raise RuntimeError("Lab 3 isolated backend replay is incomplete or mismatched")

    rows = receipt.get("files", [])
    if not isinstance(rows, list) or len(rows) != 11:
        raise RuntimeError("Lab 3 backend receipt does not enumerate eleven files")
    seen: set[str] = set()
    raw_by_name: dict[str, bytes] = {}
    files: list[dict[str, Any]] = []
    total_records = 0
    total_bytes = 0
    for row in rows:
        relative = row.get("path") if isinstance(row, dict) else None
        if (
            not isinstance(relative, str)
            or not relative.startswith("backend/")
            or relative in seen
        ):
            raise RuntimeError(f"malformed or duplicate backend row: {relative}")
        seen.add(relative)
        name = relative.removeprefix("backend/")
        if name not in LAB2_FILE_PREFIXES or name not in LAB3_FILE_SUFFIXES:
            raise RuntimeError(f"backend row is outside the frozen file inventory: {relative}")
        payload = module.normalized_local_path(relative).read_bytes()
        actual = (len(payload), len(payload.splitlines()), module.sha256(payload))
        expected = (
            row.get("final_bytes"),
            row.get("final_records"),
            row.get("final_sha256"),
        )
        if actual != expected:
            raise RuntimeError(f"backend file no longer matches receipt: {relative}")

        prefix_records, prefix_bytes, prefix_sha256 = LAB2_FILE_PREFIXES[name]
        suffix_records, suffix_bytes, suffix_sha256 = LAB3_FILE_SUFFIXES[name]
        if (
            row.get("prefix_records"),
            row.get("prefix_bytes"),
            row.get("prefix_sha256"),
            row.get("records_added"),
            row.get("suffix_bytes"),
            row.get("suffix_sha256"),
        ) != (
            prefix_records,
            prefix_bytes,
            prefix_sha256,
            suffix_records,
            suffix_bytes,
            suffix_sha256,
        ):
            raise RuntimeError(f"backend prefix/suffix receipt row changed: {relative}")
        prefix = payload[:prefix_bytes]
        suffix = payload[prefix_bytes:]
        if (len(prefix), len(prefix.splitlines()), module.sha256(prefix)) != (
            prefix_bytes,
            prefix_records,
            prefix_sha256,
        ):
            raise RuntimeError(f"backend Lab 2 byte prefix changed: {relative}")
        if (len(suffix), len(suffix.splitlines()), module.sha256(suffix)) != (
            suffix_bytes,
            suffix_records,
            suffix_sha256,
        ):
            raise RuntimeError(f"backend Lab 3 byte suffix changed: {relative}")
        if prefix and not prefix.endswith(b"\n"):
            raise RuntimeError(f"backend prefix does not end on a record boundary: {relative}")
        if suffix and not suffix.endswith(b"\n"):
            raise RuntimeError(f"backend suffix does not end on a record boundary: {relative}")
        if row.get("prefix_preserved") is not True or row.get("suffix_exact") is not True:
            raise RuntimeError(f"backend append-only proof failed: {relative}")
        raw_by_name[name] = payload
        total_bytes += len(payload)
        total_records += len(payload.splitlines())
        files.append(
            {
                "path": relative,
                "records": actual[1],
                "bytes": actual[0],
                "sha256": actual[2],
                "prefix_records": prefix_records,
                "prefix_bytes": prefix_bytes,
                "prefix_sha256": prefix_sha256,
                "suffix_records": suffix_records,
                "suffix_bytes": suffix_bytes,
                "suffix_sha256": suffix_sha256,
            }
        )
    expected_paths = {f"backend/{name}" for name in EXPECTED_DELTA_RECORDS}
    if seen != expected_paths:
        raise RuntimeError(
            f"backend path inventory mismatch: missing={sorted(expected_paths - seen)}, "
            f"unexpected={sorted(seen - expected_paths)}"
        )
    if (total_records, total_bytes) != (
        ACTIVE_ARGS.backend_records,
        ACTIVE_ARGS.backend_bytes,
    ):
        raise RuntimeError("live backend totals differ from the cumulative boundary")
    bundle = hashlib.sha256()
    for name in EXPECTED_DELTA_RECORDS:
        bundle.update(name.encode("utf-8"))
        bundle.update(b"\0")
        bundle.update(raw_by_name[name])
    if bundle.hexdigest() != ACTIVE_ARGS.backend_sha256:
        raise RuntimeError("independently recomputed backend bundle SHA-256 differs")
    receipt_raw = receipt_path.read_bytes()
    return {
        "status": "PASS_APPEND_ONLY_REPLAYABLE",
        "records": total_records,
        "bytes": total_bytes,
        "bundle_sha256": ACTIVE_ARGS.backend_sha256,
        "immutable_prefix_records": LAB2_PREFIX["records"],
        "immutable_prefix_preserved": True,
        "laboratories_complete": 3,
        "laboratories_required": 4,
        "receipt": {
            "path": BACKEND_RECEIPT,
            "bytes": len(receipt_raw),
            "sha256": module.sha256(receipt_raw),
        },
        "supporting_receipts": supporting,
        "files": files,
    }


def verify_final_local_gates(zenodo_record_id: int, zenodo_version: str) -> dict[str, Any]:
    if ACTIVE_ARGS is None:
        raise RuntimeError("local-gate verifier invoked before argument binding")
    for relative in (
        FINAL_BUILD_RECEIPT,
        VISUAL_RECEIPT,
        BROWSER_RECEIPT,
        ZENODO_RECEIPT_PATH,
    ):
        module.normalized_local_path(relative)

    build = json.loads((ROOT / FINAL_BUILD_RECEIPT).read_text(encoding="utf-8"))
    if build.get("status") != "PASS":
        raise RuntimeError("final Lab 3 build receipt is not PASS")
    require_row(
        build.get("html"),
        path=PAGES_PATH,
        size=ACTIVE_ARGS.pages_bytes,
        digest=ACTIVE_ARGS.pages_sha256,
        label="final build HTML",
    )
    require_row(
        build.get("pdf"),
        path=PDF_PATH,
        size=ACTIVE_ARGS.pdf_bytes,
        digest=ACTIVE_ARGS.pdf_sha256,
        label="final build PDF",
    )
    require_row(
        build.get("manifest"),
        path=MANIFEST_PATH,
        size=ACTIVE_ARGS.manifest_bytes,
        digest=ACTIVE_ARGS.manifest_sha256,
        label="final build manifest",
    )
    pdf_pages = build.get("pdf", {}).get("pages")
    if not isinstance(pdf_pages, int) or pdf_pages <= 529:
        raise RuntimeError("final Lab 3 PDF page census is invalid")
    backend_boundary = build.get("backend_boundary", {})
    if (
        backend_boundary.get("cumulative_records") != ACTIVE_ARGS.backend_records
        or backend_boundary.get("cumulative_bytes") != ACTIVE_ARGS.backend_bytes
        or backend_boundary.get("cumulative_bundle_sha256")
        != ACTIVE_ARGS.backend_sha256
        or backend_boundary.get("laboratories_complete") != 3
        or backend_boundary.get("laboratories_required") != 4
    ):
        raise RuntimeError("final build receipt does not bind the Lab 3 backend")
    backend_receipt_raw = module.normalized_local_path(BACKEND_RECEIPT).read_bytes()
    require_row(
        backend_boundary.get("receipt"),
        path=BACKEND_RECEIPT,
        size=len(backend_receipt_raw),
        digest=module.sha256(backend_receipt_raw),
        label="final build backend receipt",
    )

    browser_path = module.normalized_local_path(BROWSER_RECEIPT)
    browser_raw = browser_path.read_bytes()
    browser = json.loads(browser_raw.decode("utf-8"))
    if browser.get("status") != "PASS":
        raise RuntimeError("Lab 3 browser receipt is not PASS")
    require_row(
        browser.get("artifact"),
        path=PAGES_PATH,
        size=ACTIVE_ARGS.pages_bytes,
        digest=ACTIVE_ARGS.pages_sha256,
        label="browser HTML",
    )
    desktop = browser.get("desktop", {})
    mobile = browser.get("mobile", {})
    semantic = browser.get("semantic_and_binding_checks", {})
    navigation = browser.get("navigation_and_keyboard", {})
    reader_status = browser.get("reader_status_text", {})
    code_scroll = mobile.get("code_blocks_requiring_local_scroll")
    math_scroll = mobile.get("wide_display_math_nodes")
    predecessor_tables = mobile.get("predecessor_wide_table_containers")
    if not (
        browser.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0}
        and browser.get("model_provenance") == "OpenAI Codex gpt-5.6-sol, Ultra"
        and desktop.get("status") == "PASS"
        and desktop.get("page_level_horizontal_overflow") is False
        and desktop.get("centered_and_page_filling") is True
        and mobile.get("status") == "PASS"
        and mobile.get("page_level_horizontal_overflow") is False
        and mobile.get("unexpected_local_overflow_nodes") == 0
        and isinstance(code_scroll, int)
        and code_scroll > 0
        and code_scroll == mobile.get("code_blocks_with_overflow_x_auto")
        and isinstance(math_scroll, int)
        and math_scroll >= 0
        and math_scroll == mobile.get("wide_display_math_nodes_with_overflow_x_auto")
        and predecessor_tables
        == mobile.get("predecessor_wide_table_containers_with_overflow_x_auto")
        and semantic.get("duplicate_live_dom_ids") == 0
        and semantic.get("unresolved_fragment_links") == 0
        and semantic.get("runtime_external_asset_references") == 0
        and semantic.get("laboratory_stable_ids") == 25
        and semantic.get("laboratory_root_plus_stable_ids") == 26
        and semantic.get("laboratory_headings") == 18
        and semantic.get("laboratory_tasks") == 6
        and isinstance(semantic.get("laboratory_mathml_nodes"), int)
        and semantic.get("laboratory_mathml_nodes") > 0
        and semantic.get("self_contained_offline_surface") is True
        and navigation.get("toc_lab03_link_count") == 1
        and navigation.get("toc_lab03_link_href") == "#o012-d60-lab03"
        and navigation.get("toc_lab03_activation") == "PASS"
        and navigation.get("activated_hash") == "#o012-d60-lab03"
        and navigation.get("keyboard_focus", {}).get("status") == "PASS"
        and browser.get("console", {}).get("errors") == 0
        and browser.get("console", {}).get("warnings") == 0
        and reader_status.get("solution_bearing_items") == 108
        and reader_status.get("laboratories_complete") == 3
        and reader_status.get("offline_capable") is True
        and reader_status.get("checkpoint_label") == "partial"
    ):
        raise RuntimeError("Lab 3 browser QA semantics or zero-severity census changed")

    visual_path = module.normalized_local_path(VISUAL_RECEIPT)
    visual_raw = visual_path.read_bytes()
    visual = visual_raw.decode("utf-8")
    exact_visual_lines = (
        "Status: **PASS**",
        f"Artifact: `{PDF_PATH}`",
        (
            f"Identity: {ACTIVE_ARGS.pdf_bytes:,} bytes; {pdf_pages} A4 pages; "
            f"SHA-256 `{ACTIVE_ARGS.pdf_sha256}`"
        ),
        "- P1 (missing, unreadable, blank, clipped, or broken content): **0**",
        "- P2 (material layout, transition, font, formula, hierarchy, or navigation defect): **0**",
        "- P3 (minor visible cosmetic defect after correction and rerender): **0**",
    )
    if any(
        len(re.findall(rf"(?m)^{re.escape(line)}\s*$", visual)) != 1
        for line in exact_visual_lines
    ) or len(re.findall(r"(?m)^Overall disposition: \*\*PASS[^\n]*$", visual)) != 1:
        raise RuntimeError("Lab 3 visual receipt lacks its exact artifact/zero-severity PASS closure")

    zero_census = {"P1": 0, "P2": 0, "P3": 0}
    visual_checks = build.get("visual_checks", {})
    browser_checks = build.get("browser_checks", {})
    require_row(
        visual_checks.get("visual_receipt"),
        path=VISUAL_RECEIPT,
        size=len(visual_raw),
        digest=module.sha256(visual_raw),
        label="final build visual receipt",
    )
    require_row(
        browser_checks.get("browser_receipt"),
        path=BROWSER_RECEIPT,
        size=len(browser_raw),
        digest=module.sha256(browser_raw),
        label="final build browser receipt",
    )
    if not (
        visual_checks.get("status") == "PASS"
        and visual_checks.get("severity_census") == zero_census
        and browser_checks.get("status") == "PASS"
        and browser_checks.get("severity_census") == zero_census
        and browser_checks.get("unexpected_local_overflow_nodes") == 0
        and browser_checks.get("unresolved_fragment_links") == 0
        and browser_checks.get("runtime_external_asset_references") == 0
        and browser_checks.get("console_errors") == 0
        and browser_checks.get("console_warnings") == 0
    ):
        raise RuntimeError("final build receipt does not bind exact visual/browser closure")

    zenodo = json.loads((ROOT / ZENODO_RECEIPT_PATH).read_text(encoding="utf-8"))
    verification = zenodo.get("verification", {})
    if (
        zenodo.get("status") != "PUBLISHED_AND_TWICE_ANONYMOUSLY_VERIFIED"
        or zenodo.get("record_id") != zenodo_record_id
        or zenodo.get("doi") != f"10.5281/zenodo.{zenodo_record_id}"
        or zenodo.get("concept_doi") != module.CONCEPT_DOI
        or zenodo.get("version") != zenodo_version
        or verification.get("anonymous_readback_passes") != 2
        or verification.get("all_sha256_match_local_on_both_passes") is not True
        or verification.get("published_not_draft") is not True
        or verification.get("credentials_recorded") is not False
    ):
        raise RuntimeError("local Zenodo Lab 3 publication receipt is incomplete")

    public_stem = f"TOPOLOGI_ALJABAR_ID_{TOKEN}"
    expected_names = [
        f"00_{public_stem}_READER.pdf",
        f"{public_stem}_READER.html",
        f"{public_stem}_EDITABLE_SOURCE_BACKEND.zip",
        f"{public_stem}_QA_PROVENANCE.zip",
        "LICENSE.md",
        "README_RELEASE.md",
        "RELEASE_RIGHTS.md",
        "release-manifest.json",
        "SHA256SUMS",
    ]
    files = zenodo.get("files")
    if (
        not isinstance(files, list)
        or len(files) != 9
        or [row.get("filename") for row in files if isinstance(row, dict)]
        != expected_names
        or len({row.get("filename") for row in files if isinstance(row, dict)}) != 9
    ):
        raise RuntimeError("local Zenodo receipt does not contain the exact ordered nine-file inventory")
    if not (
        verification.get("exact_public_inventory") is True
        and verification.get("reader_first_by_filename") is True
        and verification.get("pdf_uploaded_first") is True
        and verification.get("anonymous_byte_readback") is True
        and verification.get("all_nine_files_read_twice") is True
        and verification.get("all_sha256_match_local_on_both_passes") is True
        and verification.get("existing_concept_reused") is True
        and verification.get("authorization_header_recorded") is False
        and verification.get("bucket_url_recorded") is False
        and verification.get("absolute_local_paths_recorded") is False
        and verification.get("user_personal_name_recorded") is False
    ):
        raise RuntimeError("local Zenodo receipt lacks exact nine-file/two-pass privacy closure")
    for index, row in enumerate(files):
        filename = row.get("filename")
        size = row.get("bytes")
        digest = row.get("sha256")
        expected_url = (
            f"https://zenodo.org/api/records/{zenodo_record_id}/files/"
            f"{urllib.parse.quote(filename, safe='')}/content"
        )
        readbacks = row.get("anonymous_readbacks")
        if (
            not isinstance(filename, str)
            or not isinstance(size, int)
            or size <= 0
            or not isinstance(digest, str)
            or re.fullmatch(r"[0-9a-f]{64}", digest) is None
            or row.get("url") != expected_url
            or not isinstance(readbacks, list)
            or len(readbacks) != 2
        ):
            raise RuntimeError(f"malformed Zenodo file/readback row: {filename}")
        artifact_raw = module.normalized_local_path(
            f"{ZENODO_RELEASE_DIR}/artifacts/{filename}"
        ).read_bytes()
        if (len(artifact_raw), module.sha256(artifact_raw)) != (size, digest):
            raise RuntimeError(f"local Zenodo payload differs from its receipt: {filename}")
        if index == 0 and (size, digest) != (
            ACTIVE_ARGS.pdf_bytes,
            ACTIVE_ARGS.pdf_sha256,
        ):
            raise RuntimeError("Zenodo primary PDF differs from the final Lab 3 reader")
        if index == 1 and (size, digest) != (
            ACTIVE_ARGS.pages_bytes,
            ACTIVE_ARGS.pages_sha256,
        ):
            raise RuntimeError("Zenodo HTML differs from the final Lab 3 reader")
        for pass_number, readback in enumerate(readbacks, start=1):
            if (
                not isinstance(readback, dict)
                or readback.get("pass") != pass_number
                or readback.get("status") != 200
                or readback.get("bytes") != size
                or readback.get("sha256") != digest
                or readback.get("url") != expected_url
            ):
                raise RuntimeError(
                    f"Zenodo anonymous readback {pass_number} changed: {filename}"
                )
    return zenodo


def verify_public_zenodo_files(record_id: int) -> dict[str, Any]:
    local = json.loads(
        module.normalized_local_path(ZENODO_RECEIPT_PATH).read_text(encoding="utf-8")
    )
    local_rows = local.get("files", [])
    public = module.anonymous_json(f"https://zenodo.org/api/records/{record_id}")
    public_rows = public.get("files")
    if not isinstance(public_rows, list) or len(public_rows) != 9:
        raise RuntimeError("public Zenodo inventory is not exactly nine files")
    by_name: dict[str, dict[str, Any]] = {}
    for row in public_rows:
        name = row.get("key") if isinstance(row, dict) else None
        if not isinstance(name, str) or name in by_name:
            raise RuntimeError(f"malformed or duplicate public Zenodo file: {name}")
        by_name[name] = row
    expected_names = [row["filename"] for row in local_rows]
    if set(by_name) != set(expected_names):
        raise RuntimeError("public Zenodo filename inventory differs from the local receipt")

    verified: list[dict[str, Any]] = []
    for row in local_rows:
        name = row["filename"]
        size = row["bytes"]
        digest = row["sha256"]
        public_row = by_name[name]
        public_links = public_row.get("links", {})
        content_url = public_links.get("content") or public_links.get("self")
        if public_row.get("size") != size or not isinstance(content_url, str):
            raise RuntimeError(f"public Zenodo metadata differs for {name}")
        expected_suffix = (
            f"/api/records/{record_id}/files/"
            f"{urllib.parse.quote(name, safe='')}/content"
        )
        parsed = urllib.parse.urlparse(content_url)
        if parsed.scheme != "https" or parsed.netloc != "zenodo.org" or parsed.path != expected_suffix:
            raise RuntimeError(f"unexpected public Zenodo content URL for {name}")
        payload = module.fetch_exact(content_url, size, digest)
        verified.append(
            {
                "filename": name,
                "bytes": len(payload),
                "sha256": module.sha256(payload),
                "anonymous_fresh_readback": True,
            }
        )
    return {
        "status": "PASS_EXACT_NINE_FILE_PUBLIC_INVENTORY_AND_FRESH_READBACK",
        "record_id": record_id,
        "files": verified,
    }


def verify_all_backend_raw(
    *,
    content_commit: str,
    backend: dict[str, Any],
) -> list[dict[str, Any]]:
    verified: list[dict[str, Any]] = []
    for row in backend["files"]:
        relative = row["path"]
        local = module.normalized_local_path(relative).read_bytes()
        quoted = urllib.parse.quote(relative, safe="/")
        url = (
            f"https://raw.githubusercontent.com/{module.OWNER}/{module.REPOSITORY}/"
            f"{content_commit}/{quoted}"
        )
        remote = module.fetch_exact(url, row["bytes"], row["sha256"])
        if remote != local:
            raise RuntimeError(f"commit-pinned backend differs locally: {relative}")
        verified.append(
            {
                **row,
                "content_commit": content_commit,
                "anonymous_commit_pinned_raw_exact": True,
            }
        )
    if len(verified) != 11:
        raise RuntimeError("commit-pinned backend readback did not cover eleven files")
    return verified


def write_atomic(path: Path, payload: dict[str, Any]) -> None:
    resolved = path.resolve()
    if not resolved.is_relative_to(ROOT.resolve()):
        raise RuntimeError("receipt output escaped the repository")
    path.parent.mkdir(parents=True, exist_ok=True)
    pending = path.parent / f".{path.name}.lab03.pending"
    if pending.exists():
        raise RuntimeError(f"bounded pending receipt already exists: {pending}")
    try:
        pending.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        os.replace(pending, path)
    finally:
        if pending.exists():
            pending.unlink()


def main() -> int:
    global ACTIVE_ARGS
    args = parse_args()
    ACTIVE_ARGS = args
    configure_transport(args)
    module.verify_backend_receipt = verify_backend_receipt
    module.verify_final_local_gates = verify_final_local_gates

    scratch_parent = ROOT / "tmp"
    scratch_parent.mkdir(parents=True, exist_ok=True)
    descriptor, scratch_name = tempfile.mkstemp(
        prefix="github-lab03-verifier-",
        suffix=".json",
        dir=scratch_parent,
    )
    os.close(descriptor)
    scratch = Path(scratch_name)
    final_output = args.output if args.output.is_absolute() else ROOT / args.output
    inherited_args = argparse.Namespace(**vars(args))
    inherited_args.output = scratch
    module.parse_args = lambda: inherited_args
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            result = module.main()
        receipt = json.loads(scratch.read_text(encoding="utf-8"))
        zenodo_public_files = verify_public_zenodo_files(args.zenodo_record_id)
        backend = receipt.get("backend", {})
        backend_raw = verify_all_backend_raw(
            content_commit=args.content_commit,
            backend=backend,
        )
        receipt["schema_version"] = "1.4"
        receipt["scope"] = (
            "Roberts 30/30; selected Fomberg Sections 1.1-1.13 complete; "
            "CA01/02/03 24/24; ordinary mastery 84/84; solution-bearing "
            "mastery 108/108; computation laboratories 1-3/4 complete; "
            "laboratory 4, proof-metadata closure, and capstone pending"
        )
        receipt["publication_truth"] = {
            "ordinary_mastery": "84/84",
            "cumulative_assessments": "24/24",
            "total_required_mastery": "108/108",
            "computation_laboratories": "3/4",
            "remaining_laboratories": 1,
            "proof_metadata_closure_pending": True,
            "capstone_pending": True,
            "course_complete": False,
        }
        receipt["boundary_inputs"] = {
            "delta_base_commit": DELTA_BASE_COMMIT,
            "predecessor_content_commit": PREDECESSOR_CONTENT_COMMIT,
            "content_commit": args.content_commit,
            "content_tree": args.content_tree,
            "html": {
                "path": PAGES_PATH,
                "bytes": args.pages_bytes,
                "sha256": args.pages_sha256,
            },
            "pdf": {
                "path": PDF_PATH,
                "bytes": args.pdf_bytes,
                "sha256": args.pdf_sha256,
            },
            "manifest": {
                "path": MANIFEST_PATH,
                "bytes": args.manifest_bytes,
                "sha256": args.manifest_sha256,
            },
            "backend": {
                "records": args.backend_records,
                "bytes": args.backend_bytes,
                "bundle_sha256": args.backend_sha256,
            },
        }
        receipt["backend"]["all_files_commit_pinned_anonymous_readback"] = {
            "status": "PASS",
            "files": backend_raw,
        }
        receipt["zenodo_public_file_readback"] = zenodo_public_files
        receipt["explicit_changed_path_inventory"] = {
            "status": "PASS_EXACT_SET",
            "files": len(EXPECTED_CHANGED_PATHS),
            "paths": sorted(EXPECTED_CHANGED_PATHS),
        }
        receipt["predecessor_retention"] = {
            "status": "PASS",
            "path": PREDECESSOR_PATH,
            "bytes": PREDECESSOR_BYTES,
            "sha256": PREDECESSOR_SHA256,
            "content_commit": PREDECESSOR_CONTENT_COMMIT,
            "pages_and_commit_pinned_raw_byte_identical": True,
        }
        write_atomic(final_output, receipt)
        print(
            json.dumps(
                {
                    "status": receipt["status"],
                    "content_commit": args.content_commit,
                    "changed_files": receipt["commit_pinned_anonymous_readback"][
                        "changed_files"
                    ],
                    "backend_files": len(backend_raw),
                    "pages_bytes": args.pages_bytes,
                    "pages_sha256": args.pages_sha256,
                    "receipt": final_output.relative_to(ROOT).as_posix(),
                },
                sort_keys=True,
            )
        )
        return result
    finally:
        if scratch.exists():
            scratch.unlink()


if __name__ == "__main__":
    raise SystemExit(main())
