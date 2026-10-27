# -*- coding: utf-8 -*-
"""Full-length storyboard builder.   sb_full.py en|ta   ->  build/sb_full_<lang>.json
Scene durations come from audio/<lang>_full/timings.json; the same visuals are used in both languages,
only on-screen text (English / Tamil) differs.  Every scene has a weight 'w' (share of its segment) or a fixed 'd'."""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lang = sys.argv[1]; I = 0 if lang == "en" else 1
T = json.load(open(f"{ROOT}/audio/{lang}_full/timings.json", encoding="utf-8"))
CH = json.load(open(f"{ROOT}/script/chapters.json", encoding="utf-8"))
GAP = 0.5
L = {t["seg"]: t["dur"] + GAP for t in T}
CHAP = {c["id"]: c for c in CH["chapters"]}
SEGOF = {}                                         # (chapter, local) -> global segment number
for s in CH["segments"]: SEGOF[(s["chapter"], s["local"])] = s["seg"]
def x(en, ta): return en if I == 0 else ta         # pick the language's string

# ---------------------------------------------------------------- shared text
CHIP = x("Archival footage", "ஆவணக் காட்சிகள்")
COUNTRY = {"Lithuania": ("Lithuania", "லிதுவேனியா"), "Georgia": ("Georgia", "ஜார்ஜியா"), "Estonia": ("Estonia", "எஸ்தோனியா"), "Latvia": ("Latvia", "லாத்வியா"),
           "Ukraine": ("Ukraine", "உக்ரைன்"), "Belarus": ("Belarus", "பெலாரஸ்"), "Moldova": ("Moldova", "மால்டோவா"), "Azerbaijan": ("Azerbaijan", "அசர்பைஜான்"),
           "Uzbekistan": ("Uzbekistan", "உஸ்பெகிஸ்தான்"), "Kyrgyzstan": ("Kyrgyzstan", "கிர்கிஸ்தான்"), "Tajikistan": ("Tajikistan", "தஜிகிஸ்தான்"),
           "Armenia": ("Armenia", "ஆர்மீனியா"), "Turkmenistan": ("Turkmenistan", "துர்க்மெனிஸ்தான்"), "Kazakhstan": ("Kazakhstan", "கஜகஸ்தான்"), "Russia": ("Russia", "ரஷ்யா")}
CN = lambda k: COUNTRY[k][I]
MONTH = {"Mar90": x("March 1990", "மார்ச் 1990"), "Apr91": x("April 1991", "ஏப்ரல் 1991"), "Aug": x("August 1991", "ஆகஸ்ட் 1991"), "Sep": x("September 1991", "செப்டம்பர் 1991"),
         "Oct": x("October 1991", "அக்டோபர் 1991"), "Dec": x("December 1991", "டிசம்பர் 1991")}
COLORS = {"Lithuania": "#3b82c4", "Georgia": "#e07a1f", "Estonia": "#2fa38a", "Latvia": "#8a4fbf", "Ukraine": "#e3c23a", "Belarus": "#4fa34f", "Moldova": "#c45a8c",
          "Azerbaijan": "#2c8fa6", "Uzbekistan": "#b5651d", "Kyrgyzstan": "#d24d57", "Tajikistan": "#6b8e23", "Armenia": "#e9967a", "Turkmenistan": "#20b2aa",
          "Kazakhstan": "#5b6fd6", "Russia": "#c8102e"}

# ---------------------------------------------------------------- scene helpers
def OV(chip=False, stamp=None, lower=None, t0=1.0):
    def f(dur):
        o = {}
        if chip: o["chip"] = CHIP
        if stamp: o["stamp"] = dict(l1=stamp[0], l2=stamp[1], t0=t0, t1=max(t0 + 1.5, dur - 0.3))
        if lower: o["lower"] = dict(name=lower[0], role=lower[1], t0=t0, t1=max(t0 + 1.5, dur - 0.3))
        return o
    return f
def P(img, w=1, kb=None, ov=None): return dict(type="photo", img=f"images/{img}", w=w, kb=kb or {}, ov=ov)
def SH(src, ss, w=1.0, y0=60, push=0.06): return dict(src=f"footage/{src}.mp4", ss=ss, w=w, y0=y0, push=push)
def V(shots, w=1, ov=None, xf=0.2): return dict(type="video", w=w, montage={"xf": xf, "shots": shots}, ov=ov if ov else OV(chip=True))
def G(html, data, w=1, ov=None): return dict(type="gfx", html=f"gfx/{html}.html", w=w, data=data, ov=ov)
def card(kind, w=1, **d): return G("cards", dict(kind=kind, **d), w=w)
def TITLE(cid):
    c = CHAP[cid]; a, b = c["years"]
    d = dict(title=x(c["en"], c["ta"]), sub=SUBS[cid], **{"from": a, "to": b})
    if cid in ("C11", "C12"): d["noyear"] = True
    return dict(type="gfx", html="gfx/title.html", d=3.5, data=d)
SUBS = {"C1": "1957 – 1985", "C2": "1985 – 1987", "C3": "1985 – 1989", "C4": "1979 – 1989", "C5": x("26 April 1986", "ஏப்ரல் 26, 1986"), "C6": "1988 – 1991",
        "C7": "1989", "C8": "1990 – 1991", "C9": x("19 – 21 August 1991", "ஆகஸ்ட் 19 – 21, 1991"), "C10": x("December 1991", "டிசம்பர் 1991"),
        "C11": x("The causes", "காரணங்கள்"), "C12": x("After 1991", "1991-க்குப் பிறகு")}

S = []
def emit(cid, local, scenes):
    seg = SEGOF[(cid, local)]; Lseg = L[seg]
    fixed = sum(s.get("d", 0) for s in scenes); free = Lseg - fixed
    wsum = sum(s.get("w", 1) for s in scenes if "d" not in s)
    for s in scenes:
        s = dict(s); dur = s.pop("d") if "d" in s else free * s.pop("w", 1) / wsum
        assert dur >= 1.5, f"scene too short ({dur:.2f}s) in {cid}.{local}"
        s.pop("w", None); s["dur"] = dur
        if callable(s.get("data")): s["data"] = s["data"](dur)
        if "ov" in s:
            f = s.pop("ov")
            if f: s["overlay"] = f(dur)
        S.append(s)

