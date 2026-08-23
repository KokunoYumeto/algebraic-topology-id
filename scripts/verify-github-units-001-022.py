#!/usr/bin/env python3
"""Anonymous GitHub/raw/Pages verification for the frozen Unit 22 commit.

No credential or local Git state is used.  Changed paths come from the official
commit API, each raw response is pinned to COMMIT and checked against both its
Git blob object ID and the frozen commit tree, and Pages is compared byte for
byte with that pinned HTML blob.  A later ``main`` is accepted only if it still
descends from COMMIT; every content check remains commit-pinned.
"""
from __future__ import annotations

import hashlib
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OWNER = "KokunoYumeto"
REPOSITORY = "algebraic-topology-id"
COMMIT = "e2b3c015c6b3dcc66b2e4741a740de6f1972d6f2"
TREE = "4ac0e8d9988663e6379cbb72e90bbb3d01ace12e"
RUN_ID = 32665215550
PAGES_URL = "https://kokunoyumeto.github.io/algebraic-topology-id/units-001-022/"
PAGES_BYTES = 3520527
PAGES_SHA256 = "15938aac7515e4ad7de66f8cf2d825744f9eb08b654165b835bfeace31aef8f4"
EXPECTED_FILES = 36
VERIFIED_AT = "2026-08-23T22:44:12+02:00"
OUTPUT = ROOT / "00_control/GITHUB_PUBLICATION_RECEIPT_UNITS_001_022.json"
API_BASE = f"https://api.github.com/repos/{OWNER}/{REPOSITORY}"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def fetch(url: str, *, accept: str = "application/vnd.github+json",
          attempts: int = 4) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Codex-anonymous-public-readback", "Accept": accept},
    )
    error: Exception | None = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                if response.status != 200:
                    raise RuntimeError(f"HTTP {response.status}: {url}")
                return response.read()
        except Exception as exc:  # bounded retry for transient public-network errors
            error = exc
            if attempt + 1 < attempts:
                time.sleep(2**attempt)
    raise RuntimeError(f"anonymous public readback failed: {url}: {error}")


def fetch_json(url: str) -> Any:
    return json.loads(fetch(url).decode("utf-8"))


