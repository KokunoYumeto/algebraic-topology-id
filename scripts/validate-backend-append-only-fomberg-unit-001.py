#!/usr/bin/env python3
"""Independent semantic validator for the Fomberg Unit 001 append-only suffix."""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
READER = LANE / "source/id-ID/fomberg/units/fomberg-unit-001-delta-complexes-simplicial-homology.md"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
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
FINAL = {
    "artifacts.jsonl": (166, 133601, "e1cc3611df5e84e465846d64623af7107709d93681049bcdae5ad01b314bc41f"),
    "assets.jsonl": (37, 23720, "a9cc6a83e0e7c771044f0984fefb32f3c0ee409b428bb626b043f6bff7264367"),
    "authority.jsonl": (6, 4374, "84c622f56dbbd5ba379361245ecfe07bc79c9f4fd6b18ba21b82b5f545211869"),
    "concepts.jsonl": (392, 123698, "e83c6047f4f934044bff8bb1a057d2db2ef4d878fad6a6ce9a54d1c490a194bf"),
    "corrections.jsonl": (425, 416934, "f0a124da975557b3871e5ce8fbe7226c595ff06a3357b4c5f8e13352e7038c54"),
    "qa.jsonl": (138, 77180, "98449c7de7856384cced4d4ed0bd5c0c01ea0bf7b292f679ba52ae8ccac83ce0"),
    "relations.jsonl": (564, 232018, "01047e8dd954fcbc0f8fbefaf8ae78415f1278d601de3ec733f4c20c9e895101"),
    "rights.jsonl": (91, 83493, "e81261979962c93827e0199126b7164dda25063f2700918697dc9ede54517053"),
    "segments.jsonl": (1413, 2094230, "6a6789c021494f6099c1e1b5b59edd9045fb08688b3ececda5d2f53000fb5a8c"),
    "terms.jsonl": (385, 246829, "c29a3f45f4e29b6741dc2fe6b70ea421f1edf1000a50e276d544aa731045fc8d"),
    "units.jsonl": (1443, 2222571, "ba9a464c3eb2ba995eca5b78e870c2d57f58896b86f94b54b40f8538106b954c"),
}
PREFIX_TOTAL = (4761, 5213679, "51b8c7f611560b9b5e88e97b3a943b54e0eb687c703f0cd34c1a3d164e4fb920")
FINAL_TOTAL = (5060, 5658648, "17f57575a062025e434e79f7f3797d05de1a41e520202521ae39a409d4b6450d")
DELTA = {name: FINAL[name][0] - PREFIX[name][0] for name in FILES}
READER_IDENTITY = (34773, 1073, "d9b64140f9340c75bc34c12bc02ee843d87de3566e331c50c2374075718aa2c6")
QA_IDENTITY = (21253, "b3b0ebc9430b80d45c64a6c528e0e36f46ca0d646a50e7b9c9c5d68285369b7a")
REVIEW_IDENTITY = (12357, "ec505152bed5690e77beb85039404c4a4b2dc23b14967e0f77b09f05bde06b68")
AUDIT_IDENTITY = (16794, "4157bfcfc12502d5fd56fb55cd162f3b45dae40eee2c5319cc7a8f245bb88e3a")
CONTRACT_IDENTITY = (15828, "cefce9ba4188f36d9e0714ef9065effb5fc12608ce69826de8b5bdfccbaf4943")
ADVERSE_IDENTITY = (135323, "4f7e75e9b556ccdb0fa2ad358600ca8be3bdc2b27e86a9f04d0619c01f46aee4")
TERMINOLOGY_IDENTITY = (46554, "3fb35df5fe6746ac782bfc4f16c19b152d48982f225797a3b9910610a3d42d53")
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
MANIFEST = LANE / "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_001_FILE_MANIFEST.csv"
RECEIPT = LANE / "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_001_RECEIPT.json"
HUMAN = LANE / "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_001_RECEIPT.md"

