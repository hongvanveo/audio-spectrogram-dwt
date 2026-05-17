#!/usr/bin/env python3
import argparse
import math
import os
import struct
import wave
import zlib
from array import array


RESULT = os.path.expanduser("~/.local/result/spectrogram_dwt_check.txt")


def mark(token):
    os.makedirs(os.path.dirname(RESULT), exist_ok=True)
    existing = set()
    if os.path.exists(RESULT):
        with open(RESULT, "r", encoding="utf-8") as handle:
            existing = {line.strip() for line in handle if line.strip()}
    existing.add(token)
    with open(RESULT, "w", encoding="utf-8") as handle:
        handle.write("\n".join(sorted(existing)) + "\n")


def read_wav(path):
    with wave.open(path, "rb") as wav:
        params = wav.getparams()
        frames = wav.readframes(params.nframes)
    if params.sampwidth != 2 or params.nchannels != 1:
        raise ValueError("cover.wav must be mono PCM16")
    samples = array("h")
    samples.frombytes(frames)
    return params, samples


def write_wav(path, params, samples):
    out = array("h", (max(-32768, min(32767, int(round(x)))) for x in samples))
    with wave.open(path, "wb") as wav:
        wav.setparams(params)
        wav.writeframes(out.tobytes())


def paeth(a, b, c):
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def read_png_gray(path):
    with open(path, "rb") as handle:
        data = handle.read()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("secret image must be PNG")
    pos = 8
    width = height = color_type = bit_depth = None
    compressed = b""
    while pos < len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        chunk = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if ctype == b"IHDR":
            width, height, bit_depth, color_type = struct.unpack(">IIBB", chunk[:10])
        elif ctype == b"IDAT":
            compressed += chunk
        elif ctype == b"IEND":
            break
    if bit_depth != 8 or color_type not in (0, 2):
        raise ValueError("secret.png must be 8-bit grayscale or RGB")
    channels = 1 if color_type == 0 else 3
    raw = zlib.decompress(compressed)
    stride = width * channels
    rows = []
    prev = [0] * stride
    i = 0
    for _ in range(height):
        filt = raw[i]
        i += 1
        scan = list(raw[i:i + stride])
        i += stride
        recon = [0] * stride
        for x, value in enumerate(scan):
            left = recon[x - channels] if x >= channels else 0
            up = prev[x]
            up_left = prev[x - channels] if x >= channels else 0
            if filt == 0:
                recon[x] = value
            elif filt == 1:
                recon[x] = (value + left) & 255
            elif filt == 2:
                recon[x] = (value + up) & 255
            elif filt == 3:
                recon[x] = (value + ((left + up) // 2)) & 255
            elif filt == 4:
                recon[x] = (value + paeth(left, up, up_left)) & 255
            else:
                raise ValueError("unsupported PNG filter")
        if channels == 1:
            rows.append([v / 255.0 for v in recon])
        else:
            rows.append([
                (0.299 * recon[j] + 0.587 * recon[j + 1] + 0.114 * recon[j + 2]) / 255.0
                for j in range(0, len(recon), 3)
            ])
        prev = recon
    mark("PASS_IMAGE_PROCESSED")
    return rows


def inverse_stft_from_image(image, out_len, sample_rate):
    bins = min(24, len(image))
    frames = min(64, len(image[0]))
    frame_len = max(128, out_len // frames)
    signal = [0.0] * (frame_len * frames)
    for frame in range(frames):
        for n in range(frame_len):
            t = (frame * frame_len + n) / float(sample_rate)
            value = 0.0
            for b in range(bins):
                mag = image[b][frame] - 0.5
                freq = 700.0 + b * 95.0
                value += mag * math.sin(2.0 * math.pi * freq * t)
            signal[frame * frame_len + n] = value / bins
    peak = max((abs(x) for x in signal), default=1.0) or 1.0
    scaled = [x / peak for x in signal]
    if len(scaled) < out_len:
        repeats = (out_len + len(scaled) - 1) // len(scaled)
        scaled = (scaled * repeats)[:out_len]
    else:
        scaled = scaled[:out_len]
    with open(".istft_signal_created", "w", encoding="utf-8") as handle:
        handle.write(f"samples={len(scaled)}\n")
    mark("PASS_ISTFT_SIGNAL_CREATED")
    return scaled


def haar_dwt(samples):
    even_len = len(samples) - (len(samples) % 2)
    approx = []
    detail = []
    inv = 1.0 / math.sqrt(2.0)
    for i in range(0, even_len, 2):
        a = samples[i]
        b = samples[i + 1]
        approx.append((a + b) * inv)
        detail.append((a - b) * inv)
    tail = samples[even_len:]
    return approx, detail, tail


def haar_idwt(approx, detail, tail):
    inv = 1.0 / math.sqrt(2.0)
    out = []
    for a, d in zip(approx, detail):
        out.append((a + d) * inv)
        out.append((a - d) * inv)
    out.extend(tail)
    return out


def embed(args):
    params, samples = read_wav(args.cover)
    mark("PASS_COVER_CREATED")
    image = read_png_gray(args.secret)
    if os.path.getsize(args.secret) > 0:
        mark("PASS_SECRET_IMAGE_CREATED")
    approx, detail, tail = haar_dwt([float(x) for x in samples])
    hidden = inverse_stft_from_image(image, len(detail), params.framerate)
    strength = args.strength
    stego_detail = [d + strength * h * 32767.0 for d, h in zip(detail, hidden)]
    stego = haar_idwt(approx, stego_detail, tail)
    write_wav(args.out, params, stego)
    with open(".dwt_highfreq_embedded", "w", encoding="utf-8") as handle:
        handle.write(f"detail_coefficients={len(detail)}\nstrength={strength}\n")
    mark("PASS_DWT_HIGHFREQ_EMBEDDED")
    mark("PASS_STEGO_CREATED")
    print(f"image_rows={len(image)}")
    print(f"image_cols={len(image[0]) if image else 0}")
    print(f"detail_coefficients={len(detail)}")
    print(f"wrote={args.out}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["embed"])
    parser.add_argument("--cover", required=True)
    parser.add_argument("--secret", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--strength", type=float, default=0.018)
    args = parser.parse_args()
    embed(args)


if __name__ == "__main__":
    main()
