#!/usr/bin/env python3
"""Deterministically append the CA02/CA03 PDF surface to the frozen reader."""

from __future__ import annotations

import argparse
import json
import re
from hashlib import sha256
from pathlib import Path
from typing import Any

import pypdf
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ByteStringObject, DictionaryObject, IndirectObject, StreamObject


PRIOR_BYTES = 8_592_243
PRIOR_SHA256 = "4da7f1368c17423cd6845c36b7d5190dac98d515ecbd32467c0c59961dd9afcb"
PRIOR_PAGES = 482
PRIOR_OUTLINE = 396
PRIOR_NAMED = 2_988
PYPDF_VERSION = "6.12.2"
SCRATCH_BASENAME = "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-build"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _framed_digest(tag: bytes, parts: list[bytes]) -> bytes:
    hasher = sha256()
    hasher.update(tag)
    for part in parts:
        hasher.update(len(part).to_bytes(8, "big"))
        hasher.update(part)
    return hasher.digest()


def _semantic_object_digest(
    value: Any,
    page_references: dict[tuple[int, int], int],
    memo: dict[tuple[int, int], bytes],
    active: set[tuple[int, int]],
) -> bytes:
    """Hash PDF object semantics without depending on rewritten object numbers."""
    if isinstance(value, IndirectObject):
        key = (value.idnum, value.generation)
        if key in page_references:
            return _framed_digest(b"PAGE", [str(page_references[key]).encode("ascii")])
        if key in memo:
            return memo[key]
        if key in active:
            return _framed_digest(b"CYCLE", [])
        active.add(key)
        result = _framed_digest(
            b"REF",
            [_semantic_object_digest(value.get_object(), page_references, memo, active)],
        )
        active.remove(key)
        memo[key] = result
        return result
    if isinstance(value, StreamObject):
        items: list[bytes] = []
        for key in sorted((str(key) for key in value.keys())):
            if key == "/Length":
                continue
            items.extend(
                (
                    key.encode("utf-8"),
                    _semantic_object_digest(value[key], page_references, memo, active),
                )
            )
        items.append(sha256(value.get_data()).digest())
        return _framed_digest(b"STREAM", items)
    if isinstance(value, DictionaryObject):
        items = []
        is_page = str(value.get("/Type", "")) == "/Page"
        for key in sorted((str(key) for key in value.keys())):
            if key == "/Length" or (is_page and key == "/Parent"):
                continue
            items.extend(
                (
                    key.encode("utf-8"),
                    _semantic_object_digest(value[key], page_references, memo, active),
                )
            )
        return _framed_digest(b"DICT", items)
    if isinstance(value, (list, tuple)):
        return _framed_digest(
            b"ARRAY",
            [_semantic_object_digest(item, page_references, memo, active) for item in value],
        )
    if isinstance(value, ByteStringObject):
        return _framed_digest(b"BYTES", [bytes(value)])
    if isinstance(value, bytes):
        return _framed_digest(b"BYTES", [value])
    if value is None:
        return _framed_digest(b"NONE", [])
    return _framed_digest(
        type(value).__name__.encode("ascii", errors="backslashreplace"),
        [str(value).encode("utf-8", errors="surrogatepass")],
    )


def page_structure_hashes(reader: PdfReader, page_count: int) -> list[str]:
    require(0 <= page_count <= len(reader.pages), "invalid structural page-hash range")
    page_references: dict[tuple[int, int], int] = {}
    for index, page in enumerate(reader.pages):
        reference = page.indirect_reference
        require(reference is not None, f"page {index + 1} has no indirect reference")
        page_references[(reference.idnum, reference.generation)] = index
    memo: dict[tuple[int, int], bytes] = {}
    return [
        _semantic_object_digest(reader.pages[index], page_references, memo, set()).hex()
        for index in range(page_count)
    ]


def aggregate_hash(values: list[str]) -> str:
    return sha256((("\n".join(values)) + "\n").encode("ascii")).hexdigest()


def outline_entries(reader: PdfReader) -> list[tuple[str, int | None]]:
    entries: list[tuple[str, int | None]] = []

    def visit(value: Any) -> None:
        if isinstance(value, list):
            for item in value:
                visit(item)
            return
        title = getattr(value, "title", None)
        if title is None and hasattr(value, "get"):
            title = value.get("/Title")
        if title is not None:
            try:
                page = reader.get_destination_page_number(value)
            except Exception:
                page = None
            entries.append((str(title), page))

    visit(reader.outline)
    return entries


