#!/usr/bin/env python3
"""Shared frozen inputs and deterministic record construction for Fomberg Unit 001."""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
SCHEMA = "curriculum.interop"
VERSION = "0.1.0"
WORKFLOW = "o012-d60-id-reader-production"
STAMP = "2026-08-24T00:00:00Z"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"

SOURCE_PATH = "source/id-ID/fomberg/units/fomberg-unit-001-delta-complexes-simplicial-homology.md"
SOURCE = LANE / SOURCE_PATH
SOURCE_IDENTITY = (34773, 1073, "d9b64140f9340c75bc34c12bc02ee843d87de3566e331c50c2374075718aa2c6")
UPSTREAM_PATH = ("authority/upstream/math-notes-563194fae879178b9a6871b249513bfc27968975/"
                 "tree/algebraic_topology.tex")
UPSTREAM = LANE / UPSTREAM_PATH
UPSTREAM_IDENTITY = (223886, 6069, "d27095de0f38f0c14b2d7716cb52d51d064f0594dd9f82f9d1b3e6af5b35a483")
SPAN_IDENTITY = (31, 614, 584, 21875,
                 "68cb0dea7aa24a42e979877a95acf61b8152c87ed86d88ad7deac7cb5cea2fe3")
NEXT_SOURCE_LINE = 615
NEXT_HEADING = r"\subsection{Singular homology}"
COMMIT = "563194fae879178b9a6871b249513bfc27968975"
TREE = "fb678966d1533d529bdd72f49d8496a3bdc14a9b"
RESOURCE = "resource:fomberg-algebraic-topology-2025"
EDITION = "edition:fomberg-at-2025-563194f"
ROOT = "unit:o012-fom-u001"
PROGRAM = "program:o012-id"
COURSE = "course:o012-d60"
ROUTE = "D60-R08"

SOURCE_RIGHTS = "rights:fomberg-cc-by-sa-4.0"
OVERLAY_RIGHTS = "rights:fomberg-build-overlay-cc0-1.0"
COMPANION_RIGHTS = "rights:o012-fom-u001-companion-cc-by-sa-4.0"
COMPOSITE_RIGHTS = "rights:o012-fom-u001-composite-cc-by-sa-4.0"
ROUTE_RIGHTS = "rights:o012-d60-integrated-route-cc-by-sa-4.0"

