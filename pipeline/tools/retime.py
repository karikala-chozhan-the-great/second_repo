#!/usr/bin/env python3
"""Rebuild timings.json from the seg_NN.wav files that are on disk (so swapped/regenerated segments are picked up).
  retime.py <audiodir> <script.txt>"""
import json, os, sys, wave
d, script = sys.argv[1], sys.argv[2]
segs = [p.strip() for p in open(script, encoding="utf-8").read().split("\n\n") if p.strip()]
T = []
for i, text in enumerate(segs, 1):
    f = os.path.join(d, f"seg_{i:02d}.wav")
    with wave.open(f) as w: dur = w.getnframes() / w.getframerate()
    T.append({"seg": i, "file": f, "dur": round(dur, 3), "text": text})
json.dump(T, open(os.path.join(d, "timings.json"), "w"), ensure_ascii=False, indent=1)
print(f"{d}: {len(T)} segments, narration {sum(t['dur'] for t in T):.1f}s")
