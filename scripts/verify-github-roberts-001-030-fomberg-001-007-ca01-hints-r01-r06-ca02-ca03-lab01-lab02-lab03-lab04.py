#!/usr/bin/env python3
"""Verify a completed Lab 4 GitHub/Pages checkpoint from exact public bytes.

The Lab 4 backend is frozen below.  The final reader identities, Git commit,
and deployment are supplied as mandatory post-build inputs rather than source
placeholders.  The predecessor content commit and the complete changed-path
inventory are also frozen below.  The verifier performs no Git mutation and no
publication.  It checks the complete GitHub comparison delta, every changed
file at the commit-pinned raw endpoint, all eleven final backend files, the
deployed Lab 4 reader, the exact nine-file Zenodo checkpoint, and both public
surfaces of the frozen Lab 3 predecessor.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
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

SPEC = importlib.util.spec_from_file_location("d60_lab04_github_verifier_base", BASE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load the frozen GitHub transport verifier")
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)
AUTHENTICATED_GH_JSON = module.gh_json


SLUG = "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04"
TOKEN = "ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04"
PAGES_PATH = f"output/html/{SLUG}/index.html"
PDF_PATH = f"output/pdf/topologi-aljabar-{SLUG}-id.pdf"
MANIFEST_PATH = f"output/ARTIFACT_MANIFEST_{TOKEN}.csv"
FINAL_BUILD_RECEIPT = f"qa/{TOKEN}_BUILD_RECEIPT.json"
VISUAL_RECEIPT = f"qa/{TOKEN}_VISUAL_QA.md"
BROWSER_RECEIPT = f"qa/{TOKEN}_BROWSER_QA.json"
BACKEND_RECEIPT = "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_004_CUMULATIVE_RECEIPT.json"
ZENODO_RELEASE_DIR = f"release/zenodo-{SLUG}"
ZENODO_RECEIPT_PATH = f"{ZENODO_RELEASE_DIR}/publication-receipt.json"
OUTPUT = ROOT / f"00_control/GITHUB_PUBLICATION_RECEIPT_{TOKEN}.json"
PAGES_URL = f"https://kokunoyumeto.github.io/algebraic-topology-id/{SLUG}/"
VERIFIER_PATH = f"scripts/verify-github-{SLUG}.py"

DELTA_BASE_COMMIT = "2196b7cb998b66c50a182a1312dcca7ddba29ccf"
PREDECESSOR_CONTENT_COMMIT = DELTA_BASE_COMMIT

PREDECESSOR_PATH = "output/html/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03/index.html"
PREDECESSOR_URL = "https://kokunoyumeto.github.io/algebraic-topology-id/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03/"
PREDECESSOR_BYTES = 15_828_588
PREDECESSOR_SHA256 = "c221955503cec820c7581c740a038ac1774999ac6a6014f8d0783da2cd08bf0d"

LAB3_PREFIX = {
    "records": 7_694,
    "bytes": 9_280_385,
    "bundle_sha256": "cddd65499da547e0c4f01b8a880f68d1c3d314c078a9179528e4a28b2c5f65a2",
    "preserved_exactly": True,
}
EXPECTED_DELTA_RECORDS = {
    'artifacts.jsonl': 10,
    'assets.jsonl': 0,
    'authority.jsonl': 0,
    'concepts.jsonl': 12,
    'corrections.jsonl': 0,
    'qa.jsonl': 7,
    'relations.jsonl': 61,
    'rights.jsonl': 1,
    'segments.jsonl': 25,
    'terms.jsonl': 12,
    'units.jsonl': 25,
}
EXPECTED_DELTA_BYTES = {
    'artifacts.jsonl': 8_608,
    'assets.jsonl': 0,
    'authority.jsonl': 0,
    'concepts.jsonl': 3_995,
    'corrections.jsonl': 0,
    'qa.jsonl': 4_268,
    'relations.jsonl': 31_427,
    'rights.jsonl': 1_650,
    'segments.jsonl': 49_515,
    'terms.jsonl': 9_657,
    'units.jsonl': 53_745,
}
LAB3_FILE_PREFIXES = {
    'artifacts.jsonl': (234, 193_675, '1535c6096f79fcd84878dca9d918e16e130571fa1f5423a210db55e3b62a782f'),
    'assets.jsonl': (87, 64_692, '1df40f8f6ca4f2fbfbe8a7b924a68a153713a20a4eebe1d014d8fb04669945f7'),
    'authority.jsonl': (6, 4_374, '84c622f56dbbd5ba379361245ecfe07bc79c9f4fd6b18ba21b82b5f545211869'),
    'concepts.jsonl': (513, 162_561, '5b921e4bb055fa53cd7f017d5d72b43a0122e5a31b5b8ec760b6efc4ca7e7fcc'),
    'corrections.jsonl': (564, 594_720, 'bd961fad5d83e96fec6ef83caa8447e2e5f282c603fd4983d79b5b4b54049fbb'),
    'qa.jsonl': (198, 109_899, '1a1eb9f45ea992496a536a0f9bac0c439bfda9d6e10de1a292329727372e0a54'),
    'relations.jsonl': (1_216, 555_459, '0504529956092a8d78f334f6cdf2dbceaa5a319ac09f812d1ccfa09d9b4f2cf0'),
    'rights.jsonl': (110, 105_027, '73fdb740a3867d2cf74c6c84c9cce4f99b8feef39ccf5d5b900425cc46cdf872'),
    'segments.jsonl': (2_115, 3_480_791, '24d76e94204df4d87100ce4394e4c534c0cbdf45897d6f29c9ef0bc66418de67'),
    'terms.jsonl': (506, 338_679, '394f877bcd0e0e537cdf09d1634185425d3fa2af6ba2c4fd955ff392dfc79214'),
    'units.jsonl': (2_145, 3_670_508, '93fc6a9bde31abf13d909e2dad66ad18d57738c326706897fd271c80fec70ecc'),
}
LAB4_FILE_SUFFIXES = {
    'artifacts.jsonl': (10, 8_608, 'b3b8ff5eb4f97493f1ad9e09bcbe27b151e33902654592696a073fd375103bf2'),
    'assets.jsonl': (0, 0, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'),
    'authority.jsonl': (0, 0, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'),
    'concepts.jsonl': (12, 3_995, '00b00928298ce79e23077806e664064a77a560b88b726e637a8e33dbc8c7fcf0'),
    'corrections.jsonl': (0, 0, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'),
    'qa.jsonl': (7, 4_268, 'f67d0f1f45b2fb2095ae28c42890ab85d97e519ab5b170432f55f29484479b97'),
    'relations.jsonl': (61, 31_427, '8d4089498d94bdb7dbfa05c587634b403ed20e9f9927be17e49e703b831e557d'),
    'rights.jsonl': (1, 1_650, '70e3c8a1844800f7802d2a2a654abde31f95fd503de05f71c5c3bd53a42f1c42'),
    'segments.jsonl': (25, 49_515, '052ae8d2c10e9a4e4bdb1b11c477893ddf023c76d720488dc3ad00d51a102677'),
    'terms.jsonl': (12, 9_657, '74e41fd0a960a9eb48a020dbba076a1fbff3168aa98ad7e812518c66140f9be3'),
    'units.jsonl': (25, 53_745, '7d2cc03cf21ab9e9b3824d5cb574c5536d32c83d8bdeaf6aed97a3de82fc3972'),
}
SUPPORTING_RECEIPTS = {
    'manifest': ('qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_004_FILE_MANIFEST.csv', 2_832, 12, '7238837f46a53131f4dfdb033dc746acf7a366eca88ba95d74c223f46aacb02e'),
    'plan': ('qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_004_PLAN.json', 6_790, 192, '44799d1bc51c1c6b3d9277353fb6e5ba9f8ba6e6a862a46ccbcc1ed8c914b888'),
    'replay': ('qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_004_REPLAY_RECEIPT.json', 384, 14, 'ebebca76a428d035f5dfaaa67d81396ceb64e8a2fe52f06efb8a509cfc2995ea'),
    'semantic': ('qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_004_RECEIPT.json', 5_754, 161, 'c15f10bd2ed8edb3686d4dd571df9b002d06a73263d008ab6cbbb15bcd80cc66'),
}
EXPECTED_CUMULATIVE_RECORDS = 7_847
EXPECTED_CHANGED_PATHS = {
    '.github/workflows/pages.yml',
    '00_control/BUILD.md',
    '00_control/CURRENT_GOAL_AND_WORKFLOW.md',
    '00_control/CURRENT_STATE.md',
    '00_control/CURSOR.json',
    '00_control/GITHUB_PUBLICATION_RECEIPT_ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03.json',
    '00_control/TERMINOLOGY.csv',
    'README.md',
    'backend/artifacts.jsonl',
    'backend/concepts.jsonl',
    'backend/qa.jsonl',
    'backend/relations.jsonl',
    'backend/rights.jsonl',
    'backend/segments.jsonl',
    'backend/terms.jsonl',
    'backend/units.jsonl',
    'output/ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04.csv',
    'output/html/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/index.html',
    'output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04-id.pdf',
    'qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_004_CUMULATIVE_RECEIPT.json',
    'qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_004_FILE_MANIFEST.csv',
    'qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_004_PLAN.json',
    'qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_004_RECEIPT.json',
    'qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_004_REPLAY_RECEIPT.json',
    'qa/BACKEND_COMPUTATION_LAB_004_FINALIZATION_RECEIPT.json',
    'qa/COMPUTATION_LAB_004_QA.json',
    'qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04_BROWSER_QA.json',
    'qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04_BUILD_DRAFT.json',
    'qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04_BUILD_RECEIPT.json',
    'qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04_RENDER_INVENTORY.csv',
    'qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04_VISUAL_QA.md',
    'qa/computation-lab-004/EXECUTION_RECEIPT.json',
    'qa/computation-lab-004/INDEPENDENT_BACKEND_CODE_AUDIT.json',
    'qa/computation-lab-004/INDEPENDENT_CODE_REVIEW.json',
    'qa/computation-lab-004/INDEPENDENT_MATH_REVIEW.json',
    'qa/computation-lab-004/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json',
    'qa/computation-lab-004/STATIC_QA.json',
    'release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/LICENSE.md',
    'release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/PACKAGE_PREPARATION_RECEIPT.json',
    'release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/README_RELEASE.md',
    'release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/RELEASE_RIGHTS.md',
    'release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/SHA256SUMS.template',
    'release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/SOURCE_PACKAGE_README.md',
    'release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/artifacts/00_TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04_READER.pdf',
    'release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/artifacts/LICENSE.md',
    'release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/artifacts/README_RELEASE.md',
    'release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/artifacts/RELEASE_RIGHTS.md',
    'release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/artifacts/SHA256SUMS',
    'release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/artifacts/TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04_EDITABLE_SOURCE_BACKEND.zip',
    'release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/artifacts/TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04_QA_PROVENANCE.zip',
    'release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/artifacts/TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04_READER.html',
    'release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/artifacts/release-manifest.json',
    'release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/frozen-inputs.json',
    'release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/frozen-inputs.template.json',
    'release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/metadata.json',
    'release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/publication-plan.json',
    'release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/publication-receipt.json',
    'release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/release-manifest.template.json',
    'release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/transaction.json',
    'scripts/build-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04.py',
    'scripts/extend-backend-computation-lab-004.py',
    'scripts/finalize-backend-computation-lab-004.py',
    'scripts/finalize-build-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04.py',
    'scripts/finalize-computation-lab-004-qa.py',
    'scripts/merge-computation-lab-004.py',
    'scripts/package-release-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04.py',
    'scripts/publish-zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04.py',
    'scripts/qa-computation-lab-004.py',
    'scripts/validate-backend-append-only-computation-lab-004.py',
    'scripts/verify-github-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04.py',
    'scripts/verify-github-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03.py',
    'source/id-ID/labs/computation-lab-004-cross-invariant-comparison.md',
    'source/id-ID/labs/expected-output-lab04.txt',
    'source/id-ID/labs/o012_d60_lab04_cross_invariants.py',
    'source/id-ID/labs/test_o012_d60_lab04_cross_invariants.py',
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
            "--expected-changed-files must equal the explicit Lab 4 inventory "
            f"({len(EXPECTED_CHANGED_PATHS)})"
        )
    if args.backend_records != EXPECTED_CUMULATIVE_RECORDS:
        parser.error(
            f"--backend-records must equal the proved Lab 4 census "
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


def github_json_resilient(endpoint: str) -> Any:
    """Read GitHub metadata publicly, falling back on gh after rate exhaustion."""

    url = endpoint if endpoint.startswith("https://") else f"https://api.github.com/{endpoint}"
    try:
        payload = module.fetch(url, accept="application/vnd.github+json", attempts=2)
    except RuntimeError as exc:
        if "HTTP Error 403" not in str(exc):
            raise
        return AUTHENTICATED_GH_JSON(endpoint)
    try:
        return json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"GitHub metadata was not valid JSON: {endpoint}") from exc


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
    module.gh_json = github_json_resilient


def verify_backend_receipt() -> dict[str, Any]:
    if ACTIVE_ARGS is None:
        raise RuntimeError("backend verifier invoked before argument binding")
    receipt_path = module.normalized_local_path(BACKEND_RECEIPT)
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if (
        receipt.get("status") != "PASS"
        or receipt.get("receipt_kind") != "cumulative_backend_boundary"
        or receipt.get("laboratory_id") != "D60-LAB04"
        or receipt.get("edition_unit_id") != "O012-ORIG-LAB04"
        or receipt.get("model_provenance") != "OpenAI Codex gpt-5.6-sol, Ultra"
    ):
        raise RuntimeError("Lab 4 backend cumulative receipt identity is not PASS")
    if receipt.get("immutable_prefix") != LAB3_PREFIX:
        raise RuntimeError("Lab 4 receipt does not preserve the exact Lab 3 prefix")
    delta = receipt.get("delta", {})
    if (
        delta.get("records") != 153
        or delta.get("bytes") != 162_865
        or delta.get("bundle_sha256")
        != "256a8333f7d1ba49086166560ed1200b4834a8914631d1cb8a094f30891dd48e"
        or delta.get("records_by_file") != EXPECTED_DELTA_RECORDS
        or delta.get("bytes_by_file") != EXPECTED_DELTA_BYTES
    ):
        raise RuntimeError("Lab 4 backend suffix identity/census changed")

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
        raise RuntimeError("Lab 4 supporting-receipt inventory or identity changed")
    supporting: list[dict[str, Any]] = []
    for name, (path, size, lines, digest) in SUPPORTING_RECEIPTS.items():
        payload = module.normalized_local_path(path).read_bytes()
        if (len(payload), payload.count(b"\n"), module.sha256(payload)) != (
            size,
            lines,
            digest,
        ):
            raise RuntimeError(f"Lab 4 supporting receipt changed: {name}")
        supporting.append(expected_support_rows[name])
    cumulative = receipt.get("cumulative", {})
    expected_cumulative = (
        ACTIVE_ARGS.backend_records,
        ACTIVE_ARGS.backend_bytes,
        ACTIVE_ARGS.backend_sha256,
        4,
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
            f"Lab 4 cumulative backend identity mismatch: {actual_cumulative}, "
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
        raise RuntimeError("Lab 4 isolated backend replay is incomplete or mismatched")

    rows = receipt.get("files", [])
    if not isinstance(rows, list) or len(rows) != 11:
        raise RuntimeError("Lab 4 backend receipt does not enumerate eleven files")
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
        if name not in LAB3_FILE_PREFIXES or name not in LAB4_FILE_SUFFIXES:
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

        prefix_records, prefix_bytes, prefix_sha256 = LAB3_FILE_PREFIXES[name]
        suffix_records, suffix_bytes, suffix_sha256 = LAB4_FILE_SUFFIXES[name]
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
            raise RuntimeError(f"backend Lab 3 byte prefix changed: {relative}")
        if (len(suffix), len(suffix.splitlines()), module.sha256(suffix)) != (
            suffix_bytes,
            suffix_records,
            suffix_sha256,
        ):
            raise RuntimeError(f"backend Lab 4 byte suffix changed: {relative}")
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
        "immutable_prefix_records": LAB3_PREFIX["records"],
        "immutable_prefix_preserved": True,
        "laboratories_complete": 4,
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

    build_path = module.normalized_local_path(FINAL_BUILD_RECEIPT)
    build = json.loads(build_path.read_text(encoding="utf-8"))
    if build.get("status") != "PASS":
        raise RuntimeError("final Lab 4 build receipt is not PASS")
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
    if pdf_pages != 558:
        raise RuntimeError("final Lab 4 PDF page census is invalid")
    backend_boundary = build.get("backend_boundary", {})
    if (
        backend_boundary.get("cumulative_records") != ACTIVE_ARGS.backend_records
        or backend_boundary.get("cumulative_bytes") != ACTIVE_ARGS.backend_bytes
        or backend_boundary.get("cumulative_bundle_sha256")
        != ACTIVE_ARGS.backend_sha256
        or backend_boundary.get("laboratories_complete") != 4
        or backend_boundary.get("laboratories_required") != 4
    ):
        raise RuntimeError("final build receipt does not bind the Lab 4 backend")
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
        raise RuntimeError("Lab 4 browser receipt is not PASS")
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
        and navigation.get("toc_lab04_link_count") == 1
        and navigation.get("toc_lab04_link_href") == "#o012-d60-lab04"
        and navigation.get("toc_lab04_activation") == "PASS"
        and navigation.get("activated_hash") == "#o012-d60-lab04"
        and navigation.get("keyboard_focus", {}).get("status") == "PASS"
        and browser.get("console", {}).get("errors") == 0
        and browser.get("console", {}).get("warnings") == 0
        and reader_status.get("solution_bearing_items") == 108
        and reader_status.get("laboratories_complete") == 4
        and reader_status.get("offline_capable") is True
        and reader_status.get("checkpoint_label") == "partial"
    ):
        raise RuntimeError("Lab 4 browser QA semantics or zero-severity census changed")

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
        raise RuntimeError("Lab 4 visual receipt lacks its exact artifact/zero-severity PASS closure")

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

    zenodo_path = module.normalized_local_path(ZENODO_RECEIPT_PATH)
    zenodo = json.loads(zenodo_path.read_text(encoding="utf-8"))
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
        raise RuntimeError("local Zenodo Lab 4 publication receipt is incomplete")

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
            raise RuntimeError("Zenodo primary PDF differs from the final Lab 4 reader")
        if index == 1 and (size, digest) != (
            ACTIVE_ARGS.pages_bytes,
            ACTIVE_ARGS.pages_sha256,
        ):
            raise RuntimeError("Zenodo HTML differs from the final Lab 4 reader")
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
        # Zenodo's file-content endpoint currently returns HTTP 406 for an
        # explicit ``Accept: application/octet-stream`` header even though the
        # successful response itself is application/octet-stream.  The shared
        # GitHub verifier needs that header for raw GitHub endpoints, so keep
        # its transport unchanged and use Zenodo's supported wildcard here.
        payload = module.fetch(content_url, accept="*/*")
        if (len(payload), module.sha256(payload)) != (size, digest):
            raise RuntimeError(f"fresh public Zenodo byte identity mismatch: {name}")
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
    pending = path.parent / f".{path.name}.lab04.pending"
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
    runtime_verifier_path = Path(__file__).resolve()
    runtime_verifier_start = runtime_verifier_path.read_bytes()
    commit_shadow_root = Path(
        tempfile.mkdtemp(prefix="github-lab04-content-commit-", dir=scratch_parent)
    )
    if not commit_shadow_root.resolve().is_relative_to(scratch_parent.resolve()):
        raise RuntimeError("content-commit shadow escaped the bounded scratch directory")
    commit_shadow_cache: dict[str, Path] = {}
    inherited_normalized_local_path = module.normalized_local_path

    def normalized_local_path_at_content_commit(relative: str) -> Path:
        if relative in EXPECTED_CHANGED_PATHS:
            if relative not in commit_shadow_cache:
                relative_path = Path(relative)
                if relative_path.is_absolute() or ".." in relative_path.parts:
                    raise RuntimeError(f"unsafe explicit content-commit path: {relative}")
                process = subprocess.run(
                    ["git", "show", "--no-ext-diff", f"{args.content_commit}:{relative}"],
                    cwd=ROOT,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=180,
                    check=False,
                )
                if process.returncode != 0:
                    raise RuntimeError(
                        f"cannot read explicit content-commit blob {relative}: "
                        f"{process.stderr.decode('utf-8', errors='replace').strip()}"
                    )
                shadow = commit_shadow_root / relative_path
                shadow.parent.mkdir(parents=True, exist_ok=True)
                shadow.write_bytes(process.stdout)
                commit_shadow_cache[relative] = shadow
            return commit_shadow_cache[relative]
        return inherited_normalized_local_path(relative)

    module.normalized_local_path = normalized_local_path_at_content_commit
    descriptor, scratch_name = tempfile.mkstemp(
        prefix="github-lab04-verifier-",
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
            "mastery 108/108; computation laboratories 1-4/4 complete; "
            "proof-metadata closure and capstone pending"
        )
        receipt["publication_truth"] = {
            "ordinary_mastery": "84/84",
            "cumulative_assessments": "24/24",
            "total_required_mastery": "108/108",
            "computation_laboratories": "4/4",
            "remaining_laboratories": 0,
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
        if set(commit_shadow_cache) != EXPECTED_CHANGED_PATHS:
            raise RuntimeError(
                "content-commit local blob witness did not cover the exact changed-path set"
            )
        published_verifier = commit_shadow_cache[VERIFIER_PATH].read_bytes()
        if published_verifier != runtime_verifier_start:
            raise RuntimeError(
                "published content-commit verifier differs from the runtime verifier"
            )
        runtime_verifier_end = runtime_verifier_path.read_bytes()
        if runtime_verifier_end != runtime_verifier_start:
            raise RuntimeError("runtime verifier changed during the publication audit")
        receipt["verifier_provenance"] = {
            "published_content_commit_copy": {
                "path": VERIFIER_PATH,
                "content_commit": args.content_commit,
                "bytes": len(published_verifier),
                "sha256": module.sha256(published_verifier),
                "anonymous_commit_pinned_raw_exact": True,
            },
            "runtime_verifier_copy": {
                "path": VERIFIER_PATH,
                "bytes": len(runtime_verifier_start),
                "sha256": module.sha256(runtime_verifier_start),
                "unchanged_during_transaction": True,
                "byte_identical_to_published_content_commit": True,
            },
        }
        receipt["local_content_commit_witness"] = {
            "status": "PASS_EXACT_EXPLICIT_SET",
            "content_commit": args.content_commit,
            "content_tree": args.content_tree,
            "files": len(commit_shadow_cache),
            "source": "local Git object database, one exact git show per explicit changed path",
            "mutable_worktree_used_for_changed_file_identity": False,
            "temporary_shadows_removed_after_transaction": True,
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
        module.normalized_local_path = inherited_normalized_local_path
        if scratch.exists():
            scratch.unlink()
        if commit_shadow_root.exists():
            shutil.rmtree(commit_shadow_root)


if __name__ == "__main__":
    raise SystemExit(main())
