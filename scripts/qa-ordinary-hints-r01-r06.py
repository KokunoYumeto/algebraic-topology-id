#!/usr/bin/env python3
"""Fail-closed structural and binding QA for the D60 R01--R06 hint layer."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


LANE = Path(__file__).resolve().parents[1]
SOURCE = LANE / "source/id-ID/mastery/ordinary-hints-r01-r06.md"
MATH_REVIEW = LANE / "qa/ordinary-hints-r01-r06/INDEPENDENT_MATH_REVIEW.json"
LANGUAGE_REVIEW = LANE / "qa/ordinary-hints-r01-r06/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json"
OUTPUT = LANE / "qa/ORDINARY_HINTS_R01_R06_QA.json"
SOURCE_SHA256 = "dc319cb191d709a5807f0c0792401f9faf2993ceede364764547f20bb4f69c2a"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"

FILES = (
    "artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
    "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
    "segments.jsonl", "terms.jsonl", "units.jsonl",
)
PREFIX = {
    "artifacts.jsonl": (193, 157480, "c50a3140513a5d243a6ce9f7256a29e97e3fab776764be476c9bfe9949a83b93"),
    "assets.jsonl": (87, 64692, "1df40f8f6ca4f2fbfbe8a7b924a68a153713a20a4eebe1d014d8fb04669945f7"),
    "authority.jsonl": (6, 4374, "84c622f56dbbd5ba379361245ecfe07bc79c9f4fd6b18ba21b82b5f545211869"),
    "concepts.jsonl": (483, 152695, "720d96a10a3c2abebab164e2181486743ef99efb50c6ef419faefbf528b8ead3"),
    "corrections.jsonl": (564, 594720, "bd961fad5d83e96fec6ef83caa8447e2e5f282c603fd4983d79b5b4b54049fbb"),
    "qa.jsonl": (166, 91181, "25d3dae94c3c117e6aeb8a020fb5076199d25e71e2184ad5bf7c59ab3db722d4"),
    "relations.jsonl": (837, 355526, "64aeedd8836ccae7a9fa9418a4a8b83f93c026432bc8c00dd0ba53a8d0e65ba9"),
    "rights.jsonl": (104, 94600, "2a034be29f7d544de52f4a0a1970bd4923531d4ac13180eaa45b432dc999b404"),
    "segments.jsonl": (1954, 3177411, "d17646479e4a8d91b618de5c4995c083dec5c208ef755d203a876645f7ab9d54"),
    "terms.jsonl": (476, 315218, "4b82f9d582ba747829373a7935fcc3cae56b96fd6b7486969ebb6d54cf927c50"),
    "units.jsonl": (1984, 3337902, "26cf11a2ba912bd8e22983204641ff22ffb0152128f20ca166195cb2abd41f3f"),
}
PREFIX_TOTAL = (6854, 8345799, "51e75d06e620762e629e9e7408da4b0c32b3e337817d9d140fbbdfa438de2f57")

EXPECTED_BINDINGS: dict[str, tuple[tuple[str, str], ...]] = {
    "D60-R01": (
        ("unit:o012-rbt-l01-ex-001", "unit:o012-rbt-l01-sol-001"),
        ("unit:o012-rbt-l01-ex-002", "unit:o012-rbt-l01-sol-002"),
        ("unit:o012-rbt-l02-ex-001", "unit:o012-rbt-l02-sol-001"),
        ("unit:o012-rbt-l02-ex-002", "unit:o012-rbt-l02-sol-002"),
        ("unit:o012-rbt-l02-ex-003", "unit:o012-rbt-l02-sol-003"),
        ("unit:o012-rbt-l02-ex-004", "unit:o012-rbt-l02-sol-004"),
    ),
    "D60-R02": (
        ("unit:o012-rbt-l03-ex-001", "unit:o012-rbt-l03-sol-001"),
        ("unit:o012-rbt-l03-ex-002", "unit:o012-rbt-l03-sol-002"),
        ("unit:o012-rbt-l03-ex-003", "unit:o012-rbt-l03-sol-003"),
        ("unit:o012-rbt-l03-ex-004", "unit:o012-rbt-l03-sol-004"),
        ("unit:o012-rbt-l03-ex-005", "unit:o012-rbt-l03-sol-005"),
        ("unit:o012-rbt-l04-ex-001", "unit:o012-rbt-l04-sol-001"),
    ),
    "D60-R03": (
        ("unit:o012-rbt-l05-mcheck-001", "unit:o012-rbt-l05-sol-001"),
        ("unit:o012-rbt-l05-mcheck-002", "unit:o012-rbt-l05-sol-002"),
        ("unit:o012-rbt-l05-mcheck-003", "unit:o012-rbt-l05-sol-003"),
        ("unit:o012-rbt-l05-mcheck-004", "unit:o012-rbt-l05-sol-004"),
        ("unit:o012-rbt-l06-mcheck-001", "unit:o012-rbt-l06-sol-001"),
        ("unit:o012-rbt-l06-mcheck-002", "unit:o012-rbt-l06-sol-002"),
    ),
    "D60-R04": (
        ("unit:o012-rbt-l07-mcheck-001", "unit:o012-rbt-l07-sol-001"),
        ("unit:o012-rbt-l07-mcheck-002", "unit:o012-rbt-l07-sol-002"),
        ("unit:o012-rbt-l07-mcheck-003", "unit:o012-rbt-l07-sol-003"),
        ("unit:o012-rbt-l07-mcheck-004", "unit:o012-rbt-l07-sol-004"),
        ("unit:o012-rbt-l08-ex-001", "unit:o012-rbt-l08-sol-001"),
        ("unit:o012-rbt-l08-mcheck-002", "unit:o012-rbt-l08-sol-002"),
    ),
    "D60-R05": (
        ("unit:o012-rbt-l11-mcheck-001", "unit:o012-rbt-l11-sol-001"),
        ("unit:o012-rbt-l11-mcheck-002", "unit:o012-rbt-l11-sol-002"),
        ("unit:o012-rbt-l11-mcheck-003", "unit:o012-rbt-l11-sol-003"),
        ("unit:o012-rbt-l12-mcheck-001", "unit:o012-rbt-l12-sol-001"),
        ("unit:o012-rbt-l12-mcheck-002", "unit:o012-rbt-l12-sol-002"),
        ("unit:o012-rbt-l12-mcheck-003", "unit:o012-rbt-l12-sol-003"),
    ),
    "D60-R06": (
        ("unit:o012-rbt-l14-ex-001", "unit:o012-rbt-l14-sol-002"),
        ("unit:o012-rbt-l14-ex-002", "unit:o012-rbt-l14-sol-003"),
        ("unit:o012-rbt-l14-mcheck-001", "unit:o012-rbt-l14-sol-001"),
        ("unit:o012-rbt-l14-mcheck-004", "unit:o012-rbt-l14-sol-004"),
        ("unit:o012-rbt-l14-mcheck-005", "unit:o012-rbt-l14-sol-005"),
        ("unit:o012-rbt-l14-mcheck-006", "unit:o012-rbt-l14-sol-006"),
    ),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def identity(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    return {
        "path": path.relative_to(LANE).as_posix(),
        "bytes": len(raw),
        "lf_lines": raw.count(b"\n"),
        "sha256": digest(raw),
    }


def canon(record: dict[str, Any]) -> bytes:
    return (json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def parse_jsonl(raw: bytes, name: str) -> list[dict[str, Any]]:
    require(not raw or (b"\r" not in raw and raw.endswith(b"\n")), f"{name}: invalid JSONL byte discipline")
    records: list[dict[str, Any]] = []
    for number, line in enumerate(raw.splitlines(keepends=True), 1):
        try:
            record = json.loads(line.decode("utf-8", errors="strict"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"{name}:{number}: invalid JSON: {exc}") from exc
        require(isinstance(record, dict) and canon(record) == line, f"{name}:{number}: noncanonical record")
        records.append(record)
    return records


def frozen_prefix() -> dict[str, list[dict[str, Any]]]:
    total_records = total_bytes = 0
    bundle = hashlib.sha256()
    parsed: dict[str, list[dict[str, Any]]] = {}
    for name in FILES:
        path = LANE / "backend" / name
        require(path.is_file(), f"missing backend file: {name}")
        live = path.read_bytes()
        expected_records, boundary, expected_sha = PREFIX[name]
        require(len(live) >= boundary, f"backend shorter than CA01 prefix: {name}")
        prefix = live[:boundary]
        observed = (len(prefix.splitlines()), len(prefix), digest(prefix))
        require(observed == (expected_records, boundary, expected_sha), f"immutable CA01 prefix drift: {name}: {observed!r}")
        parsed[name] = parse_jsonl(prefix, f"backend/{name}:ca01-prefix")
        total_records += observed[0]
        total_bytes += observed[1]
        bundle.update(name.encode("utf-8")); bundle.update(b"\0"); bundle.update(prefix)
    require((total_records, total_bytes, bundle.hexdigest()) == PREFIX_TOTAL, "immutable CA01 prefix bundle drift")
    return parsed


def component(entity_id: str) -> str:
    match = re.search(r"unit:(o012-rbt-l\d{2})(?:-|$)", entity_id)
    require(match is not None, f"cannot infer Roberts component from {entity_id}")
    return match.group(1)


def route_for_component(component_id: str) -> str:
    lecture = int(component_id.rsplit("l", 1)[1])
    ranges = ((1, 2, 1), (3, 4, 2), (5, 6, 3), (7, 10, 4), (11, 13, 5), (14, 17, 6))
    for start, end, route in ranges:
        if start <= lecture <= end:
            return f"D60-R{route:02d}"
    raise RuntimeError(f"component is outside R01--R06: {component_id}")


def review_binding(review: dict[str, Any], path: Path, expected_kind: str) -> dict[str, Any]:
    require(review.get("review_kind") == expected_kind, f"wrong review kind: {path.name}")
    require(str(review.get("status", "")).startswith("PASS"), f"review is not PASS: {path.name}")
    require(review.get("independent_from_production") is True, f"review is not independent: {path.name}")
    severity = review.get("severity_census", {})
    require((severity.get("P1"), severity.get("P2"), severity.get("P3")) == (0, 0, 0), f"unresolved review finding: {path.name}")
    if expected_kind == "independent_mathematics_and_binding":
        require(review.get("hint_source_sha256") == SOURCE_SHA256, f"math review binds stale source: {path.name}")
        require(review.get("hint_source_bytes") == 28698, f"math review source byte binding drift: {path.name}")
        require(len(review.get("item_results", [])) == 36, f"math review item census is not 36: {path.name}")
        require(review.get("review_scope", {}).get("hints_reviewed") == 36, f"math review scope census is not 36: {path.name}")
    else:
        source_identity = review.get("source_identity", {})
        require((source_identity.get("bytes"), source_identity.get("sha256")) == (28698, SOURCE_SHA256), f"language review binds stale source: {path.name}")
        require(len(review.get("item_verdicts", [])) == 36, f"language review item census is not 36: {path.name}")
        require(review.get("review_scope", {}).get("hint_count") == 36, f"language review scope census is not 36: {path.name}")
    return review


def parse_blocks(text: str) -> list[dict[str, Any]]:
    pattern = re.compile(r"(?ms)^:::\s+\{\.hint\s+#(o012-d60-r\d{2}-hint-\d{3})([^}]*)\}\n(.*?)\n:::\s*$")
    blocks: list[dict[str, Any]] = []
    for stable_id, attribute_text, body in pattern.findall(text):
        attrs = dict(re.findall(r'([a-z0-9-]+)="([^"]*)"', attribute_text))
        blocks.append({"stable_id": stable_id, "attributes": attrs, "body": body})
    return blocks


def main() -> None:
    require(SOURCE.is_file(), "ordinary-hint source is missing")
    raw = SOURCE.read_bytes()
    require((len(raw), raw.count(b"\n"), digest(raw)) == (28698, 410, SOURCE_SHA256), "sealed ordinary-hint source identity drift")
    require(b"\r" not in raw and raw.endswith(b"\n"), "source must be UTF-8/LF with final LF")
    text = raw.decode("utf-8", errors="strict")
    require(text.startswith("---\n") and "\n---\n" in text[4:], "front matter is missing")
    for marker in (
        "edition_unit_id: O012-ORIG-HINTS-R01-R06",
        'rights: "CC BY-SA 4.0"',
        "Materi edisi asli; bukan bagian dari sumber Roberts atau Fomberg.",
        MODEL,
    ):
        require(text.count(marker) == 1, f"required metadata marker missing or repeated: {marker}")

    expected_ids = {"o012-d60-hints-r01-r06"}
    expected_ids.update(f"o012-d60-hints-r{route:02d}" for route in range(1, 7))
    expected_ids.update(f"o012-d60-r{route:02d}-hint-{number:03d}" for route in range(1, 7) for number in range(1, 7))
    declared_ids = re.findall(r"(?m)(?:\{|\s)#(o012-d60-(?:hints-r01-r06|hints-r\d{2}|r\d{2}-hint-\d{3}))(?=[\s}])", text)
    require(len(declared_ids) == len(set(declared_ids)), "duplicate D60 hint-layer stable ID")
    require(set(declared_ids) == expected_ids, f"stable-ID inventory drift: {sorted(set(declared_ids) ^ expected_ids)}")
    require(len(re.findall(r"(?m)^:::\s+\{\.hint\b", text)) == 36, "hint opening census is not 36")
    require(len(re.findall(r"(?m)^:::\s*$", text)) == 36, "hint fence census is not balanced at 36")
    require(text.count("**Petunjuk.**") == 36, "visible hint label census is not 36")
    require(text.count("$$") % 2 == 0, "display-math delimiters are unbalanced")
    for marker in ("TODO", "TBD", "FILL_AFTER", "C:\\Users\\", "github_pat_", "ghp_", "access_token", "Authorization: Bearer"):
        require(marker not in text, f"forbidden marker in source: {marker}")

    blocks = parse_blocks(text)
    require(len(blocks) == 36, "could not parse exactly 36 hint blocks")
    prefix = frozen_prefix()
    units = prefix["units.jsonl"]
    relations = prefix["relations.jsonl"]
    by_id = {record["id"]: record for record in units}
    require(len(by_id) == len(units), "duplicate unit ID in immutable CA01 prefix")
    active_relations = [record for record in relations if record.get("status") == "active"]
    solves_by_target: dict[str, list[dict[str, Any]]] = defaultdict(list)
    hints_by_target: dict[str, list[dict[str, Any]]] = defaultdict(list)
    hinted_solution_ids: set[str] = set()
    for relation in active_relations:
        if relation.get("relation_type") == "solves":
            solves_by_target[relation.get("to_id")].append(relation)
        elif relation.get("relation_type") == "hints":
            hints_by_target[relation.get("to_id")].append(relation)
    for exercise_id in hints_by_target:
        edges = solves_by_target.get(exercise_id, [])
        if len(edges) == 1:
            hinted_solution_ids.add(edges[0].get("from_id"))

    observed_by_route: dict[str, list[tuple[str, str]]] = defaultdict(list)
    binding_receipts: list[dict[str, Any]] = []
    target_ids: set[str] = set()
    solution_ids: set[str] = set()
    for block in blocks:
        stable_id = block["stable_id"]
        attrs = block["attributes"]
        body = block["body"]
        match = re.fullmatch(r"o012-d60-r(\d{2})-hint-(\d{3})", stable_id)
        require(match is not None, f"malformed stable ID: {stable_id}")
        route = f"D60-R{int(match.group(1)):02d}"
        number = int(match.group(2))
        require(route in EXPECTED_BINDINGS and 1 <= number <= 6, f"out-of-scope hint ID: {stable_id}")
        require(attrs.get("data-origin") == "edition-original", f"origin mismatch: {stable_id}")
        require(attrs.get("data-course-route-unit-id") == route, f"route mismatch: {stable_id}")
        target_id = attrs.get("data-target-exercise-id")
        solution_id = attrs.get("data-existing-solution-id")
        source_path = attrs.get("data-source-path")
        component_id = attrs.get("data-component-id")
        require((target_id, solution_id) == EXPECTED_BINDINGS[route][number - 1], f"deterministic binding mismatch: {stable_id}")
        require(target_id not in target_ids and solution_id not in solution_ids, f"duplicate target or solution binding: {stable_id}")
        target_ids.add(target_id); solution_ids.add(solution_id)
        target = by_id.get(target_id); solution = by_id.get(solution_id)
        require(target is not None and target.get("status") == "active" and target.get("unit_kind") == "exercise", f"invalid target exercise: {stable_id}")
        require(solution is not None and solution.get("status") == "active" and solution.get("unit_kind") == "solution", f"invalid existing solution: {stable_id}")
        inferred_component = component(target_id)
        require(component(solution_id) == inferred_component == component_id, f"component binding mismatch: {stable_id}")
        require(route_for_component(inferred_component) == route, f"component-to-route mismatch: {stable_id}")
        require(target.get("target_locator", {}).get("path") == source_path, f"exercise source path mismatch: {stable_id}")
        require(solution.get("target_locator", {}).get("path") == source_path, f"solution source path mismatch: {stable_id}")
        solve_edges = solves_by_target.get(target_id, [])
        require(len(solve_edges) == 1 and solve_edges[0].get("from_id") == solution_id, f"existing solve edge mismatch: {stable_id}")
        require(not hints_by_target.get(target_id), f"target already had an active hint at CA01 prefix: {stable_id}")
        require(solution_id not in hinted_solution_ids, f"solution was already reserved by another hinted exercise: {stable_id}")
        target_anchor = target_id.removeprefix("unit:")
        solution_anchor = solution_id.removeprefix("unit:")
        require(f"[soal](#{target_anchor})" in body and f"[solusi lengkap](#{solution_anchor})" in body, f"reader anchor binding mismatch: {stable_id}")
        require(len(body.strip()) >= 250, f"hint is implausibly short: {stable_id}")
        observed_by_route[route].append((target_id, solution_id))
        binding_receipts.append({
            "stable_id": stable_id, "course_route_unit_id": route,
            "component_id": component_id, "target_exercise_id": target_id,
            "existing_solution_id": solution_id, "source_path": source_path,
            "existing_solve_relation_id": solve_edges[0]["id"],
        })

    require(dict(observed_by_route) == {route: list(pairs) for route, pairs in EXPECTED_BINDINGS.items()}, "route-ordered binding inventory drift")
    require(len(target_ids) == len(solution_ids) == 36, "target/solution one-to-one census mismatch")

    require(MATH_REVIEW.is_file() and LANGUAGE_REVIEW.is_file(), "both independent reviews are required")
    math_review = review_binding(json.loads(MATH_REVIEW.read_text(encoding="utf-8")), MATH_REVIEW, "independent_mathematics_and_binding")
    language_review = review_binding(json.loads(LANGUAGE_REVIEW.read_text(encoding="utf-8")), LANGUAGE_REVIEW, "independent_source_language_and_binding")
    receipt = {
        "qa_id": "O012-D60-ORDINARY-HINTS-R01-R06",
        "status": "PASS",
        "edition_unit_id": "O012-ORIG-HINTS-R01-R06",
        "model_provenance": MODEL,
        "source": {**identity(SOURCE), "stable_ids": len(declared_ids), "hint_blocks": 36},
        "immutable_ca01_backend_prefix": {"records": PREFIX_TOTAL[0], "bytes": PREFIX_TOTAL[1], "bundle_sha256": PREFIX_TOTAL[2], "preserved_exactly": True},
        "bindings": binding_receipts,
        "binding_census": {
            "routes": dict(Counter(item["course_route_unit_id"] for item in binding_receipts)),
            "distinct_target_exercises": len(target_ids),
            "distinct_existing_solutions": len(solution_ids),
            "exact_existing_solve_edges": 36,
            "preexisting_hint_edges_for_targets": 0,
            "solutions_previously_reserved_by_hint_triples": 0,
            "prompt_records_changed": 0,
            "solution_records_changed": 0,
            "solves_relations_changed": 0,
        },
        "rights": {"license": "CC BY-SA 4.0", "origin": "edition_original", "source_prompts_or_solutions_copied": False},
        "independent_reviews": {
            "mathematics": {**identity(MATH_REVIEW), "status": math_review["status"]},
            "source_language": {**identity(LANGUAGE_REVIEW), "status": language_review["status"]},
        },
        "checks": {
            "utf8_lf_and_sealed_identity": "PASS", "front_matter": "PASS",
            "stable_id_uniqueness_and_inventory": "PASS", "balanced_hint_fences": "PASS",
            "deterministic_candidate_binding": "PASS", "exercise_solution_source_binding": "PASS",
            "one_to_one_existing_solve_edges": "PASS", "no_existing_hint_collision": "PASS",
            "reader_anchor_binding": "PASS", "rights_and_origin": "PASS", "privacy": "PASS",
        },
    }
    OUTPUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "output": identity(OUTPUT), "bindings": 36}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