SLUGS = (
    "path-connected-component", "based-map", "based-homotopy-class", "affinely-independent",
    "convex-hull", "barycentric-map", "simplex", "simplex-face", "vertex", "delta-complex",
    "simplicial-complex", "simplicial-homology", "chain", "boundary-map",
    "boundary-of-a-simplex", "chain-boundary", "cycle", "homologous", "homology-class",
    "homology", "free-abelian-group", "barycentric-coordinates", "characteristic-map",
    "orientation", "abelianization", "nonexample", "singular-homology", "comparison-theorem",
)
ALIASES = {"def:sigma-complex": "o012-fom-u001-def-delta-complex",
           "exmp:delta-complex-rp2": "o012-fom-u001-exa-rp2",
           "rem:order": "o012-fom-u001-rem-order",
           "def:simplicial-complex": "o012-fom-u001-def-simplicial-complex",
           "lem:partial-partial-zero": "o012-fom-u001-lem-boundary-square"}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode() + b"\n"


def identity(path: Path, expected: tuple[int, str]) -> bytes:
    raw = path.read_bytes()
    if (len(raw), digest(raw)) != expected:
        raise SystemExit(f"identity mismatch: {path.relative_to(LANE).as_posix()}")
    return raw


def parse_reader() -> tuple[bytes, list[str], dict[str, tuple[int, int, str, dict[str, str]]]]:
    raw = READER.read_bytes()
    if (len(raw), raw.count(b"\n"), digest(raw)) != READER_IDENTITY or b"\r" in raw:
        raise SystemExit("reader identity/LF mismatch")
    text = raw.decode("utf-8"); lines = text.splitlines(); objects = []
    for number, line in enumerate(lines, 1):
        match = re.match(r'^(#{1,6})\s+.*\{([^}]*)\}\s*$', line)
        if match and (found := re.search(r'#(o012-fom-u001(?:-[A-Za-z0-9-]+)?)', match.group(2))):
            objects.append((found.group(1), number, None, "heading", match.group(2)))
    stack = []; number = 1
    while number <= len(lines):
        stripped = lines[number - 1].strip()
        if stripped.startswith(":::") and stripped != ":::":
            start = number; opener = [lines[number - 1]]
            while "}" not in opener[-1] and number < len(lines):
                number += 1; opener.append(lines[number - 1])
            joined = " ".join(opener); found = re.search(r'#(o012-fom-u001(?:-[A-Za-z0-9-]+)?)', joined)
            kind = re.match(r'^:::\s*\{\.([^\s}]+)', opener[0].strip())
            stack.append((found.group(1), start, kind.group(1), joined) if found and kind else None)
        elif stripped == ":::":
            if not stack: raise SystemExit(f"unexpected fenced close {number}")
            item = stack.pop()
            if item: objects.append((item[0], item[1], number, item[2], item[3]))
        number += 1
    heading_end = {"o012-fom-u001-notice": 39, "o012-fom-u001": 835,
                   "o012-fom-u001-s01": 438, "o012-fom-u001-s02": 835,
                   "o012-fom-u001-mastery": 1067}
    parsed = {}
    for ident, start, end, kind, opener in objects:
        attrs = {m.group(1): m.group(2) for m in re.finditer(r'(data-[a-z-]+)="([^"]*)"', opener)}
        parsed[ident] = (start, heading_end[ident] if end is None else end, kind, attrs)
    classes = Counter(item[2] for item in parsed.values())
    expected = {"heading": 5, "remark": 14, "source-audit": 12, "definition": 14,
                "example": 10, "figure": 10, "lemma": 1, "proof": 1, "corollary": 1,
                "exercise": 6, "hint": 6, "solution": 6, "boundary": 1}
    actual_aliases = {attrs["data-source-label"]: ident for ident, (_, _, _, attrs) in parsed.items()
                      if "data-source-label" in attrs}
    if len(parsed) != 87 or classes != Counter(expected) or actual_aliases != ALIASES:
        raise SystemExit("independent reader census/alias mismatch")
    return raw, lines, parsed


