#!/usr/bin/env python3
"""Fail-closed source and static QA for Fomberg Unit 006.

The reader, reviewed ledger tails, SVG redraws, and independent-review receipt
are intentionally discovered at execution time: their exact identities do not
exist until the canonical unit has been assembled.  The frozen upstream bytes,
admitted source span, topology, semantic closure, rights markers, and mastery
surface are not dynamic and therefore fail closed.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import shlex
import shutil
import subprocess
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from typing import Any


LANE = Path(__file__).resolve().parents[1]
AUDIT_OUTPUT = LANE / "qa/FOMBERG_UNIT_006_SOURCE_AUDIT.json"
QA_OUTPUT = LANE / "qa/FOMBERG_UNIT_006_QA.json"

DATE = "2026-08-25"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
COMMIT = "563194fae879178b9a6871b249513bfc27968975"
TREE = "fb678966d1533d529bdd72f49d8496a3bdc14a9b"
READER_PATH = (
    "source/id-ID/fomberg/units/"
    "fomberg-unit-006-cellular-complexes.md"
)
UNITS_DIR = "source/id-ID/fomberg/units"
ASSET_DIR = "source/id-ID/fomberg/assets/unit-006"
UPSTREAM_PATH = (
    "authority/upstream/"
    "math-notes-563194fae879178b9a6871b249513bfc27968975/"
    "tree/algebraic_topology.tex"
)
TERMINOLOGY_PATH = "00_control/TERMINOLOGY.csv"
ADVERSE_PATH = "00_control/ADVERSE_LEDGER.csv"
TERM_DRAFT_PATH = "qa/fomberg-unit-006/TERMINOLOGY_ROWS_DRAFT.csv"
ADVERSE_DRAFT_PATH = "qa/fomberg-unit-006/ADVERSE_ROWS_DRAFT.csv"
REVIEW_PATH = "qa/fomberg-unit-006/INDEPENDENT_REVIEW_FINAL.json"

UPSTREAM_IDENTITY = {
    "bytes": 223886,
    "lf_lines": 6069,
    "sha256": "d27095de0f38f0c14b2d7716cb52d51d064f0594dd9f82f9d1b3e6af5b35a483",
}
SPAN_IDENTITY = {
    "line_start": 3123,
    "line_end": 3517,
    "lf_lines": 395,
    "bytes": 15540,
    "sha256": "c16d595b8f8c4c67ea5f0f58c1ad7de83ac94efae509d3a8d3bef28da2522f19",
}
NEXT_LINE = 3518
NEXT_TEXT = r"\subsection{Cellular homology}"
SOURCE_ENVIRONMENT_COUNTS = {
    "definition": 1,
    "example": 6,
    "exercise": 1,
    "remark": 6,
}
SOURCE_ENVIRONMENT_TOTAL = 14
SOURCE_TIKZ_INLINE = 19
SOURCE_TIKZPICTURE = 2
SOURCE_LABELS = {
    "exmp:cw-for-sn-one-n-cell",
    "exmp:cw-for-torus",
    "ex:cw-for-cp",
}
EXPECTED_SVG_FILES = 7
EXPECTED_MASTERY_TRIPLES = 6


def die(message: str) -> None:
    raise SystemExit(f"Fomberg Unit 006 QA FAIL: {message}")


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


def require_identity(
    relative: str, expected: dict[str, Any]
) -> tuple[bytes, str, dict[str, Any]]:
    raw, text = strict_text(relative)
    actual = identity(relative, raw)
    for field in ("bytes", "lf_lines", "sha256"):
        require(
            actual[field] == expected[field],
            f"{relative}: {field}={actual[field]!r}, expected {expected[field]!r}",
        )
    return raw, text, actual


def receipt_bytes(obj: dict[str, Any]) -> bytes:
    return (
        json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8")
        + b"\n"
    )


def parse_attributes(
    inner: str, where: str
) -> tuple[str, list[str], dict[str, str]]:
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
            require(
                len(closer.group(1)) == node["fence_length"],
                f"line {number}: closing fence width mismatch",
            )
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
        require(
            3123 <= start <= end <= 3517,
            f"{where}: locator {start}-{end} outside admitted span",
        )
        ranges.append((start, end))
    return ranges


def source_environment_spans(span_text: str) -> list[dict[str, Any]]:
    lines = span_text.splitlines()
    stacks: dict[str, list[int]] = {
        name: [] for name in SOURCE_ENVIRONMENT_COUNTS
    }
    spans: list[dict[str, Any]] = []
    for offset, line in enumerate(lines):
        absolute = 3123 + offset
        begin = re.fullmatch(r"\s*\\begin\{([^}]+)\}(?:\[[^]]*\])?\s*", line)
        if begin and begin.group(1) in stacks:
            stacks[begin.group(1)].append(absolute)
        end = re.fullmatch(r"\s*\\end\{([^}]+)\}\s*", line)
        if end and end.group(1) in stacks:
            name = end.group(1)
            require(stacks[name], f"source {name} ends without opening")
            spans.append({
                "kind": name,
                "line_start": stacks[name].pop(),
                "line_end": absolute,
            })
    require(all(not stack for stack in stacks.values()), "unclosed source environment")
    spans.sort(key=lambda item: item["line_start"])
    return spans


def verify_source() -> dict[str, Any]:
    raw, _, upstream_identity = require_identity(UPSTREAM_PATH, UPSTREAM_IDENTITY)
    lines = raw.splitlines(keepends=True)
    require(len(lines) == 6069, "upstream physical-line count mismatch")
    span = b"".join(lines[3122:3517])
    span_actual = {
        "line_start": 3123,
        "line_end": 3517,
        "lf_lines": span.count(b"\n"),
        "bytes": len(span),
        "sha256": sha256(span),
    }
    require(span_actual == SPAN_IDENTITY, "frozen source-span identity mismatch")
    require(
        lines[3517].decode("utf-8").rstrip("\n") == NEXT_TEXT,
        "exact next source line mismatch",
    )
    span_text = span.decode("utf-8")
    env_counts = Counter(re.findall(r"\\begin\{([^}]+)\}", span_text))
    mathematical = {key: env_counts[key] for key in SOURCE_ENVIRONMENT_COUNTS}
    require(
        mathematical == SOURCE_ENVIRONMENT_COUNTS,
        f"source mathematical environment census mismatch: {mathematical}",
    )
    require(sum(mathematical.values()) == SOURCE_ENVIRONMENT_TOTAL,
            "source mathematical environment total mismatch")
    env_spans = source_environment_spans(span_text)
    require(len(env_spans) == SOURCE_ENVIRONMENT_TOTAL,
            "source environment span census mismatch")
    require(len(re.findall(r"^\\subsection\{", span_text, re.MULTILINE)) == 1,
            "source subsection count mismatch")
    require(span_text.count(r"\tikz[") == SOURCE_TIKZ_INLINE,
            "source inline-TikZ census mismatch")
    require(span_text.count(r"\begin{tikzpicture}") == SOURCE_TIKZPICTURE,
            "source TikZ-picture census mismatch")
    labels = set(re.findall(r"\\label\{([^}]+)\}", span_text))
    require(labels == SOURCE_LABELS, f"source label census mismatch: {labels}")
    return {
        "authority_identity": upstream_identity,
        "commit": COMMIT,
        "tree": TREE,
        "selected_span": span_actual,
        "subsections": 1,
        "mathematical_environments": mathematical,
        "mathematical_environment_total": SOURCE_ENVIRONMENT_TOTAL,
        "mathematical_environment_spans": env_spans,
        "source_inline_tikz_occurrences": SOURCE_TIKZ_INLINE,
        "source_tikzpicture_occurrences": SOURCE_TIKZPICTURE,
        "source_labels": sorted(labels),
        "next_line": NEXT_LINE,
        "next_line_text": NEXT_TEXT,
    }


def consecutive_ids(values: list[str], prefix: str, where: str) -> None:
    require(values, f"{where}: reviewed draft must not be empty")
    numbers: list[int] = []
    for value in values:
        match = re.fullmatch(re.escape(prefix) + r"(\d{4})", value)
        require(match is not None, f"{where}: malformed ID {value!r}")
        numbers.append(int(match.group(1)))
    require(numbers == list(range(numbers[0], numbers[0] + len(numbers))),
            f"{where}: IDs are not consecutive")


def verify_controls() -> dict[str, Any]:
    identities: dict[str, Any] = {}
    texts: dict[str, str] = {}
    for relative in (
        TERMINOLOGY_PATH, ADVERSE_PATH, TERM_DRAFT_PATH, ADVERSE_DRAFT_PATH
    ):
        raw, text = strict_text(relative)
        identities[relative] = identity(relative, raw)
        texts[relative] = text

    term_rows = list(csv.DictReader(texts[TERMINOLOGY_PATH].splitlines()))
    term_draft = list(csv.DictReader(texts[TERM_DRAFT_PATH].splitlines()))
    adverse_rows = list(csv.DictReader(texts[ADVERSE_PATH].splitlines()))
    adverse_draft = list(csv.DictReader(texts[ADVERSE_DRAFT_PATH].splitlines()))
    require(term_rows[-len(term_draft):] == term_draft,
            "terminology tail differs from reviewed draft")
    require(adverse_rows[-len(adverse_draft):] == adverse_draft,
            "adverse tail differs from reviewed draft")
    consecutive_ids([row["term_id"] for row in term_draft],
                    "O012-TERM-", "terminology")
    consecutive_ids([row["event_id"] for row in adverse_draft],
                    "O012-ADV-", "adverse")
    require(len({row["term_id"] for row in term_rows}) == len(term_rows),
            "duplicate terminology ID")
    require(len({row["event_id"] for row in adverse_rows}) == len(adverse_rows),
            "duplicate adverse ID")
    require(all(row["status"] == "admitted" for row in term_draft),
            "Unit 006 terminology not fully admitted")
    allowed = {
        "clarified_in_translation",
        "corrected_in_translation",
        "hypothesis_repaired_in_translation",
        "proof_completed_in_translation",
        "resolved_before_admission",
    }
    require(all(row["status"] in allowed for row in adverse_draft),
            "Unit 006 adverse status mismatch")
    return {
        "identities": identities,
        "terminology": {
            "rows": len(term_rows),
            "unit_rows": len(term_draft),
            "first_unit_id": term_draft[0]["term_id"],
            "terminal_id": term_draft[-1]["term_id"],
            "unit_tail_matches_reviewed_draft": True,
        },
        "adverse": {
            "rows": len(adverse_rows),
            "unit_rows": len(adverse_draft),
            "first_unit_id": adverse_draft[0]["event_id"],
            "terminal_id": adverse_draft[-1]["event_id"],
            "unit_tail_matches_reviewed_draft": True,
        },
    }


def verify_review(reader_sha: str) -> dict[str, Any]:
    raw, text = strict_text(REVIEW_PATH)
    try:
        review = json.loads(text)
    except json.JSONDecodeError as exc:
        die(f"independent review malformed ({exc})")
    require(review.get("status") == "PASS_P1_P2_P3_ZERO",
            "independent review not final PASS")
    require(review.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0},
            "independent review severity census not zero")
    require(review.get("canonical", {}).get("sha256") == reader_sha,
            "independent review canonical hash mismatch")
    require(
        review.get("upstream", {}).get("selected_span", {}).get("sha256")
        == SPAN_IDENTITY["sha256"],
            "independent review source-span hash mismatch")
    require(review.get("canonical_or_asset_mutations_by_reviewer") == 0,
            "independent review was not read-only")
    require(review.get("git_invoked_by_reviewer") is False,
            "independent review invoked Git")
    require(review.get("browser_or_network_invoked_by_reviewer") is False,
            "independent review invoked network access")
    return {
        "identity": identity(REVIEW_PATH, raw),
        "status": review["status"],
        "severity_census": review["severity_census"],
    }


def verify_assets(reader_text: str, nodes: list[dict[str, Any]]) -> dict[str, Any]:
    root = LANE / ASSET_DIR
    require(root.is_dir(), f"missing {ASSET_DIR}")
    files = sorted(path for path in root.iterdir() if path.is_file())
    require(all(path.suffix.lower() in {".svg", ".png"} for path in files),
            "Unit 006 asset directory contains an unexpected file type")
    svg_files = [path for path in files if path.suffix.lower() == ".svg"]
    png_files = [path for path in files if path.suffix.lower() == ".png"]
    require(len(svg_files) == EXPECTED_SVG_FILES,
            f"SVG file count={len(svg_files)}, expected {EXPECTED_SVG_FILES}")
    require(not png_files or (
        len(png_files) == EXPECTED_SVG_FILES
        and {path.stem for path in png_files} == {path.stem for path in svg_files}
    ), "PNG fallbacks, when present, must be one-to-one with the seven SVGs")
    identities: list[dict[str, Any]] = []
    for path in svg_files:
        raw = path.read_bytes()
        require(not raw.startswith(b"\xef\xbb\xbf"), f"{path.name}: BOM forbidden")
        require(b"\r" not in raw, f"{path.name}: CR/CRLF forbidden")
        require(raw.endswith(b"\n"), f"{path.name}: terminal LF required")
        require(b"<script" not in raw.lower(), f"{path.name}: script forbidden")
        try:
            svg = ET.fromstring(raw.decode("utf-8", errors="strict"))
        except (UnicodeDecodeError, ET.ParseError) as exc:
            die(f"{path.name}: invalid SVG/XML ({exc})")
        require(svg.tag.endswith("svg"), f"{path.name}: SVG root missing")
        for element in svg.iter():
            for key, value in element.attrib.items():
                if key.endswith("href"):
                    require(not re.match(r"(?i)https?://", value),
                            f"{path.name}: external href forbidden")
        require("viewBox" in svg.attrib, f"{path.name}: viewBox missing")
        require(svg.attrib.get("role") == "img", f"{path.name}: role=img missing")
        title = next((item for item in svg.iter() if item.tag.endswith("title")), None)
        desc = next((item for item in svg.iter() if item.tag.endswith("desc")), None)
        require(title is not None and (title.text or "").strip(),
                f"{path.name}: nonempty title missing")
        require(desc is not None and (desc.text or "").strip(),
                f"{path.name}: nonempty description missing")
        identities.append({
            "path": f"{ASSET_DIR}/{path.name}",
            "bytes": len(raw),
            "sha256": sha256(raw),
            "media_type": "image/svg+xml",
        })

    for path in png_files:
        raw = path.read_bytes()
        require(raw.startswith(b"\x89PNG\r\n\x1a\n"),
                f"{path.name}: PNG signature missing")
        require(len(raw) >= 24 and raw[12:16] == b"IHDR",
                f"{path.name}: PNG IHDR missing")
        width = int.from_bytes(raw[16:20], "big")
        height = int.from_bytes(raw[20:24], "big")
        require(width > 0 and height > 0, f"{path.name}: invalid dimensions")
        identities.append({
            "path": f"{ASSET_DIR}/{path.name}",
            "bytes": len(raw),
            "sha256": sha256(raw),
            "media_type": "image/png",
            "dimensions": [width, height],
        })

    refs = re.findall(
        r"!\[([^\]\r\n]+)\]\((\.\./assets/unit-006/([^\s)]+\.(?:svg|png)))\)",
        reader_text,
    )
    require(len(refs) == EXPECTED_SVG_FILES,
            f"reader SVG reference count={len(refs)}, expected {EXPECTED_SVG_FILES}")
    require(all(alt.strip() for alt, _, _ in refs), "empty SVG alt text")
    ref_names = [name for _, _, name in refs]
    require(len(set(ref_names)) == EXPECTED_SVG_FILES,
            "SVG reader references must be one-to-one")
    require({Path(name).stem for name in ref_names} == {path.stem for path in svg_files},
            "reader references and SVG semantic redraws differ")
    figures = [node for node in nodes if node["kind"] == "figure"]
    require(len(figures) == EXPECTED_SVG_FILES,
            f"semantic figure count={len(figures)}, expected {EXPECTED_SVG_FILES}")
    require(all(node["attrs"].get("data-origin") == "edition-original-redraw"
                for node in figures), "semantic redraw provenance missing")
    return {
        "files": sorted(identities, key=lambda item: item["path"]),
        "svg_files": len(svg_files),
        "png_fallbacks": len(png_files),
        "reader_references": [path for _, path, _ in refs],
        "accessible_alt_texts": EXPECTED_SVG_FILES,
        "semantic_figures": len(figures),
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
    require(not native.stderr.strip() and not html.stderr.strip(),
            "Pandoc emitted warnings")
    math_count = html.stdout.count("<math")
    require(math_count >= 40, f"Pandoc MathML count unexpectedly low ({math_count})")
    return {
        "version": version.stdout.splitlines()[0].strip(),
        "native_parse": "PASS",
        "mathml_render": "PASS",
        "mathml_nodes": math_count,
        "display_mathml_nodes": html.stdout.count('<math display="block"'),
        "warnings": 0,
    }


def source_kind_counts(nodes: list[dict[str, Any]]) -> Counter[str]:
    return Counter(
        node["kind"] for node in nodes
        if node["kind"] in SOURCE_ENVIRONMENT_COUNTS
        and node["attrs"].get("data-origin") == "source-derived"
    )


def verify_source_environment_coverage(
    nodes: list[dict[str, Any]], source: dict[str, Any]
) -> None:
    source_nodes = [
        node for node in nodes
        if node["kind"] in SOURCE_ENVIRONMENT_COUNTS
        and node["attrs"].get("data-origin") == "source-derived"
    ]
    for node in source_nodes:
        require("data-source-lines" in node["attrs"],
                f"{node['id']}: source-derived environment lacks locator")
    for expected in source["mathematical_environment_spans"]:
        matches = []
        for node in source_nodes:
            if node["kind"] != expected["kind"]:
                continue
            ranges = parse_source_locator(node["attrs"]["data-source-lines"], node["id"])
            if any(start <= expected["line_start"] and end >= expected["line_end"]
                   for start, end in ranges):
                matches.append(node["id"])
        require(len(matches) == 1,
                f"source {expected['kind']} {expected['line_start']}-{expected['line_end']} "
                f"represented {len(matches)} times")


def resolve_fragment_targets(text: str, own_ids: set[str]) -> dict[str, Any]:
    link_counts = Counter(re.findall(r"\]\(#([^)]+)\)", text))
    external_targets = {target for target in link_counts if target not in own_ids}
    if external_targets:
        prior_roots = (
            LANE / UNITS_DIR,
            LANE / "source/id-ID/units",
        )
        prior_text = "\n".join(
            path.read_text(encoding="utf-8")
            for unit_root in prior_roots
            for path in sorted(unit_root.iterdir())
            if path.is_file()
            and path.suffix == ".md"
            and path.name != Path(READER_PATH).name
        )
        for target in external_targets:
            require(f"#{target}" in prior_text,
                    f"unresolved prior-unit fragment #{target}")
    return {
        "count": sum(link_counts.values()),
        "distinct_targets": len(link_counts),
        "resolved": sum(link_counts.values()),
        "target_counts": dict(sorted(link_counts.items())),
    }


def verify_reader(source: dict[str, Any]) -> dict[str, Any]:
    raw, text = strict_text(READER_PATH)
    reader_identity = identity(READER_PATH, raw)
    nodes, opens, closes = parse_reader(text)
    ids = [node["id"] for node in nodes]
    require(ids and len(ids) == len(set(ids)), "stable ID count/uniqueness mismatch")
    require(all(re.fullmatch(r"o012-fom-u006(?:-[a-z0-9-]+)?", ident)
                for ident in ids), "non-Unit-006 or non-locale-neutral stable ID")
    sequence_sha = sha256(("\n".join(ids) + "\n").encode("utf-8"))
    class_counts = Counter(node["kind"] for node in nodes)
    source_counts = source_kind_counts(nodes)
    require(dict(source_counts) == SOURCE_ENVIRONMENT_COUNTS,
            f"source-derived environment census mismatch: {dict(source_counts)}")
    verify_source_environment_coverage(nodes, source)

    locators: list[dict[str, Any]] = []
    for node in nodes:
        value = node["attrs"].get("data-source-lines")
        if value is not None:
            ranges = parse_source_locator(value, node["id"])
            locators.append({
                "id": node["id"], "value": value,
                "ranges": [list(item) for item in ranges],
            })
    require(locators, "source locators absent")
    aliases = {
        node["attrs"]["data-source-label"]: node["id"]
        for node in nodes if "data-source-label" in node["attrs"]
    }
    require(set(aliases) == SOURCE_LABELS, f"source alias mismatch: {aliases}")
    fragments = resolve_fragment_targets(text, set(ids))

    node_by_id = {node["id"]: node for node in nodes}
    for number in range(1, EXPECTED_MASTERY_TRIPLES + 1):
        suffix = f"{number:03d}"
        exercise = node_by_id.get(f"o012-fom-u006-mcheck-{suffix}")
        hint = node_by_id.get(f"o012-fom-u006-hint-{suffix}")
        solution = node_by_id.get(f"o012-fom-u006-sol-{suffix}")
        require(exercise is not None and hint is not None and solution is not None,
                f"mastery triple {suffix} incomplete")
        expected_origin = "source-derived" if number == 1 else "edition-original"
        require(exercise["attrs"].get("data-origin") == expected_origin,
                f"mastery exercise {suffix}: provenance mismatch")
        require(exercise["attrs"].get("data-course-route-unit-id") == "D60-R12",
                f"mastery exercise {suffix}: route mismatch")
        require(exercise["line_start"] < hint["line_start"] < solution["line_start"],
                f"mastery triple {suffix} order invalid")
        require(solution["line_end"] - solution["line_start"] >= 8,
                f"solution {suffix} is not complete enough for admission")

    source_exercises = [
        node for node in nodes
        if node["kind"] == "exercise"
        and node["attrs"].get("data-origin") == "source-derived"
    ]
    require(len(source_exercises) == 1, "source exercise count mismatch")
    require(source_exercises[0]["attrs"].get("data-source-label") == "ex:cw-for-cp",
            "source CP^n exercise alias mismatch")

    required = [
        "Creative Commons Attribution-ShareAlike 4.0 International",
        MODEL,
        "Tidak ada prosa dari bank soal Fomberg terpisah",
        "tidak menyiratkan dukungan, pengesahan, atau",
        "afiliasi dengan Yeheli Fomberg",
        'edition_unit_id: "O012-FOM-006"',
        'course_route_unit_id: "D60-R12"',
        "lang: id-ID",
    ]
    flat_text = " ".join(text.split())
    for phrase in required:
        require(phrase in text or phrase in flat_text,
                f"required marker absent: {phrase}")
    forbidden = [
        "Translation and Transcription Project", "TTP", "C:\\Users\\",
        "AppData", "github_pat_", "ghp_", "Bearer ", "api_token",
    ]
    for phrase in forbidden:
        require(phrase not in text, f"forbidden/private string present: {phrase}")
    require("$$" in text, "mathematics surface unexpectedly absent")
    allowed_origins = {"source-derived", "edition-original", "edition-original-redraw"}
    origins = set(re.findall(r'data-origin="([^"]+)"', text))
    require(origins <= allowed_origins and {"source-derived", "edition-original"} <= origins,
            f"uncontrolled provenance value: {sorted(origins)}")

    term_rows = list(csv.DictReader((LANE / TERM_DRAFT_PATH).read_text(
        encoding="utf-8"
    ).splitlines()))
    folded_text = text.casefold()
    for row in term_rows:
        require(row["id_ID"].casefold() in folded_text,
                f"terminology evidence lacks admitted form: {row['term_id']}")

    assets = verify_assets(text, nodes)
    pandoc = verify_pandoc()
    return {
        "identity": reader_identity,
        "stable_ids": len(ids),
        "stable_ids_unique": len(set(ids)),
        "ordered_stable_ids_sha256": sequence_sha,
        "semantic_class_counts": dict(sorted(class_counts.items())),
        "source_derived_environment_counts": dict(sorted(source_counts.items())),
        "fenced_divs": {"opened": opens, "closed": closes, "balanced": True},
        "source_locators": {"count": len(locators), "valid": len(locators)},
        "source_aliases": dict(sorted(aliases.items())),
        "fragment_links": fragments,
        "mastery": {
            "exercise_hint_solution_triples": EXPECTED_MASTERY_TRIPLES,
            "complete_solutions": EXPECTED_MASTERY_TRIPLES,
            "source_exercises_preserved": 1,
        },
        "assets": assets,
        "pandoc": pandoc,
        "rights_provenance_privacy": "PASS",
    }


def main() -> None:
    source = verify_source()
    controls = verify_controls()
    reader = verify_reader(source)
    review = verify_review(reader["identity"]["sha256"])

    audit = {
        "schema_version": "1.0.0",
        "audit_id": "O012-FOMBERG-UNIT-006-SOURCE-AUDIT",
        "date": DATE,
        "status": "PASS",
        "role_id": "O012",
        "course_id": "D60",
        "edition_unit_id": "O012-FOM-006",
        "course_route_unit_id": "D60-R12",
        "component": "Fomberg Algebraic Topology Section 1.12: Cellular complexes",
        "license": "CC BY-SA 4.0",
        "model_provenance": MODEL,
        "source": source,
        "reader": reader["identity"],
        "translation_closure": {
            "contiguous_span": "3123-3517",
            "subsections_complete_in_source_order": 1,
            "source_mathematical_environments_represented": SOURCE_ENVIRONMENT_TOTAL,
            "source_exercises_preserved": 1,
            "mastery_triples_complete": EXPECTED_MASTERY_TRIPLES,
            "accessible_svg_redraws": EXPECTED_SVG_FILES,
            "next_exact_cursor": NEXT_LINE,
            "next_exact_text": NEXT_TEXT,
        },
        "correction_and_terminology_ledgers": controls,
        "independent_review": review,
    }
    audit_raw = receipt_bytes(audit)
    AUDIT_OUTPUT.write_bytes(audit_raw)

    qa = {
        "schema_version": "1.0.0",
        "qa_id": "O012-FOMBERG-UNIT-006-STATIC-QA",
        "date": DATE,
        "status": "PASS",
        "model_provenance": MODEL,
        "source_audit": {
            "path": "qa/FOMBERG_UNIT_006_SOURCE_AUDIT.json",
            "bytes": len(audit_raw),
            "sha256": sha256(audit_raw),
        },
        "source": source,
        "reader": reader,
        "controls": controls,
        "independent_review": review,
        "gates": {
            "source_identity_contiguity_and_environment_census": "PASS",
            "source_order_labels_and_exact_next_cursor": "PASS",
            "stable_structure_locators_aliases_and_links": "PASS",
            "source_exercise_and_mastery_solution_closure": "PASS",
            "terminology_and_correction_ledgers": "PASS",
            "seven_accessible_svg_redraws": "PASS",
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
        "source_environments": SOURCE_ENVIRONMENT_TOTAL,
        "source_exercises": 1,
        "mastery_triples": EXPECTED_MASTERY_TRIPLES,
        "svg_redraws": EXPECTED_SVG_FILES,
    }, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
