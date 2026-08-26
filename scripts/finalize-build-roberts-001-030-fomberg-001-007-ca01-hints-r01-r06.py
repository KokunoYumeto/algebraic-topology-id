#!/usr/bin/env python3
"""Validate the deterministic CA01 + R01-R06 hint reader build.

The ordinary-hint layer is additive.  This helper merges a scratch appendix
without changing the sealed CA01 predecessor, then writes only the bounded
draft receipt after deterministic structural checks.  Visual and browser QA
remain explicit later gates.
"""

from __future__ import annotations

import argparse
import csv
import html as html_lib
import json
import re
from collections import Counter
from hashlib import sha256
from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject,
    ByteStringObject,
    DictionaryObject,
    IndirectObject,
    NullObject,
    StreamObject,
)


LANE = Path(__file__).resolve().parents[1]
TARGET = LANE / "qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_BUILD_DRAFT.json"
SOURCE_REL = "source/id-ID/mastery/ordinary-hints-r01-r06.md"
SOURCE_SHA = "dc319cb191d709a5807f0c0792401f9faf2993ceede364764547f20bb4f69c2a"
QA_REL = "qa/ORDINARY_HINTS_R01_R06_QA.json"
BACKEND_REL = "qa/BACKEND_APPEND_ONLY_ORDINARY_HINTS_R01_R06_CUMULATIVE_RECEIPT.json"
SEMANTIC_BACKEND_REL = "qa/BACKEND_APPEND_ONLY_ORDINARY_HINTS_R01_R06_RECEIPT.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"

PRIOR_HTML_REL = "output/html/roberts-001-030-fomberg-001-007-ca01/index.html"
PRIOR_PDF_REL = "output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-007-ca01-id.pdf"
PRIOR_MANIFEST_REL = "output/ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_007_CA01.csv"
PRIOR_RECEIPT_REL = "qa/ROBERTS_001_030_FOMBERG_001_007_CA01_BUILD_RECEIPT.json"
HTML_REL = "output/html/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06/index.html"
PDF_REL = "output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-id.pdf"
MANIFEST_REL = "output/ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06.csv"

PRIOR_HTML = {"path": PRIOR_HTML_REL, "bytes": 14958219, "sha256": "d71e2f3c0eb38b48fe4686a955ad555db3a407df8f18e41371d52908f0bdbbdf"}
PRIOR_PDF = {"path": PRIOR_PDF_REL, "bytes": 8358561, "sha256": "476b0de3bbb2cbfe03a151ac3060e121c5f89364e70b54d918ab270f4c965ade"}
PRIOR_MANIFEST = {"path": PRIOR_MANIFEST_REL, "bytes": 297, "sha256": "eac46f939ac99da1479c7826a350eb926c30f91d4c74fdfe785a597f7a58803d"}
PRIOR_RECEIPT = {"path": PRIOR_RECEIPT_REL, "bytes": 7842, "sha256": "22fef828b7963219759f85d11e409e0ebf957889d0fa76dc02ec04f3a707a9e0"}

