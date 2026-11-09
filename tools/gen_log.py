#!/usr/bin/env python3
"""Generate a Clipstr access log.  usage: gen_log.py OUTFILE SEED COUNT [story]
Combined log format plus request time in seconds at the end."""
import random, sys, datetime

out, seed, count = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
story = len(sys.argv) > 4 and sys.argv[4] == "story"
r = random.Random(seed)
day = datetime.datetime(2026, 11, 10, 0, 0, 0)
UA = ["Mozilla/5.0 (X11; Linux x86_64) Firefox/126.0", "Mozilla/5.0 (Macintosh) Safari/605.1", "Mozilla/5.0 (Windows NT 10.0) Chrome/125.0", "curl/8.5.0", "Mozilla/5.0 (iPhone) Mobile Safari/604.1"]
codes = ["a1b2c3", "d4e5f6", "g7h8i9", "j0k1l2", "m3n4o5", "p6q7r8", "s9t0u1", "v2w3x4"]
ips = [f"192.0.2.{i}" for i in range(1, 120)] + [f"10.20.{r.randint(0,9)}.{r.randint(1,250)}" for _ in range(80)]

def hour_weight(h):  # busy afternoons, quiet nights
    return [1,1,1,1,1,2,3,5,8,10,11,12,12,12,12,11,10,9,8,6,4,3,2,1][h]

lines = []
def add(ts, ip, method, path, status, size, ua, rt):
    t = ts.strftime("%d/%b/%Y:%H:%M:%S +0000")
    lines.append((ts, f'{ip} - - [{t}] "{method} {path} HTTP/1.1" {status} {size} "-" "{ua}" {rt:.3f}'))

total_w = sum(hour_weight(h) for h in range(24))
for _ in range(count):
    h = r.choices(range(24), weights=[hour_weight(x) for x in range(24)])[0]
    ts = day + datetime.timedelta(hours=h, minutes=r.randint(0, 59), seconds=r.randint(0, 59))
    ip = r.choice(ips); ua = r.choice(UA)
    x = r.random()
    if x < 0.55:   add(ts, ip, "GET", f"/r/{r.choice(codes)}{r.randint(0,99)}", r.choices([302, 404], [0.93, 0.07])[0], r.randint(0, 300), ua, r.uniform(0.005, 0.08))
    elif x < 0.78: add(ts, ip, "POST", "/shorten", r.choices([201, 400, 200], [0.9, 0.08, 0.02])[0], r.randint(80, 200), ua, r.uniform(0.02, 0.2))
    elif x < 0.90: add(ts, ip, "GET", "/stats", 200, r.randint(300, 900), ua, r.uniform(0.02, 0.15))
    elif x < 0.96: add(ts, ip, "GET", "/healthz", 200, 60, "kube-probe/1.30", r.uniform(0.001, 0.01))
    else:          add(ts, ip, "GET", "/", 200, 1200, ua, r.uniform(0.01, 0.1))

if story:
    # 1. the outage: /shorten fails with 502 for seven minutes at 03:12
    start = day + datetime.timedelta(hours=3, minutes=12)
    for i in range(1400):
        ts = start + datetime.timedelta(seconds=r.randint(0, 7 * 60 - 1))
        path = r.choices(["/shorten", "/r/a1b2c312", "/stats"], [0.8, 0.12, 0.08])[0]
        bad = path == "/shorten"
        add(ts, r.choice(ips), "POST" if bad else "GET", path, 502 if bad else 200, 0 if bad else 400, r.choice(UA), r.uniform(29, 30.2) if bad else r.uniform(0.03, 0.1))
    # 2. the scraper
    for i in range(3500):
        ts = day + datetime.timedelta(hours=r.randint(9, 11), minutes=r.randint(0, 59), seconds=r.randint(0, 59))
        add(ts, "198.51.100.77", "GET", f"/r/{r.choice(codes)}{r.randint(0,999)}", r.choices([302, 404], [0.4, 0.6])[0], r.randint(0, 100), "python-requests/2.31", r.uniform(0.004, 0.02))
    # 3. the password guesser
    for i in range(600):
        ts = day + datetime.timedelta(hours=22, minutes=r.randint(0, 9), seconds=r.randint(0, 59))
        add(ts, "203.0.113.9", "POST", "/admin/login", 401, 40, "Mozilla/5.0 (compatible; hydra)", r.uniform(0.2, 0.4))
    # 4. a slow period on /stats
    for i in range(120):
        ts = day + datetime.timedelta(hours=14, minutes=r.randint(0, 9), seconds=r.randint(0, 59))
        add(ts, r.choice(ips), "GET", "/stats", 200, 800, r.choice(UA), r.uniform(4, 9))

lines.sort(key=lambda x: x[0])
with open(out, "w") as f:
    f.write("\n".join(l for _, l in lines) + "\n")