def expected_ids(stable: set[str]) -> dict[str, set[str]]:
    relations = {
        "relation:adapts:o012-fom-u001:fomberg-edition",
        "relation:contains:o012-d60:fomberg-u001",
        "relation:precedes:o012-rbt-u019:o012-fom-u001",
        "relation:contains:o012-d60-rights:fomberg-u001",
        "relation:xref:o012-d60:integrated-rights",
        "relation:precedes:o012-fom-u001:mastery",
        "relation:depends-on:fomberg-edition:commath-overlay",
        "relation:proves:o012-fom-u001-proof-001:boundary-square",
        "relation:depends-on:o012-fom-u001-cor-001:boundary-square",
    }
    relations |= {f"relation:hints:fom-u001-hint-{n:03d}:mcheck-{n:03d}" for n in range(1, 7)}
    relations |= {f"relation:solves:fom-u001-sol-{n:03d}:mcheck-{n:03d}" for n in range(1, 7)}
    relations |= {f"relation:illustrates:fom-u001-fig-{n:03d}:diagram-asset" for n in range(1, 11)}
    return {
        "artifacts.jsonl": {"artifact:o012-fom-u001-authority-gate",
                            "artifact:o012-fom-u001-authority-visual",
                            "artifact:o012-fom-u001-authority-file-manifest",
                            "artifact:o012-fom-u001-source-audit",
                            "artifact:o012-fom-u001-independent-review", "artifact:o012-fom-u001-qa"},
        "assets.jsonl": {"asset:o012-fom-u001-source-markdown",
                         "asset:o012-fom-u001-semantic-diagram-layer",
                         "asset:o012-fom-u001-build-overlay"},
        "authority.jsonl": {"resource:fomberg-algebraic-topology-2025",
                            "edition:fomberg-at-2025-563194f"},
        "concepts.jsonl": {f"concept:{slug}" for slug in SLUGS},
        "corrections.jsonl": {f"correction:o012-fom-u001-adv-{n:04d}" for n in range(408, 426)},
        "qa.jsonl": {"qa:o012-fom-u001-authority-build", "qa:o012-fom-u001-source-integrity",
                      "qa:o012-fom-u001-math", "qa:o012-fom-u001-language"},
        "relations.jsonl": relations,
        "rights.jsonl": {"rights:fomberg-cc-by-sa-4.0", "rights:fomberg-build-overlay-cc0-1.0",
                          "rights:o012-fom-u001-companion-cc-by-sa-4.0",
                          "rights:o012-fom-u001-composite-cc-by-sa-4.0",
                          "rights:o012-d60-integrated-route-cc-by-sa-4.0"},
        "segments.jsonl": {f"segment:{ident}" for ident in stable},
        "terms.jsonl": {f"term:{slug}:id-ID" for slug in SLUGS},
        "units.jsonl": {f"unit:{ident}" for ident in stable},
    }


def load_partition(parsed) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]], list[dict[str, str]]]:
    expected = expected_ids(set(parsed)); suffixes = {}; all_records = []; ids = set(); rows = []
    pb = hashlib.sha256(); fb = hashlib.sha256(); pr = pbytes = fr = fbytes = 0
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        if (len(raw.splitlines()), len(raw), digest(raw)) != FINAL[name]:
            raise SystemExit(f"{name}: final identity mismatch")
        pc, ps, ph = PREFIX[name]; prefix = raw[:ps]
        if (len(prefix.splitlines()), len(prefix), digest(prefix)) != (pc, ps, ph):
            raise SystemExit(f"{name}: immutable prefix mismatch")
        suffix_lines = raw[ps:].splitlines(keepends=True); suffix = []
        for number, line in enumerate(suffix_lines, 1):
            obj = json.loads(line.decode("utf-8"))
            if canon(obj) != line: raise SystemExit(f"{name}:{number}: noncanonical suffix")
            suffix.append(obj)
        suffix_ids = [item["id"] for item in suffix]
        if suffix_ids != sorted(suffix_ids) or set(suffix_ids) != expected[name] or len(suffix) != DELTA[name]:
            raise SystemExit(f"{name}: suffix ID/order/count mismatch")
        for line in raw.splitlines():
            obj = json.loads(line.decode("utf-8"))
            if obj["id"] in ids: raise SystemExit(f"duplicate global ID: {obj['id']}")
            ids.add(obj["id"]); all_records.append(obj)
        suffixes[name] = suffix
        rows.append({"path": f"backend/{name}", "prefix_records": str(pc), "prefix_bytes": str(ps),
                     "prefix_sha256": ph, "records_added": str(DELTA[name]),
                     "final_records": str(FINAL[name][0]), "final_bytes": str(FINAL[name][1]),
                     "final_sha256": FINAL[name][2], "prefix_preserved": "true"})
        pb.update(name.encode()); pb.update(b"\0"); pb.update(prefix)
        fb.update(name.encode()); fb.update(b"\0"); fb.update(raw)
        pr += pc; pbytes += ps; fr += len(raw.splitlines()); fbytes += len(raw)
    if (pr, pbytes, pb.hexdigest()) != PREFIX_TOTAL or (fr, fbytes, fb.hexdigest()) != FINAL_TOTAL:
        raise SystemExit("bundle identity mismatch")
    return suffixes, all_records, rows


