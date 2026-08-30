#!/usr/bin/env python3
"""Prepare the non-self-referential final capstone reader/artifact suffix."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
OUT = ROOT / "qa/capstone-final-artifacts-backend-20260829"
FILES = (
    "artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
    "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
    "segments.jsonl", "terms.jsonl", "units.jsonl",
)
TIMESTAMP = "2026-08-29T00:00:00Z"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
ROOT_UNIT = "unit:o012-d60-capstone-rev2"
RIGHTS = "rights:o012-d60-capstone-original-cc-by-sa-4.0-rev2"
EDITION_UNIT = "O012-ORIG-CAPSTONE"
MANIFEST_ID = "artifact:o012-d60-capstone-manifest-final"
EXPECTED_BASELINE = {
    "records": 8168,
    "bytes": 9836313,
    "bundle_sha256": "db8dc42ad60f52a9995ef9bf656a3b1e2d3357592e404e404559ae1a4858452f",
}


def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(row: dict[str, Any]) -> bytes:
    return (json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def bundle(raw_by_file: dict[str, bytes]) -> dict[str, Any]:
    state = hashlib.sha256()
    records = 0
    byte_count = 0
    for name in FILES:
        raw = raw_by_file[name]
        records += len(raw.splitlines())
        byte_count += len(raw)
        state.update(name.encode("utf-8"))
        state.update(b"\0")
        state.update(raw)
    return {"records": records, "bytes": byte_count, "bundle_sha256": state.hexdigest()}


def load_backend() -> tuple[dict[str, bytes], dict[str, dict[str, Any]]]:
    raw_by_file: dict[str, bytes] = {}
    by_id: dict[str, dict[str, Any]] = {}
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        require(raw.endswith(b"\n") and b"\r" not in raw, f"invalid JSONL bytes: {name}")
        for line in raw.splitlines(keepends=True):
            row = json.loads(line)
            require(canon(row) == line, f"noncanonical JSONL: {name}")
            require(row["id"] not in by_id, f"duplicate live ID: {row['id']}")
            by_id[row["id"]] = row
        raw_by_file[name] = raw
    require(bundle(raw_by_file) == EXPECTED_BASELINE, "semantic-revision baseline drift")
    require(ROOT_UNIT in by_id and RIGHTS in by_id, "semantic rev2 root/rights missing")
    return raw_by_file, by_id


def identity(path: str) -> tuple[int, str]:
    raw = (ROOT / path).read_bytes()
    return len(raw), sha(raw)


def additions(existing: dict[str, dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    out = {name: [] for name in FILES}
    qa_specs = {
        "qa:o012-d60-capstone-final-build": {
            "qa_type": "build",
            "note": "Final deterministic HTML/PDF/manifest build passed and binds the corrected capstone source plus proof census.",
            "witnesses": [
                "artifact:o012-d60-capstone-source-final",
                "artifact:o012-d60-capstone-html-final",
                "artifact:o012-d60-capstone-pdf-final",
                MANIFEST_ID,
                "artifact:o012-d60-capstone-build-receipt-final",
            ],
        },
        "qa:o012-d60-capstone-final-visual": {
            "qa_type": "visual",
            "note": "Transition page and all six capstone PDF pages passed original-detail visual inspection at P1=P2=P3=0.",
            "witnesses": ["artifact:o012-d60-capstone-pdf-final", "artifact:o012-d60-capstone-visual-qa-final"],
        },
        "qa:o012-d60-capstone-final-browser": {
            "qa_type": "browser",
            "note": "Final self-contained HTML passed desktop/mobile reflow, fragment, MathML, runtime-asset, and console checks at P1=P2=P3=0.",
            "witnesses": ["artifact:o012-d60-capstone-html-final", "artifact:o012-d60-capstone-browser-qa-final"],
        },
        "qa:o012-d60-capstone-final-proof-closure": {
            "qa_type": "proof",
            "note": "All four named proof-repair graphs remain closed after the append-only capstone semantic revision.",
            "witnesses": ["artifact:o012-d60-proof-census-final", "artifact:o012-d60-capstone-semantic-backend-receipt-final"],
        },
    }
    artifact_specs = [
        ("artifact:o012-d60-capstone-source-final", "source/id-ID/capstone/o012-d60-capstone-klein-bottle.md", "text/markdown", ["qa:o012-d60-capstone-source-rev2", "qa:o012-d60-capstone-final-build"], None),
        ("artifact:o012-d60-capstone-html-final", "output/html/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04-capstone/index.html", "text/html", ["qa:o012-d60-capstone-final-build", "qa:o012-d60-capstone-final-browser"], MANIFEST_ID),
        ("artifact:o012-d60-capstone-pdf-final", "output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04-capstone-id.pdf", "application/pdf", ["qa:o012-d60-capstone-final-build", "qa:o012-d60-capstone-final-visual"], MANIFEST_ID),
        (MANIFEST_ID, "output/ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04_CAPSTONE.csv", "text/csv", ["qa:o012-d60-capstone-final-build"], None),
        ("artifact:o012-d60-capstone-build-receipt-final", "qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04_CAPSTONE_BUILD_RECEIPT.json", "application/json", ["qa:o012-d60-capstone-final-build"], None),
        ("artifact:o012-d60-capstone-visual-qa-final", "qa/capstone/VISUAL_QA.json", "application/json", ["qa:o012-d60-capstone-final-visual"], None),
        ("artifact:o012-d60-capstone-browser-qa-final", "qa/capstone/BROWSER_QA.json", "application/json", ["qa:o012-d60-capstone-final-browser"], None),
        ("artifact:o012-d60-proof-census-final", "qa/PROOF_REPAIR_CENSUS.json", "application/json", ["qa:o012-d60-capstone-final-proof-closure"], None),
        ("artifact:o012-d60-capstone-semantic-backend-receipt-final", "qa/BACKEND_CAPSTONE_FINAL_REV2_SEMANTIC_RECEIPT.json", "application/json", ["qa:o012-d60-capstone-final-proof-closure"], None),
    ]
    for ident, path, media_type, qa_ids, manifest_id in artifact_specs:
        require(ident not in existing, f"artifact ID collision: {ident}")
        file_path = ROOT / path
        require(file_path.is_file(), f"missing final artifact: {path}")
        if path.endswith(".json"):
            data = json.loads(file_path.read_text(encoding="utf-8"))
            require(data.get("status") == "PASS", f"final receipt is not PASS: {path}")
        size, digest = identity(path)
        out["artifacts.jsonl"].append({
            "bytes": size,
            "edition_unit_id": EDITION_UNIT,
            "entity_type": "artifact",
            "id": ident,
            "locale": "id-ID",
            "manifest_artifact_id": manifest_id,
            "media_type": media_type,
            "model_provenance": MODEL,
            "path": path,
            "qa_event_ids": qa_ids,
            "rights_component_id": RIGHTS,
            "schema": "curriculum.interop",
            "schema_version": "0.1.0",
            "sha256": digest,
            "status": "active",
            "supersedes": None,
            "timestamp": TIMESTAMP,
            "toolchain": "Final D60 capstone reader, evidence, and append-only backend closure; OpenAI Codex gpt-5.6-sol, Ultra.",
            "translation_state": "built",
            "unit_id": ROOT_UNIT,
            "workflow": "o012-d60-id-reader-production",
        })
    artifact_ids = {row["id"] for row in out["artifacts.jsonl"]}
    for ident, spec in qa_specs.items():
        require(ident not in existing, f"QA ID collision: {ident}")
        require(set(spec["witnesses"]).issubset(artifact_ids), f"QA witness drift: {ident}")
        out["qa.jsonl"].append({
            "capstone_id": "D60-CAPSTONE",
            "entity_type": "qa_event",
            "id": ident,
            "model_provenance": MODEL,
            "note": spec["note"],
            "qa_type": spec["qa_type"],
            "result": "passed",
            "schema": "curriculum.interop",
            "schema_version": "0.1.0",
            "status": "active",
            "supersedes": None,
            "timestamp": TIMESTAMP,
            "unit_id": ROOT_UNIT,
            "witness_artifact_ids": spec["witnesses"],
            "workflow": "o012-d60-id-reader-production",
        })
    for name in FILES:
        out[name].sort(key=lambda row: row["id"])
    return out


def validate(add: dict[str, list[dict[str, Any]]], existing: dict[str, dict[str, Any]]) -> None:
    require(len(add["artifacts.jsonl"]) == 9 and len(add["qa.jsonl"]) == 4, "final artifact suffix census drift")
    require(sum(len(rows) for rows in add.values()) == 13, "final artifact suffix total drift")
    new_rows = [row for rows in add.values() for row in rows]
    ids = [row["id"] for row in new_rows]
    require(len(ids) == len(set(ids)) and not set(ids).intersection(existing), "final artifact ID collision")
    all_ids = set(existing).union(ids)
    for row in new_rows:
        for key in ("manifest_artifact_id", "rights_component_id", "unit_id"):
            value = row.get(key)
            if value is not None:
                require(value in all_ids, f"unknown final reference: {row['id']}.{key}={value}")
        for key in ("qa_event_ids", "witness_artifact_ids"):
            for value in row.get(key, []):
                require(value in all_ids, f"unknown final reference: {row['id']}.{key}={value}")
    by_new = {row["id"]: row for row in new_rows}
    for artifact in add["artifacts.jsonl"]:
        for qid in artifact["qa_event_ids"]:
            if qid in by_new:
                require(artifact["id"] in by_new[qid]["witness_artifact_ids"], f"artifact/QA reverse binding drift: {artifact['id']}")


def write_run(run: str, baseline: dict[str, bytes], add: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    target = OUT / run
    require(not target.exists(), f"candidate collision: {target}")
    target.mkdir(parents=True)
    suffix: dict[str, bytes] = {}
    final: dict[str, bytes] = {}
    identities: dict[str, dict[str, Any]] = {}
    for name in FILES:
        raw = b"".join(canon(row) for row in add[name])
        suffix[name] = raw
        final[name] = baseline[name] + raw
        (target / name).write_bytes(raw)
        identities[name] = {"records": len(raw.splitlines()), "bytes": len(raw), "sha256": sha(raw)}
    receipt = {
        "status": "PASS_CANDIDATE",
        "receipt_kind": "final_capstone_artifact_append_only_candidate",
        "model_provenance": MODEL,
        "baseline": bundle(baseline),
        "suffix": identities,
        "suffix_total": bundle(suffix),
        "final": bundle(final),
    }
    (target / "RECEIPT.json").write_text(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    return receipt


def main() -> int:
    require(not OUT.exists(), f"candidate output already exists: {OUT}")
    baseline, existing = load_backend()
    add = additions(existing)
    validate(add, existing)
    run_a = write_run("run-a", baseline, add)
    run_b = write_run("run-b", baseline, add)
    require(run_a == run_b, "two-run final artifact receipt drift")
    for name in FILES:
        require((OUT / "run-a" / name).read_bytes() == (OUT / "run-b" / name).read_bytes(), f"two-run final artifact byte drift: {name}")
    print(json.dumps({"status": "PASS_CANDIDATE_ONLY", "baseline": run_a["baseline"], "suffix_total": run_a["suffix_total"], "final": run_a["final"]}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
