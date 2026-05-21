#!/bin/bash
set -e
cd "$(dirname "$0")"
if [ ! -s secret.png ]; then
    echo "secret.png chua ton tai."
    exit 1
fi
printf 'opened\n' > .secret_image_viewed
python3 refresh_status.py >/dev/null 2>&1 || true
exec feh --auto-zoom secret.png
