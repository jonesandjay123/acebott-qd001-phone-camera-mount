# Stitches the render_v8.py output into docs/renders/v8/<view>.jpg (V8 alone) and
# docs/renders/v8/compare/<view>.jpg (V7 left | V8 right, labelled). Needs Pillow.   Run: python3 stitch_v7_v8.py
import os, glob
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("MOUNT_REPO") or os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "docs/renders/v8"); CMP = os.path.join(OUT, "compare")
try: font = ImageFont.truetype("DejaVuSans-Bold.ttf", 34)
except Exception: font = ImageFont.load_default(size=34)
views = sorted({os.path.basename(p)[:-7] for p in glob.glob(os.path.join(CMP, "*_V7.png"))})
for v in views:
    a = Image.open(os.path.join(CMP, f"{v}_V7.png")).convert("RGB"); b = Image.open(os.path.join(CMP, f"{v}_V8.png")).convert("RGB")
    b.save(os.path.join(OUT, f"{v}.jpg"), quality=90)
    gap = 12; im = Image.new("RGB", (a.width + b.width + gap, a.height), (255, 255, 255))
    im.paste(a, (0, 0)); im.paste(b, (a.width + gap, 0)); d = ImageDraw.Draw(im)
    for x, t in ((16, "V7  (printed)"), (a.width + gap + 16, "V8  (this build)")):
        d.rectangle((x - 8, 10, x + d.textlength(t, font=font) + 8, 56), fill=(255, 255, 255)); d.text((x, 14), t, fill=(30, 30, 30), font=font)
    im.save(os.path.join(CMP, f"{v}.jpg"), quality=88)
    os.remove(os.path.join(CMP, f"{v}_V7.png")); os.remove(os.path.join(CMP, f"{v}_V8.png"))
print("stitched", len(views), "views")
