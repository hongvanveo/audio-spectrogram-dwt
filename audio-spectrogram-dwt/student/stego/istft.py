#!/usr/bin/env python3
import json

from spectrogram_dwt_stego import (
    inverse_stft_from_image,
    mark,
    multilevel_haar_dwt,
    read_wav,
)


def get_inputs():
    # Dien ten file audio cover dung de tinh kich thuoc he so DWT vao chuoi rong ben duoi.
    COVER_FILE = ""

    # Dien file ma tran anh da xu ly tu process_image.py vao chuoi rong ben duoi.
    PROCESSED_IMAGE = ""

    OUTPUT_SIGNAL = "hidden_signal.json"
    if not COVER_FILE.strip() or not PROCESSED_IMAGE.strip():
        raise SystemExit("Hay mo istft.py va dien cover.wav va processed_image.json vao cac chuoi rong truoc khi chay.")
    return COVER_FILE, PROCESSED_IMAGE, OUTPUT_SIGNAL


def main():
    cover_file, processed_image_file, output_signal = get_inputs()
    params, samples = read_wav(cover_file)
    with open(processed_image_file, "r", encoding="utf-8") as handle:
        image_info = json.load(handle)
    image = image_info["matrix"]
    embedded_len = image_info["width"] * image_info["height"]
    _, details, _ = multilevel_haar_dwt([float(x) for x in samples], embedded_len)
    target_len = len(details[-1])
    hidden = inverse_stft_from_image(image, target_len, params.framerate)
    with open(output_signal, "w", encoding="utf-8") as handle:
        json.dump(
            {
                "source_image_matrix": processed_image_file,
                "cover": cover_file,
                "sample_rate": params.framerate,
                "target_detail_len": target_len,
                "width": image_info["width"],
                "height": image_info["height"],
                "key": image_info["key"],
                "signal": hidden,
            },
            handle,
        )
    mark("PASS_COVER_CREATED")
    mark("PASS_IMAGE_PROCESSED")
    mark("PASS_ISTFT_SIGNAL_CREATED")
    print(f"cover={cover_file}")
    print(f"processed_image={processed_image_file}")
    print(f"hidden_signal={output_signal}")
    print(f"samples={len(hidden)}")


if __name__ == "__main__":
    main()
