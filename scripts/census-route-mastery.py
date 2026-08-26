#!/usr/bin/env python3
"""Deterministically census D60 route mastery and cumulative assessments.

The receipt is evidence, not a production mutation.  It is computed only from
the frozen route controls, append-only backend JSONL, source unit locators, and
the independently reviewed CA01 source boundary.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_REL = "qa/ROUTE_MASTERY_CENSUS.json"
HANDOFF_REL = "00_control/CURRICULUM_ROUTE_AND_FOMBERG_HANDOFF.md"
CURSOR_REL = "00_control/CURSOR.json"
CA01_REL = (
    "source/id-ID/mastery/"
    "cumulative-assessment-001-foundations-coverings-homotopy.md"
)
CA01_REVIEW_REL = "qa/cumulative-assessment-001/INDEPENDENT_MATH_REVIEW.json"
SCRIPT_REL = "scripts/census-route-mastery.py"

EXPECTED_CA01_SHA256 = (
    "5888df0410ad7e8ccf50d8ea8092e43a42f6df94c242f7c09abe0616d972e6f8"
)

ROUTE_IDS = tuple(f"D60-R{number:02d}" for number in range(1, 15))
ASSESSMENT_IDS = tuple(f"D60-CA{number:02d}" for number in range(1, 4))

EXPECTED_ROUTE_COMPONENTS: dict[str, tuple[str, ...]] = {
    "D60-R01": ("o012-rbt-l01", "o012-rbt-l02"),
    "D60-R02": ("o012-rbt-l03", "o012-rbt-l04"),
    "D60-R03": ("o012-rbt-l05", "o012-rbt-l06"),
    "D60-R04": (
        "o012-rbt-l07",
        "o012-rbt-l08",
        "o012-rbt-l09",
        "o012-rbt-l10",
    ),
    "D60-R05": ("o012-rbt-l11", "o012-rbt-l12", "o012-rbt-l13"),
    "D60-R06": (
        "o012-rbt-l14",
        "o012-rbt-l15",
        "o012-rbt-l16",
        "o012-rbt-l17",
    ),
    "D60-R07": ("o012-rbt-l18", "o012-rbt-l19"),
    "D60-R08": ("o012-fom-u001",),
    "D60-R09": ("o012-fom-u002",),
    "D60-R10": ("o012-fom-u003",),
    "D60-R11": ("o012-fom-u004",),
    "D60-R12": ("o012-fom-u005", "o012-fom-u006", "o012-fom-u007"),
    "D60-R13": tuple(f"o012-rbt-l{number:02d}" for number in range(20, 28)),
    "D60-R14": ("o012-rbt-l28", "o012-rbt-l29", "o012-rbt-l30"),
}

EXPECTED_EDITION_MAPPING: dict[str, str] = {
    "D60-R01": "Roberts L1–L2, lines 136–584",
    "D60-R02": "Roberts L3–L4, lines 585–1131",
    "D60-R03": "Roberts L5–L6, lines 1132–1515",
    "D60-R04": "Roberts L7–L10, lines 1516–2272",
    "D60-R05": "Roberts L11–L13, lines 2273–3046",
    "D60-R06": "Roberts L14–L17, lines 3047–3481",
    "D60-R07": "Roberts L18–L19, lines 3482–3947",
    "D60-R08": "Fomberg §§1.1–1.2, lines 31–614",
    "D60-R09": "Fomberg §§1.3–1.4, lines 615–1290",
    "D60-R10": "Fomberg §§1.5–1.6, lines 1291–1922",
    "D60-R11": "Fomberg §§1.7–1.10, lines 1923–2846",
    "D60-R12": (
        "Fomberg §§1.12–1.13, lines 3123–4185; optional §1.11, "
        "lines 2847–3122"
    ),
    "D60-R13": "Roberts L20–L27, lines 3948–5923",
    "D60-R14": (
        "Roberts L28–L30, lines 5924–6368 plus original synthesis"
    ),
}

COMPONENT_TO_ROUTE = {
    component: route_id
    for route_id, components in EXPECTED_ROUTE_COMPONENTS.items()
    for component in components
}

ORDINARY_PER_ROUTE = 6
ORDINARY_TARGET = 84
ASSESSMENT_COUNT_TARGET = 3
ASSESSMENT_ITEMS_EACH = 8
ASSESSMENT_ITEM_TARGET = 24
TOTAL_TARGET = 108


class CensusError(RuntimeError):
    """Raised only for an operational failure that prevents a receipt."""


def read_bytes(relative_path: str) -> bytes:
    path = ROOT / relative_path
    try:
        return path.read_bytes()
    except OSError as exc:
        raise CensusError(f"cannot read {relative_path}: {exc}") from exc


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_identity(relative_path: str, data: bytes) -> dict[str, Any]:
    return {
        "path": relative_path,
        "bytes": len(data),
        "lf_count": data.count(b"\n"),
        "sha256": sha256_hex(data),
    }


def decode_utf8(relative_path: str, data: bytes) -> str:
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CensusError(f"{relative_path} is not valid UTF-8: {exc}") from exc


def parse_json(relative_path: str, data: bytes) -> Any:
    try:
        return json.loads(decode_utf8(relative_path, data))
    except json.JSONDecodeError as exc:
        raise CensusError(f"invalid JSON in {relative_path}: {exc}") from exc


def parse_jsonl(
    relative_path: str, data: bytes, validation_errors: list[str]
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    text = decode_utf8(relative_path, data)
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            validation_errors.append(f"{relative_path}:{line_number}: blank JSONL line")
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            validation_errors.append(
                f"{relative_path}:{line_number}: invalid JSON: {exc.msg}"
            )
            continue
        if not isinstance(value, dict):
            validation_errors.append(
                f"{relative_path}:{line_number}: record is not an object"
            )
            continue
        record_id = value.get("id")
        if not isinstance(record_id, str) or not record_id:
            validation_errors.append(
                f"{relative_path}:{line_number}: missing nonempty id"
            )
        elif record_id in seen_ids:
            validation_errors.append(
                f"{relative_path}:{line_number}: duplicate id {record_id}"
            )
        else:
            seen_ids.add(record_id)
        records.append(value)
    return records


def component_from_id(entity_id: str) -> str | None:
    roberts = re.search(r"unit:o012-rbt-l(\d{2})(?:-|$)", entity_id)
    if roberts:
        return f"o012-rbt-l{int(roberts.group(1)):02d}"
    fomberg = re.search(r"unit:o012-fom-u(\d{3})(?:-|$)", entity_id)
    if fomberg:
        return f"o012-fom-u{int(fomberg.group(1)):03d}"
    return None


def assessment_id_from_record(record: dict[str, Any]) -> str | None:
    explicit = record.get("assessment_id")
    if isinstance(explicit, str) and re.fullmatch(r"D60-CA\d{2}", explicit):
        return explicit
    entity_id = record.get("id")
    if not isinstance(entity_id, str):
        return None
    match = re.search(
        r"(?:^|[:-])(?:d60-)?ca(\d{2})(?:[:-]|$)", entity_id, re.IGNORECASE
    )
    if match:
        return f"D60-CA{int(match.group(1)):02d}"
    return None


def parse_and_validate_controls(
    handoff_data: bytes,
    cursor_data: bytes,
    validation_errors: list[str],
) -> tuple[dict[str, dict[str, str]], dict[str, Any]]:
    handoff_text = decode_utf8(HANDOFF_REL, handoff_data)
    parsed_routes: dict[str, dict[str, str]] = {}
    for line in handoff_text.splitlines():
        if not re.match(r"^\| D60-R\d{2} \|", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 3:
            validation_errors.append(f"malformed frozen route table line: {line}")
            continue
        route_id, required_material, edition_mapping = cells
        if route_id in parsed_routes:
            validation_errors.append(f"duplicate route table row {route_id}")
        parsed_routes[route_id] = {
            "required_material": required_material,
            "edition_mapping": edition_mapping,
        }

    if tuple(parsed_routes) != ROUTE_IDS:
        validation_errors.append(
            "frozen route table IDs/order differ: "
            f"expected {list(ROUTE_IDS)}, got {list(parsed_routes)}"
        )
    for route_id in ROUTE_IDS:
        actual = parsed_routes.get(route_id, {}).get("edition_mapping")
        expected = EXPECTED_EDITION_MAPPING[route_id]
        if actual != expected:
            validation_errors.append(
                f"{route_id} edition mapping differs: expected {expected!r}, got {actual!r}"
            )

    normalized = " ".join(handoff_text.split())
    requirement_fragment = (
        "at least six ordinary problems per route unit with hints and complete "
        "checked solutions (84), plus three cumulative assessments of eight "
        "items each (24): **108 ordinary solution-bearing items**"
    )
    if requirement_fragment not in normalized:
        validation_errors.append("frozen 84+24=108 mastery requirement not found verbatim")

    cursor = parse_json(CURSOR_REL, cursor_data)
    if not isinstance(cursor, dict):
        validation_errors.append("CURSOR.json root is not an object")
        cursor = {}
    if cursor.get("role_id") != "O012" or cursor.get("course_id") != "D60":
        validation_errors.append("CURSOR.json role/course identity is not O012/D60")
    next_action = cursor.get("next_action")
    if not isinstance(next_action, str) or "108-item mastery layer" not in next_action:
        validation_errors.append("CURSOR.json no longer names the 108-item mastery layer")
    return parsed_routes, cursor


def route_for_component_record(
    record: dict[str, Any],
    validation_errors: list[str],
    context: str,
) -> tuple[str | None, str | None, bool]:
    entity_id = record.get("id")
    if not isinstance(entity_id, str):
        validation_errors.append(f"{context}: record lacks string id")
        return None, None, False
    component = component_from_id(entity_id)
    if component is None or component not in COMPONENT_TO_ROUTE:
        validation_errors.append(f"{context}: cannot map component for {entity_id}")
        return None, component, False
    expected_route = COMPONENT_TO_ROUTE[component]
    has_direct = "course_route_unit_id" in record and bool(
        record.get("course_route_unit_id")
    )
    direct_route = record.get("course_route_unit_id")
    if has_direct and direct_route != expected_route:
        validation_errors.append(
            f"{context}: {entity_id} records {direct_route}, expected {expected_route}"
        )
    return expected_route, component, has_direct


def validate_locator(
    record: dict[str, Any], validation_errors: list[str], context: str
) -> None:
    entity_id = record.get("id", "<missing-id>")
    locator = record.get("target_locator")
    if not isinstance(locator, dict):
        validation_errors.append(f"{context}: {entity_id} lacks target_locator")
        return
    source_path = locator.get("path")
    if not isinstance(source_path, str) or not source_path.startswith("source/id-ID/"):
        validation_errors.append(
            f"{context}: {entity_id} has non-id-ID source locator {source_path!r}"
        )
    elif not (ROOT / source_path).is_file():
        validation_errors.append(
            f"{context}: {entity_id} source locator does not exist: {source_path}"
        )
    line_start = locator.get("line_start")
    line_end = locator.get("line_end")
    if (
        not isinstance(line_start, int)
        or not isinstance(line_end, int)
        or line_start < 1
        or line_end < line_start
    ):
        validation_errors.append(
            f"{context}: {entity_id} has invalid line locator {line_start}-{line_end}"
        )


def validate_ca01_source(
    ca01_data: bytes,
    review_data: bytes,
    validation_errors: list[str],
) -> dict[str, Any]:
    text = decode_utf8(CA01_REL, ca01_data)
    identity = file_identity(CA01_REL, ca01_data)
    hash_matches_review = identity["sha256"] == EXPECTED_CA01_SHA256
    if not hash_matches_review:
        validation_errors.append(
            "CA01 source hash differs from the independently reviewed boundary: "
            f"expected {EXPECTED_CA01_SHA256}, got {identity['sha256']}"
        )

    frontmatter_match = re.search(
        r"^assessment_id:\s*(D60-CA\d{2})\s*$", text, re.MULTILINE
    )
    frontmatter_assessment_id = (
        frontmatter_match.group(1) if frontmatter_match else None
    )
    if frontmatter_assessment_id != "D60-CA01":
        validation_errors.append("CA01 frontmatter assessment_id is not D60-CA01")

    block_pattern = re.compile(
        r'^::: \{\.(exercise|hint|solution) '
        r'#(o012-d60-ca01-(?:ex|hint|sol)-(\d{3}))([^}]*)\}\s*$',
        re.MULTILINE,
    )
    blocks: dict[str, list[dict[str, str]]] = {
        "exercise": [],
        "hint": [],
        "solution": [],
    }
    for match in block_pattern.finditer(text):
        block_kind, block_id, suffix, attributes = match.groups()
        blocks[block_kind].append(
            {"id": block_id, "suffix": suffix, "attributes": attributes.strip()}
        )

    expected_suffixes = [f"{number:03d}" for number in range(1, 9)]
    for block_kind, values in blocks.items():
        suffixes = sorted(value["suffix"] for value in values)
        if suffixes != expected_suffixes:
            validation_errors.append(
                f"CA01 {block_kind} suffixes differ: {suffixes}"
            )
        for value in values:
            if 'data-assessment-id="D60-CA01"' not in value["attributes"]:
                validation_errors.append(
                    f"CA01 block {value['id']} lacks data-assessment-id D60-CA01"
                )

    review = parse_json(CA01_REVIEW_REL, review_data)
    if not isinstance(review, dict):
        validation_errors.append("CA01 independent math review root is not an object")
        review = {}
    severity = review.get("severity_census")
    severity_zero = severity == {"P1": 0, "P2": 0, "P3": 0}
    review_bound = (
        review.get("status") == "PASS"
        and review.get("reader_path") == CA01_REL
        and review.get("reader_sha256") == identity["sha256"]
        and severity_zero
        and review.get("unresolved_findings") == []
    )
    if not review_bound:
        validation_errors.append(
            "CA01 independent math review is not a zero-finding PASS bound to source"
        )

    block_counts = {kind: len(values) for kind, values in blocks.items()}
    structure_complete = (
        frontmatter_assessment_id == "D60-CA01"
        and block_counts == {"exercise": 8, "hint": 8, "solution": 8}
        and all(
            sorted(value["suffix"] for value in blocks[kind]) == expected_suffixes
            for kind in blocks
        )
    )
    admissible_complete = structure_complete and hash_matches_review and review_bound
    return {
        "assessment_id": "D60-CA01",
        "identity": identity,
        "expected_reviewed_sha256": EXPECTED_CA01_SHA256,
        "hash_matches_reviewed_boundary": hash_matches_review,
        "block_counts": block_counts,
        "item_suffixes": expected_suffixes if structure_complete else None,
        "structure_complete": structure_complete,
        "independent_math_review": {
            "identity": file_identity(CA01_REVIEW_REL, review_data),
            "status": review.get("status"),
            "bound_reader_sha256": review.get("reader_sha256"),
            "severity_census": severity,
            "bound_to_current_source": review_bound,
        },
        "admissible_complete": admissible_complete,
    }


def main() -> int:
    validation_errors: list[str] = []

    handoff_data = read_bytes(HANDOFF_REL)
    cursor_data = read_bytes(CURSOR_REL)
    ca01_data = read_bytes(CA01_REL)
    ca01_review_data = read_bytes(CA01_REVIEW_REL)
    script_data = read_bytes(SCRIPT_REL)

    parsed_route_table, cursor = parse_and_validate_controls(
        handoff_data, cursor_data, validation_errors
    )

    backend_paths = sorted((ROOT / "backend").glob("*.jsonl"), key=lambda p: p.name)
    if not backend_paths:
        raise CensusError("no backend/*.jsonl files found")
    backend_bytes = {path.name: path.read_bytes() for path in backend_paths}
    if "units.jsonl" not in backend_bytes or "relations.jsonl" not in backend_bytes:
        raise CensusError("backend units.jsonl or relations.jsonl is missing")

    backend_identities: dict[str, dict[str, Any]] = {}
    for name, data in backend_bytes.items():
        relative_path = f"backend/{name}"
        identity = file_identity(relative_path, data)
        identity["record_count"] = sum(
            1 for line in decode_utf8(relative_path, data).splitlines() if line.strip()
        )
        backend_identities[name] = identity

    units = parse_jsonl("backend/units.jsonl", backend_bytes["units.jsonl"], validation_errors)
    relations = parse_jsonl(
        "backend/relations.jsonl",
        backend_bytes["relations.jsonl"],
        validation_errors,
    )
    unit_by_id = {
        unit["id"]: unit
        for unit in units
        if isinstance(unit.get("id"), str) and unit.get("id")
    }
    active_unit_by_id = {
        unit_id: unit
        for unit_id, unit in unit_by_id.items()
        if unit.get("status") == "active"
    }
    active_relations = [
        relation for relation in relations if relation.get("status") == "active"
    ]

    hint_relations = [
        relation
        for relation in active_relations
        if relation.get("relation_type") == "hints"
    ]
    solve_relations = [
        relation
        for relation in active_relations
        if relation.get("relation_type") == "solves"
    ]

    hints_by_exercise: dict[str, list[dict[str, Any]]] = defaultdict(list)
    hint_edges_by_hint: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for relation in hint_relations:
        hint_id = relation.get("from_id")
        exercise_id = relation.get("to_id")
        hint = active_unit_by_id.get(hint_id)
        exercise = active_unit_by_id.get(exercise_id)
        if hint is None or exercise is None:
            validation_errors.append(
                f"hint relation {relation.get('id')} has missing/inactive endpoint"
            )
            continue
        if hint.get("unit_kind") != "hint" or exercise.get("unit_kind") != "exercise":
            validation_errors.append(
                f"hint relation {relation.get('id')} has wrong endpoint kinds"
            )
            continue
        hints_by_exercise[exercise_id].append(relation)
        hint_edges_by_hint[hint_id].append(relation)

    for exercise_id, edges in sorted(hints_by_exercise.items()):
        if len(edges) != 1:
            validation_errors.append(
                f"exercise {exercise_id} has {len(edges)} active hint relations"
            )
    for hint_id, edges in sorted(hint_edges_by_hint.items()):
        if len(edges) != 1:
            validation_errors.append(
                f"hint {hint_id} participates in {len(edges)} active hint relations"
            )
    active_hint_ids = {
        unit_id
        for unit_id, unit in active_unit_by_id.items()
        if unit.get("unit_kind") == "hint"
    }
    related_hint_ids = set(hint_edges_by_hint)
    if active_hint_ids != related_hint_ids:
        validation_errors.append(
            "active hint units and active hint-relation sources differ: "
            f"orphan={sorted(active_hint_ids - related_hint_ids)}, "
            f"missing_units={sorted(related_hint_ids - active_hint_ids)}"
        )

    solutions_by_exercise: dict[str, list[dict[str, Any]]] = defaultdict(list)
    solution_edges_by_solution: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for relation in solve_relations:
        solution_id = relation.get("from_id")
        exercise_id = relation.get("to_id")
        solution = active_unit_by_id.get(solution_id)
        exercise = active_unit_by_id.get(exercise_id)
        if solution is None or exercise is None:
            validation_errors.append(
                f"solve relation {relation.get('id')} has missing/inactive endpoint"
            )
            continue
        if solution.get("unit_kind") != "solution" or exercise.get("unit_kind") != "exercise":
            validation_errors.append(
                f"solve relation {relation.get('id')} has wrong endpoint kinds"
            )
            continue
        solutions_by_exercise[exercise_id].append(relation)
        solution_edges_by_solution[solution_id].append(relation)

    triples: list[dict[str, Any]] = []
    triple_solution_ids: list[str] = []
    inferred_route_exercise_ids: list[str] = []
    inferred_route_member_ids: list[str] = []
    for exercise_id in sorted(hints_by_exercise):
        hint_edges = hints_by_exercise[exercise_id]
        solution_edges = solutions_by_exercise.get(exercise_id, [])
        if len(hint_edges) != 1 or len(solution_edges) != 1:
            validation_errors.append(
                f"hinted exercise {exercise_id} has {len(hint_edges)} hints and "
                f"{len(solution_edges)} solutions; expected one each"
            )
            continue
        hint_id = hint_edges[0]["from_id"]
        solution_id = solution_edges[0]["from_id"]
        exercise = active_unit_by_id[exercise_id]
        hint = active_unit_by_id[hint_id]
        solution = active_unit_by_id[solution_id]
        triple_solution_ids.append(solution_id)

        assessment_ids = {
            value
            for value in (
                assessment_id_from_record(exercise),
                assessment_id_from_record(hint),
                assessment_id_from_record(solution),
            )
            if value is not None
        }
        if len(assessment_ids) > 1:
            validation_errors.append(
                f"triple {exercise_id} has inconsistent assessment IDs {assessment_ids}"
            )
        assessment_id = next(iter(assessment_ids), None)

        route_id: str | None = None
        component: str | None = None
        route_metadata = "assessment"
        if assessment_id is None:
            member_routes: set[str] = set()
            member_components: set[str] = set()
            for member_kind, member in (
                ("exercise", exercise),
                ("hint", hint),
                ("solution", solution),
            ):
                member_route, member_component, has_direct = route_for_component_record(
                    member,
                    validation_errors,
                    f"ordinary triple {exercise_id} {member_kind}",
                )
                if member_route:
                    member_routes.add(member_route)
                if member_component:
                    member_components.add(member_component)
                if not has_direct:
                    inferred_route_member_ids.append(member["id"])
                    if member_kind == "exercise":
                        inferred_route_exercise_ids.append(member["id"])
            if len(member_routes) != 1 or len(member_components) != 1:
                validation_errors.append(
                    f"ordinary triple {exercise_id} crosses routes/components: "
                    f"routes={member_routes}, components={member_components}"
                )
            route_id = next(iter(member_routes), None)
            component = next(iter(member_components), None)
            route_metadata = (
                "direct" if "course_route_unit_id" in exercise else "inferred_from_control"
            )

        for member_kind, member in (
            ("exercise", exercise),
            ("hint", hint),
            ("solution", solution),
        ):
            validate_locator(
                member, validation_errors, f"triple {exercise_id} {member_kind}"
            )

        triples.append(
            {
                "exercise_id": exercise_id,
                "hint_id": hint_id,
                "solution_id": solution_id,
                "assessment_id": assessment_id,
                "course_route_unit_id": route_id,
                "component_id": component,
                "route_metadata": route_metadata,
                "translation_states": {
                    "exercise": exercise.get("translation_state"),
                    "hint": hint.get("translation_state"),
                    "solution": solution.get("translation_state"),
                },
                "source_path": exercise.get("target_locator", {}).get("path"),
            }
        )

    duplicate_triple_solutions = sorted(
        solution_id
        for solution_id, count in Counter(triple_solution_ids).items()
        if count != 1
    )
    if duplicate_triple_solutions:
        validation_errors.append(
            "solutions are not one-to-one across hinted exercises: "
            f"{duplicate_triple_solutions}"
        )

    ordinary_triples = [triple for triple in triples if triple["assessment_id"] is None]
    backend_assessment_triples = [
        triple for triple in triples if triple["assessment_id"] is not None
    ]
    ordinary_triple_exercise_ids = {
        triple["exercise_id"] for triple in ordinary_triples
    }

    ordinary_pair_targets_by_route: dict[str, set[str]] = {
        route_id: set() for route_id in ROUTE_IDS
    }
    ordinary_pair_edges_by_route: Counter[str] = Counter()
    for exercise_id, edges in sorted(solutions_by_exercise.items()):
        exercise = active_unit_by_id[exercise_id]
        if assessment_id_from_record(exercise) is not None:
            continue
        route_id, _, _ = route_for_component_record(
            exercise, validation_errors, f"solution-bearing exercise {exercise_id}"
        )
        if route_id is None:
            continue
        ordinary_pair_targets_by_route[route_id].add(exercise_id)
        ordinary_pair_edges_by_route[route_id] += len(edges)

    triples_by_route: dict[str, list[dict[str, Any]]] = {
        route_id: [] for route_id in ROUTE_IDS
    }
    for triple in ordinary_triples:
        route_id = triple["course_route_unit_id"]
        if route_id not in triples_by_route:
            validation_errors.append(
                f"ordinary triple {triple['exercise_id']} has invalid route {route_id}"
            )
            continue
        triples_by_route[route_id].append(triple)
    for route_id in ROUTE_IDS:
        triples_by_route[route_id].sort(key=lambda item: item["exercise_id"])

    route_detail: dict[str, dict[str, Any]] = {}
    ordinary_deficits: list[dict[str, Any]] = []
    for route_id in ROUTE_IDS:
        route_triples = triples_by_route[route_id]
        pair_ids = sorted(ordinary_pair_targets_by_route[route_id])
        reusable_ids = sorted(set(pair_ids) - ordinary_triple_exercise_ids)
        triple_count = len(route_triples)
        gap = max(ORDINARY_PER_ROUTE - triple_count, 0)
        selected_candidates = reusable_ids[:gap]
        new_problem_solution_gap = max(gap - len(selected_candidates), 0)
        route_detail[route_id] = {
            "frozen_components": list(EXPECTED_ROUTE_COMPONENTS[route_id]),
            "graph_complete_triples": triple_count,
            "capped_quota_credit": min(triple_count, ORDINARY_PER_ROUTE),
            "quota_gap": gap,
            "triple_exercise_ids": [item["exercise_id"] for item in route_triples],
            "solution_bearing_exercises": len(pair_ids),
            "solution_pair_edges": ordinary_pair_edges_by_route[route_id],
            "solution_bearing_exercise_ids": pair_ids,
            "reusable_pairs_without_hint": len(reusable_ids),
            "reusable_exercise_ids_without_hint": reusable_ids,
        }
        if gap:
            ordinary_deficits.append(
                {
                    "course_route_unit_id": route_id,
                    "missing_graph_complete_triples": gap,
                    "deterministic_candidate_hint_targets": selected_candidates,
                    "new_exercises_or_solutions_required": new_problem_solution_gap,
                    "required_action": (
                        "add separately modeled active hint units and one-to-one "
                        "hints relations to selected existing full-solution pairs"
                    ),
                }
            )

    ordinary_total = len(ordinary_triples)
    ordinary_capped_credit = sum(
        min(len(triples_by_route[route_id]), ORDINARY_PER_ROUTE)
        for route_id in ROUTE_IDS
    )
    ordinary_gap = ORDINARY_TARGET - ordinary_capped_credit

    detected_backend_assessment_ids = sorted(
        {
            assessment_id
            for unit in active_unit_by_id.values()
            if (assessment_id := assessment_id_from_record(unit)) is not None
        }
    )
    assessment_triples_by_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for triple in backend_assessment_triples:
        assessment_triples_by_id[triple["assessment_id"]].append(triple)
    backend_assessment_detail: dict[str, dict[str, Any]] = {}
    for assessment_id in sorted(
        set(detected_backend_assessment_ids) | set(assessment_triples_by_id)
    ):
        item_triples = sorted(
            assessment_triples_by_id.get(assessment_id, []),
            key=lambda item: item["exercise_id"],
        )
        backend_assessment_detail[assessment_id] = {
            "graph_complete_items": len(item_triples),
            "complete_eight_item_assessment": len(item_triples) == ASSESSMENT_ITEMS_EACH,
            "exercise_ids": [item["exercise_id"] for item in item_triples],
        }
    complete_backend_assessment_ids = sorted(
        assessment_id
        for assessment_id, detail in backend_assessment_detail.items()
        if detail["complete_eight_item_assessment"]
    )
    backend_assessment_credit = (
        len(complete_backend_assessment_ids) * ASSESSMENT_ITEMS_EACH
    )

    ca01_status = validate_ca01_source(
        ca01_data, ca01_review_data, validation_errors
    )
    source_complete_assessment_ids = set(complete_backend_assessment_ids)
    if ca01_status["admissible_complete"]:
        source_complete_assessment_ids.add("D60-CA01")
    source_complete_assessment_ids_sorted = sorted(source_complete_assessment_ids)
    source_assessment_credit = (
        len(source_complete_assessment_ids_sorted) * ASSESSMENT_ITEMS_EACH
    )
    missing_source_assessment_ids = sorted(
        set(ASSESSMENT_IDS) - source_complete_assessment_ids
    )

    route_mapping_receipt = {
        route_id: {
            "required_material": parsed_route_table.get(route_id, {}).get(
                "required_material"
            ),
            "edition_mapping": parsed_route_table.get(route_id, {}).get(
                "edition_mapping"
            ),
            "components": list(EXPECTED_ROUTE_COMPONENTS[route_id]),
        }
        for route_id in ROUTE_IDS
    }

    backend_slot_coverage = ordinary_capped_credit + backend_assessment_credit
    source_slot_coverage = ordinary_capped_credit + source_assessment_credit
    receipt: dict[str, Any] = {
        "schema_version": "1.0",
        "status": "PASS" if not validation_errors else "FAIL",
        "course_id": "D60",
        "role_id": "O012",
        "scope": {
            "method": (
                "An ordinary item counts only when one active exercise is the "
                "target of exactly one active hints edge from an active hint and "
                "exactly one active solves edge from an active full solution. "
                "Assessment triples are classified separately. Route credit is "
                "capped at six per frozen route unit."
            ),
            "output_path": OUTPUT_REL,
            "no_publication_or_backend_mutation": True,
        },
        "requirements": {
            "ordinary_per_route": ORDINARY_PER_ROUTE,
            "route_count": len(ROUTE_IDS),
            "ordinary_items": ORDINARY_TARGET,
            "cumulative_assessments": ASSESSMENT_COUNT_TARGET,
            "items_per_cumulative_assessment": ASSESSMENT_ITEMS_EACH,
            "cumulative_items": ASSESSMENT_ITEM_TARGET,
            "total_solution_bearing_items": TOTAL_TARGET,
        },
        "inputs": {
            "script": file_identity(SCRIPT_REL, script_data),
            "controls": {
                "handoff": file_identity(HANDOFF_REL, handoff_data),
                "cursor": file_identity(CURSOR_REL, cursor_data),
                "cursor_next_action": cursor.get("next_action"),
            },
            "backend_jsonl": backend_identities,
        },
        "frozen_route_mapping": route_mapping_receipt,
        "graph_validation": {
            "active_hint_units": len(active_hint_ids),
            "active_hint_relations": len(hint_relations),
            "active_solve_relations": len(solve_relations),
            "graph_complete_triples_all_classes": len(triples),
            "duplicate_or_reused_triple_solution_ids": duplicate_triple_solutions,
            "ordinary_exercises_with_inferred_route": len(
                set(inferred_route_exercise_ids)
            ),
            "ordinary_exercise_ids_with_inferred_route": sorted(
                set(inferred_route_exercise_ids)
            ),
            "ordinary_triple_member_records_with_inferred_route": len(
                set(inferred_route_member_ids)
            ),
            "validation_error_count": len(validation_errors),
            "validation_errors": sorted(validation_errors),
        },
        "ordinary_mastery": {
            "graph_complete_triple_count": ordinary_total,
            "triples": ordinary_triples,
            "route_detail": route_detail,
            "quota": {
                "raw_triples": ordinary_total,
                "capped_route_credit": ordinary_capped_credit,
                "required": ORDINARY_TARGET,
                "gap": ordinary_gap,
                "met": ordinary_gap == 0,
            },
        },
        "assessments": {
            "backend": {
                "detected_assessment_ids": detected_backend_assessment_ids,
                "detail": backend_assessment_detail,
                "complete_assessment_ids": complete_backend_assessment_ids,
                "complete_assessment_count": len(complete_backend_assessment_ids),
                "credited_items": backend_assessment_credit,
                "required_items": ASSESSMENT_ITEM_TARGET,
                "item_gap": ASSESSMENT_ITEM_TARGET - backend_assessment_credit,
            },
            "source_ca01": ca01_status,
            "source_plus_backend": {
                "complete_assessment_ids": source_complete_assessment_ids_sorted,
                "complete_assessment_count": len(source_complete_assessment_ids_sorted),
                "credited_items": source_assessment_credit,
                "required_items": ASSESSMENT_ITEM_TARGET,
                "item_gap": ASSESSMENT_ITEM_TARGET - source_assessment_credit,
                "missing_assessment_ids": missing_source_assessment_ids,
            },
        },
        "compliance": {
            "backend_admitted": {
                "ordinary_route_slots_covered": ordinary_capped_credit,
                "assessment_slots_covered": backend_assessment_credit,
                "total_slots_covered": backend_slot_coverage,
                "required": TOTAL_TARGET,
                "gap": TOTAL_TARGET - backend_slot_coverage,
                "met": backend_slot_coverage == TOTAL_TARGET,
            },
            "source_including_reviewed_ca01": {
                "ordinary_route_slots_covered": ordinary_capped_credit,
                "assessment_slots_covered": source_assessment_credit,
                "total_slots_covered": source_slot_coverage,
                "required": TOTAL_TARGET,
                "gap": TOTAL_TARGET - source_slot_coverage,
                "met": source_slot_coverage == TOTAL_TARGET,
            },
            "raw_inventory_does_not_override_required_distribution": True,
        },
        "next_deficits": {
            "ordinary_routes": ordinary_deficits,
            "ordinary_missing_triples": ordinary_gap,
            "source_assessments_to_create": missing_source_assessment_ids,
            "source_assessment_items_to_create": (
                ASSESSMENT_ITEM_TARGET - source_assessment_credit
            ),
            "source_complete_but_not_backend_admitted": sorted(
                source_complete_assessment_ids - set(complete_backend_assessment_ids)
            ),
            "backend_assessment_items_not_yet_admitted": (
                ASSESSMENT_ITEM_TARGET - backend_assessment_credit
            ),
            "backend_route_metadata": {
                "ordinary_triple_exercises_requiring_explicit_route_backfill": sorted(
                    set(inferred_route_exercise_ids)
                ),
                "ordinary_triple_member_records_requiring_explicit_route_backfill": sorted(
                    set(inferred_route_member_ids)
                ),
            },
        },
    }

    output_path = ROOT / OUTPUT_REL
    if not output_path.parent.is_dir():
        raise CensusError(f"output directory does not exist: {output_path.parent}")
    output_bytes = (
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    output_path.write_bytes(output_bytes)
    print(
        json.dumps(
            {
                "status": receipt["status"],
                "path": OUTPUT_REL,
                "bytes": len(output_bytes),
                "sha256": sha256_hex(output_bytes),
                "ordinary_triples": ordinary_total,
                "ordinary_capped_credit": ordinary_capped_credit,
                "backend_assessment_items": backend_assessment_credit,
                "source_assessment_items": source_assessment_credit,
                "validation_errors": len(validation_errors),
            },
            sort_keys=True,
        )
    )
    return 0 if not validation_errors else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CensusError as exc:
        print(f"census-route-mastery: ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
