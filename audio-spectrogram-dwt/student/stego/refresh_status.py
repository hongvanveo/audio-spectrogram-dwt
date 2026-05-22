#!/usr/bin/env python3
from pathlib import Path


def home_dir():
    return Path(__import__("os").environ.get("HOME") or str(Path.home()))


WORKDIR = home_dir() / "stego"
RESULT = home_dir() / ".local" / "result" / "spectrogram_dwt_check.txt"


def main():
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    tokens = set()
    if RESULT.is_file():
        tokens.update(line.strip() for line in RESULT.read_text(encoding="utf-8").splitlines() if line.strip())
    if (WORKDIR / "cover.wav").is_file() and (WORKDIR / "cover.wav").stat().st_size > 0:
        tokens.add("PASS_COVER_CREATED")
    if (WORKDIR / "secret.png").is_file() and (WORKDIR / "secret.png").stat().st_size > 0:
        tokens.add("PASS_SECRET_IMAGE_CREATED")
    if (WORKDIR / ".image_processed").is_file():
        tokens.add("PASS_IMAGE_PROCESSED")
    if (WORKDIR / ".istft_signal_created").is_file():
        tokens.add("PASS_ISTFT_SIGNAL_CREATED")
    if (WORKDIR / ".dwt_highfreq_embedded").is_file():
        tokens.add("PASS_DWT_HIGHFREQ_EMBEDDED")
    if (WORKDIR / "stego.wav").is_file() and (WORKDIR / "stego.wav").stat().st_size > 0:
        tokens.add("PASS_STEGO_CREATED")
    if (WORKDIR / ".analysis_done").is_file() and (WORKDIR / ".analysis_done").stat().st_size > 0:
        tokens.add("PASS_AUDIO_MODIFIED")
    if (WORKDIR / ".secret_image_viewed").is_file() and (WORKDIR / ".secret_image_viewed").stat().st_size > 0:
        tokens.add("PASS_SECRET_IMAGE_VIEWED")
    RESULT.write_text("\n".join(sorted(tokens)) + ("\n" if tokens else ""), encoding="utf-8")


if __name__ == "__main__":
    main()
