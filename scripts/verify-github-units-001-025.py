#!/usr/bin/env python3
"""Verify the public Unit 25 GitHub/Pages release from remote bytes."""
from __future__ import annotations

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
BASE_COMMIT = "884a03e88775967c3e77747c242566c0910776ef"
CONTENT_COMMIT = "24aee490d52d44e5b56d6fc4a9b337dcf3573ae5"
RELEASE_COMMIT = CONTENT_COMMIT
RELEASE_TREE = "aad55b5d0c47b60f77d0517b09c47efbd1ebda91"
RUN_ID = 32684818822
JOB_ID = 97307868869
DEPLOYMENT_ID = 6055747095
DEPLOYMENT_STATUS_ID = 17211657786
PAGES_URL = "https://kokunoyumeto.github.io/algebraic-topology-id/units-001-025/"
PAGES_BYTES = 4_112_563
PAGES_SHA256 = "38cd8437f3b4235ac6269f4e3365123fa06485269d35a424ad4f5ddd589025c1"
EXPECTED_CHANGED_FILES = 38
VERIFIED_AT = "2026-08-24T05:02:02+02:00"
OUTPUT = ROOT / "00_control/GITHUB_PUBLICATION_RECEIPT_UNITS_001_025.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(url: str, *, accept: str = "application/octet-stream", attempts: int = 4) -> bytes:
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


def archive(commit: str) -> tuple[bytes, dict[str, bytes]]:
    url = f"https://codeload.github.com/{OWNER}/{REPOSITORY}/zip/{commit}"
    payload = fetch(url, accept="application/zip")
    files: dict[str, bytes] = {}
    with zipfile.ZipFile(io.BytesIO(payload)) as zf:
        bad = zf.testzip()
        if bad is not None:
            raise RuntimeError(f"corrupt codeload entry: {bad}")
        for info in zf.infolist():
            if info.is_dir():
                continue
            parts = info.filename.split("/", 1)
            if len(parts) != 2 or not parts[1]:
                raise RuntimeError(f"invalid codeload path: {info.filename}")
            files[parts[1]] = zf.read(info)
    return payload, files


def gh_json(endpoint: str) -> Any:
    proc = subprocess.run(
        ["gh", "api", endpoint],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        timeout=180,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"GitHub CLI metadata read failed: {endpoint}: {proc.stderr.strip()}")
    return json.loads(proc.stdout)


def anonymous_main_ref() -> str:
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GIT_CONFIG_COUNT"] = "1"
    env["GIT_CONFIG_KEY_0"] = "credential.helper"
    env["GIT_CONFIG_VALUE_0"] = ""
    proc = subprocess.run(
        ["git", "ls-remote", f"https://github.com/{OWNER}/{REPOSITORY}.git", "refs/heads/main"],
        cwd=ROOT,
        env=env,
        text=True,
        encoding="utf-8",
        capture_output=True,
        timeout=180,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"anonymous main-ref read failed: {proc.stderr.strip()}")
    fields = proc.stdout.strip().split()
    if len(fields) != 2 or fields[1] != "refs/heads/main" or len(fields[0]) != 40:
        raise RuntimeError("anonymous main-ref response is malformed")
    return fields[0]


