#!/usr/bin/env python3
"""Seal the exact local input ledger for the Fomberg Unit 007 release.

This helper performs no network, Git, credential, deposition, or publication
action. It refuses to overwrite an existing ledger and derives every entry
from the release packager's bounded required-input inventory.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from hashlib import sha256
from pathlib import Path


SCRIPT = Path(__file__).resolve()
PACKAGER_PATH = SCRIPT.with_name(
    "package-release-roberts-001-030-fomberg-001-007.py"
)


def load_packager():
    spec = importlib.util.spec_from_file_location("o012_fomberg_007_packager", PACKAGER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load the Unit 007 release packager")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    value = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main() -> int:
    if sys.argv[1:]:
        raise RuntimeError("this sealer accepts no arguments")
    packager = load_packager()
    packager.verify_controls()
    target = packager.FROZEN_LEDGER
    if target.exists():
        raise RuntimeError("frozen-inputs.json already exists; refusing to overwrite")

    lane = packager.LANE.resolve()
    entries: list[dict[str, object]] = []
    for relative in sorted(packager.required_frozen_paths()):
        rel = Path(relative)
        if rel.is_absolute() or ".." in rel.parts:
            raise RuntimeError(f"unsafe required input path: {relative!r}")
        path = (lane / rel).resolve()
        path.relative_to(lane)
        if not path.is_file():
            raise FileNotFoundError(path)
        entries.append(
            {
                "path": rel.as_posix(),
                "bytes": path.stat().st_size,
                "sha256": digest(path),
            }
        )

    payload = {
        "schema_version": "1.0",
        "release_id": packager.RELEASE_ID,
        "state": "final_inputs_sealed_local_only",
        "final_boundary_paths": sorted(packager.FINAL_BOUNDARY_PATHS),
        "entries": entries,
    }
    raw = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
    temporary = target.with_suffix(".json.tmp")
    temporary.write_bytes(raw)
    temporary.replace(target)
    print(
        json.dumps(
            {
                "status": "PASS",
                "path": target.relative_to(lane).as_posix(),
                "entries": len(entries),
                "bytes": len(raw),
                "sha256": sha256(raw).hexdigest(),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
