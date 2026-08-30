#!/usr/bin/env python3
"""Verify the final D60 GitHub commit, Pages reader, routes, and Zenodo lineage."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

import requests


LANE = Path(__file__).resolve().parents[1]
OWNER = "KokunoYumeto"
REPOSITORY = "algebraic-topology-id"
API = f"https://api.github.com/repos/{OWNER}/{REPOSITORY}"
RAW = f"https://raw.githubusercontent.com/{OWNER}/{REPOSITORY}"
PAGES = f"https://{OWNER.lower()}.github.io/{REPOSITORY}"
BASE_COMMIT = "2fd93503ee70d6e0bfee0c55c8c1e41cbb7b2cb8"
SLUG = (
    "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-"
    "lab01-lab02-lab03-lab04-capstone"
)
TOKEN = (
    "ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_"
    "LAB01_LAB02_LAB03_LAB04_CAPSTONE"
)
HTML_PATH = f"output/html/{SLUG}/index.html"
PDF_PATH = f"output/pdf/topologi-aljabar-{SLUG}-id.pdf"
MANIFEST_PATH = f"output/ARTIFACT_MANIFEST_{TOKEN}.csv"
ZENODO_DIR = LANE / "release" / f"zenodo-{SLUG}"
ZENODO_RECEIPT = ZENODO_DIR / "publication-receipt.json"
OUTPUT = LANE / "00_control" / f"GITHUB_PUBLICATION_RECEIPT_{TOKEN}.json"
PREVIOUS_RECORD_ID = 22_161_294
PREVIOUS_DOI = "10.5281/zenodo.22161294"
CONCEPT_DOI = "10.5281/zenodo.22061489"
BACKEND = (
    8_338,
    10_040_043,
    "8a3ffc9618e56dfce048c41e938aabef4ffbfd3db20a03a4f52f218985230dbb",
)
BACKEND_FILES = (
    "artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
    "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
    "segments.jsonl", "terms.jsonl", "units.jsonl",
)
REQUIRED_CHANGED_PATHS = {
    ".github/workflows/pages.yml",
    "00_control/BUILD.md",
    "00_control/CURRENT_GOAL_AND_WORKFLOW.md",
    "00_control/CURRENT_STATE.md",
    "00_control/CURSOR.json",
    "README.md",
    *(f"backend/{name}" for name in BACKEND_FILES if name not in {"assets.jsonl", "authority.jsonl"}),
    HTML_PATH,
    PDF_PATH,
    MANIFEST_PATH,
    "source/id-ID/capstone/o012-d60-capstone-klein-bottle.md",
    "qa/BACKEND_CAPSTONE_FINAL_REV3_CUMULATIVE_RECEIPT.json",
    "qa/BACKEND_CAPSTONE_FINAL_REV3_VALIDATION.json",
    "qa/PROOF_REPAIR_CENSUS.json",
    f"qa/{TOKEN}_BUILD_RECEIPT.json",
    "scripts/package-release-final-capstone.py",
    "scripts/publish-zenodo-final-capstone.py",
    "scripts/verify-github-final-capstone.py",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def local_identity(relative: str) -> dict[str, Any]:
    path = (LANE / relative).resolve()
    if LANE.resolve() not in path.parents or not path.is_file():
        raise FileNotFoundError(path)
    data = path.read_bytes()
    return {"path": relative, "bytes": len(data), "sha256": sha256(data)}


def get_json(url: str, *, attempts: int = 12) -> dict[str, Any]:
    last = ""
    for attempt in range(attempts):
        response = requests.get(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "Cache-Control": "no-cache",
                "User-Agent": "Codex-D60-public-verifier",
            },
            timeout=180,
        )
        if response.status_code == 200:
            return response.json()
        last = f"HTTP {response.status_code}: {response.text[:200]}"
        if response.status_code not in {403, 404, 429, 502, 503, 504}:
            break
        time.sleep(min(3 + attempt, 15))
    raise RuntimeError(f"public JSON unavailable: {url}: {last}")


def get_bytes(url: str, *, attempts: int = 24) -> bytes:
    last = ""
    for attempt in range(attempts):
        response = requests.get(
            url,
            headers={"Cache-Control": "no-cache", "User-Agent": "Codex-D60-public-byte-verifier"},
            timeout=240,
        )
        if response.status_code == 200:
            return response.content
        last = f"HTTP {response.status_code}"
        if response.status_code not in {403, 404, 429, 502, 503, 504}:
            break
        time.sleep(min(5 + attempt, 20))
    raise RuntimeError(f"public bytes unavailable: {url}: {last}")


def verify_remote_file(commit: str, relative: str) -> dict[str, Any]:
    local = local_identity(relative)
    remote = get_bytes(f"{RAW}/{commit}/{relative}")
    if (len(remote), sha256(remote)) != (local["bytes"], local["sha256"]):
        raise RuntimeError(f"commit-pinned public byte mismatch: {relative}")
    return {**local, "url": f"{RAW}/{commit}/{relative}", "status": 200}


def backend_identity() -> dict[str, Any]:
    state = hashlib.sha256()
    records = 0
    byte_count = 0
    for name in BACKEND_FILES:
        data = (LANE / "backend" / name).read_bytes()
        records += len(data.splitlines())
        byte_count += len(data)
        state.update(name.encode("utf-8"))
        state.update(b"\0")
        state.update(data)
    identity = {"records": records, "bytes": byte_count, "bundle_sha256": state.hexdigest()}
    if (records, byte_count, identity["bundle_sha256"]) != BACKEND:
        raise RuntimeError("local final backend identity drift")
    return identity


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--content-commit", required=True)
    parser.add_argument("--content-tree", required=True)
    parser.add_argument("--run-id", type=int, required=True)
    parser.add_argument("--expected-changed-files", type=int, required=True)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    for name in ("content_commit", "content_tree"):
        if re.fullmatch(r"[0-9a-f]{40}", getattr(args, name)) is None:
            parser.error(f"--{name.replace('_', '-')} must be lowercase 40-hex")
    if args.content_commit == BASE_COMMIT:
        parser.error("content commit must advance the public predecessor")
    if args.run_id <= 0 or args.expected_changed_files <= 0:
        parser.error("run id and changed-file count must be positive")
    return args


def main() -> None:
    args = parse_args()
    if args.output.resolve() != OUTPUT.resolve():
        raise RuntimeError("output escaped the canonical task-local receipt")

    commit = get_json(f"{API}/commits/{args.content_commit}")
    if (
        commit.get("sha") != args.content_commit
        or commit.get("commit", {}).get("tree", {}).get("sha") != args.content_tree
        or BASE_COMMIT not in {row.get("sha") for row in commit.get("parents", [])}
    ):
        raise RuntimeError("commit identity/tree/parent lineage mismatch")

    comparison = get_json(f"{API}/compare/{BASE_COMMIT}...{args.content_commit}")
    changed = {row.get("filename") for row in comparison.get("files", [])}
    if comparison.get("status") != "ahead" or len(changed) != args.expected_changed_files:
        raise RuntimeError("GitHub comparison status or changed-file count drift")
    missing = sorted(REQUIRED_CHANGED_PATHS - changed)
    if missing:
        raise RuntimeError(f"required final changed paths missing: {missing}")

    run = get_json(f"{API}/actions/runs/{args.run_id}")
    if not (
        run.get("head_sha") == args.content_commit
        and run.get("status") == "completed"
        and run.get("conclusion") == "success"
        and run.get("name") == "Deploy Indonesian reader"
    ):
        raise RuntimeError("Pages workflow run did not close successfully on final commit")

    local_backend = backend_identity()
    public_commit_files = [
        verify_remote_file(args.content_commit, relative)
        for relative in (
            HTML_PATH,
            PDF_PATH,
            MANIFEST_PATH,
            ".github/workflows/pages.yml",
            *(f"backend/{name}" for name in BACKEND_FILES),
        )
    ]

    html_local = local_identity(HTML_PATH)
    pages_url = f"{PAGES}/{SLUG}/"
    pages_data = get_bytes(pages_url)
    if (len(pages_data), sha256(pages_data)) != (html_local["bytes"], html_local["sha256"]):
        raise RuntimeError("deployed Pages reader bytes differ from final local reader")
    pages_text = pages_data.decode("utf-8")
    route_rows = []
    for number in range(1, 15):
        route_id = f"D60-R{number:02d}"
        occurrences = len(re.findall(rf"\b{re.escape(route_id)}\b", pages_text))
        if occurrences == 0:
            raise RuntimeError(f"learner route missing from public reader: {route_id}")
        route_rows.append({"course_route_unit_id": route_id, "occurrences": occurrences, "status": "PASS"})
    for marker in (
        "D60-CAPSTONE",
        "D60-LAB01",
        "D60-LAB04",
        "108/108",
        "Roberts 1–30",
        "Fomberg 1–7",
    ):
        if marker not in pages_text:
            raise RuntimeError(f"public learner surface omits scope marker: {marker}")

    publication = json.loads(ZENODO_RECEIPT.read_text(encoding="utf-8"))
    if not (
        publication.get("status") == "PUBLISHED_AND_TWICE_ANONYMOUSLY_VERIFIED"
        and publication.get("previous_record_id") == PREVIOUS_RECORD_ID
        and publication.get("previous_doi") == PREVIOUS_DOI
        and publication.get("concept_doi") == CONCEPT_DOI
        and publication.get("verification", {}).get("all_nine_files_read_twice") is True
        and len(publication.get("files", [])) == 9
    ):
        raise RuntimeError("Zenodo final publication receipt is not completely closed")
    previous = get_json(f"https://zenodo.org/api/records/{PREVIOUS_RECORD_ID}")
    if previous.get("doi") != PREVIOUS_DOI or previous.get("conceptdoi") != CONCEPT_DOI:
        raise RuntimeError("public Zenodo predecessor/concept lineage drift")

    receipt = {
        "schema_version": "1.0",
        "status": "PUBLISHED_AND_ANONYMOUSLY_VERIFIED",
        "repository": f"https://github.com/{OWNER}/{REPOSITORY}",
        "content_commit": args.content_commit,
        "content_tree": args.content_tree,
        "base_commit": BASE_COMMIT,
        "changed_file_count": len(changed),
        "required_changed_paths_verified": sorted(REQUIRED_CHANGED_PATHS),
        "workflow": {
            "run_id": args.run_id,
            "url": run.get("html_url"),
            "status": run.get("status"),
            "conclusion": run.get("conclusion"),
            "head_sha": run.get("head_sha"),
        },
        "pages": {
            "url": pages_url,
            "status": 200,
            "bytes": len(pages_data),
            "sha256": sha256(pages_data),
            "all_fourteen_learner_routes_present": True,
            "routes": route_rows,
        },
        "backend": local_backend,
        "commit_pinned_public_files": public_commit_files,
        "zenodo": {
            "record_id": publication["record_id"],
            "doi": publication["doi"],
            "concept_doi": publication["concept_doi"],
            "previous_record_id": PREVIOUS_RECORD_ID,
            "previous_doi": PREVIOUS_DOI,
            "nine_files_read_twice": True,
        },
        "privacy": {
            "credentials_recorded": False,
            "authorization_headers_recorded": False,
            "absolute_local_paths_recorded": False,
            "user_personal_name_recorded": False,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"status": receipt["status"], "receipt": args.output.name, "pages": pages_url, "zenodo_doi": publication["doi"]}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"FAIL_CLOSED: {error}", file=sys.stderr)
        raise
