#!/usr/bin/env python3
"""Deterministically append computation Lab 2 to the frozen 511-page reader."""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
from hashlib import sha256
from pathlib import Path
from typing import Any

import pypdf
from pypdf import PdfReader, PdfWriter


PRIOR_BYTES = 9_193_942
PRIOR_SHA256 = "722fa7f6c3aa20d1a4c52257d3127fa500bbaf6aad66f64d62177718cd53d128"
PRIOR_PAGES = 511
PRIOR_OUTLINE = 433
PRIOR_NAMED = 3_080
PYPDF_VERSION = "6.12.2"
SCRATCH_BASENAME = "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-build"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def load_base():
    path = Path(__file__).resolve().parent / "merge-cumulative-assessments-002-003.py"
    spec = importlib.util.spec_from_file_location("o012_pdf_merge_base", path)
    require(spec is not None and spec.loader is not None, "cannot load frozen PDF merge helpers")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_contract(path: Path) -> tuple[list[tuple[int, str, str]], list[str]]:
    text = path.read_text(encoding="utf-8")
    headings = [
        (len(match.group(1)), match.group(2).strip(), match.group(3))
        for match in re.finditer(
            r"(?m)^(#{1,2})\s+(.+?)\s+\{#(o012-d60-lab02(?:-[a-z0-9]+)*)\}\s*$",
            text,
        )
    ]
    ids = re.findall(r"#(o012-d60-lab02(?:-[a-z0-9]+)*)\b", text)
    require(len(ids) == len(set(ids)) == 25, "Lab 2 stable-ID inventory is not 25 unique IDs")
    require(len(headings) == 18, "Lab 2 heading inventory is not 18")
    require(headings[0][0] == 1 and sum(level == 1 for level, _title, _ident in headings) == 2, "Lab 2 heading hierarchy lacks its two top-level surfaces")
    require(all(level in (1, 2) for level, _title, _ident in headings), "Lab 2 heading level is outside 1-2")
    require({ident for _level, _title, ident in headings}.issubset(ids), "heading ID absent from full stable-ID inventory")
    return headings, ids