def main() -> int:
    base_zip, base = archive(BASE_COMMIT)
    release_zip, release = archive(RELEASE_COMMIT)
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
        "source/id-ID/units/unit-025-lecture-025.md": (36_578, "df72add4e57236b51ff7d2a0c99af4b65299365874163cb334be5d0988c0f769"),
        "output/html/units-001-025/index.html": (PAGES_BYTES, PAGES_SHA256),
        "output/pdf/topologi-aljabar-unit-001-025-id.pdf": (1_972_209, "581d62162633a6624687517c5cf1595f5fc02a2701c2222b279711e0520b9a3f"),
        "output/ARTIFACT_MANIFEST_UNITS_001_025.csv": (249, "37175a8d7023bf394c50c4809122b1f3244b5d0b1b95a3b724bdb2ff184ab142"),
        "qa/UNITS_001_025_BUILD_RECEIPT.json": (7_729, "dd2fa5b52ed84ac939c33cfa5b9f68be4b904b014321abcb54c2ae664d0f9727"),
        "qa/BACKEND_APPEND_ONLY_UNIT_025_CUMULATIVE_RECEIPT.json": (7_562, "eacee8cad8ffe460af5f50a9be16f5c02b0671a686209e7d0073e10b2a98a2c1"),
        "qa/BACKEND_APPEND_ONLY_UNIT_025_REPLAY_COMPATIBILITY_RECEIPT.json": (3_312, "6b4ef92a4c3ad4ec2190d7f1bedac6c118ff9033a1bb6257bd96d48f86dae1f2"),
    }
    for path, (size, digest) in critical.items():
        data = release.get(path)
        if data is None or len(data) != size or sha256(data) != digest or path not in changed:
            raise RuntimeError(f"critical public artifact mismatch: {path}")

    files: list[dict[str, object]] = []
    manifest_hasher = hashlib.sha256()
    for path in changed:
        data = release[path]
        digest = sha256(data)
        status = "added" if path in added else "modified"
        manifest_hasher.update(path.encode("utf-8")); manifest_hasher.update(b"\0")
        manifest_hasher.update(str(len(data)).encode("ascii")); manifest_hasher.update(b"\0")
        manifest_hasher.update(digest.encode("ascii")); manifest_hasher.update(b"\n")
        files.append({
            "path": path,
            "status": status,
            "bytes": len(data),
            "sha256": digest,
            "release_commit": RELEASE_COMMIT,
            "anonymous_codeload_exact": True,
        })

    main_ref = anonymous_main_ref()
    if main_ref != RELEASE_COMMIT:
        raise RuntimeError(f"public main ref is {main_ref}, expected {RELEASE_COMMIT}")

    raw_url = (
        f"https://raw.githubusercontent.com/{OWNER}/{REPOSITORY}/{RELEASE_COMMIT}/"
        "output/html/units-001-025/index.html"
    )
    raw = fetch(raw_url, accept="text/html")
    pages = fetch(PAGES_URL + "?release=" + RELEASE_COMMIT, accept="text/html")
    expected_pages = release["output/html/units-001-025/index.html"]
    if raw != expected_pages or pages != expected_pages:
        raise RuntimeError("raw or Pages reader is not byte-exact to the public release archive")

    run = gh_json(f"repos/{OWNER}/{REPOSITORY}/actions/runs/{RUN_ID}")
    if (run.get("id") != RUN_ID or run.get("head_sha") != RELEASE_COMMIT
            or run.get("status") != "completed" or run.get("conclusion") != "success"):
        raise RuntimeError("workflow run identity/result mismatch")
    jobs_payload = gh_json(f"repos/{OWNER}/{REPOSITORY}/actions/runs/{RUN_ID}/jobs?per_page=100")
    jobs = [job for job in jobs_payload.get("jobs", []) if job.get("id") == JOB_ID]
    if len(jobs) != 1 or jobs[0].get("conclusion") != "success":
        raise RuntimeError("Pages job identity/result mismatch")
    deployment = gh_json(f"repos/{OWNER}/{REPOSITORY}/deployments/{DEPLOYMENT_ID}")
    if deployment.get("id") != DEPLOYMENT_ID or deployment.get("sha") != RELEASE_COMMIT:
        raise RuntimeError("Pages deployment identity mismatch")
    statuses = gh_json(f"repos/{OWNER}/{REPOSITORY}/deployments/{DEPLOYMENT_ID}/statuses")
    statuses = [item for item in statuses if item.get("id") == DEPLOYMENT_STATUS_ID]
    if (len(statuses) != 1 or statuses[0].get("state") != "success"
            or statuses[0].get("environment_url") !=
            "https://kokunoyumeto.github.io/algebraic-topology-id/"):
        raise RuntimeError("Pages deployment status mismatch")

    receipt = {
        "schema_version": "1.0",
        "receipt_id": "O012-GITHUB-PUBLICATION-UNITS-001-025",
        "status": "pushed_deployed_and_anonymously_byte_verified",
        "verified_at": VERIFIED_AT,
        "repository": f"https://github.com/{OWNER}/{REPOSITORY}",
        "branch": "main",
        "previous_public_commit": BASE_COMMIT,
        "content_commit": CONTENT_COMMIT,
        "release_commit": RELEASE_COMMIT,
        "release_tree": RELEASE_TREE,
        "anonymous_main_ref": main_ref,
        "release_delta_files": len(files),
        "release_delta_manifest_sha256": manifest_hasher.hexdigest(),
        "files": files,
        "anonymous_archives": {
            "base": {"url": f"https://codeload.github.com/{OWNER}/{REPOSITORY}/zip/{BASE_COMMIT}", "bytes": len(base_zip), "sha256": sha256(base_zip)},
            "release": {"url": f"https://codeload.github.com/{OWNER}/{REPOSITORY}/zip/{RELEASE_COMMIT}", "bytes": len(release_zip), "sha256": sha256(release_zip)},
            "zip_integrity": "PASS",
            "removed_paths": 0,
        },
        "pages": {
            "url": PAGES_URL,
            "bytes": len(pages),
            "sha256": sha256(pages),
            "raw_url": raw_url,
            "raw_bytes": len(raw),
            "raw_sha256": sha256(raw),
            "remote_exact": True,
            "source_commit": RELEASE_COMMIT,
            "source_path": "output/html/units-001-025/index.html",
            "workflow_run_id": RUN_ID,
            "workflow_id": run.get("workflow_id"),
            "check_suite_id": run.get("check_suite_id"),
            "job_id": JOB_ID,
            "deployment_id": DEPLOYMENT_ID,
            "deployment_status_id": DEPLOYMENT_STATUS_ID,
            "conclusion": "success",
        },
        "backend": {
            "records": 3913,
            "bytes": 4007903,
            "bundle_sha256": "8b50629f25c5fcbedb6d5547f8f7151c622aa90e04f71583008bd176058a4f78",
        },
        "verification_method": {
            "artifact_inventory_and_bytes": "anonymous commit-pinned codeload ZIP plus raw and Pages readback",
            "branch_ref": "anonymous git-upload-pack ls-remote with credential helper disabled",
            "workflow_metadata": "authenticated GitHub API through configured CLI; credential value never read or recorded",
            "local_worktree_used_for_public_bytes": False,
            "credentials_recorded": False,
        },
        "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra",
        "source_and_human_credit_preserved": True,
        "upstream_contacted": False,
        "unit_025_included": True,
    }
    OUTPUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "status": receipt["status"],
        "files": len(files),
        "manifest_sha256": receipt["release_delta_manifest_sha256"],
        "pages_bytes": len(pages),
        "pages_sha256": sha256(pages),
        "receipt": str(OUTPUT.relative_to(ROOT)).replace("\\", "/"),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
