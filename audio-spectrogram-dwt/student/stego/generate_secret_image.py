#!/usr/bin/env python3
import argparse
import os
import struct
import zlib


def home_path(*parts):
    base = os.environ.get("HOME") or os.path.expanduser("~")
    return os.path.join(base, *parts)


RESULT = home_path(".local", "result", "spectrogram_dwt_check.txt")


def mark(token):
    os.makedirs(os.path.dirname(RESULT), exist_ok=True)
    existing = set()
    if os.path.exists(RESULT):
        with open(RESULT, "r", encoding="utf-8") as handle:
            existing = {line.strip() for line in handle if line.strip()}
    existing.add(token)
    with open(RESULT, "w", encoding="utf-8") as handle:
        handle.write("\n".join(sorted(existing)) + "\n")


def chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def write_gray_png(path, width=64, height=64):
    rows = []
    for y in range(height):
        row = bytearray([0])
        for x in range(width):
            wave = int(80 + 70 * ((x % 16) / 15.0))
            diagonal = int(80 * ((x + y) % 32) / 31.0)
            stripe = 45 if (y // 8) % 2 == 0 else 0
            row.append(max(0, min(255, wave + diagonal + stripe)))
        rows.append(bytes(row))
    raw = b"".join(rows)
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0)
    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")
    with open(path, "wb") as handle:
        handle.write(data)
    mark("PASS_SECRET_IMAGE_CREATED")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="secret.png")
    args = parser.parse_args()
    write_gray_png(args.out)
    print(f"wrote={args.out}")


if __name__ == "__main__":
    main()
