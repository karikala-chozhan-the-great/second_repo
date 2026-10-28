#!/usr/bin/env python3
"""Compose a video from a storyboard.   compose.py storyboard.json out.mp4 [--jobs 3]

storyboard = {"lang": "en", "audio": "path.wav", "fade": 0.5, "root": "<ussr dir>",
  "scenes": [ {"dur": 6.9,                       # seconds on screen (excluding the 0.5s crossfade tail)
               "type": "photo", "img": "images/x.jpg", "kb": {"z0":1,"z1":1.14,"px":0,"py":0,"fx":.5,"fy":.5},
               "overlay": {"stamp": {"l1","l2","t0","t1"}, "lower": {"name","role","t0","t1"}}},
              {"dur": 8, "type": "gfx", "html": "gfx/map.html", "data": {...}} , ... ] }
Each clip is rendered with `fade` extra seconds so neighbours can crossfade; clips are cached by content hash."""
import argparse, concurrent.futures as cf, hashlib, json, os, subprocess, sys

ap = argparse.ArgumentParser(); ap.add_argument("storyboard"); ap.add_argument("out"); ap.add_argument("--jobs", type=int, default=3)
ap.add_argument("--keep", action="store_true"); a = ap.parse_args()
SB = json.load(open(a.storyboard, encoding="utf-8")); ROOT = SB["root"]; FADE = SB.get("fade", 0.5); LANG = SB["lang"]
CACHE = os.path.join(ROOT, "build", "cache"); os.makedirs(CACHE, exist_ok=True)
P = lambda p: p if os.path.isabs(p) else os.path.join(ROOT, p)

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(f"FAILED: {' '.join(map(str, cmd))[:300]}\n{r.stderr[-800:]}")

def fkey(sc):
    h = hashlib.md5(json.dumps(sc, sort_keys=True, ensure_ascii=False).encode())
    for k in ("img", "html"):
        if k in sc:
            f = P(sc[k]); h.update(f"{os.path.getsize(f)}:{int(os.path.getmtime(f))}".encode())
    for shot in sc.get("montage", {}).get("shots", []):
        f = P(shot["src"]); h.update(f"{shot['src']}:{os.path.getsize(f)}".encode())
    for tool in ("tools/kb.py", "tools/clip.py", "gfx/render.js", "gfx/overlay.html", "gfx/common.css"):
        f = os.path.join(ROOT, tool); h.update(f"{tool}:{int(os.path.getmtime(f))}".encode())
    h.update(LANG.encode()); return h.hexdigest()[:16]

def render(i, sc, tail):
    length = sc["dur"] + tail
    out = os.path.join(CACHE, f"{fkey(dict(sc, _len=length))}.mp4")
    if os.path.exists(out): return out
    tmp = out + ".part.mp4"
    base = tmp if not sc.get("overlay") else out + ".base.mp4"
    if sc["type"] == "photo":
        kb = sc.get("kb", {}); cmd = [sys.executable, "-I", os.path.join(ROOT, "tools/kb.py"), P(sc["img"]), base, str(length)]
        for k in ("z0", "z1", "px", "py", "fx", "fy"):
            if k in kb: cmd += [f"--{k}", str(kb[k])]
        run(cmd)
    elif sc["type"] == "video":
        specf = out + ".spec.json"; json.dump(dict(sc["montage"], root=ROOT), open(specf, "w"))
        run([sys.executable, "-I", os.path.join(ROOT, "tools/clip.py"), specf, base, str(length)]); os.remove(specf)
    else:
        data = dict(sc.get("data", {}), lang=LANG, dur=length)
        if sc["type"] == "gfx" and "img" in sc: data["img"] = P(sc["img"])
        for k in ("flag",):
            if k in data: data[k] = P(data[k])
        run(["node", os.path.join(ROOT, "gfx/render.js"), os.path.join(ROOT, sc["html"]), base, str(length), "--data", json.dumps(data, ensure_ascii=False)])
    if sc.get("overlay"):
        mov = out + ".ov.mov"
        run(["node", os.path.join(ROOT, "gfx/render.js"), os.path.join(ROOT, "gfx/overlay.html"), mov, str(length), "--alpha", "--data",
             json.dumps(dict(sc["overlay"], lang=LANG), ensure_ascii=False)])
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", base, "-i", mov, "-filter_complex", "[0][1]overlay=format=auto,format=yuv420p",
             "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-r", "30", tmp])
        for f in (base, mov): os.remove(f)
    os.replace(tmp, out); return out

