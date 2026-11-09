#!/usr/bin/env bash
# Generates the incident log in ./data/access.log (re-run to regenerate; same content every time).
set -euo pipefail
cd "$(dirname "$0")"
command -v python3 >/dev/null || { echo "python3 is required (sudo apt install python3)"; exit 1; }
mkdir -p data
python3 tools/gen_log.py data/access.log 20261110 42000 story
echo "Wrote data/access.log: $(wc -l < data/access.log) lines, $(du -h data/access.log | cut -f1)"
echo "First lines:"; head -3 data/access.log
echo
echo "Format: ip - - [time] \"METHOD path HTTP/1.1\" status bytes \"-\" \"user-agent\" request_seconds"
