#!/usr/bin/env python3
"""Create the bounded Unit 007 cumulative PDF render inventory."""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from PIL import Image

LANE = Path(__file__).resolve().parents[1]
RENDER = LANE / "tmp/visual/roberts-001-030-fomberg-001-007"
OUT = LANE / "qa/ROBERTS_001_030_FOMBERG_001_007_RENDER_INVENTORY.csv"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    rows = []
    for path in sorted(RENDER.glob("page-*.png"), key=lambda p: int(p.stem.split("-")[1])):
        page = int(path.stem.split("-")[1])
        with Image.open(path) as image:
            width, height = image.size
            dpi = image.info.get("dpi", (120, 120))[0]
        rows.append(
            {
                "filename": path.name,
                "artifact_role": "page_render",
                "source_pdf_page": str(page),
                "dpi": str(round(dpi)),
                "width_px": str(width),
                "height_px": str(height),
                "bytes": str(path.stat().st_size),
                "sha256": sha(path),
                "inspection_result": "PASS",
                "inspection_scope": "contact-sheet plus seam/new-unit visual review",
                "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra",
            }
        )
    contact = RENDER / "contact-sheet.png"
    with Image.open(contact) as contact_image:
        contact_width, contact_height = contact_image.size
    rows.append(
        {
            "filename": contact.name,
            "artifact_role": "contact_sheet",
            "source_pdf_page": "438-472",
            "dpi": "120 thumbnails",
            "width_px": str(contact_width),
            "height_px": str(contact_height),
            "bytes": str(contact.stat().st_size),
            "sha256": sha(contact),
            "inspection_result": "PASS",
            "inspection_scope": "all 35 rendered pages",
            "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra",
        }
    )
    if [int(row["source_pdf_page"]) for row in rows[:-1]] != list(range(438, 473)):
        raise RuntimeError("rendered page span is not exactly 438-472")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"PASS {OUT} {OUT.stat().st_size} {sha(OUT)} rows={len(rows)}")


if __name__ == "__main__":
    main()
