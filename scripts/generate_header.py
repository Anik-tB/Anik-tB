"""Render assets/header-dark.svg and assets/header-light.svg — modern developer profile banner."""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "dark": {
        "bg1": "#060814",
        "bg2": "#0c1126",
        "accent1": "#00d4ff",   # electric cyan
        "accent2": "#8b5cf6",   # vibrant violet
        "accent3": "#ec4899",   # rose / magenta
        "accent4": "#10b981",   # emerald
        "text_name": "#f8fafc",
        "text_role": "#f1f5f9",
        "text_univ": "#94a3b8",
        "prompt_bg": "rgba(255, 255, 255, 0.05)",
        "prompt_border": "rgba(255, 255, 255, 0.12)",
        "prompt_user": "#94a3b8",
        "prompt_cmd": "#00d4ff",
        "card_border": "rgba(255, 255, 255, 0.10)",
        "grid_color": "#ffffff",
        "grid_opacity": 0.035,
        "chip_bg": "rgba(255, 255, 255, 0.05)",
        "chip_border": "rgba(255, 255, 255, 0.12)",
        "chip_text": "#e2e8f0",
        "status_bg": "rgba(16, 185, 129, 0.10)",
        "status_border": "rgba(16, 185, 129, 0.28)",
        "status_text": "#34d399",
        "hub_bg": "#0c1228",
        "node_bg": "rgba(12, 18, 40, 0.90)",
        "node_border": "rgba(255, 255, 255, 0.14)",
        "node_text": "#e2e8f0",
        "glow_opacity": 0.45,
    },
    "light": {
        "bg1": "#f8fafc",
        "bg2": "#edf2f7",
        "accent1": "#0284c7",   # deep sky
        "accent2": "#7c3aed",   # violet
        "accent3": "#db2777",   # rose
        "accent4": "#059669",   # emerald
        "text_name": "#0f172a",
        "text_role": "#1e293b",
        "text_univ": "#475569",
        "prompt_bg": "#ffffff",
        "prompt_border": "rgba(0, 0, 0, 0.08)",
        "prompt_user": "#64748b",
        "prompt_cmd": "#0284c7",
        "card_border": "rgba(0, 0, 0, 0.08)",
        "grid_color": "#000000",
        "grid_opacity": 0.035,
        "chip_bg": "#ffffff",
        "chip_border": "rgba(0, 0, 0, 0.08)",
        "chip_text": "#334155",
        "status_bg": "rgba(5, 150, 105, 0.08)",
        "status_border": "rgba(5, 150, 105, 0.22)",
        "status_text": "#059669",
        "hub_bg": "#ffffff",
        "node_bg": "rgba(255, 255, 255, 0.95)",
        "node_border": "rgba(0, 0, 0, 0.08)",
        "node_text": "#1e293b",
        "glow_opacity": 0.18,
    },
}

SANS = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, Menlo, monospace"


def render(t):
    W, H = 1200, 360
    cx, cy = 945, 180

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Md Abu Sayum Anik — Software Engineer Profile">
<defs>
  <!-- Background Gradient -->
  <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{t['bg1']}"/>
    <stop offset="100%" stop-color="{t['bg2']}"/>
  </linearGradient>

  <!-- Name Text Gradient -->
  <linearGradient id="nameGrad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{t['accent1']}"/>
    <stop offset="50%" stop-color="{t['accent2']}"/>
    <stop offset="100%" stop-color="{t['accent3']}"/>
  </linearGradient>

  <!-- Ring Accent Gradient -->
  <linearGradient id="ringGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{t['accent1']}"/>
    <stop offset="50%" stop-color="{t['accent2']}"/>
    <stop offset="100%" stop-color="{t['accent3']}"/>
  </linearGradient>

  <!-- Node Border Gradient -->
  <linearGradient id="nodeGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{t['accent1']}" stop-opacity="0.6"/>
    <stop offset="100%" stop-color="{t['accent2']}" stop-opacity="0.4"/>
  </linearGradient>

  <!-- Grid Pattern -->
  <pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse">
    <path d="M 36 0 L 0 0 0 36" fill="none" stroke="{t['grid_color']}" stroke-width="0.75" opacity="{t['grid_opacity']}"/>
  </pattern>

  <radialGradient id="gridFade" cx="0.45" cy="0.5" r="0.65">
    <stop offset="0%" stop-color="#fff" stop-opacity="1"/>
    <stop offset="100%" stop-color="#fff" stop-opacity="0"/>
  </radialGradient>
  <mask id="gridMask">
    <rect width="{W}" height="{H}" fill="url(#gridFade)"/>
  </mask>

  <!-- Glow Filter -->
  <filter id="blurGlow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="45"/>
  </filter>
  <filter id="dotGlow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="3" result="blur"/>
    <feComposite in="SourceGraphic" in2="blur" operator="over"/>
  </filter>

  <!-- Card Clip -->
  <clipPath id="cardClip">
    <rect width="{W}" height="{H}" rx="18"/>
  </clipPath>
