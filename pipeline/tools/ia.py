#!/usr/bin/env python3
"""archive.org helper (public-domain footage).
  ia.py search "<lucene query>" [rows]     id | year | license | title
  ia.py info <id>                          files, sizes, description
  ia.py get <id> <outname>                 download the largest 4:3 .mp4 to footage/<outname>.mp4, log license to images/credits.csv"""
import csv, json, os, sys, time, urllib.error, urllib.parse, urllib.request
UA = {"User-Agent": "ussr-doc-video/1.0 (educational documentary; polite single-threaded fetcher)"}
HERE = os.path.dirname(os.path.abspath(__file__)); FOOT = os.path.join(HERE, "..", "footage"); CP = os.path.join(HERE, "..", "images", "credits.csv")

def jget(url):
    for k in range(6):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
        except urllib.error.HTTPError as e:
            if e.code in (429, 503): time.sleep(int(e.headers.get("Retry-After", 20)) + 2); continue
            raise

def pick(meta):
    mp4 = [f for f in meta["files"] if f["name"].lower().endswith(".mp4") and "512kb" not in f["name"].lower()]
    return max(mp4, key=lambda f: int(f.get("size", 0))) if mp4 else None

if sys.argv[1] == "search":
    d = jget("https://archive.org/advancedsearch.php?" + urllib.parse.urlencode({"q": sys.argv[2], "fl[]": ["identifier", "title", "year", "licenseurl"], "rows": sys.argv[3] if len(sys.argv) > 3 else 10, "output": "json"}, doseq=True))["response"]
    print("found", d["numFound"])
    for x in d["docs"]: print(f'{x["identifier"][:50]} | {x.get("year")} | {str(x.get("licenseurl"))[-22:]} | {str(x.get("title"))[:70]}')
elif sys.argv[1] == "info":
    m = jget(f"https://archive.org/metadata/{sys.argv[2]}"); print(m["metadata"].get("title"), "|", m["metadata"].get("licenseurl")); print(str(m["metadata"].get("description"))[:400])
    for f in m["files"]:
        if f["name"].lower().endswith((".mp4", ".mpg", ".ogv")): print(" ", f["name"], f.get("width"), "x", f.get("height"), f.get("length"), "s", round(int(f.get("size", 0)) / 1e6, 1), "MB")
else:
    iid, out = sys.argv[2], sys.argv[3]; m = jget(f"https://archive.org/metadata/{iid}"); f = pick(m)
    url = f"https://archive.org/download/{iid}/" + urllib.parse.quote(f["name"]); os.makedirs(FOOT, exist_ok=True); path = os.path.join(FOOT, out + ".mp4")
    for k in range(6):
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300).read(); break
        except urllib.error.HTTPError as e:
            if e.code in (429, 503): time.sleep(int(e.headers.get("Retry-After", 30)) + 2); continue
            raise
    open(path, "wb").write(data)
    md = m["metadata"]; new = not os.path.exists(CP)
    with open(CP, "a", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        if new: w.writerow(["file", "title", "author", "license", "source_url"])
        w.writerow([out + ".mp4", md.get("title", ""), str(md.get("creator") or md.get("collection", "")), md.get("licenseurl", "public domain (archive.org)"), f"https://archive.org/details/{iid}"])
    print(f"saved {out}.mp4 {len(data)/1e6:.1f}MB {f.get('width')}x{f.get('height')} {f.get('length')}s lic={md.get('licenseurl')}")
