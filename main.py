#!/usr/bin/env python3
"""THE SUNDAY ATLAS — MakeFun entry carrier for Akun 10
(@sindyariana115203), NI22 Wave 7.

Wave 7 rebuild from the fresh 22 Nov 2026 pool (bedah Top 1, section 4):
15 cards + 24 briefs = 39 stories, navy on cream, Layout A (3 leads).
Fonts enlarged x1.45 vs Wave 6 so headlines stay legible at 300 px.
Stdlib-only carrier: verifies the PNG signature, reads the IHDR dimensions
and REFUSES to ship an image that breaks the 1024x1024 gate, copies
entry.png byte-for-byte into MAKEFUN_OUTPUT_DIR (fallback /output), then
verifies the copy is byte-identical.
"""
import hashlib
import os
import shutil
import struct
import sys

CONCEPT = "THE SUNDAY ATLAS — The World in One Image"
ACCOUNT = "@sindyariana115203"
ACCOUNT_LABEL = "Akun 10"
BOUNTY = "news-image-20261122"
STORIES = 39  # 15 cards + 24 briefs, 7 regions
MAX_SIDE = 1024  # server gate: dimensions must stay within 1x1..1024x1024

HERE = os.path.dirname(os.path.abspath(__file__))
ENTRY = os.path.join(HERE, "entry.png")
PNG_SIG = b"\x89PNG\r\n\x1a\n"


def png_dimensions(path):
    with open(path, "rb") as f:
        head = f.read(33)
    if len(head) < 33 or head[:8] != PNG_SIG:
        raise ValueError("entry.png: bad PNG signature")
    if head[12:16] != b"IHDR":
        raise ValueError("entry.png: first chunk is not IHDR")
    return struct.unpack(">II", head[16:24])


def sha256_of(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    if not os.path.isfile(ENTRY):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    width, height = png_dimensions(ENTRY)
    if width > MAX_SIDE or height > MAX_SIDE:
        print(f"dimension gate: {width}x{height} exceeds {MAX_SIDE}x{MAX_SIDE}",
              file=sys.stderr)
        return 1
    digest = sha256_of(ENTRY)
    size = os.path.getsize(ENTRY)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(ENTRY, dest)

    if sha256_of(dest) != digest or os.path.getsize(dest) != size:
        print("copy verification FAILED: output bytes differ", file=sys.stderr)
        return 1

    print(f"Concept : {CONCEPT}")
    print(f"Account : {ACCOUNT} ({ACCOUNT_LABEL})")
    print(f"Bounty  : {BOUNTY}")
    print(f"File    : entry.png -> {dest}")
    print(f"Size    : {size} bytes")
    print(f"Dim     : {width}x{height} px (gate <= {MAX_SIDE}x{MAX_SIDE}: OK)")
    print(f"SHA256  : {digest}")
    print(f"Stories : {STORIES} (15 cards + 24 briefs, 7 regions)")
    print("Copy verified byte-identical.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