def xfade_join(items, out, fade):
    """items: [(path, d)] where each file lasts d+fade. Output lasts sum(d)+fade. Written atomically (.part -> rename)."""
    final = out; out = final + ".part.mp4"
    if len(items) == 1:
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", items[0][0], "-c", "copy", out]); os.replace(out, final); return
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]; fc = []
    for k, (p, d) in enumerate(items):
        cmd += ["-i", p]; fc.append(f"[{k}:v]settb=AVTB,fps=30,format=yuv420p[s{k}]")
    T = 0.0; prev = "s0"
    for k in range(1, len(items)):
        T += items[k - 1][1]
        lab = f"x{k}"; fc.append(f"[{prev}][s{k}]xfade=transition=fade:duration={fade}:offset={T:.3f}[{lab}]")
        prev = lab
    cmd += ["-filter_complex", ";".join(fc), "-map", f"[{prev}]", "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-r", "30", out]
    run(cmd); os.replace(out, final)

def maybe_join(j):
    grp, o = j
    if os.path.exists(o):
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", o], capture_output=True, text=True)
        try: ok = float(r.stdout) > 0 and os.path.getmtime(o) >= max(os.path.getmtime(p) for p, _ in grp)
        except ValueError: ok = False
        if ok: print(f"  reuse {os.path.basename(o)}", flush=True); return
    xfade_join(grp, o, FADE)

scenes = SB["scenes"]; n = len(scenes)
print(f"rendering {n} scenes ({a.jobs} parallel)...", flush=True)
with cf.ThreadPoolExecutor(a.jobs) as ex:
    futs = [ex.submit(render, i, sc, FADE) for i, sc in enumerate(scenes)]
    clips = []
    for i, f in enumerate(futs):
        clips.append(f.result()); print(f"  scene {i+1}/{n} ok", flush=True)

# xfade offsets: transition k starts when clip k-1's own duration (d) has played, i.e. fade overlaps the tail
GROUP = 8; level = [(c, sc["dur"]) for c, sc in zip(clips, scenes)]; tmpdir = os.path.join(ROOT, "build", "tmp_join"); os.makedirs(tmpdir, exist_ok=True); lv = 0
while len(level) > 1:
    jobs = []
    for gi in range(0, len(level), GROUP):
        grp = level[gi:gi + GROUP]; jobs.append((grp, os.path.join(tmpdir, f"{LANG}_L{lv}_{gi}.mp4")))
    with cf.ThreadPoolExecutor(3) as ex2:
        list(ex2.map(maybe_join, jobs))
    level = [(o, sum(d for _, d in grp)) for grp, o in jobs]; lv += 1
    print(f"  joined level {lv} ({len(level)} clips)", flush=True)
video, vdur = level[0]; total = sum(sc["dur"] for sc in scenes) + FADE   # last clip keeps its fade tail
fo = max(0, total - 0.8)
run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", P(SB["audio"]),
     "-filter_complex", f"[0:v]fade=t=in:st=0:d=0.6,fade=t=out:st={fo:.2f}:d=0.8[v];[1:a]{"" if SB.get("premixed") else "loudnorm=I=-16:TP=-1.5:LRA=11,"}aresample=48000,adelay={int(FADE*1000)}|{int(FADE*1000)},apad[a]",
     "-map", "[v]", "-map", "[a]", "-t", f"{total:.3f}", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
     "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", a.out])
print(f"wrote {a.out} ({total:.1f}s)")
