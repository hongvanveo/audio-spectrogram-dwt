#!/bin/bash
set -e
cd "$(dirname "$0")"
if [ ! -s cover.wav ]; then
    echo "cover.wav chua ton tai."
    exit 1
fi
exec aplay -q cover.wav
