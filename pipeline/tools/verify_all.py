#!/usr/bin/env python3
"""Run verify.py on every segment (4 in parallel) and print a table.  verify_all.py en|ta"""
import json, re, subprocess, sys, tempfile, os, concurrent.futures as cf
lang = sys.argv[1]; R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(f"{R}/audio/{lang}_full/timings.json", encoding="utf-8"))
def one(t):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f: f.write(t["text"]); fn = f.name
    r = subprocess.run([sys.executable, "-I", f"{R}/tools/verify.py", t["file"], fn, "--lang", lang], capture_output=True, text=True); os.unlink(fn)
    m = re.search(r"Character error rate: ([\d.]+)%", r.stdout)
    return t["seg"], (float(m.group(1)) if m else None), "\n".join(l for l in r.stdout.splitlines() if l.strip().startswith("script:"))[:400]
with cf.ThreadPoolExecutor(4) as ex: res = sorted(ex.map(one, T))
bad = [r for r in res if r[1] is None or r[1] > 3.0]
print(f"{lang}: mean CER {sum(r[1] for r in res if r[1] is not None)/len(res):.2f}%   max {max(r[1] for r in res if r[1] is not None):.1f}%   over 3%: {[r[0] for r in bad]}")
for seg, c, d in res:
    if c is None or c > 2.0: print(f"  seg {seg}: {c}%\n{d}")
json.dump(res, open(f"{R}/build/verify_{lang}.json", "w"))
