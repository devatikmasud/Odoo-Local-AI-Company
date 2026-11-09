#!/usr/bin/env python3
"""Generates the vector/procedural images (logo, hero art, wave + network backgrounds).
Run:  python3 build/make_assets.py   (needs Pillow + numpy for the wave background only)"""
import math, pathlib, random
ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"

# ---------------------------------------------------------------- logo
HEX_OUT = "32,3 58,17.5 58,46.5 32,61 6,46.5 6,17.5"
HEX_IN = "32,12 51,22.5 51,42.5 32,53 13,42.5 13,22.5"
def logo(light=False):
    if light:
        o, i, y, s = "#ffffff", "#ffffff", "#ffffff", "#ffffff"
        defs = ""
    else:
        o, i, y, s = "url(#lg)", "#1b8fe6", "#1b8fe6", "#0a2a5c"
        defs = ('<defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1">'
                '<stop offset="0" stop-color="#0a2a5c"/><stop offset="1" stop-color="#0b3f86"/></linearGradient></defs>')
    ow, iw, yw = (4.2, 1.8, 2.4) if light else (5, 2.4, 3)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" stroke-linejoin="round" stroke-linecap="round">'
            f'<title>EIGENKERN</title>{defs}'
            f'<polygon points="{HEX_OUT}" stroke="{o}" stroke-width="{ow}"/>'
            f'<polygon points="{HEX_IN}" stroke="{i}" stroke-width="{iw}"/>'
            f'<path d="M13 22.5 32 33 51 22.5" stroke="{y}" stroke-width="{yw}"/>'
            f'<path d="M32 33V53" stroke="{s}" stroke-width="{yw + .4}"/></svg>\n')
(IMG / "brand").mkdir(parents=True, exist_ok=True)
(IMG / "brand" / "logo-mark.svg").write_text(logo(False))
(IMG / "brand" / "logo-mark-light.svg").write_text(logo(True))
(ROOT / "assets" / "favicon.svg").write_text(logo(False))

# ---------------------------------------------------------------- option art
(IMG / "solutions").mkdir(parents=True, exist_ok=True)
(IMG / "solutions" / "ki-box.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 180" role="img" aria-label="EIGENKERN KI-Box">
<defs>
<linearGradient id="f" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#26364f"/><stop offset=".5" stop-color="#0d1829"/><stop offset="1" stop-color="#060b15"/></linearGradient>
<linearGradient id="s" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1c2638"/><stop offset="1" stop-color="#0a101b"/></linearGradient>
<linearGradient id="r" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2fb8ff" stop-opacity=".45"/><stop offset="1" stop-color="#2fb8ff" stop-opacity="0"/></linearGradient>
<filter id="g" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3.2"/></filter>
<filter id="b"><feGaussianBlur stdDeviation="9"/></filter></defs>
<ellipse cx="110" cy="150" rx="92" ry="10" fill="#2fb8ff" opacity=".35" filter="url(#b)"/>
<path d="M22 150 L128 150 L128 176 L22 170z" fill="url(#r)" opacity=".55"/>
<path d="M18 36 L132 26 L132 142 L18 134z" fill="url(#f)"/>
<path d="M132 26 L196 40 L196 134 L132 142z" fill="url(#s)"/>
<g stroke="#2d3a50" stroke-width="1.6" opacity=".9"><path d="M142 33v107M152 35v103M162 37v99M172 39v95M182 41v91"/></g>
<path d="M18 36 L132 26 L196 40" fill="none" stroke="#475a76" stroke-width="1.6"/>
<g fill="none" stroke="#35c6ff" stroke-linecap="round"><path d="M132 28V141" stroke-width="5" filter="url(#g)"/><path d="M132 28V141" stroke-width="1.8" stroke="#a6e6ff"/><path d="M19 135 L132 143" stroke-width="4" filter="url(#g)" opacity=".9"/><path d="M19 135 L132 143" stroke-width="1.4"/></g>
<g transform="translate(75 62)" fill="none" stroke="#9fe4ff" stroke-width="1.4" stroke-linejoin="round"><polygon points="0,-11 9.5,-5.5 9.5,5.5 0,11 -9.5,5.5 -9.5,-5.5"/><path d="M-9.5 -5.5 0 0 9.5 -5.5M0 0V11"/></g>
<text x="75" y="96" text-anchor="middle" font-family="Inter,'Segoe UI',Arial,sans-serif" font-size="11" letter-spacing="1.4" fill="#bfe9ff">EIGENKERN</text></svg>
''')
(IMG / "solutions" / "cloud-lock.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 170" role="img" aria-label="Cloud mit Schloss">
<defs><linearGradient id="c" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#cfe2f6"/></linearGradient>
<linearGradient id="k" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1d5db0"/><stop offset="1" stop-color="#0a2f66"/></linearGradient>
<filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#5b8fc9" flood-opacity=".35"/></filter></defs>
<g filter="url(#sh)"><path d="M52 128c-21 0-36-13-36-31 0-17 13-30 31-31 5-24 25-40 50-40 27 0 47 17 50 41 18 2 31 15 31 31 0 17-14 30-34 30z" fill="url(#c)"/></g>
<path d="M60 70c8-18 26-28 46-26" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".9"/>
<g filter="url(#sh)"><path d="M82 92v-12a18 18 0 0 1 36 0v12" fill="none" stroke="#9fb9d9" stroke-width="7" stroke-linecap="round"/>
<rect x="72" y="88" width="56" height="46" rx="10" fill="url(#k)"/></g>
<circle cx="100" cy="108" r="6.5" fill="#e7f1ff"/><path d="M100 112v10" stroke="#e7f1ff" stroke-width="5" stroke-linecap="round"/></svg>
''')

