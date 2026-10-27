# -*- coding: utf-8 -*-
"""Write the delivery text files for one language.   deliver.py en|ta   ->  out/<lang>/{CREDITS.md, DESCRIPTION.md, chapters.txt}
Credits cover only the assets that actually appear in that language's storyboard."""
import csv, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lang = sys.argv[1]; I = 0 if lang == "en" else 1
x = lambda en, ta: en if I == 0 else ta
sb = json.load(open(f"{ROOT}/build/sb_full_{lang}.json", encoding="utf-8")); CH = json.load(open(f"{ROOT}/script/chapters.json", encoding="utf-8"))
T = json.load(open(f"{ROOT}/audio/{lang}_full/timings.json", encoding="utf-8"))
os.makedirs(f"{ROOT}/out/{lang}", exist_ok=True)

# ---- which files are used
blob = json.dumps(sb, ensure_ascii=False)
used = sorted(set(re.findall(r'(?:images|footage)/([A-Za-z0-9_\-]+\.(?:jpg|png|mp4))', blob)))
rows = {r["file"]: r for r in csv.DictReader(open(f"{ROOT}/images/credits.csv", encoding="utf-8"))}
SRC = {"universal_newsreels": "Universal Newsreel collection, US National Archives (via the Internet Archive)"}
lines = []
for f in used:
    r = rows.get(f)
    if not r: print("no credit row for", f); continue
    title = re.sub(r"^File:", "", r["title"]); lic = r["license"]
    author = r["author"]
    if f.endswith(".mp4"): author = SRC["universal_newsreels"]; lic = "Public domain"
    lines.append(f"- **{title}** — {author or 'unknown'} — {lic} — {r['source_url']}")
music = [("Gathering Darkness", "Gathering_Darkness"), ("Echoes of Time v2", "Echoes_of_Time_v2"), ("Ossuary 5 - Rest", "Ossuary_5__Rest"), ("Long Time Coming", "Long_Time_Coming")]
mlines = [f'- "{t}" by Kevin MacLeod (incompetech.com) — Licensed under Creative Commons: By Attribution 4.0 — http://creativecommons.org/licenses/by/4.0/' for t, _ in music]
extra = ["- Maps: Natural Earth data (public domain) via the `world-atlas` package; modern borders are shown on all maps.",
         "- Soviet flag: public-domain image (Wikimedia Commons). Russian flag: flag-icons (MIT).",
         "- Fonts: Noto Sans and Noto Sans Tamil (SIL Open Font License)."]

# ---- chapter timestamps (video time = sum of scene lengths before the chapter's first segment)
L = {t["seg"]: t["dur"] + 0.5 for t in T}
start, chapters = 0.0, []
first = {}
for s in CH["segments"]:
    if s["local"] == 1: first[s["chapter"]] = s["seg"]
def ts(sec): sec = int(round(sec)); return f"{sec // 60}:{sec % 60:02d}"
for c in CH["chapters"]:
    t0 = sum(L[i] for i in range(1, first[c["id"]]))
    chapters.append((ts(t0), x(c["en"], c["ta"])))
total = sum(s["dur"] for s in sb["scenes"]) + 0.5
open(f"{ROOT}/out/{lang}/chapters.txt", "w", encoding="utf-8").write("\n".join(f"{a} {b}" for a, b in chapters) + "\n")

disc = x("This video uses an AI-generated (synthetic) narration voice. Archival clips are labelled “Archival footage” and come from public-domain newsreels of earlier decades (1950s–60s); no free footage exists of the 1985–1991 events themselves, so those chapters use maps, charts, timelines and still photographs.",
         "இந்த வீடியோவில் செயற்கை நுண்ணறிவு (AI) உருவாக்கிய குரல் பயன்படுத்தப்பட்டுள்ளது. “ஆவணக் காட்சிகள்” எனக் குறிக்கப்பட்ட காணொளிகள் முந்தைய பத்தாண்டுகளின் (1950–60கள்) பொது உரிமைச் செய்திப்படங்கள்; 1985–1991 நிகழ்வுகளுக்கு இலவசமாகப் பயன்படுத்தக்கூடிய காட்சிகள் இல்லாததால், அந்தப் பகுதிகளில் வரைபடங்கள், விளக்கப்படங்கள், காலவரிசைகள், புகைப்படங்கள் பயன்படுத்தப்பட்டுள்ளன.")
