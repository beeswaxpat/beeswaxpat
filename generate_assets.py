"""
Beeswax Pat - X/Twitter Profile Assets
PFP: Sentinel Eye (Terminator T-800 inspired)
Banner: Blade Runner Tokyo cityscape with ANSI Shadow BEESWAX PAT wordmark only
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import math
import random
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Palette ---
NEON_CYAN = (0, 230, 255)
NEON_MAGENTA = (255, 50, 120)
NEON_HOTPINK = (255, 80, 200)
NEON_AMBER = (255, 152, 0)
NEON_PURPLE = (180, 100, 255)
NEON_RED = (255, 40, 40)
DARK_BASE = (8, 8, 18)
DARK_BLUE = (12, 15, 35)
DARK_PURPLE = (24, 12, 36)
WHITE = (255, 255, 255)

# --- Fonts (Windows native) ---
FONT_MONO = "C:\\Windows\\Fonts\\consola.ttf"
FONT_MONO_BOLD = "C:\\Windows\\Fonts\\consolab.ttf"
FONT_DISPLAY = "C:\\Windows\\Fonts\\segoeuib.ttf"
FONT_HEAVY = "C:\\Windows\\Fonts\\segoeuiz.ttf"

# Japanese font candidates (fall back gracefully)
JP_FONT_CANDIDATES = [
    "C:\\Windows\\Fonts\\YuGothB.ttc",
    "C:\\Windows\\Fonts\\YuGothM.ttc",
    "C:\\Windows\\Fonts\\msgothic.ttc",
    "C:\\Windows\\Fonts\\meiryob.ttc",
]


def load_jp_font(size):
    for path in JP_FONT_CANDIDATES:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.truetype(FONT_MONO_BOLD, size)


# --- ANSI Shadow art (from beeswaxpat/banner.svg) ---
ASCII_ART = [
    "██████╗ ███████╗███████╗███████╗██╗    ██╗ █████╗ ██╗  ██╗    ██████╗  █████╗ ████████╗",
    "██╔══██╗██╔════╝██╔════╝██╔════╝██║    ██║██╔══██╗╚██╗██╔╝    ██╔══██╗██╔══██╗╚══██╔══╝",
    "██████╔╝█████╗  █████╗  ███████╗██║ █╗ ██║███████║ ╚███╔╝     ██████╔╝███████║   ██║   ",
    "██╔══██╗██╔══╝  ██╔══╝  ╚════██║██║███╗██║██╔══██║ ██╔██╗     ██╔═══╝ ██╔══██║   ██║   ",
    "██████╔╝███████╗███████║███████║╚███╔███╔╝██║  ██║██╔╝ ██╗    ██║     ██║  ██║   ██║   ",
    "╚═════╝ ╚══════╝╚══════╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝   ╚═╝   ",
]

KATAKANA = list("アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボ")

# Vertical neon signs — coherent Beeswax-Pat / agentic-themed words in katakana
# Full unabbreviated words. Each renders top-to-bottom on a tall building.
# The selection algorithm picks the longest word that fits each tower's height.
VERTICAL_SIGN_WORDS = [
    "オーパス",                    # OPUS (4)
    "ミソス",                      # MYTHOS (3)
    "クロード",                    # CLAUDE (4)
    "エージェント",                # AGENT (5)
    "コード",                      # CODE (3)
    "マインド",                    # MIND (4)
    "ニューラル",                  # NEURAL (5)
    "データ",                      # DATA (3)
    "システム",                    # SYSTEM (4)
    "マトリックス",                # MATRIX (6)
    "アンドロイド",                # ANDROID (6)
    "スカイネット",                # SKYNET (6)
    "ビーズワックス",              # BEESWAX (7)
    "サイバー",                    # CYBER (4)
    "コンシャスネス",              # CONSCIOUSNESS (7)
    "トランスディメンショナル",    # TRANSDIMENSIONAL (12)
    "ディメンション",              # DIMENSION (7)
    "シンギュラリティ",            # SINGULARITY (8)
    "スーン",                      # SOON (3)
    "ニューロ",                    # NEURO (4)
    "アルゴリズム",                # ALGORITHM (6)
    "ターミネーター",              # TERMINATOR (7)
]

# Featured billboard phrases — full unabbreviated statements
BILLBOARD_TEXTS = [
    "AGI スーン",                  # AGI SOON
    "オーパス 4.7",                # OPUS 4.7
    "クロード",                    # CLAUDE
    "エージェント",                # AGENT
    "ビーズワックス",              # BEESWAX
    "コンシャスネス",              # CONSCIOUSNESS
    "シンギュラリティ",            # SINGULARITY
    "ニューラル",                  # NEURAL
    "コード",                      # CODE
    "AGI",
    "マインド",                    # MIND
]


# ===== Helpers =====

def lerp(c1, c2, t):
    t = max(0, min(1, t))
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(len(c1)))


def draw_neon_text(img, text, x, y, font, color, glow_radius=12, glow_alpha=80):
    W, H = img.size
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow, "RGBA").text((x, y), text, font=font, fill=(*color, glow_alpha))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=glow_radius))
    img = Image.alpha_composite(img, glow)

    glow2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow2, "RGBA").text((x, y), text, font=font, fill=(*color, min(255, glow_alpha + 40)))
    glow2 = glow2.filter(ImageFilter.GaussianBlur(radius=max(1, glow_radius // 3)))
    img = Image.alpha_composite(img, glow2)

    sharp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    core = lerp(color, WHITE, 0.6)
    ImageDraw.Draw(sharp, "RGBA").text((x, y), text, font=font, fill=(*core, 255))
    img = Image.alpha_composite(img, sharp)
    return img


def draw_chromatic_text(img, text, x, y, font, glow_radius=8, offset=3):
    img = draw_neon_text(img, text, x + offset, y, font, NEON_CYAN, glow_radius=glow_radius, glow_alpha=70)
    img = draw_neon_text(img, text, x - offset, y, font, NEON_MAGENTA, glow_radius=glow_radius, glow_alpha=70)
    W, H = img.size
    sharp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sharp, "RGBA").text((x, y), text, font=font, fill=(*WHITE, 250))
    img = Image.alpha_composite(img, sharp)
    return img


def draw_scanlines(draw, w, h, gap=3, alpha=14):
    for y in range(0, h, gap):
        draw.line([(0, y), (w, y)], fill=(0, 0, 0, alpha), width=1)


def draw_rain(draw, w, h, density=350, color=NEON_CYAN, alpha_range=(6, 20)):
    for _ in range(density):
        rx = random.randint(0, w)
        ry = random.randint(0, h)
        length = random.randint(8, 30)
        a = random.randint(*alpha_range)
        draw.line([(rx, ry), (rx, ry + length)], fill=(*color[:3], a), width=1)


def draw_vignette(img, strength=80, depth=50):
    W, H = img.size
    vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vig, "RGBA")
    for band in range(strength):
        a = int(depth * (1 - band / strength) ** 2)
        if a > 0:
            vd.line([(0, band), (W, band)], fill=(0, 0, 0, a))
            vd.line([(0, H - 1 - band), (W, H - 1 - band)], fill=(0, 0, 0, a))
            vd.line([(band, 0), (band, H)], fill=(0, 0, 0, a))
            vd.line([(W - 1 - band, 0), (W - 1 - band, H)], fill=(0, 0, 0, a))
    return Image.alpha_composite(img, vig)


def draw_grain(img, density=2000, alpha_range=(3, 12)):
    W, H = img.size
    grain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    grd = ImageDraw.Draw(grain, "RGBA")
    for _ in range(density):
        gx = random.randint(0, W - 1)
        gy = random.randint(0, H - 1)
        ga = random.randint(*alpha_range)
        grd.point((gx, gy), fill=(255, 255, 255, ga))
    return Image.alpha_composite(img, grain)


# ===== PFP: Sentinel Eye (T-800 homage) =====

def generate_pfp():
    print("Generating PFP — Sentinel Eye (Terminator T-800 homage)...")
    random.seed(7)
    W, H = 1024, 1024
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    cx, cy = W // 2, H // 2

    # 1. Subtle red atmospheric haze
    bg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bgd = ImageDraw.Draw(bg, "RGBA")
    for r in range(W // 2, 0, -10):
        t = 1 - r / (W // 2)
        bgd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(25, 5, 5, int(45 * t)))
    bg = bg.filter(ImageFilter.GaussianBlur(radius=80))
    img = Image.alpha_composite(img, bg)

    # 2. Wide red eye glow emanation
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_layer, "RGBA")
    for r in range(int(W * 0.50), 0, -3):
        t = 1 - r / (W * 0.50)
        a = int(180 * t ** 1.8)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 25, 25, a))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=50))
    img = Image.alpha_composite(img, glow_layer)

    # 3. Outer chrome bezel ring with vertical lighting (lit from above)
    bezel_outer = int(W * 0.46)
    bezel_inner = int(W * 0.32)

    chrome = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    chrome_draw = ImageDraw.Draw(chrome, "RGBA")
    # Pie slices around the ring, color based on angle (lit from top)
    n_slices = 144
    for i in range(n_slices):
        start_deg = i * (360 / n_slices)
        end_deg = start_deg + (360 / n_slices) + 0.5  # slight overlap to avoid seams
        mid_angle = math.radians(start_deg + 360 / n_slices / 2)
        # PIL angles: 0 = east, 90 = south. So vertical position uses sin(angle).
        # We want bright on top (angle ~270°, sin = -1) and dark on bottom (angle ~90°, sin = +1)
        vert = math.sin(mid_angle)
        brightness = 0.5 - 0.5 * vert  # 1.0 at top, 0.0 at bottom
        brightness = brightness ** 1.5
        chrome_col = lerp((20, 22, 28), (220, 225, 235), brightness)
        chrome_draw.pieslice(
            [cx - bezel_outer, cy - bezel_outer, cx + bezel_outer, cy + bezel_outer],
            start=start_deg, end=end_deg, fill=(*chrome_col, 255))
    # Cut out the inner area (so chrome is just the ring)
    cutout = Image.new("L", (W, H), 255)
    ImageDraw.Draw(cutout).ellipse(
        [cx - bezel_inner, cy - bezel_inner, cx + bezel_inner, cy + bezel_inner], fill=0)
    r_, g_, b_, a_ = chrome.split()
    chrome = Image.merge("RGBA", (r_, g_, b_, ImageChops.multiply(a_, cutout)))
    img = Image.alpha_composite(img, chrome)

    # 4. Inner shadow ring (separating chrome from iris)
    shadow_ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow_ring, "RGBA").ellipse(
        [cx - bezel_inner, cy - bezel_inner, cx + bezel_inner, cy + bezel_inner],
        outline=(0, 0, 0, 220), width=8)
    shadow_ring = shadow_ring.filter(ImageFilter.GaussianBlur(radius=3))
    img = Image.alpha_composite(img, shadow_ring)

    # 5. Inner iris area — dark recessed
    iris_outer = bezel_inner - 6
    iris_recess = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(iris_recess, "RGBA").ellipse(
        [cx - iris_outer, cy - iris_outer, cx + iris_outer, cy + iris_outer],
        fill=(12, 6, 6, 255))
    img = Image.alpha_composite(img, iris_recess)

    # 6. Mechanical aperture blades
    iris_inner = int(W * 0.13)
    blade_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bld = ImageDraw.Draw(blade_layer, "RGBA")
    n_blades = 8
    blade_offset = math.radians(22.5)
    for i in range(n_blades):
        angle = i * (2 * math.pi / n_blades) + blade_offset
        a1 = angle - math.pi / n_blades * 0.85
        a2 = angle + math.pi / n_blades * 0.85
        # Outer points (touch the chrome shadow ring)
        p1 = (cx + int(iris_outer * math.cos(a1)), cy + int(iris_outer * math.sin(a1)))
        p2 = (cx + int(iris_outer * math.cos(a2)), cy + int(iris_outer * math.sin(a2)))
        # Inner point (offset to one side for asymmetric overlap look)
        inner_angle = angle + math.radians(8)
        p3 = (cx + int(iris_inner * math.cos(inner_angle)),
              cy + int(iris_inner * math.sin(inner_angle)))
        # Shading per blade
        vert = math.sin(angle)
        brightness = 0.5 - 0.5 * vert
        brightness = brightness ** 1.4
        col = lerp((30, 35, 42), (155, 165, 180), brightness)
        bld.polygon([p1, p2, p3], fill=(*col, 235))
        # Blade edge highlight
        bld.line([p2, p3], fill=(*lerp(col, WHITE, 0.4), 200), width=1)
        # Blade shadow edge
        bld.line([p1, p3], fill=(0, 0, 0, 180), width=1)
    img = Image.alpha_composite(img, blade_layer)

    # 7. Bright red iris glow ring (around the inner core)
    red_glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rgd = ImageDraw.Draw(red_glow, "RGBA")
    glow_outer_r = iris_inner + 22
    glow_inner_r = iris_inner - 4
    for r in range(glow_outer_r, glow_inner_r, -1):
        t = (glow_outer_r - r) / (glow_outer_r - glow_inner_r)
        a = int(220 * (1 - abs(t - 0.5) * 2))
        if a > 0:
            rgd.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 30, 30, a), width=2)
    red_glow = red_glow.filter(ImageFilter.GaussianBlur(radius=6))
    img = Image.alpha_composite(img, red_glow)

    # Sharp red inner ring
    sharp_red = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sharp_red, "RGBA").ellipse(
        [cx - iris_inner, cy - iris_inner, cx + iris_inner, cy + iris_inner],
        outline=(255, 70, 70, 255), width=4)
    img = Image.alpha_composite(img, sharp_red)

    # 8. Black pupil interior
    pupil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(pupil, "RGBA").ellipse(
        [cx - iris_inner + 4, cy - iris_inner + 4,
         cx + iris_inner - 4, cy + iris_inner - 4],
        fill=(0, 0, 0, 255))
    img = Image.alpha_composite(img, pupil)

    # 9. Bright red core glow (the LED itself)
    core_r = int(iris_inner * 0.4)
    core_glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cgd = ImageDraw.Draw(core_glow, "RGBA")
    for r in range(core_r + 50, 0, -1):
        a = int(255 * (1 - r / (core_r + 50)) ** 2.2)
        if a > 0:
            cgd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 60, 60, a))
    core_glow = core_glow.filter(ImageFilter.GaussianBlur(radius=10))
    img = Image.alpha_composite(img, core_glow)

    # 10. Solid bright red core with white-hot center
    core = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(core, "RGBA")
    cd.ellipse([cx - core_r, cy - core_r, cx + core_r, cy + core_r],
               fill=(255, 110, 110, 255))
    inner_r = core_r // 2
    cd.ellipse([cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r],
               fill=(255, 200, 200, 255))
    cd.ellipse([cx - inner_r // 2, cy - inner_r // 2,
                cx + inner_r // 2, cy + inner_r // 2],
               fill=(255, 250, 250, 255))
    img = Image.alpha_composite(img, core)

    # 11. Hex bolts on the chrome bezel (8 bolts, 45° apart)
    bolt_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bod = ImageDraw.Draw(bolt_layer, "RGBA")
    bolt_r = int((bezel_outer + bezel_inner) / 2)
    bolt_size = 14
    for i in range(8):
        angle = i * math.pi / 4 + math.pi / 8
        bx = cx + int(bolt_r * math.cos(angle))
        by = cy + int(bolt_r * math.sin(angle))
        # Hex bolt
        vert = math.sin(angle)
        brightness = 0.5 - 0.5 * vert
        bolt_col = lerp((25, 27, 33), (180, 185, 195), brightness ** 1.3)
        # Hex shape (6 points)
        hex_pts = []
        for k in range(6):
            ha = k * math.pi / 3
            hex_pts.append((bx + int(bolt_size * math.cos(ha)),
                            by + int(bolt_size * math.sin(ha))))
        bod.polygon(hex_pts, fill=(*bolt_col, 255), outline=(10, 10, 14, 255))
        # Inner indent
        inner_hex = []
        for k in range(6):
            ha = k * math.pi / 3
            inner_hex.append((bx + int(bolt_size * 0.6 * math.cos(ha)),
                              by + int(bolt_size * 0.6 * math.sin(ha))))
        bod.polygon(inner_hex, fill=(0, 0, 0, 180))
    img = Image.alpha_composite(img, bolt_layer)

    # 12. Battle damage scratches across chrome
    scratch = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scratch, "RGBA")
    for _ in range(20):
        angle = random.uniform(0, 2 * math.pi)
        r1 = random.randint(bezel_inner + 8, bezel_outer - 8)
        r2 = r1 + random.randint(-25, 25)
        a_off = random.uniform(-0.06, 0.06)
        x1 = cx + int(r1 * math.cos(angle))
        y1 = cy + int(r1 * math.sin(angle))
        x2 = cx + int(r2 * math.cos(angle + a_off))
        y2 = cy + int(r2 * math.sin(angle + a_off))
        sd.line([(x1, y1), (x2, y2)],
                fill=(230, 230, 235, random.randint(60, 130)), width=1)
    # Also some dark scratches/dings
    for _ in range(10):
        angle = random.uniform(0, 2 * math.pi)
        r = random.randint(bezel_inner + 10, bezel_outer - 10)
        x = cx + int(r * math.cos(angle))
        y = cy + int(r * math.sin(angle))
        size = random.randint(2, 5)
        sd.ellipse([x - size, y - size, x + size, y + size], fill=(0, 0, 0, 140))
    img = Image.alpha_composite(img, scratch)

    # 13. HUD targeting elements
    hud = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hud, "RGBA")
    bracket_size = 70
    bracket_w = 4
    margin = 70
    red = (255, 50, 50, 220)
    # Top-left
    hd.line([(margin, margin), (margin + bracket_size, margin)], fill=red, width=bracket_w)
    hd.line([(margin, margin), (margin, margin + bracket_size)], fill=red, width=bracket_w)
    # Top-right
    hd.line([(W - margin - bracket_size, margin), (W - margin, margin)], fill=red, width=bracket_w)
    hd.line([(W - margin, margin), (W - margin, margin + bracket_size)], fill=red, width=bracket_w)
    # Bottom-left
    hd.line([(margin, H - margin), (margin + bracket_size, H - margin)], fill=red, width=bracket_w)
    hd.line([(margin, H - margin - bracket_size), (margin, H - margin)], fill=red, width=bracket_w)
    # Bottom-right
    hd.line([(W - margin - bracket_size, H - margin), (W - margin, H - margin)], fill=red, width=bracket_w)
    hd.line([(W - margin, H - margin - bracket_size), (W - margin, H - margin)], fill=red, width=bracket_w)

    # HUD text labels
    hud_font = ImageFont.truetype(FONT_MONO_BOLD, 18)
    hud_small = ImageFont.truetype(FONT_MONO_BOLD, 14)
    hd.text((margin + 10, margin + 80), "T-800", font=hud_font, fill=(255, 60, 60, 230))
    hd.text((margin + 10, margin + 100), "[ACTIVE]", font=hud_small, fill=(255, 60, 60, 200))
    hd.text((margin + 10, margin + 118), "AGENTIC.SYS", font=hud_small, fill=(255, 60, 60, 180))

    # Bottom-right: range data + crosshair
    hd.text((W - margin - 130, H - margin - 100), "0xBEE5_4D", font=hud_small, fill=(255, 60, 60, 200))
    hd.text((W - margin - 130, H - margin - 82), "TGT.LOCK", font=hud_small, fill=(255, 60, 60, 200))
    # Tiny crosshair
    hd.line([(W - margin - 40, H - margin - 50), (W - margin - 10, H - margin - 50)], fill=red, width=2)
    hd.line([(W - margin - 25, H - margin - 65), (W - margin - 25, H - margin - 35)], fill=red, width=2)

    # Top-right tiny binary readout
    binary_lines = ["01010110", "11001011", "10110010", "01101001"]
    for i, line in enumerate(binary_lines):
        hd.text((W - margin - 90, margin + 80 + i * 16), line, font=hud_small, fill=(255, 60, 60, 160))

    # Bottom-left: scanning bar
    bar_x = margin + 10
    bar_y = H - margin - 40
    bar_w = 100
    bar_h = 4
    hd.rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], outline=(255, 60, 60, 200), width=1)
    hd.rectangle([bar_x, bar_y, bar_x + int(bar_w * 0.73), bar_y + bar_h], fill=(255, 60, 60, 220))
    hd.text((bar_x, bar_y - 22), "SCAN 73%", font=hud_small, fill=(255, 60, 60, 200))

    img = Image.alpha_composite(img, hud)

    # 14. Horizontal scanning beam across the iris
    sweep_y = cy - 40
    sweep = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    swd = ImageDraw.Draw(sweep, "RGBA")
    for offset in range(-3, 4):
        a = max(0, 80 - abs(offset) * 18)
        swd.line([(cx - bezel_outer, sweep_y + offset),
                  (cx + bezel_outer, sweep_y + offset)], fill=(255, 60, 60, a))
    sweep = sweep.filter(ImageFilter.GaussianBlur(radius=2))
    img = Image.alpha_composite(img, sweep)

    # 15. Overlays
    sl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_scanlines(ImageDraw.Draw(sl, "RGBA"), W, H, gap=3, alpha=14)
    img = Image.alpha_composite(img, sl)

    img = draw_vignette(img, strength=130, depth=85)
    img = draw_grain(img, density=3500, alpha_range=(3, 11))

    # Save
    p1024 = os.path.join(OUTPUT_DIR, "pfp-1024.png")
    img.convert("RGB").save(p1024, "PNG", quality=95)
    p400 = os.path.join(OUTPUT_DIR, "pfp-400.png")
    img.resize((400, 400), Image.LANCZOS).convert("RGB").save(p400, "PNG", quality=95)
    p32 = os.path.join(OUTPUT_DIR, "pfp-32.png")
    img.resize((32, 32), Image.LANCZOS).convert("RGB").save(p32, "PNG", quality=95)

    print(f"  -> {p1024}")
    print(f"  -> {p400}")
    print(f"  -> {p32}")


# ===== Banner: Blade Runner Tokyo =====

def generate_banner_tokyo():
    print("Generating banner — Blade Runner Tokyo cityscape...")
    random.seed(42)
    W, H = 1500, 500
    img = Image.new("RGBA", (W, H), (*DARK_BASE, 255))

    # Background gradient — dark with magenta+purple atmospheric tint
    for y in range(H):
        ty = y / H
        base_row = lerp(DARK_BASE, DARK_PURPLE, ty * 0.85)
        for x in range(0, W, 2):
            tx = 1 - abs(x / W - 0.5) * 2
            base = lerp(base_row, (44, 14, 56), tx * 0.20)
            img.putpixel((x, y), (*base, 255))
            if x + 1 < W:
                img.putpixel((x + 1, y), (*base, 255))
    draw = ImageDraw.Draw(img, "RGBA")

    # Upper magenta fog band
    fog = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fog, "RGBA")
    horizon1 = 300
    for y in range(horizon1 - 70, horizon1 + 90):
        t = max(0, 1 - abs(y - horizon1) / 80)
        a = int(32 * t * t)
        fd.line([(0, y), (W, y)], fill=(*NEON_HOTPINK, a))
    # Lower cyan fog
    horizon2 = 440
    for y in range(horizon2 - 30, H):
        t = max(0, 1 - abs(y - horizon2) / 60)
        a = int(22 * t)
        fd.line([(0, y), (W, y)], fill=(*NEON_CYAN, a))
    img = Image.alpha_composite(img, fog)
    draw = ImageDraw.Draw(img, "RGBA")

    # Distant background neon spots (the city deep)
    spots = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    spd = ImageDraw.Draw(spots, "RGBA")
    neon_positions = [
        (180, 200, NEON_MAGENTA, 50, 38),
        (340, 170, NEON_HOTPINK, 42, 30),
        (520, 220, NEON_CYAN, 38, 26),
        (720, 180, NEON_AMBER, 55, 40),
        (900, 200, NEON_MAGENTA, 32, 24),
        (1080, 170, NEON_CYAN, 46, 32),
        (1280, 210, NEON_AMBER, 38, 26),
        (1420, 190, NEON_PURPLE, 44, 30),
    ]
    for nx, ny, nc, nr, na in neon_positions:
        for r in range(nr, 0, -2):
            a = int(na * (1 - (r / nr) ** 2))
            if a > 0:
                spd.ellipse([nx - r, ny - r, nx + r, ny + r], fill=(*nc, a))
    spots = spots.filter(ImageFilter.GaussianBlur(radius=1))
    img = Image.alpha_composite(img, spots)
    draw = ImageDraw.Draw(img, "RGBA")

    # CITYSCAPE — generate buildings
    base_y = 470
    buildings = []
    bx_cursor = 5
    while bx_cursor < W:
        kind = random.choices(
            ['skinny', 'block', 'mid', 'tall'],
            weights=[35, 20, 30, 15])[0]
        if kind == 'skinny':
            bw = random.randint(18, 30)
            bh = random.randint(180, 360)
        elif kind == 'block':
            bw = random.randint(60, 105)
            bh = random.randint(110, 200)
        elif kind == 'tall':
            bw = random.randint(35, 55)
            bh = random.randint(280, 420)
        else:  # mid
            bw = random.randint(35, 65)
            bh = random.randint(150, 260)
        buildings.append({
            'x': bx_cursor, 'w': bw, 'h': bh, 'kind': kind,
            'sign': False, 'billboard': False
        })
        bx_cursor += bw + random.randint(0, 5)

    # Draw building silhouettes
    for b in buildings:
        bx, bw, bh = b['x'], b['w'], b['h']
        c = lerp(DARK_BASE, (32, 18, 46), random.uniform(0.3, 0.65))
        draw.rectangle([bx, base_y - bh, bx + bw, base_y], fill=(*c, 245))

    # Draw lit windows on a dedicated layer (so we can soften it)
    window_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(window_layer, "RGBA")
    for b in buildings:
        bx, bw, bh = b['x'], b['w'], b['h']
        # Four-tier density so the cityscape has dim AND blazing buildings
        roll = random.random()
        if roll < 0.18:
            win_prob, a_range = 0.04, (40, 80)         # dark / unlit
        elif roll < 0.48:
            win_prob, a_range = 0.13, (60, 110)        # quietly lit
        elif roll < 0.80:
            win_prob, a_range = 0.24, (80, 145)        # busy floor
        else:
            win_prob, a_range = 0.42, (140, 210)       # blazing — apartment fully lit
        # Coherent per-building palette: each tower owns 1-2 colors
        primary = random.choice([NEON_CYAN, NEON_AMBER, (255, 220, 130), NEON_HOTPINK])
        secondary = random.choice([NEON_AMBER, (255, 200, 100), NEON_CYAN])
        for wy in range(base_y - bh + 12, base_y - 5, 10):
            for wx in range(bx + 3, bx + bw - 3, 5):
                if random.random() < win_prob:
                    col = primary if random.random() < 0.78 else secondary
                    a = random.randint(*a_range)
                    wd.rectangle([wx, wy, wx + 2, wy + 3], fill=(*col, a))
    # Soften pixel-grid edges so they don't strobe
    window_layer = window_layer.filter(ImageFilter.GaussianBlur(radius=0.6))
    img = Image.alpha_composite(img, window_layer)
    draw = ImageDraw.Draw(img, "RGBA")

    # Vertical katakana neon signs on tall/skinny buildings
    sign_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sign_font = load_jp_font(20)
    sign_font_big = load_jp_font(26)
    eligible = [b for b in buildings if b['kind'] in ('skinny', 'tall')
                and b['h'] >= 200 and b['w'] >= 18]
    chosen = random.sample(eligible, min(9, len(eligible)))
    # Process tallest first so long words (TRANSDIMENSIONAL, SINGULARITY) get a tower that fits
    chosen.sort(key=lambda b: b['h'], reverse=True)
    # Pool of words to use (no repeats within a banner), longest first
    word_pool = sorted(VERTICAL_SIGN_WORDS, key=len, reverse=True)
    for b in chosen:
        bx, bw, bh = b['x'], b['w'], b['h']
        sign_color = random.choice([NEON_HOTPINK, NEON_CYAN, NEON_AMBER, NEON_MAGENTA, (255, 100, 255)])
        font_use = sign_font_big if bw > 28 else sign_font
        char_h = 28 if bw > 28 else 22
        # How many characters fit on this building?
        sign_top = base_y - bh + random.randint(20, 40)
        max_chars = max(2, (base_y - 25 - sign_top) // char_h)
        # Pick the longest word from the pool that fits
        word = None
        for candidate in word_pool:
            if len(candidate) <= max_chars:
                word = candidate
                word_pool.remove(candidate)
                break
        if word is None:
            # Fallback: take first word and truncate
            if word_pool:
                word = word_pool.pop(0)[:max_chars]
            else:
                continue
        sign_x = bx + bw // 2 - (13 if bw > 28 else 11)
        for i, char in enumerate(word):
            ch_y = sign_top + i * char_h
            if ch_y > base_y - 25:
                break
            sign_layer = draw_neon_text(sign_layer, char, sign_x, ch_y, font_use,
                                         sign_color, glow_radius=4, glow_alpha=90)
        b['sign'] = True

    img = Image.alpha_composite(img, sign_layer)

    # Horizontal billboard panels on block buildings
    bb_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    block_buildings = [b for b in buildings if b['kind'] == 'block']
    random.shuffle(block_buildings)
    for b in block_buildings[:5]:
        bx, bw, bh = b['x'], b['w'], b['h']
        bb_x = bx + 4
        bb_y = base_y - bh + random.randint(25, 90)
        bb_w = bw - 8
        bb_h = random.randint(22, 38)
        col = random.choice([NEON_HOTPINK, NEON_CYAN, NEON_AMBER, NEON_MAGENTA, NEON_PURPLE])
        # Outer glow
        for inset in range(-12, 0, 2):
            a = int(35 * (1 - abs(inset) / 12))
            ImageDraw.Draw(bb_layer, "RGBA").rectangle(
                [bb_x + inset, bb_y + inset, bb_x + bb_w - inset, bb_y + bb_h - inset],
                outline=(*col, a), width=1)
        # Filled panel
        ImageDraw.Draw(bb_layer, "RGBA").rectangle(
            [bb_x, bb_y, bb_x + bb_w, bb_y + bb_h], fill=(*col, 110))
        # Border
        ImageDraw.Draw(bb_layer, "RGBA").rectangle(
            [bb_x, bb_y, bb_x + bb_w, bb_y + bb_h], outline=(*col, 240), width=1)
        # Featured Beeswax-Pat phrase on the billboard if wide enough
        if bb_w > 50:
            billboard_font = load_jp_font(16)
            # Pick a phrase that fits the available width
            max_chars = max(2, bb_w // 14)
            candidates = [t for t in BILLBOARD_TEXTS if len(t) <= max_chars]
            if candidates:
                phrase = random.choice(candidates)
                bb_layer = draw_neon_text(
                    bb_layer, phrase,
                    bb_x + (bb_w - len(phrase) * 14) // 2,
                    bb_y + 8, billboard_font, WHITE,
                    glow_radius=2, glow_alpha=160,
                )
    img = Image.alpha_composite(img, bb_layer)

    # Spinner cars (small bright dots with light trails)
    cars_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cars_layer, "RGBA")
    for _ in range(5):
        car_x = random.randint(80, W - 80)
        car_y = random.randint(160, 290)
        col = random.choice([NEON_CYAN, NEON_AMBER, NEON_HOTPINK, WHITE])
        # Headlight
        for r in range(6, 0, -1):
            a = int(255 * (1 - r / 6) ** 1.5)
            cd.ellipse([car_x - r, car_y - r, car_x + r, car_y + r], fill=(*col, a))
        # Light trail
        trail_dir = random.choice([1, -1])
        trail_len = random.randint(40, 100)
        for i in range(trail_len):
            a = int(180 * (1 - i / trail_len) ** 1.5)
            tx = car_x - i * trail_dir
            ty = car_y + random.randint(-1, 1)
            cd.point((tx, ty), fill=(*col, a))
            if i < trail_len // 3:
                cd.point((tx, ty + 1), fill=(*col, a // 2))
                cd.point((tx, ty - 1), fill=(*col, a // 2))
    cars_glow = cars_layer.filter(ImageFilter.GaussianBlur(radius=2))
    img = Image.alpha_composite(img, cars_glow)
    img = Image.alpha_composite(img, cars_layer)

    # Wet street reflection
    street = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(street, "RGBA")
    for y in range(base_y, H):
        t = (y - base_y) / (H - base_y)
        a_cyan = int(14 * (1 - t))
        a_pink = int(8 * (1 - t))
        sd.line([(0, y), (W, y)], fill=(*NEON_CYAN, a_cyan))
        if y % 2 == 0:
            sd.line([(0, y), (W, y)], fill=(*NEON_HOTPINK, a_pink))
    img = Image.alpha_composite(img, street)
    draw = ImageDraw.Draw(img, "RGBA")

    # Heavy rain — multiple passes
    rain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rain, "RGBA")
    draw_rain(rd, W, H, density=600, color=NEON_CYAN, alpha_range=(8, 26))
    draw_rain(rd, W, H, density=200, color=WHITE, alpha_range=(5, 18))
    draw_rain(rd, W, H, density=120, color=NEON_HOTPINK, alpha_range=(4, 14))
    img = Image.alpha_composite(img, rain)

    # Steam/smoke wisps near street level
    steam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    std = ImageDraw.Draw(steam, "RGBA")
    for _ in range(8):
        sx = random.randint(50, W - 50)
        sy = random.randint(base_y - 40, base_y - 5)
        sw = random.randint(80, 200)
        sh = random.randint(15, 30)
        std.ellipse([sx - sw // 2, sy - sh // 2, sx + sw // 2, sy + sh // 2],
                    fill=(180, 180, 200, random.randint(15, 40)))
    steam = steam.filter(ImageFilter.GaussianBlur(radius=12))
    img = Image.alpha_composite(img, steam)

    # ASCII Shadow BEESWAX PAT wordmark — top center
    art_font = ImageFont.truetype(FONT_MONO_BOLD, 14)
    line_h = 16
    longest = max(ASCII_ART, key=len)
    bb = art_font.getbbox(longest)
    art_w = bb[2] - bb[0]
    art_x = (W - art_w) // 2
    art_y = 30

    for i, line in enumerate(ASCII_ART):
        ly = art_y + i * line_h
        img = draw_chromatic_text(img, line, art_x, ly, art_font, glow_radius=4, offset=2)

    # Overlays
    sl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_scanlines(ImageDraw.Draw(sl, "RGBA"), W, H, gap=3, alpha=12)
    img = Image.alpha_composite(img, sl)
    img = draw_vignette(img, strength=80, depth=50)
    img = draw_grain(img, density=3000, alpha_range=(3, 12))

    path = os.path.join(OUTPUT_DIR, "banner-1500x500.png")
    img.convert("RGB").save(path, "PNG", quality=95)
    print(f"  -> {path}")


if __name__ == "__main__":
    print("=" * 60)
    print("Beeswax Pat — X Profile Asset Generator (v2)")
    print("=" * 60)
    generate_pfp()
    print()
    generate_banner_tokyo()
    print()
    print("All assets in:", OUTPUT_DIR)
