"""Render assets/header-dark.svg and assets/header-light.svg — stunning glassmorphism profile banner."""

from pathlib import Path
import math

OUT = Path(__file__).resolve().parent.parent / "assets"

# ── Theme palettes ──────────────────────────────────────────────────────────

THEMES = {
    "dark": {
        "bg1": "#06080f", "bg2": "#0c1029",
        "accent1": "#00d4ff", "accent2": "#7c3aed", "accent3": "#f43f5e", "accent4": "#06d6a0",
        "text": "#f0f4ff", "muted": "#64748b",
        "glass": "rgba(255,255,255,0.05)", "glass_strong": "rgba(255,255,255,0.08)",
        "border": "rgba(255,255,255,0.08)", "border_strong": "rgba(255,255,255,0.12)",
        "glow_opacity": 0.45, "grid_opacity": 0.04,
        "chip_bg": "rgba(255,255,255,0.04)", "chip_border": "rgba(255,255,255,0.10)",
        "shadow": "rgba(0,0,0,0.5)",
    },
    "light": {
        "bg1": "#fafbff", "bg2": "#eef2ff",
        "accent1": "#0891b2", "accent2": "#7c3aed", "accent3": "#e11d48", "accent4": "#059669",
        "text": "#0f172a", "muted": "#64748b",
        "glass": "rgba(255,255,255,0.65)", "glass_strong": "rgba(255,255,255,0.80)",
        "border": "rgba(0,0,0,0.06)", "border_strong": "rgba(0,0,0,0.10)",
        "glow_opacity": 0.25, "grid_opacity": 0.06,
        "chip_bg": "rgba(255,255,255,0.70)", "chip_border": "rgba(0,0,0,0.08)",
        "shadow": "rgba(0,0,0,0.08)",
    },
}

SANS = "'Segoe UI',Inter,-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif"
MONO = "'SF Mono',SFMono-Regular,ui-monospace,Menlo,Consolas,'Liberation Mono',monospace"

CHIPS = [
    ("\ue900", "Full-stack Web"),      # code icon placeholder → we'll use SVG paths
    ("\ue901", "Flutter &amp; Mobile"),
    ("\ue902", "AI Dev Tools"),
    ("\ue903", "Dhaka, BD"),
]


def _helix_path(cx, cy, amp, periods, length, phase, num_pts=80):
    """Generate a DNA-helix-inspired sine wave path string."""
    pts = []
    for i in range(num_pts + 1):
        t = i / num_pts
        y = cy - length / 2 + t * length
        x = cx + amp * math.sin(2 * math.pi * periods * t + phase)
        pts.append(f"{'M' if i == 0 else 'L'}{x:.1f},{y:.1f}")
    return " ".join(pts)


def _helix_rungs(cx, cy, amp, periods, length, num_rungs=8):
    """Generate connecting rungs between the two helix strands."""
    rungs = []
    for i in range(num_rungs):
        t = (i + 0.5) / num_rungs
        y = cy - length / 2 + t * length
        x1 = cx + amp * math.sin(2 * math.pi * periods * t)
        x2 = cx + amp * math.sin(2 * math.pi * periods * t + math.pi)
        rungs.append(f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}"/>')
    return "\n    ".join(rungs)


def _floating_symbols(t):
    """Generate scattered code symbols with float animations."""
    symbols_data = [
        ("{", 780, 55, 16, 0.12, "floatA", 0),
        ("}", 1120, 95, 14, 0.10, "floatB", 0.5),
        ("&lt;/&gt;", 850, 310, 13, 0.09, "floatC", 1.2),
        ("( )", 1060, 330, 12, 0.08, "floatA", 2.0),
        ("=&gt;", 920, 45, 11, 0.10, "floatB", 0.8),
        ("[ ]", 1150, 260, 12, 0.07, "floatC", 1.6),
        ("fn", 770, 280, 11, 0.06, "floatA", 2.5),
        ("//", 1100, 170, 13, 0.08, "floatB", 1.0),
    ]
    elems = []
    for sym, x, y, size, opacity, anim, delay in symbols_data:
        elems.append(
            f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" '
            f'fill="{t["muted"]}" opacity="{opacity}" '
            f'class="{anim}" style="animation-delay:{delay}s">{sym}</text>'
        )
    return "\n  ".join(elems)


