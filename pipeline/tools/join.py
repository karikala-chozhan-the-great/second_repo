#!/usr/bin/env python3
"""Join seg_*.wav from timings.json with a gap after each segment -> one WAV; also write start times."""
import json, sys, wave
d, out, gap = sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
T = json.load(open(f"{d}/timings.json")); frames = []; t = 0.0
for i, s in enumerate(T):
    with wave.open(s["file"]) as w:
        p = (w.getnchannels(), w.getsampwidth(), w.getframerate()); frames.append(w.readframes(w.getnframes()))
    s["start"] = round(t, 3); t += s["dur"] + (gap if i < len(T) - 1 else 0)
    if i < len(T) - 1: frames.append(b"\x00" * (int(gap * p[2]) * p[1] * p[0]))
with wave.open(out, "wb") as w:
    w.setnchannels(p[0]); w.setsampwidth(p[1]); w.setframerate(p[2]); w.writeframes(b"".join(frames))
json.dump(T, open(f"{d}/timings.json", "w"), ensure_ascii=False, indent=1)
print(f"{out}: {t:.1f}s")
