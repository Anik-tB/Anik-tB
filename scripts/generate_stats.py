"""Render assets/stats-dark.svg and assets/stats-light.svg from live GitHub data.

Every number on the card comes from the GitHub GraphQL API. If the API call
fails, the script exits non-zero and leaves the previous cards untouched rather
than drawing placeholder numbers.
"""

import datetime as dt
import json
import os
import sys
import urllib.request
from html import escape
from pathlib import Path

USER = os.environ.get("PROFILE_USER", "Anik-tB")
OUT = Path(__file__).resolve().parent.parent / "assets"

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    repositories(first: 100, ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false) {
      totalCount
      nodes {
        name
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""

THEMES = {
    "dark": {
        "bg1": "#06080f", "bg2": "#0c1029",
        "panel": "#0d1120", "panel_border": "rgba(255,255,255,0.07)",
        "text": "#f0f4ff", "muted": "#64748b",
        "grid": "rgba(255,255,255,0.04)", "grid_line": "#141830",
        "accent": "#00d4ff", "accent2": "#7c3aed", "accent3": "#f43f5e",
        "glow_opacity": 0.18,
    },
    "light": {
        "bg1": "#fafbff", "bg2": "#f0f2ff",
        "panel": "#ffffff", "panel_border": "rgba(0,0,0,0.06)",
        "text": "#0f172a", "muted": "#64748b",
        "grid": "rgba(0,0,0,0.04)", "grid_line": "#e8ecf4",
        "accent": "#0891b2", "accent2": "#7c3aed", "accent3": "#e11d48",
        "glow_opacity": 0.08,
    },
}

SANS = "Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "'SF Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

# ── SVG icon paths for metric tiles ──
METRIC_ICONS = {
    "contributions": '<path d="M12,2 C8,2 4,5 4,9 C4,14 12,22 12,22 C12,22 20,14 20,9 C20,5 16,2 12,2 Z" fill="none" stroke="url(#iconGrad)" stroke-width="1.8" stroke-linecap="round"/><path d="M12,6 L13.5,9 L17,9.5 L14.5,12 L15,15.5 L12,14 L9,15.5 L9.5,12 L7,9.5 L10.5,9 Z" fill="url(#iconGrad)" opacity="0.5"/>',
    "commits": '<circle cx="12" cy="12" r="4" fill="none" stroke="url(#iconGrad)" stroke-width="1.8"/><line x1="12" y1="2" x2="12" y2="8" stroke="url(#iconGrad)" stroke-width="1.8" stroke-linecap="round"/><line x1="12" y1="16" x2="12" y2="22" stroke="url(#iconGrad)" stroke-width="1.8" stroke-linecap="round"/>',
    "current": '<path d="M13,2 L4,14 H11 L10,22 L20,9 H13 Z" fill="none" stroke="url(#iconGrad)" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>',
    "longest": '<path d="M12,2 L15,8 L22,9 L17,14 L18.5,21 L12,17.5 L5.5,21 L7,14 L2,9 L9,8 Z" fill="none" stroke="url(#iconGrad)" stroke-width="1.8" stroke-linejoin="round"/>',
    "repos": '<path d="M4,4 L4,18 C4,19.1 4.9,20 6,20 L20,20" fill="none" stroke="url(#iconGrad)" stroke-width="1.8" stroke-linecap="round"/><path d="M8,2 L8,16 L20,16 L20,6 L14,6 L12,2 Z" fill="none" stroke="url(#iconGrad)" stroke-width="1.8" stroke-linejoin="round"/>',
}


def fetch():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("GITHUB_TOKEN is not set")
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"Bearer {token}", "User-Agent": "profile-stats"},
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        data = json.load(res)
    if "errors" in data:
        sys.exit(f"GraphQL errors: {data['errors']}")
    return data["data"]["user"]


def summarize(user):
    cc = user["contributionsCollection"]
    days = [d for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    counts = [d["contributionCount"] for d in days]

    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    # Today may not have activity yet, so the current streak may end yesterday
    current = 0
    tail = counts[:-1] if counts and counts[-1] == 0 else counts
    for c in reversed(tail):
        if not c:
            break
        current += 1

    weeks = [sum(d["contributionCount"] for d in w["contributionDays"])
             for w in cc["contributionCalendar"]["weeks"]]
    week_starts = [w["contributionDays"][0]["date"] for w in cc["contributionCalendar"]["weeks"]]

    # Each repo counts equally, so one repo with committed dependencies can't
    # swamp the chart with a language that is mostly vendored code.
    langs = {}
    for repo in user["repositories"]["nodes"]:
        repo_total = sum(e["size"] for e in repo["languages"]["edges"])
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            share, color = langs.get(name, (0, edge["node"]["color"] or "#888888"))
            langs[name] = (share + edge["size"] / repo_total, color)
    total = sum(s for s, _ in langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1][0])[:6]
    top = [(name, size / total * 100, color) for name, (size, color) in top]

    return {
        "contributions": cc["contributionCalendar"]["totalContributions"],
        "commits": cc["totalCommitContributions"],
        "prs": cc["totalPullRequestContributions"],
        "current": current,
        "longest": longest,
        "repos": user["repositories"]["totalCount"],
        "stars": sum(r["stargazerCount"] for r in user["repositories"]["nodes"]),
        "followers": user["followers"]["totalCount"],
        "weeks": weeks,
        "week_starts": week_starts,
        "langs": top,
        "updated": dt.date.today().strftime("%d %b %Y"),
    }


def days(n):
    return f"{n} day" if n == 1 else f"{n} days"


def render(s, t):
    W, H = 1200, 400
    out = []
    add = out.append

    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="GitHub activity for {USER} over the last 12 months">')

    # ── Styles ──
    add(f"""<style>
  .label{{font:600 11px/1 {SANS};fill:{t['muted']};letter-spacing:.08em;text-transform:uppercase}}
  .num{{font:700 28px/1 {SANS};fill:{t['text']}}}
  .small{{font:400 11px/1 {SANS};fill:{t['muted']}}}
  .lang{{font:500 13px/1 {SANS};fill:{t['text']}}}
  .pct{{font:400 12px/1 {MONO};fill:{t['muted']}}}
  .bar{{transform-box:fill-box;transform-origin:bottom;animation:grow 1s cubic-bezier(.16,1,.3,1) both}}
  .fade{{animation:fadeIn .8s ease both}}
  .slideUp{{opacity:0;transform:translateY(12px);animation:slideIn .7s cubic-bezier(.16,1,.3,1) forwards}}
  .langBar{{animation:widthGrow 1.2s cubic-bezier(.16,1,.3,1) both}}
  @keyframes grow{{from{{transform:scaleY(0)}}to{{transform:scaleY(1)}}}}
  @keyframes fadeIn{{from{{opacity:0}}to{{opacity:1}}}}
  @keyframes slideIn{{to{{opacity:1;transform:translateY(0)}}}}
  @keyframes widthGrow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
  @media(prefers-reduced-motion:reduce){{.bar,.fade,.slideUp,.langBar{{animation:none;opacity:1;transform:none}}}}
</style>""")

    # ── Defs ──
    add(f"""<defs>
  <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{t['bg1']}"/><stop offset="100%" stop-color="{t['bg2']}"/>
  </linearGradient>
  <linearGradient id="barGrad" x1="0" y1="1" x2="0" y2="0">
    <stop offset="0%" stop-color="{t['accent']}"/><stop offset="100%" stop-color="{t['accent2']}"/>
  </linearGradient>
  <linearGradient id="iconGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{t['accent']}"/><stop offset="100%" stop-color="{t['accent2']}"/>
  </linearGradient>
  <linearGradient id="accentLine" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{t['accent']}"/><stop offset="50%" stop-color="{t['accent2']}"/><stop offset="100%" stop-color="{t['accent3']}"/>
  </linearGradient>
  <filter id="barGlow" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="3" result="blur"/><feComposite in="SourceGraphic" in2="blur" operator="over"/>
  </filter>
  <pattern id="meshDots" width="28" height="28" patternUnits="userSpaceOnUse">
    <circle cx="14" cy="14" r="0.6" fill="{t['text']}" opacity="0.04"/>
  </pattern>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="16"/></clipPath>
</defs>""")

    # ── Background ──
    add(f'<g clip-path="url(#card)">')
    add(f'<rect width="{W}" height="{H}" fill="url(#bgGrad)"/>')
    add(f'<rect width="{W}" height="{H}" fill="url(#meshDots)"/>')

    # Subtle glow orbs
    add(f'<g filter="url(#barGlow)" opacity="{t["glow_opacity"]}">')
    add(f'  <circle cx="200" cy="80" r="120" fill="{t["accent"]}" opacity="0.4"/>')
    add(f'  <circle cx="800" cy="350" r="100" fill="{t["accent2"]}" opacity="0.3"/>')
    add(f'  <circle cx="1100" cy="100" r="80" fill="{t["accent3"]}" opacity="0.2"/>')
    add(f'</g>')

    # ── Metric tiles ──
    metrics = [
        (f"{s['contributions']:,}", "Contributions", "contributions"),
        (f"{s['commits']:,}", "Commits", "commits"),
        (days(s["current"]), "Current Streak", "current"),
        (days(s["longest"]), "Longest Streak", "longest"),
        (f"{s['repos']}", "Public Repos", "repos"),
    ]
    tile_w = (W - 60 - 4 * 14) / 5
    for i, (value, label, icon_key) in enumerate(metrics):
        x = 30 + i * (tile_w + 14)
        delay = i * 60
        icon_svg = METRIC_ICONS[icon_key]

        add(f'<g class="slideUp" style="animation-delay:{delay}ms">')
        # Tile background
        add(f'  <rect x="{x:.1f}" y="26" width="{tile_w:.1f}" height="88" rx="12" '
            f'fill="{t["panel"]}" stroke="{t["panel_border"]}"/>')
        # Gradient accent left border
        add(f'  <rect x="{x:.1f}" y="38" width="3" height="48" rx="1.5" fill="url(#accentLine)" opacity="0.8"/>')
        # Icon
        add(f'  <g transform="translate({x + 14:.1f}, 38) scale(0.85)">{icon_svg}</g>')
        # Number
        add(f'  <text x="{x + 40:.1f}" y="62" class="num">{escape(value)}</text>')
        # Label
        add(f'  <text x="{x + 14:.1f}" y="100" class="label">{escape(label)}</text>')
        add(f'</g>')

    # ── Weekly contributions chart ──
    cx, cy, cw, ch = 30, 140, 720, 228
    add(f'<g class="fade" style="animation-delay:350ms">')
    add(f'  <rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="14" '
        f'fill="{t["panel"]}" stroke="{t["panel_border"]}"/>')
    add(f'  <text x="{cx + 20}" y="{cy + 28}" class="label">Weekly Contributions · Last 12 Months</text>')

    weeks = s["weeks"]
    peak = max(weeks) or 1
    px, pw = cx + 20, cw - 40
    base, ph = cy + ch - 36, ch - 80

    # Grid lines
    for frac in (0.25, 0.5, 0.75, 1.0):
        y = base - ph * frac
        add(f'  <line x1="{px}" x2="{px + pw}" y1="{y:.1f}" y2="{y:.1f}" '
            f'stroke="{t["grid_line"]}" stroke-dasharray="2 5"/>')
        if frac in (0.5, 1.0):
            add(f'  <text x="{px + pw + 4}" y="{y + 4:.1f}" class="pct" font-size="10">{round(peak * frac)}</text>')

    add(f'  <line x1="{px}" x2="{px + pw}" y1="{base}" y2="{base}" stroke="{t["panel_border"]}"/>')

    step = pw / len(weeks)
    bw = max(3.0, step - 2.5)
    for i, v in enumerate(weeks):
        h = max(2.5, ph * v / peak) if v else 2.5
        fill = "url(#barGrad)" if v else t["grid"]
        add(f'  <rect class="bar" style="animation-delay:{i * 14}ms" '
            f'x="{px + i * step:.1f}" y="{base - h:.1f}" '
            f'width="{bw:.1f}" height="{h:.1f}" rx="2" fill="{fill}">'
            f'<title>{s["week_starts"][i]}: {v}</title></rect>')

    # Month labels
    seen = set()
    for i, start in enumerate(s["week_starts"]):
        d = dt.date.fromisoformat(start)
        key = (d.year, d.month)
        if d.day <= 7 and key not in seen:
            seen.add(key)
            if len(seen) % 2:
                add(f'  <text x="{px + i * step:.1f}" y="{base + 18}" class="small">{d.strftime("%b")}</text>')
    add(f'</g>')

    # ── Languages panel ──
    lx, ly, lw, lh = 766, 140, 404, 228
    add(f'<g class="fade" style="animation-delay:450ms">')
    add(f'  <rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="14" '
        f'fill="{t["panel"]}" stroke="{t["panel_border"]}"/>')
    add(f'  <text x="{lx + 20}" y="{ly + 28}" class="label">Languages · Share Per Repo</text>')

    # Language bar
    bx, by, bwid, bh = lx + 20, ly + 48, lw - 40, 10
    add(f'  <clipPath id="lc"><rect x="{bx}" y="{by}" width="{bwid}" height="{bh}" rx="5"/></clipPath>')
    add(f'  <g clip-path="url(#lc)">')
    used = sum(p for _, p, _ in s["langs"])
    x = bx
    for name, pct, color in s["langs"]:
        w = bwid * pct / used
        add(f'    <rect class="langBar" x="{x:.1f}" y="{by}" width="{w + 0.5:.1f}" height="{bh}" fill="{color}"/>')
        x += w
    add(f'  </g>')

    # Language entries (2 columns)
    for i, (name, pct, color) in enumerate(s["langs"]):
        col, row = i % 2, i // 2
        tx = bx + col * (bwid / 2)
        ty = by + 32 + row * 40
        delay = 500 + i * 80
        add(f'  <g class="slideUp" style="animation-delay:{delay}ms">')
        add(f'    <rect x="{tx}" y="{ty - 9}" width="10" height="10" rx="3" fill="{color}"/>')
        add(f'    <text x="{tx + 18}" y="{ty}" class="lang">{escape(name)}</text>')
        add(f'    <text x="{tx + 18}" y="{ty + 18}" class="pct">{pct:.1f}%</text>')
        add(f'  </g>')

    add(f'</g>')

    # ── Footer ──
    add(f'<text x="{W - 30}" y="{H - 10}" class="pct" text-anchor="end" font-size="10" opacity="0.6">'
        f'⭐ {s["stars"]} stars · 👥 {s["followers"]} followers · updated {s["updated"]}</text>')

    add(f'</g>')  # close clip-path group

    # Outer border
    add(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{t["panel_border"]}"/>')
    add("</svg>")
    return "\n".join(out)


def main():
    stats = summarize(fetch())
    OUT.mkdir(exist_ok=True)
    for name, theme in THEMES.items():
        (OUT / f"stats-{name}.svg").write_text(render(stats, theme), encoding="utf-8")
    print(json.dumps({k: v for k, v in stats.items() if k not in ("weeks", "week_starts")}, indent=2))


if __name__ == "__main__":
    main()
