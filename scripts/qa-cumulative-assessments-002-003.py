#!/usr/bin/env python3
"""Fail-closed structural and independent-review QA for D60-CA02/CA03."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


LANE = Path(__file__).resolve().parents[1]
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
OUTPUT = LANE / "qa/CUMULATIVE_ASSESSMENTS_002_003_QA.json"
CONFIG: dict[str, dict[str, Any]] = {
    "D60-CA02": {
        "token": "ca02",
        "edition_unit_id": "O012-ORIG-CA02",
        "reader": LANE / "source/id-ID/mastery/cumulative-assessment-002-homology-excision-cellular.md",
        "math_review": LANE / "qa/cumulative-assessment-002/INDEPENDENT_MATH_REVIEW.json",
        "language_review": LANE / "qa/cumulative-assessment-002/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json",
        "allowed_primary_routes": {"D60-R08", "D60-R09", "D60-R10", "D60-R11", "D60-R12"},
        "required_primary_routes": {"D60-R08", "D60-R09", "D60-R10", "D60-R11", "D60-R12"},
    },
    "D60-CA03": {
        "token": "ca03",
        "edition_unit_id": "O012-ORIG-CA03",
        "reader": LANE / "source/id-ID/mastery/cumulative-assessment-003-cohomology-degree-synthesis.md",
        "math_review": LANE / "qa/cumulative-assessment-003/INDEPENDENT_MATH_REVIEW.json",
        "language_review": LANE / "qa/cumulative-assessment-003/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json",
        "allowed_primary_routes": {"D60-R13", "D60-R14"},
        "required_primary_routes": {"D60-R13", "D60-R14"},
    },
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    return {
        "path": path.relative_to(LANE).as_posix(),
        "bytes": len(raw),
        "lf_lines": raw.count(b"\n"),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def load_review(path: Path, expected_kind: str, reader_sha256: str, assessment_id: str) -> dict[str, Any]:
    require(path.is_file(), f"missing independent review: {path.relative_to(LANE)}")
    review = json.loads(path.read_text(encoding="utf-8"))
    require(review.get("review_kind") == expected_kind, f"wrong review kind: {path.name}")
    require(str(review.get("status", "")).startswith("PASS"), f"review is not PASS: {path.name}")
    require(review.get("independent_from_production") is True, f"review is not independent: {path.name}")
    require(review.get("reader_sha256") == reader_sha256, f"review binds stale reader: {path.name}")
    require(review.get("assessment_id") in (None, assessment_id), f"review assessment mismatch: {path.name}")
    severity = review.get("severity_census", {})
    require((severity.get("P1"), severity.get("P2"), severity.get("P3")) == (0, 0, 0), f"unresolved findings: {path.name}")
    return review


def validate_assessment(assessment_id: str, cfg: dict[str, Any]) -> dict[str, Any]:
    reader: Path = cfg["reader"]
    require(reader.is_file(), f"missing reader: {reader.relative_to(LANE)}")
    raw = reader.read_bytes()
    require(raw and b"\r" not in raw and raw.endswith(b"\n"), f"reader must be nonempty UTF-8/LF: {reader.name}")
    text = raw.decode("utf-8", errors="strict")
    token = str(cfg["token"])
    edition_unit_id = str(cfg["edition_unit_id"])
    for marker in (
        f"assessment_id: {assessment_id}",
        f"edition_unit_id: {edition_unit_id}",
        'rights: "CC BY-SA 4.0"',
        MODEL,
    ):
        require(marker in text, f"required marker missing in {reader.name}: {marker}")

    expected_ids = {f"o012-d60-{token}", f"o012-d60-{token}-coverage"}
    expected_ids.update(f"o012-d60-{token}-s{i:02d}" for i in range(1, 9))
    for kind in ("ex", "hint", "sol"):
        expected_ids.update(f"o012-d60-{token}-{kind}-{i:03d}" for i in range(1, 9))
    ids = re.findall(rf"#(o012-d60-{token}(?:-[a-z0-9]+)*)\b", text)
    require(len(ids) == len(set(ids)), f"duplicate stable IDs in {reader.name}")
    require(set(ids) == expected_ids, f"stable-ID inventory drift in {reader.name}: {sorted(set(ids) ^ expected_ids)}")

    openings = re.findall(r"(?m)^:::\s+\{", text)
    closings = re.findall(r"(?m)^:::\s*$", text)
    require(len(openings) == len(closings) == 24, f"fenced-div inventory is not 24 balanced blocks: {reader.name}")
    for css_class in ("exercise", "hint", "solution"):
        require(len(re.findall(rf"(?m)^:::\s+\{{\.{css_class}\b", text)) == 8, f"{css_class} count is not eight: {reader.name}")

    routes: list[str] = []
    for item in range(1, 9):
        item_routes: set[str] = set()
        for kind in ("ex", "hint", "sol"):
            stable_id = f"o012-d60-{token}-{kind}-{item:03d}"
            match = re.search(rf"(?m)^:::\s+\{{\.[a-z]+\s+#{stable_id}\s+([^\n]+)\}}$", text)
            require(match is not None, f"missing fenced-div attributes: {stable_id}")
            attributes = match.group(1)
            require('data-origin="edition-original"' in attributes, f"origin missing: {stable_id}")
            require(f'data-assessment-id="{assessment_id}"' in attributes, f"assessment binding missing: {stable_id}")
            route_match = re.search(r'data-course-route-unit-id="(D60-R\d{2})"', attributes)
            require(route_match is not None, f"primary route missing: {stable_id}")
            route = route_match.group(1)
            require(route in cfg["allowed_primary_routes"], f"out-of-scope primary route {route}: {stable_id}")
            item_routes.add(route)
        require(len(item_routes) == 1, f"triple route mismatch at item {item}: {reader.name}")
        routes.append(item_routes.pop())
    require(cfg["required_primary_routes"].issubset(set(routes)), f"required route coverage missing: {reader.name}")

    hints = re.findall(r"(?ms)^:::\s+\{\.hint\b[^\n]*\}\n(.*?)\n:::\s*$", text)
    solutions = re.findall(r"(?ms)^:::\s+\{\.solution\b[^\n]*\}\n(.*?)\n:::\s*$", text)
    require(len(hints) == len(solutions) == 8, f"triple extraction failed: {reader.name}")
    require(all(len(block.strip()) >= 100 for block in hints), f"an assessment hint is implausibly short: {reader.name}")
    require(all(len(block.strip()) >= 450 for block in solutions), f"a complete solution is implausibly short: {reader.name}")
    require(text.count("$$") % 2 == 0, f"unbalanced display-math delimiters: {reader.name}")
    for marker in ("TODO", "TBD", "FILL_AFTER", "C:\\Users\\", "github_pat_", "ghp_", "access_token", "BEGIN PRIVATE KEY"):
        require(marker not in text, f"forbidden marker in {reader.name}: {marker}")
    require("bank masalah Fomberg" in text, f"excluded-problem-bank notice missing: {reader.name}")

    reader_sha = hashlib.sha256(raw).hexdigest()
    math_review = load_review(cfg["math_review"], "independent_mathematics", reader_sha, assessment_id)
    language_review = load_review(cfg["language_review"], "independent_source_language", reader_sha, assessment_id)
    return {
        "assessment_id": assessment_id,
        "edition_unit_id": edition_unit_id,
        "reader": {
            "identity": identity(reader),
            "stable_ids": len(ids),
            "exercise_hint_solution_triples": 8,
            "complete_checked_solutions": 8,
            "primary_route_sequence": routes,
            "primary_route_coverage": sorted(set(routes)),
        },
        "rights": {"license": "CC BY-SA 4.0", "origin": "edition_original", "source_problem_bank_used": False},
        "independent_reviews": {
            "mathematics": {**identity(cfg["math_review"]), "status": math_review["status"]},
            "source_language": {**identity(cfg["language_review"]), "status": language_review["status"]},
        },
    }


def main() -> None:
    assessments = [validate_assessment(assessment_id, cfg) for assessment_id, cfg in CONFIG.items()]
    all_ids: list[str] = []
    for assessment in assessments:
        token = assessment["assessment_id"].lower().replace("d60-", "")
        reader = LANE / CONFIG[assessment["assessment_id"]]["reader"].relative_to(LANE)
        all_ids.extend(re.findall(rf"#(o012-d60-{token}(?:-[a-z0-9]+)*)\b", reader.read_text(encoding="utf-8")))
    require(len(all_ids) == len(set(all_ids)) == 68, "combined CA02/CA03 stable-ID inventory is not 68 unique IDs")
    receipt = {
        "qa_id": "O012-D60-CUMULATIVE-ASSESSMENTS-002-003",
        "status": "PASS",
        "model_provenance": MODEL,
        "assessments": assessments,
        "cumulative_items_added": 16,
        "exercise_hint_solution_triples": 16,
        "complete_checked_solutions": 16,
        "mastery_postcondition": {"ordinary": 84, "ca01": 8, "ca02": 8, "ca03": 8, "total": 108},
        "checks": {
            "utf8_lf": "PASS",
            "front_matter": "PASS",
            "stable_id_uniqueness_and_inventory": "PASS",
            "balanced_fenced_divs": "PASS",
            "route_binding": "PASS",
            "sixteen_hints": "PASS",
            "sixteen_full_solutions": "PASS",
            "display_math_balance": "PASS",
            "rights_and_origin": "PASS",
            "privacy": "PASS",
        },
    }
    OUTPUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "output": identity(OUTPUT)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