</defs>

<style>
  .kicker {{ font: 600 13px {MONO}; letter-spacing: 0.05em; }}
  .name {{ font: 800 50px {SANS}; letter-spacing: -0.03em; }}
  .role {{ font: 600 19px {SANS}; fill: {t['text_role']}; letter-spacing: -0.01em; }}
  .univ {{ font: 400 14.5px {SANS}; fill: {t['text_univ']}; }}
  .statusText {{ font: 600 12px {SANS}; fill: {t['status_text']}; }}
  .chipText {{ font: 500 13px {SANS}; fill: {t['chip_text']}; }}
  .nodeText {{ font: 600 12px {MONO}; fill: {t['node_text']}; }}
  .codeSymbol {{ font: 700 34px {MONO}; }}

  /* Smooth Spin for Orbit */
  .orbitSpin {{
    transform-origin: {cx}px {cy}px;
    animation: spinOrbit 45s linear infinite;
  }}
  @keyframes spinOrbit {{
    0% {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
  }}

  /* Pulsing Ambient Orbs */
  .orbFloat1 {{
    animation: float1 12s ease-in-out infinite alternate;
  }}
  .orbFloat2 {{
    animation: float2 15s ease-in-out infinite alternate;
  }}
  @keyframes float1 {{
    0% {{ transform: translate(0, 0); }}
    100% {{ transform: translate(-20px, 15px); }}
  }}
  @keyframes float2 {{
    0% {{ transform: translate(0, 0); }}
    100% {{ transform: translate(15px, -18px); }}
  }}

  /* Green Status Pulse */
  .pulseDot {{
    animation: pulse 2.2s ease-in-out infinite;
  }}
  @keyframes pulse {{
    0%, 100% {{ opacity: 1; transform: scale(1); }}
    50% {{ opacity: 0.55; transform: scale(1.35); }}
  }}

  @media (prefers-reduced-motion: reduce) {{
    .orbitSpin, .orbFloat1, .orbFloat2, .pulseDot {{ animation: none; }}
  }}
</style>

<g clip-path="url(#cardClip)">
  <!-- ▸ Canvas Base -->
  <rect width="{W}" height="{H}" fill="url(#bgGrad)"/>
  <rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#gridMask)"/>

  <!-- ▸ Ambient Lighting Behind Right Core -->
  <g filter="url(#blurGlow)" opacity="{t['glow_opacity']}">
    <circle class="orbFloat1" cx="{cx - 30}" cy="{cy - 40}" r="110" fill="{t['accent1']}"/>
    <circle class="orbFloat2" cx="{cx + 40}" cy="{cy + 40}" r="100" fill="{t['accent2']}"/>
    <circle class="orbFloat1" cx="{cx - 60}" cy="{cy + 50}" r="75" fill="{t['accent3']}"/>
    <circle cx="200" cy="140" r="100" fill="{t['accent1']}" opacity="0.35"/>
  </g>

  <!-- ======================================================== -->
  <!-- LEFT COLUMN: Profile Info (100% Real Data)               -->
  <!-- ======================================================== -->

  <!-- 1. Terminal Kicker -->
  <g transform="translate(64, 70)">
    <rect x="-8" y="-17" width="186" height="28" rx="6" fill="{t['prompt_bg']}" stroke="{t['prompt_border']}" stroke-width="1"/>
    <text x="4" y="2" class="kicker">
      <tspan fill="{t['prompt_user']}">~/anik-tb</tspan>
      <tspan fill="{t['prompt_cmd']}"> $ whoami</tspan>
    </text>
  </g>

  <!-- 2. Full Name -->
  <text x="62" y="132" class="name" fill="url(#nameGrad)">Md Abu Sayum Anik</text>

  <!-- 3. Headline Role -->
  <text x="64" y="170" class="role">Software Engineer · Full-Stack &amp; AI Tools</text>

  <!-- 4. University Info -->
  <text x="64" y="198" class="univ">CSE @ United International University · Dhaka, Bangladesh</text>

  <!-- 5. Status Badge -->
  <g transform="translate(64, 222)">
    <rect x="0" y="0" width="206" height="28" rx="14" fill="{t['status_bg']}" stroke="{t['status_border']}" stroke-width="1"/>
    <g transform="translate(14, 14)">
      <circle cx="0" cy="0" r="4.5" fill="{t['accent4']}" filter="url(#dotGlow)" class="pulseDot"/>
      <circle cx="0" cy="0" r="4" fill="{t['accent4']}"/>
    </g>
    <text x="27" y="18" class="statusText">Available for opportunities</text>
  </g>

  <!-- 6. Tag Chips Row -->
  <g transform="translate(64, 274)">
    <!-- Chip 1: Full-stack Web -->
    <g transform="translate(0, 0)">
      <rect x="0" y="0" width="144" height="34" rx="17" fill="{t['chip_bg']}" stroke="{t['chip_border']}" stroke-width="1"/>
      <!-- Code Icon -->
      <g transform="translate(14, 10)" stroke="{t['accent1']}" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="10 4 14 8 10 12"/>
        <polyline points="4 12 0 8 4 4"/>
      </g>
      <text x="37" y="21.5" class="chipText">Full-Stack Web</text>
    </g>

    <!-- Chip 2: Flutter Apps -->
    <g transform="translate(154, 0)">
      <rect x="0" y="0" width="130" height="34" rx="17" fill="{t['chip_bg']}" stroke="{t['chip_border']}" stroke-width="1"/>
      <!-- Mobile Icon -->
      <g transform="translate(14, 9)" stroke="{t['accent2']}" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <rect x="1" y="0" width="10" height="15" rx="2"/>
        <line x1="6" y1="12" x2="6.01" y2="12"/>
      </g>
      <text x="35" y="21.5" class="chipText">Flutter Apps</text>
    </g>

    <!-- Chip 3: AI Dev Tools -->
    <g transform="translate(294, 0)">
      <rect x="0" y="0" width="128" height="34" rx="17" fill="{t['chip_bg']}" stroke="{t['chip_border']}" stroke-width="1"/>
      <!-- Sparkle / AI Icon -->
      <g transform="translate(13, 9)" fill="{t['accent3']}">
        <path d="M7.5 0 L9 5 L14 6.5 L9 8 L7.5 13 L6 8 L1 6.5 L6 5 Z"/>
      </g>
      <text x="34" y="21.5" class="chipText">AI Dev Tools</text>
    </g>

    <!-- Chip 4: Dhaka, BD -->
    <g transform="translate(432, 0)">
      <rect x="0" y="0" width="116" height="34" rx="17" fill="{t['chip_bg']}" stroke="{t['chip_border']}" stroke-width="1"/>
      <!-- Location Map Pin Icon -->
      <g transform="translate(14, 9)" stroke="{t['accent1']}" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <path d="M11 5.5 C11 9.5 5.5 14 5.5 14 C5.5 14 0 9.5 0 5.5 C0 2.5 2.5 0 5.5 0 C8.5 0 11 2.5 11 5.5 Z"/>
        <circle cx="5.5" cy="5.5" r="2" fill="{t['accent1']}"/>
      </g>
      <text x="34" y="21.5" class="chipText">Dhaka, BD</text>
    </g>
  </g>

  <!-- ======================================================== -->
  <!-- RIGHT COLUMN: Modern Tech Core with Real Stack           -->
  <!-- ======================================================== -->

  <!-- Concentric Orbital Cyber Rings -->
  <g fill="none">
    <!-- Outer dashed orbit -->
    <circle cx="{cx}" cy="{cy}" r="142" stroke="url(#ringGrad)" stroke-width="1.2" stroke-dasharray="3 8" opacity="0.4"/>
    <!-- Middle ring -->
    <circle cx="{cx}" cy="{cy}" r="110" stroke="url(#ringGrad)" stroke-width="1.6" opacity="0.75"/>
    <!-- Inner dashed ring -->
    <circle cx="{cx}" cy="{cy}" r="78" stroke="url(#ringGrad)" stroke-width="1.2" stroke-dasharray="2 6" opacity="0.4"/>
  </g>

  <!-- Orbiting Satellites (Rotates around cx, cy) -->
  <g class="orbitSpin">
    <circle cx="{cx + 142}" cy="{cy}" r="5.5" fill="{t['accent1']}"/>
    <circle cx="{cx}" cy="{cy - 110}" r="4.5" fill="{t['accent2']}"/>
    <circle cx="{cx - 78}" cy="{cy}" r="4" fill="{t['accent3']}"/>
    <circle cx="{cx}" cy="{cy + 142}" r="3.5" fill="{t['accent1']}"/>
  </g>

  <!-- Real Tech Badges Positioned Around Core -->
  <!-- 1. Next.js 15 (Top) -->
  <g transform="translate({cx - 48}, {cy - 146})">
    <rect x="0" y="0" width="96" height="28" rx="14" fill="{t['node_bg']}" stroke="url(#nodeGrad)" stroke-width="1"/>
    <text x="48" y="18" text-anchor="middle" class="nodeText">Next.js 15</text>
  </g>

  <!-- 2. Python (Right) -->
  <g transform="translate({cx + 104}, {cy - 14})">
    <rect x="0" y="0" width="84" height="28" rx="14" fill="{t['node_bg']}" stroke="url(#nodeGrad)" stroke-width="1"/>
    <text x="42" y="18" text-anchor="middle" class="nodeText">Python</text>
  </g>

  <!-- 3. Flutter (Bottom) -->
  <g transform="translate({cx - 44}, {cy + 118})">
    <rect x="0" y="0" width="88" height="28" rx="14" fill="{t['node_bg']}" stroke="url(#nodeGrad)" stroke-width="1"/>
    <text x="44" y="18" text-anchor="middle" class="nodeText">Flutter</text>
  </g>

  <!-- 4. FastAPI (Left) -->
  <g transform="translate({cx - 188}, {cy - 14})">
    <rect x="0" y="0" width="84" height="28" rx="14" fill="{t['node_bg']}" stroke="url(#nodeGrad)" stroke-width="1"/>
    <text x="42" y="18" text-anchor="middle" class="nodeText">FastAPI</text>
  </g>

  <!-- Central Hub Circle with </> Symbol -->
  <circle cx="{cx}" cy="{cy}" r="52" fill="{t['hub_bg']}" stroke="url(#ringGrad)" stroke-width="2"/>
  <circle cx="{cx}" cy="{cy}" r="45" fill="none" stroke="{t['accent1']}" stroke-width="0.8" opacity="0.3"/>
  <text x="{cx}" y="{cy + 11}" text-anchor="middle" class="codeSymbol" fill="url(#nameGrad)">&lt;/&gt;</text>
</g>

<!-- Outer Card Border -->
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{t['card_border']}" stroke-width="1"/>
</svg>
"""


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, theme in THEMES.items():
        path = OUT / f"header-{name}.svg"
        path.write_text(render(theme), encoding="utf-8")
        print(f"  ✓ {path}")
    print("Done — clean modern headers generated.")
