#!/usr/bin/env python3
"""sheet.py video.mp4 out.png [step=4] [start=0] [end=] -> contact sheet with timestamps"""
import subprocess, sys, os, tempfile, glob
from PIL import Image, ImageDraw
v, out = sys.argv[1], sys.argv[2]; step = float(sys.argv[3]) if len(sys.argv) > 3 else 4; t0 = float(sys.argv[4]) if len(sys.argv) > 4 else 0
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", v], capture_output=True, text=True).stdout)
t1 = float(sys.argv[5]) if len(sys.argv) > 5 else dur
ts = []; t = t0
while t < t1: ts.append(t); t += step
W, H, cols = 320, 240, 5; rows = (len(ts) + cols - 1) // cols; sh = Image.new("RGB", (W * cols, H * rows), (15, 15, 15))
with tempfile.TemporaryDirectory() as d:
    for i, t in enumerate(ts):
        p = os.path.join(d, f"{i}.png"); subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(t), "-i", v, "-frames:v", "1", "-vf", f"scale={W}:{H}", p])
        if os.path.exists(p):
            sh.paste(Image.open(p), ((i % cols) * W, (i // cols) * H)); dr = ImageDraw.Draw(sh)
            dr.rectangle([(i % cols) * W, (i // cols) * H, (i % cols) * W + 62, (i // cols) * H + 16], fill=(0, 0, 0)); dr.text(((i % cols) * W + 4, (i // cols) * H + 2), f"{t:.0f}s", fill=(255, 255, 0))
sh.save(out); print(out, len(ts), "frames")
