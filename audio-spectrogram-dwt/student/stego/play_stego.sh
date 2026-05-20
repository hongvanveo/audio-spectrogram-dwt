#!/bin/bash
set -e
cd "$(dirname "$0")"
if [ ! -s stego.wav ]; then
    echo "stego.wav chua ton tai."
    exit 1
fi
exec aplay -q stego.wav
