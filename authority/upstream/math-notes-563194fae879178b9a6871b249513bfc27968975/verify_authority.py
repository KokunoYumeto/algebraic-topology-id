#!/usr/bin/env python3
"""Verify the frozen SourceHut witness without invoking Git.

This script performs two bounded checks: it hashes the extracted archive as
Git blob/tree objects, and it asks the official SourceHut upload-pack endpoint
for a depth-one witness of the exact commit so the commit-to-tree edge can be
verified directly. It never creates a repository or mutates the frozen tree.
"""

from __future__ import annotations

import hashlib
import os
import re
import struct
import sys
import urllib.request
import zlib
from pathlib import Path


COMMIT = "563194fae879178b9a6871b249513bfc27968975"
EXPECTED_TREE = "fb678966d1533d529bdd72f49d8496a3bdc14a9b"
REPOSITORY = "https://git.sr.ht/~yp/math-notes"
ROOT = Path(__file__).resolve().parent
TREE = ROOT / "tree"


def object_id(kind: bytes, body: bytes) -> tuple[bytes, str]:
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
            raw_id, hex_id, descendants = tree_id(child)
            mode = b"40000"
            inventory.extend(descendants)
        elif child.is_file():
            data = child.read_bytes()
            raw_id, hex_id = object_id(b"blob", data)
            mode = b"100644"
            inventory.append(
                {
                    "path": child.relative_to(TREE).as_posix(),
                    "mode": mode.decode("ascii"),
                    "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "git_blob_sha1": hex_id,
                }
            )
        else:
            raise RuntimeError(f"unsupported archive entry type: {child}")
        payload.extend(mode + b" " + os.fsencode(child.name) + b"\0" + raw_id)
    raw_tree, hex_tree = object_id(b"tree", bytes(payload))
    return raw_tree, hex_tree, inventory


def pkt_line(payload: bytes) -> bytes:
    return f"{len(payload) + 4:04x}".encode("ascii") + payload


def official_depth_one_response() -> bytes:
    info_url = f"{REPOSITORY}/info/refs?service=git-upload-pack"
    with urllib.request.urlopen(info_url, timeout=30) as response:
        advertisement = response.read()
    if COMMIT.encode("ascii") + b" HEAD" not in advertisement:
        raise RuntimeError("official advertisement does not identify the frozen commit as HEAD")

    request_body = b"".join(
        [
            pkt_line(f"want {COMMIT} no-progress ofs-delta\n".encode("ascii")),
            pkt_line(b"deepen 1\n"),
            b"0000",
            pkt_line(b"done\n"),
        ]
    )
    request = urllib.request.Request(
        f"{REPOSITORY}/git-upload-pack",
        data=request_body,
        method="POST",
        headers={
            "Content-Type": "application/x-git-upload-pack-request",
            "Accept": "application/x-git-upload-pack-result",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def first_pack_objects(response: bytes, limit: int = 2) -> list[tuple[int, bytes, str]]:
    pack_at = response.find(b"PACK")
    if pack_at < 0:
        raise RuntimeError("official response contains no PACK stream")
    pack = response[pack_at:]
    if len(pack) < 12 or pack[:4] != b"PACK":
        raise RuntimeError("malformed PACK header")
    version, count = struct.unpack(">II", pack[4:12])
    if version not in (2, 3):
        raise RuntimeError(f"unsupported PACK version {version}")
    if count < limit:
        raise RuntimeError(f"PACK has only {count} objects")

    offset = 12
    objects: list[tuple[int, bytes, str]] = []
    for _ in range(limit):
        byte = pack[offset]
        offset += 1
        object_type = (byte >> 4) & 0x07
        size = byte & 0x0F
        shift = 4
        while byte & 0x80:
            byte = pack[offset]
            offset += 1
            size |= (byte & 0x7F) << shift
            shift += 7
        if object_type in (6, 7):
            raise RuntimeError("a required leading commit/tree object is delta encoded")
        decompressor = zlib.decompressobj()
        body = decompressor.decompress(pack[offset:])
        if not decompressor.eof:
            raise RuntimeError("truncated zlib member in PACK")
        consumed = len(pack[offset:]) - len(decompressor.unused_data)
        offset += consumed
        if len(body) != size:
            raise RuntimeError(f"PACK size mismatch: header {size}, body {len(body)}")
        kinds = {1: b"commit", 2: b"tree", 3: b"blob", 4: b"tag"}
        kind = kinds.get(object_type)
        if kind is None:
            raise RuntimeError(f"unexpected leading object type {object_type}")
        _, hex_id = object_id(kind, body)
        objects.append((object_type, body, hex_id))
    return objects


def main() -> int:
    _, local_tree, inventory = tree_id(TREE)
    response = official_depth_one_response()
    objects = first_pack_objects(response)
    commit_type, commit_body, commit_id = objects[0]
    tree_type, _tree_body, remote_tree_object_id = objects[1]
    tree_match = re.search(rb"^tree ([0-9a-f]{40})$", commit_body, re.MULTILINE)
    commit_tree = tree_match.group(1).decode("ascii") if tree_match else ""

    print(f"official_commit={commit_id}")
    print(f"official_commit_tree={commit_tree}")
    print(f"official_leading_tree_object={remote_tree_object_id}")
    print(f"local_archive_tree={local_tree}")
    print(f"tracked_files={len(inventory)}")
    print(f"depth_one_response_bytes={len(response)}")
    print(f"depth_one_response_sha256={hashlib.sha256(response).hexdigest()}")

    checks = [
        commit_type == 1,
        tree_type == 2,
        commit_id == COMMIT,
        commit_tree == EXPECTED_TREE,
        remote_tree_object_id == EXPECTED_TREE,
        local_tree == EXPECTED_TREE,
        len(inventory) == 63,
    ]
    if not all(checks):
        print("authority_verification=FAIL", file=sys.stderr)
        return 1
    print("authority_verification=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
