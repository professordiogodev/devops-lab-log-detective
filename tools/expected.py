#!/usr/bin/env python3
"""Computes the expected analyze.sh output independently. usage: expected.py LOGFILE"""
import re, sys, collections
line_re = re.compile(r'^(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) (\S+) [^"]*" (\d{3}) (\d+) "[^"]*" "[^"]*" ([\d.]+)$')
total = 0; classes = collections.Counter(); ips = collections.Counter(); paths5 = collections.Counter(); minutes5 = collections.Counter()
for l in open(sys.argv[1]):
    m = line_re.match(l.rstrip("\n"))
    if not m: continue
    ip, ts, meth, path, st, size, rt = m.groups(); total += 1
    classes[st[0] + "xx"] += 1; ips[ip] += 1
    if st[0] == "5":
        paths5[path] += 1; minutes5[ts[12:17]] += 1
def top(c, n):
    # descending by count, ties alphabetical, so output is deterministic
    return sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:n]
print(f"TOTAL {total}")
for c in ("2xx", "3xx", "4xx", "5xx"): print(f"STATUS {c} {classes.get(c, 0)}")
print("TOP_IPS")
for ip, n in top(ips, 5): print(f"{n} {ip}")
print("TOP_5XX_PATHS")
for p, n in top(paths5, 5): print(f"{n} {p}")
pm = top(minutes5, 1)
print("PEAK_5XX_MINUTE " + (f"{pm[0][0]} {pm[0][1]}" if pm else "none 0"))
