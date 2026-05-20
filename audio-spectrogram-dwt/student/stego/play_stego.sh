#!/bin/bash
set -e
cd "$(dirname "$0")"
if [ ! -s stego.wav ]; then
    echo "stego.wav chua ton tai."
    exit 1
fi
if ! ls /dev/snd/pcm* >/dev/null 2>&1; then
    echo "VM/container chua duoc expose soundcard, nen khong the phat audio truc tiep."
    exit 1
fi
exec aplay -q stego.wav
