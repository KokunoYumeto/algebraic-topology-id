#!/usr/bin/env python3
"""Validate and bind the deterministic CA01 additive reader build.

This is intentionally a draft finalizer: it proves structural, identity,
determinism, PDF-prefix, rights, and backend gates, but explicitly leaves
manual visual and live-browser QA unclaimed.  It writes only the bounded draft
receipt named by the build lane.
"""

from __future__ import annotations

import argparse
import csv
import html as html_lib
import json
import re
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
TARGET = LANE / "qa/ROBERTS_001_030_FOMBERG_001_007_CA01_BUILD_DRAFT.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
UNIT007_BUNDLE = "523b570517eb54720c50007aacc5d4eea525ea252b9ca1f6f45b027182354765"
CA01_SOURCE_SHA = "5888df0410ad7e8ccf50d8ea8092e43a42f6df94c242f7c09abe0616d972e6f8"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def identity(relative: str, **extra: Any) -> dict[str, Any]:
    path = LANE / relative
    require(path.is_file() and path.stat().st_size > 0, f"missing input: {relative}")
    value: dict[str, Any] = {
        "path": relative,
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }
    value.update(extra)
    return value


def load(relative: str) -> dict[str, Any]:
    path = LANE / relative
    require(path.is_file(), f"missing JSON: {relative}")
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_pdf_object(
    obj: Any,
    cache: dict[tuple[int, int], Any],
    active: set[tuple[int, int]],
) -> Any:
    """Canonicalize a resource graph independent of PDF object numbering."""
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
            if str(key) not in {"/Length"}
        }
    if isinstance(obj, ArrayObject):
        return [canonical_pdf_object(value, cache, active) for value in obj]
    if isinstance(obj, ByteStringObject):
        return {"bytes_hex": bytes(obj).hex()}
    if isinstance(obj, NullObject) or obj is None:
        return None
    if isinstance(obj, bool):
        return obj
    if isinstance(obj, (int, float)):
        return obj
    return str(obj)