def validate_semantics(suffixes, records, parsed, reader_raw) -> None:
    by_id = {item["id"]: item for item in records}
    spec = importlib.util.spec_from_file_location("o012_generic_fom001_independent", LANE / "scripts/validate-backend.py")
    if spec is None or spec.loader is None: raise SystemExit("cannot load generic validator")
    generic = importlib.util.module_from_spec(spec); spec.loader.exec_module(generic)
    generic.validate_shapes(records); generic.validate_references(records, by_id)
    generic.validate_artifact_manifests(records, LANE)
    identity(LANE / "qa/FOMBERG_UNIT_001_QA.json", QA_IDENTITY)
    review = identity(LANE / "qa/FOMBERG_UNIT_001_INDEPENDENT_REVIEW.md", REVIEW_IDENTITY)
    identity(LANE / "qa/FOMBERG_UNIT_001_SOURCE_AUDIT.md", AUDIT_IDENTITY)
    identity(LANE / "qa/FOMBERG_UNIT_001_BACKEND_CONTRACT.md", CONTRACT_IDENTITY)
    identity(LANE / "00_control/ADVERSE_LEDGER.csv", ADVERSE_IDENTITY)
    identity(LANE / "00_control/TERMINOLOGY.csv", TERMINOLOGY_IDENTITY)
    if b'FINAL_SEVERITY_COUNTS: {"P1":0,"P2":0,"P3":0}' not in review:
        raise SystemExit("review severity gate mismatch")
    units = suffixes["units.jsonl"]; segments = suffixes["segments.jsonl"]
    if ({x["source_local_id"] for x in units} != set(parsed)
            or {x["source_local_id"] for x in segments} != set(parsed)
            or len(units) != 87 or len(segments) != 87):
        raise SystemExit("87-pair stable mapping mismatch")
    root = by_id["unit:o012-fom-u001"]; root_seg = by_id["segment:o012-fom-u001"]
    if (root["unit_kind"], root["order"], root.get("edition_order"), root.get("route_order"),
        root["target_locator"]["line_start"], root["target_locator"]["line_end"],
        root_seg["target_locator"]["line_start"], root_seg["target_locator"]["line_end"]) != (
            "reader_unit", 31, 1, 8, 1, 1073, 40, 835):
        raise SystemExit("root/heading dual architecture mismatch")
    lines = reader_raw.splitlines(keepends=True)
    for record in units + segments:
        loc = record["target_locator"]; start, end = loc["line_start"], loc["line_end"]
        if (loc["file_sha256"] != READER_IDENTITY[2] or loc["path"] !=
                "source/id-ID/fomberg/units/fomberg-unit-001-delta-complexes-simplicial-homology.md"
                or digest(b"".join(lines[start - 1:end])) != loc["content_sha256"]):
            raise SystemExit(f"target locator mismatch: {record['id']}")
        alias = parsed[record["source_local_id"]][3].get("data-source-label")
        if alias and record.get("source_aliases") != [alias]:
            raise SystemExit(f"source alias missing: {record['id']}")
    diagram = by_id["asset:o012-fom-u001-semantic-diagram-layer"]
    if (diagram.get("source_diagram_count"), diagram.get("semantic_figure_block_count"),
        diagram.get("source_format_counts"), len(diagram.get("semantic_unit_ids", []))) != (
            14, 10, {"tikzpicture": 6, "inline_tikz": 6, "tikzcd": 2}, 10):
        raise SystemExit("diagram grouping mismatch")
    proof = by_id["unit:o012-fom-u001-proof-001"]
    if proof.get("repair_id") != "FOM-U001-PR-001" or proof.get("proof_status") != "complete_original_repair":
        raise SystemExit("proof-repair record mismatch")
    proof_segment = by_id["segment:o012-fom-u001-proof-001"]
    if proof_segment.get("source_locator") != {
            "path": "algebraic_topology.tex",
            "commit_sha": "563194fae879178b9a6871b249513bfc27968975",
            "line_start": 521, "line_end": 548, "precision": "exact_source_span"}:
        raise SystemExit("proof-repair exact upstream locator mismatch")
    for ident in ("unit:o012-fom-u001-def-009", "unit:o012-fom-u001-cor-001",
                  "unit:o012-fom-u001-def-010", "unit:o012-fom-u001-def-011"):
        if by_id[ident].get("boundary_convention") != "B_n=im(partial_{n+1})":
            raise SystemExit("standard B_n convention not bound")
    relations = suffixes["relations.jsonl"]
    for n in range(1, 7):
        exercise = f"unit:o012-fom-u001-mcheck-{n:03d}"
        if sum(x["relation_type"] == "hints" and x["to_id"] == exercise for x in relations) != 1:
            raise SystemExit(f"mastery hint closure mismatch {n}")
        if sum(x["relation_type"] == "solves" and x["to_id"] == exercise for x in relations) != 1:
            raise SystemExit(f"mastery solution closure mismatch {n}")
        if by_id[f"unit:o012-fom-u001-sol-{n:03d}"].get("solution_status") != "complete_checked_solution":
            raise SystemExit(f"mastery solution status mismatch {n}")
    adverse = list(csv.DictReader(io.StringIO((LANE / "00_control/ADVERSE_LEDGER.csv").read_text(encoding="utf-8"))))
    terms = list(csv.DictReader(io.StringIO((LANE / "00_control/TERMINOLOGY.csv").read_text(encoding="utf-8"))))
    if {x.get("adverse_ledger_id") for x in suffixes["corrections.jsonl"]} != {f"O012-ADV-{n:04d}" for n in range(408, 426)}:
        raise SystemExit("correction/ledger coverage mismatch")
    if {x.get("terminology_control_id") for x in suffixes["terms.jsonl"]} != {f"O012-TERM-{n:04d}" for n in range(366, 394)}:
        raise SystemExit("term/ledger coverage mismatch")
    if adverse[-1]["event_id"] != "O012-ADV-0425" or terms[-1]["term_id"] != "O012-TERM-0393":
        raise SystemExit("ledger endpoints mismatch")
    rights = {x["id"]: x for x in suffixes["rights.jsonl"]}
    if (rights["rights:fomberg-cc-by-sa-4.0"]["license_expression"] != "CC-BY-SA-4.0"
            or rights["rights:fomberg-build-overlay-cc0-1.0"]["license_expression"] != "CC0-1.0"
            or "Roberts CC BY 4.0" not in rights["rights:o012-d60-integrated-route-cc-by-sa-4.0"]["attribution"]):
        raise SystemExit("component/integrated rights mismatch")
    for artifact in suffixes["artifacts.jsonl"]:
        raw = (LANE / artifact["path"]).read_bytes()
        if (len(raw), digest(raw)) != (artifact["bytes"], artifact["sha256"]):
            raise SystemExit(f"artifact identity mismatch: {artifact['id']}")
    suffix_raw = b"".join(canon(x) for name in FILES for x in suffixes[name])
    if (b"C:\\Users" in suffix_raw or b"token" in suffix_raw.lower() or b"published" in suffix_raw
            or b"FOM-PR-01" in suffix_raw or b"FOM-PR-08" in suffix_raw):
        raise SystemExit("privacy/premature-claim/later-repair contamination")
    if reader_raw.count(MODEL.encode()) != 1:
        raise SystemExit("model provenance count mismatch")


