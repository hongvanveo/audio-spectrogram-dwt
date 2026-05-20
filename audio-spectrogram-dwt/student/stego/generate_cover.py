#!/usr/bin/env python3
import argparse
import math
import os
import wave
from array import array


def home_path(*parts):
    base = os.environ.get("HOME") or os.path.expanduser("~")
    return os.path.join(base, *parts)


def mark(token):
    result = home_path(".local", "result", "spectrogram_dwt_check.txt")
    os.makedirs(os.path.dirname(result), exist_ok=True)
    existing = ""
    if os.path.exists(result):
        with open(result, "r", encoding="utf-8") as handle:
            existing = handle.read()
    if token not in existing:
        with open(result, "a", encoding="utf-8") as handle:
            handle.write(token + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="cover.wav")
    parser.add_argument("--seconds", type=float, default=7.0)
    parser.add_argument("--rate", type=int, default=44100)
    args = parser.parse_args()

    samples = array("h")
    for i in range(int(args.seconds * args.rate)):
        t = i / args.rate
        value = 0.40 * math.sin(2 * math.pi * 520 * t)
        value += 0.30 * math.sin(2 * math.pi * 1040 * t)
        value += 0.12 * math.sin(2 * math.pi * 1600 * t)
        samples.append(int(value * 25000))

    with wave.open(args.out, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(args.rate)
        wav.writeframes(samples.tobytes())
    mark("PASS_COVER_CREATED")
    print(f"created={args.out}")


if __name__ == "__main__":
    main()
