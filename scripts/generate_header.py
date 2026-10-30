"""Render assets/header-dark.svg and assets/header-light.svg (static profile banner)."""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "dark": {"bg1": "#0d0b14", "bg2": "#161127", "border": "#2a2440", "text": "#f1eefb",
             "sub": "#b7b0d6", "muted": "#7f78a3", "dot": "#2a2440", "chip": "#1c1730",
             "a1": "#a08ae6", "a2": "#7d95f5", "a3": "#c29af0", "glow": 0.55},
    "light": {"bg1": "#fbfaff", "bg2": "#f0ecfd", "border": "#e2dcf5", "text": "#17122b",
              "sub": "#4b4370", "muted": "#7a729e", "dot": "#ddd6f3", "chip": "#ffffff",
              "a1": "#7b61d6", "a2": "#4f6fe8", "a3": "#a46be0", "glow": 0.35},
}

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

CHIPS = ["Full-stack web", "Flutter apps", "AI developer tools", "Dhaka, Bangladesh"]


def render(t):
    W, H = 1200, 340
    chips, x = [], 64
    for label in CHIPS:
        w = 22 + len(label) * 8.1
        chips.append(f'<rect x="{x}" y="244" width="{w:.0f}" height="34" rx="17" fill="{t["chip"]}" stroke="{t["border"]}"/>'
                      f'<text x="{x + w / 2:.0f}" y="266" text-anchor="middle" class="chip">{label}</text>')
        x += w + 10
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Md Abu Sayum Anik, software engineer">
<style>
  .kicker{{font:500 15px {MONO};fill:{t['a1']};letter-spacing:.04em}}
  .name{{font:700 58px {SANS};fill:{t['text']};letter-spacing:-.02em}}
  .sub{{font:400 22px {SANS};fill:{t['sub']}}}
  .chip{{font:500 14px {SANS};fill:{t['sub']}}}
  .in{{animation:in .9s cubic-bezier(.22,1,.36,1) both}}
  .orb{{animation:drift 14s ease-in-out infinite alternate}}
  .orb2{{animation:drift2 18s ease-in-out infinite alternate}}
  .spin{{transform-origin:960px 170px;animation:spin 40s linear infinite}}
  @keyframes in{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
  @keyframes drift{{to{{transform:translate(-30px,18px)}}}}
  @keyframes drift2{{to{{transform:translate(26px,-14px)}}}}
  @keyframes spin{{to{{transform:rotate(360deg)}}}}
  @media (prefers-reduced-motion:reduce){{.in,.orb,.orb2,.spin{{animation:none}}}}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg2']}"/></linearGradient>
  <linearGradient id="ring" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['a1']}"/><stop offset=".5" stop-color="{t['a2']}"/><stop offset="1" stop-color="{t['a3']}"/></linearGradient>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="{t['dot']}"/></pattern>
  <radialGradient id="fadeDots" cx=".78" cy=".5" r=".6"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
  <mask id="dm"><rect width="{W}" height="{H}" fill="url(#fadeDots)"/></mask>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="48"/></filter>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="20"/></clipPath>
</defs>
<g clip-path="url(#card)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#dots)" mask="url(#dm)"/>
  <g filter="url(#blur)" opacity="{t['glow']}">
    <circle class="orb" cx="930" cy="120" r="120" fill="{t['a1']}"/>
    <circle class="orb2" cx="1050" cy="230" r="100" fill="{t['a2']}"/>
    <circle class="orb" cx="840" cy="250" r="80" fill="{t['a3']}"/>
  </g>
  <g fill="none" stroke="url(#ring)">
    <circle cx="960" cy="170" r="112" stroke-width="1.5" opacity=".9"/>
    <circle cx="960" cy="170" r="146" stroke-width="1" opacity=".45" stroke-dasharray="2 7"/>
    <circle cx="960" cy="170" r="78" stroke-width="1" opacity=".35"/>
  </g>
  <g class="spin"><circle cx="1072" cy="170" r="6" fill="{t['a3']}"/><circle cx="960" cy="24" r="3.5" fill="{t['a2']}"/></g>
  <text x="960" y="186" text-anchor="middle" font-family="{MONO}" font-size="44" font-weight="600" fill="url(#ring)">&lt;/&gt;</text>
  <g class="in"><text x="64" y="96" class="kicker">~/anik-tb $ whoami</text></g>
  <g class="in" style="animation-delay:.08s"><text x="62" y="162" class="name">Md Abu Sayum Anik</text></g>
  <g class="in" style="animation-delay:.16s"><text x="64" y="206" class="sub">Software engineer · CSE at United International University</text></g>
  <g class="in" style="animation-delay:.24s">{''.join(chips)}</g>
</g>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="20" fill="none" stroke="{t['border']}" stroke-width="1.5"/>
</svg>
"""


if __name__ == "__main__":
    for name, theme in THEMES.items():
        (OUT / f"header-{name}.svg").write_text(render(theme), encoding="utf-8")
