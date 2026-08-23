#!/usr/bin/env python3
"""Independent structural validator for the O012 Units 001--019 backend.

This imports only the generic, offline checks from the historical validator
and widens its frozen source set to the current contiguous Roberts boundary.
It intentionally does not run the old 001--013-only boundary assertions.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path


LANE = Path(__file__).resolve().parents[1]
LEGACY_PATH = LANE / "scripts/validate-backend.py"
SOURCE_SPECS = {
    "source/id-ID/reader-unit-001.md": (225, "dccc7b727695d26d0b425c0eae22db1697cea93e295391fa7685fbca2d011dc7"),
    **{
        f"source/id-ID/units/unit-{n:03d}-lecture-{n:03d}.md": spec
        for n, spec in {
            2: (674, "9aa5063c167cc0b2bc8a5edbc81cb36995606d5073a1afe22db608609ad29377"),
            3: (618, "f757bc58ea6f0d0dbe37ebdb2e44da7d3814b32052d8e23a39331d66d1f025b2"),
            4: (632, "35aa8adfec6f7652f9a9f21f2c6b6656347309f866689a0939d6f0c517974ea3"),
            5: (663, "9d25dc7cd89c0c9f69841850b03489e742e8dc50c2e68ca405aff593ec128f90"),
            6: (893, "2276a34177100bc14e3e9f96461f6a7ab3bf27a25f652af4cc2d27493f420c8e"),
            7: (749, "f93659dd290272ad3d526b74565f7bdc7316c366c09f1efaac599abde4cbc59d"),
            8: (930, "4b5c579a1891a99ddff89c458f9d653ec03973e0aaa32839c87be5896ab653a8"),
            9: (939, "c6076a71d38ab54553a0bf5ed42289063044ebcbeb29689df220081e5621a8a1"),
            10: (934, "ef76aedb378cb8a3d18a20f672082ee976561a877270082968e7df0a1514a8d5"),
            11: (959, "7acb205dd9f760631f7548208d77470e22cd208849439e2ad2a8eb4b2465b0f8"),
            12: (1024, "b7ba7cad3d12605628693d57d50a41e06f40a6b7da1109752fe05d870b4b28f0"),
            13: (1306, "f3827dc052a70930ad31cc6f9b1a745bf8a17bac31b4f9249cd178b06ac302b6"),
            14: (947, "da6f18b455d76adafd8b9b648ed7c277958eca95c0b7d76a8bd9895d79ec6677"),
            15: (835, "e9ab0565ae460236a69c77389b76d32405873156fc451be9cf95c3749e7fe9d1"),
            16: (984, "31dfc4c3647f7d6a1d398d2123efe1faa82348428df0180eee2a2358572f9054"),
            17: (952, "47576d7c26a436ba915c276b692e2bc0ead6fae038295fee3a82a50426ed9a96"),
            18: (1663, "9d0564f6a074441332e42755d46d9a0e858189a5ff4d8b5be52b1def12532598"),
            19: (1865, "ba34773d63e4dc70fccdf4fa19fbdc8a397062a4bc359978f3261a70ff64f98c"),
        }.items()
    },
}


def load_legacy():
    spec = importlib.util.spec_from_file_location("legacy_backend_validator", LEGACY_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def bundle_sha256(records_by_file: dict[str, bytes]) -> str:
    digest = hashlib.sha256()
    for name in sorted(records_by_file):
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(records_by_file[name])
    return digest.hexdigest()


def validate_hierarchy_allowing_open_source_questions(legacy, records, by_id) -> None:
    """Run the generic hierarchy checks while keeping source questions open.

    Units 014 and 015 preserve two source ``question`` blocks without claiming
    an answer artifact.  The translated edition may close them later; that is
    not a referential defect at this boundary.  Exercise/solution closure is
    still mandatory, and any existing answer relation must be well-typed.
    """
    units = [record for record in records if record["entity_type"] == "unit"]
    roots = [record for record in units if record["unit_kind"] == "reader_unit"]
    if len(roots) != len(SOURCE_SPECS):
        raise legacy.ValidationError(f"expected {len(SOURCE_SPECS)} reader roots, found {len(roots)}")
    unit_by_id = {record["id"]: record for record in units}
    sibling_orders = {}
    for unit in units:
        path = unit["path"]
        if not isinstance(path, list) or not path or path[-1] != unit["id"]:
            raise legacy.ValidationError(f"invalid path: {unit['id']}")
        if any(item not in unit_by_id for item in path):
            raise legacy.ValidationError(f"path contains non-unit: {unit['id']}")
        parent = unit["parent_id"]
        if parent in unit_by_id:
            if path[:-1] != unit_by_id[parent]["path"]:
                raise legacy.ValidationError(f"path does not extend parent: {unit['id']}")
        elif len(path) != 1 or unit["unit_kind"] != "reader_unit":
            raise legacy.ValidationError(f"non-root has non-unit parent: {unit['id']}")
        sibling_orders.setdefault(parent, []).append(unit["order"])
        root = unit_by_id[path[0]]
        if root["unit_kind"] != "reader_unit" or unit["target_locator"]["path"] != root["target_locator"]["path"]:
            raise legacy.ValidationError(f"root/source mismatch: {unit['id']}")
    for parent, orders in sibling_orders.items():
        if len(orders) != len(set(orders)):
            raise legacy.ValidationError(f"duplicate child order values: {parent}")
    relations = [record for record in records if record["entity_type"] == "relation"]
    solves = [record for record in relations if record["relation_type"] == "solves"]
    exercises = {record["id"] for record in units if record["unit_kind"] == "exercise"}
    solutions = {record["id"] for record in units if record["unit_kind"] == "solution"}
    exercise_links = {exercise: 0 for exercise in exercises}
    solution_links = {solution: 0 for solution in solutions}
    for relation in solves:
        if relation["from_id"] not in solutions or relation["to_id"] not in exercises:
            raise legacy.ValidationError(f"ill-typed solves relation: {relation['id']}")
        exercise_links[relation["to_id"]] += 1
        solution_links[relation["from_id"]] += 1
    if any(count != 1 for count in exercise_links.values()) or set(exercise_links) != exercises:
        raise legacy.ValidationError("every exercise must have exactly one solves relation")
    if any(count < 1 for count in solution_links.values()) or set(solution_links) != solutions:
        raise legacy.ValidationError("every solution must solve at least one exercise")
    answers = [record for record in relations if record["relation_type"] == "answers"]
    for relation in answers:
        if by_id[relation["from_id"]].get("unit_kind") != "answer" or by_id[relation["to_id"]].get("unit_kind") != "question":
            raise legacy.ValidationError(f"ill-typed answers relation: {relation['id']}")


def main() -> int:
    legacy = load_legacy()
    legacy.SOURCE_FILES = {path: sha for path, (_, sha) in SOURCE_SPECS.items()}
    legacy.SOURCE_LINE_COUNTS = {path: lines for path, (lines, _) in SOURCE_SPECS.items()}
    legacy.EXPECTED_SOURCE_ID_COUNT = 710
    records, owner_file = legacy.load_records(LANE / "backend")
    by_id = {record["id"]: record for record in records}
    if len(by_id) != len(records):
        raise legacy.ValidationError("duplicate backend IDs")
    legacy.validate_shapes(records)
    legacy.validate_references(records, by_id)
    legacy.validate_files_and_spans(records, by_id, LANE)
    validate_hierarchy_allowing_open_source_questions(legacy, records, by_id)
    edition = by_id["edition:roberts-at-2019-b947ad2"]
    if edition["source_line_start"] != 134 or edition["source_line_end"] != 3947:
        raise legacy.ValidationError("edition boundary is not Notes.tex:134-3947")
    expected_roots = [f"unit:o012-rbt-u{n:03d}" for n in range(1, 20)]
    if edition.get("local_derivative_unit_ids") != expected_roots:
        raise legacy.ValidationError("edition root list is not the exact Units 001-019 sequence")
    if by_id["rights:o012-units-001-019-composite-cc-by-4.0"]["component_scope"] != expected_roots:
        raise legacy.ValidationError("cumulative rights component scope mismatch")
    for n in range(14, 20):
        unit = by_id[f"unit:o012-rbt-u{n:03d}"]
        if unit["target_locator"]["line_start"] != 1 or unit["target_locator"]["line_end"] != SOURCE_SPECS[f"source/id-ID/units/unit-{n:03d}-lecture-{n:03d}.md"][0]:
            raise legacy.ValidationError(f"Unit {n:03d} root span mismatch")
    adverse = [
        record for record in records
        if record["entity_type"] == "correction"
        and record.get("adverse_ledger_id", "").startswith("O012-ADV-")
        and 14 <= int(record["adverse_ledger_id"][-4:]) <= 278
    ]
    new_adverse = [record for record in adverse if record.get("unit_id", "") in {f"unit:o012-rbt-u{n:03d}" for n in range(14, 20)}]
    if len(new_adverse) != 91:
        raise legacy.ValidationError("new adverse-ledger closure is incomplete")
    backend_files = {path.name: path.read_bytes() for path in (LANE / "backend").glob("*.jsonl")}
    print(json.dumps({
        "status": "PASS",
        "records": len(records),
        "jsonl_files": len(backend_files),
        "source_files": len(SOURCE_SPECS),
        "stable_source_ids": 710,
        "units_014_019_corrections": len(new_adverse),
        "backend_bytes": sum(len(raw) for raw in backend_files.values()),
        "backend_bundle_sha256": bundle_sha256(backend_files),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"backend 001-019 validation: FAIL: {exc}")
        raise