# ================================================================= PROLOGUE (same scenes as the approved previews)
GP = 0.55 if lang == "en" else 0.5
Lp = L[1]; d_card = Lp * GP
A = dict(src="footage/mayday1961.mp4", ss=4.2, w=1.0, y0=40, push=0.07); B = dict(src="footage/moscow1965.mp4", ss=15.5, w=1.0, y0=60, push=0.06)
C = dict(src="footage/mayday1961.mp4", ss=28.2, w=1.0, y0=95, push=0.06); Dm = dict(src="footage/moscow1965.mp4", ss=84.2, w=1.2, y0=50, push=0.08)
S.append(dict(dur=d_card, type="gfx", html="gfx/datecard.html", data={"l1": x("25 December 1991", "25 டிசம்பர் 1991"), "l2": x("Moscow", "மாஸ்கோ")}))
S.append(dict(dur=Lp - d_card, type="video", montage={"xf": 0.2, "shots": [A, B, Dm] if lang == "en" else [A, B, C, Dm]}, overlay={"chip": CHIP}))
L2 = L[2]
S.append(dict(dur=L2, type="gfx", html="gfx/map.html", data={"caption": x("Soviet republics", "சோவியத் குடியரசுகள்"), "order": [{"k": "Russia", "stay": True, "col": "#a30d25"}],
    "stats": [dict(label=l, v=v, pre=p, suf=s, t=L2 * f + 0.5) for (l, v, p, s), f in zip(
        [(x("time zones", "நேர மண்டலங்கள்"), 11, "", ""), (x("republics", "குடியரசுகள்"), 15, "", ""),
         (x("people (approx.)", "மக்கள் (கிட்டத்தட்ட)"), x(290, 29), "", x(" million", " கோடி"))], (0.34, 0.5, 0.66))]}))
L3 = L[3]
S.append(dict(dur=L3, type="video", montage={"xf": 0.25, "shots": [dict(src="footage/sputnik1957.mp4", ss=20.0, w=1.0, y0=60, push=0.05),
    dict(src="footage/gagarin1961.mp4", ss=36.0, w=1.0, y0=70, push=0.05), dict(src="footage/wall1962.mp4", ss=12.0, w=1.0, y0=50, push=0.06)]},
    overlay={"chip": CHIP, "stamp": dict(l1=x("Berlin", "பெர்லின்"), l2="1962", t0=(L3 + 0.5) * 0.68, t1=L3 + 0.3)}))
L4 = L[4]; order0 = [(k, m) for k, m in [("Lithuania", "Mar90"), ("Georgia", "Apr91"), ("Estonia", "Aug"), ("Latvia", "Aug"), ("Ukraine", "Aug"), ("Belarus", "Aug"), ("Moldova", "Aug"),
    ("Azerbaijan", "Aug"), ("Uzbekistan", "Aug"), ("Kyrgyzstan", "Aug"), ("Tajikistan", "Sep"), ("Armenia", "Sep"), ("Turkmenistan", "Oct"), ("Kazakhstan", "Dec")]]
ORDER_ALL = [{"k": k, "label": CN(k), "date": MONTH[m], "col": COLORS[k]} for k, m in order0] + [{"k": "Russia", "label": "", "date": "", "col": "#c8102e", "stay": True}]
S.append(dict(dur=L4, type="gfx", html="gfx/map.html", data={"caption": x("Soviet republics", "சோவியத் குடியரசுகள்"), "title": x("1990 – 1991: the breakaway", "1990 – 1991: பிரிந்து சென்ற குடியரசுகள்"),
    "order": ORDER_ALL, "t0": 0.7, "step": round((L4 - 1.2) / 14, 3)}))
L5 = L[5]; w5 = [1, 1, 1, 1.25]; d5 = [L5 * q / sum(w5) for q in w5]
def ov5(stamp=None, lower=None, d=1):
    o = {}
    if stamp: o["stamp"] = dict(l1=stamp[0], l2=stamp[1], t0=0.8, t1=d - 0.2)
    if lower: o["lower"] = dict(name=lower[0], role=lower[1], t0=0.8, t1=d - 0.2)
    return o
BREZ = (x("Leonid Brezhnev", "லியோனிட் பிரெஷ்நேவ்"), x("General Secretary, 1964–1982", "பொதுச் செயலாளர், 1964–1982"))
GORB = (x("Mikhail Gorbachev", "மிகைல் கோர்பச்சேவ்"), x("General Secretary, 1985–1991", "பொதுச் செயலாளர், 1985–1991"))
S.append(dict(dur=d5[0], type="photo", img="images/brezhnev_nixon_1973.png", kb=dict(z1=1.12, px=.03), overlay=ov5(lower=BREZ, d=d5[0])))
S.append(dict(dur=d5[1], type="gfx", html="gfx/map.html", data={"mapfile": "map_data_south.js", "caption": x("Soviet–Afghan war", "சோவியத்–ஆப்கான் போர்"), "counter": "", "focus": {"names": ["Afghanistan"], "col": "#e3c23a",
    "t0": 0.6, "title": x("Afghanistan", "ஆப்கானிஸ்தான்"), "sub": "1979 – 1989", "arrows": [{"from": "Termez", "to": "Kabul", "t": 1.2, "dur": 1.6, "bend": -30}, {"from": "Kushka", "to": "Kandahar", "t": 1.8, "dur": 1.6, "bend": 25}],
    "labels": [{"at": "Kabul", "text": x("Kabul", "காபூல்"), "dx": 18, "dy": -12, "t": 2.8}]}}))
S.append(dict(dur=d5[2], type="photo", img="images/chernobyl_reactor4.jpg", kb=dict(z1=1.14, px=-.03), overlay=ov5(stamp=(x("Chernobyl", "செர்னோபில்"), x("26 April 1986", "26 ஏப்ரல் 1986")), d=d5[2])))
S.append(dict(dur=d5[3], type="photo", img="images/gorbachev_1987.jpg", kb=dict(z1=1.12, fy=.38, py=.05), overlay=ov5(lower=GORB, d=d5[3])))

# ================================================================= CHAPTER 1 – THE GIANT
SPUT = SH("sputnik1957", 8.0, 1, 60, .05); GAG = SH("gagarin1961", 12.0, 1, 70, .05)
emit("C1", 1, [TITLE("C1"), V([SPUT, GAG], w=1.4), P("gagarin_1961.jpg", w=1.3, kb=dict(z0=1.0, z1=1.12, fx=.5, fy=.28, py=.22),
     ov=OV(lower=(x("Yuri Gagarin", "யூரி ககாரின்"), x("First human in space, 1961", "விண்வெளிக்குச் சென்ற முதல் மனிதர், 1961"))))])
emit("C1", 2, [V([SH("nixon_khrushchev1959", 58.0, 1.4, 60, .06), SH("cuba1962", 6.0, 1.0, 60, .06), SH("cuba1962", 46.0, 1.2, 55, .06)], w=1,
     ov=lambda dur: dict(chip=CHIP, stamp=dict(l1=x("Cuban Missile Crisis", "கியூபா ஏவுகணை நெருக்கடி"), l2=x("October 1962", "அக்டோபர் 1962"), t0=dur * 0.6, t1=dur - 0.2)))])
