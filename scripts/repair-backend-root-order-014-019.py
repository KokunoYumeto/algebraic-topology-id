#!/usr/bin/env python3
"""Repair the first backend extension's root-child order collision.

The initial extension used fixed notice/lecture/mastery ordinals and exposed
the Unit 014 entry boundary as an additional root child.  This one-time,
fail-closed repair reorders only Units 014--019 root children by their exact
source line starts; it preserves every other field and every historical line.
"""

from __future__ import annotations

import json
from pathlib import Path


LANE = Path(__file__).resolve().parents[1]
BACKEND_FILE = LANE / "backend/units.jsonl"


def canonical(record: dict) -> bytes:
    return json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"


def main() -> int:
    raw_lines = BACKEND_FILE.read_bytes().splitlines(keepends=True)
    records = [json.loads(line.decode("utf-8")) for line in raw_lines]
    changed = 0
    for number in range(14, 20):
        root = f"unit:o012-rbt-u{number:03d}"
        children = [record for record in records if record.get("parent_id") == root]
        children.sort(key=lambda record: (record["target_locator"]["line_start"], record["id"]))
        for order, record in enumerate(children, start=1):
            if record["order"] != order:
                record["order"] = order
                changed += 1
    output = b"".join(canonical(record) for record in sorted(records, key=lambda record: record["id"]))
    if b"\r" in output or not output.endswith(b"\n"):
        raise SystemExit("repair would produce noncanonical JSONL")
    BACKEND_FILE.write_bytes(output)
    print(f"repaired_root_children={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