def merge(prior_path: Path, append_path: Path, output_path: Path, source: Path, scratch_root: Path) -> dict[str, Any]:
    require(pypdf.__version__ == PYPDF_VERSION, f"expected pypdf {PYPDF_VERSION}; got {pypdf.__version__}")
    require(prior_path.is_file() and append_path.is_file() and source.is_file(), "PDF/source input missing")
    require(scratch_root.is_dir() and scratch_root.name == SCRATCH_BASENAME, "invalid bounded scratch root")
    require(output_path.parent == scratch_root and output_path.suffix.lower() == ".pdf", "output is not a direct PDF child of bounded scratch")
    require(output_path not in {prior_path, append_path, source}, "output aliases an input")
    require(prior_path.stat().st_size == PRIOR_BYTES and digest(prior_path) == PRIOR_SHA256, "frozen predecessor PDF identity drift")
    headings, stable_ids = source_contract(source)
    base = load_base()

    prior = PdfReader(str(prior_path))
    appendix = PdfReader(str(append_path))
    prior_page_structure = base.page_structure_hashes(prior, PRIOR_PAGES)
    prior_outline = base.outline_entries(prior)
    appendix_outline = base.outline_entries(appendix)
    require(len(prior.pages) == PRIOR_PAGES and len(prior_outline) == PRIOR_OUTLINE, "predecessor PDF page/outline boundary drift")
    require(len(prior.named_destinations) == PRIOR_NAMED, "predecessor named-destination boundary drift")
    require(len(appendix.pages) > 0, "appendix PDF is empty")
    require(len(appendix_outline) == len(headings), "appendix outline does not match 18 source headings")
    source_outline_titles = [title for _level, title, _ident in headings]
    appendix_outline_titles = [title for title, _page in appendix_outline]
    require(
        source_outline_titles == appendix_outline_titles,
        f"appendix outline titles differ from source: source={source_outline_titles!r}; appendix={appendix_outline_titles!r}",
    )
    require(all(page is not None and 0 <= page < len(appendix.pages) for _title, page in appendix_outline), "appendix outline has unresolved pages")

    appendix_named = appendix.named_destinations
    appendix_named_pages = {name: appendix.get_destination_page_number(destination) for name, destination in appendix_named.items()}
    require(all(name in appendix_named_pages and appendix_named_pages[name] is not None for name in stable_ids), "appendix lacks one or more Lab 2 destinations")
    prior_named_pages = {name: prior.get_destination_page_number(destination) for name, destination in prior.named_destinations.items()}
    require(set(stable_ids).isdisjoint(prior_named_pages), "Lab 2 stable ID collides with predecessor")

    external_targets = [target for target in base.link_targets(appendix, 0) if target not in stable_ids and target not in prior_named_pages]
    require(not external_targets, f"appendix contains unresolved PDF GoTo targets: {sorted(set(external_targets))}")

    writer = PdfWriter()
    writer.append(str(prior_path), import_outline=True)
    appendix._named_destinations_cache = {}  # noqa: SLF001 - suppress generic LaTeX name import.
    writer.append(appendix, import_outline=False)
    for name in stable_ids:
        writer.add_named_destination(name, PRIOR_PAGES + int(appendix_named_pages[name]))

    current_parent = None
    for (level, title, _ident), (_pdf_title, local_page) in zip(headings, appendix_outline, strict=True):
        page_number = PRIOR_PAGES + int(local_page)
        if level == 1:
            current_parent = writer.add_outline_item(title, page_number, is_open=True)
        else:
            require(current_parent is not None, "level-2 outline item precedes a level-1 parent")
            writer.add_outline_item(title, page_number, parent=current_parent)

    writer.add_metadata({
        "/Title": "Topologi Aljabar — Roberts 30/30, Fomberg 1.1–1.13, Asesmen Kumulatif 1–3, dan Laboratorium Komputasi 1–2",
        "/Author": "David Michael Roberts; Yeheli Fomberg; edisi Bahasa Indonesia dengan pendamping penguasaan",
        "/Subject": "Checkpoint komposit parsial dengan 108 soal bersolusi dan Laboratorium Komputasi 1–2",
        "/Creator": f"{MODEL}; atas arahan pengguna",
        "/Producer": "pypdf deterministic append",
        "/CreationDate": "D:20260828000000+02'00'",
        "/ModDate": "D:20260828000000+02'00'",
    })
    writer.page_mode = "/UseOutlines"
    writer._ID = None  # noqa: SLF001 - deterministic trailer without /ID.
    with output_path.open("wb") as stream:
        writer.write(stream)

    merged = PdfReader(str(output_path))
    merged_prefix_structure = base.page_structure_hashes(merged, PRIOR_PAGES)
    merged_outline = base.outline_entries(merged)
    merged_named_pages = {name: merged.get_destination_page_number(destination) for name, destination in merged.named_destinations.items()}
    require(len(merged.pages) == PRIOR_PAGES + len(appendix.pages), "merged PDF page count drift")
    require(merged_prefix_structure == prior_page_structure, "predecessor per-page PDF structure changed")
    require(merged_outline[:PRIOR_OUTLINE] == prior_outline and len(merged_outline) == PRIOR_OUTLINE + len(headings), "predecessor outline is not exact prefix")
    require(len(merged_named_pages) == PRIOR_NAMED + len(stable_ids), "merged named-destination census drift")
    require(all(merged_named_pages.get(name) == page for name, page in prior_named_pages.items()), "predecessor named destinations changed")
    require(all(merged_named_pages.get(name) == PRIOR_PAGES + int(appendix_named_pages[name]) for name in stable_ids), "Lab 2 named destinations changed")
    merged_targets = base.link_targets(merged, PRIOR_PAGES)
    require(all(target in merged_named_pages for target in merged_targets), "merged appendix contains unresolved GoTo target")
    return {
        "status": "PASS",
        "bytes": output_path.stat().st_size,
        "sha256": digest(output_path),
        "pages": len(merged.pages),
        "appendix_pages": len(appendix.pages),
        "pypdf": pypdf.__version__,
        "outline_entries": len(merged_outline),
        "named_destinations": len(merged_named_pages),
        "stable_id_destinations_added": len(stable_ids),
        "outline_entries_added": len(headings),
        "predecessor_page_count": PRIOR_PAGES,
        "predecessor_page_structure_algorithm": "sha256-pypdf-semantic-v1",
        "predecessor_page_structure_aggregate_sha256": base.aggregate_hash(prior_page_structure),
        "predecessor_page_structure_sha256": prior_page_structure,
        "predecessor_outline_exact_prefix": True,
        "predecessor_named_destinations_preserved": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prior", required=True)
    parser.add_argument("--append", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--scratch-root", required=True)
    args = parser.parse_args()
    result = merge(*(Path(value).resolve() for value in (args.prior, args.append, args.output, args.source, args.scratch_root)))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
