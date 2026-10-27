#!/usr/bin/env python3
"""Archival montage: cut shots from newsreel footage, crop 4:3 -> 16:9, upscale to 1080p, grade, join with short dissolves.

  clip.py spec.json out.mp4 <total_seconds>

spec = {"root": "<ussr dir>", "xf": 0.2,
        "shots": [{"src": "footage/mayday1961.mp4", "ss": 4.0, "w": 1.0, "y0": 60, "push": 0.06}, ...]}
 w     relative weight of the shot's on-screen time (total on-screen time is exactly <total_seconds>)
 y0    top of the 640x360 crop window inside the 640x480 frame (0..120, default 60 = centred)
 push  slow push-in, fraction of extra zoom over the shot (default 0.06)"""
import json, os, subprocess, sys

spec = json.load(open(sys.argv[1], encoding="utf-8")); out = sys.argv[2]; total = float(sys.argv[3])
ROOT = spec["root"]; XF = spec.get("xf", 0.2); shots = spec["shots"]; n = len(shots)
sw = sum(s.get("w", 1.0) for s in shots)
# with n shots and (n-1) overlaps of XF, visible time = sum(d_i) - (n-1)*XF  ->  d_i = (total + (n-1)*XF) * w_i / sw
durs = [(total + (n - 1) * XF) * s.get("w", 1.0) / sw for s in shots]

GRADE = ("eq=contrast=1.14:brightness=-0.02:gamma=0.95:saturation=0.0,"
         "curves=all='0/0 0.22/0.17 0.5/0.5 0.8/0.86 1/1',"
         "colorbalance=rs=.05:gs=.02:bs=-.07:rm=.05:gm=.02:bm=-.06:rh=.04:bh=-.05,"
         "unsharp=5:5:0.7:5:5:0.0,vignette=angle=PI/4.2,noise=alls=11:allf=t+u,format=yuv420p")

cmd = ["ffmpeg", "-y", "-loglevel", "error"]; fc = []
for i, (s, d) in enumerate(zip(shots, durs)):
    cmd += ["-ss", str(s["ss"]), "-t", f"{d + 0.05:.3f}", "-i", os.path.join(ROOT, s["src"]) if not os.path.isabs(s["src"]) else s["src"]]
    y0 = int(s.get("y0", 60)); push = s.get("push", 0.06)
    # crop 16:9 window, upscale with a slow push-in (scale grows with time, centre crop back to 1920x1080)
    fc.append(f"[{i}:v]fps=30,tpad=stop_mode=clone:stop_duration=8,crop=640:360:0:{y0},scale=1920:1080:flags=lanczos,"
              f"scale=w='1920*(1+{push}*t/{d:.3f})':h=-2:eval=frame:flags=bilinear,crop=1920:1080,setsar=1,"
              f"trim=duration={d:.3f},setpts=PTS-STARTPTS[v{i}]")
prev = "v0"; T = 0.0
for i in range(1, n):
    T += durs[i - 1] - XF; lab = f"x{i}"
    fc.append(f"[{prev}][v{i}]xfade=transition=fade:duration={XF}:offset={T:.3f}[{lab}]"); prev = lab
fc.append(f"[{prev}]{GRADE},trim=duration={total:.3f},setpts=PTS-STARTPTS[outv]")
cmd += ["-filter_complex", ";".join(fc), "-map", "[outv]", "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-r", "30", "-frames:v", str(round(total * 30)), out]
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode: sys.exit(f"clip.py failed:\n{r.stderr[-1200:]}")
print(f"wrote {out} ({total:.2f}s, {n} shots)")
