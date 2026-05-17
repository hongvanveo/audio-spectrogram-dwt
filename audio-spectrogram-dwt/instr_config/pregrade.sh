#!/bin/bash
: <<'END'
Pregrade script for the spectrogram-DWT image-in-audio lab.
It rebuilds grading state from the learner's current files so checkwork
reflects the actual task progress instead of stale markers.
END

homedir=$1
destdir=$2
dbg=/tmp/audio-spectrogram-dwt-pregrade.log

workdir="$homedir/$destdir/stego"
resultdir="$homedir/$destdir/.local/result"
result="$resultdir/spectrogram_dwt_check.txt"

mkdir -p "$resultdir"
: > "$result"
echo "pregrade for $homedir/$destdir" > "$dbg"

pass() { echo "PASS_$1" >> "$result"; }
fail() { echo "FAIL_$1: $2" >> "$result"; }

if [ -s "$workdir/cover.wav" ]; then
    pass "COVER_CREATED"
else
    fail "COVER_CREATED" "cover.wav missing"
fi

if [ -s "$workdir/secret.png" ]; then
    pass "SECRET_IMAGE_CREATED"
else
    fail "SECRET_IMAGE_CREATED" "secret.png missing"
fi

if grep -q "PASS_IMAGE_PROCESSED" "$result" 2>/dev/null || [ -s "$workdir/.istft_signal_created" ]; then
    pass "IMAGE_PROCESSED"
else
    fail "IMAGE_PROCESSED" "image processing not completed"
fi

if [ -s "$workdir/.istft_signal_created" ]; then
    pass "ISTFT_SIGNAL_CREATED"
else
    fail "ISTFT_SIGNAL_CREATED" "ISTFT signal marker missing"
fi

if [ -s "$workdir/.dwt_highfreq_embedded" ]; then
    pass "DWT_HIGHFREQ_EMBEDDED"
else
    fail "DWT_HIGHFREQ_EMBEDDED" "DWT high-frequency embedding marker missing"
fi

if [ -s "$workdir/stego.wav" ]; then
    pass "STEGO_CREATED"
else
    fail "STEGO_CREATED" "stego.wav missing"
fi

if [ -s "$workdir/.analysis_done" ]; then
    pass "AUDIO_MODIFIED"
else
    fail "AUDIO_MODIFIED" "analysis step not completed"
fi