emit("C1", 3, [V([SH("mayday1961", 24.0, 1.0, 60, .06), SH("moscow1965", 28.0, 1.0, 60, .06)], w=1.4),
     P("brezhnev_nixon_1973.png", w=1.3, kb=dict(z1=1.12, px=.03), ov=OV(lower=BREZ)),
     P("apollo_soyuz_1975.jpg", w=1.1, kb=dict(z0=1.12, z1=1.0, px=-.02), ov=OV(stamp=(x("Apollo–Soyuz", "அப்போலோ–சோயுஸ்"), x("A handshake in orbit, 1975", "விண்வெளியில் கைகுலுக்கல், 1975"))))])
emit("C1", 4, [card("list", w=1, title=x("The planned economy", "திட்டமிட்ட பொருளாதாரம்"), t0=1.2, step=2.6, gap=190,
     items=[x("Growth slowing down", "வளர்ச்சி மெதுவடைந்தது"), x("Shortages of basic goods", "அடிப்படைப் பொருட்களுக்குப் பற்றாக்குறை"), x("Long queues", "நீண்ட வரிசைகள்")])])
emit("C1", 5, [G("timeline", dict(mode="bars", title=x("Leaders of the Soviet Union", "சோவியத் ஒன்றியத்தின் தலைவர்கள்"), axis={"from": 1964, "to": 1992}, tick=4, h=420, t0=0.8, step=3.2,
        items=[dict(name=x("Brezhnev", "பிரெஷ்நேவ்"), years="1964–1982", **{"from": 1964, "to": 1982}, col="#8f1022"), dict(name=x("Andropov", "ஆண்ட்ரோபோவ்"), years="1982–84", **{"from": 1982, "to": 1984.1}, col="#6d1a2a"),
               dict(name=x("Chernenko", "செர்னென்கோ"), years="1984–85", **{"from": 1984.1, "to": 1985.2}, col="#561a28"), dict(name=x("Gorbachev", "கோர்பச்சேவ்"), years="1985–1991", **{"from": 1985.2, "to": 1991.98}, col="#c8102e")]), w=2.2),
     P("gorbachev_1987.jpg", w=1.3, kb=dict(z1=1.12, fy=.38, py=.05), ov=OV(lower=GORB))])

# ================================================================= CHAPTER 2 – A NEW LEADER
emit("C2", 1, [TITLE("C2"), P("gorbachev_1987.jpg", w=1.0, kb=dict(z0=1.0, z1=1.1, fy=.4, py=-.03), ov=OV(lower=GORB)),
     card("definition", w=1.5, word=x("Perestroika", "பெரெஸ்ட்ரோயிகா"), pron=x("[ pyeh-ryes-TROY-kah ]", ""), meaning=x("restructuring", "மறுசீரமைப்பு"),
          sub=x("Loosening central planning, letting enterprises decide more for themselves", "மத்தியத் திட்டமிடலைத் தளர்த்தி, நிறுவனங்கள் தாமே முடிவெடுக்க விடுவது"))])
emit("C2", 2, [card("definition", w=1.0, word=x("Glasnost", "கிளாஸ்நோஸ்ட்"), pron=x("[ GLAHZ-nohst ]", ""), meaning=x("openness", "வெளிப்படைத்தன்மை"),
          sub=x("Free speech, open reporting, public debate", "கருத்துச் சுதந்திரம், வெளிப்படையான செய்தி, பொது விவாதம்")),
     card("list", w=1.0, title=x("What glasnost changed", "கிளாஸ்நோஸ்ட் கொண்டுவந்த மாற்றங்கள்"), t0=0.8, step=1.0, gap=150,
          items=[x("Newspapers report hidden problems", "மறைக்கப்பட்ட பிரச்சினைகளை நாளிதழ்கள் வெளியிடுகின்றன"), x("Banned books are published", "தடை நூல்கள் வெளிவருகின்றன"),
                 x("Leaders openly criticised", "தலைவர்கள் வெளிப்படையாக விமர்சிக்கப்படுகின்றனர்"), x("Political prisoners released", "அரசியல் கைதிகள் விடுதலை")])])
emit("C2", 3, [P("reagan_gorbachev_inf.jpg", w=1.5, kb=dict(z0=1.0, z1=1.1, px=-.02), ov=OV(stamp=(x("Washington", "வாஷிங்டன்"), x("December 1987", "டிசம்பர் 1987")))),
     card("bigtext", w=1.0, text=x("INF Treaty", "ஐ.என்.எஃப் ஒப்பந்தம்"), sub=x("The first agreement to eliminate a whole class of nuclear missiles", "ஒரு முழு வகை அணு ஏவுகணைகளை ஒழிக்கும் முதல் ஒப்பந்தம்"))])
emit("C2", 4, [G("timeline", dict(mode="events", noticks=True, title="1985 – 1991", axis={"from": 1985, "to": 1992}, sweep=5.5, step=1.2,
        items=[dict(at=1985.2, y="1985", label=x("Gorbachev takes power", "கோர்பச்சேவ் ஆட்சிக்கு வருகிறார்"), t=0.9), dict(at=1986.3, y="1986", label=x("Chernobyl", "செர்னோபில்"), t=2.0),
               dict(at=1989.85, y="1989", label=x("Berlin Wall opens", "பெர்லின் சுவர் திறக்கிறது"), t=3.1), dict(at=1991.65, y="1991", label=x("August coup", "ஆகஸ்ட் சதி"), t=4.2),
               dict(at=1991.98, y="", label=x("USSR ends", "சோவியத் ஒன்றியம் முடிவு"), t=5.2)]), w=1)])

# ================================================================= CHAPTER 3 – AN ECONOMY IN TROUBLE
emit("C3", 1, [TITLE("C3"), card("list", w=1, title=x("A planned economy", "திட்டமிடப்பட்ட பொருளாதாரம்"), t0=1.2, step=3.0, gap=170,
     items=[x("Fixed prices", "நிர்ணயிக்கப்பட்ட விலைகள்"), x("Production quotas", "உற்பத்தி இலக்குகள்"), x("A huge share of resources for the military", "வளங்களில் பெரும்பகுதி இராணுவத்துக்கு"),
            x("Weak consumer goods", "நலிந்த நுகர்வுப் பொருட்கள்")])])
