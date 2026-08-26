#!/usr/bin/env python3
"""Fail-closed structural QA for the first D60 cumulative assessment."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


LANE = Path(__file__).resolve().parents[1]
READER = LANE / "source/id-ID/mastery/cumulative-assessment-001-foundations-coverings-homotopy.md"
MATH_REVIEW = LANE / "qa/cumulative-assessment-001/INDEPENDENT_MATH_REVIEW.json"
LANGUAGE_REVIEW = LANE / "qa/cumulative-assessment-001/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json"
OUTPUT = LANE / "qa/CUMULATIVE_ASSESSMENT_001_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(path: Path) -> dict[str, object]:
    return {
        "path": path.relative_to(LANE).as_posix(),
        "bytes": path.stat().st_size,
        "lf_lines": path.read_bytes().count(b"\n"),
        "sha256": digest(path),
    }


def load_review(path: Path, expected_kind: str) -> dict[str, object]:
    require(path.is_file(), f"missing independent review: {path.relative_to(LANE)}")
    review = json.loads(path.read_text(encoding="utf-8"))
    require(review.get("review_kind") == expected_kind, f"wrong review kind: {path.name}")
    require(str(review.get("status", "")).startswith("PASS"), f"review is not PASS: {path.name}")
    require(review.get("independent_from_production") is True, f"review is not independent: {path.name}")
    severity = review.get("severity_census", {})
    require(
        (severity.get("P1"), severity.get("P2"), severity.get("P3")) == (0, 0, 0),
        f"unresolved review findings: {path.name}",
    )
    require(review.get("reader_sha256") == digest(READER), f"review binds stale reader: {path.name}")
    return review


def main() -> None:
    require(READER.is_file(), "cumulative assessment reader is missing")
    raw = READER.read_bytes()
    require(raw and b"\r" not in raw, "reader must be nonempty UTF-8/LF")
    text = raw.decode("utf-8")
    require(text.startswith("---\n") and "\n---\n" in text[4:], "front matter is missing")
    for marker in (
        'assessment_id: D60-CA01',
        'edition_unit_id: O012-ORIG-CA01',
        'rights: "CC BY-SA 4.0"',
        MODEL,
    ):
        require(marker in text, f"required metadata marker missing: {marker}")

    expected_ids = {"o012-d60-ca01", "o012-d60-ca01-coverage"}
    expected_ids.update(f"o012-d60-ca01-s{i:02d}" for i in range(1, 9))
    for kind in ("ex", "hint", "sol"):
        expected_ids.update(f"o012-d60-ca01-{kind}-{i:03d}" for i in range(1, 9))
    ids = re.findall(r"#(o012-d60-ca01(?:-[a-z0-9]+)*)\b", text)
    require(len(ids) == len(set(ids)), "assessment contains duplicate stable IDs")
    require(set(ids) == expected_ids, f"stable-ID inventory drift: {sorted(set(ids) ^ expected_ids)}")

    openings = re.findall(r"(?m)^:::\s+\{", text)
    closings = re.findall(r"(?m)^:::\s*$", text)
    require(len(openings) == len(closings) == 24, "fenced-div inventory is not 24 balanced triples")
    for css_class in ("exercise", "hint", "solution"):
        require(
            len(re.findall(rf"(?m)^:::\s+\{{\.{css_class}\b", text)) == 8,
            f"{css_class} count is not eight",
        )

    route_by_item = {
        1: "D60-R01",
        2: "D60-R02",
        3: "D60-R03",
        4: "D60-R04",
        5: "D60-R05",
        6: "D60-R06",
        7: "D60-R07",
        8: "D60-R06",
    }
    for item, route in route_by_item.items():
        for kind in ("ex", "hint", "sol"):
            stable_id = f"o012-d60-ca01-{kind}-{item:03d}"
            pattern = rf"(?m)^:::\s+\{{\.[a-z]+\s+#{stable_id}\s+([^\n]+)\}}$"
            match = re.search(pattern, text)
            require(match is not None, f"missing fenced-div attributes for {stable_id}")
            attributes = match.group(1)
            require('data-origin="edition-original"' in attributes, f"origin missing: {stable_id}")
            require('data-assessment-id="D60-CA01"' in attributes, f"assessment binding missing: {stable_id}")
            require(
                f'data-course-route-unit-id="{route}"' in attributes,
                f"route binding mismatch: {stable_id}",
            )

    solution_blocks = re.findall(
        r"(?ms)^:::\s+\{\.solution\b[^\n]*\}\n(.*?)\n:::\s*$", text
    )
    require(len(solution_blocks) == 8, "solution extraction did not find eight blocks")
    require(all(len(block.strip()) >= 450 for block in solution_blocks), "a full solution is implausibly short")
    require(text.count("$$") % 2 == 0, "display-math delimiters are unbalanced")
    for marker in ("TODO", "TBD", "FILL_AFTER", "C:\\Users\\", "github_pat_", "ghp_", "access_token"):
        require(marker not in text, f"forbidden marker in reader: {marker}")
    require("bank masalah Fomberg" in text, "excluded-problem-bank notice missing")

    math_review = load_review(MATH_REVIEW, "independent_mathematics")
    language_review = load_review(LANGUAGE_REVIEW, "independent_source_language")
    receipt = {
        "qa_id": "O012-D60-CUMULATIVE-ASSESSMENT-001",
        "status": "PASS",
        "assessment_id": "D60-CA01",
        "edition_unit_id": "O012-ORIG-CA01",
        "model_provenance": MODEL,
        "reader": {
            "identity": identity(READER),
            "stable_ids": len(ids),
            "exercise_hint_solution_triples": 8,
            "complete_checked_solutions": 8,
            "primary_route_coverage": sorted(set(route_by_item.values())),
            "secondary_route_coverage": ["D60-R04", "D60-R05"],
        },
        "rights": {
            "license": "CC BY-SA 4.0",
            "origin": "edition_original",
            "source_problem_bank_used": False,
        },
        "independent_reviews": {
            "mathematics": {**identity(MATH_REVIEW), "status": math_review["status"]},
            "source_language": {**identity(LANGUAGE_REVIEW), "status": language_review["status"]},
        },
        "checks": {
            "utf8_lf": "PASS",
            "front_matter": "PASS",
            "stable_id_uniqueness_and_inventory": "PASS",
            "balanced_fenced_divs": "PASS",
            "route_binding": "PASS",
            "eight_hints": "PASS",
            "eight_full_solutions": "PASS",
            "display_math_balance": "PASS",
            "rights_and_origin": "PASS",
            "privacy": "PASS",
        },
    }
    OUTPUT.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"status": "PASS", "output": identity(OUTPUT)}, indent=2))


if __name__ == "__main__":
    main()
