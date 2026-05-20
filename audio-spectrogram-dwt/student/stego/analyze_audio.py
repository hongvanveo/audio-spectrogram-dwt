#!/usr/bin/env python3
import argparse
import math
import os
import wave
from array import array


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


def read(path):
    with wave.open(path, "rb") as wav:
        params = wav.getparams()
        frames = wav.readframes(params.nframes)
    samples = array("h")
    samples.frombytes(frames)
    return params, samples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cover", required=True)
    parser.add_argument("--stego", required=True)
    args = parser.parse_args()
    p1, cover = read(args.cover)
    p2, stego = read(args.stego)
    if p1[:3] != p2[:3] or len(cover) != len(stego):
        raise SystemExit("audio files are not comparable")
    signal = sum(float(x) * x for x in cover)
    noise = sum(float(a - b) * (a - b) for a, b in zip(cover, stego))
    changed = sum(1 for a, b in zip(cover, stego) if a != b)
    snr = float("inf") if noise == 0 else 10 * math.log10(signal / noise)
    print(f"changed_samples={changed}")
    print(f"snr_db={snr:.2f}")
    marker = ".analysis_done"
    if changed > 0:
        with open(marker, "w", encoding="utf-8") as handle:
            handle.write(f"changed_samples={changed}\n")
            handle.write(f"snr_db={snr:.2f}\n")
        mark("PASS_AUDIO_MODIFIED")
    elif os.path.exists(marker):
        os.remove(marker)


if __name__ == "__main__":
    main()
