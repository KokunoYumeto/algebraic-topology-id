#!/usr/bin/env python3
"""Fail-closed source and static QA for Fomberg Unit 004.

This validator binds the admitted Indonesian reader to the frozen upstream
span, checks its semantic and mastery surfaces, and writes deterministic
receipts only after every assertion passes.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import shlex
import shutil
import struct
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


LANE = Path(__file__).resolve().parents[1]
AUDIT_OUTPUT = LANE / "qa/FOMBERG_UNIT_004_SOURCE_AUDIT.json"
QA_OUTPUT = LANE / "qa/FOMBERG_UNIT_004_QA.json"

DATE = "2026-08-25"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
COMMIT = "563194fae879178b9a6871b249513bfc27968975"
TREE = "fb678966d1533d529bdd72f49d8496a3bdc14a9b"
READER_PATH = (
    "source/id-ID/fomberg/units/"
    "fomberg-unit-004-excision-mayer-vietoris-naturality-comparison.md"
)
PRIOR_READER_PATH = (
    "source/id-ID/fomberg/units/"
    "fomberg-unit-003-exact-sequences-relative-homology.md"
)
UPSTREAM_PATH = (
    "authority/upstream/"
    "math-notes-563194fae879178b9a6871b249513bfc27968975/"
    "tree/algebraic_topology.tex"
)
TERMINOLOGY_PATH = "00_control/TERMINOLOGY.csv"
ADVERSE_PATH = "00_control/ADVERSE_LEDGER.csv"
TERM_DRAFT_PATH = "qa/fomberg-unit-004/TERMINOLOGY_ROWS_DRAFT.csv"
ADVERSE_DRAFT_PATH = "qa/fomberg-unit-004/ADVERSE_ROWS_DRAFT.csv"
REVIEW_PATH = "qa/fomberg-unit-004/INDEPENDENT_REVIEW_FINAL.json"

READER_IDENTITY = {
    "bytes": 87293,
    "lf_lines": 2364,
    "sha256": "2c04d647b58afe044f5549bcba9ad3572075775711bb3aaec45d0e94fe3d3e91",
}
UPSTREAM_IDENTITY = {
    "bytes": 223886,
    "lf_lines": 6069,
    "sha256": "d27095de0f38f0c14b2d7716cb52d51d064f0594dd9f82f9d1b3e6af5b35a483",
}
SPAN_IDENTITY = {
    "line_start": 1923,
    "line_end": 2846,
    "lf_lines": 924,
    "bytes": 38503,
    "sha256": "ddde995b54154623ccc565117aee63cce8361d2ada1c3c9f2852775b1aaac638",
}
NEXT_LINE = 2847
NEXT_TEXT = r"\subsection{Degree maps}"
REVIEW_IDENTITY = {
    "bytes": 2524,
    "lf_lines": 87,
    "sha256": "3c43a86f24adcb042b0ccc43d2e5031478ba622acd8925eca92721cf2cd5d102",
}
CONTROL_IDENTITIES = {
    TERMINOLOGY_PATH: {
        "bytes": 53356,
        "lf_lines": 435,
        "sha256": "cf974537fd20758cbe5bdfba7561c81df8db0ec34de3d2b61f4347d02093c9e7",
    },
    ADVERSE_PATH: {
        "bytes": 184841,
        "lf_lines": 523,
        "sha256": "c2ae75371712f74541f3a96539ec601e40fee6d788dbb22989c99cf49d85d83f",
    },
}
DRAFT_IDENTITIES = {
    TERM_DRAFT_PATH: {
        "bytes": 3536,
        "lf_lines": 20,
        "sha256": "bd633e1189e01ed0eaf1f25d951c9ccf022ea1e1e7a5ce8190d261a1f514bb22",
    },
    ADVERSE_DRAFT_PATH: {
        "bytes": 17312,
        "lf_lines": 25,
        "sha256": "545dbb902b00409ce18de5b0e0aaf081d4b6ce04da92a5b3d71173cc07e24355",
    },
}

EXPECTED_HEADING_IDS = [
    "o012-fom-u004-notice",
    "o012-fom-u004",
    "o012-fom-u004-s07",
    "o012-fom-u004-s08",
    "o012-fom-u004-s09",
    "o012-fom-u004-s10",
    "o012-fom-u004-mastery",
]
EXPECTED_CLASS_COUNTS = {
    "boundary": 1,
    "corollary": 1,
    "definition": 3,
    "example": 2,
    "exercise": 7,
    "figure": 19,
    "heading": 7,
    "hint": 7,
    "lemma": 2,
    "proof": 14,
    "proof-supplement": 3,
    "proposition": 4,
    "remark": 10,
    "solution": 7,
    "source-audit": 17,
    "source-omission": 8,
    "theorem": 5,
}
EXPECTED_ID_SEQUENCE_SHA256 = (
    "1fbbae04da5968b1004b20868bb28d1bb402e7ed0042a65c7c115d11f19fc7fb"
)
EXPECTED_LINK_TARGET_COUNTS = Counter({
    "o012-fom-u003-cor-sphere-homology": 1,
    "o012-fom-u004-lem-compact-finite-simplices": 1,
    "o012-fom-u004-lem-five": 1,
    "o012-fom-u004-proof-pr05a": 1,
    "o012-fom-u004-proof-pr05b": 1,
    "o012-fom-u004-proof-relative-generator-repair": 1,
    "o012-fom-u004-prop-simplex-generator": 1,
    "o012-fom-u004-prop-sing-simp": 1,
    "o012-fom-u004-prop-wedge-homology": 1,
    "o012-fom-u004-rem-excision-cover-form": 1,
    "o012-fom-u004-thm-invariance-dimension": 2,
    "o012-fom-u004-thm-relative-quotient": 2,
})
SOURCE_ENVIRONMENT_COUNTS = {
    "corollary": 1,
    "definition": 3,
    "example": 2,
    "lemma": 2,
    "proof": 10,
    "proposition": 4,
    "remark": 10,
    "theorem": 5,
}
SOURCE_ENVIRONMENT_TOTAL = 37
REPAIR_IDS = [f"FOM-PR-{number:02d}" for number in range(5, 12)]

ASSET_SPECS = {
    "excision-equivalence.png": (
        139672,
        "8d4e0aa9ffe93edbe3d3eb3def640ace8d2ffbcc45044cd5dcd3a1de1124b650",
        (1920, 860),
    ),
    "excision-equivalence.svg": (
        3613,
        "e69df6490440c5c81416fe0c713d160e91d01216c944bb146aba94540234c3ad",
        None,
    ),
    "mayer-vietoris-cover.png": (
        111228,
        "55ca7d82c34c8381a0ff6d9a2cb89a04ed9c364298277cb3f2a22d5d98e00769",
        (1800, 860),
    ),
    "mayer-vietoris-cover.svg": (
        2699,
        "73da09f59c7b27bcc5ef5dd7b568c97f8bb9da846cf4d0c77d5bfa6536adf733",
        None,
    ),
    "rp2-mayer-vietoris-cover.png": (
        154975,
        "d086a936b73046b2d505204cd016e5b2e6db539245a0f40b77e4d79ee2c85525",
        (1360, 1040),
    ),
    "rp2-mayer-vietoris-cover.svg": (
        3039,
        "fe2eed2d863ee12a01e982cb5158481601216a337d91e79aa3316ffc7b6252e0",
        None,
    ),
}
EXPECTED_RASTER_REFS = [
    "../assets/unit-004/excision-equivalence.png",
    "../assets/unit-004/mayer-vietoris-cover.png",
    "../assets/unit-004/rp2-mayer-vietoris-cover.png",
]


def die(message: str) -> None:
    raise SystemExit(f"Fomberg Unit 004 QA FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        die(message)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def strict_text(relative: str) -> tuple[bytes, str]:
    path = LANE / relative
    require(path.is_file(), f"missing {relative}")
    raw = path.read_bytes()
    require(not raw.startswith(b"\xef\xbb\xbf"), f"{relative}: BOM forbidden")
    require(b"\r" not in raw, f"{relative}: CR/CRLF forbidden")
    require(raw.endswith(b"\n"), f"{relative}: terminal LF required")
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        die(f"{relative}: invalid UTF-8 ({exc})")
    require("\ufffd" not in text, f"{relative}: replacement character forbidden")
    return raw, text


def identity(relative: str, raw: bytes | None = None) -> dict[str, Any]:
    payload = (LANE / relative).read_bytes() if raw is None else raw
    return {
        "path": relative,
        "bytes": len(payload),
        "lf_lines": payload.count(b"\n"),
        "sha256": sha256(payload),
        "encoding": "UTF-8",
        "newline": "LF",
    }


def require_identity(relative: str, expected: dict[str, Any]) -> tuple[bytes, str, dict[str, Any]]:
    raw, text = strict_text(relative)
    actual = identity(relative, raw)
    for field in ("bytes", "lf_lines", "sha256"):
        require(actual[field] == expected[field],
                f"{relative}: {field}={actual[field]!r}, expected {expected[field]!r}")
    return raw, text, actual


def receipt_bytes(obj: dict[str, Any]) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2)
            .encode("utf-8") + b"\n")


def parse_attributes(inner: str, where: str) -> tuple[str, list[str], dict[str, str]]:
    try:
        tokens = shlex.split(inner, posix=True)
    except ValueError as exc:
        die(f"{where}: malformed attributes ({exc})")
    ids: list[str] = []
    classes: list[str] = []
    attrs: dict[str, str] = {}
    for token in tokens:
        if token.startswith("#"):
            ids.append(token[1:])
        elif token.startswith("."):
            classes.append(token[1:])
        elif "=" in token:
            key, value = token.split("=", 1)
            require(key and key not in attrs, f"{where}: duplicate/empty attribute")
            attrs[key] = value
        else:
            die(f"{where}: unparsed token {token!r}")
    require(len(ids) == 1 and ids[0], f"{where}: exactly one ID required")
    require(len(classes) == len(set(classes)), f"{where}: duplicate class")
    return ids[0], classes, attrs


def parse_reader(text: str) -> tuple[list[dict[str, Any]], int, int]:
    nodes: list[dict[str, Any]] = []
    stack: list[dict[str, Any]] = []
    opens = 0
    closes = 0
    for number, line in enumerate(text.splitlines(), 1):
        heading = re.match(r"^(#{1,6})\s+(.+?)\s+\{([^{}]+)\}\s*$", line)
        if heading:
            ident, classes, attrs = parse_attributes(
                heading.group(3), f"heading line {number}"
            )
            nodes.append({
                "id": ident,
                "kind": "heading",
                "classes": classes,
                "attrs": attrs,
                "line_start": number,
                "line_end": number,
            })
        opener = re.match(r"^(:{3,})\s+(\{.*\})\s*$", line)
        if opener:
            ident, classes, attrs = parse_attributes(
                opener.group(2)[1:-1].strip(), f"fence line {number}"
            )
            require(len(classes) == 1, f"fence line {number}: one class required")
            node = {
                "id": ident,
                "kind": classes[0],
                "classes": classes,
                "attrs": attrs,
                "line_start": number,
                "line_end": 0,
                "fence_length": len(opener.group(1)),
            }
            stack.append(node)
            nodes.append(node)
            opens += 1
            continue
        closer = re.match(r"^(:{3,})\s*$", line)
        if closer:
            require(stack, f"line {number}: unmatched closing fence")
            node = stack.pop()
            require(len(closer.group(1)) == node["fence_length"],
                    f"line {number}: closing fence width mismatch")
            node["line_end"] = number
            closes += 1
    require(not stack, "unclosed fenced div")
    require(opens == closes, "fenced-div imbalance")
    return nodes, opens, closes


def parse_source_locator(value: str, where: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    for part in value.split(","):
        match = re.fullmatch(r"(\d+)(?:-(\d+))?", part.strip())
        require(match is not None, f"{where}: invalid locator {part!r}")
        start = int(match.group(1))
        end = int(match.group(2) or start)
        require(1923 <= start <= end <= 2846,
                f"{where}: locator {start}-{end} outside admitted span")
        ranges.append((start, end))
    return ranges


def png_dimensions(raw: bytes) -> tuple[int, int]:
    require(raw[:8] == b"\x89PNG\r\n\x1a\n", "invalid PNG signature")
    require(raw[12:16] == b"IHDR", "PNG IHDR missing")
    return struct.unpack(">II", raw[16:24])


def verify_source() -> dict[str, Any]:
    raw, text, upstream_identity = require_identity(UPSTREAM_PATH, UPSTREAM_IDENTITY)
    lines = raw.splitlines(keepends=True)
    require(len(lines) == 6069, "upstream physical-line count mismatch")
    span = b"".join(lines[1922:2846])
    span_actual = {
        "line_start": 1923,
        "line_end": 2846,
        "lf_lines": span.count(b"\n"),
        "bytes": len(span),
        "sha256": sha256(span),
    }
    require(span_actual == SPAN_IDENTITY, "frozen source-span identity mismatch")
    require(lines[2846].decode("utf-8").rstrip("\n") == NEXT_TEXT,
            "exact next source line mismatch")
    span_text = span.decode("utf-8")
    env_counts = Counter(re.findall(r"\\begin\{([^}]+)\}", span_text))
    mathematical = {key: env_counts[key] for key in SOURCE_ENVIRONMENT_COUNTS}
    require(mathematical == SOURCE_ENVIRONMENT_COUNTS,
            f"source mathematical environment census mismatch: {mathematical}")
    require(sum(mathematical.values()) == SOURCE_ENVIRONMENT_TOTAL,
            "source mathematical environment total mismatch")
    subsections = re.findall(r"^\\subsection\{", span_text, flags=re.MULTILINE)
    require(len(subsections) == 4, "source subsection count mismatch")
    return {
        "authority_identity": upstream_identity,
        "commit": COMMIT,
        "tree": TREE,
        "selected_span": span_actual,
        "subsections": 4,
        "mathematical_environments": mathematical,
        "mathematical_environment_total": SOURCE_ENVIRONMENT_TOTAL,
        "next_line": NEXT_LINE,
        "next_line_text": NEXT_TEXT,
    }


def verify_controls() -> dict[str, Any]:
    identities: dict[str, Any] = {}
    texts: dict[str, str] = {}
    for relative, expected in {**CONTROL_IDENTITIES, **DRAFT_IDENTITIES}.items():
        _, text, ident = require_identity(relative, expected)
        identities[relative] = ident
        texts[relative] = text

    term_rows = list(csv.DictReader(texts[TERMINOLOGY_PATH].splitlines()))
    term_draft = list(csv.DictReader(texts[TERM_DRAFT_PATH].splitlines()))
    adverse_rows = list(csv.DictReader(texts[ADVERSE_PATH].splitlines()))
    adverse_draft = list(csv.DictReader(texts[ADVERSE_DRAFT_PATH].splitlines()))
    require(len(term_rows) == 434 and len(term_draft) == 19,
            "terminology row count mismatch")
    require(len(adverse_rows) == 522 and len(adverse_draft) == 24,
            "adverse row count mismatch")
    require(term_rows[-19:] == term_draft, "terminology tail differs from reviewed draft")
    require(adverse_rows[-24:] == adverse_draft,
            "adverse tail differs from reviewed draft")
    require(len({row["term_id"] for row in term_rows}) == 434,
            "duplicate terminology ID")
    require(len({row["event_id"] for row in adverse_rows}) == 522,
            "duplicate adverse ID")
    require(term_rows[-1]["term_id"] == "O012-TERM-0434",
            "terminology terminal ID mismatch")
    require(adverse_rows[-1]["event_id"] == "O012-ADV-0522",
            "adverse terminal ID mismatch")
    for repair in REPAIR_IDS:
        require(any(repair in row["observed"] for row in adverse_draft),
                f"{repair}: no adverse-ledger evidence")
    return {
        "identities": identities,
        "terminology": {
            "rows": 434,
            "unit_rows": 19,
            "terminal_id": "O012-TERM-0434",
            "unit_tail_matches_reviewed_draft": True,
        },
        "adverse": {
            "rows": 522,
            "unit_rows": 24,
            "terminal_id": "O012-ADV-0522",
            "unit_tail_matches_reviewed_draft": True,
        },
    }


def verify_review() -> dict[str, Any]:
    raw, text, ident = require_identity(REVIEW_PATH, REVIEW_IDENTITY)
    try:
        review = json.loads(text)
    except json.JSONDecodeError as exc:
        die(f"independent review malformed ({exc})")
    require(review.get("status") == "PASS_P1_P2_P3_ZERO",
            "independent review not final PASS")
    require(review.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0},
            "independent review severity census not zero")
    require(review.get("canonical", {}).get("sha256") == READER_IDENTITY["sha256"],
            "independent review canonical hash mismatch")
    require(review.get("upstream_span", {}).get("sha256") == SPAN_IDENTITY["sha256"],
            "independent review source-span hash mismatch")
    require(review.get("file_mutations_by_reviewer") == 0,
            "independent review was not read-only")
    return {"identity": ident, "status": review["status"],
            "severity_census": review["severity_census"]}


def verify_assets(reader_text: str, nodes: list[dict[str, Any]]) -> dict[str, Any]:
    root = LANE / "source/id-ID/fomberg/assets/unit-004"
    identities: list[dict[str, Any]] = []
    for name, (expected_bytes, expected_sha, expected_dims) in ASSET_SPECS.items():
        path = root / name
        require(path.is_file(), f"missing asset {name}")
        raw = path.read_bytes()
        require(len(raw) == expected_bytes, f"{name}: byte count mismatch")
        require(sha256(raw) == expected_sha, f"{name}: SHA-256 mismatch")
        item: dict[str, Any] = {
            "path": f"source/id-ID/fomberg/assets/unit-004/{name}",
            "bytes": len(raw),
            "sha256": sha256(raw),
        }
        if expected_dims is not None:
            dims = png_dimensions(raw)
            require(dims == expected_dims, f"{name}: dimensions mismatch")
            item["dimensions"] = list(dims)
        else:
            require(raw.lstrip().startswith(b"<svg") or b"<svg" in raw[:500],
                    f"{name}: SVG root missing")
        identities.append(item)

    raster_refs = re.findall(r"!\[[^\]]+\]\((\.\./assets/unit-004/[^)]+)\)",
                             reader_text)
    require(raster_refs == EXPECTED_RASTER_REFS, "reader raster references mismatch")
    require(reader_text.count("{.semantic-redraw") == 3,
            "semantic-redraw marker count mismatch")
    figures = [node for node in nodes if node["kind"] == "figure"]
    require(len(figures) == 19, "semantic figure count mismatch")
    for node in figures:
        require(node["attrs"].get("data-origin") == "edition-original-redraw",
                f"{node['id']}: redraw provenance missing")
        require(node["line_end"] - node["line_start"] >= 4,
                f"{node['id']}: semantic description too short")
    return {
        "files": identities,
        "raster_reader_refs": raster_refs,
        "semantic_figures": 19,
        "raster_redraws": 3,
        "all_redraw_provenance_present": True,
    }


def verify_pandoc() -> dict[str, Any]:
    executable = shutil.which("pandoc")
    require(executable is not None, "Pandoc unavailable")
    version = subprocess.run(
        [executable, "--version"], check=False, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace",
        timeout=30,
    )
    native = subprocess.run(
        [executable, "--from=markdown+fenced_divs+tex_math_dollars",
         "--to=native", "--wrap=none", str(LANE / READER_PATH)],
        check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace", timeout=60, cwd=LANE,
    )
    html = subprocess.run(
        [executable, "--from=markdown+fenced_divs+tex_math_dollars",
         "--to=html5", "--mathml", "--wrap=none", str(LANE / READER_PATH)],
        check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace", timeout=60, cwd=LANE,
    )
    require(version.returncode == 0 and version.stdout.splitlines(),
            "Pandoc version probe failed")
    require(native.returncode == 0,
            f"Pandoc native parse failed: {native.stderr[-800:]}")
    require(html.returncode == 0,
            f"Pandoc MathML render failed: {html.stderr[-800:]}")
    math_count = html.stdout.count("<math")
    require(math_count >= 100, f"Pandoc MathML count unexpectedly low ({math_count})")
    return {
        "version": version.stdout.splitlines()[0].strip(),
        "native_parse": "PASS",
        "mathml_render": "PASS",
        "mathml_nodes": math_count,
    }


def verify_reader() -> dict[str, Any]:
    raw, text, reader_identity = require_identity(READER_PATH, READER_IDENTITY)
    prior_raw, prior_text = strict_text(PRIOR_READER_PATH)
    require(sha256(prior_raw) ==
            "2571f62b977c00bff20e04756925a73497c0129f8c987940db0e1a649177f6b9",
            "prior-unit cross-link witness changed")
    nodes, opens, closes = parse_reader(text)
    ids = [node["id"] for node in nodes]
    require(len(ids) == 117 and len(set(ids)) == 117,
            "stable ID count/uniqueness mismatch")
    require(all(re.fullmatch(r"[a-z0-9][a-z0-9-]*", ident) for ident in ids),
            "non-locale-neutral stable ID syntax")
    sequence_sha = sha256(("\n".join(ids) + "\n").encode("utf-8"))
    require(sequence_sha == EXPECTED_ID_SEQUENCE_SHA256,
            "ordered stable-ID sequence mismatch")
    headings = [node["id"] for node in nodes if node["kind"] == "heading"]
    require(headings == EXPECTED_HEADING_IDS, "heading topology/order mismatch")
    class_counts = Counter(node["kind"] for node in nodes)
    require(dict(sorted(class_counts.items())) == EXPECTED_CLASS_COUNTS,
            f"semantic class census mismatch: {dict(class_counts)}")

    locators: list[dict[str, Any]] = []
    for node in nodes:
        value = node["attrs"].get("data-source-lines")
        if value is not None:
            ranges = parse_source_locator(value, node["id"])
            locators.append({"id": node["id"], "value": value,
                             "ranges": [list(item) for item in ranges]})
    require(len(locators) == 93, "source locator count mismatch")

    link_counts = Counter(re.findall(r"\]\(#([^)]+)\)", text))
    require(link_counts == EXPECTED_LINK_TARGET_COUNTS,
            f"fragment-link census mismatch: {link_counts}")
    for target in link_counts:
        if target.startswith("o012-fom-u004-"):
            require(target in ids, f"unresolved same-unit fragment #{target}")
        else:
            require(target == "o012-fom-u003-cor-sphere-homology" and
                    f"#{target}" in prior_text,
                    f"unresolved cross-unit fragment #{target}")

    node_by_id = {node["id"]: node for node in nodes}
    for number in range(1, 8):
        suffix = f"{number:03d}"
        exercise = node_by_id.get(f"o012-fom-u004-mcheck-{suffix}")
        hint = node_by_id.get(f"o012-fom-u004-hint-{suffix}")
        solution = node_by_id.get(f"o012-fom-u004-sol-{suffix}")
        require(exercise is not None and hint is not None and solution is not None,
                f"mastery triple {suffix} incomplete")
        require(exercise["line_start"] < hint["line_start"] < solution["line_start"],
                f"mastery triple {suffix} order invalid")
        require(solution["line_end"] - solution["line_start"] >= 8,
                f"solution {suffix} is not complete enough for admission")

    for repair in REPAIR_IDS:
        require(repair in text, f"{repair}: missing from reader")
    for repair in ("05", "06", "07", "08", "09", "10", "11"):
        pattern = (r'data-repair-id="FOM-PR-' + repair + r'"[^>\n]*'
                   r'data-proof-status="complete_original_repair"')
        require(re.search(pattern, text) is not None,
                f"FOM-PR-{repair}: complete original proof marker missing")

    required_prose = [
        "Creative Commons Attribution-ShareAlike 4.0 International",
        "OpenAI Codex gpt-5.6-sol, Ultra",
        "Tidak ada prosa dari bank soal Fomberg terpisah",
        "tidak menyiratkan dukungan, pengesahan, atau",
        "afiliasi dengan Yeheli Fomberg",
        "edition_unit_id: \"O012-FOM-004\"",
        "course_route_unit_id: \"D60-R11\"",
    ]
    for phrase in required_prose:
        require(phrase in text, f"required rights/provenance phrase absent: {phrase}")
    forbidden = [
        "Translation and Transcription Project",
        "TTP",
        "C:\\Users\\",
        "AppData",
        "github_pat_",
        "ghp_",
        "Bearer ",
        "api_token",
    ]
    for phrase in forbidden:
        require(phrase not in text, f"forbidden/private string present: {phrase}")
    require("lang: id-ID" in text, "id-ID locale declaration missing")
    require("$$" in text, "mathematics surface unexpectedly absent")

    assets = verify_assets(text, nodes)
    pandoc = verify_pandoc()
    return {
        "identity": reader_identity,
        "stable_ids": 117,
        "stable_ids_unique": 117,
        "ordered_stable_ids_sha256": sequence_sha,
        "semantic_class_counts": dict(sorted(class_counts.items())),
        "fenced_divs": {"opened": opens, "closed": closes, "balanced": True},
        "source_locators": {"count": len(locators), "valid": len(locators)},
        "fragment_links": {"count": sum(link_counts.values()),
                           "resolved": sum(link_counts.values()),
                           "target_counts": dict(sorted(link_counts.items()))},
        "proof_repairs": REPAIR_IDS,
        "mastery": {"exercise_hint_solution_triples": 7,
                    "complete_solutions": 7},
        "assets": assets,
        "pandoc": pandoc,
        "rights_provenance_privacy": "PASS",
    }


def main() -> None:
    source = verify_source()
    controls = verify_controls()
    review = verify_review()
    reader = verify_reader()

    audit = {
        "schema_version": "1.0.0",
        "audit_id": "O012-FOMBERG-UNIT-004-SOURCE-AUDIT",
        "date": DATE,
        "status": "PASS",
        "role_id": "O012",
        "course_id": "D60",
        "edition_unit_id": "O012-FOM-004",
        "course_route_unit_id": "D60-R11",
        "component": "Fomberg Algebraic Topology Sections 1.7-1.10",
        "license": "CC BY-SA 4.0",
        "model_provenance": MODEL,
        "source": source,
        "reader": reader["identity"],
        "translation_closure": {
            "contiguous_span": "1923-2846",
            "subsections_complete_in_source_order": 4,
            "source_mathematical_environments_represented": 37,
            "proof_repairs_complete": REPAIR_IDS,
            "mastery_triples_complete": 7,
            "next_exact_cursor": 2847,
            "next_exact_text": NEXT_TEXT,
        },
        "correction_and_terminology_ledgers": controls,
        "independent_review": review,
    }
    audit_raw = receipt_bytes(audit)
    AUDIT_OUTPUT.write_bytes(audit_raw)

    qa = {
        "schema_version": "1.0.0",
        "qa_id": "O012-FOMBERG-UNIT-004-STATIC-QA",
        "date": DATE,
        "status": "PASS",
        "model_provenance": MODEL,
        "source_audit": {
            "path": "qa/FOMBERG_UNIT_004_SOURCE_AUDIT.json",
            "bytes": len(audit_raw),
            "sha256": sha256(audit_raw),
        },
        "source": source,
        "reader": reader,
        "controls": controls,
        "independent_review": review,
        "gates": {
            "source_identity_and_contiguity": "PASS",
            "source_order_and_environment_census": "PASS",
            "stable_structure_and_links": "PASS",
            "mathematics_and_proof_repairs": "PASS",
            "mastery_solution_closure": "PASS",
            "terminology_and_correction_ledgers": "PASS",
            "figures_accessibility_and_redraw_provenance": "PASS",
            "pandoc_native_and_mathml": "PASS",
            "license_attribution_nonendorsement_model_and_privacy": "PASS",
            "independent_review_p1_p2_p3_zero": "PASS",
        },
    }
    qa_raw = receipt_bytes(qa)
    QA_OUTPUT.write_bytes(qa_raw)
    print(json.dumps({
        "status": "PASS",
        "source_audit": {"bytes": len(audit_raw), "sha256": sha256(audit_raw)},
        "qa": {"bytes": len(qa_raw), "sha256": sha256(qa_raw)},
        "reader": reader["identity"],
        "stable_ids": reader["stable_ids"],
        "source_locators": reader["source_locators"]["count"],
        "proof_repairs": REPAIR_IDS,
        "mastery_triples": 7,
    }, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
