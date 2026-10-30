"""Render assets/header-dark.svg and assets/header-light.svg — high-end developer profile banner."""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "dark": {
        "bg1": "#060813",
        "bg2": "#0c1228",
        "accent1": "#00d4ff",   # cyan
        "accent2": "#9d4edd",   # violet
        "accent3": "#f72585",   # magenta/rose
        "accent4": "#10b981",   # emerald
        "text": "#f8fafc",
        "text_sub": "#cbd5e1",
        "muted": "#94a3b8",
        "terminal_bg": "#0b0f1e",
        "terminal_border": "rgba(255, 255, 255, 0.12)",
        "terminal_header": "#11182c",
        "card_border": "rgba(255, 255, 255, 0.10)",
        "grid_color": "#ffffff",
        "grid_opacity": 0.035,
        "chip_bg": "rgba(255, 255, 255, 0.05)",
        "chip_border": "rgba(255, 255, 255, 0.12)",
        "chip_text": "#e2e8f0",
        "status_bg": "rgba(16, 185, 129, 0.12)",
        "status_border": "rgba(16, 185, 129, 0.30)",
        "status_text": "#34d399",
        "code_keyword": "#c084fc",
        "code_var": "#38bdf8",
        "code_prop": "#7dd3fc",
        "code_str": "#34d399",
        "code_amber": "#fbbf24",
        "code_punct": "#94a3b8",
        "glow1_op": 0.35,
        "glow2_op": 0.30,
    },
    "light": {
        "bg1": "#f8fafc",
        "bg2": "#eef2ff",
        "accent1": "#0284c7",   # deep sky
        "accent2": "#7c3aed",   # violet
        "accent3": "#db2777",   # pink
        "accent4": "#059669",   # emerald
        "text": "#0f172a",
        "text_sub": "#334155",
        "muted": "#64748b",
        "terminal_bg": "#ffffff",
        "terminal_border": "rgba(0, 0, 0, 0.08)",
        "terminal_header": "#f1f5f9",
        "card_border": "rgba(0, 0, 0, 0.08)",
        "grid_color": "#000000",
        "grid_opacity": 0.04,
        "chip_bg": "#ffffff",
        "chip_border": "rgba(0, 0, 0, 0.08)",
        "chip_text": "#334155",
        "status_bg": "rgba(5, 150, 105, 0.10)",
        "status_border": "rgba(5, 150, 105, 0.25)",
        "status_text": "#059669",
        "code_keyword": "#7c3aed",
        "code_var": "#0284c7",
        "code_prop": "#0369a1",
        "code_str": "#059669",
        "code_amber": "#d97706",
        "code_punct": "#64748b",
        "glow1_op": 0.15,
        "glow2_op": 0.12,
    },
}

SANS = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, Menlo, monospace"


