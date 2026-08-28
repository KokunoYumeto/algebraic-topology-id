#!/usr/bin/env python3
"""Verify the public CA02/CA03 GitHub and Pages checkpoint from remote bytes."""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import os
import subprocess
import time
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OWNER = "KokunoYumeto"
REPOSITORY = "algebraic-topology-id"
BASE_COMMIT = "e65f5b82ed2c811dc79d8f18494b033c10104689"
CONTENT_COMMIT = "657f21813ef39bd9e86558a2f4e16e79c23ce491"
CONTENT_TREE = "2d7da6665cabbfe9ea8a0157cd533b53ff053b5c"
RUN_ID = 33129294989
JOB_ID = 98714787548
DEPLOYMENT_ID = 6133283357
DEPLOYMENT_STATUS_ID = 17437766400
EXPECTED_CHANGED_FILES = 66
PAGES_URL = (
    "https://kokunoyumeto.github.io/algebraic-topology-id/"
    "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03/"
)
PAGES_PATH = (
    "output/html/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03/"
    "index.html"
)
PAGES_BYTES = 15_287_428
PAGES_SHA256 = "417e50656ae0a61134c480f59df1bcd54d66a68c938d1d54f9c931ba37e2a5d6"
PREDECESSOR_URL = (
    "https://kokunoyumeto.github.io/algebraic-topology-id/"
    "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06/"
)
PREDECESSOR_PATH = (
    "output/html/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06/index.html"
)
PREDECESSOR_BYTES = 15_026_881
PREDECESSOR_SHA256 = "7ed278d73a324ba0a9e5acadedf448221b3791db7322fdf6d29225afd0124d2b"
OUTPUT = ROOT / (
    "00_control/GITHUB_PUBLICATION_RECEIPT_ROBERTS_001_030_FOMBERG_001_007_"
    "CA01_HINTS_R01_R06_CA02_CA03.json"
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(url: str, *, accept: str = "application/octet-stream", attempts: int = 5) -> bytes:
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
        payload = fetch(url, accept="text/html")
        last = (len(payload), sha256(payload))
        if last == (size, digest):
            return payload
        if attempt + 1 < attempts:
            time.sleep(3)
    raise RuntimeError(f"public byte identity mismatch: {url}: got {last}")


def archive(commit: str) -> tuple[bytes, dict[str, bytes]]:
    url = f"https://codeload.github.com/{OWNER}/{REPOSITORY}/zip/{commit}"
    payload = fetch(url, accept="application/zip")
    files: dict[str, bytes] = {}
    with zipfile.ZipFile(io.BytesIO(payload)) as archive_file:
        bad = archive_file.testzip()
        if bad is not None:
            raise RuntimeError(f"corrupt codeload entry: {bad}")
        for info in archive_file.infolist():
            if info.is_dir():
                continue
            parts = info.filename.split("/", 1)
            if len(parts) != 2 or not parts[1]:
                raise RuntimeError(f"invalid codeload path: {info.filename}")
            files[parts[1]] = archive_file.read(info)
    return payload, files


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
        raise RuntimeError(f"GitHub metadata read failed: {endpoint}: {process.stderr.strip()}")
    return json.loads(process.stdout)


def anonymous_main_ref() -> str:
    environment = os.environ.copy()
    environment["GIT_TERMINAL_PROMPT"] = "0"
    environment["GIT_CONFIG_COUNT"] = "1"
    environment["GIT_CONFIG_KEY_0"] = "credential.helper"
    environment["GIT_CONFIG_VALUE_0"] = ""
    process = subprocess.run(
        ["git", "ls-remote", f"https://github.com/{OWNER}/{REPOSITORY}.git", "refs/heads/main"],
        cwd=ROOT,
        env=environment,
        text=True,
        encoding="utf-8",
        capture_output=True,
        timeout=180,
        check=False,
    )
    if process.returncode != 0:
        raise RuntimeError(f"anonymous main-ref read failed: {process.stderr.strip()}")
    fields = process.stdout.strip().split()
    if len(fields) != 2 or fields[1] != "refs/heads/main" or len(fields[0]) != 40:
        raise RuntimeError("anonymous main-ref response is malformed")
    return fields[0]


def main() -> int:
    base_zip, base = archive(BASE_COMMIT)
    release_zip, release = archive(CONTENT_COMMIT)
    added = sorted(set(release) - set(base))
    removed = sorted(set(base) - set(release))
    modified = sorted(path for path in set(base) & set(release) if base[path] != release[path])
    changed = sorted(added + modified)
    if removed or len(changed) != EXPECTED_CHANGED_FILES or len(changed) != len(set(changed)):
        raise RuntimeError(
            f"unexpected public release delta: added={len(added)} modified={len(modified)} "
            f"removed={len(removed)} total={len(changed)}"
        )

    critical = {
        PAGES_PATH: (PAGES_BYTES, PAGES_SHA256),
        "output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-id.pdf":
            (8_915_996, "74ed9b5bf0f79a98693369dc7beba3e84ac81c711cc96b9951ae950ae9632a16"),
        "output/ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03.csv":
            (345, "40220aec7c99f28892775a2d274bcc24ae3cc847946737424a254d97aa7f5c69"),
        "source/id-ID/mastery/cumulative-assessment-002-homology-excision-cellular.md":
            (25_321, "2f8dc58eb4fb2da06e239d8e0979112c5f50c846f584900a2e7ea4999a8685ea"),
        "source/id-ID/mastery/cumulative-assessment-003-cohomology-degree-synthesis.md":
            (26_074, "35c2c9a1b7edbeb1902245b567754e33f4720e11b48d2822bad7666a6a626894"),
        "qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_BUILD_RECEIPT.json":
            (81_018, "596f0e89e8c4abe310019dca95f0e457e7b70983f490afba26291211af0f55b9"),
        "qa/BACKEND_APPEND_ONLY_CUMULATIVE_ASSESSMENTS_002_003_CUMULATIVE_RECEIPT.json":
            (11_073, "61e5a3791ca4cacf7a2fbe0c09f5b638afd1c2c427f8784d04b96331903d53c7"),
        "qa/ROUTE_MASTERY_CENSUS.json":
            (141_526, "67a79a47f966d65862f5006e4255c620f7fc79a9fb02c51e4836cb578ff66977"),
        "release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03/publication-receipt.json":
            (11_228, "d097cabe1c857b498ec0bf1dcca620e6cd957797ab70777ba229b6c3540a2871"),
    }
    for path, (size, digest) in critical.items():
        payload = release.get(path)
        if payload is None or len(payload) != size or sha256(payload) != digest or path not in changed:
            raise RuntimeError(f"critical public artifact mismatch: {path}")

    files: list[dict[str, object]] = []
    manifest_hasher = hashlib.sha256()
    changed_bytes = 0
    for path in changed:
        payload = release[path]
        digest = sha256(payload)
        changed_bytes += len(payload)
        manifest_hasher.update(path.encode("utf-8"))
        manifest_hasher.update(b"\0")
        manifest_hasher.update(str(len(payload)).encode("ascii"))
        manifest_hasher.update(b"\0")
        manifest_hasher.update(digest.encode("ascii"))
        manifest_hasher.update(b"\n")
        files.append(
            {
                "path": path,
                "status": "added" if path in added else "modified",
                "bytes": len(payload),
                "sha256": digest,
                "content_commit": CONTENT_COMMIT,
                "anonymous_codeload_exact": True,
            }
        )

    main_ref = anonymous_main_ref()
    if main_ref != CONTENT_COMMIT:
        raise RuntimeError(f"public main ref is {main_ref}, expected {CONTENT_COMMIT}")

    raw_url = f"https://raw.githubusercontent.com/{OWNER}/{REPOSITORY}/{CONTENT_COMMIT}/{PAGES_PATH}"
    raw = fetch_exact(raw_url, PAGES_BYTES, PAGES_SHA256)
    pages = fetch_exact(PAGES_URL + "?release=" + CONTENT_COMMIT, PAGES_BYTES, PAGES_SHA256)
    predecessor = fetch_exact(
        PREDECESSOR_URL + "?predecessor=" + CONTENT_COMMIT,
        PREDECESSOR_BYTES,
        PREDECESSOR_SHA256,
    )
    if raw != release[PAGES_PATH] or pages != release[PAGES_PATH]:
        raise RuntimeError("raw or Pages reader is not byte-exact to the public release archive")
    if predecessor != release[PREDECESSOR_PATH]:
        raise RuntimeError("predecessor Pages reader changed unexpectedly")

    commit = gh_json(f"repos/{OWNER}/{REPOSITORY}/git/commits/{CONTENT_COMMIT}")
    if commit.get("sha") != CONTENT_COMMIT or commit.get("tree", {}).get("sha") != CONTENT_TREE:
        raise RuntimeError("content commit/tree mismatch")
    run = gh_json(f"repos/{OWNER}/{REPOSITORY}/actions/runs/{RUN_ID}")
    if (
        run.get("id") != RUN_ID
        or run.get("head_sha") != CONTENT_COMMIT
        or run.get("status") != "completed"
        or run.get("conclusion") != "success"
    ):
        raise RuntimeError("workflow run identity/result mismatch")
    jobs_payload = gh_json(f"repos/{OWNER}/{REPOSITORY}/actions/runs/{RUN_ID}/jobs?per_page=100")
    jobs = [job for job in jobs_payload.get("jobs", []) if job.get("id") == JOB_ID]
    if len(jobs) != 1 or jobs[0].get("conclusion") != "success":
        raise RuntimeError("Pages job identity/result mismatch")
    deployment = gh_json(f"repos/{OWNER}/{REPOSITORY}/deployments/{DEPLOYMENT_ID}")
    if deployment.get("id") != DEPLOYMENT_ID or deployment.get("sha") != CONTENT_COMMIT:
        raise RuntimeError("Pages deployment identity mismatch")
    statuses = gh_json(f"repos/{OWNER}/{REPOSITORY}/deployments/{DEPLOYMENT_ID}/statuses")
    statuses = [item for item in statuses if item.get("id") == DEPLOYMENT_STATUS_ID]
    if (
        len(statuses) != 1
        or statuses[0].get("state") != "success"
        or statuses[0].get("environment_url")
        != "https://kokunoyumeto.github.io/algebraic-topology-id/"
    ):
        raise RuntimeError("Pages deployment status mismatch")

    receipt = {
        "schema_version": "1.0",
        "status": "PASS_PUSHED_DEPLOYED_AND_ANONYMOUSLY_BYTE_VERIFIED",
        "verified_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "scope": (
            "Roberts 30/30; selected Fomberg Sections 1.1-1.13 complete; "
            "CA01/02/03 24/24; ordinary mastery 84/84; solution-bearing mastery 108/108; "
            "four laboratories, proof-metadata closure, and capstone pending"
        ),
        "repository": f"https://github.com/{OWNER}/{REPOSITORY}",
        "branch": "main",
        "parent": BASE_COMMIT,
        "content_commit": CONTENT_COMMIT,
        "content_tree": CONTENT_TREE,
        "push": {
            "status": "PASS",
            "remote_ref": "refs/heads/main",
            "anonymous_remote_commit": main_ref,
        },
        "pages_workflow": {
            "status": "completed",
            "conclusion": "success",
            "run_id": RUN_ID,
            "workflow_id": run.get("workflow_id"),
            "check_suite_id": run.get("check_suite_id"),
            "job_id": JOB_ID,
            "deployment_id": DEPLOYMENT_ID,
            "deployment_status_id": DEPLOYMENT_STATUS_ID,
            "deployment_state": "success",
            "run_url": run.get("html_url"),
        },
        "commit_pinned_anonymous_readback": {
            "status": "PASS",
            "method": "anonymous commit-pinned codeload ZIP with integrity test",
            "changed_files": len(files),
            "changed_bytes": changed_bytes,
            "matched_files": len(files),
            "mismatched_files": 0,
            "removed_files": 0,
            "commit_delta_manifest_sha256": manifest_hasher.hexdigest(),
            "files": files,
            "base_archive": {
                "url": f"https://codeload.github.com/{OWNER}/{REPOSITORY}/zip/{BASE_COMMIT}",
                "bytes": len(base_zip),
                "sha256": sha256(base_zip),
            },
            "content_archive": {
                "url": f"https://codeload.github.com/{OWNER}/{REPOSITORY}/zip/{CONTENT_COMMIT}",
                "bytes": len(release_zip),
                "sha256": sha256(release_zip),
            },
        },
        "pages_anonymous_readback": [
            {
                "url": PAGES_URL,
                "http_status": 200,
                "bytes": len(pages),
                "sha256": sha256(pages),
                "matches_content_commit": True,
            },
            {
                "url": raw_url,
                "http_status": 200,
                "bytes": len(raw),
                "sha256": sha256(raw),
                "matches_content_commit": True,
            },
            {
                "url": PREDECESSOR_URL,
                "http_status": 200,
                "bytes": len(predecessor),
                "sha256": sha256(predecessor),
                "matches_frozen_predecessor": True,
            },
        ],
        "publication_truth": {
            "ordinary_mastery": "84/84",
            "cumulative_assessments": "24/24",
            "total_required_mastery": "108/108",
            "remaining_laboratories": 4,
            "proof_metadata_closure_pending": True,
            "capstone_pending": True,
            "course_complete": False,
        },
        "sibling_zenodo_checkpoint": {
            "version": "0.31.2",
            "record_id": 22135136,
            "doi": "10.5281/zenodo.22135136",
            "concept_doi": "10.5281/zenodo.22061489",
            "anonymous_exact_readback": True,
        },
        "credentials_recorded": False,
        "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra",
        "source_and_human_credit_preserved": True,
        "upstream_contacted": False,
    }
    OUTPUT.write_text(
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
                "receipt": str(OUTPUT.relative_to(ROOT)).replace("\\", "/"),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
