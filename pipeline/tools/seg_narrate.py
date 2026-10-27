#!/usr/bin/env python3
"""Narrate each blank-line-separated segment separately with the plugin's synth(); write
seg_NN.wav files plus timings.json (duration of each segment) so visuals can be synced."""
import argparse, io, json, os, sys, wave
sys.path.insert(0, os.path.dirname(__file__))
import narrate

ap = argparse.ArgumentParser()
ap.add_argument("script"); ap.add_argument("outdir")
ap.add_argument("--model", default="gemini-3.8-flash-tts")
ap.add_argument("--voice", default="Alnilam")
ap.add_argument("--style", required=True)
ap.add_argument("--only", help="comma list of segment numbers to (re)generate")
a = ap.parse_args()
key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("key")
if not key: sys.exit("no key in env")
os.makedirs(a.outdir, exist_ok=True)
segs = [p.strip() for p in open(a.script, encoding="utf-8").read().split("\n\n") if p.strip()]
only = {int(x) for x in a.only.split(",")} if a.only else None
timings = []
for i, text in enumerate(segs, 1):
    path = os.path.join(a.outdir, f"seg_{i:02d}.wav")
    if only is None or i in only or not os.path.exists(path):
        parts = []
        for c in narrate.chunk_text(text, 1200):
            raw = narrate.synth(key, a.model, c, a.voice, a.style)
            with wave.open(io.BytesIO(raw)) as w:
                params = (w.getnchannels(), w.getsampwidth(), w.getframerate()); parts.append(w.readframes(w.getnframes()))
        gap = b"\x00" * (int(0.25 * params[2]) * params[1] * params[0])
        pcm = gap.join(parts)
        with wave.open(path, "wb") as w:
            w.setnchannels(params[0]); w.setsampwidth(params[1]); w.setframerate(params[2]); w.writeframes(pcm)
    with wave.open(path) as w:
        dur = w.getnframes() / w.getframerate()
    timings.append({"seg": i, "file": path, "dur": round(dur, 3), "text": text})
    print(f"seg {i}: {dur:.1f}s", file=sys.stderr)
json.dump(timings, open(os.path.join(a.outdir, "timings.json"), "w"), ensure_ascii=False, indent=1)
print(f"total {sum(t['dur'] for t in timings):.1f}s", file=sys.stderr)
