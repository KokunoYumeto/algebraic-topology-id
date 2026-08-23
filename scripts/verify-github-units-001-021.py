#!/usr/bin/env python3
"""Anonymous public-byte verification for the frozen Units 001-021 commit."""

from __future__ import annotations

import hashlib
import json
import subprocess
import time
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMMIT = "dced81432b21edd7bffeae33a25e0c678de4d896"
TREE = "758121e256ae28da17f0968dbffc2fbafd2ecdc6"
OWNER = "KokunoYumeto"
REPOSITORY = "algebraic-topology-id"
RUN_ID = 32662474151
JOB_ID = 97250635604
DEPLOYMENT_ID = 6052011091
DEPLOYMENT_STATUS_ID = 17201415972
PAGES_URL = (
    "https://kokunoyumeto.github.io/algebraic-topology-id/units-001-021/"
)
OUTPUT = ROOT / "00_control" / "GITHUB_PUBLICATION_RECEIPT_UNITS_001_021.json"
VERIFIED_AT = "2026-08-23T21:51:15+02:00"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_bytes(*args: str) -> bytes:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


def fetch(url: str, attempts: int = 4) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Codex-public-readback",
            "Accept": "application/vnd.github+json",
        },
    )
    error: Exception | None = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                if response.status != 200:
                    raise RuntimeError(f"HTTP {response.status}: {url}")
                return response.read()
        except Exception as exc:  # bounded transient retry
            error = exc
            if attempt + 1 < attempts:
                time.sleep(2**attempt)
    raise RuntimeError(f"public readback failed: {url}: {error}")


def fetch_json(url: str):
    return json.loads(fetch(url).decode("utf-8"))


def main() -> int:
    changed = git_bytes(
        "diff-tree", "--no-commit-id", "--name-only", "-r", COMMIT
    ).decode("utf-8").splitlines()
    if len(changed) != 38 or len(changed) != len(set(changed)):
        raise RuntimeError(f"unexpected content-commit inventory: {len(changed)}")

    api_base = f"https://api.github.com/repos/{OWNER}/{REPOSITORY}"
    commit_meta = fetch_json(f"{api_base}/git/commits/{COMMIT}")
    if commit_meta.get("sha") != COMMIT or commit_meta.get("tree", {}).get("sha") != TREE:
        raise RuntimeError("public commit/tree identity mismatch")

    remote_ref = fetch_json(f"{api_base}/git/ref/heads/main")
    remote_sha = remote_ref.get("object", {}).get("sha")
    if remote_sha != COMMIT:
        comparison = fetch_json(f"{api_base}/compare/{COMMIT}...{remote_sha}")
        if (
            comparison.get("status") not in {"ahead", "identical"}
            or comparison.get("merge_base_commit", {}).get("sha") != COMMIT
        ):
            raise RuntimeError("public main no longer descends from the content commit")

    run = fetch_json(f"{api_base}/actions/runs/{RUN_ID}")
    if (
        run.get("head_sha") != COMMIT
        or run.get("status") != "completed"
        or run.get("conclusion") != "success"
    ):
        raise RuntimeError("Pages workflow run is not successful for the content commit")

    jobs = fetch_json(f"{api_base}/actions/runs/{RUN_ID}/jobs").get("jobs", [])
    matching_jobs = [item for item in jobs if item.get("id") == JOB_ID]
    if len(matching_jobs) != 1 or matching_jobs[0].get("conclusion") != "success":
        raise RuntimeError("Pages job identity/status mismatch")

    statuses = fetch_json(f"{api_base}/deployments/{DEPLOYMENT_ID}/statuses")
    matching_statuses = [item for item in statuses if item.get("id") == DEPLOYMENT_STATUS_ID]
    if (
        len(matching_statuses) != 1
        or matching_statuses[0].get("state") != "success"
        or matching_statuses[0].get("environment_url")
        != "https://kokunoyumeto.github.io/algebraic-topology-id/"
    ):
        raise RuntimeError("Pages deployment identity/status mismatch")

    files: list[dict[str, object]] = []
    manifest_hasher = hashlib.sha256()
    for path in changed:
        local = git_bytes("show", f"{COMMIT}:{path}")
        quoted = urllib.parse.quote(path, safe="/")
        raw_url = (
            f"https://raw.githubusercontent.com/{OWNER}/{REPOSITORY}/"
            f"{COMMIT}/{quoted}"
        )
        remote = fetch(raw_url)
        if remote != local:
            raise RuntimeError(f"raw public byte mismatch: {path}")
        digest = sha256(local)
        manifest_hasher.update(path.encode("utf-8"))
        manifest_hasher.update(b"\0")
        manifest_hasher.update(str(len(local)).encode("ascii"))
        manifest_hasher.update(b"\0")
        manifest_hasher.update(digest.encode("ascii"))
        manifest_hasher.update(b"\n")
        files.append(
            {
                "path": path,
                "bytes": len(local),
                "sha256": digest,
                "remote_exact": True,
            }
        )

    pages = fetch(PAGES_URL + "?commit=" + COMMIT)
    expected_pages = git_bytes(
        "show", f"{COMMIT}:output/html/units-001-021/index.html"
    )
    if pages != expected_pages:
        raise RuntimeError("Pages reader byte mismatch")

    receipt = {
        "schema_version": "1.0",
        "receipt_id": "O012-GITHUB-PUBLICATION-UNITS-001-021",
        "status": "pushed_deployed_and_anonymously_byte_verified",
        "verified_at": VERIFIED_AT,
        "repository": f"https://github.com/{OWNER}/{REPOSITORY}",
        "branch": "main",
        "content_commit": COMMIT,
        "tree": TREE,
        "remote_ref_at_verification": COMMIT,
        "content_commit_files": len(files),
        "content_commit_manifest_sha256": manifest_hasher.hexdigest(),
        "files": files,
        "pages": {
            "url": PAGES_URL,
            "bytes": len(pages),
            "sha256": sha256(pages),
            "remote_exact": True,
            "workflow_run_id": RUN_ID,
            "workflow_run_url": run.get("html_url"),
            "job_id": JOB_ID,
            "deployment_id": DEPLOYMENT_ID,
            "deployment_status_id": DEPLOYMENT_STATUS_ID,
            "conclusion": "success",
        },
        "backend": {
            "records": 3111,
            "bytes": 2896429,
            "bundle_sha256": "cf5acacf3ad2351869297dd8d3827787377422fa30c8c1385e60833b23913db9",
        },
        "zenodo_state": {
            "public_through_unit": 20,
            "record_id": 22071667,
            "doi": "10.5281/zenodo.22071667",
            "concept_doi": "10.5281/zenodo.22061489",
            "unit_021_update_deliberately_deferred": "one-unit delta is not a substantial DOI boundary",
        },
        "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra",
        "source_and_human_credit_preserved": True,
        "upstream_contacted": False,
        "unit_022_included": False,
    }
    OUTPUT.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": receipt["status"],
                "files": len(files),
                "manifest_sha256": receipt["content_commit_manifest_sha256"],
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
