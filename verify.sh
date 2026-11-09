#!/usr/bin/env bash
# Run with: ./verify.sh
set -uo pipefail
cd "$(dirname "$0")"
[ -f data/access.log ] || { echo "Run ./setup.sh first"; exit 1; }
pass=0; failn=0
check() { local d="$1"; shift; if "$@" >/dev/null 2>&1; then echo "PASS  $d"; pass=$((pass+1)); else echo "FAIL  $d"; failn=$((failn+1)); fi; }
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
python3 tools/gen_log.py "$tmp/other.log" 777 6000 story
python3 tools/gen_log.py "$tmp/quiet.log" 5 800

same() { # log
  diff <(python3 tools/expected.py "$1") <(./analyze.sh "$1" 2>/dev/null | sed 's/[[:space:]]*$//')
}

echo "== analyze.sh =="
check "analyze.sh exists and is executable"                      test -x analyze.sh
check "analyze.sh uses strict mode"                              grep -q 'set -euo pipefail' analyze.sh
check "output matches exactly on the incident log"               same data/access.log
check "output matches exactly on a different log (no hard-coding)" same "$tmp/other.log"
check "works on a log with no server errors at all"              bash -c "diff <(python3 tools/expected.py '$tmp/quiet.log') <(./analyze.sh '$tmp/quiet.log' 2>/dev/null)"
check "a missing file gives exit code 2 and a message"           bash -c "./analyze.sh /nonexistent >/dev/null 2>&1; [ \$? = 2 ]"
check "no argument gives a usage message and exit code 2"        bash -c "./analyze.sh >/dev/null 2>&1; [ \$? = 2 ]"

echo "== alert.sh =="
check "alert.sh exists and is executable"                        test -x alert.sh
check "2.3% errors with threshold 1% -> ALERT, exit 1"           bash -c "out=\$(./alert.sh data/access.log 1 2>&1); [ \$? = 1 ] && grep -qi alert <<< \"\$out\""
check "2.3% errors with threshold 5% -> OK, exit 0"              bash -c "out=\$(./alert.sh data/access.log 5 2>&1); [ \$? = 0 ] && ! grep -qi alert <<< \"\$out\""
check "quiet log with threshold 0.5% -> OK"                      bash -c "./alert.sh '$tmp/quiet.log' 0.5 >/dev/null 2>&1"
check "no arguments: usage and exit code 2"                      bash -c "./alert.sh >/dev/null 2>&1; [ \$? = 2 ]"

echo
if [ "$failn" -eq 0 ]; then echo "ALL CHECKS PASSED ($pass/$pass)"; else echo "$failn check(s) failed, $pass passed"; fi
exit "$failn"
