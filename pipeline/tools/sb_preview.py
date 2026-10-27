#!/usr/bin/env python3
"""Build the 1-minute preview storyboard for a language from audio/<lang>_prev/timings.json.
  sb_preview.py en|ta [--allow-missing]   -> build/sb_preview_<lang>.json"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lang = sys.argv[1]; allow = "--allow-missing" in sys.argv
T = json.load(open(f"{ROOT}/audio/{lang}_prev/timings.json", encoding="utf-8")); GAP = 0.5
seg_len = {t["seg"]: t["dur"] + GAP for t in T}; seg_len[T[-1]["seg"]] = T[-1]["dur"] + GAP  # last segment also gets a tail

TX = {
 "en": dict(
  stamp_flag=("Moscow", "25 December 1991"), chip="Archival footage", date=("25 December 1991", "Moscow"), stats=[("time zones", 11, "", ""), ("republics", 15, "", ""), ("people (approx.)", 290, "", " million")],
  cap="Soviet republics", brk="1990 – 1991: the breakaway",
  countries={"Lithuania": "Lithuania", "Georgia": "Georgia", "Estonia": "Estonia", "Latvia": "Latvia", "Ukraine": "Ukraine", "Belarus": "Belarus",
             "Moldova": "Moldova", "Azerbaijan": "Azerbaijan", "Uzbekistan": "Uzbekistan", "Kyrgyzstan": "Kyrgyzstan", "Tajikistan": "Tajikistan",
             "Armenia": "Armenia", "Turkmenistan": "Turkmenistan", "Kazakhstan": "Kazakhstan"},
  months={"Mar": "March 1990", "Apr": "April 1991", "Aug": "August 1991", "Sep": "September 1991", "Oct": "October 1991", "Dec": "December 1991"},
  berlin=("Berlin", "1962"), afghan_cap="Soviet–Afghan war", afghan_t=("Afghanistan", "1979 – 1989"), kabul="Kabul",
  brezhnev=("Leonid Brezhnev", "General Secretary, 1964–1982"), afghan=("Afghanistan", "1979–1989"), cher=("Chernobyl", "26 April 1986"),
  gorb=("Mikhail Gorbachev", "General Secretary, 1985–1991"), title="The Fall of the Soviet Union", sub="1922 – 1991"),
 "ta": dict(
  stamp_flag=("மாஸ்கோ", "25 டிசம்பர் 1991"), chip="ஆவணக் காட்சிகள்", date=("25 டிசம்பர் 1991", "மாஸ்கோ"), stats=[("நேர மண்டலங்கள்", 11, "", ""), ("குடியரசுகள்", 15, "", ""), ("மக்கள் (கிட்டத்தட்ட)", 29, "", " கோடி")],
  cap="சோவியத் குடியரசுகள்", brk="1990 – 1991: பிரிந்து சென்ற குடியரசுகள்",
  countries={"Lithuania": "லிதுவேனியா", "Georgia": "ஜார்ஜியா", "Estonia": "எஸ்தோனியா", "Latvia": "லாத்வியா", "Ukraine": "உக்ரைன்", "Belarus": "பெலாரஸ்",
             "Moldova": "மால்டோவா", "Azerbaijan": "அசர்பைஜான்", "Uzbekistan": "உஸ்பெகிஸ்தான்", "Kyrgyzstan": "கிர்கிஸ்தான்", "Tajikistan": "தஜிகிஸ்தான்",
             "Armenia": "ஆர்மீனியா", "Turkmenistan": "துர்க்மெனிஸ்தான்", "Kazakhstan": "கஜகஸ்தான்"},
  months={"Mar": "மார்ச் 1990", "Apr": "ஏப்ரல் 1991", "Aug": "ஆகஸ்ட் 1991", "Sep": "செப்டம்பர் 1991", "Oct": "அக்டோபர் 1991", "Dec": "டிசம்பர் 1991"},
  berlin=("பெர்லின்", "1962"), afghan_cap="சோவியத்–ஆப்கான் போர்", afghan_t=("ஆப்கானிஸ்தான்", "1979 – 1989"), kabul="காபூல்",
  brezhnev=("லியோனிட் பிரெஷ்நேவ்", "பொதுச் செயலாளர், 1964–1982"), afghan=("ஆப்கானிஸ்தான்", "1979–1989"), cher=("செர்னோபில்", "26 ஏப்ரல் 1986"),
  gorb=("மிகைல் கோர்பச்சேவ்", "பொதுச் செயலாளர், 1985–1991"), title="சோவியத் ஒன்றியத்தின் வீழ்ச்சி", sub="1922 – 1991"),
}[lang]

ORDER = [("Lithuania", "Mar", "#3b82c4"), ("Georgia", "Apr", "#e07a1f"), ("Estonia", "Aug", "#2fa38a"), ("Latvia", "Aug", "#8a4fbf"), ("Ukraine", "Aug", "#e3c23a"),
         ("Belarus", "Aug", "#4fa34f"), ("Moldova", "Aug", "#c45a8c"), ("Azerbaijan", "Aug", "#2c8fa6"), ("Uzbekistan", "Aug", "#b5651d"), ("Kyrgyzstan", "Aug", "#d24d57"),
         ("Tajikistan", "Sep", "#6b8e23"), ("Armenia", "Sep", "#e9967a"), ("Turkmenistan", "Oct", "#20b2aa"), ("Kazakhstan", "Dec", "#5b6fd6")]
order = [{"k": k, "label": TX["countries"][k], "date": TX["months"][m], "col": c} for k, m, c in ORDER] + [{"k": "Russia", "label": "", "date": "", "col": "#c8102e", "stay": True}]

def img(name):
    for ext in (".jpg", ".png"):
        if os.path.exists(f"{ROOT}/images/{name}{ext}"): return f"images/{name}{ext}"
    if allow: print("  (missing", name, "-> placeholder)", file=sys.stderr); return "images/gorbachev_1987.jpg"
    sys.exit(f"missing image: {name}")

S = []
L = seg_len
# seg 1: date card as the narrator gives the date, then archival Red Square / Kremlin footage as "the red flag came down"
fr = 0.55 if lang == "en" else 0.5
d_card = L[1] * fr; d_foot = L[1] - d_card
A = {"src": "footage/mayday1961.mp4", "ss": 4.2, "w": 1.0, "y0": 40, "push": 0.07}      # wide Red Square, Lenin Mausoleum
B = {"src": "footage/moscow1965.mp4", "ss": 15.5, "w": 1.0, "y0": 60, "push": 0.06}     # marching column with flag
C = {"src": "footage/mayday1961.mp4", "ss": 28.2, "w": 1.0, "y0": 95, "push": 0.06}     # St Basil's, balloons
Dm = {"src": "footage/moscow1965.mp4", "ss": 84.2, "w": 1.2, "y0": 50, "push": 0.08}    # convoy with flag pole in foreground
S.append(dict(dur=d_card, type="gfx", html="gfx/datecard.html", data={"l1": TX["date"][0], "l2": TX["date"][1]}))
S.append(dict(dur=d_foot, type="video", montage={"xf": 0.2, "shots": [A, B, Dm] if lang == "en" else [A, B, C, Dm]}, overlay={"chip": TX["chip"]}))
# seg 2: the size of the Soviet Union – map + counting stats
S.append(dict(dur=L[2], type="gfx", html="gfx/map.html", data={"caption": TX["cap"], "order": [{"k": "Russia", "stay": True, "col": "#a30d25"}],
              "stats": [dict(label=l, v=v, pre=p, suf=s, t=L[2] * f + 0.5) for (l, v, p, s), f in zip(TX["stats"], (0.34, 0.5, 0.66))]}))
# seg 3: first satellite, first human in space, divided Europe – public-domain Universal Newsreel footage
d3 = L[3]
S.append(dict(dur=d3, type="video", montage={"xf": 0.25, "shots": [
                {"src": "footage/sputnik1957.mp4", "ss": 20.0, "w": 1.0, "y0": 60, "push": 0.05},
                {"src": "footage/gagarin1961.mp4", "ss": 36.0, "w": 1.0, "y0": 70, "push": 0.05},
                {"src": "footage/wall1962.mp4", "ss": 12.0, "w": 1.0, "y0": 50, "push": 0.06}]},
              overlay={"chip": TX["chip"], "stamp": dict(l1=TX["berlin"][0], l2=TX["berlin"][1], t0=(d3 + 0.5) * 0.68, t1=d3 + 0.3)}))
# seg 4: it ceased to exist – breakaway map
step = (L[4] - 1.2) / 14
S.append(dict(dur=L[4], type="gfx", html="gfx/map.html", data={"caption": TX["cap"], "title": TX["brk"], "order": order, "t0": 0.7, "step": round(step, 3)}))
# seg 5: causes – Brezhnev stagnation, Afghan war, Chernobyl, Gorbachev
w = [1, 1, 1, 1.25]; tot = sum(w)
def ov(stamp=None, lower=None, d=1):
    o = {}
    if stamp: o["stamp"] = dict(l1=stamp[0], l2=stamp[1], t0=0.8, t1=d - 0.2)
    if lower: o["lower"] = dict(name=lower[0], role=lower[1], t0=0.8, t1=d - 0.2)
    return o
d5 = [L[5] * x / tot for x in w]
S.append(dict(dur=d5[0], type="photo", img=img("brezhnev_nixon_1973"), kb=dict(z1=1.12, px=.03), overlay=ov(lower=TX["brezhnev"], d=d5[0])))
S.append(dict(dur=d5[1], type="gfx", html="gfx/map.html", data={"mapfile": "map_data_south.js", "caption": TX["afghan_cap"], "counter": "", "focus": {"names": ["Afghanistan"], "col": "#e3c23a",
              "t0": 0.6, "title": TX["afghan_t"][0], "sub": TX["afghan_t"][1], "arrows": [{"from": "Termez", "to": "Kabul", "t": 1.2, "dur": 1.6, "bend": -30}, {"from": "Kushka", "to": "Kandahar", "t": 1.8, "dur": 1.6, "bend": 25}],
              "labels": [{"at": "Kabul", "text": TX["kabul"], "dx": 18, "dy": -12, "t": 2.8}]}}))
S.append(dict(dur=d5[2], type="photo", img=img("chernobyl_reactor4"), kb=dict(z1=1.14, px=-.03), overlay=ov(stamp=TX["cher"], d=d5[2])))
S.append(dict(dur=d5[3], type="photo", img=img("gorbachev_1987"), kb=dict(z1=1.12, fy=.38, py=.05), overlay=ov(lower=TX["gorb"], d=d5[3])))
# outro title card (silent)
S.append(dict(dur=4.0, type="gfx", html="gfx/title.html", data={"title": TX["title"], "sub": TX["sub"], "from": 1922, "to": 1991}))

sb = {"lang": lang, "root": ROOT, "fade": 0.5, "audio": f"audio/{lang}_prev.wav", "scenes": S}
out = f"{ROOT}/build/sb_preview_{lang}.json"; json.dump(sb, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(out, "scenes", len(S), "total", round(sum(s["dur"] for s in S), 1))