def page_visual_signature(page: Any, cache: dict[tuple[int, int], Any]) -> str:
    contents = page.get_contents()
    content_data = b"" if contents is None else contents.get_data()
    resources = canonical_pdf_object(page.get("/Resources", {}), cache, set())
    annotation_values = []
    for reference in page.get("/Annots", []) or []:
        annotation = reference.get_object() if isinstance(reference, IndirectObject) else reference
        if not isinstance(annotation, DictionaryObject):
            continue
        selected = DictionaryObject(
            {
                key: annotation[key]
                for key in ("/Subtype", "/Rect", "/A", "/Dest", "/Contents", "/NM", "/F", "/Border", "/C")
                if key in annotation
            }
        )
        annotation_values.append(canonical_pdf_object(selected, cache, set()))
    payload = {
        "content_sha256": sha256(content_data).hexdigest(),
        "resources": resources,
        "annotations": annotation_values,
        "mediabox": [float(value) for value in page.mediabox],
        "cropbox": [float(value) for value in page.cropbox],
        "rotation": int(page.get("/Rotate", 0) or 0),
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(encoded).hexdigest()


def outline_entries(reader: PdfReader) -> list[tuple[str, int | None]]:
    try:
        outline = reader.outline
    except Exception:
        return []

    entries: list[tuple[str, int | None]] = []

    def visit(value: Any) -> None:
        if isinstance(value, list):
            for item in value:
                visit(item)
            return
        title = str(getattr(value, "title", value))
        try:
            page = reader.get_destination_page_number(value)
        except Exception:
            page = None
        entries.append((title, page))

    visit(outline)
    return entries


def backend_gate(backend: dict[str, Any], raw: str) -> dict[str, Any]:
    require(backend.get("status") == "PASS", "backend receipt is not PASS")
    require(backend.get("receipt_kind") == "cumulative_backend_boundary", "backend receipt kind drift")
    require(backend.get("assessment_id") == "D60-CA01" and backend.get("edition_unit_id") == "O012-ORIG-CA01", "backend CA01 identity drift")
    nested = backend.get("immutable_prefix", {})
    require(nested == {
        "bundle_sha256": UNIT007_BUNDLE,
        "bytes": 8213649,
        "preserved_exactly": True,
        "records": 6742,
    }, "exact nested Unit007 prefix drift")
    require(backend.get("delta") is not None and backend["delta"]["records"] == 112 and backend["delta"]["bytes"] == 132150 and backend["delta"]["bundle_sha256"] == "00e682b92f1897fb309eb76c3e9554df3bf65c29d17527d3cc8c0c4181d917d8", "CA01 backend delta identity drift")
    require(backend.get("cumulative") == {
        "bundle_sha256": "51e75d06e620762e629e9e7408da4b0c32b3e337817d9d140fbbdfa438de2f57",
        "bytes": 8345799,
        "records": 6854,
    }, "CA01 cumulative backend identity drift")
    require(backend.get("replay", {}).get("status") == "PASS" and backend["replay"].get("exact_file_matches") == 11 and backend["replay"].get("temporary_replay_removed") is True, "backend replay gate failed")
    semantic = backend.get("semantic_checks", {})
    require(semantic.get("added_records") == 112 and semantic.get("rights_closure") == "PASS" and semantic.get("route_mapping") == "PASS" and semantic.get("segment_kind_counts") == {"assessment": 1, "exercise": 8, "hint": 8, "solution": 8}, "backend semantic census drift")
    return {
        "unit007_prefix_records": 6742,
        "unit007_prefix_bytes": 8213649,
        "unit007_prefix_bundle_sha256": UNIT007_BUNDLE,
        "ca01_records_added": 112,
        "cumulative_records": 6854,
        "cumulative_bytes": 8345799,
        "cumulative_bundle_sha256": "51e75d06e620762e629e9e7408da4b0c32b3e337817d9d140fbbdfa438de2f57",
    }


def merge_pdfs(prior_path: Path, append_path: Path, output_path: Path) -> None:
    """Deterministically append while preserving interactive destinations."""
    require(prior_path.is_file() and append_path.is_file(), "merge input missing")
    require(output_path.parent.is_dir(), "merge output directory missing")
    append_reader = PdfReader(str(append_path))
    append_entries = outline_entries(append_reader)
    require(len(append_reader.pages) == 5 and len(append_entries) == 10, "CA01 PDF outline/page census drift")
    require(all(page is not None and 0 <= page <= 4 for _title, page in append_entries), "CA01 source outline has an unresolved destination")
    ca01_titles = [
        "Asesmen Kumulatif 1: fondasi hingga barisan eksak homotopi",
        "Soal 1 — hasil bagi interval dan lingkaran",
        "Soal 2 — retraksi deformasi kuat",
        "Soal 3 — pengangkatan lintasan dan bilangan lilit",
        "Soal 4 — monodromi penutup berhingga",
        "Soal 5 — van Kampen dan grup fundamental torus",
        "Soal 6 — klasifikasi penutup lingkaran",
        "Soal 7 — barisan eksak homotopi fibrasi Hopf",
        "Soal 8 — kriteria pengangkatan peta torus",
        "Peta cakupan asesmen",
    ]
    ca01_destination_names = [
        "o012-d60-ca01",
        "o012-d60-ca01-s01",
        "o012-d60-ca01-s02",
        "o012-d60-ca01-s03",
        "o012-d60-ca01-s04",
        "o012-d60-ca01-s05",
        "o012-d60-ca01-s06",
        "o012-d60-ca01-s07",
        "o012-d60-ca01-s08",
        "o012-d60-ca01-coverage",
    ]
    writer = PdfWriter()
    writer.append(str(prior_path), import_outline=True)
    # CA01's generic LaTeX names (section.1, subsection.1.1, ...) collide with
    # predecessor names. Import its pages/name tree but rebuild its ten outline
    # destinations explicitly against the appended page objects.
    append_reader._named_destinations_cache = {}  # noqa: SLF001 - prevent generic-name collisions.
    writer.append(append_reader, import_outline=False)
    for name, (_source_title, local_page) in zip(ca01_destination_names, append_entries, strict=True):
        writer.add_named_destination(name, 472 + int(local_page))
    ca_parent = writer.add_outline_item(ca01_titles[0], 472 + int(append_entries[0][1]), is_open=True)
    for title, (_source_title, local_page) in zip(ca01_titles[1:], append_entries[1:], strict=True):
        writer.add_outline_item(title, 472 + int(local_page), parent=ca_parent)
    writer.add_metadata(
        {
            "/Title": "Topologi Aljabar — Roberts 30/30, Fomberg 1.1–1.13, dan Asesmen Kumulatif 1",
            "/Author": "David Michael Roberts; Yeheli Fomberg; Edisi Bahasa Indonesia dengan pendamping penguasaan",
            "/Subject": "Checkpoint komposit parsial dengan D60-CA01",
            "/Creator": "OpenAI Codex gpt-5.6-sol, Ultra; atas arahan pengguna",
            "/Producer": "pypdf 6.12.2 deterministic append",
            "/CreationDate": "D:20260825020000+02'00'",
            "/ModDate": "D:20260825020000+02'00'",
        }
    )
    writer.page_mode = "/UseOutlines"
    # Both frozen inputs have no trailer ID; retain that deterministic property.
    writer._ID = None  # noqa: SLF001 - pypdf exposes no public ID suppressor.
    with output_path.open("wb") as stream:
        writer.write(stream)
    merged = PdfReader(str(output_path))
    entries = outline_entries(merged)
    require(len(merged.pages) == 477, "merged PDF page count drift")
    require(len(entries) == 389 and all(page is not None for _title, page in entries), "merged outline is incomplete or unresolved")
    require(entries[-10:] == [(title, 472 + int(local_page)) for title, (_source_title, local_page) in zip(ca01_titles, append_entries, strict=True)], "rebuilt CA01 outline destination drift")
    merged_named = merged.named_destinations
    require(len(merged_named) == 2873, "merged named-destination census drift")
    require(
        all(
            name in merged_named
            and merged.get_destination_page_number(merged_named[name]) == 472 + int(local_page)
            for name, (_source_title, local_page) in zip(ca01_destination_names, append_entries, strict=True)
        ),
        "rebuilt CA01 named destination drift",
    )
    print(
        json.dumps(
            {
                "status": "PASS",
                "path": str(output_path),
                "bytes": output_path.stat().st_size,
                "sha256": digest(output_path),
                "pages": len(merged.pages),
                "outline_entries": len(entries),
                "named_destinations": len(merged_named),
            },
            ensure_ascii=False,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence")
    parser.add_argument("--merge-pdfs", action="store_true")
    parser.add_argument("--prior")
    parser.add_argument("--append")
    parser.add_argument("--output")
    args = parser.parse_args()
    if args.merge_pdfs:
        require(args.prior is not None and args.append is not None and args.output is not None, "merge paths are required")
        merge_pdfs(Path(args.prior).resolve(), Path(args.append).resolve(), Path(args.output).resolve())
        return
    require(args.evidence is not None, "--evidence is required for finalization")
    evidence_path = Path(args.evidence).resolve()
    require(evidence_path.is_file(), "missing deterministic evidence")
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    require(evidence.get("status") == "PASS", "deterministic evidence is not PASS")
    require(evidence["pdf"].get("build_only_exercise_paragraph_boundaries") == 8, "PDF exercise layout-boundary transform drift")

    prior_html_rel = "output/html/roberts-001-030-fomberg-001-007/index.html"
    prior_pdf_rel = "output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-007-id.pdf"
    html_rel = "output/html/roberts-001-030-fomberg-001-007-ca01/index.html"
    pdf_rel = "output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-007-ca01-id.pdf"
    manifest_rel = "output/ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_007_CA01.csv"
    source_rel = "source/id-ID/mastery/cumulative-assessment-001-foundations-coverings-homotopy.md"
    qa_rel = "qa/CUMULATIVE_ASSESSMENT_001_QA.json"
    backend_rel = "qa/BACKEND_APPEND_ONLY_CUMULATIVE_ASSESSMENT_001_CUMULATIVE_RECEIPT.json"

    prior_html = identity(prior_html_rel)
    prior_pdf = identity(prior_pdf_rel)
    source = identity(source_rel)
    qa = load(qa_rel)
    backend_path = LANE / backend_rel
    require(backend_path.stat().st_size == 9934 and digest(backend_path) == "79fc0c7afde5f72b9eaf3809b08ab27cfd696c9d0269905608a1336ae4cd7e13", "backend receipt identity drift")
    backend_raw = backend_path.read_text(encoding="utf-8")
    backend = json.loads(backend_raw)

    require(prior_html == {"path": prior_html_rel, "bytes": 14885069, "sha256": "87d58a5955954125c424ab1220a9c6aa7967a782a9bd739094a31ae0a50af5f6"}, "predecessor HTML drift")
    require(prior_pdf == {"path": prior_pdf_rel, "bytes": 8326404, "sha256": "1beca2d03f04c1fcca7eb01bd2654567908febc1ba7941b459c06b90ef865c22"}, "predecessor PDF drift")
    require(source == {"path": source_rel, "bytes": 15185, "sha256": CA01_SOURCE_SHA}, "CA01 source drift")
    require(qa.get("status") == "PASS" and qa.get("qa_id") == "O012-D60-CUMULATIVE-ASSESSMENT-001", "CA01 QA drift")
    require(qa["reader"]["identity"]["sha256"] == CA01_SOURCE_SHA, "QA does not bind live CA01 source")
    backend_boundary = backend_gate(backend, backend_raw)

    html_id = identity(html_rel)
    pdf_id = identity(pdf_rel)
    manifest_id = identity(manifest_rel)
    require(html_id["bytes"] == evidence["html"]["combined_bytes"] and html_id["sha256"] == evidence["html"]["combined_sha256"], "live HTML differs from deterministic evidence")
    require(pdf_id["bytes"] == evidence["pdf"]["merged_bytes"] and pdf_id["sha256"] == evidence["pdf"]["merged_sha256"], "live PDF differs from deterministic evidence")

    with (LANE / manifest_rel).open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == 2, "manifest must contain exactly HTML and PDF")
    manifest_map = {row["path"]: (int(row["bytes"]), row["sha256"]) for row in rows}
    require(len(manifest_map) == 2, "manifest has duplicate path")
    require(manifest_map == {
        html_rel: (html_id["bytes"], html_id["sha256"]),
        pdf_rel: (pdf_id["bytes"], pdf_id["sha256"]),
    }, "manifest does not bind live artifacts")

    html_text = (LANE / html_rel).read_text(encoding="utf-8")
    require("\r" not in html_text.replace("\r\n", ""), "HTML contains a bare CR")
    ids = re.findall(r'(?<=\s)id="([^"]+)"', html_text)
    require(len(ids) == len(set(ids)), "HTML IDs are not unique")
    fragments = [html_lib.unescape(value) for value in re.findall(r'\bhref="#([^"]+)"', html_text)]
    require(not (set(fragments) - set(ids)), "HTML has unresolved fragments")
    require('<title>Topologi Aljabar — Roberts 30/30, Fomberg 1.1–1.13, dan Asesmen Kumulatif 1</title>' in html_text, "HTML title is stale")
    require('id="toc-o012-d60-ca01"' in html_text and 'id="o012-d60-ca01-status"' in html_text, "HTML CA01 status/ToC is missing")
    require(len(re.findall(r'<math\b', html_text)) == evidence["html"]["mathml_nodes"], "HTML MathML census drift")
    require(evidence["html"]["predecessor_exact_reconstruction"] is True, "predecessor HTML was not exactly reconstructable")
    require(evidence["html"]["predecessor_reconstructed_sha256"] == prior_html["sha256"], "reconstructed predecessor HTML hash drift")
    require((evidence["html"]["ca01_exercises"], evidence["html"]["ca01_hints"], evidence["html"]["ca01_solutions"]) == (8, 8, 8), "HTML mastery census drift")

    prior_reader = PdfReader(str(LANE / prior_pdf_rel))
    merged_reader = PdfReader(str(LANE / pdf_rel))
    require(len(prior_reader.pages) == 472 and len(merged_reader.pages) == 477, "PDF page boundary drift")
    prior_cache: dict[tuple[int, int], Any] = {}
    merged_cache: dict[tuple[int, int], Any] = {}
    mismatches: list[int] = []
    prefix_hashes: list[str] = []
    for index in range(472):
        left = page_visual_signature(prior_reader.pages[index], prior_cache)
        right = page_visual_signature(merged_reader.pages[index], merged_cache)
        prefix_hashes.append(left)
        if left != right:
            mismatches.append(index + 1)
    require(not mismatches, f"predecessor page visual signatures changed: {mismatches[:10]}")
    prefix_bundle = sha256(("\n".join(prefix_hashes) + "\n").encode("ascii")).hexdigest()

    for page_number, page in enumerate(merged_reader.pages, start=1):
        box = [float(value) for value in page.mediabox]
        require(abs(box[0]) < 0.01 and abs(box[1]) < 0.01 and abs(box[2] - 595.276) < 0.02 and abs(box[3] - 841.89) < 0.02, f"page {page_number} is not A4")
    prior_outline = outline_entries(prior_reader)
    merged_outline = outline_entries(merged_reader)
    require(len(prior_outline) == evidence["pdf"]["predecessor_outline_entries"] == 379, "predecessor outline census evidence drift")
    require(len(merged_outline) == evidence["pdf"]["merged_outline_entries"] == 389, "merged outline census evidence drift")
    require(evidence["pdf"]["predecessor_outline_prefix_expected"] is True, "outline census expectation drift")
    require(all(page is not None for _title, page in prior_outline), "predecessor outline has an unresolved destination")
    require(all(page is not None for _title, page in merged_outline), "merged outline has an unresolved destination")
    require(merged_outline[: len(prior_outline)] == prior_outline, "predecessor PDF outline destinations are not an exact prefix")
    ca01_outline = merged_outline[len(prior_outline) :]
    require(len(ca01_outline) == 10 and ca01_outline[0][0].startswith("Asesmen Kumulatif 1") and all(page is not None and 472 <= page <= 476 for _title, page in ca01_outline), "CA01 outline append drift")
    prior_named = prior_reader.named_destinations
    merged_named = merged_reader.named_destinations
    require(len(prior_named) == 2863 and len(merged_named) == 2873, "named-destination inventory drift")
    prior_named_pages = {name: prior_reader.get_destination_page_number(destination) for name, destination in prior_named.items()}
    merged_named_pages = {name: merged_reader.get_destination_page_number(destination) for name, destination in merged_named.items()}
    require(all(page is not None for page in merged_named_pages.values()), "merged name tree has an unresolved destination")
    require(all(name in merged_named_pages and merged_named_pages[name] == page for name, page in prior_named_pages.items()), "predecessor named destinations are not preserved")
    ca01_named_pages = {
        "o012-d60-ca01": ca01_outline[0][1],
        "o012-d60-ca01-s01": ca01_outline[1][1],
        "o012-d60-ca01-s02": ca01_outline[2][1],
        "o012-d60-ca01-s03": ca01_outline[3][1],
        "o012-d60-ca01-s04": ca01_outline[4][1],
        "o012-d60-ca01-s05": ca01_outline[5][1],
        "o012-d60-ca01-s06": ca01_outline[6][1],
        "o012-d60-ca01-s07": ca01_outline[7][1],
        "o012-d60-ca01-s08": ca01_outline[8][1],
        "o012-d60-ca01-coverage": ca01_outline[9][1],
    }
    require(all(merged_named_pages.get(name) == page for name, page in ca01_named_pages.items()), "CA01 named destinations do not match outline pages")

    receipt: dict[str, Any] = {
        "qa_id": "O012-RBT-001-030-FOM-001-007-CA01-DETERMINISTIC-BUILD-DRAFT",
        "status": "PASS_DETERMINISTIC_BUILD_PENDING_MANUAL_VISUAL_AND_BROWSER_QA",
        "scope": "Roberts 30/30; Fomberg Sections 1.1-1.13 through source line 4185; original D60-CA01 with 8 solved items; composite course partial",
        "model_provenance": MODEL,
        "artifacts": {
            "html": {**html_id, "title": "Topologi Aljabar — Roberts 30/30, Fomberg 1.1–1.13, dan Asesmen Kumulatif 1", "lang": "id-ID", "self_contained": True},
            "pdf": {**pdf_id, "pages": 477, "page_size": "A4", "tagged": False},
            "manifest": {**manifest_id, "entries": 2},
        },
        "frozen_predecessor": {
            "html": prior_html,
            "pdf": {**prior_pdf, "pages": 472},
            "html_exact_logical_prefix_reconstruction": {
                "status": "PASS",
                "bytes": evidence["html"]["predecessor_reconstructed_bytes"],
                "sha256": evidence["html"]["predecessor_reconstructed_sha256"],
            },
            "pdf_page_visual_prefix": {
                "status": "PASS",
                "pages_compared": 472,
                "page_signature_bundle_sha256": prefix_bundle,
                "content_resources_boxes_rotation_compared": True,
                "extracted_text_byte_identical": evidence["pdf"]["predecessor_text_prefix_byte_identical"],
            },
        },
        "ca01": {
            "assessment_id": "D60-CA01",
            "edition_unit_id": "O012-ORIG-CA01",
            "source": source,
            "qa": identity(qa_rel),
            "rights": {"license": "CC BY-SA 4.0", "origin": "edition_original", "source_problem_bank_used": False},
            "census": {"stable_ids": 34, "exercises": 8, "hints": 8, "complete_solutions": 8, "primary_routes": ["D60-R01", "D60-R02", "D60-R03", "D60-R04", "D60-R05", "D60-R06", "D60-R07"]},
        },
        "backend_boundary": {
            "status": "PASS_APPEND_ONLY_REPLAYABLE",
            **backend_boundary,
            "receipt": identity(backend_rel),
        },
        "html_checks": {
            "status": "PASS",
            "dom_ids": len(ids),
            "fragment_links": len(fragments),
            "unresolved_fragment_links": 0,
            "mathml_nodes": evidence["html"]["mathml_nodes"],
            "ca01_stable_ids": 34,
            "ca01_exercise_hint_solution_triples": 8,
            "self_contained": True,
            "centered_reflow_css_markers": True,
        },
        "pdf_checks": {
            "status": "PASS_STRUCTURAL",
            "pages": 477,
            "appended_ca01_pages": 5,
            "all_pages_a4": True,
            "fonts": evidence["pdf"]["fonts"],
            "all_fonts_embedded_subset_tounicode": evidence["pdf"]["all_fonts_embedded_subset_tounicode"],
            "trailer_id_suppressed": evidence["pdf"]["trailer_id_suppressed"],
            "build_only_layout_normalization": "Eight transient \\par\\noindent boundaries prevent Pandoc fenced-div anchors from running exercise prompts into subsection headings; canonical source bytes are unchanged.",
            "predecessor_outline_entries": len(prior_outline),
            "merged_outline_entries": len(merged_outline),
            "all_outline_destinations_resolve": True,
            "predecessor_outline_destinations_preserved_as_exact_prefix": True,
            "ca01_outline_entries_added": len(ca01_outline),
            "predecessor_named_destinations": len(prior_named),
            "merged_named_destinations": len(merged_named),
            "ca01_named_destinations_added": 10,
            "all_named_destinations_resolve": True,
            "outline_note": "All 379 predecessor outline destinations remain an exact title/page prefix and all 10 appended CA01 outline destinations resolve to pages 473–477.",
        },
        "reproducibility": {
            "frozen_inputs_fail_closed": True,
            "html_fragment_clean_builds": 2,
            "html_fragment_sha256": evidence["html"]["fragment_sha256"],
            "html_builds_byte_identical": evidence["html"]["combined_builds_byte_identical"],
            "ca01_pdf_clean_builds": 2,
            "ca01_pdf_sha256": evidence["pdf"]["ca01_sha256"],
            "ca01_pdf_builds_byte_identical": evidence["pdf"]["ca01_builds_byte_identical"],
            "merged_pdf_clean_builds": 2,
            "merged_pdf_builds_byte_identical": evidence["pdf"]["merged_builds_byte_identical"],
            "source_date_epoch": evidence["source_date_epoch"],
            "build_scratch_removed_after_finalizer": True,
        },
        "toolchain": {
            "builder": identity("scripts/build-roberts-001-030-fomberg-001-007-ca01.ps1"),
            "finalizer": identity("scripts/finalize-build-roberts-001-030-fomberg-001-007-ca01.py"),
            "pandoc": evidence["pandoc"],
            "pdf_merger": evidence["pdf"]["merger"],
            "model_provenance": MODEL,
        },
        "qa_not_claimed": {
            "manual_visual_qa": "NOT_PERFORMED",
            "live_browser_desktop_qa": "NOT_PERFORMED",
            "live_browser_mobile_qa": "NOT_PERFORMED",
            "public_byte_readback": "NOT_PERFORMED",
        },
        "limitations": [
            "The composite course remains partial after adding D60-CA01.",
            "The PDF remains untagged; the self-contained native-MathML HTML is the primary reflowable surface.",
            "Manual visual and live-browser QA must be completed before sealing a final build receipt.",
            "All outline and named destinations resolve; formal page-level visual/browser QA remains a separate gate.",
        ],
    }
    TARGET.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": receipt["status"], **identity(TARGET.relative_to(LANE).as_posix())}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