def source_contract(path: Path, token: str) -> tuple[list[tuple[int, str, str]], list[str]]:
    text = path.read_text(encoding="utf-8")
    headings: list[tuple[int, str, str]] = []
    for match in re.finditer(r"(?m)^(#{1,2})\s+(.+?)\s+\{#(o012-d60-" + token + r"(?:-[a-z0-9]+)*)\}\s*$", text):
        headings.append((len(match.group(1)), match.group(2).strip(), match.group(3)))
    ids = re.findall(r"#(o012-d60-" + token + r"(?:-[a-z0-9]+)*)\b", text)
    require(len(ids) == len(set(ids)) == 34, f"{token} stable-ID inventory is not 34 unique IDs")
    require(len(headings) == 10 and headings[0][0] == 1 and all(level == 2 for level, _title, _ident in headings[1:]), f"{token} heading hierarchy is not 1+9")
    require({ident for _level, _title, ident in headings}.issubset(ids), f"{token} heading IDs are absent from full source inventory")
    return headings, ids


def link_targets(reader: PdfReader, first_page: int) -> list[str]:
    targets: list[str] = []
    for page in reader.pages[first_page:]:
        for annotation_ref in page.get("/Annots", []):
            annotation = annotation_ref.get_object()
            if annotation.get("/Subtype") != "/Link":
                continue
            action = annotation.get("/A")
            if action is None:
                continue
            action = action.get_object() if hasattr(action, "get_object") else action
            if action.get("/S") != "/GoTo":
                continue
            destination = action.get("/D")
            if isinstance(destination, str):
                targets.append(destination.lstrip("/"))
            elif isinstance(destination, ByteStringObject):
                targets.append(bytes(destination).decode("utf-8").lstrip("/"))
    return targets


