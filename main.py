"""THE SUNDAY ATLAS untuk @sindyariana115203 (Akun 10) — NI22 Wave 7.

Atlas Minggu ini merangkum berita dunia dalam satu halaman persegi yang rapat dan terbaca sekilas.
Skrip kecil ini hanya bertugas memeriksa berkas gambar di sisinya lalu
menyalinnya utuh ke folder keluaran, tanpa mengubah satu byte pun.
"""

import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

CONCEPT = "THE SUNDAY ATLAS"
ACCOUNT = "@sindyariana115203"
ACCOUNT_LABEL = "Akun 10"
BOUNTY = "news-image-20261122"
STORIES = 36
MAX_SIDE = 1024

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def main():
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        return fail("entry.png tidak ditemukan di sebelah main.py")

    header = source.read_bytes()[:33]
    if len(header) < 33 or header[:8] != PNG_SIGNATURE:
        return fail("signature PNG tidak sah")
    if header[12:16] != b"IHDR":
        return fail("chunk IHDR tidak ada di posisi yang diharapkan")
    width, height = struct.unpack(">II", header[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        return fail(f"dimensi {width}x{height} melewati batas {MAX_SIDE}")

    data = source.read_bytes()
    size = len(data)
    digest = hashlib.sha256(data).hexdigest()

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(source, target)

    copied = target.read_bytes()
    if len(copied) != size or hashlib.sha256(copied).hexdigest() != digest:
        return fail("salinan tidak sama persis dengan sumber")

    print(f"Concept: {CONCEPT}")
    print(f"Account: {ACCOUNT} ({ACCOUNT_LABEL})")
    print(f"Bounty: {BOUNTY}")
    print("File: entry.png")
    print(f"Size: {size}")
    print(f"Dim: {width}x{height}")
    print(f"SHA256: {digest}")
    print(f"Stories: {STORIES}")
    print("Copy verified byte-identical.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