def write_receipts(rows, parsed) -> None:
    out = io.StringIO(newline="")
    fields = ["path", "prefix_records", "prefix_bytes", "prefix_sha256", "records_added",
              "final_records", "final_bytes", "final_sha256", "prefix_preserved"]
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n"); writer.writeheader(); writer.writerows(rows)
    manifest_raw = out.getvalue().encode("utf-8"); MANIFEST.write_bytes(manifest_raw)
    receipt = {
        "schema_version": "1.0.0", "receipt_id": "O012-BACKEND-FOMBERG-UNIT-001-SEMANTIC-APPEND-ONLY",
        "status": "PASS", "scope": "Fomberg Unit 001 semantic append only; no reader build or publication claim",
        "immutability": {"prefix_records": PREFIX_TOTAL[0], "prefix_bytes": PREFIX_TOTAL[1],
                         "prefix_bundle_sha256": PREFIX_TOTAL[2], "prefix_preserved_byte_for_byte": True},
        "append": {"records_added": sum(DELTA.values()), "records_by_file": DELTA},
        "current": {"total_records": FINAL_TOTAL[0], "total_bytes": FINAL_TOTAL[1],
                    "bundle_sha256": FINAL_TOTAL[2],
                    "files": {name: {"records": FINAL[name][0], "bytes": FINAL[name][1], "sha256": FINAL[name][2]}
                              for name in FILES}},
        "source": {"reader_bytes": READER_IDENTITY[0], "reader_lines": READER_IDENTITY[1],
                   "reader_sha256": READER_IDENTITY[2], "stable_ids": len(parsed),
                   "next_source_line": 615, "terminal_source_eof": False,
                   "source_span_sha256": "68cb0dea7aa24a42e979877a95acf61b8152c87ed86d88ad7deac7cb5cea2fe3"},
        "closure": {"unit_records": 87, "segment_records": 87, "source_aliases": ALIASES,
                    "source_diagrams": 14, "semantic_figure_blocks": 10,
                    "mastery_triples": 6, "proof_repair": "FOM-U001-PR-001",
                    "boundary_convention": "B_n=im(partial_{n+1})",
                    "adverse_through": "O012-ADV-0425", "terminology_through": "O012-TERM-0393",
                    "review_final_counts": {"P1": 0, "P2": 0, "P3": 0}},
        "evidence": {"qa": {"bytes": QA_IDENTITY[0], "sha256": QA_IDENTITY[1]},
                     "review": {"bytes": REVIEW_IDENTITY[0], "sha256": REVIEW_IDENTITY[1]},
                     "audit": {"bytes": AUDIT_IDENTITY[0], "sha256": AUDIT_IDENTITY[1]},
                     "contract": {"bytes": CONTRACT_IDENTITY[0], "sha256": CONTRACT_IDENTITY[1]}},
        "file_manifest": {"path": "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_001_FILE_MANIFEST.csv",
                          "bytes": len(manifest_raw), "sha256": digest(manifest_raw)},
        "model_provenance": MODEL,
    }
    receipt_raw = json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n"
    RECEIPT.write_bytes(receipt_raw)
    human = ("# Fomberg Unit 001 semantic backend append-only receipt\n\n"
             "Status: **PASS**\n\n"
             f"- Immutable Roberts Units 001-030 prefix: {PREFIX_TOTAL[0]:,} records / {PREFIX_TOTAL[1]:,} bytes / `{PREFIX_TOTAL[2]}`.\n"
             f"- Appended Fomberg Unit 001: {sum(DELTA.values())} records, including 87 unit and 87 segment records.\n"
             f"- Current backend: {FINAL_TOTAL[0]:,} records / {FINAL_TOTAL[1]:,} bytes / `{FINAL_TOTAL[2]}`.\n"
             "- Reader closure: 87 stable IDs, five source aliases, 14 source diagrams in ten semantic blocks, six solved mastery triples, and proof repair `FOM-U001-PR-001`.\n"
             "- Independent review: P1=0, P2=0, P3=0.\n"
             "- Cursor: source line 615; source EOF is false.\n"
             "- This is semantic admission only; no HTML, PDF, publication, or later-unit completion is claimed.\n")
    HUMAN.write_bytes(human.encode("utf-8"))


def main() -> int:
    reader_raw, _, parsed = parse_reader()
    suffixes, records, rows = load_partition(parsed)
    validate_semantics(suffixes, records, parsed, reader_raw)
    write_receipts(rows, parsed)
    print("Fomberg Unit 001 semantic append-only backend validation: PASS")
    print(f"prefix_bundle_sha256={PREFIX_TOTAL[2]}")
    print(f"records_added={sum(DELTA.values())}")
    print(f"final_records={FINAL_TOTAL[0]}")
    print(f"final_bytes={FINAL_TOTAL[1]}")
    print(f"final_bundle_sha256={FINAL_TOTAL[2]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
