#!/usr/bin/env bash
rc=0
for f in analyze.sh alert.sh; do
  if [ -f "$f" ] && bash -n "$f" 2>/dev/null && grep -q 'set -euo pipefail' "$f"; then echo "- ✅ $f is valid bash with strict mode"
  else echo "- ❌ $f is missing, has a syntax error, or lacks 'set -euo pipefail'"; rc=1; fi
done
grep -qE '^ALL CHECKS PASSED \(' SUBMISSION.md && echo "- ✅ SUBMISSION.md shows ALL CHECKS PASSED" || { echo "- ❌ paste the verify.sh output ('ALL CHECKS PASSED') into SUBMISSION.md"; rc=1; }
exit $rc