def merge(
    prior_path: Path,
    append_path: Path,
    output_path: Path,
    source_a: Path,
    source_b: Path,
    scratch_root: Path,
) -> dict[str, Any]:
    require(pypdf.__version__ == PYPDF_VERSION, f"expected pypdf {PYPDF_VERSION}; got {pypdf.__version__}")
    require(prior_path.is_file() and append_path.is_file(), "PDF input missing")
    require(source_a.is_file() and source_b.is_file(), "Markdown source input missing")
    require(scratch_root.is_dir() and scratch_root.name == SCRATCH_BASENAME, "invalid bounded scratch root")
    require(output_path.parent == scratch_root and output_path.suffix.lower() == ".pdf", "PDF output is not a direct child of bounded scratch")
    require(output_path not in {prior_path, append_path, source_a, source_b}, "PDF output aliases an input")
    require(output_path.parent.is_dir(), "PDF output parent missing")
    require(prior_path.stat().st_size == PRIOR_BYTES and digest(prior_path) == PRIOR_SHA256, "frozen predecessor PDF identity drift")
    headings_a, ids_a = source_contract(source_a, "ca02")
    headings_b, ids_b = source_contract(source_b, "ca03")
    stable_ids = ids_a + ids_b
    require(len(stable_ids) == len(set(stable_ids)) == 68, "combined source stable-ID inventory is not 68 unique IDs")

    prior = PdfReader(str(prior_path))
    appendix = PdfReader(str(append_path))
    prior_page_structure = page_structure_hashes(prior, PRIOR_PAGES)
    prior_outline = outline_entries(prior)
    appendix_outline = outline_entries(appendix)
    require(len(prior.pages) == PRIOR_PAGES and len(prior_outline) == PRIOR_OUTLINE, "predecessor PDF page/outline boundary drift")
    require(len(prior.named_destinations) == PRIOR_NAMED, "predecessor named-destination boundary drift")
    require(len(appendix.pages) > 0, "appendix PDF is empty")
    require(len(appendix_outline) == 20, "appendix outline is not the 20 source headings")
    expected_titles = [title for _level, title, _ident in headings_a + headings_b]
    require([title for title, _page in appendix_outline] == expected_titles, "appendix outline titles differ from sources")
    require(all(page is not None and 0 <= page < len(appendix.pages) for _title, page in appendix_outline), "appendix outline contains unresolved pages")

    appendix_named = appendix.named_destinations
    appendix_named_pages = {name: appendix.get_destination_page_number(destination) for name, destination in appendix_named.items()}
    require(all(name in appendix_named_pages and appendix_named_pages[name] is not None for name in stable_ids), "appendix lacks one or more of the 68 stable-ID destinations")
    prior_named_pages = {name: prior.get_destination_page_number(destination) for name, destination in prior.named_destinations.items()}
    require(set(stable_ids).isdisjoint(prior_named_pages), "new stable-ID collides with predecessor name tree")

    writer = PdfWriter()
    writer.append(str(prior_path), import_outline=True)
    appendix._named_destinations_cache = {}  # noqa: SLF001 - suppress generic LaTeX name import.
    writer.append(appendix, import_outline=False)
    for name in stable_ids:
        writer.add_named_destination(name, PRIOR_PAGES + int(appendix_named_pages[name]))

    offset = 0
    for headings in (headings_a, headings_b):
        root_title = headings[0][1]
        root_local_page = int(appendix_outline[offset][1])
        parent = writer.add_outline_item(root_title, PRIOR_PAGES + root_local_page, is_open=True)
        for (_level, title, _ident), (_pdf_title, local_page) in zip(headings[1:], appendix_outline[offset + 1 : offset + 10], strict=True):
            writer.add_outline_item(title, PRIOR_PAGES + int(local_page), parent=parent)
        offset += 10

    writer.add_metadata({
        "/Title": "Topologi Aljabar — Roberts 30/30, Fomberg 1.1–1.13, dan Asesmen Kumulatif 1–3",
        "/Author": "David Michael Roberts; Yeheli Fomberg; edisi Bahasa Indonesia dengan pendamping penguasaan",
        "/Subject": "Checkpoint komposit parsial dengan 84 soal rute dan 24 soal asesmen kumulatif bersolusi",
        "/Creator": f"{MODEL}; atas arahan pengguna",
        "/Producer": "pypdf deterministic append",
        "/CreationDate": "D:20260827000000+02'00'",
        "/ModDate": "D:20260827000000+02'00'",
    })
    writer.page_mode = "/UseOutlines"
    writer._ID = None  # noqa: SLF001 - deterministic trailer without /ID.
    with output_path.open("wb") as stream:
        writer.write(stream)

    merged = PdfReader(str(output_path))
    merged_prefix_structure = page_structure_hashes(merged, PRIOR_PAGES)
    merged_outline = outline_entries(merged)
    merged_named_pages = {name: merged.get_destination_page_number(destination) for name, destination in merged.named_destinations.items()}
    require(len(merged.pages) == PRIOR_PAGES + len(appendix.pages), "merged PDF page count drift")
    require(merged_prefix_structure == prior_page_structure, "predecessor per-page PDF structure changed")
    require(merged_outline[:PRIOR_OUTLINE] == prior_outline and len(merged_outline) == PRIOR_OUTLINE + 20, "predecessor outline is not exact prefix")
    require(len(merged_named_pages) == PRIOR_NAMED + 68, "merged named-destination census drift")
    require(all(merged_named_pages.get(name) == page for name, page in prior_named_pages.items()), "predecessor named destinations changed")
    require(all(merged_named_pages.get(name) == PRIOR_PAGES + int(appendix_named_pages[name]) for name in stable_ids), "new stable destinations changed")
    external_targets = [target for target in link_targets(merged, PRIOR_PAGES) if target not in stable_ids]
    require(not external_targets, f"appendix contains unresolved/external PDF GoTo targets: {sorted(set(external_targets))}")
    return {
        "status": "PASS",
        "bytes": output_path.stat().st_size,
        "sha256": digest(output_path),
        "pages": len(merged.pages),
        "appendix_pages": len(appendix.pages),
        "pypdf": pypdf.__version__,
        "outline_entries": len(merged_outline),
        "named_destinations": len(merged_named_pages),
        "stable_id_destinations_added": 68,
        "predecessor_page_count": PRIOR_PAGES,
        "predecessor_page_structure_algorithm": "sha256-pypdf-semantic-v1",
        "predecessor_page_structure_aggregate_sha256": aggregate_hash(prior_page_structure),
        "predecessor_page_structure_sha256": prior_page_structure,
        "predecessor_outline_exact_prefix": True,
        "predecessor_named_destinations_preserved": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prior", required=True)
    parser.add_argument("--append", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--source-a", required=True)
    parser.add_argument("--source-b", required=True)
    parser.add_argument("--scratch-root", required=True)
    args = parser.parse_args()
    result = merge(
        *(Path(value).resolve() for value in (args.prior, args.append, args.output, args.source_a, args.source_b, args.scratch_root))
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