emit("C3", 2, [G("chart", dict(title=x("Oil price", "எண்ணெய் விலை"), unit=x("US dollars per barrel, approximate annual average", "ஒரு பீப்பாய்க்கு அமெரிக்க டாலர், சுமார் ஆண்டுச் சராசரி"),
     x=[1979, 1992], y=[0, 40], ystep=10, xticks=[1980, 1985, 1990], pre="$", draw=5.0, points=[{"x": 1980, "y": 37.4}, {"x": 1985, "y": 26.9}, {"x": 1986, "y": 14.4, "below": True}, {"x": 1990, "y": 23.2}, {"x": 1991, "y": 20.2}],
     annot={"x": 1986, "from": 26.9, "to": 14.4, "label": x("about −46%", "சுமார் −46%"), "t": 7.5},
     source=x("Source: US crude oil price series (approximate, nominal)", "ஆதாரம்: அமெரிக்க கச்சா எண்ணெய் விலைத் தொடர் (தோராயம்)")), w=1)])
emit("C3", 3, [card("list", w=1, title=x("Strain on the economy", "பொருளாதாரத்தின் நெருக்கடி"), t0=1.0, step=3.4, gap=180,
     items=[x("Shortages grow worse", "பற்றாக்குறை மோசமாகிறது"), x("Budget deficit widens", "பட்ஜெட் பற்றாக்குறை விரிவடைகிறது"), x("Ration coupons return: sugar, soap", "ரேஷன் சீட்டுகள் திரும்புகின்றன: சர்க்கரை, சோப்பு")])])
emit("C3", 4, [card("bigtext", w=1, text=x("Empty shelves", "காலி அலமாரிகள்"), sub=x("Openness gave people the freedom to complain", "வெளிப்படைத்தன்மை குறை சொல்லும் சுதந்திரத்தைத் தந்தது"))])

# ================================================================= CHAPTER 4 – THE WAR
def afghan_map(extra=None, **k):
    d = {"mapfile": "map_data_south.js", "caption": x("Soviet–Afghan war", "சோவியத்–ஆப்கான் போர்"), "counter": "", "focus": {"names": ["Afghanistan"], "col": "#e3c23a", "t0": 0.6,
         "title": x("Afghanistan", "ஆப்கானிஸ்தான்"), "sub": "1979 – 1989", "arrows": [{"from": "Termez", "to": "Kabul", "t": 1.4, "dur": 1.8, "bend": -30}, {"from": "Kushka", "to": "Kandahar", "t": 2.2, "dur": 1.8, "bend": 25}],
         "labels": [{"at": "Kabul", "text": x("Kabul", "காபூல்"), "dx": 18, "dy": -12, "t": 3.2}]}}
    return G("map", d, **k)
emit("C4", 1, [TITLE("C4"), afghan_map(w=1)])
emit("C4", 2, [card("bignum", w=1, title=x("The Soviet–Afghan war", "சோவியத்–ஆப்கான் போர்"), nums=[dict(v=9, suf=x("years", "ஆண்டுகள்"), label=x("of war", "போர்"), t=1.0),
     dict(v=15000, pre="≈ ", label=x("Soviet soldiers killed", "சோவியத் வீரர்கள் கொல்லப்பட்டனர்"), t=3.5)], sub=x("Afghan casualties were far higher", "ஆப்கானியர்களின் இழப்பு இதைவிட மிக அதிகம்"))])
emit("C4", 3, [G("timeline", dict(mode="events", noticks=True, title=x("1979 – 1989", "1979 – 1989"), axis={"from": 1979, "to": 1990}, sweep=5, step=1.5,
     items=[dict(at=1979.95, y=x("Dec 1979", "டிச. 1979"), label=x("Soviet troops enter Afghanistan", "சோவியத் படைகள் ஆப்கானிஸ்தானுக்குள் நுழைகின்றன"), t=1.0),
            dict(at=1989.12, y=x("Feb 1989", "பிப். 1989"), label=x("The last troops leave", "கடைசி வீரர்கள் வெளியேறுகின்றனர்"), t=5.5)]), w=1)])

# ================================================================= CHAPTER 5 – CHERNOBYL
emit("C5", 1, [TITLE("C5"), G("map", dict(mapfile="map_data_ee.js", caption=x("Chernobyl, Ukraine", "செர்னோபில், உக்ரைன்"), counter="", repcol="#3a3a44",
        paint=[{"k": "Ukraine", "col": "#e3c23a", "t": 0.5}], texts=[dict(at="Chernobyl", text=x("Chernobyl", "செர்னோபில்"), t=1.2, dx=-18, dy=-16, anchor="end", dot=True),
        dict(at="Kyiv", text=x("Kyiv", "கீவ்"), t=2.0, dx=-18, dy=26, anchor="end", dot=True), dict(at="Moscow", text=x("Moscow", "மாஸ்கோ"), t=2.8, dx=18, dy=-14, anchor="start", dot=True)],
        note={"name": x("26 April 1986", "ஏப்ரல் 26, 1986"), "date": x("Reactor No. 4 explodes", "நான்காம் உலை வெடிக்கிறது"), "t": 1.0}), w=1.4),
     P("chernobyl_reactor4.jpg", w=1.2, kb=dict(z1=1.12, px=-.03), ov=OV(stamp=(x("Chernobyl today", "இன்றைய செர்னோபில்"), x("Reactor No. 4 and its shelter", "நான்காம் உலையும் அதன் மூடிய கூடும்"))))])
emit("C5", 2, [P("chernobyl_radar.jpg", w=1.2, kb=dict(z0=1.0, z1=1.1, px=.02), ov=OV(stamp=(x("Radar image of the area", "அப்பகுதியின் ரேடார் படம்"), "NASA / JPL"))),
     card("list", w=1.5, title=x("The human cost", "மனித இழப்பு"), t0=0.8, step=2.8, gap=170, items=[x("Tens of thousands evacuated from Pripyat", "பிரிப்யாத்திலிருந்து பல்லாயிரம் பேர் வெளியேற்றம்"),
          x("Hundreds of thousands eventually resettled", "பல நூறாயிரம் பேர் இடம் மாற்றம்"), x("Firefighters, soldiers and miners at the site", "தீயணைப்பு வீரர்கள், படைவீரர்கள், சுரங்கத் தொழிலாளர்கள்")])])
emit("C5", 3, [card("bigtext", w=1, text=x("A turning point?", "ஒரு திருப்புமுனையா?"), sub=x("Gorbachev later suggested it may have been the real turning point", "அதுவே உண்மையான திருப்புமுனை என்று கோர்பச்சேவ் பின்னர் கூறினார்"))])