credits = [f"# {x('Credits and licences', 'மூலங்களும் உரிமங்களும்')} — {x('The Fall of the Soviet Union', 'சோவியத் ஒன்றியத்தின் வீழ்ச்சி')}", "",
           "## " + x("Footage and images used in this video", "இந்த வீடியோவில் பயன்படுத்தப்பட்ட காட்சிகளும் படங்களும்"), *lines, "", "## " + x("Music", "இசை"), *mlines, "", "## " + x("Other", "மற்றவை"), *extra, "",
           "## " + x("Notes", "குறிப்புகள்"), "- " + disc,
           "- " + x("The Chernobyl reactor photograph is CC BY-SA 4.0 (Mattias Hill): keep the attribution above in the description. Please check YouTube's current rules on disclosing synthetic or altered content when you upload.",
                   "செர்னோபில் உலைப் புகைப்படம் CC BY-SA 4.0 (மேட்டியாஸ் ஹில்) உரிமம் கொண்டது: மேலே உள்ள பெயர் குறிப்பை விளக்கத்தில் வைத்திருங்கள். பதிவேற்றும்போது செயற்கை உள்ளடக்கம் குறித்த YouTube-இன் தற்போதைய விதிகளைச் சரிபார்க்கவும்."), ""]
open(f"{ROOT}/out/{lang}/CREDITS.md", "w", encoding="utf-8").write("\n".join(credits))

title = x("The Fall of the Soviet Union (1985–1991) | How a Superpower Ended", "சோவியத் ஒன்றியத்தின் வீழ்ச்சி (1985–1991) | ஒரு வல்லரசு எப்படி முடிவுக்கு வந்தது")
intro = x("On 25 December 1991 the Soviet flag came down over the Kremlin. In about fifteen minutes, this documentary follows the road to that evening: the stagnation of the Brezhnev years, Gorbachev's glasnost and perestroika, the oil-price collapse, the war in Afghanistan, Chernobyl, the Baltic Way, the fall of the Berlin Wall, the August 1991 coup, the Belovezha Accords, and the end of the Soviet Union.",
          "ஆயிரத்து தொள்ளாயிரத்து தொண்ணூற்றொன்று டிசம்பர் 25 அன்று கிரெம்ளின் மீதிருந்த சோவியத் கொடி இறக்கப்பட்டது. அந்த மாலைக்கு இட்டுச்சென்ற பாதையை சுமார் பதினைந்து நிமிடங்களில் இந்த ஆவணப்படம் விளக்குகிறது: பிரெஷ்நேவ் காலத் தேக்கம், கோர்பச்சேவின் கிளாஸ்நோஸ்ட், பெரெஸ்ட்ரோயிகா, எண்ணெய் விலைச் சரிவு, ஆப்கானிஸ்தான் போர், செர்னோபில், பால்டிக் பாதை, பெர்லின் சுவரின் வீழ்ச்சி, 1991 ஆகஸ்ட் சதி, பெலோவேஷ் ஒப்பந்தம், சோவியத் ஒன்றியத்தின் முடிவு.")
tags = x("Soviet Union, USSR, fall of the Soviet Union, Gorbachev, Yeltsin, Cold War, glasnost, perestroika, Chernobyl, Berlin Wall, history documentary, 1991, Russia history",
         "சோவியத் ஒன்றியம், சோவியத் வீழ்ச்சி, கோர்பச்சேவ், யெல்ட்சின், பனிப்போர், செர்னோபில், பெர்லின் சுவர், வரலாறு, ஆவணப்படம், ரஷ்ய வரலாறு")
desc = [f"TITLE: {title}", "", intro, "", x("CHAPTERS", "அத்தியாயங்கள்"), *[f"{a} {b}" for a, b in chapters], "", disc, "", x("Credits (also in CREDITS.md):", "மூலங்கள் (CREDITS.md-இலும்):"),
        *lines, *mlines, *extra, "", "TAGS: " + tags, ""]
open(f"{ROOT}/out/{lang}/DESCRIPTION.md", "w", encoding="utf-8").write("\n".join(desc))
print(lang, "files used:", len(used), "| video length", ts(total), "| chapters:", len(chapters))