def main() -> int:
    commit_url = f"{API_BASE}/commits/{COMMIT}"
    commit = fetch_json(commit_url)
    if (commit.get("sha") != COMMIT
            or commit.get("commit", {}).get("tree", {}).get("sha") != TREE):
        raise RuntimeError("public commit/tree identity mismatch")
    changed = sorted(commit.get("files", []), key=lambda item: item.get("filename", ""))
    paths = [item.get("filename") for item in changed]
    if (len(changed) != EXPECTED_FILES or len(paths) != len(set(paths))
            or any(not isinstance(path, str) or not path for path in paths)
            or any(item.get("status") == "removed" for item in changed)):
        raise RuntimeError(f"unexpected commit inventory: {len(changed)}")

    tree_url = f"{API_BASE}/git/trees/{TREE}?recursive=1"
    tree = fetch_json(tree_url)
    if tree.get("sha") != TREE or tree.get("truncated") is not False:
        raise RuntimeError("public commit tree is absent or truncated")
    tree_entries = {item.get("path"): item for item in tree.get("tree", [])
                    if item.get("type") == "blob"}

    ref_url = f"{API_BASE}/git/ref/heads/main"
    remote_ref = fetch_json(ref_url).get("object", {}).get("sha")
    if not isinstance(remote_ref, str):
        raise RuntimeError("public main ref is unavailable")
    comparison_url: str | None = None
    comparison_status = "identical"
    if remote_ref != COMMIT:
        comparison_url = f"{API_BASE}/compare/{COMMIT}...{remote_ref}"
        comparison = fetch_json(comparison_url)
        comparison_status = comparison.get("status")
        if (comparison_status not in {"ahead", "identical"}
                or comparison.get("merge_base_commit", {}).get("sha") != COMMIT):
            raise RuntimeError("public main no longer descends from frozen Unit 22 commit")

    run_url = f"{API_BASE}/actions/runs/{RUN_ID}"
    run = fetch_json(run_url)
    if (run.get("id") != RUN_ID or run.get("head_sha") != COMMIT
            or run.get("status") != "completed" or run.get("conclusion") != "success"):
        raise RuntimeError("Pages workflow run is not successful for frozen commit")
    jobs_url = f"{API_BASE}/actions/runs/{RUN_ID}/jobs?per_page=100"
    jobs_payload = fetch_json(jobs_url)
    jobs = [job for job in jobs_payload.get("jobs", [])
            if job.get("name") == "deploy" and job.get("status") == "completed"
            and job.get("conclusion") == "success"]
    if len(jobs) != 1:
        raise RuntimeError("unique successful Pages deploy job not found")
    job = jobs[0]
    job_id = job.get("id")
    if not isinstance(job_id, int):
        raise RuntimeError("Pages job ID is invalid")

    deployments_url = (
        f"{API_BASE}/deployments?sha={COMMIT}&environment=github-pages&per_page=100"
    )
    deployments = fetch_json(deployments_url)
    matches: list[tuple[dict[str, Any], dict[str, Any], str]] = []
    for deployment in deployments:
        if (deployment.get("sha") != COMMIT
                or deployment.get("environment") != "github-pages"):
            continue
        status_url = deployment.get("statuses_url")
        if not isinstance(status_url, str):
            continue
        for status in fetch_json(status_url):
            if (status.get("state") == "success"
                    and status.get("target_url") == job.get("html_url")
                    and status.get("environment_url") ==
                    "https://kokunoyumeto.github.io/algebraic-topology-id/"):
                matches.append((deployment, status, status_url))
    if len(matches) != 1:
        raise RuntimeError("unique successful deployment/status for Pages run not found")
    deployment, deployment_status, statuses_url = matches[0]

    files: list[dict[str, object]] = []
    raw_by_path: dict[str, bytes] = {}
    manifest_hasher = hashlib.sha256()
    for item in changed:
        path = item["filename"]
        blob_sha = item.get("sha")
        entry = tree_entries.get(path)
        if (not isinstance(blob_sha, str) or len(blob_sha) != 40 or not entry
                or entry.get("sha") != blob_sha or entry.get("mode") != "100644"):
            raise RuntimeError(f"commit/tree blob identity mismatch: {path}")
        quoted = urllib.parse.quote(path, safe="/")
        raw_url = (f"https://raw.githubusercontent.com/{OWNER}/{REPOSITORY}/"
                   f"{COMMIT}/{quoted}")
        raw = fetch(raw_url, accept="application/octet-stream")
        if (git_blob_sha1(raw) != blob_sha or entry.get("size") != len(raw)):
            raise RuntimeError(f"raw public blob mismatch: {path}")
        digest = sha256(raw)
        manifest_hasher.update(path.encode("utf-8")); manifest_hasher.update(b"\0")
        manifest_hasher.update(str(len(raw)).encode("ascii")); manifest_hasher.update(b"\0")
        manifest_hasher.update(digest.encode("ascii")); manifest_hasher.update(b"\n")
        raw_by_path[path] = raw
        files.append({
            "path": path, "status": item.get("status"), "blob_sha1": blob_sha,
            "bytes": len(raw), "sha256": digest, "tree_entry_exact": True,
            "raw_commit_pinned": COMMIT, "remote_exact": True,
        })

    expected_pages = raw_by_path.get("output/html/units-001-022/index.html")
    if (expected_pages is None or len(expected_pages) != PAGES_BYTES
            or sha256(expected_pages) != PAGES_SHA256):
        raise RuntimeError("commit-pinned Pages source identity mismatch")
    pages = fetch(PAGES_URL + "?commit=" + COMMIT, accept="text/html")
    if pages != expected_pages:
        raise RuntimeError("deployed Pages reader is not byte-exact to frozen commit")

    receipt = {
        "schema_version": "1.0",
        "receipt_id": "O012-GITHUB-PUBLICATION-UNITS-001-022",
        "status": "pushed_deployed_and_anonymously_byte_verified",
        "verified_at": VERIFIED_AT,
        "repository": f"https://github.com/{OWNER}/{REPOSITORY}",
        "branch": "main",
        "content_commit": COMMIT,
        "tree": TREE,
        "remote_ref_at_verification": remote_ref,
        "remote_ref_descends_from_content_commit": True,
        "comparison_status": comparison_status,
        "content_commit_files": len(files),
        "content_commit_manifest_sha256": manifest_hasher.hexdigest(),
        "changed_inventory_source": commit_url,
        "tree_inventory_source": tree_url,
        "files": files,
        "pages": {
            "url": PAGES_URL, "bytes": len(pages), "sha256": sha256(pages),
            "remote_exact": True, "source_commit": COMMIT,
            "source_path": "output/html/units-001-022/index.html",
            "workflow_run_id": RUN_ID, "workflow_id": run.get("workflow_id"),
            "check_suite_id": run.get("check_suite_id"),
            "workflow_run_url": run.get("html_url"), "job_id": job_id,
            "job_url": job.get("html_url"),
            "deployment_id": deployment.get("id"),
            "deployment_status_id": deployment_status.get("id"),
            "conclusion": "success",
        },
        "official_api_evidence": {
            "commit": commit_url, "tree": tree_url, "main_ref": ref_url,
            "comparison": comparison_url, "workflow_run": run_url,
            "jobs": jobs_url, "deployments": deployments_url,
            "deployment_statuses": statuses_url,
        },
        "backend": {
            "records": 3337, "bytes": 3176534,
            "bundle_sha256":
            "38b98ca6258133036ded9e3cb72894f4181d4b6faa46af9e96a2128ab25c9df2",
        },
        "verification_method": {
            "authentication": "anonymous",
            "local_git_used": False,
            "commit_raw_urls_pinned": True,
            "git_blob_sha1_checked": True,
            "commit_tree_entries_checked": True,
            "credentials_recorded": False,
        },
        "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra",
        "source_and_human_credit_preserved": True,
        "upstream_contacted": False,
        "unit_022_included": True,
    }
    OUTPUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8", newline="\n")
    print(json.dumps({
        "status": receipt["status"], "files": len(files),
        "manifest_sha256": receipt["content_commit_manifest_sha256"],
        "pages_bytes": len(pages), "pages_sha256": sha256(pages),
        "job_id": job_id, "deployment_id": deployment.get("id"),
        "deployment_status_id": deployment_status.get("id"),
        "receipt": str(OUTPUT.relative_to(ROOT)).replace("\\", "/"),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