PREFIX = {
    "artifacts.jsonl": (160, 128377, "dcafca44e0fdd9daea5534f9cb6e12ddc85d66e83657cf7905f0c76287d99356"),
    "assets.jsonl": (34, 21271, "70623b74c22df743708785dd6a213d8086dd4280db983ea14b8f08075b3e8ee6"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (364, 114998, "0ba79f3eb7f33775e2fc1e9897de40652522ebb426688617521f226cf5ee159b"),
    "corrections.jsonl": (407, 397287, "39c7fbc05989e947f4de409ef43b50f55534fecb04d6c662501401c3e295d0d8"),
    "qa.jsonl": (134, 75118, "2cdfe9c1a159e2d6b1c80e158b16a991814983f07d704c30776c2ccc54108706"),
    "relations.jsonl": (533, 218443, "cc56f5be615b567baf381505a883b6dd2344f8eaf1318f3f0ec4f5b4d70c418e"),
    "rights.jsonl": (86, 79588, "2540e545302261e342f8a41211295e7c435e870ad52e267485d4a66f5b439d0e"),
    "segments.jsonl": (1326, 1912371, "054699f1e9d902de23f5dff26d3ecee7b7e1da502fb971468bb17975c7ca65eb"),
    "terms.jsonl": (357, 226725, "27c19bbacd1fd21fc371b29c64cf7e3b1f37bae6472e3670697830a98279c67f"),
    "units.jsonl": (1356, 2036780, "53b5f8d6a688a71bc7f38f80bda670141109b974742dec7e9428ad43de0f495e"),
}
PREFIX_TOTAL = (4761, 5213679,
                "51b8c7f611560b9b5e88e97b3a943b54e0eb687c703f0cd34c1a3d164e4fb920")
DELTA = {"artifacts.jsonl": 6, "assets.jsonl": 3, "authority.jsonl": 2,
         "concepts.jsonl": 28, "corrections.jsonl": 18, "qa.jsonl": 4,
         "relations.jsonl": 31, "rights.jsonl": 5, "segments.jsonl": 87,
         "terms.jsonl": 28, "units.jsonl": 87}

IDENTITIES = {
    "qa/FOMBERG_UNIT_001_SOURCE_AUDIT.md": (16794, "4157bfcfc12502d5fd56fb55cd162f3b45dae40eee2c5319cc7a8f245bb88e3a"),
    "qa/FOMBERG_UNIT_001_SOURCE_AUDIT.json": (4513, "f8706a32f0bf7cdb0695d9d70e808dd0b03dfa2af6a6c40bd3817b9c4a7956b0"),
    "qa/FOMBERG_UNIT_001_BACKEND_CONTRACT.md": (15828, "cefce9ba4188f36d9e0714ef9065effb5fc12608ce69826de8b5bdfccbaf4943"),
    "qa/FOMBERG_UNIT_001_INDEPENDENT_REVIEW.md": (12357, "ec505152bed5690e77beb85039404c4a4b2dc23b14967e0f77b09f05bde06b68"),
    "00_control/ADVERSE_LEDGER.csv": (135323, "4f7e75e9b556ccdb0fa2ad358600ca8be3bdc2b27e86a9f04d0619c01f46aee4"),
    "00_control/TERMINOLOGY.csv": (46554, "3fb35df5fe6746ac782bfc4f16c19b152d48982f225797a3b9910610a3d42d53"),
    "00_control/CURRICULUM_ROUTE_AND_FOMBERG_HANDOFF.md": (8115, "0faecfb535065cff3ac88eb0e59b55ff311981535a842e32981ca499eb4228d3"),
    "qa/FOMBERG_AUTHORITY_BUILD_GATE_QA.json": (3402, "110ae5058f254f780812fa12e51e73cc6d1f1e6e03a319dbdfb18ecedf79fe71"),
    "qa/FOMBERG_AUTHORITY_BUILD_GATE_VISUAL_QA.md": (2698, "bdc4609eedb03aa30fc1841f2f65415e034189cbae8f4e022615b59d2b34ccb7"),
    "qa/FOMBERG_AUTHORITY_BUILD_GATE_FILE_MANIFEST.csv": (3170, "51da0c57ee1c9c9337e16aca8df54a69602965188f0c39ebf2c44c3dc4175129"),
    "qa/BACKEND_APPEND_ONLY_UNIT_030_CUMULATIVE_RECEIPT.json": (3976, "d4f7c7310ae22b8fc53d354b72beefad637ac353be418b9fbc56ddd8cd0a65f7"),
    UPSTREAM_PATH: (223886, "d27095de0f38f0c14b2d7716cb52d51d064f0594dd9f82f9d1b3e6af5b35a483"),
    "authority/upstream/math-notes-563194fae879178b9a6871b249513bfc27968975/tree/header.tex": (14097, "7c4c5cbe901c1b6c7ae8d6053d42cd28110ece34dd90bc60c5bcb7423e45e28e"),
    "authority/upstream/math-notes-563194fae879178b9a6871b249513bfc27968975/tree/LICENSE": (20140, "0b7fc2608b6d990314e908569407a6058b4a29175167c6d91ca0070c946661be"),
    "authority/upstream/math-notes-563194fae879178b9a6871b249513bfc27968975/build-overlay/commath.sty": (1346, "524c17aef50ed58686c9ed0b0b274e7f2ccdb35380869fef9c66ce3a120a6d19"),
    "authority/upstream/math-notes-563194fae879178b9a6871b249513bfc27968975/archive/math-notes-563194fae879178b9a6871b249513bfc27968975.tar.gz": (2236609, "423c2c34b62a1b443e63be72e80a5c35d5cd6daf4e5b3be8e48dad1d1f897443"),
}

ALIASES = {
    "def:sigma-complex": "o012-fom-u001-def-delta-complex",
    "exmp:delta-complex-rp2": "o012-fom-u001-exa-rp2",
    "rem:order": "o012-fom-u001-rem-order",
    "def:simplicial-complex": "o012-fom-u001-def-simplicial-complex",
    "lem:partial-partial-zero": "o012-fom-u001-lem-boundary-square",
}

TERM_SLUGS = (
    "path-connected-component", "based-map", "based-homotopy-class",
    "affinely-independent", "convex-hull", "barycentric-map", "simplex",
    "simplex-face", "vertex", "delta-complex", "simplicial-complex",
    "simplicial-homology", "chain", "boundary-map", "boundary-of-a-simplex",
    "chain-boundary", "cycle", "homologous", "homology-class", "homology",
    "free-abelian-group", "barycentric-coordinates", "characteristic-map",
    "orientation", "abelianization", "nonexample", "singular-homology",
    "comparison-theorem",
)
TERM_EVIDENCE = (
    "rem-001", "audit-pi-n", "audit-pi-n", "def-001", "def-002", "def-004",
    "def-002", "def-005", "def-delta-complex", "def-delta-complex",
    "def-simplicial-complex", "s02", "def-007", "def-boundary", "def-006",
    "def-009", "def-008", "def-011", "def-010", "def-010", "def-007",
    "def-004", "def-delta-complex", "rem-order", "rem-013", "exa-005",
    "rem-013", "rem-013",
)
CORRECTION_TARGETS = {
    408: ("audit-pi-n",), 409: ("audit-affine-ambient",),
    410: ("audit-001", "def-003", "def-004", "def-005", "audit-002"),
    411: ("audit-003", "exa-torus", "exa-rp2"), 412: ("audit-005", "def-007", "def-boundary"),
    413: ("audit-006", "audit-007", "exa-007", "exa-008"),
    414: ("audit-face-sign", "rem-012"),
    415: ("proof-001", "lem-boundary-square", "audit-008"),
    416: ("def-009", "def-010", "def-011", "audit-009"),
    417: ("fig-010",), 418: ("rem-013", "audit-010"),
    419: ("rem-001", "exa-circle", "rem-order", "rem-007", "rem-008", "rem-009", "exa-008", "def-011"),
    420: ("rem-012", "audit-face-sign"), 421: ("fig-001", "fig-006", "fig-008"),
    422: ("fig-002", "fig-003"), 423: ("rem-013", "audit-010"),
    424: ("def-011", "audit-009"), 425: ("rem-003", "exa-005", "fig-005"),
}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8") + b"\n"


def common(kind: str, ident: str) -> dict[str, Any]:
    return {"entity_type": kind, "id": ident, "schema": SCHEMA,
            "schema_version": VERSION, "status": "active", "supersedes": None,
            "timestamp": STAMP, "workflow": WORKFLOW}


def file_identity(relative: str) -> dict[str, Any]:
    raw = (LANE / relative).read_bytes()
    return {"path": relative, "bytes": len(raw), "lines": raw.count(b"\n"),
            "sha256": digest(raw)}


def require_identity(relative: str, expected: tuple[int, str]) -> bytes:
    raw = (LANE / relative).read_bytes()
    if (len(raw), digest(raw)) != expected:
        raise SystemExit(f"frozen input identity mismatch: {relative}")
    return raw


def verify_prefix(backend: Path = BACKEND) -> tuple[dict[str, bytes], list[dict[str, Any]]]:
    prefix: dict[str, bytes] = {}; records: list[dict[str, Any]] = []
    seen: set[str] = set(); bundle = hashlib.sha256()
    for name in FILES:
        live = (backend / name).read_bytes(); count, size, sha = PREFIX[name]
        if len(live) < size:
            raise SystemExit(f"{name}: shorter than immutable Unit 30 prefix")
        raw = live[:size]
        if (len(raw), len(raw.splitlines()), digest(raw)) != (size, count, sha):
            raise SystemExit(f"{name}: immutable Unit 30 prefix mismatch")
        if b"\r" in raw or not raw.endswith(b"\n"):
            raise SystemExit(f"{name}: invalid prefix LF discipline")
        for number, line in enumerate(raw.splitlines(keepends=True), 1):
            obj = json.loads(line.decode("utf-8"))
            if canon(obj) != line or obj["id"] in seen:
                raise SystemExit(f"{name}:{number}: noncanonical/duplicate prefix")
            seen.add(obj["id"]); records.append(obj)
        prefix[name] = raw
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(raw)
    if (len(records), sum(map(len, prefix.values())), bundle.hexdigest()) != PREFIX_TOTAL:
        raise SystemExit("immutable Unit 30 bundle identity mismatch")
    return prefix, records


def _attrs(text: str) -> dict[str, str]:
    return {m.group(1): m.group(2) for m in re.finditer(r'(data-[a-z-]+)="([^"]*)"', text)}


def parse_reader() -> tuple[list[str], list[dict[str, Any]]]:
    raw = SOURCE.read_bytes()
    if (len(raw), raw.count(b"\n"), digest(raw)) != SOURCE_IDENTITY:
        raise SystemExit("Fomberg Unit 001 reader identity mismatch")
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n"):
        raise SystemExit("reader must be UTF-8 without BOM and LF-only")
    text = raw.decode("utf-8")
    if "\ufffd" in text or text.count(MODEL) != 1:
        raise SystemExit("reader encoding/model-provenance mismatch")
    lines = text.splitlines()
    nodes: list[dict[str, Any]] = []
    heading_re = re.compile(r'^(#{1,6})\s+(.*?)\s*\{([^}]*)\}\s*$')
    for number, line in enumerate(lines, 1):
        match = heading_re.match(line)
        if not match:
            continue
        ident = re.search(r'#(o012-fom-u001(?:-[A-Za-z0-9-]+)?)', match.group(3))
        if ident:
            nodes.append({"id": ident.group(1), "kind": "heading", "line_start": number,
                          "level": len(match.group(1)), "title": match.group(2),
                          "attrs": _attrs(match.group(3)), "opener_end": number})
    stack: list[dict[str, Any] | None] = []
    number = 1
    while number <= len(lines):
        stripped = lines[number - 1].strip()
        if stripped.startswith(":::") and stripped != ":::":
            opener_start = number; opener = [lines[number - 1]]
            while "}" not in opener[-1] and number < len(lines):
                number += 1; opener.append(lines[number - 1])
            joined = " ".join(opener)
            ident = re.search(r'#(o012-fom-u001(?:-[A-Za-z0-9-]+)?)', joined)
            kind = re.match(r'^:::\s*\{\.([^\s}]+)', opener[0].strip())
            node = None
            if ident and kind:
                node = {"id": ident.group(1), "kind": kind.group(1),
                        "line_start": opener_start, "opener_end": number,
                        "attrs": _attrs(joined)}
            stack.append(node)
        elif stripped == ":::":
            if not stack:
                raise SystemExit(f"reader unexpected fenced-div close at line {number}")
            node = stack.pop()
            if node:
                node["line_end"] = number
                body = [item.strip() for item in lines[node["opener_end"]:number - 1]
                        if item.strip()]
                node["title"] = body[0] if body else node["kind"]
                nodes.append(node)
        number += 1
    if stack:
        raise SystemExit("reader has unclosed fenced div")
    nodes.sort(key=lambda item: (item["line_start"], 0 if item["kind"] == "heading" else 1))
    heading_ends = {"o012-fom-u001-notice": 39, "o012-fom-u001": 835,
                    "o012-fom-u001-s01": 438, "o012-fom-u001-s02": 835,
                    "o012-fom-u001-mastery": 1067}
    for node in nodes:
        if node["kind"] == "heading":
            node["line_end"] = heading_ends[node["id"]]
    ids = [node["id"] for node in nodes]
    classes = Counter(node["kind"] for node in nodes)
    expected_classes = {"heading": 5, "remark": 14, "source-audit": 12,
                        "definition": 14, "example": 10, "figure": 10,
                        "lemma": 1, "proof": 1, "corollary": 1,
                        "exercise": 6, "hint": 6, "solution": 6, "boundary": 1}
    if len(ids) != 87 or len(set(ids)) != 87 or dict(classes) != expected_classes:
        raise SystemExit(f"reader stable-ID/class census mismatch: {len(ids)}, {dict(classes)}")
    if [node["id"] for node in nodes if node["kind"] == "heading"] != [
            "o012-fom-u001-notice", "o012-fom-u001", "o012-fom-u001-s01",
            "o012-fom-u001-s02", "o012-fom-u001-mastery"]:
        raise SystemExit("actual heading identity/order mismatch")
    actual_aliases = {node["attrs"].get("data-source-label"): node["id"] for node in nodes
                      if node["attrs"].get("data-source-label")}
    if actual_aliases != ALIASES:
        raise SystemExit(f"source alias mismatch: {actual_aliases}")
    return lines, nodes


def verify_upstream() -> None:
    raw = UPSTREAM.read_bytes()
    if (len(raw), raw.count(b"\n"), digest(raw)) != UPSTREAM_IDENTITY:
        raise SystemExit("frozen Fomberg authoring source mismatch")
    lines = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").splitlines()
    start, end, line_count, size, sha = SPAN_IDENTITY
    span = ("\n".join(lines[start - 1:end]) + "\n").encode("utf-8")
    if (len(span.splitlines()), len(span), digest(span)) != (line_count, size, sha):
        raise SystemExit("Fomberg Unit 001 upstream span mismatch")
    if lines[NEXT_SOURCE_LINE - 1].strip() != NEXT_HEADING:
        raise SystemExit("Fomberg next-source cursor mismatch")


def read_controls() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    adverse = list(csv.DictReader((LANE / "00_control/ADVERSE_LEDGER.csv").read_text(encoding="utf-8").splitlines()))
    terms = list(csv.DictReader((LANE / "00_control/TERMINOLOGY.csv").read_text(encoding="utf-8").splitlines()))
    selected_adverse = [row for row in adverse if 408 <= int(row["event_id"].rsplit("-", 1)[1]) <= 425]
    selected_terms = [row for row in terms if 366 <= int(row["term_id"].rsplit("-", 1)[1]) <= 393]
    if ([row["event_id"] for row in selected_adverse] != [f"O012-ADV-{n:04d}" for n in range(408, 426)]
            or any(row["status"] not in {"corrected_in_translation", "proof_completed_in_translation",
                                         "clarified_in_translation", "resolved_before_admission"}
                   for row in selected_adverse)):
        raise SystemExit("adverse-ledger Unit 001 closure mismatch")
    if ([row["term_id"] for row in selected_terms] != [f"O012-TERM-{n:04d}" for n in range(366, 394)]
            or any(row["status"] != "admitted" for row in selected_terms)):
        raise SystemExit("terminology-ledger Unit 001 closure mismatch")
    return selected_adverse, selected_terms


def verify_all_inputs() -> dict[str, Any]:
    for relative, expected in IDENTITIES.items():
        require_identity(relative, expected)
    verify_upstream()
    gate = json.loads((LANE / "qa/FOMBERG_AUTHORITY_BUILD_GATE_QA.json").read_text(encoding="utf-8"))
    if (gate.get("status") != "PASS" or gate.get("admission_status") != "PASS"
            or gate.get("failed_checks") or len(gate.get("checks", {})) != 55
            or not all(gate["checks"].values())):
        raise SystemExit("55/55 Fomberg authority/build gate is not PASS")
    audit = json.loads((LANE / "qa/FOMBERG_UNIT_001_SOURCE_AUDIT.json").read_text(encoding="utf-8"))
    if (audit.get("unit", {}).get("next_line") != 615
            or audit.get("counts", {}).get("diagrams_total") != 14
            or audit.get("unit", {}).get("sha256_preserving_lf") != SPAN_IDENTITY[4]):
        raise SystemExit("Unit 001 source audit mismatch")
    review = (LANE / "qa/FOMBERG_UNIT_001_INDEPENDENT_REVIEW.md").read_text(encoding="utf-8")
    if 'FINAL_SEVERITY_COUNTS: {"P1":0,"P2":0,"P3":0}' not in review:
        raise SystemExit("independent review has nonzero or absent final severity counts")
    lines, nodes = parse_reader(); adverse, terms = read_controls()
    reader = "\n".join(lines) + "\n"
    required = [r"\sigma=[v_0,\ldots,v_n]\in C_n^\Delta(X)",
                r"(-1)^{p+q}", r"(-1)^{p+q-1}",
                r"B_n^\Delta(X)", r"\partial_{n+1}",
                r"B_n^\Delta(X)\subseteq Z_n^\Delta(X)",
                r"H_n^\Delta(X)", r"z_1-z_2\in B_n^\Delta(X)"]
    if any(item not in reader for item in required):
        raise SystemExit("proof repair or standard B_n convention mismatch")
    figures = [node for node in nodes if node["kind"] == "figure"]
    if len(figures) != 10 or [node["id"] for node in figures] != [f"o012-fom-u001-fig-{n:03d}" for n in range(1, 11)]:
        raise SystemExit("semantic figure-block inventory mismatch")
    for n in range(1, 7):
        if not all(f"o012-fom-u001-{kind}-{n:03d}" in {node["id"] for node in nodes}
                   for kind in ("mcheck", "hint", "sol")):
            raise SystemExit(f"mastery triple {n} missing")
    return {"lines": lines, "nodes": nodes, "adverse": adverse, "terms": terms,
            "gate": gate, "audit": audit}


def target_locator(lines: list[str], start: int, end: int) -> dict[str, Any]:
    raw_lines = SOURCE.read_bytes().splitlines(keepends=True)
    return {"path": SOURCE_PATH, "line_start": start, "line_end": end,
            "file_sha256": SOURCE_IDENTITY[2],
            "content_sha256": digest(b"".join(raw_lines[start - 1:end]))}


def source_locator(source_range: str | None) -> dict[str, Any]:
    if source_range:
        start, end = map(int, source_range.split("-"))
        return {"path": "algebraic_topology.tex", "commit_sha": COMMIT,
                "line_start": start, "line_end": end, "precision": "exact_source_span"}
    return {"kind": "edition_original", "path": SOURCE_PATH,
            "precision": "exact_target_span"}


def clean_title(title: str, kind: str) -> str:
    if title.startswith("data-"):
        return {"definition": "Definisi", "example": "Contoh", "remark": "Catatan",
                "lemma": "Lema"}.get(kind, kind)
    value = re.sub(r"\*\*", "", title).strip()
    return value[:240] if value else kind


def node_parentage(nodes: list[dict[str, Any]]) -> dict[str, tuple[str, int, list[str]]]:
    result: dict[str, tuple[str, int, list[str]]] = {}
    root_children = ["o012-fom-u001-notice", "o012-fom-u001-s01",
                     "o012-fom-u001-s02", "o012-fom-u001-mastery",
                     "o012-fom-u001-boundary-001"]
    for order, ident in enumerate(root_children, 1):
        result[ident] = (ROOT, order, [ROOT, f"unit:{ident}"])
    groups = (("o012-fom-u001-s01", 42, 438),
              ("o012-fom-u001-s02", 439, 835),
              ("o012-fom-u001-mastery", 836, 1067))
    for parent_local, start, end in groups:
        children = [node for node in nodes if node["kind"] != "heading"
                    and start <= node["line_start"] <= end]
        for order, node in enumerate(children, 1):
            result[node["id"]] = (f"unit:{parent_local}", order,
                                  [ROOT, f"unit:{parent_local}", f"unit:{node['id']}"])
    return result


def load_generic():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_fom001", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def build_additions(data: dict[str, Any], qa_identity: tuple[int, str]) -> dict[str, list[dict[str, Any]]]:
    lines: list[str] = data["lines"]; nodes: list[dict[str, Any]] = data["nodes"]
    additions: dict[str, list[dict[str, Any]]] = {name: [] for name in FILES}
    all_concepts = [f"concept:{slug}" for slug in TERM_SLUGS]

    def add(name: str, record: dict[str, Any]) -> None:
        additions[name].append(record)

    # Rights are component-scoped and deliberately preserve the Roberts/Fomberg split.
    rights_rows = (
        (SOURCE_RIGHTS, "Yeheli Fomberg, Algebraic Topology notes, based on lectures by Nir Lazarovich.",
         "Translated and adapted into Indonesian; source corrections and semantic diagram reflows are identified.",
         [RESOURCE, EDITION], "CC-BY-SA-4.0", "https://creativecommons.org/licenses/by-sa/4.0/",
         "Fomberg source component remains CC BY-SA 4.0."),
        (OVERLAY_RIGHTS, "commath.sty compatibility overlay dedicated to the public domain under CC0 1.0.",
         "Build-only compatibility overlay; it does not alter the mathematical source.",
         ["asset:o012-fom-u001-build-overlay"], "CC0-1.0", "https://creativecommons.org/publicdomain/zero/1.0/",
         "Overlay-only rights; no source relicensing."),
        (COMPANION_RIGHTS, "Original Indonesian mastery, solutions, proof repair, audits, and accessibility descriptions.",
         "Original additions are distinguished from Fomberg source-derived content.", [ROOT],
         "CC-BY-SA-4.0", "https://creativecommons.org/licenses/by-sa/4.0/",
         "Original companion layer; source component remains separately attributed."),
        (COMPOSITE_RIGHTS, "Fomberg source adaptation plus original Indonesian Unit 001 companion layer.",
         "Integrated reader preserves component-level provenance and change notices.", [ROOT],
         "CC-BY-SA-4.0", "https://creativecommons.org/licenses/by-sa/4.0/",
         "Composite Unit 001; component-scoped rights records control."),
        (ROUTE_RIGHTS, "O012/D60 integrated route: Roberts CC BY 4.0; Fomberg and original layers CC BY-SA 4.0.",
         "The route arrangement is CC BY-SA 4.0 without relicensing the Roberts CC BY 4.0 component.", [COURSE, ROOT],
         "CC-BY-SA-4.0", "https://creativecommons.org/licenses/by-sa/4.0/",
         "Integrated-route arrangement; Roberts and Fomberg component licenses remain controlling."),
    )
    for ident, attribution, change, scope, expression, url, third in rights_rows:
        rec = common("rights", ident); rec.update(attribution=attribution, change_notice=change,
            component_scope=scope, license_expression=expression, license_url=url,
            non_endorsement="Independent Indonesian edition; no source-author or lecturer endorsement.",
            third_party_status=third); add("rights.jsonl", rec)

    resource = common("resource", RESOURCE); resource.update(
        author="Yeheli Fomberg; based on lectures by Nir Lazarovich",
        license_expression="CC-BY-SA-4.0", rights_component_id=SOURCE_RIGHTS,
        source_locale="en", source_url="https://git.sr.ht/~yp/math-notes",
        title="Algebraic Topology", translation_state="source_frozen",
        commit_sha=COMMIT, tree_sha=TREE)
    edition = common("edition", EDITION); edition.update(
        archive_bytes=2236609,
        archive_path="authority/upstream/math-notes-563194fae879178b9a6871b249513bfc27968975/archive/math-notes-563194fae879178b9a6871b249513bfc27968975.tar.gz",
        archive_sha256="423c2c34b62a1b443e63be72e80a5c35d5cd6daf4e5b3be8e48dad1d1f897443",
        commit_sha=COMMIT, tree_sha=TREE, local_derivative_unit_id=ROOT,
        local_derivative_unit_ids=[ROOT], resource_id=RESOURCE,
        rights_component_id=SOURCE_RIGHTS, source_line_start=31,
        source_line_end=4185, first_unit_line_end=614, source_path="algebraic_topology.tex",
        translation_state="source_frozen", tree_identity_status="commit_tree_archive_frozen")
    add("authority.jsonl", resource); add("authority.jsonl", edition)

    for slug, row, evidence in zip(TERM_SLUGS, data["terms"], TERM_EVIDENCE, strict=True):
        concept = common("concept", f"concept:{slug}"); concept.update(
            canonical_label=row["source_term"], domain=row["scope"], locale_neutral=True)
        term = common("term", f"term:{slug}:id-ID"); term.update(
            concept_id=f"concept:{slug}", evidence_segment_id=f"segment:o012-fom-u001-{evidence}",
            locale="id-ID", preferred=row["id_ID"], register="textbook",
            rejected_forms=[], rights_component_id=COMPOSITE_RIGHTS, scope_unit_id=ROOT,
            source_term=row["source_term"], terminology_control_id=row["term_id"],
            terminology_status=row["status"], usage_note=row["note"], variants=[])
        add("concepts.jsonl", concept); add("terms.jsonl", term)

    parentage = node_parentage(nodes)
    source_kinds = {"definition", "example", "remark", "figure", "lemma", "corollary"}
    node_by_id = {node["id"]: node for node in nodes}
    for node in nodes:
        ident = node["id"]; uid = f"unit:{ident}"; kind = node["kind"]
        source_range = node["attrs"].get("data-source-lines")
        is_root = ident == "o012-fom-u001"
        is_source = kind in source_kinds or ident in {"o012-fom-u001", "o012-fom-u001-s01", "o012-fom-u001-s02"}
        if kind == "proof": is_source = False
        rights = COMPOSITE_RIGHTS if is_root else (SOURCE_RIGHTS if is_source else COMPANION_RIGHTS)
        provenance = "composite_translated_and_original" if is_root else (
            "translated_adapted_from_upstream" if is_source else
            ("edition_original_proof_repair" if kind == "proof" else "edition_original"))
        if is_root:
            unit_target = target_locator(lines, 1, len(lines)); parent = COURSE; order = 31; path = [ROOT]
            display = "Topologi Aljabar — Komponen Fomberg Unit 001: Kompleks-Delta dan Homologi Simpleksial"
        else:
            unit_target = target_locator(lines, node["line_start"], node["line_end"])
            parent, order, path = parentage[ident]
            display = clean_title(node["title"], kind)
        unit_kind = "reader_unit" if is_root else ({"heading": "section"}.get(kind, kind.replace("-", "_")))
        unit = common("unit", uid); unit.update(
            component_source_commit=COMMIT, component_source_id=RESOURCE,
            concept_ids=all_concepts, course_id=COURSE, course_route_unit_id=ROUTE,
            display_title=display, edition_id=EDITION, edition_unit_id=ROOT,
            locale="id-ID", model_provenance=MODEL, order=order, parent_id=parent,
            path=path, program_id=PROGRAM, provenance_relation=provenance,
            resource_id=RESOURCE, rights_component_id=rights, source_local_id=ident,
            target_locator=unit_target, translation_state="structurally_verified",
            unit_kind=unit_kind)
        if is_root:
            unit.update(edition_order=1, route_order=8, source_locator={
                "path": "algebraic_topology.tex", "commit_sha": COMMIT,
                "line_start": 31, "line_end": 614, "precision": "exact_unit_span",
                "span_bytes": 21875, "span_sha256": SPAN_IDENTITY[4]})
        alias = node["attrs"].get("data-source-label")
        if alias: unit["source_aliases"] = [alias]
        if ident in {"o012-fom-u001-lem-boundary-square", "o012-fom-u001-proof-001"}:
            unit["repair_id"] = "FOM-U001-PR-001"
            unit["proof_status"] = ("complete_original_repair" if kind == "proof"
                                    else "statement_with_complete_repaired_proof")
        if ident == "o012-fom-u001-cor-001": unit["proof_status"] = "direct_from_boundary_square_zero"
        if ident in {"o012-fom-u001-def-009", "o012-fom-u001-cor-001",
                     "o012-fom-u001-def-010", "o012-fom-u001-def-011"}:
            unit["boundary_convention"] = "B_n=im(partial_{n+1})"
        if kind == "solution": unit["solution_status"] = "complete_checked_solution"
        add("units.jsonl", unit)

        segment_start = node["line_start"]; segment_end = node["line_end"]
        segment_rights = SOURCE_RIGHTS if ident == "o012-fom-u001" else rights
        segment_provenance = "translated_adapted_from_upstream" if ident == "o012-fom-u001" else provenance
        segment = common("segment", f"segment:{ident}"); segment.update(
            component_source_commit=COMMIT, component_source_id=RESOURCE,
            concept_ids=all_concepts, course_route_unit_id=ROUTE, edition_id=EDITION,
            edition_unit_id=ROOT, locale="id-ID", model_provenance=MODEL, order=order,
            provenance_relation=segment_provenance, resource_id=RESOURCE,
            rights_component_id=segment_rights,
            segment_kind=("source_heading" if ident == "o012-fom-u001" else unit_kind),
            source_local_id=ident,
            source_locator=({"path": "algebraic_topology.tex", "commit_sha": COMMIT,
                             "line_start": 31, "line_end": 614,
                             "precision": "exact_unit_span"}
                            if ident == "o012-fom-u001" else
                            source_locator(source_range if (is_source or kind == "proof") else None)),
            target_locator=target_locator(lines, segment_start, segment_end),
            translation_state="structurally_verified", unit_id=uid)
        if alias: segment["source_aliases"] = [alias]
        for key in ("repair_id", "proof_status", "boundary_convention", "solution_status"):
            if key in unit: segment[key] = unit[key]
        add("segments.jsonl", segment)

    # Assets.
    overlay_path = "authority/upstream/math-notes-563194fae879178b9a6871b249513bfc27968975/build-overlay/commath.sty"
    assets = (
        ("asset:o012-fom-u001-source-markdown", SOURCE_PATH, SOURCE_IDENTITY[0], SOURCE_IDENTITY[2],
         "text/markdown; charset=utf-8", "canonical_reader_source", COMPOSITE_RIGHTS, {}),
        ("asset:o012-fom-u001-semantic-diagram-layer", SOURCE_PATH, SOURCE_IDENTITY[0], SOURCE_IDENTITY[2],
         "text/markdown; charset=utf-8", "semantic_diagram_accessibility_layer", SOURCE_RIGHTS,
         {"source_diagram_count": 14, "semantic_figure_block_count": 10,
          "source_format_counts": {"tikzpicture": 6, "inline_tikz": 6, "tikzcd": 2},
          "semantic_unit_ids": [f"unit:o012-fom-u001-fig-{n:03d}" for n in range(1, 11)]}),
        ("asset:o012-fom-u001-build-overlay", overlay_path, 1346,
         "524c17aef50ed58686c9ed0b0b274e7f2ccdb35380869fef9c66ce3a120a6d19",
         "text/x-tex; charset=utf-8", "build_compatibility_overlay", OVERLAY_RIGHTS, {}),
    )
    for ident, path, size, sha, media, role, rights, extra in assets:
        rec = common("asset", ident); rec.update(bytes=size, edition_id=EDITION,
            media_type=media, path=path, resource_id=RESOURCE,
            rights_component_id=rights, role=role, sha256=sha, **extra); add("assets.jsonl", rec)

    qa_path = "qa/FOMBERG_UNIT_001_QA.json"
    evidence = (
        ("artifact:o012-fom-u001-authority-gate", "qa/FOMBERG_AUTHORITY_BUILD_GATE_QA.json", *IDENTITIES["qa/FOMBERG_AUTHORITY_BUILD_GATE_QA.json"], "application/json", ["qa:o012-fom-u001-authority-build"], "source_frozen"),
        ("artifact:o012-fom-u001-authority-visual", "qa/FOMBERG_AUTHORITY_BUILD_GATE_VISUAL_QA.md", *IDENTITIES["qa/FOMBERG_AUTHORITY_BUILD_GATE_VISUAL_QA.md"], "text/markdown; charset=utf-8", ["qa:o012-fom-u001-authority-build"], "visually_checked"),
        ("artifact:o012-fom-u001-authority-file-manifest", "qa/FOMBERG_AUTHORITY_BUILD_GATE_FILE_MANIFEST.csv", *IDENTITIES["qa/FOMBERG_AUTHORITY_BUILD_GATE_FILE_MANIFEST.csv"], "text/csv; charset=utf-8", ["qa:o012-fom-u001-authority-build"], "source_frozen"),
        ("artifact:o012-fom-u001-source-audit", "qa/FOMBERG_UNIT_001_SOURCE_AUDIT.md", *IDENTITIES["qa/FOMBERG_UNIT_001_SOURCE_AUDIT.md"], "text/markdown; charset=utf-8", ["qa:o012-fom-u001-source-integrity"], "source_frozen"),
        ("artifact:o012-fom-u001-independent-review", "qa/FOMBERG_UNIT_001_INDEPENDENT_REVIEW.md", *IDENTITIES["qa/FOMBERG_UNIT_001_INDEPENDENT_REVIEW.md"], "text/markdown; charset=utf-8", ["qa:o012-fom-u001-math", "qa:o012-fom-u001-language"], "mathematically_reviewed"),
        ("artifact:o012-fom-u001-qa", qa_path, qa_identity[0], qa_identity[1], "application/json", ["qa:o012-fom-u001-source-integrity", "qa:o012-fom-u001-language"], "built"),
    )
    for ident, path, size, sha, media, qa_ids, state in evidence:
        rec = common("artifact", ident); rec.update(bytes=size, locale="id-ID",
            manifest_artifact_id=None, media_type=media, path=path, qa_event_ids=qa_ids,
            rights_component_id=COMPOSITE_RIGHTS, sha256=sha,
            toolchain=("Fomberg Unit 001 evidence; algebraic_topology.tex:31-614; "
                       f"{SPAN_IDENTITY[4]}; {MODEL}; route D60-R08; semantic admission only."),
            translation_state=state, unit_id=ROOT); add("artifacts.jsonl", rec)

    qa_rows = (
        ("qa:o012-fom-u001-authority-build", "authority_build",
         "Official commit/tree/archive/source/header/license identities and 55/55 deterministic authority/build checks passed.",
         ["artifact:o012-fom-u001-authority-gate", "artifact:o012-fom-u001-authority-visual", "artifact:o012-fom-u001-authority-file-manifest"]),
        ("qa:o012-fom-u001-source-integrity", "source",
         "Exact 31-614 span, cursor 615, 87 IDs, five aliases, and 14 diagrams in ten semantic figure blocks passed.",
         ["artifact:o012-fom-u001-source-audit", "artifact:o012-fom-u001-qa"]),
        ("qa:o012-fom-u001-math", "math",
         "Independent review passed P1=P2=P3=0; FOM-U001-PR-001 and the standard B_n convention are complete.",
         ["artifact:o012-fom-u001-independent-review"]),
        ("qa:o012-fom-u001-language", "language",
         "Independent Indonesian review passed P1=P2=P3=0 after all pre-admission repairs.",
         ["artifact:o012-fom-u001-independent-review", "artifact:o012-fom-u001-qa"]),
    )
    for ident, kind, note, witnesses in qa_rows:
        rec = common("qa_event", ident); rec.update(note=note, qa_type=kind,
            result="passed", unit_id=ROOT, witness_artifact_ids=witnesses); add("qa.jsonl", rec)

    # Corrections are generated directly from the frozen adverse ledger.
    type_map = {415: "proof_completion", 417: "source_clarification", 419: "source_typo",
                421: "diagram_fidelity", 422: "accessibility_correction",
                424: "notation_correction", 425: "language_correction"}
    for row in data["adverse"]:
        number = int(row["event_id"].rsplit("-", 1)[1]); suffixes = CORRECTION_TARGETS[number]
        affected = [f"unit:o012-fom-u001-{suffix}" for suffix in suffixes]
        rec = common("correction", f"correction:o012-fom-u001-adv-{number:04d}"); rec.update(
            adverse_ledger_id=row["event_id"], affected_unit_ids=affected,
            correction_type=type_map.get(number, "mathematical_correction"),
            edition_id=EDITION, evidence=row["source_location"],
            evidence_segment_id=f"segment:o012-fom-u001-{suffixes[0]}",
            rationale=row["rationale"], resource_id=RESOURCE,
            source_defect=row["observed"], target_change=row["action"], unit_id=ROOT,
            upstream_report_disposition="not_contacted"); add("corrections.jsonl", rec)

    def relation(ident: str, from_id: str, to_id: str, kind: str, note: str, **extra: Any) -> None:
        rec = common("relation", ident); rec.update(from_id=from_id, to_id=to_id,
            relation_type=kind, note=note, **extra); add("relations.jsonl", rec)
    relation("relation:adapts:o012-fom-u001:fomberg-edition", ROOT, EDITION, "adapts", "Indonesian Unit 001 adapts the exact Fomberg lines 31-614 span.")
    relation("relation:contains:o012-d60:fomberg-u001", COURSE, ROOT, "contains", "Course route D60-R08 contains Fomberg Unit 001.", course_route_unit_id=ROUTE)
    relation("relation:precedes:o012-rbt-u019:o012-fom-u001", "unit:o012-rbt-u019", ROOT, "precedes", "Roberts D60-R07 terminus precedes the D60-R08 homology bridge.")
    relation("relation:contains:o012-d60-rights:fomberg-u001", ROUTE_RIGHTS, ROOT, "contains", "Integrated-route rights contain the Fomberg composite unit.")
    relation("relation:xref:o012-d60:integrated-rights", COURSE, ROUTE_RIGHTS, "xref", "Current route-rights pointer without mutating historic course authority.")
    relation("relation:precedes:o012-fom-u001:mastery", ROOT, "unit:o012-fom-u001-mastery", "precedes", "Translated source body precedes the original solved mastery layer.")
    relation("relation:depends-on:fomberg-edition:commath-overlay", EDITION, "asset:o012-fom-u001-build-overlay", "depends-on", "Frozen build uses the separately licensed CC0 compatibility overlay.")
    relation("relation:proves:o012-fom-u001-proof-001:boundary-square", "unit:o012-fom-u001-proof-001", "unit:o012-fom-u001-lem-boundary-square", "proves", "Complete proof repair FOM-U001-PR-001 proves boundary squared is zero.", repair_id="FOM-U001-PR-001")
    relation("relation:depends-on:o012-fom-u001-cor-001:boundary-square", "unit:o012-fom-u001-cor-001", "unit:o012-fom-u001-lem-boundary-square", "depends-on", "The boundary-subgroup corollary follows from the lemma.")
    for n in range(1, 7):
        relation(f"relation:hints:fom-u001-hint-{n:03d}:mcheck-{n:03d}",
                 f"unit:o012-fom-u001-hint-{n:03d}", f"unit:o012-fom-u001-mcheck-{n:03d}",
                 "hints", f"Hint for Fomberg Unit 001 mastery check {n}.")
        relation(f"relation:solves:fom-u001-sol-{n:03d}:mcheck-{n:03d}",
                 f"unit:o012-fom-u001-sol-{n:03d}", f"unit:o012-fom-u001-mcheck-{n:03d}",
                 "solves", f"Complete checked solution for Fomberg Unit 001 mastery check {n}.")
    for n in range(1, 11):
        relation(f"relation:illustrates:fom-u001-fig-{n:03d}:diagram-asset",
                 f"unit:o012-fom-u001-fig-{n:03d}", "asset:o012-fom-u001-semantic-diagram-layer",
                 "illustrates", f"Semantic figure block {n} preserves and accessibly describes its source diagram group.")

    for name, records in additions.items():
        records.sort(key=lambda item: item["id"])
        if len(records) != DELTA[name] or len({item["id"] for item in records}) != len(records):
            raise SystemExit(f"{name}: derived suffix count/ID mismatch ({len(records)} != {DELTA[name]})")
    return additions


def expected_ids(data: dict[str, Any], qa_identity: tuple[int, str]) -> dict[str, set[str]]:
    return {name: {item["id"] for item in records}
            for name, records in build_additions(data, qa_identity).items()}
