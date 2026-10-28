# -*- coding: utf-8 -*-
"""Caption file from the narration script and timings (video time = joined-audio start + the 0.5 s audio delay).   srt.py en|ta"""
import json, os, re, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); lang = sys.argv[1]
T = json.load(open(f"{R}/audio/{lang}_full/timings.json", encoding="utf-8"))
MAXC, LINEC = (84, 42) if lang == "en" else (68, 34)
def ts(t): ms = int(round(t * 1000)); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
def wrap(s):
    if len(s) <= LINEC: return s
    mid = len(s) // 2; best = min((i for i, c in enumerate(s) if c == " "), key=lambda i: abs(i - mid), default=None)
    return s if best is None else s[:best] + "\n" + s[best + 1:]
def chunks(text):
    sents = [x.strip() for x in re.split(r"(?<=[.!?;:])\s+", text) if x.strip()]; out, cur = [], ""
    for s in sents:
        while len(s) > MAXC:                                   # very long sentence: cut at a space near the limit
            cut = s.rfind(" ", 0, MAXC); cut = cut if cut > 20 else MAXC
            if cur: out.append(cur); cur = ""
            out.append(s[:cut].strip()); s = s[cut:].strip()
        if cur and len(cur) + 1 + len(s) > MAXC: out.append(cur); cur = s
        else: cur = (cur + " " + s).strip()
    if cur: out.append(cur)
    return out
lines, n = [], 0
for t in T:
    t0 = t["start"] + 0.5; ch = chunks(t["text"]); tot = sum(len(c) for c in ch); cur = t0
    for c in ch:
        d = t["dur"] * len(c) / tot; n += 1
        lines.append(f"{n}\n{ts(cur)} --> {ts(cur + d - 0.05)}\n{wrap(c)}\n"); cur += d
os.makedirs(f"{R}/out/{lang}", exist_ok=True)
open(f"{R}/out/{lang}/captions_{lang}.srt", "w", encoding="utf-8").write("\n".join(lines))
print(lang, n, "captions; last ends", ts(T[-1]["start"] + 0.5 + T[-1]["dur"]))