def render(t):
    W, H = 1200, 360

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

  <!-- Accent Border Gradient -->
  <linearGradient id="borderGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{t['accent1']}" stop-opacity="0.6"/>
    <stop offset="50%" stop-color="{t['accent2']}" stop-opacity="0.3"/>
    <stop offset="100%" stop-color="{t['accent3']}" stop-opacity="0.5"/>
  </linearGradient>

  <!-- Radial Glow Behind Code Terminal -->
  <radialGradient id="termGlow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0%" stop-color="{t['accent2']}" stop-opacity="{t['glow1_op']}"/>
    <stop offset="100%" stop-color="{t['accent1']}" stop-opacity="0"/>
  </radialGradient>

  <!-- Radial Glow Top Left -->
  <radialGradient id="heroGlow" cx="0.2" cy="0.2" r="0.6">
    <stop offset="0%" stop-color="{t['accent1']}" stop-opacity="{t['glow2_op']}"/>
    <stop offset="100%" stop-color="{t['bg1']}" stop-opacity="0"/>
  </radialGradient>

  <!-- Grid Pattern -->
  <pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse">
    <path d="M 36 0 L 0 0 0 36" fill="none" stroke="{t['grid_color']}" stroke-width="0.75" opacity="{t['grid_opacity']}"/>
  </pattern>

  <radialGradient id="gridFade" cx="0.5" cy="0.5" r="0.6">
    <stop offset="0%" stop-color="#fff" stop-opacity="1"/>
    <stop offset="100%" stop-color="#fff" stop-opacity="0"/>
  </radialGradient>
  <mask id="gridMask">
    <rect width="{W}" height="{H}" fill="url(#gridFade)"/>
  </mask>

  <!-- Glow Filters -->
  <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="40" result="blur"/>
  </filter>
  <filter id="badgeGlow" x="-50%" y="-50%" width="200%" height="200%">
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
  .name {{ font: 800 46px {SANS}; letter-spacing: -0.03em; }}
  .role {{ font: 600 18px {SANS}; fill: {t['text_sub']}; letter-spacing: -0.01em; }}
  .univ {{ font: 400 14px {SANS}; fill: {t['muted']}; }}
  .statusText {{ font: 600 12px {SANS}; fill: {t['status_text']}; }}
  .chipText {{ font: 500 12.5px {SANS}; fill: {t['chip_text']}; }}

  /* Terminal Code Styling */
  .termTitle {{ font: 500 12px {MONO}; fill: {t['muted']}; }}
  .codeLine {{ font: 500 12.5px/1.7 {MONO}; }}
  .lineNum {{ font: 400 12px/1.7 {MONO}; fill: {t['muted']}; opacity: 0.45; user-select: none; }}

  /* Cursor Blink Animation */
  .cursor {{
    fill: {t['accent1']};
    animation: blink 1s step-end infinite;
  }}
  @keyframes blink {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0; }}
  }}

  /* Status Dot Pulse */
  .pulseDot {{
    animation: pulse 2.2s ease-in-out infinite;
  }}
  @keyframes pulse {{
    0%, 100% {{ transform: scale(1); opacity: 1; }}
    50% {{ transform: scale(1.35); opacity: 0.6; }}
  }}

  /* Floating Animation for Code Window */
  .floatWindow {{
    animation: subtleFloat 8s ease-in-out infinite alternate;
  }}
  @keyframes subtleFloat {{
    0% {{ transform: translateY(0); }}
    100% {{ transform: translateY(-5px); }}
  }}

  @media (prefers-reduced-motion: reduce) {{
    .cursor, .pulseDot, .floatWindow {{ animation: none; }}
  }}
</style>

