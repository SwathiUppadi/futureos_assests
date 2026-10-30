import sys, os
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1350
NAVY = (27, 42, 74)
ORANGE = (232, 93, 38)
WHITE = (255, 255, 255)
MUTED = (190, 200, 220)
FD = "/usr/share/fonts/truetype/google-fonts/"

def font(name, size):
    for n in (name, "Poppins-Bold.ttf"):
        p = FD + n
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

BOLD = "Poppins-Bold.ttf"
SEMI = "Poppins-SemiBold.ttf"
REG = "Poppins-Regular.ttf"
MARGIN = 90

def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def draw_block(d, text, fnt, y, color=WHITE, gap=1.25, width=W - 2 * MARGIN):
    for line in wrap(d, text, fnt, width):
        d.text((MARGIN, y), line, font=fnt, fill=color)
        y += int(fnt.size * gap)
    return y

def base(n, total=6):
    im = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 14], fill=ORANGE)
    d.text((MARGIN, H - 110), "FutureOS", font=font(BOLD, 40), fill=WHITE)
    d.text((W - MARGIN - 90, H - 104), f"{n}/{total}", font=font(SEMI, 32), fill=MUTED)
    d.rectangle([MARGIN, H - 140, MARGIN + 80, H - 134], fill=ORANGE)
    return im, d

slides = []

# 1 cover
im, d = base(1)
d.rounded_rectangle([MARGIN, 150, MARGIN + 330, 218], radius=8, fill=ORANGE)
d.text((MARGIN + 28, 162), "AI Trend Alert", font=font(SEMI, 34), fill=WHITE)
y = 330
y = draw_block(d, "Europe just put", font(BOLD, 88), y)
y = draw_block(d, "€20M", font(BOLD, 150), y + 5, color=ORANGE, gap=1.1)
y = draw_block(d, "behind AI that helps doctors talk to patients", font(BOLD, 72), y + 10)
slides.append(im)

# 2 number
im, d = base(2)
d.text((MARGIN, 230), "€20M", font=font(BOLD, 260), fill=ORANGE)
draw_block(d, "The EU-funded ASCLEPIUS consortium is developing AI tools that support healthcare consultations.", font(SEMI, 54), 600)
slides.append(im)

# 3 what is
im, d = base(3)
y = draw_block(d, "What ASCLEPIUS is", font(BOLD, 84), 200, color=ORANGE)
y = draw_block(d, "An EU-funded consortium exploring how AI can support the conversation between healthcare professionals and patients.", font(SEMI, 52), y + 50)
draw_block(d, "Umeå University alone was awarded nearly €1M.", font(REG, 46), y + 50, color=MUTED)
slides.append(im)

# 4 where AI helps
im, d = base(4)
y = draw_block(d, "Where AI can help in a consultation", font(BOLD, 74), 190, color=ORANGE)
y += 40
steps = ["Patient interaction", "History taking", "Information synthesis", "Decision support", "Plan & follow-up"]
f = font(SEMI, 46)
for i, s in enumerate(steps):
    d.ellipse([MARGIN, y + 6, MARGIN + 62, y + 68], fill=ORANGE)
    d.text((MARGIN + 31, y + 37), str(i + 1), font=font(BOLD, 36), fill=WHITE, anchor="mm")
    d.text((MARGIN + 100, y + 8), s, font=f, fill=WHITE)
    y += 96
draw_block(d, "Some parts of this process can already be handled by current generative AI systems.", font(REG, 40), y + 30, color=MUTED)
slides.append(im)

# 5 open question
im, d = base(5)
y = draw_block(d, "The open question:", font(BOLD, 80), 270, color=ORANGE)
y = draw_block(d, "how to do it safely", font(BOLD, 96), y + 5)
draw_block(d, "Healthcare AI isn't only about diagnosis. Communication is a huge, under-built space.", font(SEMI, 48), y + 60, color=MUTED)
slides.append(im)

# 6 CTA
im, d = base(6)
y = draw_block(d, "Explore healthcare AI with", font(BOLD, 84), 340)
y = draw_block(d, "FutureOS", font(BOLD, 150), y + 5, color=ORANGE, gap=1.1)
y = draw_block(d, "Link in bio", font(SEMI, 60), y + 60)
d.text((MARGIN, y + 20), "Swipe for more  →", font=font(REG, 40), fill=MUTED)
slides.append(im)

for i, s in enumerate(slides, 1):
    s.save(os.path.join(OUT, f"slide-{i}.png"), optimize=True)
print("saved", len(slides))