# ================================================================= CHAPTER 6 – FORCES UNLEASHED
emit("C6", 1, [TITLE("C6"), G("map", dict(mapfile="map_data_caucasus.js", caption=x("Nagorno-Karabakh", "நகோர்னோ-கரபாக்"), counter="", repcol="#3a3a44",
        paint=[{"k": "Armenia", "col": "#e9967a", "t": 0.5}, {"k": "Azerbaijan", "col": "#2c8fa6", "t": 0.8}],
        texts=[dict(at="Yerevan", text=x("Yerevan", "யெரெவான்"), t=1.5, dx=-16, dy=-12, anchor="end", dot=True), dict(at="Baku", text=x("Baku", "பாகு"), t=2.2, dx=16, dy=-12, anchor="start", dot=True),
               dict(at="Stepanakert", text=x("Karabakh", "கரபாக்"), t=3.0, dx=16, dy=28, anchor="start", dot=True)],
        note={"name": x("February 1988", "பிப்ரவரி 1988"), "date": x("Armenians demand to join Armenia", "ஆர்மீனியாவுடன் இணையக் கோரிக்கை"), "t": 1.0}), w=1)])
emit("C6", 2, [G("map", dict(mapfile="map_data_baltic.js", caption=x("The Baltic states", "பால்டிக் நாடுகள்"), counter="", repcol="#3a3a44",
        paint=[{"k": "Estonia", "col": "#2fa38a", "t": 0.5}, {"k": "Latvia", "col": "#8a4fbf", "t": 0.8}, {"k": "Lithuania", "col": "#3b82c4", "t": 1.1}],
        texts=[dict(cent=k, text=CN(k), t=1.5 + i * 0.4, size=32) for i, k in enumerate(["Estonia", "Latvia", "Lithuania"])],
        note={"name": x("1939: the secret pact", "1939: ரகசிய ஒப்பந்தம்"), "date": x("Molotov–Ribbentrop Pact", "மொலோட்டோவ்–ரிப்பன்ட்ரோப் ஒப்பந்தம்"), "t": 2.5}), w=1)])
BALTIC_WAY = G("map", dict(mapfile="map_data_baltic.js", caption=x("The Baltic Way", "பால்டிக் பாதை"), counter="", repcol="#3a3a44",
        paint=[{"k": "Estonia", "col": "#2fa38a", "t": 0.3}, {"k": "Latvia", "col": "#8a4fbf", "t": 0.3}, {"k": "Lithuania", "col": "#3b82c4", "t": 0.3}],
        chain={"pts": ["Tallinn", "Riga", "Vilnius"], "t": 1.2, "dur": 5.0, "n": 130, "col": "#ffd84a"},
        texts=[dict(at="Tallinn", text=x("Tallinn", "தாலின்"), t=1.4, dx=-18, dy=-18, anchor="end", dot=True), dict(at="Riga", text=x("Riga", "ரிகா"), t=3.4, dx=-18, dy=-4, anchor="end", dot=True),
               dict(at="Vilnius", text=x("Vilnius", "வில்னியஸ்"), t=5.8, dx=18, dy=28, anchor="start", dot=True)],
        note={"name": x("23 August 1989", "ஆகஸ்ட் 23, 1989"), "date": x("≈ 675 km · about two million people", "≈ 675 கி.மீ · ஏறத்தாழ இருபது லட்சம் பேர்"), "t": 1.0}), w=1.5)
emit("C6", 3, [BALTIC_WAY, card("bignum", w=1, title=x("The Baltic Way · 23 August 1989", "பால்டிக் பாதை · ஆகஸ்ட் 23, 1989"),
     nums=[dict(v=x(2, 20), suf=x("million", "லட்சம்"), label=x("people joined hands", "பேர் கைகோர்த்தனர்"), t=0.8), dict(v=675, pre="≈ ", suf=x("km", "கி.மீ"), label=x("human chain across three countries", "மூன்று நாடுகளில் மனிதச் சங்கிலி"), t=2.0)],
     sub=x("Estonia · Latvia · Lithuania", "எஸ்தோனியா · லாத்வியா · லிதுவேனியா"))])
emit("C6", 4, [G("map", dict(mapfile="map_data_full.js", caption=x("Soviet crackdowns", "சோவியத் அடக்குமுறைகள்"), counter="", repcol="#3a3a44",
        paint=[{"k": "Georgia", "col": "#e07a1f", "t": 0.5}, {"k": "Lithuania", "col": "#3b82c4", "t": 0.5}],
        texts=[dict(at="Tbilisi", text=x("Tbilisi · April 1989", "திபிலிசி · ஏப்ரல் 1989"), t=1.8, dx=-16, dy=40, anchor="middle", dot=True, size=34),
               dict(at="Vilnius", text=x("Vilnius · January 1991", "வில்னியஸ் · ஜனவரி 1991"), t=4.5, dx=0, dy=-26, anchor="middle", dot=True, size=34)]), w=1.4),
     card("bigtext", w=1.0, text=x("Nationalism", "தேசியவாதம்"), sub=x("The strongest political force in the country", "நாட்டின் வலிமையான அரசியல் சக்தி"))])

# ================================================================= CHAPTER 7 – 1989
EE_FOOT = x("Modern borders shown", "தற்கால எல்லைகள் காட்டப்பட்டுள்ளன")
def ee(paint, texts, caption, note=None, **k):
    d = dict(mapfile="map_data_ee.js", caption=caption, counter="", repcol="#3a3a44", paint=paint, texts=texts, title=EE_FOOT, ttlsize=30)
    if note: d["note"] = note
    return G("map", d, **k)
GOLD = "#e3c23a"
emit("C7", 1, [TITLE("C7"), ee([{"k": "Poland", "col": GOLD, "t": 1.2}, {"k": "Hungary", "col": GOLD, "t": 4.0}],
     [dict(at="Warsaw", text=x("Poland · June 1989", "போலந்து · ஜூன் 1989"), t=1.8, dy=-22, size=30, dot=True), dict(at="Budapest", text=x("Hungary · border opens", "ஹங்கேரி · எல்லை திறப்பு"), t=4.6, dy=44, size=30, dot=True)],
     x("Eastern Europe, 1989", "கிழக்கு ஐரோப்பா, 1989"), w=1)])
emit("C7", 2, [dict(type="gfx", html="gfx/datecard.html", d=3.0, data={"l1": x("9 November 1989", "நவம்பர் 9, 1989"), "l2": x("Berlin", "பெர்லின்")}),
     P("brandenburg_1989.jpg", w=1.4, kb=dict(z0=1.08, z1=1.0, px=-.03), ov=OV(stamp=(x("Brandenburg Gate", "பிராண்டன்பர்க் வாயில்"), "1989"))),
     V([SH("wall1962", 28.0, 1.0, 55, .06), SH("wall1962", 40.0, 1.0, 50, .06)], w=1.0, ov=lambda dur: dict(chip=CHIP, stamp=dict(l1=x("The Berlin Wall", "பெர்லின் சுவர்"), l2=x("as it stood in 1962", "1962-இல் இருந்தபடி"), t0=0.8, t1=dur - 0.2)))])
