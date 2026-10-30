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
        "bg": "#0d0b14", "panel": "#15121f", "border": "#2a2440",
        "text": "#ece9f8", "muted": "#8f88b0", "grid": "#231e33",
        "accent": "#a08ae6", "accent2": "#7d95f5", "accent3": "#c29af0",
    },
    "light": {
        "bg": "#fbfaff", "panel": "#f3f0fc", "border": "#e2dcf5",
        "text": "#1b1530", "muted": "#6b6390", "grid": "#e9e4f7",
        "accent": "#7b61d6", "accent2": "#4f6fe8", "accent3": "#a46be0",
    },
}

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"


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
    W, H = 1000, 340
    out = []
    add = out.append
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="GitHub activity for {USER} over the last 12 months">')
    add(f"""<style>
  .label{{font:500 12px {SANS};fill:{t['muted']};letter-spacing:.06em;text-transform:uppercase}}
  .num{{font:600 30px {SANS};fill:{t['text']}}}
  .small{{font:400 12px {SANS};fill:{t['muted']}}}
  .lang{{font:500 13px {SANS};fill:{t['text']}}}
  .pct{{font:400 12px {MONO};fill:{t['muted']}}}
  .bar{{transform-box:fill-box;transform-origin:bottom;animation:grow .9s cubic-bezier(.22,1,.36,1) both}}
  .fade{{animation:fade .8s ease both}}
  @keyframes grow{{from{{transform:scaleY(0)}}to{{transform:scaleY(1)}}}}
  @keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
  @media (prefers-reduced-motion:reduce){{.bar,.fade{{animation:none}}}}
</style>""")
    add(f"""<defs>
  <linearGradient id="g" x1="0" y1="1" x2="0" y2="0">
    <stop offset="0" stop-color="{t['accent2']}"/><stop offset="1" stop-color="{t['accent3']}"/>
  </linearGradient>
</defs>""")
    add(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="{t["bg"]}" stroke="{t["border"]}"/>')

    # Metric row
    metrics = [
        (f"{s['contributions']:,}", "Contributions"),
        (f"{s['commits']:,}", "Commits"),
        (days(s["current"]), "Current streak"),
        (days(s["longest"]), "Longest streak"),
        (f"{s['repos']}", "Public repos"),
    ]
    tile_w = (W - 48 - 4 * 12) / 5
    for i, (value, label) in enumerate(metrics):
        x = 24 + i * (tile_w + 12)
        add(f'<g class="fade" style="animation-delay:{i * 60}ms">')
        add(f'<rect x="{x:.1f}" y="24" width="{tile_w:.1f}" height="76" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/>')
        add(f'<text x="{x + 16:.1f}" y="64" class="num">{escape(value)}</text>')
        add(f'<text x="{x + 16:.1f}" y="86" class="label">{escape(label)}</text>')
        add("</g>")

    # Weekly contributions chart
    cx, cy, cw, ch = 24, 128, 600, 188
    add(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/>')
    add(f'<text x="{cx + 16}" y="{cy + 26}" class="label">Weekly contributions · last 12 months</text>')
    weeks = s["weeks"]
    peak = max(weeks) or 1
    px, pw, base, ph = cx + 16, cw - 32, cy + ch - 34, ch - 78
    for frac in (0.5, 1.0):
        y = base - ph * frac
        add(f'<line x1="{px}" x2="{px + pw}" y1="{y:.1f}" y2="{y:.1f}" stroke="{t["grid"]}" stroke-dasharray="3 4"/>')
        add(f'<text x="{px + pw}" y="{y - 4:.1f}" class="pct" text-anchor="end">{round(peak * frac)}</text>')
    add(f'<line x1="{px}" x2="{px + pw}" y1="{base}" y2="{base}" stroke="{t["border"]}"/>')
    step = pw / len(weeks)
    bw = max(2.0, step - 3)
    for i, v in enumerate(weeks):
        h = max(2.0, ph * v / peak) if v else 2.0
        fill = "url(#g)" if v else t["grid"]
        add(f'<rect class="bar" style="animation-delay:{i * 12}ms" x="{px + i * step:.1f}" y="{base - h:.1f}" '
            f'width="{bw:.1f}" height="{h:.1f}" rx="1.5" fill="{fill}"><title>{s["week_starts"][i]}: {v}</title></rect>')
    seen = set()
    for i, start in enumerate(s["week_starts"]):
        d = dt.date.fromisoformat(start)
        key = (d.year, d.month)
        if d.day <= 7 and key not in seen and i % 1 == 0:
            seen.add(key)
            if len(seen) % 2:
                add(f'<text x="{px + i * step:.1f}" y="{base + 18}" class="small">{d.strftime("%b")}</text>')

    # Languages
    lx, ly, lw, lh = 640, 128, 336, 188
    add(f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/>')
    add(f'<text x="{lx + 16}" y="{ly + 26}" class="label">Languages · share per repo</text>')
    bx, by, bwid = lx + 16, ly + 42, lw - 32
    add(f'<clipPath id="lc"><rect x="{bx}" y="{by}" width="{bwid}" height="8" rx="4"/></clipPath><g clip-path="url(#lc)">')
    used = sum(p for _, p, _ in s["langs"])
    x = bx
    for name, pct, color in s["langs"]:
        w = bwid * pct / used
        add(f'<rect x="{x:.1f}" y="{by}" width="{w + 0.5:.1f}" height="8" fill="{color}"/>')
        x += w
    add("</g>")
    for i, (name, pct, color) in enumerate(s["langs"]):
        col, row = i % 2, i // 2
        tx, ty = bx + col * (bwid / 2), by + 40 + row * 34
        add(f'<g class="fade" style="animation-delay:{300 + i * 60}ms">')
        add(f'<circle cx="{tx + 5}" cy="{ty - 4}" r="5" fill="{color}"/>')
        add(f'<text x="{tx + 18}" y="{ty}" class="lang">{escape(name)}</text>')
        add(f'<text x="{tx + 18}" y="{ty + 16}" class="pct">{pct:.1f}%</text>')
        add("</g>")

    add(f'<text x="{W - 24}" y="{H - 8}" class="pct" text-anchor="end" font-size="10">'
        f'{s["stars"]} stars · {s["followers"]} followers · updated {s["updated"]}</text>')
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