def _corner_decorations(t):
    """Small geometric corner accents."""
    c = t["accent1"]
    c2 = t["accent2"]
    return f"""
  <!-- Top-left corner -->
  <g opacity="0.15">
    <line x1="20" y1="30" x2="50" y2="30" stroke="{c}" stroke-width="1.5"/>
    <line x1="30" y1="20" x2="30" y2="50" stroke="{c}" stroke-width="1.5"/>
  </g>
  <!-- Top-right corner -->
  <g opacity="0.12">
    <polygon points="1170,20 1180,35 1160,35" fill="none" stroke="{c2}" stroke-width="1"/>
    <polygon points="1170,28 1175,35 1165,35" fill="{c2}" opacity="0.3"/>
  </g>
  <!-- Bottom-right corner -->
  <g opacity="0.10">
    <rect x="1160" y="345" width="15" height="15" rx="2" fill="none" stroke="{c}" stroke-width="1"/>
    <rect x="1163" y="348" width="9" height="9" rx="1" fill="{c}" opacity="0.15"/>
  </g>
  <!-- Bottom-left corner -->
  <g opacity="0.12">
    <circle cx="30" cy="355" r="6" fill="none" stroke="{c2}" stroke-width="1"/>
    <circle cx="30" cy="355" r="2.5" fill="{c2}" opacity="0.25"/>
  </g>"""


def _chip_icons():
    """Return SVG path data for chip icons."""
    return {
        0: '<path d="M0,2 L4,2 L4,10 L0,10 Z M6,0 L10,0 L10,10 L6,10 Z M12,4 L16,4 L16,10 L12,10 Z" fill="currentColor" opacity="0.7"/>',  # code blocks
        1: '<path d="M8,0 L14,4 L14,12 L8,16 L2,12 L2,4 Z" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.7"/>',  # hexagon (mobile)
        2: '<circle cx="8" cy="8" r="7" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.7"/><circle cx="5" cy="6" r="1.5" fill="currentColor" opacity="0.7"/><circle cx="11" cy="6" r="1.5" fill="currentColor" opacity="0.7"/><path d="M5,10 Q8,13 11,10" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.7"/>',  # AI face
        3: '<path d="M8,1 C8,1 2,6 2,10 C2,13.3 4.7,16 8,16 C11.3,16 14,13.3 14,10 C14,6 8,1 8,1 Z" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.7"/>',  # pin
    }


