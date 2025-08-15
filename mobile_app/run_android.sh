#!/usr/bin/env bash
# Run FindTheGap AR prototype on an attached Android device.
#
# Usage:
#   ./run_android.sh [DEVICE_ID]
# If DEVICE_ID is omitted, the first available Android device is used.
# The script resolves dependencies and launches the app with verbose logging.

set -euo pipefail
cd "$(dirname "$0")"

flutter pub get

DEVICE_ID=${1:-}
if [[ -n "$DEVICE_ID" ]]; then
  flutter run -d "$DEVICE_ID" --verbose
else
  flutter run -d android --verbose
fi
