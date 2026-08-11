"""ChronoVerify app icon, 1024x1024, drawn at 4x and downsampled.

Brass magnifier with a verification check inside the lens, on the void-dark
brand background. Built for the AlternativeTo listing (128x128 minimum there);
the same file works anywhere a large square icon is needed.

Run:  python chronoverify_icon.py   ->  out/chronoverify-icon-1024.png
"""
from PIL import Image, ImageDraw, ImageFilter

S = 4                      # supersample factor
W = 1024 * S               # working canvas
BG_TOP, BG_BOT = (22, 22, 29), (10, 10, 15)          # #16161d -> #0A0A0F
BRASS_LIGHT = (232, 196, 122)                        # #e8c47a
BRASS_MID = (210, 162, 76)                           # #d2a24c (brand)
BRASS_DARK = (150, 106, 44)                          # #966a2c
LENS_FILL = (28, 28, 38)                             # #1c1c26
CHECK = (238, 208, 145)


def vgrad(size, top, bot):
    g = Image.linear_gradient("L").resize((size, size))
    a = Image.new("RGB", (size, size), top)
    b = Image.new("RGB", (size, size), bot)
    return Image.composite(b, a, g)


def brass(size, angle=35):
    g = Image.linear_gradient("L").rotate(angle, expand=False).resize((size, size))
    a = Image.new("RGB", (size, size), BRASS_LIGHT)
    b = Image.new("RGB", (size, size), BRASS_DARK)
    return Image.composite(b, a, g)


def rounded_mask(size, radius):
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
    return m


img = vgrad(W, BG_TOP, BG_BOT)

# soft brass glow behind the lens
glow = Image.new("L", (W, W), 0)
gd = ImageDraw.Draw(glow)
cx, cy, R = int(0.43 * W), int(0.43 * W), int(0.30 * W)
gd.ellipse([cx - R * 1.5, cy - R * 1.5, cx + R * 1.5, cy + R * 1.5], fill=26)
glow = glow.filter(ImageFilter.GaussianBlur(W // 14))
img = Image.composite(Image.new("RGB", (W, W), BRASS_MID), img, glow)

draw = ImageDraw.Draw(img)
ring_w = int(0.075 * W)

# handle: 45 degrees from ring edge toward bottom-right corner
hw = int(0.055 * W)
hx0 = cx + int((R - ring_w * 0.2) * 0.7071)
hy0 = cy + int((R - ring_w * 0.2) * 0.7071)
hx1, hy1 = int(0.80 * W), int(0.80 * W)
handle_mask = Image.new("L", (W, W), 0)
ImageDraw.Draw(handle_mask).line([hx0, hy0, hx1, hy1], fill=255, width=hw * 2)
ImageDraw.Draw(handle_mask).ellipse([hx1 - hw, hy1 - hw, hx1 + hw, hy1 + hw], fill=255)
img = Image.composite(brass(W, angle=65), img, handle_mask)

# lens interior
draw.ellipse([cx - R + ring_w // 2, cy - R + ring_w // 2,
              cx + R - ring_w // 2, cy + R - ring_w // 2], fill=LENS_FILL)

# ring (annulus) in brass gradient
ring_mask = Image.new("L", (W, W), 0)
rd = ImageDraw.Draw(ring_mask)
rd.ellipse([cx - R, cy - R, cx + R, cy + R], fill=255)
rd.ellipse([cx - R + ring_w, cy - R + ring_w, cx + R - ring_w, cy + R - ring_w], fill=0)
img = Image.composite(brass(W), img, ring_mask)

# faint highlight streak across the upper lens
streak = Image.new("L", (W, W), 0)
sd = ImageDraw.Draw(streak)
sd.ellipse([cx - int(R * 0.62), cy - int(R * 0.74), cx + int(R * 0.1), cy - int(R * 0.1)], fill=16)
streak = streak.filter(ImageFilter.GaussianBlur(W // 40))
inner = Image.new("L", (W, W), 0)
ImageDraw.Draw(inner).ellipse([cx - R + ring_w, cy - R + ring_w, cx + R - ring_w, cy + R - ring_w], fill=255)
streak = Image.composite(streak, Image.new("L", (W, W), 0), inner)
img = Image.composite(Image.new("RGB", (W, W), (255, 255, 255)), img, streak)

# checkmark inside the lens
ck_w = int(0.052 * W)
p1 = (cx - int(R * 0.42), cy + int(R * 0.02))
p2 = (cx - int(R * 0.10), cy + int(R * 0.34))
p3 = (cx + int(R * 0.48), cy - int(R * 0.30))
ck = Image.new("L", (W, W), 0)
cd = ImageDraw.Draw(ck)
cd.line([p1, p2, p3], fill=255, width=ck_w, joint="curve")
for p in (p1, p3):
    cd.ellipse([p[0] - ck_w // 2, p[1] - ck_w // 2, p[0] + ck_w // 2, p[1] + ck_w // 2], fill=255)
img = Image.composite(Image.new("RGB", (W, W), CHECK), img, ck)

# rounded-corner crop + hairline edge so it reads on dark UIs
radius = int(0.225 * W)
mask = rounded_mask(W, radius)
out = Image.new("RGBA", (W, W), (0, 0, 0, 0))
out.paste(img, (0, 0), mask)
edge = ImageDraw.Draw(out)
edge.rounded_rectangle([S, S, W - 1 - S, W - 1 - S], radius=radius,
                       outline=(255, 255, 255, 18), width=2 * S)

final = out.resize((1024, 1024), Image.LANCZOS)
final.save("out/chronoverify-icon-1024.png")
print("wrote out/chronoverify-icon-1024.png", final.size)
