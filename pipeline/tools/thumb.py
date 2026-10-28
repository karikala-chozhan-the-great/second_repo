# -*- coding: utf-8 -*-
"""1280x720 thumbnails (en + ta) from a newsreel frame + flag + title text.   thumb.py"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps, ImageFilter
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", "4.2", "-i", f"{R}/footage/mayday1961.mp4", "-frames:v", "1", f"{R}/build/thumb_src.png"], check=True)
src = Image.open(f"{R}/build/thumb_src.png").convert("L").crop((0, 40, 640, 400)).resize((1280, 720), Image.LANCZOS)
src = ImageEnhance.Contrast(ImageOps.autocontrast(src, cutoff=1)).enhance(1.25)
bg = ImageOps.colorize(src, black=(10, 8, 8), white=(236, 222, 196), mid=(120, 96, 80)).convert("RGBA")
# dark gradient from the left so text reads, plus vignette
g = Image.new("L", (1280, 720)); gd = ImageDraw.Draw(g)
for x in range(1280): gd.line([(x, 0), (x, 720)], fill=int(235 * max(0, 1 - x / 1000) ** 1.3))
bg.paste(Image.new("RGBA", (1280, 720), (8, 4, 6, 255)), (0, 0), g)
flag = Image.open(f"{R}/images/flag_su.png").convert("RGBA").resize((360, 180), Image.LANCZOS)
def font(path, size): return ImageFont.truetype(path, size)
NB = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"; NT = "/usr/share/fonts/truetype/noto/NotoSansTamil-Bold.ttf"
def draw(lines, name):
    im = bg.copy(); d = ImageDraw.Draw(im)
    im.paste(flag, (860, 60), flag); d.rectangle([860, 60, 1220, 240], outline=(255, 255, 255, 200), width=4)
    d.rectangle([60, 120, 76, 600], fill=(200, 16, 46, 255))
    y = 120
    for txt, size, col, fnt in lines:
        f = font(fnt, size); d.text((110, y), txt, font=f, fill=col, stroke_width=5, stroke_fill=(0, 0, 0, 255)); y += int(size * 1.28)
    im.convert("RGB").save(f"{R}/out/{name}", quality=92); print("wrote", name)
W_, G_ = (255, 255, 255, 255), (232, 185, 35, 255)
draw([("THE FALL OF THE", 84, W_, NB), ("SOVIET UNION", 142, G_, NB), ("1985 – 1991", 74, W_, NB)], "thumbnail_en.jpg")
draw([("சோவியத்", 112, G_, NT), ("ஒன்றியத்தின்", 112, G_, NT), ("வீழ்ச்சி", 150, W_, NT), ("1985 – 1991", 64, W_, NB)], "thumbnail_ta.jpg")
