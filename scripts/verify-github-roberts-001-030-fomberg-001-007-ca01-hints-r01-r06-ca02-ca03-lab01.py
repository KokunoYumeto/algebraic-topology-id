#!/usr/bin/env python3
"""Verify the public Lab 1 GitHub/Pages checkpoint from immutable remote bytes.

The verifier performs no Git operation and makes no remote mutation.  GitHub's
compare API supplies the complete explicit delta from the post-publication
CA02/CA03 receipt commit; every non-removed path in that delta is then fetched
anonymously at the new commit and compared byte-for-byte with its exact local
counterpart.  The current raw reader, deployed Pages reader, and the raw/Pages
surfaces of the frozen predecessor content commit receive additional exact-byte
checks.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER = "KokunoYumeto"
REPOSITORY = "algebraic-topology-id"
GIT_DELTA_BASE_COMMIT = "84f31b8bece744b0fde7732085e1acd503eb6728"
PREDECESSOR_CONTENT_COMMIT = "657f21813ef39bd9e86558a2f4e16e79c23ce491"
CONCEPT_DOI = "10.5281/zenodo.22061489"

PAGES_URL = (
    "https://kokunoyumeto.github.io/algebraic-topology-id/"
    "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01/"
)
PAGES_PATH = (
    "output/html/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-"
    "ca02-ca03-lab01/index.html"
)
PAGES_BYTES = 15_389_821
PAGES_SHA256 = "bb0cf484271370878508a6b774e442ee57aaf82b1a3bbca1bed086729360f7ff"

PREDECESSOR_URL = (
    "https://kokunoyumeto.github.io/algebraic-topology-id/"
    "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03/"
)
PREDECESSOR_PATH = (
    "output/html/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-"
    "ca02-ca03/index.html"
)
PREDECESSOR_BYTES = 15_287_428
PREDECESSOR_SHA256 = "417e50656ae0a61134c480f59df1bcd54d66a68c938d1d54f9c931ba37e2a5d6"

PDF_PATH = (
    "output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-007-ca01-"
    "hints-r01-r06-ca02-ca03-lab01-id.pdf"
)
MANIFEST_PATH = (
    "output/ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_007_CA01_"
    "HINTS_R01_R06_CA02_CA03_LAB01.csv"
)
FINAL_BUILD_RECEIPT = (
    "qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_"
    "LAB01_BUILD_RECEIPT.json"
)
VISUAL_RECEIPT = (
    "qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_"
    "LAB01_VISUAL_QA.md"
)
BROWSER_RECEIPT = (
    "qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_"
    "LAB01_BROWSER_QA.json"
)
ZENODO_RELEASE_DIR = (
    "release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-"
    "ca02-ca03-lab01"
)
ZENODO_RECEIPT_PATH = f"{ZENODO_RELEASE_DIR}/publication-receipt.json"
OUTPUT = ROOT / (
    "00_control/GITHUB_PUBLICATION_RECEIPT_ROBERTS_001_030_FOMBERG_001_007_"
    "CA01_HINTS_R01_R06_CA02_CA03_LAB01.json"
)


# These identities are frozen at the completed local Lab 1 boundary.  The bool
# marks files which must occur in the public delta from GIT_DELTA_BASE_COMMIT.
# The three
# unchanged backend files are still checked locally because they participate in
# the cumulative backend identity, but they need not be republished.
FIXED_LOCAL_IDENTITIES: dict[str, tuple[int, str, bool]] = {
    "source/id-ID/labs/computation-lab-001-monodromy-presentations.md": (
        12_275,
        "165e2f9ba587714fb32a2f5a6432920a36493ebc6902d580f55df9c8ab4c65c4",
        True,
    ),
    "source/id-ID/labs/o012_d60_lab01_monodromy.py": (
        8_818,
        "a9c8875aeb2642921a2d152cd0ed316c6c67969a466240ada9836d3c42252628",
        True,
    ),
    "source/id-ID/labs/test_o012_d60_lab01_monodromy.py": (
        3_032,
        "ae30ca6604b2a96b12c7df125fdcaa6deea00a9e4594f6b161d7d4785d9b949b",
        True,
    ),
    "source/id-ID/labs/expected-output-lab01.txt": (
        478,
        "ddaa8015f314e53895c311e12be4d2d1dcaa1fa3f20def4ee112f28077a38717",
        True,
    ),
    "00_control/TERMINOLOGY.csv": (
        63_366,
        "205c37e300fb17116498156abf970e9dfbfdb34d082d7435c2e96eb9ef1092e5",
        True,
    ),
    "qa/computation-lab-001/STATIC_QA.json": (
        3_394,
        "f74501aad725291c9e9f522e13568ce5c7fb772939e23535f55edcafc0790932",
        True,
    ),
    "qa/computation-lab-001/INDEPENDENT_MATH_REVIEW.json": (
        2_923,
        "b7ae0519b960be5d6de706b46cbd527978c783b697982ba8b2a1a7a5c3a81e86",
        True,
    ),
    "qa/computation-lab-001/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json": (
        2_638,
        "e333fe4398caa72911d7ab85f000a73913cf438dd261436ca3c5fad8ade474b0",
        True,
    ),
    "qa/computation-lab-001/EXECUTION_RECEIPT.json": (
        1_858,
        "ea8c6481c461135b8a00b3fefcf57b6ee1d2c14d7a94a79fbf2c0daaa1bb25db",
        True,
    ),
    "qa/COMPUTATION_LAB_001_QA.json": (
        4_258,
        "75dede0eaa0edbb22c75470dc641bdd10f95aac57c05331171ace4ac9e68aa2b",
        True,
    ),
    "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_001_PLAN.json": (
        9_902,
        "7b45f26028c62fe933f805f9cf0a7aec582c309f61087012db3f79743c0ef0e7",
        True,
    ),
    "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_001_RECEIPT.json": (
        1_773,
        "8ca7af6761c821752c304c02112e1bf2ce0b36bc1bf8f8d840a2b5637afd4f78",
        True,
    ),
    "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_001_REPLAY_RECEIPT.json": (
        372,
        "baeb93b0af8e8421c9d7d61eaad7d69671e75fba365b35c434cca90e0f8bc061",
        True,
    ),
    "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_001_CUMULATIVE_RECEIPT.json": (
        9_727,
        "90f445294eea58aca5bcebe6acaff7293251b21e32aa25f3b62705e64cf8ab74",
        True,
    ),
    "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_001_FILE_MANIFEST.csv": (
        2_828,
        "f73574b3a87c79101eaca79ce8ed5a85bb7be560a5dd92ca806c41b337fbdc2b",
        True,
    ),
    "backend/artifacts.jsonl": (
        176_452,
        "b79da3c77f733a175cf900c655816d4a06fa3f060a495a2644d30b010ce5e8d0",
        True,
    ),
    "backend/assets.jsonl": (
        64_692,
        "1df40f8f6ca4f2fbfbe8a7b924a68a153713a20a4eebe1d014d8fb04669945f7",
        False,
    ),
    "backend/authority.jsonl": (
        4_374,
        "84c622f56dbbd5ba379361245ecfe07bc79c9f4fd6b18ba21b82b5f545211869",
        False,
    ),
    "backend/concepts.jsonl": (
        155_292,
        "c8ccbc4ee38e0a4f0b0d8ee6088774574a4138a7e611bbaa08133fa3ff2ad764",
        True,
    ),
    "backend/corrections.jsonl": (
        594_720,
        "bd961fad5d83e96fec6ef83caa8447e2e5f282c603fd4983d79b5b4b54049fbb",
        False,
    ),
    "backend/qa.jsonl": (
        101_370,
        "65a0890de4efa5051264900fa85dae8631e073148f3daf1d3fe7ce4132ebc5e9",
        True,
    ),
    "backend/relations.jsonl": (
        498_962,
        "6d91e165cb79d4a03d1b21939f934a2155591f2bd2f7e91420a08b6178e485bf",
        True,
    ),
    "backend/rights.jsonl": (
        101_740,
        "aa6c6bf27d9636bbe22d16b6f550a75cce7e8ef7142dffc04f8f4aa3667af69b",
        True,
    ),
    "backend/segments.jsonl": (
        3_387_764,
        "8499116f271fca22b3f30aeba2e6d2410c3a480a1bc000120fc44c195ffd5806",
        True,
    ),
    "backend/terms.jsonl": (
        321_259,
        "908dd1dcdea9ca52acfc91c681a538a0599670d3d3f7ad25a1d9313b508a1740",
        True,
    ),
    "backend/units.jsonl": (
        3_569_075,
        "5ae55e8fc36311878a5209a4f9404faa16784bc22b98883a4dcbfaaf9f71fd22",
        True,
    ),
    PAGES_PATH: (PAGES_BYTES, PAGES_SHA256, True),
    PDF_PATH: (
        9_193_942,
        "722fa7f6c3aa20d1a4c52257d3127fa500bbaf6aad66f64d62177718cd53d128",
        True,
    ),
    MANIFEST_PATH: (
        357,
        "cbb39a0f0a7b4831fa5eaa2e9b3beb6fc5fa15379ec322f2abb8279fa2b7d824",
        True,
    ),
}

REQUIRED_DYNAMIC_CHANGED = {
    ".github/workflows/pages.yml",
    "00_control/CURRENT_STATE.md",
    "00_control/CURSOR.json",
    "00_control/BUILD.md",
    "README.md",
    FINAL_BUILD_RECEIPT,
    VISUAL_RECEIPT,
    BROWSER_RECEIPT,
    ZENODO_RECEIPT_PATH,
    "scripts/verify-github-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-"
    "ca02-ca03-lab01.py",
}

ALLOWED_CHANGED_PREFIXES = (
    "00_control/",
    "backend/",
    "output/",
    "qa/",
    ZENODO_RELEASE_DIR + "/",
    "scripts/",
    "source/id-ID/labs/",
)
ALLOWED_CHANGED_FILES = {".github/workflows/pages.yml", "README.md"}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(
    url: str,
    *,
    accept: str = "application/octet-stream",
    attempts: int = 5,
) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Codex-anonymous-public-readback", "Accept": accept},
    )
    error: Exception | None = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                if response.status != 200:
                    raise RuntimeError(f"HTTP {response.status}: {url}")
                return response.read()
        except Exception as exc:
            error = exc
            if attempt + 1 < attempts:
                time.sleep(2**attempt)
    raise RuntimeError(f"public readback failed: {url}: {error}")


def fetch_exact(url: str, size: int, digest: str, *, attempts: int = 8) -> bytes:
    last: tuple[int, str] | None = None
    for attempt in range(attempts):
        payload = fetch(url)
        last = (len(payload), sha256(payload))
        if last == (size, digest):
            return payload
        if attempt + 1 < attempts:
            time.sleep(3)
    raise RuntimeError(f"public byte identity mismatch: {url}: got {last}")


def gh_json(endpoint: str) -> Any:
    process = subprocess.run(
        ["gh", "api", endpoint],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        timeout=180,
        check=False,
    )
    if process.returncode != 0:
        raise RuntimeError(
            f"GitHub metadata read failed: {endpoint}: {process.stderr.strip()}"
        )
    return json.loads(process.stdout)


def anonymous_json(url: str) -> Any:
    return json.loads(fetch(url, accept="application/json"))


def normalized_local_path(relative: str) -> Path:
    candidate = ROOT / Path(relative)
    resolved_root = ROOT.resolve()
    resolved = candidate.resolve()
    if not resolved.is_relative_to(resolved_root):
        raise RuntimeError(f"changed path escapes repository: {relative}")
    if candidate.is_symlink() or not candidate.is_file():
        raise RuntimeError(f"changed path is not an ordinary local file: {relative}")
    return candidate


def allowed_changed_path(path: str) -> bool:
    return path in ALLOWED_CHANGED_FILES or path.startswith(ALLOWED_CHANGED_PREFIXES)


def verify_fixed_local_identities() -> None:
    for path, (expected_bytes, expected_sha, _) in FIXED_LOCAL_IDENTITIES.items():
        payload = normalized_local_path(path).read_bytes()
        actual = (len(payload), sha256(payload))
        expected = (expected_bytes, expected_sha)
        if actual != expected:
            raise RuntimeError(
                f"frozen local identity mismatch: {path}: got {actual}, expected {expected}"
            )

    predecessor = normalized_local_path(PREDECESSOR_PATH).read_bytes()
    if (len(predecessor), sha256(predecessor)) != (
        PREDECESSOR_BYTES,
        PREDECESSOR_SHA256,
    ):
        raise RuntimeError("local frozen predecessor reader identity mismatch")


def verify_backend_receipt() -> dict[str, object]:
    receipt_path = ROOT / "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_001_CUMULATIVE_RECEIPT.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if receipt.get("status") != "PASS":
        raise RuntimeError("Lab 1 backend cumulative receipt is not PASS")
    if receipt.get("immutable_prefix") != {
        "bundle_sha256": "97edc6371a0bf670ebdaaa4fab8618ec138ae25c4bf54ca9172139934ba0b464",
        "bytes": 8_840_132,
        "preserved_exactly": True,
        "records": 7_273,
    }:
        raise RuntimeError("Lab 1 immutable backend prefix receipt changed")
    cumulative = receipt.get("cumulative", {})
    if (
        cumulative.get("records"),
        cumulative.get("bytes"),
        cumulative.get("bundle_sha256"),
        cumulative.get("computation_laboratories_complete"),
        cumulative.get("computation_laboratories_required"),
    ) != (
        7_404,
        8_975_700,
        "4740eb2ff83b4f9df3c0d90c2426ff77e652b23cad0bbe7763c54ebdefa60b4b",
        1,
        4,
    ):
        raise RuntimeError("Lab 1 cumulative backend identity changed")

    actual_bytes = 0
    actual_records = 0
    for row in receipt.get("files", []):
        path = row.get("path")
        if not isinstance(path, str) or not path.startswith("backend/"):
            raise RuntimeError("malformed backend file row")
        payload = normalized_local_path(path).read_bytes()
        records = len(payload.splitlines())
        if (
            len(payload),
            records,
            sha256(payload),
        ) != (
            row.get("final_bytes"),
            row.get("final_records"),
            row.get("final_sha256"),
        ):
            raise RuntimeError(f"backend file no longer matches receipt: {path}")
        if row.get("prefix_preserved") is not True or row.get("suffix_exact") is not True:
            raise RuntimeError(f"backend append-only flags failed: {path}")
        actual_bytes += len(payload)
        actual_records += records
    if (actual_records, actual_bytes) != (7_404, 8_975_700):
        raise RuntimeError("backend file totals do not match cumulative receipt")
    return {
        "records": actual_records,
        "bytes": actual_bytes,
        "bundle_sha256": cumulative["bundle_sha256"],
        "immutable_prefix_records": 7_273,
        "immutable_prefix_preserved": True,
    }


def verify_final_local_gates(zenodo_record_id: int, zenodo_version: str) -> dict[str, Any]:
    for path in (FINAL_BUILD_RECEIPT, VISUAL_RECEIPT, BROWSER_RECEIPT, ZENODO_RECEIPT_PATH):
        normalized_local_path(path)

    build = json.loads((ROOT / FINAL_BUILD_RECEIPT).read_text(encoding="utf-8"))
    if not str(build.get("status", "")).startswith("PASS"):
        raise RuntimeError("final Lab 1 build receipt is not PASS")
    browser = json.loads((ROOT / BROWSER_RECEIPT).read_text(encoding="utf-8"))
    if not str(browser.get("status", "")).startswith("PASS"):
        raise RuntimeError("Lab 1 browser receipt is not PASS")
    visual_text = (ROOT / VISUAL_RECEIPT).read_text(encoding="utf-8")
    if "PASS" not in visual_text:
        raise RuntimeError("Lab 1 visual receipt does not record PASS")

    zenodo = json.loads((ROOT / ZENODO_RECEIPT_PATH).read_text(encoding="utf-8"))
    expected_doi = f"10.5281/zenodo.{zenodo_record_id}"
    verification = zenodo.get("verification", {})
    if (
        zenodo.get("status") != "PUBLISHED_AND_TWICE_ANONYMOUSLY_VERIFIED"
        or zenodo.get("record_id") != zenodo_record_id
        or zenodo.get("doi") != expected_doi
        or zenodo.get("concept_doi") != CONCEPT_DOI
        or zenodo.get("version") != zenodo_version
        or verification.get("anonymous_readback_passes") != 2
        or verification.get("all_sha256_match_local_on_both_passes") is not True
        or verification.get("published_not_draft") is not True
        or verification.get("credentials_recorded") is not False
    ):
        raise RuntimeError("local Zenodo Lab 1 publication receipt is incomplete or mismatched")
    return zenodo


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
    parser.add_argument("--expected-changed-files", type=int)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    for name in ("content_commit", "content_tree"):
        value = getattr(args, name)
        if re.fullmatch(r"[0-9a-f]{40}", value) is None:
            parser.error(f"--{name.replace('_', '-')} must be a lowercase 40-hex SHA")
    if args.content_commit == GIT_DELTA_BASE_COMMIT:
        parser.error("new content commit must differ from the frozen predecessor")
    for name in (
        "run_id",
        "job_id",
        "deployment_id",
        "deployment_status_id",
        "zenodo_record_id",
    ):
        if getattr(args, name) <= 0:
            parser.error(f"--{name.replace('_', '-')} must be positive")
    if args.expected_changed_files is not None and args.expected_changed_files <= 0:
        parser.error("--expected-changed-files must be positive")
    return args


def main() -> int:
    args = parse_args()
    verify_fixed_local_identities()
    backend = verify_backend_receipt()
    local_zenodo = verify_final_local_gates(args.zenodo_record_id, args.zenodo_version)

    comparison = gh_json(
        f"repos/{OWNER}/{REPOSITORY}/compare/"
        f"{GIT_DELTA_BASE_COMMIT}...{args.content_commit}?per_page=100"
    )
    if comparison.get("base_commit", {}).get("sha") != GIT_DELTA_BASE_COMMIT:
        raise RuntimeError("GitHub comparison base is not the frozen predecessor")
    if comparison.get("status") != "ahead" or comparison.get("ahead_by", 0) < 1:
        raise RuntimeError("new content commit is not strictly ahead of the predecessor")
    remote_rows = comparison.get("files", [])
    if not remote_rows:
        raise RuntimeError("GitHub comparison returned no changed files")
    if len(remote_rows) >= 300:
        raise RuntimeError("GitHub compare file list may be truncated at the 300-file cap")
    if args.expected_changed_files is not None and len(remote_rows) != args.expected_changed_files:
        raise RuntimeError(
            f"changed-file count mismatch: got {len(remote_rows)}, "
            f"expected {args.expected_changed_files}"
        )

    by_path: dict[str, dict[str, Any]] = {}
    for row in remote_rows:
        path = row.get("filename")
        status = row.get("status")
        if not isinstance(path, str) or path in by_path:
            raise RuntimeError("GitHub comparison contains malformed or duplicate paths")
        if status not in {"added", "modified"}:
            raise RuntimeError(f"removed/renamed or unsupported public delta path: {path}: {status}")
        if not allowed_changed_path(path):
            raise RuntimeError(f"public delta path is outside the Lab 1 boundary: {path}")
        by_path[path] = row

    changed = set(by_path)
    required = REQUIRED_DYNAMIC_CHANGED | {
        path for path, (_, _, must_change) in FIXED_LOCAL_IDENTITIES.items() if must_change
    }
    missing_required = sorted(required - changed)
    if missing_required:
        raise RuntimeError(f"required Lab 1 public delta paths are missing: {missing_required}")

    files: list[dict[str, object]] = []
    manifest_hasher = hashlib.sha256()
    changed_bytes = 0
    for path in sorted(changed):
        local = normalized_local_path(path).read_bytes()
        quoted = urllib.parse.quote(path, safe="/")
        raw_url = (
            f"https://raw.githubusercontent.com/{OWNER}/{REPOSITORY}/"
            f"{args.content_commit}/{quoted}"
        )
        remote = fetch_exact(raw_url, len(local), sha256(local))
        if remote != local:
            raise RuntimeError(f"commit-pinned raw payload differs from local file: {path}")
        digest = sha256(local)
        changed_bytes += len(local)
        manifest_hasher.update(path.encode("utf-8"))
        manifest_hasher.update(b"\0")
        manifest_hasher.update(str(len(local)).encode("ascii"))
        manifest_hasher.update(b"\0")
        manifest_hasher.update(digest.encode("ascii"))
        manifest_hasher.update(b"\n")
        files.append(
            {
                "path": path,
                "status": by_path[path]["status"],
                "bytes": len(local),
                "sha256": digest,
                "content_commit": args.content_commit,
                "anonymous_commit_pinned_raw_exact": True,
            }
        )

    main_ref_payload = gh_json(
        f"repos/{OWNER}/{REPOSITORY}/git/ref/heads/main"
    )
    main_ref = main_ref_payload.get("object", {}).get("sha")
    if main_ref != args.content_commit:
        raise RuntimeError(f"public main ref is {main_ref}, expected {args.content_commit}")

    current_local = normalized_local_path(PAGES_PATH).read_bytes()
    current_raw_url = (
        f"https://raw.githubusercontent.com/{OWNER}/{REPOSITORY}/"
        f"{args.content_commit}/{PAGES_PATH}"
    )
    current_raw = fetch_exact(current_raw_url, PAGES_BYTES, PAGES_SHA256)
    pages = fetch_exact(PAGES_URL + "?release=" + args.content_commit, PAGES_BYTES, PAGES_SHA256)
    predecessor = fetch_exact(
        PREDECESSOR_URL + "?predecessor=" + args.content_commit,
        PREDECESSOR_BYTES,
        PREDECESSOR_SHA256,
    )
    predecessor_raw_url = (
        f"https://raw.githubusercontent.com/{OWNER}/{REPOSITORY}/"
        f"{PREDECESSOR_CONTENT_COMMIT}/{PREDECESSOR_PATH}"
    )
    predecessor_raw = fetch_exact(
        predecessor_raw_url,
        PREDECESSOR_BYTES,
        PREDECESSOR_SHA256,
    )
    if current_raw != current_local or pages != current_local:
        raise RuntimeError("raw or Pages Lab 1 reader is not byte-exact to the local reader")
    if predecessor != normalized_local_path(PREDECESSOR_PATH).read_bytes():
        raise RuntimeError("predecessor Pages reader changed unexpectedly")
    if predecessor_raw != predecessor:
        raise RuntimeError("predecessor raw and Pages readers are not byte-identical")

    commit = gh_json(f"repos/{OWNER}/{REPOSITORY}/git/commits/{args.content_commit}")
    if (
        commit.get("sha") != args.content_commit
        or commit.get("tree", {}).get("sha") != args.content_tree
    ):
        raise RuntimeError("content commit/tree mismatch")
    run = gh_json(f"repos/{OWNER}/{REPOSITORY}/actions/runs/{args.run_id}")
    if (
        run.get("id") != args.run_id
        or run.get("head_sha") != args.content_commit
        or run.get("status") != "completed"
        or run.get("conclusion") != "success"
    ):
        raise RuntimeError("workflow run identity/result mismatch")
    jobs_payload = gh_json(
        f"repos/{OWNER}/{REPOSITORY}/actions/runs/{args.run_id}/jobs?per_page=100"
    )
    jobs = [job for job in jobs_payload.get("jobs", []) if job.get("id") == args.job_id]
    if len(jobs) != 1 or jobs[0].get("conclusion") != "success":
        raise RuntimeError("Pages job identity/result mismatch")
    deployment = gh_json(f"repos/{OWNER}/{REPOSITORY}/deployments/{args.deployment_id}")
    if deployment.get("id") != args.deployment_id or deployment.get("sha") != args.content_commit:
        raise RuntimeError("Pages deployment identity mismatch")
    statuses = gh_json(f"repos/{OWNER}/{REPOSITORY}/deployments/{args.deployment_id}/statuses")
    matching_statuses = [
        item for item in statuses if item.get("id") == args.deployment_status_id
    ]
    if (
        len(matching_statuses) != 1
        or matching_statuses[0].get("state") != "success"
        or matching_statuses[0].get("environment_url")
        != "https://kokunoyumeto.github.io/algebraic-topology-id/"
    ):
        raise RuntimeError("Pages deployment status mismatch")

    zenodo_public = anonymous_json(f"https://zenodo.org/api/records/{args.zenodo_record_id}")
    expected_zenodo_doi = f"10.5281/zenodo.{args.zenodo_record_id}"
    if (
        zenodo_public.get("id") != args.zenodo_record_id
        or zenodo_public.get("doi") != expected_zenodo_doi
        or zenodo_public.get("conceptdoi") != CONCEPT_DOI
        or zenodo_public.get("metadata", {}).get("version") != args.zenodo_version
    ):
        raise RuntimeError("public Zenodo sibling record identity/version mismatch")

    receipt = {
        "schema_version": "1.1",
        "status": "PASS_PUSHED_DEPLOYED_AND_ANONYMOUSLY_BYTE_VERIFIED",
        "verified_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "scope": (
            "Roberts 30/30; selected Fomberg Sections 1.1-1.13 complete; "
            "CA01/02/03 24/24; ordinary mastery 84/84; solution-bearing mastery "
            "108/108; computation laboratory 1/4 complete; laboratories 2-4, "
            "proof-metadata closure, and capstone pending"
        ),
        "repository": f"https://github.com/{OWNER}/{REPOSITORY}",
        "branch": "main",
        "parent": GIT_DELTA_BASE_COMMIT,
        "predecessor_reader_content_commit": PREDECESSOR_CONTENT_COMMIT,
        "content_commit": args.content_commit,
        "content_tree": args.content_tree,
        "push": {
            "status": "PASS",
            "remote_ref": "refs/heads/main",
            "remote_commit": main_ref,
            "metadata_transport": (
                "authenticated GitHub API; every public file and reader surface is "
                "verified separately without credentials"
            ),
        },
        "pages_workflow": {
            "status": "completed",
            "conclusion": "success",
            "run_id": args.run_id,
            "workflow_id": run.get("workflow_id"),
            "check_suite_id": run.get("check_suite_id"),
            "job_id": args.job_id,
            "deployment_id": args.deployment_id,
            "deployment_status_id": args.deployment_status_id,
            "deployment_state": "success",
            "run_url": run.get("html_url"),
        },
        "commit_pinned_anonymous_readback": {
            "status": "PASS",
            "method": (
                "GitHub compare API explicit delta plus anonymous commit-pinned raw "
                "byte/SHA-256 verification of every changed file"
            ),
            "changed_files": len(files),
            "changed_bytes": changed_bytes,
            "matched_files": len(files),
            "mismatched_files": 0,
            "removed_files": 0,
            "compare_url": comparison.get("html_url"),
            "commit_delta_manifest_sha256": manifest_hasher.hexdigest(),
            "files": files,
        },
        "reader_anonymous_readback": [
            {
                "surface": "GitHub Pages",
                "url": PAGES_URL,
                "http_status": 200,
                "bytes": len(pages),
                "sha256": sha256(pages),
                "matches_content_commit": True,
            },
            {
                "surface": "commit-pinned raw GitHub",
                "url": current_raw_url,
                "http_status": 200,
                "bytes": len(current_raw),
                "sha256": sha256(current_raw),
                "matches_content_commit": True,
            },
            {
                "surface": "frozen predecessor GitHub Pages",
                "url": PREDECESSOR_URL,
                "http_status": 200,
                "bytes": len(predecessor),
                "sha256": sha256(predecessor),
                "matches_frozen_predecessor": True,
            },
            {
                "surface": "frozen predecessor commit-pinned raw GitHub",
                "url": predecessor_raw_url,
                "http_status": 200,
                "bytes": len(predecessor_raw),
                "sha256": sha256(predecessor_raw),
                "content_commit": PREDECESSOR_CONTENT_COMMIT,
                "matches_frozen_predecessor": True,
            },
        ],
        "backend": backend,
        "publication_truth": {
            "ordinary_mastery": "84/84",
            "cumulative_assessments": "24/24",
            "total_required_mastery": "108/108",
            "computation_laboratories": "1/4",
            "remaining_laboratories": 3,
            "proof_metadata_closure_pending": True,
            "capstone_pending": True,
            "course_complete": False,
        },
        "sibling_zenodo_checkpoint": {
            "version": args.zenodo_version,
            "record_id": args.zenodo_record_id,
            "doi": expected_zenodo_doi,
            "concept_doi": CONCEPT_DOI,
            "public_api_identity_verified": True,
            "publication_receipt_status": local_zenodo["status"],
            "anonymous_exact_readback_passes": 2,
        },
        "credentials_recorded": False,
        "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra",
        "source_and_human_credit_preserved": True,
        "upstream_contacted": False,
    }

    output = args.output if args.output.is_absolute() else ROOT / args.output
    if not output.resolve().is_relative_to(ROOT.resolve()):
        raise RuntimeError("receipt output must remain inside the repository")
    output.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "status": receipt["status"],
                "files": len(files),
                "changed_bytes": changed_bytes,
                "manifest_sha256": manifest_hasher.hexdigest(),
                "pages_bytes": len(pages),
                "pages_sha256": sha256(pages),
                "zenodo_record_id": args.zenodo_record_id,
                "receipt": str(output.relative_to(ROOT)).replace("\\", "/"),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
