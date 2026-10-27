#!/usr/bin/env python3
"""Mix narration with a quiet, ducked music bed.
  mix.py narration.wav out.wav track1.mp3 [track2.mp3 ...] [--music-lufs -33] [--duck 8]
Narration -> -16 LUFS; music tracks crossfaded (6 s), leveled to --music-lufs, faded in/out, and ducked under speech."""
import argparse, subprocess, sys
ap = argparse.ArgumentParser(); ap.add_argument("narration"); ap.add_argument("out"); ap.add_argument("tracks", nargs="+")
ap.add_argument("--music-lufs", type=float, default=-33.0); ap.add_argument("--tail", type=float, default=6.0, help="extra seconds after narration"); a = ap.parse_args()
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.narration], capture_output=True, text=True).stdout)
total = dur + a.tail
# take tracks until they cover the length (6 s crossfades eat time)
use, have = [], 0.0
for t in a.tracks:
    l = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", t], capture_output=True, text=True).stdout)
    use.append((t, l)); have += l - (6 if use[1:] else 0)
    if have >= total: break
if have < total: sys.exit(f"tracks cover only {have:.0f}s of {total:.0f}s")
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", a.narration]
for t, _ in use: cmd += ["-i", t]
fc = ["[0:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,asplit=2[nar][sc]"]
prev = "1:a"
for k in range(2, len(use) + 1):
    fc.append(f"[{prev}][{k}:a]acrossfade=d=6:c1=tri:c2=tri[m{k}]"); prev = f"m{k}"
fc.append(f"[{prev}]aresample=48000,loudnorm=I={a.music_lufs}:TP=-6:LRA=7,atrim=0:{total:.2f},afade=t=in:st=0:d=3,afade=t=out:st={total-5:.2f}:d=5[mus]")
fc.append("[mus][sc]sidechaincompress=threshold=0.02:ratio=6:attack=30:release=600:makeup=1[duck]")
fc.append("[nar][duck]amix=inputs=2:normalize=0:duration=longest,alimiter=limit=0.95[out]")
cmd += ["-filter_complex", ";".join(fc), "-map", "[out]", "-ar", "48000", "-ac", "1", a.out]
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode: sys.exit(r.stderr[-1500:])
print(f"wrote {a.out} ({total:.0f}s) using {[t.split('/')[-1] for t,_ in use]}")
