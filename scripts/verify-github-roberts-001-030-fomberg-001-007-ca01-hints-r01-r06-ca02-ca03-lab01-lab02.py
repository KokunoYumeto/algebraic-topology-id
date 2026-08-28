#!/usr/bin/env python3
"""Verify the public Lab 2 GitHub/Pages checkpoint from immutable bytes.

This wrapper deliberately reuses the fail-closed Lab 1 transport verifier while
replacing every boundary-specific identity and gate with the completed Lab 2
boundary.  It performs no Git mutation.  The generated receipt records the
complete GitHub comparison delta, commit-pinned raw readback, Pages deployment,
the frozen Lab 1 predecessor, and the sibling Zenodo v0.31.4 identity.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / (
    "scripts/verify-github-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-"
    "ca02-ca03-lab01.py"
)
SPEC = importlib.util.spec_from_file_location("d60_lab01_github_verifier", BASE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load the frozen Lab 1 GitHub verifier")
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)

module.GIT_DELTA_BASE_COMMIT = "9eb4e7ba2e864f14aa07e175b32d332558273a4b"
module.PREDECESSOR_CONTENT_COMMIT = "a8311697800102ce65ce7f67752b0179ccaa9109"
module.PAGES_URL = (
    "https://kokunoyumeto.github.io/algebraic-topology-id/"
    "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02/"
)
module.PAGES_PATH = (
    "output/html/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-"
    "ca02-ca03-lab01-lab02/index.html"
)
module.PAGES_BYTES = 15_615_104
module.PAGES_SHA256 = "d0c6afddfa92759d475258bf08f20ea4019eccf72b7554128b2b938bd247b375"
module.PREDECESSOR_URL = (
    "https://kokunoyumeto.github.io/algebraic-topology-id/"
    "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01/"
)
module.PREDECESSOR_PATH = (
    "output/html/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-"
    "ca02-ca03-lab01/index.html"
)
module.PREDECESSOR_BYTES = 15_389_821
module.PREDECESSOR_SHA256 = (
    "bb0cf484271370878508a6b774e442ee57aaf82b1a3bbca1bed086729360f7ff"
)
module.PDF_PATH = (
    "output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-007-ca01-"
    "hints-r01-r06-ca02-ca03-lab01-lab02-id.pdf"
)
module.MANIFEST_PATH = (
    "output/ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_007_CA01_"
    "HINTS_R01_R06_CA02_CA03_LAB01_LAB02.csv"
)
module.FINAL_BUILD_RECEIPT = (
    "qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_"
    "LAB01_LAB02_BUILD_RECEIPT.json"
)
module.VISUAL_RECEIPT = (
    "qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_"
    "LAB01_LAB02_VISUAL_QA.md"
)
module.BROWSER_RECEIPT = (
    "qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_"
    "LAB01_LAB02_BROWSER_QA.json"
)
module.ZENODO_RELEASE_DIR = (
    "release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-"
    "ca02-ca03-lab01-lab02"
)
module.ZENODO_RECEIPT_PATH = f"{module.ZENODO_RELEASE_DIR}/publication-receipt.json"
module.OUTPUT = ROOT / (
    "00_control/GITHUB_PUBLICATION_RECEIPT_ROBERTS_001_030_FOMBERG_001_007_"
    "CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02.json"
)

module.FIXED_LOCAL_IDENTITIES = {
    "source/id-ID/labs/computation-lab-002-chain-matrices-smith-normal-form.md": (
        16_529,
        "532a1e4dacbfb33b680fbe7251accfc16fda933ed7f49f41e836fec15e096b5b",
        True,
    ),
    "source/id-ID/labs/o012_d60_lab02_smith_normal_form.py": (
        22_052,
        "47735d76fb1c979d78daaa068a9a32f807ebb234c2da3e5e597f75861e27ae3c",
        True,
    ),
    "source/id-ID/labs/test_o012_d60_lab02_smith_normal_form.py": (
        7_891,
        "475872356d92f3f439ab353602c293b94db2324fe42209d30f2be6e51b13e2dc",
        True,
    ),
    "source/id-ID/labs/expected-output-lab02.txt": (
        795,
        "965994efd39713b7591d43fab5d02bb43d200b68e67c4fa98a5b534452bb537c",
        True,
    ),
    "00_control/TERMINOLOGY.csv": (
        65_333,
        "93d680886e18f2fe2aa64f4f4ce583448b1bebcf6bf22016fd35d60be51b21cc",
        True,
    ),
    "qa/COMPUTATION_LAB_002_QA.json": (
        4_318,
        "c084e575a621906ac7d8a1c6dca6f604de99b8e58a788409be17bb7392dd4319",
        True,
    ),
    module.PAGES_PATH: (module.PAGES_BYTES, module.PAGES_SHA256, True),
    module.PDF_PATH: (
        9_507_127,
        "1bad03f9ba031ba91967a0a0ac2af6d15a0f768882cd541fe26dcbe26c4edd0b",
        True,
    ),
    module.MANIFEST_PATH: (
        369,
        "11d45714eddfecfc63a6d660f1dedac99a3ecf3d5fb36dc19961e34fb26c137c",
        True,
    ),
}

module.REQUIRED_DYNAMIC_CHANGED = {
    ".github/workflows/pages.yml",
    "00_control/CURRENT_GOAL_AND_WORKFLOW.md",
    "00_control/CURRENT_STATE.md",
    "00_control/CURSOR.json",
    "00_control/BUILD.md",
    "README.md",
    module.FINAL_BUILD_RECEIPT,
    module.VISUAL_RECEIPT,
    module.BROWSER_RECEIPT,
    module.ZENODO_RECEIPT_PATH,
    "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_002_CUMULATIVE_RECEIPT.json",
    "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_002_FILE_MANIFEST.csv",
    "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_002_PLAN.json",
    "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_002_RECEIPT.json",
    "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_002_REPLAY_RECEIPT.json",
    "scripts/verify-github-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-"
    "ca02-ca03-lab01-lab02.py",
}
module.ALLOWED_CHANGED_PREFIXES = (
    "00_control/",
    "backend/",
    "output/",
    "qa/",
    module.ZENODO_RELEASE_DIR + "/",
    "scripts/",
    "source/id-ID/labs/",
)


def verify_backend_receipt() -> dict[str, object]:
    path = ROOT / "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_002_CUMULATIVE_RECEIPT.json"
    receipt = json.loads(path.read_text(encoding="utf-8"))
    if receipt.get("status") != "PASS":
        raise RuntimeError("Lab 2 backend cumulative receipt is not PASS")
    if receipt.get("immutable_prefix") != {
        "bundle_sha256": "4740eb2ff83b4f9df3c0d90c2426ff77e652b23cad0bbe7763c54ebdefa60b4b",
        "bytes": 8_975_700,
        "preserved_exactly": True,
        "records": 7_404,
    }:
        raise RuntimeError("Lab 2 immutable backend prefix receipt changed")
    cumulative = receipt.get("cumulative", {})
    expected = (
        7_546,
        9_122_755,
        "ac3a0377861ed2b728f9c7473579fdd4febe43e454a92f3ea06451e13d46c8f8",
        2,
        4,
    )
    actual = (
        cumulative.get("records"),
        cumulative.get("bytes"),
        cumulative.get("bundle_sha256"),
        cumulative.get("computation_laboratories_complete"),
        cumulative.get("computation_laboratories_required"),
    )
    if actual != expected:
        raise RuntimeError(f"Lab 2 cumulative backend identity changed: {actual}")
    total_bytes = 0
    total_records = 0
    for row in receipt.get("files", []):
        relative = row.get("path")
        if not isinstance(relative, str) or not relative.startswith("backend/"):
            raise RuntimeError("malformed Lab 2 backend file row")
        payload = module.normalized_local_path(relative).read_bytes()
        identity = (len(payload), len(payload.splitlines()), module.sha256(payload))
        expected_identity = (
            row.get("final_bytes"), row.get("final_records"), row.get("final_sha256")
        )
        if identity != expected_identity:
            raise RuntimeError(f"backend file no longer matches receipt: {relative}")
        if row.get("prefix_preserved") is not True or row.get("suffix_exact") is not True:
            raise RuntimeError(f"backend append-only flags failed: {relative}")
        total_bytes += len(payload)
        total_records += len(payload.splitlines())
    if (total_records, total_bytes) != (7_546, 9_122_755):
        raise RuntimeError("backend file totals do not match Lab 2 receipt")
    return {
        "records": total_records,
        "bytes": total_bytes,
        "bundle_sha256": cumulative["bundle_sha256"],
        "immutable_prefix_records": 7_404,
        "immutable_prefix_preserved": True,
    }


def verify_final_local_gates(zenodo_record_id: int, zenodo_version: str) -> dict[str, Any]:
    for relative in (
        module.FINAL_BUILD_RECEIPT,
        module.VISUAL_RECEIPT,
        module.BROWSER_RECEIPT,
        module.ZENODO_RECEIPT_PATH,
    ):
        module.normalized_local_path(relative)
    build = json.loads((ROOT / module.FINAL_BUILD_RECEIPT).read_text(encoding="utf-8"))
    browser = json.loads((ROOT / module.BROWSER_RECEIPT).read_text(encoding="utf-8"))
    visual = (ROOT / module.VISUAL_RECEIPT).read_text(encoding="utf-8")
    if not str(build.get("status", "")).startswith("PASS"):
        raise RuntimeError("final Lab 2 build receipt is not PASS")
    if not str(browser.get("status", "")).startswith("PASS"):
        raise RuntimeError("Lab 2 browser receipt is not PASS")
    if "PASS" not in visual:
        raise RuntimeError("Lab 2 visual receipt does not record PASS")
    zenodo = json.loads((ROOT / module.ZENODO_RECEIPT_PATH).read_text(encoding="utf-8"))
    verification = zenodo.get("verification", {})
    if (
        zenodo.get("status") != "PUBLISHED_AND_TWICE_ANONYMOUSLY_VERIFIED"
        or zenodo.get("record_id") != zenodo_record_id
        or zenodo.get("doi") != f"10.5281/zenodo.{zenodo_record_id}"
        or zenodo.get("concept_doi") != module.CONCEPT_DOI
        or zenodo.get("version") != zenodo_version
        or verification.get("anonymous_readback_passes") != 2
        or verification.get("all_sha256_match_local_on_both_passes") is not True
        or verification.get("published_not_draft") is not True
        or verification.get("credentials_recorded") is not False
    ):
        raise RuntimeError("local Zenodo Lab 2 publication receipt is incomplete")
    return zenodo


module.verify_backend_receipt = verify_backend_receipt
module.verify_final_local_gates = verify_final_local_gates


def main() -> int:
    args = module.parse_args()
    module.parse_args = lambda: args
    result = module.main()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    receipt = json.loads(output.read_text(encoding="utf-8"))
    receipt["schema_version"] = "1.2"
    receipt["scope"] = (
        "Roberts 30/30; selected Fomberg Sections 1.1-1.13 complete; "
        "CA01/02/03 24/24; ordinary mastery 84/84; solution-bearing mastery "
        "108/108; computation laboratories 1-2/4 complete; laboratories 3-4, "
        "proof-metadata closure, and capstone pending"
    )
    receipt["publication_truth"] = {
        "ordinary_mastery": "84/84",
        "cumulative_assessments": "24/24",
        "total_required_mastery": "108/108",
        "computation_laboratories": "2/4",
        "remaining_laboratories": 2,
        "proof_metadata_closure_pending": True,
        "capstone_pending": True,
        "course_complete": False,
    }
    output.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"status": receipt["status"], "receipt": str(output)}, sort_keys=True))
    return result


if __name__ == "__main__":
    raise SystemExit(main())
