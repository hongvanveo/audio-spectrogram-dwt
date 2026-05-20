#!/usr/bin/env python3
import argparse
import math
import os
import random
import struct
import wave
import zlib
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
    return rows


def permute_image(image, key):
    height = len(image)
    width = len(image[0]) if image else 0
    flat = [value for row in image for value in row]
    order = list(range(len(flat)))
    rng = random.Random(key)
    rng.shuffle(order)
    shuffled = [flat[idx] for idx in order]
    out = []
    for start in range(0, len(shuffled), width):
        out.append(shuffled[start:start + width])
    mark("PASS_IMAGE_PROCESSED")
    return out


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


def haar_dwt_level(samples):
    approx = []
    detail = []
    inv = 1.0 / math.sqrt(2.0)
    for i in range(0, len(samples), 2):
        a = samples[i]
        b = samples[i + 1] if i + 1 < len(samples) else samples[i]
        approx.append((a + b) * inv)
        detail.append((a - b) * inv)
    return approx, detail


def haar_idwt_level(approx, detail, out_len):
    inv = 1.0 / math.sqrt(2.0)
    out = []
    for a, d in zip(approx, detail):
        out.append((a + d) * inv)
        out.append((a - d) * inv)
    return out[:out_len]


def multilevel_haar_dwt(samples, embedded_len):
    approx = list(samples)
    details = []
    sizes = []
    max_level = max(1, int(math.floor(math.log2(max(2, len(samples) / max(1, embedded_len))))))
    for _ in range(max_level):
        sizes.append(len(approx))
        approx, detail = haar_dwt_level(approx)
        details.append(detail)
    return approx, details, sizes


def multilevel_haar_idwt(approx, details, sizes):
    current = list(approx)
    for detail, size in zip(reversed(details), reversed(sizes)):
        current = haar_idwt_level(current, detail, size)
    return current


def scale_hidden_signal(hidden, reference):
    ref_peak = max((abs(x) for x in reference), default=1.0) or 1.0
    hidden_peak = max((abs(x) for x in hidden), default=1.0) or 1.0
    scaled = hidden_peak / ref_peak if ref_peak > 0 else 1.0
    return [x / scaled for x in hidden], scaled


def embed(args):
    params, samples = read_wav(args.cover)
    mark("PASS_COVER_CREATED")
    image = read_png_gray(args.secret)
    if os.path.getsize(args.secret) > 0:
        mark("PASS_SECRET_IMAGE_CREATED")
    encrypted_image = permute_image(image, args.key)
    approx, details, sizes = multilevel_haar_dwt([float(x) for x in samples], len(encrypted_image) * len(encrypted_image[0]))
    target_detail = list(details[-1])
    hidden = inverse_stft_from_image(encrypted_image, len(target_detail), params.framerate)
    overwritten_detail, scaled = scale_hidden_signal(hidden, target_detail)
    details[-1] = overwritten_detail
    stego = multilevel_haar_idwt(approx, details, sizes)
    write_wav(args.out, params, stego)
    with open(".dwt_highfreq_embedded", "w", encoding="utf-8") as handle:
        handle.write(f"detail_coefficients={len(target_detail)}\n")
        handle.write(f"levels={len(details)}\n")
        handle.write(f"key={args.key}\n")
        handle.write(f"scaled={scaled:.6f}\n")
    mark("PASS_DWT_HIGHFREQ_EMBEDDED")
    mark("PASS_STEGO_CREATED")
    print(f"image_rows={len(encrypted_image)}")
    print(f"image_cols={len(encrypted_image[0]) if encrypted_image else 0}")
    print(f"dwt_levels={len(details)}")
    print(f"detail_coefficients={len(target_detail)}")
    print(f"wrote={args.out}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["embed"])
    parser.add_argument("--cover", required=True)
    parser.add_argument("--secret", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--key", type=int, default=3101)
    args = parser.parse_args()
    embed(args)


if __name__ == "__main__":
    main()