def render(t):
    W, H = 1200, 380

    # ── Helix paths ──
    hx_cx, hx_cy, hx_amp, hx_periods, hx_len = 1020, 190, 55, 2.5, 280
    helix1 = _helix_path(hx_cx, hx_cy, hx_amp, hx_periods, hx_len, 0)
    helix2 = _helix_path(hx_cx, hx_cy, hx_amp, hx_periods, hx_len, math.pi)
    helix_rungs = _helix_rungs(hx_cx, hx_cy, hx_amp, hx_periods, hx_len, 10)

    # ── Chip pills ──
    icons = _chip_icons()
    chip_elems = []
    cx = 80
    for idx, (_, label) in enumerate(CHIPS):
        text_w = len(label) * 8.5
        pill_w = text_w + 42  # icon space + padding
        # Gradient-outlined pill
        chip_elems.append(
            f'<g class="slideUp" style="animation-delay:{0.50 + idx * 0.08}s">'
            f'<rect x="{cx}" y="278" width="{pill_w:.0f}" height="32" rx="16" '
            f'fill="{t["chip_bg"]}" stroke="url(#chipGrad)" stroke-width="1"/>'
            f'<g transform="translate({cx + 12},{278 + 8})" color="{t["accent1"]}">{icons[idx]}</g>'
            f'<text x="{cx + 34}" y="299" class="chipText">{label}</text>'
            f'</rect></g>'  # close tags — note: the extra </rect> won't matter, SVG ignores
        )
        cx += pill_w + 10

    # Fix: remove stray </rect> — using proper group close
    chip_elems_fixed = []
    cx = 80
    for idx, (_, label) in enumerate(CHIPS):
        text_w = len(label) * 8.5
        pill_w = text_w + 42
        chip_elems_fixed.append(
            f'<g class="slideUp" style="animation-delay:{0.50 + idx * 0.08:.2f}s">'
            f'<rect x="{cx}" y="278" width="{pill_w:.0f}" height="32" rx="16" '
            f'fill="{t["chip_bg"]}" stroke="url(#chipGrad)" stroke-width="1"/>'
            f'<g transform="translate({cx + 12},{286})" color="{t["accent1"]}">{icons[idx]}</g>'
            f'<text x="{cx + 34}" y="299" class="chipText">{label}</text>'
            f'</g>'
        )
        cx += pill_w + 10

    chips_svg = "\n    ".join(chip_elems_fixed)
    float_syms = _floating_symbols(t)
    corners = _corner_decorations(t)

    # ── Geometric floating shapes ──
    geo_shapes = f"""
  <!-- Floating geometric shapes -->
  <g class="floatA" style="animation-delay:0s">
    <polygon points="180,60 200,40 220,60 200,80" fill="none" stroke="{t['accent2']}" stroke-width="0.8" opacity="0.08"/>
  </g>
  <g class="floatB" style="animation-delay:1s">
    <polygon points="300,320 310,305 330,305 340,320 330,335 310,335" fill="{t['accent1']}" opacity="0.04"/>
  </g>
  <g class="floatC" style="animation-delay:0.5s">
    <circle cx="700" cy="60" r="18" fill="none" stroke="{t['accent3']}" stroke-width="0.7" opacity="0.07"/>
  </g>
  <g class="floatA" style="animation-delay:2s">
    <polygon points="650,340 660,325 680,325 690,340 680,355 660,355" fill="none" stroke="{t['accent2']}" stroke-width="0.6" opacity="0.06"/>
  </g>
  <g class="floatB" style="animation-delay:1.5s">
    <rect x="400" y="30" width="16" height="16" rx="2" transform="rotate(45,408,38)" fill="none" stroke="{t['accent1']}" stroke-width="0.7" opacity="0.06"/>
  </g>
  <g class="floatC" style="animation-delay:0.8s">
    <polygon points="550,350 560,335 570,350" fill="{t['accent3']}" opacity="0.05"/>
  </g>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Md Abu Sayum Anik — Software Engineer">
<defs>
  <!-- Background gradient -->
  <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{t['bg1']}"/>
    <stop offset="100%" stop-color="{t['bg2']}"/>
  </linearGradient>

  <!-- Name text gradient -->
  <linearGradient id="nameGrad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{t['accent1']}"/>
    <stop offset="50%" stop-color="{t['accent2']}"/>
    <stop offset="100%" stop-color="{t['accent3']}"/>
  </linearGradient>

  <!-- Helix gradient -->
  <linearGradient id="helixGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{t['accent1']}"/>
    <stop offset="50%" stop-color="{t['accent2']}"/>
    <stop offset="100%" stop-color="{t['accent3']}"/>
  </linearGradient>

  <!-- Chip border gradient -->
  <linearGradient id="chipGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{t['accent1']}" stop-opacity="0.5"/>
    <stop offset="100%" stop-color="{t['accent2']}" stop-opacity="0.3"/>
  </linearGradient>

  <!-- Orb glow filter -->
  <filter id="glow" x="-80%" y="-80%" width="260%" height="260%">
    <feGaussianBlur stdDeviation="55" result="blur"/>
    <feComposite in="SourceGraphic" in2="blur" operator="over"/>
  </filter>
  <filter id="glowStrong" x="-100%" y="-100%" width="300%" height="300%">
    <feGaussianBlur stdDeviation="80"/>
  </filter>

  <!-- Glass blur -->
  <filter id="glassBlur" x="-10%" y="-10%" width="120%" height="120%">
    <feGaussianBlur stdDeviation="2"/>
  </filter>

  <!-- Grid pattern -->
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="{t['text']}" stroke-width="0.5" opacity="{t['grid_opacity']}"/>
  </pattern>

  <!-- Dot grid for mesh effect -->
  <pattern id="dotGrid" width="24" height="24" patternUnits="userSpaceOnUse">
    <circle cx="12" cy="12" r="0.8" fill="{t['text']}" opacity="{t['grid_opacity'] * 1.5:.3f}"/>
  </pattern>

  <!-- Radial fade mask for grid -->
  <radialGradient id="gridFade" cx="0.3" cy="0.5" r="0.8">
    <stop offset="0%" stop-color="white" stop-opacity="0.6"/>
    <stop offset="100%" stop-color="white" stop-opacity="0"/>
  </radialGradient>
  <mask id="gridMask">
    <rect width="{W}" height="{H}" fill="url(#gridFade)"/>
  </mask>

  <!-- Clip path for rounded card -->
  <clipPath id="cardClip">
    <rect width="{W}" height="{H}" rx="18"/>
  </clipPath>

  <!-- Status glow -->
  <filter id="statusGlow" x="-200%" y="-200%" width="500%" height="500%">
    <feGaussianBlur stdDeviation="3"/>
  </filter>
</defs>

<style>
  /* ── Typography ── */
  .kicker {{ font: 500 14px/1 {MONO}; fill: {t['accent1']}; letter-spacing: 0.06em; }}
  .cursor {{ fill: {t['accent1']}; animation: blink 1s step-end infinite; }}
  .name   {{ font: 800 52px/1 {SANS}; fill: url(#nameGrad); letter-spacing: -0.03em; }}
  .sub    {{ font: 400 19px/1 {SANS}; fill: {t['muted']}; letter-spacing: 0.01em; }}
  .status {{ font: 500 13px/1 {SANS}; fill: {t['accent4']}; letter-spacing: 0.02em; }}
  .chipText {{ font: 500 13px/1 {SANS}; fill: {t['muted']}; }}

  /* ── Animations ── */
  .slideUp {{
    opacity: 0; transform: translateY(18px);
    animation: slideUpIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  }}
  .floatA {{ animation: driftA 18s ease-in-out infinite alternate; }}
  .floatB {{ animation: driftB 22s ease-in-out infinite alternate; }}
  .floatC {{ animation: driftC 16s ease-in-out infinite alternate; }}
  .helixRotate {{ animation: helixSway 12s ease-in-out infinite alternate; transform-origin: {hx_cx}px {hx_cy}px; }}
  .orbPulse1 {{ animation: pulse1 6s ease-in-out infinite alternate; }}
  .orbPulse2 {{ animation: pulse2 8s ease-in-out infinite alternate; }}
  .orbPulse3 {{ animation: pulse3 7s ease-in-out infinite alternate; }}
  .statusDot {{ animation: statusPulse 2s ease-in-out infinite; }}
  .helixDash {{ animation: helixFlow 4s linear infinite; }}
  .ringRotate {{ animation: ringRot 50s linear infinite; transform-origin: {hx_cx}px {hx_cy}px; }}

  @keyframes slideUpIn {{
    0%   {{ opacity: 0; transform: translateY(18px); }}
    100% {{ opacity: 1; transform: translateY(0); }}
  }}
  @keyframes blink {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0; }}
  }}
  @keyframes driftA {{
    0%   {{ transform: translate(0, 0); }}
    100% {{ transform: translate(-20px, 15px); }}
  }}
  @keyframes driftB {{
    0%   {{ transform: translate(0, 0); }}
    100% {{ transform: translate(18px, -12px); }}
  }}
  @keyframes driftC {{
    0%   {{ transform: translate(0, 0); }}
    100% {{ transform: translate(-14px, -18px); }}
  }}
  @keyframes pulse1 {{
    0%   {{ opacity: {t['glow_opacity']}; transform: scale(1); }}
    100% {{ opacity: {t['glow_opacity'] * 0.6:.2f}; transform: scale(1.15); }}
  }}
  @keyframes pulse2 {{
    0%   {{ opacity: {t['glow_opacity'] * 0.8:.2f}; transform: scale(1); }}
    100% {{ opacity: {t['glow_opacity'] * 0.5:.2f}; transform: scale(1.2); }}
  }}
  @keyframes pulse3 {{
    0%   {{ opacity: {t['glow_opacity'] * 0.7:.2f}; transform: scale(1); }}
    100% {{ opacity: {t['glow_opacity'] * 0.45:.2f}; transform: scale(1.1); }}
  }}
  @keyframes helixSway {{
    0%   {{ transform: rotate(-2deg); }}
    100% {{ transform: rotate(2deg); }}
  }}
  @keyframes helixFlow {{
    0%   {{ stroke-dashoffset: 0; }}
    100% {{ stroke-dashoffset: -40; }}
  }}
  @keyframes statusPulse {{
    0%, 100% {{ opacity: 1; r: 5; }}
    50% {{ opacity: 0.5; r: 7; }}
  }}
  @keyframes ringRot {{
    0%   {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
  }}

  /* ── Respect reduced motion ── */
  @media (prefers-reduced-motion: reduce) {{
    .slideUp {{ animation: none; opacity: 1; transform: none; }}
    .floatA, .floatB, .floatC,
    .helixRotate, .orbPulse1, .orbPulse2, .orbPulse3,
    .statusDot, .cursor, .helixDash, .ringRotate {{
      animation: none;
    }}
  }}
</style>

<g clip-path="url(#cardClip)">
  <!-- ▸ Base background -->
  <rect width="{W}" height="{H}" fill="url(#bgGrad)"/>

  <!-- ▸ Subtle grid mesh -->
  <rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#gridMask)"/>
  <rect width="{W}" height="{H}" fill="url(#dotGrid)" mask="url(#gridMask)" opacity="0.5"/>

  <!-- ▸ Floating geometric shapes -->
  {geo_shapes}

  <!-- ▸ Glowing orbs -->
  <g filter="url(#glowStrong)">
    <circle class="orbPulse1" cx="860" cy="100" r="110" fill="{t['accent1']}" opacity="{t['glow_opacity']}"/>
    <circle class="orbPulse2" cx="1050" cy="240" r="100" fill="{t['accent2']}" opacity="{t['glow_opacity'] * 0.8:.2f}"/>
    <circle class="orbPulse3" cx="750" cy="300" r="80" fill="{t['accent3']}" opacity="{t['glow_opacity'] * 0.6:.2f}"/>
    <circle class="orbPulse1 floatB" cx="350" cy="50" r="60" fill="{t['accent2']}" opacity="{t['glow_opacity'] * 0.25:.2f}"/>
    <circle class="orbPulse2 floatA" cx="200" cy="320" r="50" fill="{t['accent1']}" opacity="{t['glow_opacity'] * 0.2:.2f}"/>
  </g>

  <!-- ▸ DNA Helix (right side) -->
  <g class="helixRotate" opacity="0.7">
    <!-- Strand 1 -->
    <path d="{helix1}" fill="none" stroke="{t['accent1']}" stroke-width="2" opacity="0.6"
          stroke-dasharray="8 4" class="helixDash"/>
    <!-- Strand 2 -->
    <path d="{helix2}" fill="none" stroke="{t['accent2']}" stroke-width="2" opacity="0.5"
          stroke-dasharray="8 4" class="helixDash" style="animation-delay:-2s"/>
    <!-- Rungs -->
    <g stroke="{t['accent3']}" stroke-width="0.8" opacity="0.25">
      {helix_rungs}
    </g>
    <!-- Node dots along helix -->
    <g fill="{t['accent1']}" opacity="0.5">
      <circle cx="{hx_cx + hx_amp}" cy="{hx_cy - hx_len * 0.35:.0f}" r="3"/>
      <circle cx="{hx_cx - hx_amp}" cy="{hx_cy + hx_len * 0.15:.0f}" r="2.5"/>
      <circle cx="{hx_cx + hx_amp * 0.7:.0f}" cy="{hx_cy + hx_len * 0.4:.0f}" r="2"/>
    </g>
    <g fill="{t['accent2']}" opacity="0.4">
      <circle cx="{hx_cx - hx_amp}" cy="{hx_cy - hx_len * 0.35:.0f}" r="2.5"/>
      <circle cx="{hx_cx + hx_amp}" cy="{hx_cy + hx_len * 0.15:.0f}" r="3"/>
    </g>
  </g>

  <!-- ▸ Rotating geometric ring -->
  <g class="ringRotate" opacity="0.2">
    <circle cx="{hx_cx}" cy="{hx_cy}" r="160" fill="none" stroke="url(#helixGrad)" stroke-width="0.8" stroke-dasharray="3 9"/>
  </g>
  <circle cx="{hx_cx}" cy="{hx_cy}" r="180" fill="none" stroke="{t['accent1']}" stroke-width="0.4" opacity="0.06" stroke-dasharray="1 15"/>

  <!-- ▸ Floating code symbols -->
  {float_syms}

  <!-- ▸ Glassmorphism panel -->
  <g class="slideUp" style="animation-delay:0.05s">
    <rect x="45" y="40" width="620" height="300" rx="16"
          fill="{t['glass']}" stroke="{t['border']}" stroke-width="1"/>
    <!-- Inner highlight line (top edge of glass) -->
    <line x1="61" y1="40.5" x2="649" y2="40.5" stroke="{t['border_strong']}" stroke-width="0.5" opacity="0.5"/>
  </g>

  <!-- ▸ Kicker line with blinking cursor -->
  <g class="slideUp" style="animation-delay:0.15s">
    <text x="80" y="95" class="kicker">&gt; initializing anik.dev ...</text>
    <rect x="302" y="82" width="9" height="16" rx="1" class="cursor" opacity="0.9"/>
  </g>

  <!-- ▸ Name -->
  <g class="slideUp" style="animation-delay:0.25s">
    <text x="78" y="160" class="name">Md Abu Sayum Anik</text>
  </g>

  <!-- ▸ Subtitle with role -->
  <g class="slideUp" style="animation-delay:0.35s">
    <text x="80" y="198" class="sub">Software Engineer · CSE at United International University</text>
  </g>

  <!-- ▸ Status indicator -->
  <g class="slideUp" style="animation-delay:0.42s">
    <circle cx="88" cy="235" r="5" fill="{t['accent4']}" class="statusDot" filter="url(#statusGlow)"/>
    <circle cx="88" cy="235" r="5" fill="{t['accent4']}" opacity="0.6"/>
    <text x="102" y="239" class="status">Available for opportunities</text>
  </g>

  <!-- ▸ Tag chips -->
  <g>
    {chips_svg}
  </g>

  <!-- ▸ Corner decorations -->
  {corners}

  <!-- ▸ Ambient horizontal line accent -->
  <line x1="80" y1="215" x2="340" y2="215" stroke="url(#chipGrad)" stroke-width="0.5" opacity="0.4" class="slideUp" style="animation-delay:0.4s"/>
  <line x1="80" y1="265" x2="580" y2="265" stroke="url(#chipGrad)" stroke-width="0.5" opacity="0.25" class="slideUp" style="animation-delay:0.48s"/>
</g>

<!-- ▸ Card outer border -->
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{t['border']}" stroke-width="1"/>

</svg>
"""


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, theme in THEMES.items():
        path = OUT / f"header-{name}.svg"
        path.write_text(render(theme), encoding="utf-8")
        print(f"  ✓ {path}")
    print("Done — headers generated.")
