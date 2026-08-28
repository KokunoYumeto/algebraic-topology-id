#!/usr/bin/env python3
"""Deterministically append the verified computation Lab 1 reader surface."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PRIOR_HTML = ROOT / "output/html/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03/index.html"
PRIOR_PDF = ROOT / "output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-id.pdf"
SOURCE = ROOT / "source/id-ID/labs/computation-lab-001-monodromy-presentations.md"
PROGRAM = ROOT / "source/id-ID/labs/o012_d60_lab01_monodromy.py"
TESTS = ROOT / "source/id-ID/labs/test_o012_d60_lab01_monodromy.py"
EXPECTED = ROOT / "source/id-ID/labs/expected-output-lab01.txt"
SOURCE_QA = ROOT / "qa/COMPUTATION_LAB_001_QA.json"
BACKEND_RECEIPT = ROOT / "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_001_CUMULATIVE_RECEIPT.json"
MERGER = ROOT / "scripts/merge-computation-lab-001.py"
SLUG = "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01"
HTML_OUT = ROOT / f"output/html/{SLUG}/index.html"
PDF_OUT = ROOT / f"output/pdf/topologi-aljabar-{SLUG}-id.pdf"
MANIFEST_OUT = ROOT / "output/ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01.csv"
DRAFT_RECEIPT = ROOT / "qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_BUILD_DRAFT.json"
SCRATCH = ROOT / f"tmp/pdfs/{SLUG}-build"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"

PRIOR_HTML_ID = (15_287_428, "417e50656ae0a61134c480f59df1bcd54d66a68c938d1d54f9c931ba37e2a5d6")
PRIOR_PDF_ID = (8_915_996, "74ed9b5bf0f79a98693369dc7beba3e84ac81c711cc96b9951ae950ae9632a16")
PRIOR_PAGES = 501
PRIOR_OUTLINE = 416
PRIOR_NAMED = 3056


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def identity(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(raw),
        "lf_lines": raw.count(b"\n"),
        "sha256": digest_bytes(raw),
    }


def disciplined(path: Path) -> str:
    raw = path.read_bytes()
    require(raw and b"\r" not in raw and raw.endswith(b"\n"), f"input is not nonempty LF UTF-8: {path.name}")
    return raw.decode("utf-8", errors="strict")


def command(args: list[str], *, cwd: Path = ROOT, capture: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        args,
        cwd=cwd,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
        timeout=900,
        check=False,
        env={**os.environ, "SOURCE_DATE_EPOCH": "1787875200", "FORCE_SOURCE_DATE": "1"},
    )
    if result.returncode != 0:
        stderr = (result.stderr or b"").decode("utf-8", errors="replace")
        raise RuntimeError(f"command failed ({result.returncode}): {args!r}\n{stderr}")
    return result


def tool(name: str) -> str:
    value = shutil.which(name)
    require(value is not None, f"required tool missing: {name}")
    return value


def replace_once(text: str, old: str, new: str, label: str) -> str:
    require(text.count(old) == 1, f"HTML anchor missing or duplicated: {label}")
    return text.replace(old, new, 1)


def write_atomic(destination: Path, source: Path) -> None:
    require(source.is_file() and source.resolve().is_relative_to(SCRATCH.resolve()), "atomic source outside bounded scratch")
    destination.parent.mkdir(parents=True, exist_ok=True)
    pending = destination.parent / f".{destination.name}.lab01.pending"
    backup = destination.parent / f".{destination.name}.lab01.rollback"
    require(not pending.exists() and not backup.exists(), f"atomic temporary collision: {destination}")
    shutil.copyfile(source, pending)
    require(pending.stat().st_size == source.stat().st_size and digest(pending) == digest(source), "atomic pending copy mismatch")
    if destination.exists():
        shutil.copyfile(destination, backup)
    try:
        os.replace(pending, destination)
        require(destination.stat().st_size == source.stat().st_size and digest(destination) == digest(source), "promoted artifact mismatch")
    except Exception:
        if backup.exists():
            os.replace(backup, destination)
        elif destination.exists():
            destination.unlink()
        raise
    finally:
        if pending.exists():
            pending.unlink()
        if backup.exists():
            backup.unlink()


def expand_source() -> str:
    source = disciplined(SOURCE)
    program = disciplined(PROGRAM).rstrip("\n")
    tests = disciplined(TESTS).rstrip("\n")
    expected = disciplined(EXPECTED).rstrip("\n")
    replacements = {
        "O012_LAB01_INCLUDE_PROGRAM": f"```python\n{program}\n```",
        "O012_LAB01_INCLUDE_TESTS": f"```python\n{tests}\n```",
        "O012_LAB01_INCLUDE_EXPECTED": f"```text\n{expected}\n```",
    }
    for marker, value in replacements.items():
        require(source.count(marker) == 1, f"include marker drift: {marker}")
        source = source.replace(marker, value)
    link_replacements = {
        "[`o012_d60_lab01_monodromy.py`](o012_d60_lab01_monodromy.py)": "`o012_d60_lab01_monodromy.py`",
        "[`test_o012_d60_lab01_monodromy.py`](test_o012_d60_lab01_monodromy.py)": "`test_o012_d60_lab01_monodromy.py`",
        "[`expected-output-lab01.txt`](expected-output-lab01.txt)": "`expected-output-lab01.txt`",
    }
    for old, new in link_replacements.items():
        require(source.count(old) == 1, f"canonical file link drift: {old}")
        source = source.replace(old, new)
    return source


def render_page(mutool: str, pdf: Path, page: int, destination: Path, dpi: int = 160) -> None:
    command([mutool, "draw", "-q", "-F", "png", "-r", str(dpi), "-c", "rgb", "-A", "8", "-o", str(destination), str(pdf), str(page)])
    require(destination.is_file() and destination.stat().st_size > 0, f"render failed: {pdf.name} page {page}")


def main() -> int:
    require(PRIOR_HTML.is_file() and (PRIOR_HTML.stat().st_size, digest(PRIOR_HTML)) == PRIOR_HTML_ID, "frozen predecessor HTML drift")
    require(PRIOR_PDF.is_file() and (PRIOR_PDF.stat().st_size, digest(PRIOR_PDF)) == PRIOR_PDF_ID, "frozen predecessor PDF drift")
    for path in (SOURCE, PROGRAM, TESTS, EXPECTED, SOURCE_QA, BACKEND_RECEIPT, MERGER):
        require(path.is_file(), f"missing required input: {path.name}")
    qa = json.loads(disciplined(SOURCE_QA))
    require(qa.get("status") == "PASS" and qa.get("laboratory_id") == "D60-LAB01", "source QA gate failed")
    require(qa.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0}, "source QA findings remain")
    backend = json.loads(disciplined(BACKEND_RECEIPT))
    require(backend.get("status") == "PASS" and backend.get("receipt_kind") == "cumulative_backend_boundary", "backend gate failed")
    require(backend.get("immutable_prefix", {}).get("preserved_exactly") is True, "backend prefix not preserved")
    require(backend.get("cumulative", {}).get("records") == 7404 and backend.get("cumulative", {}).get("bundle_sha256") == "4740eb2ff83b4f9df3c0d90c2426ff77e652b23cad0bbe7763c54ebdefa60b4b", "backend boundary mismatch")
    require(backend.get("replay", {}).get("status") == "PASS" and backend.get("replay", {}).get("temporary_replay_removed") is True, "backend replay gate failed")

    scratch_resolved = SCRATCH.resolve()
    allowed = (ROOT / "tmp/pdfs").resolve()
    require(scratch_resolved.parent == allowed and scratch_resolved.name == f"{SLUG}-build", "unsafe scratch path")
    require(not SCRATCH.exists(), "bounded build scratch already exists")
    SCRATCH.mkdir(parents=True)
    try:
        pandoc = tool("pandoc")
        mutool = tool("mutool")
        pdfinfo = tool("pdfinfo")
        pdffonts = tool("pdffonts")
        pdftotext = tool("pdftotext")
        python = sys.executable
        pandoc_version = command([pandoc, "--version"]).stdout.decode("utf-8").splitlines()[0]
        mutool_version = command([mutool, "-v"]).stderr.decode("utf-8", errors="replace").strip().splitlines()[0]
        require(pandoc_version == "pandoc 3.9.0.2", f"unexpected Pandoc: {pandoc_version}")
        require(mutool_version == "mutool version 1.23.0", f"unexpected mutool: {mutool_version}")

        expanded = expand_source()
        expanded_path = SCRATCH / "lab01-expanded.md"
        expanded_path.write_text(expanded, encoding="utf-8", newline="\n")
        fragment_a = SCRATCH / "lab01-a.html"
        fragment_b = SCRATCH / "lab01-b.html"
        html_args = [
            pandoc, str(expanded_path), "--from=markdown+fenced_divs+tex_math_dollars",
            "--to=html5", "--mathml", "--section-divs", "--strip-comments", "--fail-if-warnings",
        ]
        command([*html_args, f"--output={fragment_a}"])
        command([*html_args, f"--output={fragment_b}"])
        require(digest(fragment_a) == digest(fragment_b), "Lab 1 HTML fragments differ")
        fragment = fragment_a.read_text(encoding="utf-8").replace("\r\n", "\n")
        require("<html" not in fragment and "<body" not in fragment, "fragment unexpectedly has a document shell")
        ids = re.findall(r'\bid="(o012-d60-lab01(?:-[a-z0-9]+)*)"', fragment)
        require(len(ids) == len(set(ids)) == 24, "fragment stable-ID census drift")
        require(len(re.findall(r'class="[^"]*\bexercise\b', fragment)) == 6, "fragment task census drift")
        require(len(re.findall(r'class="[^"]*\bhint\b', fragment)) == 1, "fragment hint census drift")
        require(fragment.count("<pre") >= 3 and "<math" in fragment and "$" not in fragment, "fragment code/math conversion failed")

        prior_raw = PRIOR_HTML.read_bytes()
        prior = prior_raw.decode("utf-8")
        nl = "\r\n" if "\r\n" in prior else "\n"
        require("\r" not in prior.replace("\r\n", ""), "predecessor HTML contains bare CR")
        old_title = "<title>Topologi Aljabar — Roberts 30/30, Fomberg 1.1–1.13, dan Asesmen Kumulatif 1–3</title>"
        new_title = "<title>Topologi Aljabar — Roberts 30/30, Fomberg 1.1–1.13, Asesmen Kumulatif 1–3, dan Laboratorium Komputasi 1</title>"
        old_heading = '<h1 class="title">Topologi Aljabar — Roberts 30/30, Fomberg' + nl + '1.1–1.13, dan Asesmen Kumulatif 1–3</h1>'
        new_heading = '<h1 class="title">Topologi Aljabar — Roberts 30/30, Fomberg' + nl + '1.1–1.13, Asesmen Kumulatif 1–3, dan Laboratorium Komputasi 1</h1>'
        old_subtitle = '<p class="subtitle">Komponen Roberts lengkap; jembatan Fomberg melalui' + nl + 'homologi seluler; 84 soal rute dan 24 soal asesmen kumulatif dengan petunjuk serta solusi lengkap; checkpoint komposit parsial</p>'
        new_subtitle = '<p class="subtitle">Komponen Roberts lengkap; jembatan Fomberg melalui' + nl + 'homologi seluler; 108 soal bersolusi; Laboratorium Komputasi 1 lengkap dan dapat dijalankan luring; checkpoint komposit parsial</p>'
        combined = replace_once(prior, old_title, new_title, "title")
        combined = replace_once(combined, old_heading, new_heading, "heading")
        combined = replace_once(combined, old_subtitle, new_subtitle, "subtitle")

        css_insert = nl + "pre { max-width: 100%; overflow-x: auto; white-space: pre; }"
        style_close = combined.find(nl + "</style>")
        require(style_close > 0, "style close missing")
        combined = combined[:style_close] + css_insert + combined[style_close:]
        nav_close = nl + "</ul>" + nl + "</nav>"
        nav_pos = combined.rfind(nav_close)
        require(nav_pos > 0, "top-level ToC close missing")
        toc_insert = nl + '<li><a href="#o012-d60-lab01" id="toc-o012-d60-lab01">Laboratorium Komputasi 1 — Monodromi Ruang Penutup dan Presentasi Grup</a></li>'
        combined = combined[:nav_pos] + toc_insert + combined[nav_pos:]

        old_status = "Jalur komposit masih parsial karena lapisan penguasaan lintas-rute," + nl + "laboratorium, dan capstone belum selesai; kursor sumber berikutnya tepat" + nl + "pada baris 4186."
        new_status = "Jalur komposit masih parsial karena tiga laboratorium komputasi," + nl + "penutupan metadata bukti, dan capstone belum selesai; kursor sumber berikutnya" + nl + "tetap pada baris 4186."
        combined = replace_once(combined, old_status, new_status, "status sentence")
        status_start = combined.find('<section id="o012-composite-status"')
        status_end = combined.find(nl + "</section>", status_start)
        require(status_start > 0 and status_end > status_start, "composite status close missing")
        status_insert = nl + '<aside id="o012-d60-lab01-checkpoint-status" class="note" data-origin="edition-original">' + nl + '<p><strong>Tambahan checkpoint.</strong> Laboratorium Komputasi 1 menambahkan program Python berpustaka standar, enam uji deterministik, keluaran acuan, interpretasi, petunjuk, dan solusi lengkap untuk monodromi ruang penutup serta presentasi grup. Lapisan asli edisi ini berlisensi CC BY-SA 4.0 dan tidak memakai bank masalah Fomberg.</p>' + nl + '</aside>'
        combined = combined[:status_end] + status_insert + combined[status_end:]
        body_close = nl + "</body>"
        body_pos = combined.rfind(body_close)
        require(body_pos > 0, "body close missing")
        fragment_insert = nl + fragment.rstrip("\r\n").replace("\n", nl)
        combined = combined[:body_pos] + fragment_insert + combined[body_pos:]

        reconstructed = combined
        for insertion in (fragment_insert, status_insert, toc_insert, css_insert):
            pos = reconstructed.rfind(insertion)
            require(pos >= 0, "cannot reverse HTML insertion")
            reconstructed = reconstructed[:pos] + reconstructed[pos + len(insertion):]
        reconstructed = replace_once(reconstructed, new_status, old_status, "reverse status")
        reconstructed = replace_once(reconstructed, new_subtitle, old_subtitle, "reverse subtitle")
        reconstructed = replace_once(reconstructed, new_heading, old_heading, "reverse heading")
        reconstructed = replace_once(reconstructed, new_title, old_title, "reverse title")
        require(reconstructed.encode("utf-8") == prior_raw, "exact HTML predecessor reconstruction failed")

        html_a = SCRATCH / "combined-a.html"
        html_b = SCRATCH / "combined-b.html"
        html_a.write_text(combined, encoding="utf-8", newline="")
        html_b.write_text(combined, encoding="utf-8", newline="")
        require(digest(html_a) == digest(html_b), "combined HTML writes differ")
        all_ids = re.findall(r'(?<=\s)id="([^"]+)"', combined)
        require(len(all_ids) == len(set(all_ids)), "duplicate HTML ID")
        id_set = set(all_ids)
        links = [value for value in re.findall(r'\bhref="#([^"]+)"', combined)]
        require(not (set(links) - id_set), f"unresolved HTML fragments: {sorted(set(links)-id_set)[:5]}")
        require('id="toc-o012-d60-lab01"' in combined and 'id="o012-d60-lab01"' in combined, "Lab 1 ToC/source missing")
        require("pre { max-width: 100%; overflow-x: auto;" in combined, "local code overflow CSS missing")
        private_markers = ("C:\\Users\\", "github_pat_", "ghp_", "access_token", "FILL_AFTER", "BEGIN PRIVATE KEY")
        require(not any(marker in combined for marker in private_markers), "private/transient marker in HTML")

        pdf_text = re.sub(r"\A---\n.*?\n---\n", "", expanded, count=1, flags=re.DOTALL)
        fence_re = re.compile(r"(?m)^(::: \{\.(?:exercise|hint) )#(o012-d60-lab01(?:-[a-z0-9]+)*)([^\r\n]*\})$")
        require(len(fence_re.findall(pdf_text)) == 7, "PDF fenced stable-ID transform census drift")
        pdf_text = fence_re.sub(r"\1\3\n\n```{=latex}\n\\hypertarget{\2}{}\n\\par\\noindent\n```", pdf_text)
        heading_re = re.compile(r"(?m)^(#{1,2})\s+(.+?)\s+\{#(o012-d60-lab01(?:-[a-z0-9]+)*)\}\s*$")
        require(len(heading_re.findall(pdf_text)) == 17, "PDF heading stable-ID transform census drift")
        pdf_text = heading_re.sub(r"\1 \2\n\n```{=latex}\n\\hypertarget{\3}{}\n```", pdf_text)
        pdf_source = SCRATCH / "lab01-layout.md"
        pdf_source.write_text(pdf_text, encoding="utf-8", newline="\n")
        pdf_header = SCRATCH / "lab01-header.tex"
        pdf_header.write_text(
            "\\AddToHook{begindocument/end}{\\pdftrailerid{}}\n"
            "\\usepackage{listings}\n"
            "\\lstset{breaklines=true,breakatwhitespace=false,basicstyle=\\ttfamily\\scriptsize,columns=fullflexible,keepspaces=true,showstringspaces=false,upquote=true}\n",
            encoding="utf-8",
            newline="\n",
        )
        work_pdf = SCRATCH / "lab01-work.pdf"
        append_a = SCRATCH / "lab01-a.pdf"
        append_b = SCRATCH / "lab01-b.pdf"
        pdf_args = [
            pandoc, str(pdf_source), "--from=markdown+fenced_divs+tex_math_dollars", "--standalone",
            "--number-sections", "--strip-comments", "--listings", "--metadata=lang:id-ID",
            "--metadata=pagetitle:Laboratorium Komputasi 1", "--metadata=date:28 Agustus 2026",
            "--pdf-engine=pdflatex", f"--include-in-header={pdf_header}", "--variable=papersize:a4",
            "--variable=geometry:margin=21mm", "--variable=fontsize:11pt", "--variable=colorlinks:true",
            "--variable=linkcolor:blue", "--variable=pdf-trailer-id:",
        ]
        command([*pdf_args, f"--output={work_pdf}"])
        shutil.copyfile(work_pdf, append_a)
        command([*pdf_args, f"--output={work_pdf}"])
        shutil.copyfile(work_pdf, append_b)
        require(digest(append_a) == digest(append_b), "Lab 1 appendix PDF builds differ")
        append_info = command([pdfinfo, str(append_a)]).stdout.decode("utf-8", errors="replace")
        require(re.search(r"(?m)^Page size:.*\(A4\)\s*$", append_info) is not None and re.search(r"(?m)^Encrypted:\s+no\s*$", append_info) is not None, "appendix PDF gate failed")
        append_pages_match = re.search(r"(?m)^Pages:\s+(\d+)\s*$", append_info)
        require(append_pages_match is not None, "appendix page count missing")
        appendix_pages = int(append_pages_match.group(1))
        require(appendix_pages > 0, "appendix PDF empty")
        append_trailer = command([mutool, "show", str(append_a), "trailer"]).stdout.decode("utf-8", errors="replace")
        require(re.search(r"(?m)^\s*/ID\s", append_trailer) is None, "appendix trailer contains /ID")
        append_outline = command([mutool, "show", str(append_a), "outline"]).stdout.decode("utf-8", errors="replace")
        outline_rows = [line for line in append_outline.splitlines() if re.match(r"^(?:\+|\||-)", line)]
        require(len(outline_rows) == 17, "appendix outline census drift")

        merged_a = SCRATCH / "combined-a.pdf"
        merged_b = SCRATCH / "combined-b.pdf"
        merge_args = [python, "-B", str(MERGER), "--prior", str(PRIOR_PDF), "--append", str(append_a), "--source", str(SOURCE), "--scratch-root", str(SCRATCH)]
        merge_result_a = json.loads(command([*merge_args, "--output", str(merged_a)]).stdout)
        merge_args_b = [python, "-B", str(MERGER), "--prior", str(PRIOR_PDF), "--append", str(append_b), "--source", str(SOURCE), "--scratch-root", str(SCRATCH), "--output", str(merged_b)]
        merge_result_b = json.loads(command(merge_args_b).stdout)
        require(digest(merged_a) == digest(merged_b), "merged Lab 1 PDFs differ")
        require(merge_result_a.get("status") == "PASS" and merge_result_a.get("pypdf") == "6.12.2", "PDF merger gate failed")
        require(merge_result_a.get("predecessor_page_structure_aggregate_sha256") == merge_result_b.get("predecessor_page_structure_aggregate_sha256"), "predecessor structure differs across deterministic builds")
        structure_hashes = merge_result_a["predecessor_page_structure_sha256"]
        require(len(structure_hashes) == PRIOR_PAGES, "predecessor structural page census drift")

        prior_text = SCRATCH / "prior-001-501.txt"
        merged_prefix_text = SCRATCH / "merged-001-501.txt"
        merged_text = SCRATCH / "merged-all.txt"
        command([pdftotext, "-enc", "UTF-8", "-f", "1", "-l", str(PRIOR_PAGES), str(PRIOR_PDF), str(prior_text)])
        command([pdftotext, "-enc", "UTF-8", "-f", "1", "-l", str(PRIOR_PAGES), str(merged_a), str(merged_prefix_text)])
        require(digest(prior_text) == digest(merged_prefix_text), "extracted predecessor text changed")
        command([pdftotext, "-enc", "UTF-8", str(merged_a), str(merged_text)])
        all_pdf_text = merged_text.read_text(encoding="utf-8", errors="replace")
        for required in ("Laboratorium Komputasi 1", "monodromi", "presentasi_citra", "basis_bebas", "CC BY-SA 4.0"):
            require(required in all_pdf_text, f"required PDF text missing: {required}")
        require(not any(marker in all_pdf_text for marker in private_markers), "private/transient marker in PDF text")
        font_output = command([pdffonts, str(merged_a)]).stdout.decode("utf-8", errors="replace").splitlines()
        font_rows = [line for line in font_output[2:] if line.strip()]
        require(font_rows, "PDF font inventory empty")
        for row in font_rows:
            match = re.search(r"\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$", row)
            require(match is not None and match.groups() == ("yes", "yes", "yes"), f"PDF font gate failed: {row}")
        merged_trailer = command([mutool, "show", str(merged_a), "trailer"]).stdout.decode("utf-8", errors="replace")
        require(re.search(r"(?m)^\s*/ID\s", merged_trailer) is None, "merged trailer contains /ID")
        final_info = command([pdfinfo, str(merged_a)]).stdout.decode("utf-8", errors="replace")
        page_match = re.search(r"(?m)^Pages:\s+(\d+)\s*$", final_info)
        require(page_match is not None and int(page_match.group(1)) == PRIOR_PAGES + appendix_pages, "merged PDF page count mismatch")
        pages = int(page_match.group(1))

        transition_prior = SCRATCH / "transition-prior.png"
        transition_merged = SCRATCH / "transition-merged.png"
        render_page(mutool, PRIOR_PDF, PRIOR_PAGES, transition_prior)
        render_page(mutool, merged_a, PRIOR_PAGES, transition_merged)
        require(digest(transition_prior) == digest(transition_merged), "rendered transition predecessor page changed")

        staged_manifest = SCRATCH / "artifact-manifest.csv"
        manifest_lines = ["path,bytes,sha256"]
        for public_path, staged in ((HTML_OUT, html_a), (PDF_OUT, merged_a)):
            manifest_lines.append(f"{public_path.relative_to(ROOT).as_posix()},{staged.stat().st_size},{digest(staged)}")
        staged_manifest.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8", newline="\n")
        receipt = {
            "status": "PASS_DETERMINISTIC_BUILD_PENDING_VISUAL_BROWSER_QA",
            "source_date_epoch": 1787875200,
            "model_provenance": MODEL,
            "pandoc": pandoc_version,
            "mutool": mutool_version,
            "pypdf": merge_result_a["pypdf"],
            "sources": [identity(path) for path in (SOURCE, PROGRAM, TESTS, EXPECTED)],
            "frozen_predecessor": {
                "html_bytes": PRIOR_HTML_ID[0], "html_sha256": PRIOR_HTML_ID[1],
                "pdf_bytes": PRIOR_PDF_ID[0], "pdf_sha256": PRIOR_PDF_ID[1], "pdf_pages": PRIOR_PAGES,
                "html_exact_reconstruction": True, "pdf_extracted_text_prefix_identical": True,
                "pdf_page_structure_algorithm": merge_result_a["predecessor_page_structure_algorithm"],
                "pdf_page_structure_aggregate_sha256": merge_result_a["predecessor_page_structure_aggregate_sha256"],
                "pdf_page_structure_sha256": structure_hashes,
                "transition_page_render_dpi": 160,
                "transition_page_render_sha256": digest(transition_prior),
            },
            "html": {
                "path": HTML_OUT.relative_to(ROOT).as_posix(), "bytes": html_a.stat().st_size,
                "sha256": digest(html_a), "dom_ids": len(all_ids), "fragment_links": len(links),
                "stable_ids_added": 24, "tasks_added": 6, "deterministic_writes": 2,
                "code_blocks_locally_scrollable": True,
            },
            "pdf": {
                "path": PDF_OUT.relative_to(ROOT).as_posix(), "bytes": merged_a.stat().st_size,
                "sha256": digest(merged_a), "pages": pages, "appendix_pages": appendix_pages,
                "stable_id_destinations_added": 24, "outline_entries_added": 17,
                "outline_entries": merge_result_a["outline_entries"], "named_destinations": merge_result_a["named_destinations"],
                "fonts": len(font_rows), "all_fonts_embedded_subset_tounicode": True,
                "trailer_id_suppressed": True, "deterministic_appendix_builds": 2, "deterministic_merged_builds": 2,
            },
            "manifest": {"path": MANIFEST_OUT.relative_to(ROOT).as_posix(), "bytes": staged_manifest.stat().st_size, "sha256": digest(staged_manifest)},
            "qa": identity(SOURCE_QA),
            "backend_receipt": identity(BACKEND_RECEIPT),
        }
        staged_receipt = SCRATCH / "build-draft.json"
        staged_receipt.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        for destination, staged in ((HTML_OUT, html_a), (PDF_OUT, merged_a), (MANIFEST_OUT, staged_manifest), (DRAFT_RECEIPT, staged_receipt)):
            write_atomic(destination, staged)
        print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
        return 0
    finally:
        if SCRATCH.exists():
            require(SCRATCH.resolve().parent == (ROOT / "tmp/pdfs").resolve(), "unsafe scratch cleanup target")
            shutil.rmtree(SCRATCH)
        require(not SCRATCH.exists(), "bounded scratch removal failed")


if __name__ == "__main__":
    raise SystemExit(main())