emit("C7", 3, [ee([{"k": "Poland", "col": GOLD, "t": 0.0}, {"k": "Hungary", "col": GOLD, "t": 0.0}, {"k": "Czechia", "col": "#e07a1f", "t": 1.5}, {"k": "Slovakia", "col": "#e07a1f", "t": 1.5},
      {"k": "Bulgaria", "col": "#c45a8c", "t": 3.8}, {"k": "Romania", "col": "#2c8fa6", "t": 6.0}],
     [dict(at="Prague", text=x("Czechoslovakia · Nov 1989", "செக்கோஸ்லோவாக்கியா · நவ. 1989"), t=1.8, dy=-24, size=28, dot=True), dict(at="Sofia", text=x("Bulgaria · Nov 1989", "பல்கேரியா · நவ. 1989"), t=4.1, dy=46, size=28, dot=True),
      dict(at="Bucharest", text=x("Romania · Dec 1989", "ருமேனியா · டிச. 1989"), t=6.3, dy=-24, size=28, dot=True)], x("The Eastern Bloc unravels", "கிழக்குக் கூட்டணி சிதறுகிறது"), w=1)])

# ================================================================= CHAPTER 8 – TWO LEADERS
YELTSIN = dict(name=x("Boris Yeltsin", "போரிஸ் யெல்ட்சின்"), role=x("Chairman of the Russian Supreme Soviet, 1990 · President of Russia, 1991", "ரஷ்ய உச்ச சோவியத் தலைவர், 1990 · ரஷ்ய அதிபர், 1991"), years="1931 – 2007")
emit("C8", 1, [TITLE("C8"), card("list", w=1, title=x("March 1990", "மார்ச் 1990"), t0=1.2, step=3.0, gap=200, items=[x("The Communist Party gives up its monopoly on power", "கம்யூனிஸ்ட் கட்சி அதிகார ஏகபோகத்தைக் கைவிடுகிறது"),
     x("Gorbachev becomes president of the USSR", "கோர்பச்சேவ் சோவியத் ஒன்றியத்தின் அதிபராகிறார்")])])
emit("C8", 2, [card("person", w=1.2, **YELTSIN), G("timeline", dict(mode="events", noticks=True, title=x("Yeltsin and Russia", "யெல்ட்சினும் ரஷ்யாவும்"), axis={"from": 1990, "to": 1992}, sweep=5, step=1.5,
     items=[dict(at=1990.4, y=x("May 1990", "மே 1990"), label=x("Heads the Russian parliament", "ரஷ்ய நாடாளுமன்றத் தலைவர்"), t=1.0), dict(at=1990.45, y=x("Jun 1990", "ஜூன் 1990"), label=x("Russia declares sovereignty", "ரஷ்யா இறையாண்மையை அறிவிக்கிறது"), t=2.8),
            dict(at=1991.45, y=x("Jun 1991", "ஜூன் 1991"), label=x("Elected President of Russia", "ரஷ்ய அதிபராகத் தேர்வு"), t=4.6)]), w=1.3)])
VOTED = ["Russia", "Ukraine", "Belarus", "Kazakhstan", "Uzbekistan", "Kyrgyzstan", "Tajikistan", "Turkmenistan", "Azerbaijan"]
emit("C8", 3, [G("map", dict(mapfile="map_data_full.js", caption=x("Referendum · 17 March 1991", "வாக்கெடுப்பு · மார்ச் 17, 1991"), counter="", repcol="#3a3a44",
        paint=[{"k": k, "col": "#2fa38a", "t": 0.6 + i * 0.25} for i, k in enumerate(VOTED)],
        note={"name": x("About 76% voted yes", "ஏறத்தாழ 76% ஆம் என்றனர்"), "date": x("Six republics did not take part", "ஆறு குடியரசுகள் பங்கேற்கவில்லை"), "t": 1.5}), w=1.4),
     card("bignum", w=1, title=x("A renewed union?", "புதுப்பிக்கப்பட்ட ஒன்றியமா?"), nums=[dict(v=76, pre="≈ ", suf="%", label=x("voted yes", "ஆம் என்றனர்"), t=0.8), dict(v=6, label=x("of 15 republics did not take part", "15 குடியரசுகளில் பங்கேற்காதவை"), t=2.2)])])

# ================================================================= CHAPTER 9 – THE COUP
emit("C9", 1, [TITLE("C9"), card("bigtext", w=1, text=x("20 August 1991", "ஆகஸ்ட் 20, 1991"), sub=x("The day the new Union Treaty was due to be signed", "புதிய ஒன்றிய ஒப்பந்தம் கையெழுத்தாகவிருந்த நாள்"))])
emit("C9", 2, [G("map", dict(mapfile="map_data_ee.js", caption=x("19 August 1991", "ஆகஸ்ட் 19, 1991"), counter="", repcol="#3a3a44", title=EE_FOOT, ttlsize=30,
        paint=[{"k": "Russia", "col": "#c8102e", "t": 0.3}, {"k": "Ukraine", "col": "#5b4f2a", "t": 0.3}],
        texts=[dict(at="Moscow", text=x("Moscow: tanks roll in", "மாஸ்கோ: டாங்கிகள் நுழைகின்றன"), t=2.0, dx=-18, dy=-16, anchor="end", dot=True, size=32),
               dict(at="Foros", text=x("Foros, Crimea: Gorbachev held under guard", "ஃபோரோஸ், கிரிமியா: கோர்பச்சேவ் காவலில்"), t=4.0, dx=0, dy=48, anchor="middle", dot=True, size=32)],
        note={"name": x("An emergency committee takes power", "ஓர் அவசரக் குழு அதிகாரத்தைக் கைப்பற்றுகிறது"), "date": x("State of emergency declared", "அவசர நிலை அறிவிப்பு"), "t": 1.0}), w=1)])
emit("C9", 3, [card("person", w=1.5, name=x("Boris Yeltsin", "போரிஸ் யெல்ட்சின்"), role=x("Outside the Russian parliament building, Moscow", "மாஸ்கோவில் ரஷ்ய நாடாளுமன்றக் கட்டடத்தின் முன்"), years=x("19 August 1991", "ஆகஸ்ட் 19, 1991")),
     card("bignum", w=1, title=x("Defending the parliament", "நாடாளுமன்றத்தைக் காத்தல்"), nums=[dict(v=3, label=x("people died in the clashes", "பேர் மோதல்களில் உயிரிழந்தனர்"), t=0.8)], sub=x("The army would not storm the building", "இராணுவம் அந்தக் கட்டடத்தைத் தாக்க மறுத்தது"))])