<g clip-path="url(#cardClip)">
  <!-- ▸ Canvas Base -->
  <rect width="{W}" height="{H}" fill="url(#bgGrad)"/>
  <rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#gridMask)"/>

  <!-- ▸ Background Glow Orbs -->
  <circle cx="220" cy="140" r="160" fill="url(#heroGlow)" filter="url(#softGlow)"/>
  <circle cx="920" cy="180" r="180" fill="url(#termGlow)" filter="url(#softGlow)"/>

  <!-- ======================================================== -->
  <!-- LEFT COLUMN: Identity & Highlights                       -->
  <!-- ======================================================== -->

  <!-- 1. Terminal Kicker -->
  <g transform="translate(60, 68)">
    <rect x="-8" y="-16" width="186" height="26" rx="6" fill="{t['chip_bg']}" stroke="{t['chip_border']}" stroke-width="0.8"/>
    <text x="4" y="2" class="kicker">
      <tspan fill="{t['muted']}">~/anik $</tspan>
      <tspan fill="{t['accent1']}"> whoami</tspan>
      <tspan class="cursor">_</tspan>
    </text>
  </g>

  <!-- 2. Full Name -->
  <text x="60" y="128" class="name" fill="url(#nameGrad)">Md Abu Sayum Anik</text>

  <!-- 3. Headline Role -->
  <text x="60" y="162" class="role">Software Engineer · Full-Stack &amp; AI Tools</text>

  <!-- 4. University Info -->
  <g transform="translate(60, 188)">
    <text x="0" y="0" class="univ">CSE @ United International University · Dhaka, Bangladesh</text>
  </g>

  <!-- 5. Status Badge -->
  <g transform="translate(60, 216)">
    <rect x="0" y="0" width="206" height="28" rx="14" fill="{t['status_bg']}" stroke="{t['status_border']}" stroke-width="1"/>
    <!-- Glowing Status Indicator Dot -->
    <g transform="translate(14, 14)">
      <circle cx="0" cy="0" r="4.5" fill="{t['accent4']}" filter="url(#badgeGlow)" class="pulseDot"/>
      <circle cx="0" cy="0" r="4" fill="{t['accent4']}"/>
    </g>
    <text x="27" y="18" class="statusText">Available for opportunities</text>
  </g>

  <!-- 6. Tag Chips Row -->
  <g transform="translate(60, 272)">
    <!-- Chip 1: Full-stack Web -->
    <g transform="translate(0, 0)">
      <rect x="0" y="0" width="138" height="32" rx="16" fill="{t['chip_bg']}" stroke="{t['chip_border']}" stroke-width="1"/>
      <!-- Code Icon -->
      <g transform="translate(14, 9)" stroke="{t['accent1']}" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="10 4 14 8 10 12"/>
        <polyline points="4 12 0 8 4 4"/>
      </g>
      <text x="36" y="20.5" class="chipText">Full-Stack Web</text>
    </g>

    <!-- Chip 2: Flutter Apps -->
    <g transform="translate(148, 0)">
      <rect x="0" y="0" width="128" height="32" rx="16" fill="{t['chip_bg']}" stroke="{t['chip_border']}" stroke-width="1"/>
      <!-- Mobile Icon -->
      <g transform="translate(14, 8)" stroke="{t['accent2']}" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <rect x="1" y="0" width="10" height="15" rx="2"/>
        <line x1="6" y1="12" x2="6.01" y2="12"/>
      </g>
      <text x="34" y="20.5" class="chipText">Flutter Apps</text>
    </g>

    <!-- Chip 3: AI Dev Tools -->
    <g transform="translate(286, 0)">
      <rect x="0" y="0" width="124" height="32" rx="16" fill="{t['chip_bg']}" stroke="{t['chip_border']}" stroke-width="1"/>
      <!-- Sparkle / AI Icon -->
      <g transform="translate(13, 8)" fill="{t['accent3']}">
        <path d="M7.5 0 L9 5 L14 6.5 L9 8 L7.5 13 L6 8 L1 6.5 L6 5 Z"/>
      </g>
      <text x="33" y="20.5" class="chipText">AI Dev Tools</text>
    </g>

    <!-- Chip 4: Dhaka, BD -->
    <g transform="translate(420, 0)">
      <rect x="0" y="0" width="112" height="32" rx="16" fill="{t['chip_bg']}" stroke="{t['chip_border']}" stroke-width="1"/>
      <!-- Map Pin Icon (REAL LOCATION PIN) -->
      <g transform="translate(14, 8)" stroke="{t['accent1']}" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <path d="M11 5.5 C11 9.5 5.5 14 5.5 14 C5.5 14 0 9.5 0 5.5 C0 2.5 2.5 0 5.5 0 C8.5 0 11 2.5 11 5.5 Z"/>
        <circle cx="5.5" cy="5.5" r="2" fill="{t['accent1']}"/>
      </g>
      <text x="33" y="20.5" class="chipText">Dhaka, BD</text>
    </g>
  </g>

  <!-- ======================================================== -->
  <!-- RIGHT COLUMN: Modern IDE / Code Window Card             -->
  <!-- ======================================================== -->

  <g class="floatWindow" transform="translate(630, 42)">
    <!-- Terminal Box Container -->
    <rect x="0" y="0" width="510" height="276" rx="14" fill="{t['terminal_bg']}" stroke="{t['terminal_border']}" stroke-width="1"/>
    
    <!-- Top Header Bar -->
    <path d="M 0 14 Q 0 0 14 0 L 496 0 Q 510 0 510 14 L 510 38 L 0 38 Z" fill="{t['terminal_header']}"/>
    <line x1="0" y1="38" x2="510" y2="38" stroke="{t['terminal_border']}" stroke-width="0.8"/>

    <!-- macOS Window Buttons -->
    <circle cx="20" cy="19" r="5" fill="#ff5f56"/>
    <circle cx="36" cy="19" r="5" fill="#ffbd2e"/>
    <circle cx="52" cy="19" r="5" fill="#27c93f"/>

    <!-- Tab Title with file indicator -->
    <text x="74" y="23" class="termTitle">anik.config.ts</text>
    <rect x="420" y="11" width="72" height="18" rx="4" fill="{t['chip_bg']}" stroke="{t['terminal_border']}" stroke-width="0.7"/>
    <text x="456" y="23" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{t['accent1']}">TS 5.7</text>

    <!-- Code Content -->
    <g transform="translate(20, 64)" class="codeLine">
      <!-- Line 1 -->
      <text x="0" y="0">
        <tspan class="lineNum">1 </tspan>
        <tspan fill="{t['code_keyword']}">export const</tspan> <tspan fill="{t['code_var']}">developer</tspan> <tspan fill="{t['code_punct']}">=</tspan> <tspan fill="{t['code_punct']}">&amp;#123;</tspan>
      </text>

      <!-- Line 2 -->
      <text x="0" y="24">
        <tspan class="lineNum">2 </tspan>
        <tspan fill="{t['code_punct']}">  </tspan><tspan fill="{t['code_prop']}">name</tspan><tspan fill="{t['code_punct']}">: </tspan><tspan fill="{t['code_str']}">&quot;Md Abu Sayum Anik&quot;</tspan><tspan fill="{t['code_punct']}">,</tspan>
      </text>

      <!-- Line 3 -->
      <text x="0" y="48">
        <tspan class="lineNum">3 </tspan>
        <tspan fill="{t['code_punct']}">  </tspan><tspan fill="{t['code_prop']}">focus</tspan><tspan fill="{t['code_punct']}">: </tspan><tspan fill="{t['code_str']}">&quot;Full-Stack &amp; AI Systems&quot;</tspan><tspan fill="{t['code_punct']}">,</tspan>
      </text>

      <!-- Line 4 -->
      <text x="0" y="72">
        <tspan class="lineNum">4 </tspan>
        <tspan fill="{t['code_punct']}">  </tspan><tspan fill="{t['code_prop']}">craft</tspan><tspan fill="{t['code_punct']}">: </tspan><tspan fill="{t['code_punct']}">[</tspan><tspan fill="{t['code_amber']}">&quot;Next.js&quot;</tspan><tspan fill="{t['code_punct']}">, </tspan><tspan fill="{t['code_amber']}">&quot;FastAPI&quot;</tspan><tspan fill="{t['code_punct']}">, </tspan><tspan fill="{t['code_amber']}">&quot;Flutter&quot;</tspan><tspan fill="{t['code_punct']}">],</tspan>
      </text>

      <!-- Line 5 -->
      <text x="0" y="96">
        <tspan class="lineNum">5 </tspan>
        <tspan fill="{t['code_punct']}">  </tspan><tspan fill="{t['code_prop']}">building</tspan><tspan fill="{t['code_punct']}">: </tspan><tspan fill="{t['accent3']}">&quot;GenoNexus 🧬&quot;</tspan><tspan fill="{t['code_punct']}">,</tspan>
      </text>

      <!-- Line 6 -->
      <text x="0" y="120">
        <tspan class="lineNum">6 </tspan>
        <tspan fill="{t['code_punct']}">  </tspan><tspan fill="{t['code_prop']}">highlight</tspan><tspan fill="{t['code_punct']}">: </tspan><tspan fill="{t['code_amber']}">&quot;1st Place AOOP Showcase 🏆&quot;</tspan><tspan fill="{t['code_punct']}">,</tspan>
      </text>

      <!-- Line 7 -->
      <text x="0" y="144">
        <tspan class="lineNum">7 </tspan>
        <tspan fill="{t['code_punct']}">  </tspan><tspan fill="{t['code_prop']}">status</tspan><tspan fill="{t['code_punct']}">: </tspan><tspan fill="{t['code_str']}">&quot;open_for_hire&quot;</tspan>
      </text>

      <!-- Line 8 -->
      <text x="0" y="168">
        <tspan class="lineNum">8 </tspan>
        <tspan fill="{t['code_punct']}">&amp;#125;;</tspan>
        <tspan class="cursor" fill="{t['accent1']}">▋</tspan>
      </text>
    </g>

    <!-- Bottom Accent Line -->
    <line x1="20" y1="262" x2="160" y2="262" stroke="url(#borderGrad)" stroke-width="2" stroke-linecap="round"/>
  </g>
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
    print("Done — new headers generated successfully.")
