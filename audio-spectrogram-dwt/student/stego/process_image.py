#!/usr/bin/env python3
import json
import os

from spectrogram_dwt_stego import mark, permute_image, read_png_gray


def get_inputs():
    # Dien ten file anh bi mat can xu ly vao chuoi rong ben duoi.
    SECRET_IMAGE = ""

    # Dien khoa dung de hoan vi anh truoc khi nhung.
    PERMUTATION_KEY = 3101

    OUTPUT_MATRIX = "processed_image.json"
    if not SECRET_IMAGE.strip():
        raise SystemExit("Hay mo process_image.py va dien ten secret.png vao chuoi rong truoc khi chay.")
    return SECRET_IMAGE, PERMUTATION_KEY, OUTPUT_MATRIX


def main():
    secret_image, permutation_key, output_matrix = get_inputs()
    image = read_png_gray(secret_image)
    processed = permute_image(image, permutation_key)
    with open(output_matrix, "w", encoding="utf-8") as handle:
        json.dump(
            {
                "source": secret_image,
                "key": permutation_key,
                "height": len(processed),
                "width": len(processed[0]) if processed else 0,
                "matrix": processed,
            },
            handle,
        )
    with open(".image_processed", "w", encoding="utf-8") as handle:
        handle.write(f"source={secret_image}\n")
        handle.write(f"key={permutation_key}\n")
        handle.write(f"output={output_matrix}\n")
    if os.path.getsize(secret_image) > 0:
        mark("PASS_SECRET_IMAGE_CREATED")
    mark("PASS_IMAGE_PROCESSED")
    print(f"source={secret_image}")
    print(f"key={permutation_key}")
    print(f"processed={output_matrix}")


if __name__ == "__main__":
    main()
