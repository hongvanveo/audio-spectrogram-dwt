#!/usr/bin/env python3
import json

from spectrogram_dwt_stego import (
    mark,
    multilevel_haar_dwt,
    multilevel_haar_idwt,
    read_wav,
    scale_hidden_signal,
    write_wav,
)


def get_inputs():
    # Dien ten file audio cover vao chuoi rong ben duoi.
    COVER_FILE = ""

    # Dien file tin hieu mien thoi gian tu istft.py vao chuoi rong ben duoi.
    HIDDEN_SIGNAL = ""

    OUTPUT_AUDIO = "stego.wav"
    if not COVER_FILE.strip() or not HIDDEN_SIGNAL.strip():
        raise SystemExit("Hay mo dwt_embed.py va dien cover.wav va hidden_signal.json vao cac chuoi rong truoc khi chay.")
    return COVER_FILE, HIDDEN_SIGNAL, OUTPUT_AUDIO


def main():
    cover_file, hidden_signal_file, output_audio = get_inputs()
    params, samples = read_wav(cover_file)
    with open(hidden_signal_file, "r", encoding="utf-8") as handle:
        hidden_info = json.load(handle)
    hidden = hidden_info["signal"]
    embedded_len = hidden_info["width"] * hidden_info["height"]
    approx, details, sizes = multilevel_haar_dwt([float(x) for x in samples], embedded_len)
    target_detail = list(details[-1])
    if len(hidden) != len(target_detail):
        raise ValueError("hidden_signal.json khong khop voi cover.wav")
    overwritten_detail, scaled = scale_hidden_signal(hidden, target_detail)
    details[-1] = overwritten_detail
    stego = multilevel_haar_idwt(approx, details, sizes)
    write_wav(output_audio, params, stego)
    with open(".dwt_highfreq_embedded", "w", encoding="utf-8") as handle:
        handle.write(f"detail_coefficients={len(target_detail)}\n")
        handle.write(f"levels={len(details)}\n")
        handle.write(f"key={hidden_info['key']}\n")
        handle.write(f"scaled={scaled:.6f}\n")
    mark("PASS_COVER_CREATED")
    mark("PASS_ISTFT_SIGNAL_CREATED")
    mark("PASS_DWT_HIGHFREQ_EMBEDDED")
    mark("PASS_STEGO_CREATED")
    print(f"cover={cover_file}")
    print(f"hidden_signal={hidden_signal_file}")
    print(f"dwt_levels={len(details)}")
    print(f"detail_coefficients={len(target_detail)}")
    print(f"stego={output_audio}")


if __name__ == "__main__":
    main()
