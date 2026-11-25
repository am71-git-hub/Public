#!/bin/bash
# Usage: ./play.sh [laptop|numpad]
# Starts NetHack with one of the configs in this folder.
# Defaults to laptop (vi keys, number_pad:0) if no argument given.

LAYOUT=${1:-laptop}
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RC="$HERE/nethackrc-$LAYOUT"

if [[ ! -f "$RC" ]]; then
  echo "Unknown layout: $LAYOUT  (choices: laptop, numpad)"
  exit 1
fi

# Debian/Ubuntu install the terminal version as nethack-console; elsewhere it's nethack.
NH=$(command -v nethack-console || command -v nethack)
NETHACKOPTIONS="@$RC" exec "$NH"