emit("C9", 4, [G("timeline", dict(mode="events", noticks=True, title=x("August 1991", "ஆகஸ்ட் 1991"), axis={"from": 18, "to": 31}, sweep=5.5, step=1.5,
     items=[dict(at=19, y=x("19 Aug", "ஆக. 19"), label=x("The coup begins", "சதி தொடங்குகிறது"), t=1.0), dict(at=21.5, y=x("21 Aug", "ஆக. 21"), label=x("The coup collapses", "சதி தோற்கிறது"), t=3.0),
            dict(at=24, y=x("24 Aug", "ஆக. 24"), label=x("Gorbachev quits as party leader", "கட்சித் தலைவர் பதவியிலிருந்து கோர்பச்சேவ் விலகல்"), t=5.0),
            dict(at=29, y=x("29 Aug", "ஆக. 29"), label=x("Party activities suspended", "கட்சிச் செயல்பாடுகள் நிறுத்தம்"), t=7.0)]), w=1)])

# ================================================================= CHAPTER 10 – THE END
L10 = L[SEGOF[("C10", 1)]]
ORD10 = [("Estonia", "Aug"), ("Latvia", "Aug"), ("Ukraine", "Aug"), ("Belarus", "Aug"), ("Moldova", "Aug"), ("Azerbaijan", "Aug"), ("Uzbekistan", "Aug"), ("Kyrgyzstan", "Aug"),
         ("Tajikistan", "Sep"), ("Armenia", "Sep"), ("Turkmenistan", "Oct"), ("Kazakhstan", "Dec")]
emit("C10", 1, [TITLE("C10"), G("map", lambda dur: dict(caption=x("Soviet republics", "சோவியத் குடியரசுகள்"), title=x("Autumn 1991", "1991 இலையுதிர்காலம்"), startCount=13,
        done=[{"k": "Lithuania", "col": COLORS["Lithuania"]}, {"k": "Georgia", "col": COLORS["Georgia"]}],
        order=[{"k": k, "label": CN(k), "date": MONTH[m], "col": COLORS[k]} for k, m in ORD10] + [{"k": "Russia", "label": "", "date": "", "col": "#c8102e", "stay": True}],
        t0=0.8, step=round(max(0.7, (dur - 1.6) / 12), 3)), w=1)])
emit("C10", 2, [G("map", dict(mapfile="map_data_ee.js", caption=x("Belovezha, 8 December 1991", "பெலோவேஷ், டிசம்பர் 8, 1991"), counter="", repcol="#3a3a44", title=EE_FOOT, ttlsize=30,
        paint=[{"k": "Russia", "col": "#c8102e", "t": 0.5}, {"k": "Ukraine", "col": GOLD, "t": 0.9}, {"k": "Belarus", "col": "#4fa34f", "t": 1.3}],
        texts=[dict(at="Belovezha", text=x("Belovezha Forest, Belarus", "பெலோவேஷ் காடு, பெலாரஸ்"), t=2.2, dx=-18, dy=-16, anchor="end", dot=True, size=32)],
        note={"name": x("The Soviet Union “ceases to exist”", "சோவியத் ஒன்றியம் “இனி இல்லை”"), "date": x("Russia · Ukraine · Belarus", "ரஷ்யா · உக்ரைன் · பெலாரஸ்"), "t": 1.0}), w=1.2),
     card("list", w=1.0, title=x("The three leaders", "மூன்று தலைவர்கள்"), t0=0.6, step=1.5, gap=170, items=[x("Boris Yeltsin · Russia", "போரிஸ் யெல்ட்சின் · ரஷ்யா"), x("Leonid Kravchuk · Ukraine", "லியோனிட் கிராவ்சுக் · உக்ரைன்"),
          x("Stanislau Shushkevich · Belarus", "ஸ்டானிஸ்லாவ் ஷுஷ்கேவிச் · பெலாரஸ்")])])
CIS = ["Russia", "Ukraine", "Belarus", "Moldova", "Armenia", "Azerbaijan", "Kazakhstan", "Uzbekistan", "Turkmenistan", "Kyrgyzstan", "Tajikistan"]
emit("C10", 3, [G("map", dict(mapfile="map_data_full.js", caption=x("Commonwealth of Independent States", "சுதந்திர நாடுகளின் பொதுநலவாயம்"), counter="", repcol="#3a3a44",
        paint=[{"k": k, "col": "#20b2aa", "t": 0.8 + i * 0.35} for i, k in enumerate(CIS)],
        note={"name": x("21 December 1991 · Alma-Ata", "டிசம்பர் 21, 1991 · அல்மா-அட்டா"), "date": x("Eleven republics join", "பதினொரு குடியரசுகள் இணைகின்றன"), "t": 1.0}), w=1)])
emit("C10", 4, [dict(type="gfx", html="gfx/datecard.html", d=3.2, data={"l1": x("25 December 1991", "25 டிசம்பர் 1991"), "l2": x("Moscow", "மாஸ்கோ")}),
     P("gorbachev_1987.jpg", w=1, kb=dict(z0=1.12, z1=1.0, fy=.4), ov=OV(lower=(x("Mikhail Gorbachev", "மிகைல் கோர்பச்சேவ்"), x("Resigns as President of the USSR", "சோவியத் ஒன்றிய அதிபர் பதவியிலிருந்து விலகுகிறார்"))))])
emit("C10", 5, [G("flagfade", dict(su="flag_su_img.png", caption=x("Moscow · 25 December 1991", "மாஸ்கோ · டிசம்பர் 25, 1991"), swap=None), w=1.7),
     card("bigtext", w=1.0, text="1922 – 1991", sub=x("After sixty-nine years", "அறுபத்தொன்பது ஆண்டுகளுக்குப் பிறகு"))])

# ================================================================= CHAPTER 11 – WHY DID IT FALL?
emit("C11", 1, [TITLE("C11"), card("list", w=1, title=x("Why did it fall?", "ஏன் வீழ்ந்தது?"), t0=1.2, step=3.0, gap=190, items=[x("The economy could not keep up", "பொருளாதாரம் ஈடுகொடுக்க முடியவில்லை"),
     x("Afghanistan and Chernobyl eroded trust", "ஆப்கானிஸ்தானும் செர்னோபிலும் நம்பிக்கையைத் தேய்த்தன")])])
