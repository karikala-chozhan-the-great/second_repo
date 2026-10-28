# -*- coding: utf-8 -*-
"""Quality checks for a finished video.   qa.py en|ta   -> prints a report, writes build/qa_<lang>/sheet_{1,2,3}.png (a frame every 20 s)"""
import json, os, re, subprocess, sys
from PIL import Image, ImageDraw
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); lang = sys.argv[1]; V = f"{R}/out/{lang}_full.mp4"; O = f"{R}/build/qa_{lang}"; os.makedirs(O, exist_ok=True)
sb = json.load(open(f"{R}/build/sb_full_{lang}.json", encoding="utf-8")); expect = sum(s["dur"] for s in sb["scenes"]) + 0.5
def sh(cmd): return subprocess.run(cmd, capture_output=True, text=True)
pr = json.loads(sh(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels,duration", "-show_entries", "format=duration,size,bit_rate", "-of", "json", V]).stdout)
v = next(s for s in pr["streams"] if s["codec_type"] == "video"); a = next(s for s in pr["streams"] if s["codec_type"] == "audio"); dur = float(pr["format"]["duration"])
print(f"[{lang}] video {v['codec_name']} {v['width']}x{v['height']} {v['r_frame_rate']} | audio {a['codec_name']} {a['sample_rate']} Hz x{a['channels']} | duration {dur:.2f}s (expected {expect:.2f}s, diff {dur-expect:+.2f}s) | size {int(pr['format']['size'])/1e6:.0f} MB | {int(pr['format']['bit_rate'])/1e6:.1f} Mbps")
ok = v["width"] == 1920 and v["height"] == 1080 and abs(dur - expect) < 1.0
r = sh(["ffmpeg", "-hide_banner", "-nostats", "-i", V, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
summ = r[r.rfind("Summary:"):]; I = re.search(r"I:\s+(-?[\d.]+) LUFS", summ); LRA = re.search(r"LRA:\s+([\d.]+) LU", summ); PK = re.search(r"Peak:\s+(-?[\d.]+) dBFS", summ)
print(f"loudness: {I.group(1)} LUFS integrated | LRA {LRA.group(1)} LU | true peak {PK.group(1)} dBFS   (target about -16 LUFS, peak below -1)")
ok = ok and I and -18 < float(I.group(1)) < -14 and PK and float(PK.group(1)) <= -0.5
r = sh(["ffmpeg", "-hide_banner", "-nostats", "-i", V, "-vn", "-af", "silencedetect=noise=-50dB:d=3", "-f", "null", "-"]).stderr
sil = re.findall(r"silence_start: ([\d.]+)|silence_end: ([\d.]+) \| silence_duration: ([\d.]+)", r)
print("silences over 3 s (-50 dB):", [(round(float(a or 0), 1), round(float(c), 1)) for a, b, c in sil if c] or "none")
r = sh(["ffmpeg", "-hide_banner", "-nostats", "-i", V, "-an", "-vf", "blackdetect=d=0.4:pix_th=0.06", "-f", "null", "-"]).stderr
blk = re.findall(r"black_start:([\d.]+) black_end:([\d.]+) black_duration:([\d.]+)", r)
print("black frames over 0.4 s:", [(float(a), float(c)) for a, b, c in blk] or "none")
# contact sheets: a frame every 20 s, 15 per sheet (3 columns x 5 rows of 640x360)
ts = [t for t in range(2, int(dur), 20)]
for k in range(0, len(ts), 15):
    chunk = ts[k:k + 15]; sheet = Image.new("RGB", (640 * 3, 360 * ((len(chunk) + 2) // 3)), (20, 20, 20))
    for i, t in enumerate(chunk):
        f = f"{O}/f_{t:04d}.png"; sh(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(t), "-i", V, "-frames:v", "1", "-vf", "scale=640:360", f])
        im = Image.open(f); sheet.paste(im, ((i % 3) * 640, (i // 3) * 360)); d = ImageDraw.Draw(sheet)
        d.rectangle([(i % 3) * 640, (i // 3) * 360, (i % 3) * 640 + 70, (i // 3) * 360 + 18], fill=(0, 0, 0)); d.text(((i % 3) * 640 + 4, (i // 3) * 360 + 3), f"{t//60}:{t%60:02d}", fill=(255, 255, 0))
    sheet.save(f"{O}/sheet_{k // 15 + 1}.png")
print(f"contact sheets: {O}/sheet_1.png .. sheet_{(len(ts) + 14) // 15}.png   | basic checks {'PASS' if ok else 'NEED ATTENTION'}")
