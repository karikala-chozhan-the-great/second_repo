# The Fall of the Soviet Union — documentary (English + Tamil)

A ~15-minute documentary about the collapse of the USSR (1985–1991), produced in two languages for two YouTube channels.
Narration is AI-generated (Gemini text-to-speech, voice *Alnilam*); everything else is assembled from public-domain and
Creative-Commons material with ffmpeg and a headless-Chromium graphics renderer.

| | English | Tamil |
|---|---|---|
| Video | `videos/en/` | `videos/ta/` |
| Narration script | `scripts/narration_en.txt` | `scripts/narration_ta.txt` |
| Credits, YouTube description, chapter timestamps | `metadata/en/` | `metadata/ta/` |

Video files are stored with **Git LFS** (`git lfs install` before cloning, or `git lfs pull` afterwards).

## Read this before publishing
- **Tamil narration has not been reviewed by a native speaker.** An automatic transcribe-back check measured clarity only
  (differences were spelling/sandhi variants), not naturalness.
- **No free footage of the 1985–1991 events exists in the sources used.** Archival clips are 1950s–60s public-domain
  newsreels, labelled "Archival footage" on screen. Chapters about 1985–1991 use maps (modern borders), charts, timelines and still photos.
- **Disclosures:** the narration is a synthetic voice; check YouTube's current rules on disclosing synthetic content and
  Google's terms for generated audio. Music is Kevin MacLeod, CC BY 4.0 — the credit line must go in the description
  (`metadata/*/CREDITS.md`). The Chernobyl reactor photo is CC BY-SA 4.0 (Mattias Hill).
- Figures: Soviet losses in Afghanistan (~15,000), Baltic Way (~675 km, ~2 million people), the 17 March 1991 referendum (~76% yes,
  six republics did not take part) and the oil-price chart (approximate US crude prices) were checked against web sources; the exact clock time of the flag lowering is not stated.

## How it was built (`pipeline/`)
1. `script/full.py` (+ `ta_override.py`) holds the paired English/Tamil segments and writes the narration text and `chapters.json`.
2. `tools/seg_narrate.py` narrates each segment (`tools/narrate.py` is the Gemini TTS client from the `narration-tools` plugin; it reads the key from `GOOGLE_API_KEY` or `key`),
   `tools/retime.py` + `tools/join.py` build timings and the joined track, `tools/verify_all.py` transcribes it back for a clarity check,
   `tools/mix.py` mixes a quiet, ducked music bed.
3. `tools/ia.py` downloads public-domain footage from archive.org; `tools/clip.py` grades and cuts newsreel montages; `tools/kb.py` does Ken Burns on stills.
4. `gfx/*.html` are the animated scenes (maps, charts, timelines, cards) rendered frame by frame by `gfx/render.js` (Playwright/Chromium).
   Map data is generated with `gfx/node/mkmap.js` (`npm install` in `gfx/node`, then see its header for arguments).
5. `tools/sb_full.py <en|ta>` turns segment timings into a storyboard; `tools/compose.py` renders the scenes, joins them with crossfades and muxes the audio.
   `tools/deliver.py` writes credits, description and chapter timestamps.

Source footage and images are not stored here (they are public and re-downloadable); `metadata/credits_all_assets.csv` lists every asset with its licence and URL.
