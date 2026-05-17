#!/usr/bin/env python3
import subprocess
import sys


def get_inputs():
    # TODO: sua ten file audio goc ma em muon dung de nhung anh.
    COVER_FILE = "TODO_COVER_FILENAME"

    # TODO: sua ten file anh bi mat ma em tao truoc khi nhung.
    SECRET_IMAGE = "TODO_SECRET_IMAGE_FILENAME"

    output_audio = "stego.wav"
    if "TODO" in COVER_FILE or "TODO" in SECRET_IMAGE:
        raise SystemExit("Hay mo embed_task.py va dien ten cover.wav va secret.png truoc khi chay.")
    return COVER_FILE, SECRET_IMAGE, output_audio


def main():
    cover_file, secret_image, output_audio = get_inputs()
    cmd = [
        "python3",
        "spectrogram_dwt_stego.py",
        "embed",
        "--cover",
        cover_file,
        "--secret",
        secret_image,
        "--out",
        output_audio,
    ]
    subprocess.run(cmd, check=True)
    print(f"Da nhung anh {secret_image} vao {output_audio} su dung audio {cover_file}.")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
