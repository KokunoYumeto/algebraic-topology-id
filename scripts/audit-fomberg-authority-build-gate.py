#!/usr/bin/env python3
"""Create the bounded Fomberg authority/build-gate manifests without Git."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tarfile
import urllib.request
from pathlib import Path


LANE = Path(__file__).resolve().parent.parent
AUTHORITY = (
    LANE
    / "authority"
    / "upstream"
    / "math-notes-563194fae879178b9a6871b249513bfc27968975"
)
TREE = AUTHORITY / "tree"
ARCHIVE = (
    AUTHORITY
    / "archive"
    / "math-notes-563194fae879178b9a6871b249513bfc27968975.tar.gz"
)
OFFICIAL_PDF = AUTHORITY / "official" / "algebraic_topology.pdf"
SOURCE = TREE / "algebraic_topology.tex"
HEADER = TREE / "header.tex"
LICENSE = TREE / "LICENSE"
OVERLAY = AUTHORITY / "build-overlay" / "commath.sty"
BASELINE = AUTHORITY / "build-baseline"
BASELINE_PDF = BASELINE / "algebraic_topology-baseline.pdf"
BUILD_RESULT = BASELINE / "BUILD_RESULT.json"
PACKAGE_MANIFEST = BASELINE / "tex-input-manifest.csv"
PASS3_LOG = BASELINE / "pdflatex-pass-3.log"
PASS_LOGS = {
    pass_number: BASELINE / f"pdflatex-pass-{pass_number}.log"
    for pass_number in (1, 2, 3)
}
VERIFY_AUTHORITY = AUTHORITY / "verify_authority.py"
TREE_MANIFEST = AUTHORITY / "AUTHORITY_TREE_MANIFEST.csv"
OUTPUT_MANIFEST = AUTHORITY / "AUTHORITY_BUILD_MANIFEST.json"
QA_RECEIPT = LANE / "qa" / "FOMBERG_AUTHORITY_BUILD_GATE_QA.json"
VISUAL_QA = LANE / "qa" / "FOMBERG_AUTHORITY_BUILD_GATE_VISUAL_QA.md"
FILE_MANIFEST = LANE / "qa" / "FOMBERG_AUTHORITY_BUILD_GATE_FILE_MANIFEST.csv"

COMMIT = "563194fae879178b9a6871b249513bfc27968975"
EXPECTED_TREE = "fb678966d1533d529bdd72f49d8496a3bdc14a9b"
EXPECTED = {
    ARCHIVE: (2_236_609, "423c2c34b62a1b443e63be72e80a5c35d5cd6daf4e5b3be8e48dad1d1f897443"),
    SOURCE: (223_886, "d27095de0f38f0c14b2d7716cb52d51d064f0594dd9f82f9d1b3e6af5b35a483"),
    HEADER: (14_097, "7c4c5cbe901c1b6c7ae8d6053d42cd28110ece34dd90bc60c5bcb7423e45e28e"),
    LICENSE: (20_140, "0b7fc2608b6d990314e908569407a6058b4a29175167c6d91ca0070c946661be"),
    OFFICIAL_PDF: (383_089, "148aba71473e3201993e562c5e5d0f05f1a0417f4bcbd4593bead5ab236e43cd"),
    OVERLAY: (1_346, "524c17aef50ed58686c9ed0b0b274e7f2ccdb35380869fef9c66ce3a120a6d19"),
    BASELINE_PDF: (664_609, "f0f8f815423dbdc3b368b48a5972bfc62be87ae8b5c4bfcd1b7a74b8871417ff"),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_record(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"path": path.relative_to(LANE).as_posix(), "bytes": len(data), "sha256": sha256(data)}


def git_object_id(kind: bytes, body: bytes) -> tuple[bytes, str]:
    framed = kind + b" " + str(len(body)).encode("ascii") + b"\0" + body
    digest = hashlib.sha1(framed).digest()
    return digest, digest.hex()


def tree_id(directory: Path) -> tuple[bytes, str, list[dict[str, object]]]:
    children = sorted(
        directory.iterdir(),
        key=lambda item: os.fsencode(item.name) + (b"/" if item.is_dir() else b""),
    )
    payload = bytearray()
    inventory: list[dict[str, object]] = []
    for child in children:
        if child.is_dir():
            raw_id, _hex_id, descendants = tree_id(child)
            mode = b"40000"
            inventory.extend(descendants)
        elif child.is_file():
            data = child.read_bytes()
            raw_id, hex_id = git_object_id(b"blob", data)
            mode = b"100644"
            inventory.append(
                {
                    "path": child.relative_to(TREE).as_posix(),
                    "mode": mode.decode("ascii"),
                    "bytes": len(data),
                    "sha256": sha256(data),
                    "git_blob_sha1": hex_id,
                }
            )
        else:
            raise RuntimeError(f"unsupported authority entry: {child}")
        payload.extend(mode + b" " + os.fsencode(child.name) + b"\0" + raw_id)
    raw_tree, hex_tree = git_object_id(b"tree", bytes(payload))
    return raw_tree, hex_tree, inventory


def command_text(arguments: list[str]) -> str:
    result = subprocess.run(arguments, check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return result.stdout


def pdfinfo(path: Path) -> dict[str, str]:
    text = command_text(["pdfinfo", str(path)])
    values: dict[str, str] = {}
    for line in text.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    return values


def page_text(path: Path, page: int) -> str:
    return command_text(["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(path), "-"])


def package_rows() -> list[dict[str, str]]:
    with PACKAGE_MANIFEST.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def macro_usage(text: str, name: str) -> dict[str, object]:
    pattern = re.compile(r"\\" + re.escape(name) + r"(?![A-Za-z@])")
    matches = list(pattern.finditer(text))
    optional_arguments: list[str] = []
    optional_lines: list[dict[str, object]] = []
    for match in matches:
        optional = re.match(r"\s*\[([^\]]*)\]", text[match.end() :])
        if optional:
            value = optional.group(1)
            optional_arguments.append(value)
            optional_lines.append(
                {
                    "line": text.count("\n", 0, match.start()) + 1,
                    "value": value,
                }
            )
    return {
        "count": len(matches),
        "optional_arguments": optional_arguments,
        "optional_lines": optional_lines,
    }


def main() -> int:
    checks: dict[str, bool] = {}
    for path, (expected_bytes, expected_hash) in EXPECTED.items():
        record = file_record(path)
        checks[f"identity:{path.name}"] = (
            record["bytes"] == expected_bytes and record["sha256"] == expected_hash
        )

    _raw_tree, local_tree, inventory = tree_id(TREE)
    checks["authority_tree_id"] = local_tree == EXPECTED_TREE
    checks["authority_tracked_file_count"] = len(inventory) == 63

    archive_members: list[dict[str, object]] = []
    archive_mismatches: list[str] = []
    with tarfile.open(ARCHIVE, "r:gz") as archive:
        file_members = [member for member in archive.getmembers() if member.isfile()]
        for member in file_members:
            relative = member.name.split("/", 1)[1]
            stream = archive.extractfile(member)
            if stream is None:
                raise RuntimeError(f"could not read archive member: {member.name}")
            data = stream.read()
            extracted = TREE / relative
            if not extracted.is_file() or extracted.read_bytes() != data:
                archive_mismatches.append(relative)
            archive_members.append({"path": relative, "bytes": len(data), "sha256": sha256(data)})
    checks["archive_member_count"] = len(archive_members) == 63
    checks["archive_matches_extracted_tree"] = not archive_mismatches

    verification = subprocess.run(
        [sys.executable, str(VERIFY_AUTHORITY)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    ).stdout
    live_fields = dict(
        line.split("=", 1) for line in verification.splitlines() if "=" in line
    )
    checks["live_official_commit"] = live_fields.get("official_commit") == COMMIT
    checks["live_official_commit_tree"] = live_fields.get("official_commit_tree") == EXPECTED_TREE
    checks["live_official_leading_tree"] = live_fields.get("official_leading_tree_object") == EXPECTED_TREE
    checks["live_authority_verification"] = live_fields.get("authority_verification") == "PASS"

    with urllib.request.urlopen("https://yp.srht.site/notes/", timeout=30) as response:
        notes_page = response.read()
        notes_status = response.status
    notes_text = notes_page.decode("utf-8", errors="replace")
    checks["official_notes_page_http_200"] = notes_status == 200
    checks["official_notes_page_license"] = (
        "All notes are licensed under" in notes_text
        and "creativecommons.org/licenses/by-sa/4.0/" in notes_text
    )
    checks["official_notes_page_tex_link"] = (
        "https://yp.srht.site/notes/math/algebraic_topology.tex" in notes_text
    )
    checks["official_notes_page_pdf_link"] = (
        "https://yp.srht.site/notes/math/algebraic_topology.pdf" in notes_text
    )

    source_bytes = SOURCE.read_bytes()
    source_lines = source_bytes.splitlines(keepends=True)
    selected = b"".join(source_lines[30:4185])
    selected_text = selected.decode("utf-8")
    full_text = source_bytes.decode("utf-8")
    checks["source_line_count"] = len(source_lines) == 6069
    checks["selected_line_span"] = len(source_lines[30:4185]) == 4155
    checks["selected_span_hash"] = sha256(selected) == "4b96191b5e3cf5006d82175d609a4be8bba567458f7ee1c9f01cfe53490a645c"
    checks["selected_sections_1_1_through_1_13"] = (
        len(re.findall(r"^\\subsection\{", selected_text, re.MULTILINE)) == 13
        and selected_text.lstrip().startswith("\\section{Homology}")
        and "\\subsection{Cellular homology}" in selected_text
        and "\\subsection{Extras before cohomology}" not in selected_text
    )

    external_commands = re.compile(
        r"\\(?:includegraphics|input|include|includepdf|lstinputlisting|"
        r"verbatiminput|addbibresource|bibliography)\b"
    )
    checks["selected_no_external_file_commands"] = not external_commands.search(selected_text)
    checks["full_only_header_input"] = (
        len(external_commands.findall(full_text)) == 1 and "\\input{header.tex}" in full_text
    )
    checks["full_no_external_figures"] = "\\includegraphics" not in full_text

    commath_names = (
        "set", "del", "norm", "abs", "dif", "Dif", "od", "dod", "pd",
        "pdd", "md", "tder", "der", "pder", "jac", "grad", "curl", "div",
        "vect", "sbr", "cbr", "eval", "envert", "enVert", "ten",
    )
    selected_commath_usage = {
        name: usage
        for name in commath_names
        if (usage := macro_usage(selected_text, name))["count"]
    }
    full_commath_usage = {
        name: usage
        for name in commath_names
        if (usage := macro_usage(full_text, name))["count"]
    }
    checks["selected_commath_usage_is_bounded"] = selected_commath_usage == {
        "set": {"count": 147, "optional_arguments": [], "optional_lines": []},
        "del": {
            "count": 60,
            "optional_arguments": ["4", "4", "4", "1"],
            "optional_lines": [
                {"line": 762, "value": "4"},
                {"line": 782, "value": "4"},
                {"line": 794, "value": "4"},
                {"line": 3500, "value": "1"},
            ],
        },
        "norm": {"count": 2, "optional_arguments": [], "optional_lines": []},
        "abs": {"count": 2, "optional_arguments": [], "optional_lines": []},
    }
    checks["full_commath_usage_is_bounded"] = full_commath_usage == {
        "set": {"count": 174, "optional_arguments": [], "optional_lines": []},
        "del": {
            "count": 107,
            "optional_arguments": ["4", "4", "4", "1"],
            "optional_lines": [
                {"line": 792, "value": "4"},
                {"line": 812, "value": "4"},
                {"line": 824, "value": "4"},
                {"line": 3530, "value": "1"},
            ],
        },
        "norm": {"count": 2, "optional_arguments": [], "optional_lines": []},
        "abs": {"count": 2, "optional_arguments": [], "optional_lines": []},
    }
    checks["unused_removed_package_commands"] = all(
        token not in full_text
        for token in ("\\vv", "\\diff", "\\WithArrows", "curve=", "squiggly")
    )

    license_text = LICENSE.read_text(encoding="utf-8")
    header_text = HEADER.read_text(encoding="utf-8")
    checks["license_cc_by_sa_4"] = license_text.startswith("Attribution-ShareAlike 4.0 International")
    checks["author_credit_present"] = "\\def\\nauthor{Yeheli Fomberg}" in header_text
    checks["lecture_credit_present"] = "\\def\\nlecturer {Nir Lazarovich}" in full_text
    checks["nonendorsement_present"] = "These notes are not endorsed by the lecturers." in header_text
    checks["overlay_cc0_marker"] = "SPDX-License-Identifier: CC0-1.0" in OVERLAY.read_text(encoding="utf-8")

    build_result = json.loads(BUILD_RESULT.read_text(encoding="utf-8"))
    checks["two_clean_builds"] = build_result.get("clean_build_count") == 2
    checks["three_passes_each"] = build_result.get("passes_per_build") == 3
    checks["byte_identical_builds"] = build_result.get("byte_identical") is True
    checks["baseline_pdf_matches_result"] = (
        build_result.get("pdf_bytes") == BASELINE_PDF.stat().st_size
        and build_result.get("pdf_sha256") == sha256(BASELINE_PDF.read_bytes())
    )
    warning_patterns = {
        "latex_warning": r"LaTeX Warning:",
        "package_warning": r"Package .* Warning:",
        "overfull": r"Overfull \\[hv]box",
        "underfull": r"Underfull \\[hv]box",
        "undefined_control": r"Undefined control sequence",
        "latex_error": r"LaTeX Error",
        "fatal": r"Fatal error|Emergency stop",
    }
    pass_warning_counts = {
        str(pass_number): {
            name: len(
                re.findall(
                    pattern,
                    path.read_text(encoding="utf-8", errors="replace"),
                )
            )
            for name, pattern in warning_patterns.items()
        }
        for pass_number, path in PASS_LOGS.items()
    }
    checks["first_pass_has_convergence_only"] = pass_warning_counts["1"] == {
        "latex_warning": 52,
        "package_warning": 0,
        "overfull": 1,
        "underfull": 0,
        "undefined_control": 0,
        "latex_error": 0,
        "fatal": 0,
    }
    checks["second_pass_clean"] = not any(pass_warning_counts["2"].values())
    checks["final_pass_clean"] = not any(pass_warning_counts["3"].values())

    official_info = pdfinfo(OFFICIAL_PDF)
    baseline_info = pdfinfo(BASELINE_PDF)
    checks["official_pdf_57_a4_pages"] = (
        official_info.get("Pages") == "57" and "A4" in official_info.get("Page size", "")
    )
    checks["baseline_pdf_57_a4_pages"] = (
        baseline_info.get("Pages") == "57" and "A4" in baseline_info.get("Page size", "")
    )
    checks["selected_pdf_boundary_official"] = (
        "Example 1.33" in page_text(OFFICIAL_PDF, 39)
        and "1.14" in page_text(OFFICIAL_PDF, 40)
        and "Extras before cohomology" in page_text(OFFICIAL_PDF, 40)
    )
    checks["selected_pdf_boundary_baseline"] = (
        "Example 1.33" in page_text(BASELINE_PDF, 39)
        and "1.14" in page_text(BASELINE_PDF, 40)
        and "Extras before cohomology" in page_text(BASELINE_PDF, 40)
    )
    baseline_text = command_text(["pdftotext", "-layout", str(BASELINE_PDF), "-"])
    malformed_delimiter_literals = {
        "([) 4]": baseline_text.count("([) 4]"),
        "([) 1]": baseline_text.count("([) 1]"),
    }
    checks["no_leaked_commath_optional_tokens"] = not any(
        malformed_delimiter_literals.values()
    )

    font_text = command_text(["pdffonts", str(BASELINE_PDF)])
    font_rows = [line for line in font_text.splitlines()[2:] if line.strip()]
    checks["all_fonts_embedded"] = bool(font_rows) and all(
        re.search(r"\s+yes\s+(?:yes|no)\s+(?:yes|no)\s+\d+\s+\d+\s*$", row)
        for row in font_rows
    )
    type3_rows = [row for row in font_rows if "Type 3" in row]
    checks["known_type3_font_count"] = len(type3_rows) == 1
    checks["baseline_untagged_disclosed"] = baseline_info.get("Tagged") == "no"

    packages = package_rows()
    checks["package_input_count"] = len(packages) == build_result.get("package_input_count") == 106
    checks["package_inputs_hash_complete"] = all(
        row.get("path") and row.get("bytes") and re.fullmatch(r"[0-9a-f]{64}", row.get("sha256", ""))
        for row in packages
    )
    checks["no_frozen_asset_loaded"] = not any(
        "\\tree\\assets\\" in row["path"].lower() or "/tree/assets/" in row["path"].lower()
        for row in packages
    )
    visual_text = VISUAL_QA.read_text(encoding="utf-8") if VISUAL_QA.is_file() else ""
    visual_page_inventory = [1, 3, 10, 20, 30, 35, 39, 40, 57]
    checks["visual_qa_receipt_present"] = bool(visual_text)
    checks["visual_qa_page_inventory"] = (
        "pages 1, 3, 10, 20, 30, 35, 39, 40, and 57" in visual_text
    )
    checks["visual_qa_repaired_pages"] = all(
        marker in visual_text
        for marker in ("physical pages 10 and 35", "zero occurrences", "corrected comparison")
    )

    with TREE_MANIFEST.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "mode", "bytes", "sha256", "git_blob_sha1"])
        writer.writeheader()
        writer.writerows(sorted(inventory, key=lambda row: str(row["path"])))

    status = "PASS" if all(checks.values()) else "FAIL"
    manifest = {
        "schema_version": "1.0.0",
        "audit_date": "2026-08-24",
        "status": status,
        "scope": "Fomberg authority, exact overlay, full-source deterministic baseline, and selected-witness admission gate; no translation performed",
        "official_authority": {
            "notes_page": "https://yp.srht.site/notes/",
            "repository": "https://git.sr.ht/~yp/math-notes",
            "commit": COMMIT,
            "tree": EXPECTED_TREE,
            "tracked_files": len(inventory),
            "live_verification": live_fields,
            "notes_page_http_status": notes_status,
            "notes_page_bytes": len(notes_page),
            "notes_page_sha256": sha256(notes_page),
        },
        "frozen_files": [file_record(path) for path in (ARCHIVE, SOURCE, HEADER, LICENSE, OFFICIAL_PDF)],
        "archive": {
            "file_members": len(archive_members),
            "mismatches_against_extracted_tree": archive_mismatches,
            "tree_manifest": TREE_MANIFEST.relative_to(LANE).as_posix(),
            "tree_manifest_sha256": sha256(TREE_MANIFEST.read_bytes()),
        },
        "selected_witness": {
            "source_lines": "31-4185 inclusive",
            "source_line_count": 4155,
            "bytes_preserving_lf": len(selected),
            "sha256_preserving_lf": sha256(selected),
            "subsections": "1.1-1.13",
            "physical_pdf_pages": "1-39",
            "next_source_line": 4186,
            "next_pdf_page": 40,
            "next_heading": "1.14 Extras before cohomology",
            "inline_tikzpicture_count": len(re.findall(r"\\begin\{tikzpicture\}", selected_text)),
            "inline_tikzcd_count": len(re.findall(r"\\begin\{tikzcd\}", selected_text)),
            "external_file_commands": len(external_commands.findall(selected_text)),
        },
        "rights_and_credits": {
            "license": "CC BY-SA 4.0",
            "notes_author": "Yeheli Fomberg",
            "based_on_lectures_by": "Nir Lazarovich",
            "nonendorsement_notice_present": True,
            "problem_bank_selected": False,
            "component_assets": "No external figures/files are referenced; selected diagrams are inline licensed TeX.",
            "overlay_license": "CC0-1.0",
        },
        "dependency_overlay": {
            "selected_commath_usage": selected_commath_usage,
            "full_commath_usage": full_commath_usage,
            "commath_overlay": file_record(OVERLAY),
            "disposable_header_omissions": ["esvect", "esdiff", "witharrows", "quiver"],
            "frozen_header_edited": False,
        },
        "build": {
            **build_result,
            "baseline_pdf": file_record(BASELINE_PDF),
            "package_manifest": file_record(PACKAGE_MANIFEST),
            "package_input_count": len(packages),
            "pass_warning_counts": pass_warning_counts,
            "malformed_delimiter_literal_counts": malformed_delimiter_literals,
            "official_pdfinfo": official_info,
            "baseline_pdfinfo": baseline_info,
            "font_rows": len(font_rows),
            "type3_font_rows": len(type3_rows),
            "accessibility_limit": "PDF is untagged; one embedded BBM Type 3 font has no Unicode map.",
        },
        "visual_qa": {
            "receipt": file_record(VISUAL_QA),
            "rendered_pages": visual_page_inventory,
            "repaired_affected_pages": [10, 35],
        },
        "admission": {
            "status": status,
            "selected_source_lines": "31-4185 inclusive",
            "selected_pdf_pages": "1-39",
            "translation_performed": False,
        },
        "checks": checks,
    }
    OUTPUT_MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    qa = {
        "schema_version": "1.0.0",
        "audit_date": "2026-08-24",
        "status": status,
        "manifest": file_record(OUTPUT_MANIFEST),
        "authority_tree_manifest": file_record(TREE_MANIFEST),
        "baseline_pdf": file_record(BASELINE_PDF),
        "checks": checks,
        "failed_checks": [name for name, passed in checks.items() if not passed],
        "admission_status": status,
        "visual_qa_receipt": file_record(VISUAL_QA),
        "file_manifest": "qa/FOMBERG_AUTHORITY_BUILD_GATE_FILE_MANIFEST.csv",
    }
    QA_RECEIPT.write_text(json.dumps(qa, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    generated_paths = [
        TREE_MANIFEST,
        OUTPUT_MANIFEST,
        AUTHORITY / "build-overlay" / "commath.sty",
        AUTHORITY / "build-overlay" / "README.md",
        *sorted(path for path in BASELINE.iterdir() if path.is_file()),
        QA_RECEIPT,
        VISUAL_QA,
        LANE / "scripts" / "build-fomberg-authority-baseline.ps1",
        Path(__file__).resolve(),
    ]
    roles = {
        TREE_MANIFEST: "authority-tree-inventory",
        OUTPUT_MANIFEST: "authority-build-manifest",
        AUTHORITY / "build-overlay" / "commath.sty": "cc0-build-overlay",
        AUTHORITY / "build-overlay" / "README.md": "overlay-rights-documentation",
        QA_RECEIPT: "machine-qa-receipt",
        VISUAL_QA: "visual-qa-receipt",
        LANE / "scripts" / "build-fomberg-authority-baseline.ps1": "deterministic-builder",
        Path(__file__).resolve(): "authority-build-auditor",
    }
    with FILE_MANIFEST.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "role", "bytes", "sha256"])
        writer.writeheader()
        for path in generated_paths:
            record = file_record(path)
            writer.writerow(
                {
                    **record,
                    "role": roles.get(path, "baseline-build-evidence"),
                }
            )
    print(json.dumps({"status": status, "checks": len(checks), "failed": qa["failed_checks"]}, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