# ---------------------------------------------------------------- network lines (CTA band)
random.seed(7)
def network(w=1920, h=260):
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice" aria-hidden="true">']
    for x0, x1 in ((0, 520), (1400, 1920)):
        pts = [(random.uniform(x0, x1), random.uniform(10, h - 10)) for _ in range(22)]
        for i, (x, y) in enumerate(pts):
            near = sorted(pts, key=lambda p: (p[0] - x) ** 2 + (p[1] - y) ** 2)[1:3]
            for nx, ny in near:
                out.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{nx:.0f}" y2="{ny:.0f}" stroke="#2bb6d8" stroke-opacity=".3" stroke-width="1"/>')
        for x, y in pts:
            out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice((1.6, 2.2, 3))}" fill="#46d3f0" fill-opacity=".75"/>')
    out.append('</svg>')
    return "".join(out)
(IMG / "bg").mkdir(parents=True, exist_ok=True)
(IMG / "bg" / "network.svg").write_text(network())

# ---------------------------------------------------------------- dotted wave background (Wächter)
try:
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter
    W, H = 1920, 600
    rng = np.random.default_rng(5)
    xs = np.linspace(0, 1, W)[None, :]
    base = np.zeros((H, W, 3), dtype=np.float32)
    left = np.array([3, 22, 52], np.float32); right = np.array([6, 54, 100], np.float32)
    t = np.linspace(0, 1, W)[None, :, None]
    base[:] = left * (1 - t) + right * t
    yy, xx = np.mgrid[0:H, 0:W]
    glow = np.exp(-(((xx - 1350) / 520) ** 2 + ((yy - 260) / 230) ** 2))[..., None]
    base += glow * np.array([6, 70, 120], np.float32)
    img = Image.fromarray(np.clip(base, 0, 255).astype("uint8")).convert("RGBA")
    dots = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(dots)
    ribbons = [(330, 70, .0042, 0.0, 55), (400, 90, .0035, 1.8, 70), (260, 60, .005, 3.1, 40), (460, 50, .0045, 4.4, 45)]
    for cy, A, f, ph, th in ribbons:
        for _ in range(3000):
            x = rng.uniform(520, W)
            fade = min(1, (x - 520) / 500) * (1 if x < 1700 else max(0, (W - x) / 220 + .35))
            y = cy + A * math.sin(x * f + ph) + 38 * math.sin(x * f * 2.3 + ph * 1.7) + rng.normal(0, th * (.35 + .65 * abs(math.sin(x * .0019 + ph))))
            if not 0 <= y < H: continue
            a = int(255 * fade * rng.uniform(.1, .7))
            r = rng.choice([.8, 1.0, 1.2, 1.6])
            d.ellipse((x - r, y - r, x + r, y + r), fill=(90, 205, 255, a))
    glowl = dots.filter(ImageFilter.GaussianBlur(3.5))
    img = Image.alpha_composite(img, glowl); img = Image.alpha_composite(img, dots)
    img.convert("RGB").save(IMG / "bg" / "waves.jpg", quality=82, optimize=True, progressive=True)
except ImportError:
    print("Pillow/numpy missing – wave background not regenerated")
print("assets ok")