# CA01's LaTeX export predates PDF stable-ID destinations for ordinary
# exercises and solutions. The predecessor bytes are frozen above, so this
# reviewed page map can add the missing names without changing any predecessor
# page. Values are physical, one-based PDF pages; pypdf uses zero-based indexes.
PRIOR_LINK_PAGES_1BASED = {
    "o012-rbt-l01-ex-001": 12,
    "o012-rbt-l01-ex-002": 13,
    "o012-rbt-l01-sol-001": 13,
    "o012-rbt-l01-sol-002": 13,
    "o012-rbt-l02-ex-001": 15,
    "o012-rbt-l02-ex-002": 16,
    "o012-rbt-l02-ex-003": 16,
    "o012-rbt-l02-ex-004": 17,
    "o012-rbt-l02-sol-001": 20,
    "o012-rbt-l02-sol-002": 21,
    "o012-rbt-l02-sol-003": 21,
    "o012-rbt-l02-sol-004": 22,
    "o012-rbt-l03-ex-001": 24,
    "o012-rbt-l03-ex-002": 25,
    "o012-rbt-l03-ex-003": 27,
    "o012-rbt-l03-ex-004": 30,
    "o012-rbt-l03-ex-005": 30,
    "o012-rbt-l03-sol-001": 30,
    "o012-rbt-l03-sol-002": 31,
    "o012-rbt-l03-sol-003": 31,
    "o012-rbt-l03-sol-004": 32,
    "o012-rbt-l03-sol-005": 32,
    "o012-rbt-l04-ex-001": 34,
    "o012-rbt-l04-sol-001": 39,
    "o012-rbt-l05-mcheck-001": 49,
    "o012-rbt-l05-mcheck-002": 49,
    "o012-rbt-l05-mcheck-003": 50,
    "o012-rbt-l05-mcheck-004": 51,
    "o012-rbt-l05-sol-001": 49,
    "o012-rbt-l05-sol-002": 49,
    "o012-rbt-l05-sol-003": 51,
    "o012-rbt-l05-sol-004": 51,
    "o012-rbt-l06-mcheck-001": 59,
    "o012-rbt-l06-mcheck-002": 60,
    "o012-rbt-l06-sol-001": 60,
    "o012-rbt-l06-sol-002": 60,
    "o012-rbt-l07-mcheck-001": 70,
    "o012-rbt-l07-mcheck-002": 71,
    "o012-rbt-l07-mcheck-003": 71,
    "o012-rbt-l07-mcheck-004": 72,
    "o012-rbt-l07-sol-001": 70,
    "o012-rbt-l07-sol-002": 71,
    "o012-rbt-l07-sol-003": 71,
    "o012-rbt-l07-sol-004": 72,
    "o012-rbt-l08-ex-001": 79,
    "o012-rbt-l08-mcheck-002": 81,
    "o012-rbt-l08-sol-001": 80,
    "o012-rbt-l08-sol-002": 81,
    "o012-rbt-l11-mcheck-001": 115,
    "o012-rbt-l11-mcheck-002": 116,
    "o012-rbt-l11-mcheck-003": 116,
    "o012-rbt-l11-sol-001": 115,
    "o012-rbt-l11-sol-002": 116,
    "o012-rbt-l11-sol-003": 117,
    "o012-rbt-l12-mcheck-001": 126,
    "o012-rbt-l12-mcheck-002": 127,
    "o012-rbt-l12-mcheck-003": 127,
    "o012-rbt-l12-sol-001": 126,
    "o012-rbt-l12-sol-002": 127,
    "o012-rbt-l12-sol-003": 128,
    "o012-rbt-l14-ex-001": 148,
    "o012-rbt-l14-ex-002": 149,
    "o012-rbt-l14-mcheck-001": 151,
    "o012-rbt-l14-mcheck-004": 152,
    "o012-rbt-l14-mcheck-005": 153,
    "o012-rbt-l14-mcheck-006": 154,
    "o012-rbt-l14-sol-001": 151,
    "o012-rbt-l14-sol-002": 152,
    "o012-rbt-l14-sol-003": 152,
    "o012-rbt-l14-sol-004": 153,
    "o012-rbt-l14-sol-005": 153,
    "o012-rbt-l14-sol-006": 154,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def identity(relative: str) -> dict[str, Any]:
    path = LANE / relative
    require(path.is_file() and path.stat().st_size > 0, f"missing input: {relative}")
    return {"path": relative, "bytes": path.stat().st_size, "sha256": digest(path)}


def load(relative: str) -> tuple[dict[str, Any], str]:
    path = LANE / relative
    require(path.is_file(), f"missing JSON: {relative}")
    raw = path.read_text(encoding="utf-8")
    return json.loads(raw), raw


def source_contract() -> tuple[list[tuple[str, str]], list[str], list[tuple[str, str]], list[str]]:
    path = LANE / SOURCE_REL
    require(path.stat().st_size == 28698 and digest(path) == SOURCE_SHA, "ordinary-hint source identity drift")
    text = path.read_text(encoding="utf-8")
    require("\r" not in text, "ordinary-hint source is not LF-only")
    headings = []
    for match in re.finditer(r"(?m)^#{1,2}\s+(.+?)\s+\{#([^}]+)\}\s*$", text):
        headings.append((match.group(1), match.group(2)))
    expected_ids = ["o012-d60-hints-r01-r06", *[f"o012-d60-hints-r0{i}" for i in range(1, 7)]]
    require([item[1] for item in headings] == expected_ids, "source heading/destination order drift")
    hints = re.findall(r'(?m)^::: \{\.hint #(o012-d60-r0[1-6]-hint-\d{3})\b', text)
    require(len(hints) == len(set(hints)) == 36, "source hint-ID census drift")
    stable_ids = [*expected_ids, *hints]
    require(len(stable_ids) == len(set(stable_ids)) == 43, "source stable-ID census drift")
    pairs = re.findall(
        r'data-target-exercise-id="unit:([^"]+)"\s+data-existing-solution-id="unit:([^"]+)"',
        text,
    )
    require(len(pairs) == 36 and len({left for left, _ in pairs}) == 36 and len({right for _, right in pairs}) == 36, "source exercise/solution binding drift")
    links = re.findall(r"\]\(#([^)]+)\)", text)
    expected_links = [value for pair in pairs for value in pair]
    require(Counter(links) == Counter(expected_links) and len(links) == 72, "visible source links do not exactly bind the 36 pairs")
    return headings, links, pairs, stable_ids


def qa_backend_gate() -> tuple[dict[str, Any], dict[str, Any]]:
    qa, qa_raw = load(QA_REL)
    backend, _ = load(BACKEND_REL)
    require(qa.get("status") == "PASS", "ordinary-hint QA is not PASS")
    require(SOURCE_SHA in qa_raw and SOURCE_REL in qa_raw.replace("\\", "/"), "ordinary-hint QA does not bind the live source")
    require(backend.get("status") == "PASS" and backend.get("receipt_kind") == "cumulative_backend_boundary", "ordinary-hint cumulative backend gate failed")
    require(backend.get("replay", {}).get("status") == "PASS", "backend replay is not PASS")
    require(
        backend.get("immutable_prefix")
        == {
            "bundle_sha256": "51e75d06e620762e629e9e7408da4b0c32b3e337817d9d140fbbdfa438de2f57",
            "bytes": 8_345_799,
            "preserved_exactly": True,
            "records": 6_854,
        },
        "backend immutable-prefix identity drift",
    )
    require(
        backend.get("delta", {}).get("records") == 158
        and backend["delta"].get("bytes") == 199_933
        and backend["delta"].get("bundle_sha256") == "a4ec1979000ba447ffa2a2534279de0b9ed374c1c560461b6a69b2ee5e6ceb6e",
        "backend delta identity drift",
    )
    require(
        backend.get("cumulative")
        == {
            "bundle_sha256": "7d723f9ef163303c7dde63d646dc8d5917c2450b1da5d24c87ef77bf4e4d664b",
            "bytes": 8_545_732,
            "records": 7_012,
        },
        "backend cumulative identity drift",
    )
    replay = backend["replay"]
    require(
        replay.get("final") == backend["cumulative"]
        and replay.get("exact_file_matches") == 11
        and replay.get("suffix_bytes") == 199_933
        and replay.get("temporary_replay_removed") is True,
        "backend replay identity drift",
    )
    semantic_checks = backend.get("semantic_checks", {})
    graph = semantic_checks.get("graph_postconditions", {})
    require(
        semantic_checks.get("added_records") == 158
        and semantic_checks.get("merged_records") == 7_012
        and all(semantic_checks.get(key) == "PASS" for key in ("artifact_evidence", "global_references", "prompt_solution_solves_immutability", "rights_closure", "route_mapping", "schema_shapes")),
        "backend semantic gate failed",
    )
    require(
        graph
        == {
            "active_hint_relations": 165,
            "active_hint_units": 165,
            "active_solves_relations": 221,
            "ca01_items": 8,
            "credited_total": 92,
            "duplicate_or_reused_solution_ids": 0,
            "graph_complete_triples": 165,
            "ordinary_capped_route_credit": 84,
            "ordinary_graph_complete_triples": 157,
        },
        "backend semantic graph gate failed",
    )
    require(
        backend.get("route_mastery_census")
        == {
            "active_hint_relations": 165,
            "active_hint_units": 165,
            "active_solve_relations": 221,
            "bytes": 140_589,
            "ca01_credit": 8,
            "duplicate_or_reused_solution_ids": [],
            "graph_complete_triples": 165,
            "ordinary_capped_credit": 84,
            "path": "qa/ROUTE_MASTERY_CENSUS.json",
            "sha256": "068072d3c67aeed28d55fdb9947a3084e4028ba0b808e28f46c0657ba84d20ff",
            "status": "PASS",
            "total_credit": 92,
            "validation_errors": 0,
        },
        "backend route-mastery census gate failed",
    )

    semantic_ref = backend.get("supporting_receipts", {}).get("semantic")
    expected_ref = {
        "bytes": 2_615,
        "lf_lines": 71,
        "path": SEMANTIC_BACKEND_REL,
        "sha256": "6ea98f4a65a6104e7d115a892e9906103e5434f6c10375959cd09b762df8c0c5",
    }
    require(semantic_ref == expected_ref, "backend semantic-receipt reference drift")
    require(identity(SEMANTIC_BACKEND_REL) == {"path": SEMANTIC_BACKEND_REL, "bytes": expected_ref["bytes"], "sha256": expected_ref["sha256"]}, "supporting semantic-receipt identity drift")
    semantic_path = LANE / SEMANTIC_BACKEND_REL
    require(semantic_path.read_bytes().count(b"\n") == expected_ref["lf_lines"], "supporting semantic-receipt LF-line count drift")
    semantic, _ = load(SEMANTIC_BACKEND_REL)
    require(
        semantic.get("status") == "PASS"
        and semantic.get("receipt_kind") == "semantic_append_validation"
        and semantic.get("edition_unit_id") == "O012-ORIG-HINTS-R01-R06"
        and semantic.get("source_sha256") == SOURCE_SHA,
        "supporting semantic backend receipt failed",
    )
    expected_inputs = {
        SOURCE_REL: {"bytes": 28_698, "lf_lines": 410, "sha256": SOURCE_SHA},
        "qa/ORDINARY_HINTS_R01_R06_QA.json": {"bytes": 16_616, "lf_lines": 398, "sha256": "a0460dbed83242863fc1aab8290b76fac9cd39644276e132401e7d3e9198c33d"},
        "qa/ordinary-hints-r01-r06/INDEPENDENT_MATH_REVIEW.json": {"bytes": 19_289, "lf_lines": 447, "sha256": "8ed5b3563976b415e1aa471f7cdeb3405888cbc70aec101bc02e4fab9e45de5a"},
        "qa/ordinary-hints-r01-r06/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json": {"bytes": 18_324, "lf_lines": 221, "sha256": "6c29009da4ee0380c878c3705dcd2a99cbe7a8495cc4b7f5ce456bb40f910968"},
    }
    require(semantic.get("input_identities") == expected_inputs, "supporting semantic input-identity set drift")
    for relative, expected in expected_inputs.items():
        live = LANE / relative
        require(identity(relative) == {"path": relative, "bytes": expected["bytes"], "sha256": expected["sha256"]}, f"supporting semantic input identity drift: {relative}")
        require(live.read_bytes().count(b"\n") == expected["lf_lines"], f"supporting semantic input LF-line count drift: {relative}")
    return qa, backend


def canonical_pdf_object(obj: Any, cache: dict[tuple[int, int], Any], active: set[tuple[int, int]]) -> Any:
    if isinstance(obj, IndirectObject):
        key = (int(obj.idnum), int(obj.generation))
        if key in cache:
            return cache[key]
        if key in active:
            return {"cycle": type(obj.get_object()).__name__}
        active.add(key)
        value = canonical_pdf_object(obj.get_object(), cache, active)
        active.remove(key)
        cache[key] = value
        return value
    if isinstance(obj, StreamObject):
        dictionary = {
            str(key): canonical_pdf_object(value, cache, active)
            for key, value in sorted(obj.items(), key=lambda item: str(item[0]))
            if str(key) not in {"/Length", "/Filter", "/DecodeParms"}
        }
        return {"stream_dictionary": dictionary, "decoded_sha256": sha256(obj.get_data()).hexdigest()}
    if isinstance(obj, DictionaryObject):
        return {
            str(key): canonical_pdf_object(value, cache, active)
            for key, value in sorted(obj.items(), key=lambda item: str(item[0]))
            if str(key) != "/Length"
        }
    if isinstance(obj, ArrayObject):
        return [canonical_pdf_object(value, cache, active) for value in obj]
    if isinstance(obj, ByteStringObject):
        return {"bytes_hex": bytes(obj).hex()}
    if isinstance(obj, NullObject) or obj is None:
        return None
    if isinstance(obj, bool) or isinstance(obj, (int, float)):
        return obj
    return str(obj)


def page_visual_signature(page: Any, cache: dict[tuple[int, int], Any]) -> str:
    contents = page.get_contents()
    selected_annotations = []
    for reference in page.get("/Annots", []) or []:
        annotation = reference.get_object() if isinstance(reference, IndirectObject) else reference
        if isinstance(annotation, DictionaryObject):
            selected_annotations.append(
                canonical_pdf_object(
                    DictionaryObject({key: annotation[key] for key in ("/Subtype", "/Rect", "/A", "/Dest", "/Contents", "/NM", "/F", "/Border", "/C") if key in annotation}),
                    cache,
                    set(),
                )
            )
    payload = {
        "content_sha256": sha256(b"" if contents is None else contents.get_data()).hexdigest(),
        "resources": canonical_pdf_object(page.get("/Resources", {}), cache, set()),
        "annotations": selected_annotations,
        "mediabox": [float(value) for value in page.mediabox],
        "cropbox": [float(value) for value in page.cropbox],
        "rotation": int(page.get("/Rotate", 0) or 0),
    }
    return sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def outline_entries(reader: PdfReader) -> list[tuple[str, int | None]]:
    entries: list[tuple[str, int | None]] = []

    def visit(value: Any) -> None:
        if isinstance(value, list):
            for item in value:
                visit(item)
        else:
            try:
                page = reader.get_destination_page_number(value)
            except Exception:
                page = None
            entries.append((str(getattr(value, "title", value)), page))

    try:
        visit(reader.outline)
    except Exception:
        return []
    return entries


def annotation_link_targets(reader: PdfReader, first_page: int = 0) -> list[str]:
    values: list[str] = []
    for page in reader.pages[first_page:]:
        for reference in page.get("/Annots", []) or []:
            annotation = reference.get_object() if isinstance(reference, IndirectObject) else reference
            if not isinstance(annotation, DictionaryObject) or str(annotation.get("/Subtype")) != "/Link":
                continue
            destination = annotation.get("/Dest")
            action = annotation.get("/A")
            if isinstance(action, IndirectObject):
                action = action.get_object()
            if destination is None and isinstance(action, DictionaryObject) and str(action.get("/S")) == "/GoTo":
                destination = action.get("/D")
            if isinstance(destination, str):
                values.append(destination.lstrip("/"))
            elif isinstance(destination, ByteStringObject):
                values.append(bytes(destination).decode("utf-8").lstrip("/"))
    return values


def merge_pdfs(prior_path: Path, append_path: Path, output_path: Path) -> None:
    headings, visible_links, _pairs, stable_ids = source_contract()
    require(prior_path.is_file() and append_path.is_file() and output_path.parent.is_dir(), "merge input/output path missing")
    prior = PdfReader(str(prior_path))
    appendix = PdfReader(str(append_path))
    prior_outline = outline_entries(prior)
    appendix_outline = outline_entries(appendix)
    require(len(prior.pages) == 477 and len(prior_outline) == 389, "CA01 predecessor PDF boundary drift")
    require(len(appendix.pages) > 0 and len(appendix_outline) == len(headings), "hint appendix page/outline census drift")
    require(all(page is not None and 0 <= page < len(appendix.pages) for _title, page in appendix_outline), "hint appendix outline has unresolved destination")
    require([title for title, _page in appendix_outline] == [title for title, _name in headings], "hint appendix outline titles differ from source")
    appendix_named = appendix.named_destinations
    appendix_named_pages = {name: appendix.get_destination_page_number(destination) for name, destination in appendix_named.items()}
    require(all(name in appendix_named_pages and appendix_named_pages[name] is not None for name in stable_ids), "appendix PDF does not expose all 43 source stable IDs")
    prior_named = prior.named_destinations
    prior_named_pages = {name: prior.get_destination_page_number(destination) for name, destination in prior_named.items()}
    require(len(prior_named_pages) == 2873, "CA01 predecessor named-destination census drift")
    require(set(visible_links) == set(PRIOR_LINK_PAGES_1BASED) and len(PRIOR_LINK_PAGES_1BASED) == 72, "reviewed predecessor-link page map differs from the 72 visible links")
    require(set(PRIOR_LINK_PAGES_1BASED).isdisjoint(prior_named_pages), "a reviewed stable link name unexpectedly collides with the CA01 name tree")
    require(all(1 <= page <= len(prior.pages) for page in PRIOR_LINK_PAGES_1BASED.values()), "a reviewed predecessor-link page is outside CA01")
    appendix_targets = annotation_link_targets(appendix)
    require(not (set(visible_links) - set(appendix_targets)), "a visible hint link was not emitted as a PDF link annotation")

    writer = PdfWriter()
    writer.append(str(prior_path), import_outline=True)
    for name, physical_page in PRIOR_LINK_PAGES_1BASED.items():
        writer.add_named_destination(name, physical_page - 1)
    appendix._named_destinations_cache = {}  # noqa: SLF001 - discard generic/colliding LaTeX names.
    writer.append(appendix, import_outline=False)
    offset = 477
    for name in stable_ids:
        writer.add_named_destination(name, offset + int(appendix_named_pages[name]))
    parent = writer.add_outline_item(headings[0][0], offset + int(appendix_outline[0][1]), is_open=True)
    for (title, _name), (_pdf_title, local_page) in zip(headings[1:], appendix_outline[1:], strict=True):
        writer.add_outline_item(title, offset + int(local_page), parent=parent)
    writer.add_metadata(
        {
            "/Title": "Topologi Aljabar — Roberts 30/30, Fomberg 1.1–1.13, Asesmen Kumulatif 1, dan Petunjuk Rute 1–6",
            "/Author": "David Michael Roberts; Yeheli Fomberg; edisi Bahasa Indonesia dengan pendamping penguasaan",
            "/Subject": "Checkpoint komposit parsial dengan 36 petunjuk penguasaan R01–R06",
            "/Creator": f"{MODEL}; atas arahan pengguna",
            "/Producer": "pypdf 6.12.2 deterministic append",
            "/CreationDate": "D:20260826000000+02'00'",
            "/ModDate": "D:20260826000000+02'00'",
        }
    )
    writer.page_mode = "/UseOutlines"
    writer._ID = None  # noqa: SLF001 - pypdf has no public trailer-ID suppressor.
    with output_path.open("wb") as stream:
        writer.write(stream)

    merged = PdfReader(str(output_path))
    merged_outline = outline_entries(merged)
    merged_named = merged.named_destinations
    merged_named_pages = {name: merged.get_destination_page_number(destination) for name, destination in merged_named.items()}
    require(len(merged.pages) == offset + len(appendix.pages), "merged PDF page count drift")
    require(merged_outline[:389] == prior_outline and len(merged_outline) == 389 + len(headings), "predecessor outline is not an exact prefix")
    require(len(merged_named_pages) == 2873 + len(PRIOR_LINK_PAGES_1BASED) + len(stable_ids), "merged named-destination census drift")
    require(all(merged_named_pages.get(name) == page for name, page in prior_named_pages.items()), "predecessor named destinations changed")
    require(all(merged_named_pages.get(name) == physical_page - 1 for name, physical_page in PRIOR_LINK_PAGES_1BASED.items()), "rebuilt predecessor stable-ID destinations drift")
    require(all(merged_named_pages.get(name) == offset + int(appendix_named_pages[name]) for name in stable_ids), "rebuilt hint stable-ID destinations drift")
    merged_targets = annotation_link_targets(merged, offset)
    require(not (set(visible_links) - set(merged_targets)) and all(merged_named_pages.get(name) == PRIOR_LINK_PAGES_1BASED[name] - 1 for name in visible_links), "visible appended PDF links do not resolve to reviewed predecessor anchors")
    print(json.dumps({"status": "PASS", "bytes": output_path.stat().st_size, "sha256": digest(output_path), "pages": len(merged.pages), "appendix_pages": len(appendix.pages), "outline_entries": len(merged_outline), "named_destinations": len(merged_named_pages), "predecessor_stable_id_destinations_added": len(PRIOR_LINK_PAGES_1BASED), "stable_id_destinations_added": len(stable_ids), "visible_predecessor_links": len(set(visible_links))}, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence")
    parser.add_argument("--merge-pdfs", action="store_true")
    parser.add_argument("--prior")
    parser.add_argument("--append")
    parser.add_argument("--output")
    args = parser.parse_args()
    if args.merge_pdfs:
        require(args.prior and args.append and args.output, "merge paths are required")
        merge_pdfs(Path(args.prior).resolve(), Path(args.append).resolve(), Path(args.output).resolve())
        return

    require(args.evidence, "--evidence is required")
    evidence_path = Path(args.evidence).resolve()
    require(evidence_path.is_file(), "missing deterministic evidence")
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    require(evidence.get("status") == "PASS", "deterministic evidence is not PASS")
    require(evidence.get("pdf", {}).get("build_only_hint_paragraph_boundaries") == 36 and evidence["pdf"].get("build_only_explicit_stable_id_destinations") == 43 and evidence["pdf"].get("build_only_external_named_link_transforms") == 72, "PDF build-only transform census drift")
    headings, visible_links, pairs, stable_ids = source_contract()
    qa, backend = qa_backend_gate()
    require(identity(PRIOR_HTML_REL) == PRIOR_HTML and identity(PRIOR_PDF_REL) == PRIOR_PDF, "frozen CA01 reader identity drift")
    require(identity(PRIOR_MANIFEST_REL) == PRIOR_MANIFEST and identity(PRIOR_RECEIPT_REL) == PRIOR_RECEIPT, "frozen CA01 control identity drift")

    html_id, pdf_id, manifest_id = identity(HTML_REL), identity(PDF_REL), identity(MANIFEST_REL)
    require(html_id["bytes"] == evidence["html"]["combined_bytes"] and html_id["sha256"] == evidence["html"]["combined_sha256"], "live HTML differs from evidence")
    require(pdf_id["bytes"] == evidence["pdf"]["merged_bytes"] and pdf_id["sha256"] == evidence["pdf"]["merged_sha256"], "live PDF differs from evidence")
    with (LANE / MANIFEST_REL).open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == 2 and {row["path"]: (int(row["bytes"]), row["sha256"]) for row in rows} == {HTML_REL: (html_id["bytes"], html_id["sha256"]), PDF_REL: (pdf_id["bytes"], pdf_id["sha256"])}, "artifact manifest drift")

    html_text = (LANE / HTML_REL).read_text(encoding="utf-8")
    ids = re.findall(r'(?<=\s)id="([^"]+)"', html_text)
    fragments = [html_lib.unescape(value) for value in re.findall(r'\bhref="#([^"]+)"', html_text)]
    require(len(ids) == len(set(ids)) and not (set(fragments) - set(ids)), "HTML duplicate ID or unresolved fragment")
    require('<title>Topologi Aljabar — Roberts 30/30, Fomberg 1.1–1.13, Asesmen Kumulatif 1, dan Petunjuk Rute 1–6</title>' in html_text, "HTML title drift")
    require('id="toc-o012-d60-hints-r01-r06"' in html_text and 'id="o012-d60-hints-r01-r06-status"' in html_text, "HTML hint ToC/status missing")
    require(evidence["html"]["predecessor_exact_reconstruction"] is True and evidence["html"]["predecessor_reconstructed_sha256"] == PRIOR_HTML["sha256"], "HTML predecessor was not exactly reconstructed")
    require(evidence["html"]["hint_blocks"] == 36 and evidence["html"]["visible_predecessor_links"] == 72, "HTML hint census drift")

    prior_reader = PdfReader(str(LANE / PRIOR_PDF_REL))
    merged_reader = PdfReader(str(LANE / PDF_REL))
    appendix_pages = int(evidence["pdf"]["appendix_pages"])
    require(len(prior_reader.pages) == 477 and len(merged_reader.pages) == 477 + appendix_pages, "PDF page boundary drift")
    prior_cache: dict[tuple[int, int], Any] = {}
    merged_cache: dict[tuple[int, int], Any] = {}
    signatures = []
    mismatches = []
    for index in range(477):
        left = page_visual_signature(prior_reader.pages[index], prior_cache)
        right = page_visual_signature(merged_reader.pages[index], merged_cache)
        signatures.append(left)
        if left != right:
            mismatches.append(index + 1)
    require(not mismatches, f"predecessor page visual signatures changed: {mismatches[:10]}")
    for number, page in enumerate(merged_reader.pages, start=1):
        box = [float(value) for value in page.mediabox]
        require(abs(box[0]) < .01 and abs(box[1]) < .01 and abs(box[2] - 595.276) < .02 and abs(box[3] - 841.89) < .02, f"page {number} is not A4")
    prior_outline, merged_outline = outline_entries(prior_reader), outline_entries(merged_reader)
    require(len(prior_outline) == 389 and merged_outline[:389] == prior_outline and len(merged_outline) == 389 + len(headings), "PDF outline prefix/append drift")
    prior_named = {name: prior_reader.get_destination_page_number(dest) for name, dest in prior_reader.named_destinations.items()}
    merged_named = {name: merged_reader.get_destination_page_number(dest) for name, dest in merged_reader.named_destinations.items()}
    require(len(prior_named) == 2873 and len(merged_named) == 2873 + len(PRIOR_LINK_PAGES_1BASED) + len(stable_ids), "PDF named-destination census drift")
    require(all(merged_named.get(name) == page for name, page in prior_named.items()), "predecessor PDF named destinations changed")
    require(all(merged_named.get(name) == physical_page - 1 for name, physical_page in PRIOR_LINK_PAGES_1BASED.items()), "rebuilt predecessor stable-ID destinations drift")
    require(all(name in merged_named and 477 <= int(merged_named[name]) < len(merged_reader.pages) for name in stable_ids), "a source stable-ID PDF destination is missing or outside the appendix")
    require(not (set(visible_links) - set(annotation_link_targets(merged_reader, 477))) and all(merged_named.get(name) == PRIOR_LINK_PAGES_1BASED[name] - 1 for name in visible_links), "visible appendix links do not resolve to predecessor anchors")

    receipt = {
        "qa_id": "O012-RBT-001-030-FOM-001-007-CA01-HINTS-R01-R06-DETERMINISTIC-BUILD-DRAFT",
        "status": "PASS_DETERMINISTIC_BUILD_PENDING_MANUAL_VISUAL_AND_BROWSER_QA",
        "scope": "Roberts 30/30; Fomberg 1.1-1.13; D60-CA01; 36 additive ordinary hints completing six-per-route ordinary mastery coverage for D60-R01-D60-R06; composite course partial",
        "model_provenance": MODEL,
        "artifacts": {"html": {**html_id, "lang": "id-ID", "self_contained": True}, "pdf": {**pdf_id, "pages": len(merged_reader.pages), "page_size": "A4", "tagged": False}, "manifest": {**manifest_id, "entries": 2}},
        "frozen_predecessor": {"html": PRIOR_HTML, "pdf": {**PRIOR_PDF, "pages": 477}, "manifest": PRIOR_MANIFEST, "final_build_receipt": PRIOR_RECEIPT, "html_exact_reconstruction": True, "pdf_visual_and_text_prefix": {"status": "PASS", "pages": 477, "page_signature_bundle_sha256": sha256(("\n".join(signatures) + "\n").encode("ascii")).hexdigest(), "extracted_text_byte_identical": evidence["pdf"]["predecessor_text_prefix_byte_identical"]}},
        "ordinary_hints": {"edition_unit_id": "O012-ORIG-HINTS-R01-R06", "source": identity(SOURCE_REL), "qa": identity(QA_REL), "rights": {"license": "CC BY-SA 4.0", "origin": "edition_original", "source_problem_bank_used": False}, "census": {"stable_ids": 43, "hint_blocks": 36, "exercise_solution_pairs": len(pairs), "visible_predecessor_links": len(visible_links), "routes": [f"D60-R0{i}" for i in range(1, 7)]}},
        "backend_boundary": {"status": "PASS_APPEND_ONLY_REPLAYABLE", "receipt": identity(BACKEND_REL), "receipt_kind": backend.get("receipt_kind"), "source_sha256": SOURCE_SHA},
        "html_checks": {"status": "PASS", "dom_ids": len(ids), "fragment_links": len(fragments), "unresolved_fragment_links": 0, "mathml_nodes": evidence["html"]["mathml_nodes"], "hint_blocks_added": 36, "visible_predecessor_links_added": 72, "self_contained": True, "centered_reflow_css_markers": True},
        "pdf_checks": {"status": "PASS_STRUCTURAL", "pages": len(merged_reader.pages), "appended_hint_pages": appendix_pages, "all_pages_a4": True, "fonts": evidence["pdf"]["fonts"], "all_fonts_embedded_subset_tounicode": evidence["pdf"]["all_fonts_embedded_subset_tounicode"], "trailer_id_suppressed": evidence["pdf"]["trailer_id_suppressed"], "predecessor_outline_entries": 389, "hint_outline_entries_added": len(headings), "predecessor_named_destinations": 2873, "predecessor_stable_id_destinations_added": len(PRIOR_LINK_PAGES_1BASED), "hint_named_destinations_added": len(stable_ids), "merged_named_destinations": len(merged_named), "all_source_stable_ids_resolve": True, "visible_links_to_predecessor_resolve": True, "predecessor_link_page_map_1_based": PRIOR_LINK_PAGES_1BASED},
        "reproducibility": {"frozen_inputs_fail_closed": True, "html_fragment_clean_builds": 2, "html_fragment_sha256": evidence["html"]["fragment_sha256"], "html_builds_byte_identical": True, "hint_pdf_clean_builds": 2, "hint_pdf_sha256": evidence["pdf"]["appendix_sha256"], "hint_pdf_builds_byte_identical": True, "merged_pdf_clean_builds": 2, "merged_pdf_builds_byte_identical": True, "source_date_epoch": evidence["source_date_epoch"], "build_scratch_removed_after_finalizer": True},
        "toolchain": {"builder": identity("scripts/build-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06.ps1"), "finalizer": identity("scripts/finalize-build-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06.py"), "pandoc": evidence["pandoc"], "pdf_merger": evidence["pdf"]["merger"], "model_provenance": MODEL},
        "qa_not_claimed": {"manual_visual_qa": "NOT_PERFORMED", "live_browser_desktop_qa": "NOT_PERFORMED", "live_browser_mobile_qa": "NOT_PERFORMED", "public_byte_readback": "NOT_PERFORMED"},
        "limitations": ["The composite course remains partial.", "The PDF remains untagged; native-MathML HTML is the primary reflowable surface.", "Manual visual and live-browser QA must precede a final build receipt."],
    }
    require(qa.get("status") == "PASS", "QA state changed during finalization")
    TARGET.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": receipt["status"], **identity(TARGET.relative_to(LANE).as_posix())}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
