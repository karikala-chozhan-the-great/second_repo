#!/usr/bin/env python3
"""Ken Burns photo clip with ffmpeg: kb.py img out.mp4 dur [--z0 1.0 --z1 1.15 --px 0 --py 0]
px,py = total pan over the clip as a fraction of the image (+x moves the view right)."""
import argparse, subprocess, sys
ap = argparse.ArgumentParser(); ap.add_argument("img"); ap.add_argument("out"); ap.add_argument("dur", type=float)
ap.add_argument("--z0", type=float, default=1.0); ap.add_argument("--z1", type=float, default=1.14)
ap.add_argument("--px", type=float, default=0.0); ap.add_argument("--py", type=float, default=0.0)
ap.add_argument("--up", type=int, default=2880, help="zoompan working width"); ap.add_argument("--fx", type=float, default=0.5, help="focus x 0-1 at start"); ap.add_argument("--fy", type=float, default=0.5)
a = ap.parse_args()
N = max(2, round(a.dur * 30)); p = f"(on/{N-1})"; s = f"({p}*{p}*(3-2*{p}))"  # smoothstep
z = f"{a.z0}+({a.z1}-{a.z0})*{s}"
# view centre moves from (fx,fy) by (px,py); clamp so the crop stays inside the image
cx = f"iw*({a.fx}+{a.px}*{s})"; cy = f"ih*({a.fy}+{a.py}*{s})"
x = f"max(0,min(iw-iw/zoom,{cx}-iw/zoom/2))"; y = f"max(0,min(ih-ih/zoom,{cy}-ih/zoom/2))"
vf = (f"scale={a.up}:{a.up*9//16}:force_original_aspect_ratio=increase:flags=bicubic,crop={a.up}:{a.up*9//16},"
      f"zoompan=z='{z}':x='{x}':y='{y}':d={N}:s=1920x1080:fps=30,"
      "eq=contrast=1.06:saturation=0.88:gamma=0.97,vignette=angle=PI/4.5,format=yuv420p")
r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", a.img, "-vf", vf, "-frames:v", str(N),
                    "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-r", "30", a.out])
sys.exit(r.returncode)