emit("C11", 2, [card("list", w=1, title=x("More causes", "மேலும் காரணங்கள்"), t0=0.8, step=3.4, gap=190, items=[x("Nationalism: fifteen peoples", "தேசியவாதம்: பதினைந்து மக்கள்"),
     x("Leaders' choices: Gorbachev, Yeltsin", "தலைவர்களின் முடிவுகள்: கோர்பச்சேவ், யெல்ட்சின்"), x("No single cause", "ஒரே காரணம் இல்லை")])])
emit("C11", 3, [card("bigtext", w=1, text=x("How quickly it came", "எவ்வளவு வேகமாக வந்தது"), sub="1985 – 1991")])

# ================================================================= CHAPTER 12 – LEGACY
emit("C12", 1, [TITLE("C12"), G("map", dict(mapfile="map_data_full.js", caption=x("Fifteen new countries", "பதினைந்து புதிய நாடுகள்"), counter="", repcol="#3a3a44",
        paint=[{"k": k, "col": COLORS[k], "t": 0.6 + i * 0.3} for i, k in enumerate(["Russia", "Ukraine", "Belarus", "Estonia", "Latvia", "Lithuania", "Moldova", "Georgia", "Armenia", "Azerbaijan", "Kazakhstan", "Uzbekistan", "Turkmenistan", "Kyrgyzstan", "Tajikistan"])],
        texts=[dict(cent=k, text=CN(k), t=1.0 + i * 0.3, size=30) for i, k in enumerate(["Russia", "Ukraine", "Belarus", "Estonia", "Latvia", "Lithuania", "Moldova", "Georgia", "Armenia", "Azerbaijan", "Kazakhstan", "Uzbekistan", "Turkmenistan", "Kyrgyzstan", "Tajikistan"])]), w=1)])
emit("C12", 2, [card("list", w=1.1, title=x("The 1990s", "தொண்ணூறுகள்"), t0=0.8, step=2.8, gap=180, items=[x("New freedoms", "புதிய சுதந்திரங்கள்"), x("Hardship and inflation", "வறுமையும் பணவீக்கமும்"), x("Uncertainty", "நிச்சயமின்மை")]),
     V([SH("moscow1965", 8.0, 1.0, 60, .06), SH("mayday1961", 56.0, 1.0, 60, .06)], w=1.0)])
emit("C12", 3, [V([SH("kremlin1959", 14.0, 1.0, 60, .05), SH("mayday1961", 4.2, 1.0, 40, .06), SH("moscow1965", 84.2, 1.2, 50, .08)], w=1)])
S.append(dict(dur=4.5, type="gfx", html="gfx/cards.html", data={"kind": "end", "title": x("The Fall of the Soviet Union", "சோவியத் ஒன்றியத்தின் வீழ்ச்சி"), "sub": x("Thank you for watching", "பார்த்ததற்கு நன்றி"),
    "lines": [x("Archival footage: Universal Newsreel / US National Archives (public domain) · NASA", "ஆவணக் காட்சிகள்: யுனிவர்சல் நியூஸ்ரீல் / அமெரிக்கத் தேசிய ஆவணக் காப்பகம் (பொது உரிமை) · நாசா"),
              x("Photos: public-domain and Creative Commons images. Full credits in the description", "படங்கள்: பொது உரிமை மற்றும் கிரியேட்டிவ் காமன்ஸ் படங்கள். முழு விவரங்கள் விளக்கத்தில்"),
              x("Music: Kevin MacLeod (incompetech.com), CC BY 4.0 · Narration: AI-generated voice", "இசை: கெவின் மேக்லியோட் (incompetech.com), CC BY 4.0 · குரல்: செயற்கை நுண்ணறிவு")]}))

def freeze_time(s):
    h, d = s["html"], s["data"]
    if "cards" in h:
        k = d["kind"]
        if k == "list": return d.get("t0", 0.8) + (len(d["items"]) - 1) * d.get("step", 0.9) + 1.6
        if k == "definition": return 4.0
        if k == "bignum": return max([n.get("t", 1) for n in d["nums"]] + [0]) + 3.4
        if k == "person": return 3.0
        if k == "bigtext": return 3.4
        if k == "end": return 3.2
    if "timeline" in h:
        if d["mode"] == "bars": return d.get("t0", 0.6) + 1.5 * d.get("step", 0.7) + (len(d["items"]) - 1) * d.get("step", 0.7) + 1.6
        return max(max(i.get("t", 0) for i in d["items"]) + 1.2, 0.2 + d.get("sweep", 5) + 0.3)
    if "chart" in h: return max((d["annot"].get("t", 0) if d.get("annot") else 0) + 1.2, 0.5 + d.get("draw", 5) + 0.8)
    if "map" in h:
        t = [1.0]
        t += [o["t"] + 0.9 for o in d.get("paint", [])]; t += [o["t"] + 0.7 for o in d.get("texts", [])]
        if d.get("chain"): t.append(d["chain"].get("t", 1) + d["chain"].get("dur", 4) + 0.5)
        if d.get("note"): t.append(d["note"].get("t", 0.5) + 0.8)
        for o in d.get("stats", []): t.append(o["t"] + 1.0)
        F = d.get("focus")
        if F:
            t.append(F.get("t0", 0.5) + 1.0); t += [a["t"] + a.get("dur", 1.6) + 0.3 for a in F.get("arrows", [])]; t += [l["t"] + 0.7 for l in F.get("labels", [])]
        if d.get("order"):
            n = len([o for o in d["order"] if not o.get("stay")]); t.append(d.get("t0", 1.0) + n * d.get("step", 0.6) + 0.8)
        return max(t) + 0.6
    return None
# resolve any scene still carrying a callable 'data'
for s in S:
    if callable(s.get("data")): s["data"] = s["data"](s["dur"])
for s in S:
    if s["type"] == "gfx" and "flagfade" in s["html"]: s["data"].pop("swap", None)

for s in S:
    if s["type"] == "gfx" and any(k in s["html"] for k in ("cards", "timeline", "chart", "map")):
        ft = freeze_time(s)
        if ft is not None and ft < s["dur"] + 0.5 - 1.0: s["data"]["freeze"] = round(max(1.0, ft), 2)

sb = {"lang": lang, "root": ROOT, "fade": 0.5, "audio": f"audio/{lang}_full_mix.wav", "premixed": True, "scenes": S}
out = f"{ROOT}/build/sb_full_{lang}.json"; json.dump(sb, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
tot = sum(s["dur"] for s in S) + 0.5
print(out, "scenes", len(S), "video", f"{tot:.1f}s = {int(tot // 60)}:{int(tot % 60):02d}")
