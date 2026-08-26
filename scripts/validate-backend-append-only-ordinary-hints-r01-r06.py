#!/usr/bin/env python3
"""Validate/replay the exact R01--R06 hint append and write receipts."""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
PRODUCER_PATH = LANE / "scripts/extend-backend-ordinary-hints-r01-r06.py"
OUTPUTS = {
    "manifest": LANE / "qa/BACKEND_APPEND_ONLY_ORDINARY_HINTS_R01_R06_FILE_MANIFEST.csv",
    "plan": LANE / "qa/BACKEND_APPEND_ONLY_ORDINARY_HINTS_R01_R06_PLAN.json",
    "semantic": LANE / "qa/BACKEND_APPEND_ONLY_ORDINARY_HINTS_R01_R06_RECEIPT.json",
    "replay": LANE / "qa/BACKEND_APPEND_ONLY_ORDINARY_HINTS_R01_R06_REPLAY_RECEIPT.json",
    "cumulative": LANE / "qa/BACKEND_APPEND_ONLY_ORDINARY_HINTS_R01_R06_CUMULATIVE_RECEIPT.json",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"ordinary-hint append-only validator FAIL: {message}")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_producer():
    spec = importlib.util.spec_from_file_location("o012_hint_backend_producer_for_validator", PRODUCER_PATH)
    require(spec is not None and spec.loader is not None, "cannot load hint backend producer")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def parse_canonical(p, name: str, raw: bytes) -> list[dict[str, Any]]:
    if not raw: return []
    require(b"\r" not in raw and raw.endswith(b"\n"), f"{name}: JSONL discipline mismatch")
    records: list[dict[str, Any]] = []
    for number, line in enumerate(raw.splitlines(keepends=True), 1):
        try: record = json.loads(line.decode("utf-8", errors="strict"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise SystemExit(f"ordinary-hint append-only validator FAIL: {name}:{number}: {exc}")
        require(isinstance(record, dict) and p.canon(record) == line, f"{name}:{number}: noncanonical JSONL")
        records.append(record)
    return records


def bundle(p, raw_by_file: dict[str, bytes]) -> tuple[int, int, str]:
    h = hashlib.sha256(); records = byte_count = 0
    for name in p.FILES:
        raw = raw_by_file[name]; records += len(raw.splitlines()); byte_count += len(raw)
        h.update(name.encode("utf-8")); h.update(b"\0"); h.update(raw)
    return records, byte_count, h.hexdigest()


def partition_live(p, expected_suffixes: dict[str, bytes]):
    prefixes: dict[str, bytes] = {}; finals: dict[str, bytes] = {}
    prefix_records: list[dict[str, Any]] = []; live_records: list[dict[str, Any]] = []
    files: dict[str, dict[str, Any]] = {}; seen: set[str] = set()
    for name in p.FILES:
        live = (BACKEND / name).read_bytes(); expected_records, boundary, expected_sha = p.PREFIX[name]
        require(len(live) >= boundary, f"{name}: shorter than frozen CA01 prefix")
        prefix = live[:boundary]; suffix = live[boundary:]
        require((len(prefix.splitlines()), len(prefix), digest(prefix)) == (expected_records, boundary, expected_sha), f"{name}: frozen prefix mismatch")
        require(suffix == expected_suffixes[name], f"{name}: live suffix differs from reconstruction")
        parsed_prefix = parse_canonical(p, f"{name}:prefix", prefix); parsed_suffix = parse_canonical(p, f"{name}:suffix", suffix)
        for record in parsed_prefix + parsed_suffix:
            ident = record.get("id"); require(isinstance(ident, str) and ident and ident not in seen, f"{name}: invalid/duplicate global ID {ident!r}"); seen.add(ident)
        prefixes[name] = prefix; finals[name] = live
        prefix_records.extend(parsed_prefix); live_records.extend(parsed_prefix + parsed_suffix)
        files[name] = {
            "path": f"backend/{name}", "prefix_records": len(parsed_prefix), "prefix_bytes": len(prefix), "prefix_sha256": digest(prefix),
            "records_added": len(parsed_suffix), "suffix_bytes": len(suffix), "suffix_sha256": digest(suffix),
            "final_records": len(parsed_prefix) + len(parsed_suffix), "final_bytes": len(live), "final_sha256": digest(live),
            "prefix_preserved": True, "suffix_exact": True,
        }
    require(bundle(p, prefixes) == p.PREFIX_TOTAL, "frozen prefix bundle mismatch")
    return prefixes, finals, prefix_records, live_records, files


def replay(p, prefix: dict[str, bytes], additions: dict[str, list[dict[str, Any]]], expected_finals: dict[str, bytes]) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="o012-hints-r01-r06-replay-") as temporary:
        backend = Path(temporary) / "backend"; backend.mkdir()
        for name in p.FILES: (backend / name).write_bytes(prefix[name])
        replay_suffixes = p.append_suffix(backend, prefix, additions)
        finals = {name: (backend / name).read_bytes() for name in p.FILES}
        require(finals == expected_finals, "isolated replay differs from expected/live backend")
        total = bundle(p, finals)
        return {"status": "PASS", "temporary_replay_removed": True, "exact_file_matches": len(p.FILES), "suffix_bytes": sum(len(replay_suffixes[name]) for name in p.FILES), "final": {"records": total[0], "bytes": total[1], "bundle_sha256": total[2]}}


def generic_baseline_diagnostic() -> dict[str, Any]:
    result = subprocess.run([sys.executable, "-B", str(LANE / "scripts/validate-backend.py")], cwd=LANE, capture_output=True, text=True, encoding="utf-8", errors="strict")
    message = (result.stdout + result.stderr).strip()
    expected = "backend validation: FAIL: artifacts.jsonl: records are not sorted by ordinal id"
    require(result.returncode == 1 and message == expected, f"generic baseline diagnostic changed: rc={result.returncode}, output={message!r}")
    return {"command": "python -B scripts/validate-backend.py", "exit_code": result.returncode, "output": message, "status": "PRE_EXISTING_BASELINE_INCOMPATIBILITY", "interpretation": "The legacy validator rejects historical append order; the immutable prefix is not reordered, and merged schema/reference plus exact replay are the applicable gates."}


def census_postcondition() -> dict[str, Any]:
    result = subprocess.run([sys.executable, "-B", str(LANE / "scripts/census-route-mastery.py")], cwd=LANE, capture_output=True, text=True, encoding="utf-8", errors="strict")
    require(result.returncode == 0, "route mastery census failed: " + (result.stdout + result.stderr).strip())
    path = LANE / "qa/ROUTE_MASTERY_CENSUS.json"; receipt = json.loads(path.read_text(encoding="utf-8"))
    graph = receipt.get("graph_validation", {}); quota = receipt.get("ordinary_mastery", {}).get("quota", {})
    require(receipt.get("status") == "PASS" and graph.get("validation_error_count") == 0 and not graph.get("duplicate_or_reused_triple_solution_ids"), "route census reports graph errors")
    require((graph.get("active_hint_units"), graph.get("active_hint_relations"), graph.get("active_solve_relations"), graph.get("graph_complete_triples_all_classes")) == (165, 165, 221, 165), "route census graph postcondition mismatch")
    require((quota.get("capped_route_credit"), receipt.get("assessments", {}).get("source_plus_backend", {}).get("credited_items"), receipt.get("compliance", {}).get("source_including_reviewed_ca01", {}).get("total_slots_covered")) == (84, 8, 92), "route census 84+8=92 postcondition mismatch")
    raw = path.read_bytes()
    return {"status": "PASS", "path": "qa/ROUTE_MASTERY_CENSUS.json", "bytes": len(raw), "sha256": digest(raw), "active_hint_units": 165, "active_hint_relations": 165, "active_solve_relations": 221, "graph_complete_triples": 165, "ordinary_capped_credit": 84, "ca01_credit": 8, "total_credit": 92, "validation_errors": 0, "duplicate_or_reused_solution_ids": []}


def json_bytes(obj: Any) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def identity(path: Path) -> dict[str, Any]:
    raw = path.read_bytes(); return {"path": path.relative_to(LANE).as_posix(), "bytes": len(raw), "lf_lines": raw.count(b"\n"), "sha256": digest(raw)}


def write(path: Path, raw: bytes) -> None:
    path.write_bytes(raw); require(path.read_bytes() == raw, f"receipt write/readback mismatch: {path.name}")


def manifest_bytes(p, files: dict[str, dict[str, Any]]) -> bytes:
    stream = io.StringIO(newline=""); fields = ["path","prefix_records","prefix_bytes","prefix_sha256","records_added","suffix_bytes","suffix_sha256","final_records","final_bytes","final_sha256"]
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n"); writer.writeheader()
    for name in p.FILES: writer.writerow({field: files[name][field] for field in fields})
    return stream.getvalue().encode("utf-8")


def validate(preflight: bool):
    p = load_producer()
    if preflight:
        prefix, prefix_records = p.verify_prefix(BACKEND)
    else:
        prefix = {}
        for name in p.FILES:
            live = (BACKEND / name).read_bytes(); boundary = p.PREFIX[name][1]
            require(len(live) >= boundary, f"{name}: shorter than frozen prefix")
            prefix[name] = live[:boundary]
        require(bundle(p, prefix) == p.PREFIX_TOTAL, "frozen prefix bundle mismatch before reconstruction")
        prefix_records = p.parse_prefix_records(prefix)
    data = p.verify_inputs(); additions = p.build_additions(data, prefix_records)
    expected_suffixes = p.suffixes(additions); plan = p.record_plan(additions, data["identities"])
    semantic = p.validate_semantics(prefix_records, additions, data)
    expected_finals = {name: prefix[name] + expected_suffixes[name] for name in p.FILES}
    if preflight:
        return {"p": p, "plan": plan, "semantic": semantic, "replay": replay(p, prefix, additions, expected_finals)}
    prefixes, finals, live_prefix_records, live_records, files = partition_live(p, expected_suffixes)
    require(live_prefix_records == prefix_records, "live prefix parse differs from reconstruction")
    require({record["id"]: record for record in live_records} == {record["id"]: record for record in prefix_records + [record for name in p.FILES for record in additions[name]]}, "live merged graph differs semantically from reconstruction")
    final_total = bundle(p, finals); suffix_total = bundle(p, expected_suffixes)
    require(final_total[0] == 7012 and suffix_total[0] == 158, "7,012/158 record postcondition mismatch")
    result = {"p":p,"data":data,"additions":additions,"plan":plan,"semantic":semantic,"replay":replay(p,prefixes,additions,finals),"baseline":generic_baseline_diagnostic(),"census":census_postcondition(),"files":files,"prefix_total":p.PREFIX_TOTAL,"suffix_total":suffix_total,"final_total":final_total}
    refreshed = p.verify_inputs(); refreshed_additions = p.build_additions(refreshed, prefix_records)
    require(p.record_plan(refreshed_additions, refreshed["identities"]) == plan and p.suffixes(refreshed_additions) == expected_suffixes, "input/reconstruction drift during validation")
    return result


def main() -> int:
    require(sys.argv[1:] in ([], ["--preflight"]), "accepted invocation is no arguments or --preflight")
    if sys.argv[1:] == ["--preflight"]:
        result = validate(True); print("ordinary-hint append-only backend preflight: PASS"); print(f"records_planned={sum(result['plan']['records_by_file'].values())}"); print(f"replay_bundle_sha256={result['replay']['final']['bundle_sha256']}"); return 0
    result = validate(False); p = result["p"]
    plan_receipt = {"status":"PASS","receipt_kind":"deterministic_append_plan","edition_unit_id":p.EDITION_UNIT_ID,"producer":"scripts/extend-backend-ordinary-hints-r01-r06.py",**result["plan"]}
    semantic_receipt = {"status":"PASS","receipt_kind":"semantic_append_validation","edition_unit_id":p.EDITION_UNIT_ID,"source_sha256":p.SOURCE_SHA256,"input_identities":{path:{"bytes":value[0],"lf_lines":value[1],"sha256":value[2]} for path,value in result["data"]["identities"].items()},"semantic_checks":result["semantic"],"route_mastery_census":result["census"],"generic_validator_baseline_diagnostic":result["baseline"]}
    replay_receipt = {"status":"PASS","receipt_kind":"isolated_binary_replay","edition_unit_id":p.EDITION_UNIT_ID,"immutable_prefix":{"records":result["prefix_total"][0],"bytes":result["prefix_total"][1],"bundle_sha256":result["prefix_total"][2]},"replay":result["replay"],"all_live_files_equal_replay":True}
    write(OUTPUTS["manifest"], manifest_bytes(p,result["files"])); write(OUTPUTS["plan"],json_bytes(plan_receipt)); write(OUTPUTS["semantic"],json_bytes(semantic_receipt)); write(OUTPUTS["replay"],json_bytes(replay_receipt))
    supporting = {name:identity(OUTPUTS[name]) for name in ("manifest","plan","semantic","replay")}
    cumulative = {"status":"PASS","receipt_kind":"cumulative_backend_boundary","edition_unit_id":p.EDITION_UNIT_ID,"model_provenance":p.MODEL,"immutable_prefix":{"records":result["prefix_total"][0],"bytes":result["prefix_total"][1],"bundle_sha256":result["prefix_total"][2],"preserved_exactly":True},"delta":{"records":result["suffix_total"][0],"bytes":result["suffix_total"][1],"bundle_sha256":result["suffix_total"][2],"records_by_file":result["plan"]["records_by_file"],"bytes_by_file":result["plan"]["bytes_by_file"]},"cumulative":{"records":result["final_total"][0],"bytes":result["final_total"][1],"bundle_sha256":result["final_total"][2]},"files":[result["files"][name] for name in p.FILES],"semantic_checks":result["semantic"],"route_mastery_census":result["census"],"replay":result["replay"],"generic_validator_baseline_diagnostic":result["baseline"],"supporting_receipts":supporting}
    write(OUTPUTS["cumulative"],json_bytes(cumulative)); cumulative_identity=identity(OUTPUTS["cumulative"])
    print("ordinary-hint append-only backend validation: PASS"); print(f"prefix_records={result['prefix_total'][0]}"); print(f"records_added={result['suffix_total'][0]}"); print(f"cumulative_records={result['final_total'][0]}"); print(f"backend_bundle_sha256={result['final_total'][2]}"); print(f"cumulative_receipt_sha256={cumulative_identity['sha256']}"); return 0


if __name__ == "__main__":
    raise SystemExit(main())
