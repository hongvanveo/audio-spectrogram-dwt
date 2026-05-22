#!/bin/bash
set -e
cd "$(dirname "$0")"
if [ ! -s cover.wav ]; then
    echo "cover.wav chua ton tai."
    exit 1
fi

if [ -S "${PULSE_SERVER#unix:}" ]; then
    exec paplay cover.wav
fi

if aplay -L 2>/dev/null | grep -qx 'pulse'; then
    exec aplay -D pulse -q cover.wav
fi

if ls /dev/snd/pcm* >/dev/null 2>&1; then
    exec aplay -q cover.wav
fi

echo "Khong tim thay backend audio kha dung trong container."
echo "Can co PulseAudio/PipeWire socket hoac /dev/snd de phat audio truc tiep."
exit 1
