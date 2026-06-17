import os
import urllib.request
import json
import re

def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN is missing. Using fallback mock data.")
        render_svg(520, 48, 18, 12, 14, 2)
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    # GraphQL Query to fetch user stats
    query = """
    query {
      user(login: "Anik-tB") {
        repositories(first: 100, ownerAffiliations: OWNER) {
          totalCount
          nodes {
            stargazerCount
          }
        }
        contributionsCollection {
          totalCommitContributions
          totalPullRequestContributions
          totalIssueContributions
        }
        followers {
          totalCount
        }
      }
    }
    """

    try:
        req = urllib.request.Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": query}).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            
            if "errors" in res_data:
                print("GraphQL errors:", res_data["errors"])
                raise Exception("GraphQL Query failed")

            user_data = res_data["data"]["user"]
            
            # Extract statistics
            repos = user_data["repositories"]["totalCount"]
            stars = sum(node["stargazerCount"] for node in user_data["repositories"]["nodes"])
            commits = user_data["contributionsCollection"]["totalCommitContributions"]
            prs = user_data["contributionsCollection"]["totalPullRequestContributions"]
            issues = user_data["contributionsCollection"]["totalIssueContributions"]
            followers = user_data["followers"]["totalCount"]

            print(f"Stats loaded: Commits={commits}, Repos={repos}, Stars={stars}, PRs={prs}, Issues={issues}, Followers={followers}")
            render_svg(commits, repos, stars, prs, issues, followers)

    except Exception as e:
        print(f"Error fetching data: {e}. Falling back to default stats.")
        # Fallback values if API fails
        render_svg(450, 12, 15, 8, 10, 2)

def render_svg(commits, repos, stars, prs, issues, followers):
    # Calculations for RPG HUD
    level = 10 + (commits // 30) + (stars * 2)
    
    # HP (Commits based)
    max_hp = max(100, ((commits // 100) + 1) * 100)
    hp_percent = min(100, (commits / max_hp) * 100)
    
    # MP (Stars based)
    max_mp = max(50, ((stars // 5) + 1) * 5)
    mp_percent = min(100, (stars / max_mp) * 100)
    
    # EXP (Repos based)
    max_exp = 50
    exp_percent = min(100, (repos / max_exp) * 100)

    # Attributes mapping
    strength = commits
    agility = prs * 8 + 10
    intelligence = repos * 5 + 15
    vitality = issues * 6 + 12
    luck = followers * 15 + 5

    # SVG design
    svg_content = f"""<svg width="800" height="380" viewBox="0 0 800 380" fill="none" xmlns="http://www.w3.org/2000/svg">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&amp;family=Share+Tech+Mono&amp;display=swap');
        
        .bg {{
            fill: #08080f;
            stroke: #BD00FF;
            stroke-width: 2;
            rx: 16px;
        }}
        .grid {{
            stroke: #16162a;
            stroke-width: 1;
            stroke-dasharray: 4 4;
        }}
        .text-mono {{
            font-family: 'Share Tech Mono', monospace;
            fill: #C9D1D9;
        }}
        .text-header {{
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            fill: #00F0FF;
            letter-spacing: 2px;
        }}
        .text-neon {{
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            fill: #BD00FF;
            text-shadow: 0 0 8px #BD00FF;
        }}
        .text-green {{
            fill: #00FF41;
            text-shadow: 0 0 8px #00FF41;
        }}
        .bar-bg {{
            fill: #141424;
            rx: 4px;
        }}
        .bar-fill-hp {{
            fill: #00FF41;
            filter: drop-shadow(0px 0px 4px #00FF41);
            rx: 4px;
        }}
        .bar-fill-mp {{
            fill: #BD00FF;
            filter: drop-shadow(0px 0px 4px #BD00FF);
            rx: 4px;
        }}
        .bar-fill-exp {{
            fill: #00F0FF;
            filter: drop-shadow(0px 0px 4px #00F0FF);
            rx: 4px;
        }}
        .neon-border {{
            stroke: #BD00FF;
            filter: drop-shadow(0px 0px 5px #BD00FF);
        }}
        .neon-border-cyan {{
            stroke: #00F0FF;
            filter: drop-shadow(0px 0px 5px #00F0FF);
        }}
        .status-dot {{
            fill: #00FF41;
            animation: blink 1.5s infinite;
        }}
        .scan-line {{
            stroke: #00F0FF;
            stroke-opacity: 0.15;
            stroke-width: 2;
            animation: scan 6s linear infinite;
        }}
        .inv-slot {{
            fill: #0d0d17;
            stroke: #1b1b33;
            stroke-width: 1.5;
            rx: 8px;
            transition: all 0.3s;
        }}
        .inv-slot:hover {{
            stroke: #00F0FF;
            fill: #141426;
            filter: drop-shadow(0px 0px 6px #00F0FF);
        }}
        @keyframes blink {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.3; }}
        }}
        @keyframes scan {{
            0% {{ y1: 10; y2: 10; }}
            50% {{ y1: 370; y2: 370; }}
            100% {{ y1: 10; y2: 10; }}
        }}
    </style>

    <!-- Background card with neon border -->
    <rect x="5" y="5" width="790" height="370" class="bg" />

    <!-- Technical grid overlay -->
    <line x1="5" y1="60" x2="795" y2="60" stroke="#1b1b33" stroke-width="2" />
    <line x1="420" y1="60" x2="420" y2="260" stroke="#1b1b33" stroke-width="2" />
    <line x1="5" y1="260" x2="795" y2="260" stroke="#1b1b33" stroke-width="2" />

    <!-- Grid patterns -->
    <path d="M 0,110 L 800,110 M 0,160 L 800,160 M 0,210 L 800,210" class="grid" />
    <path d="M 120,60 L 120,260 M 270,60 L 270,260 M 550,60 L 550,260 M 670,60 L 670,260" class="grid" />

    <!-- Scan line animation -->
    <line x1="6" y1="10" x2="794" y2="10" class="scan-line" />

    <!-- Header info -->
    <text x="30" y="38" class="text-header" font-size="20">PLAYER IDENTITY HUD</text>
    <text x="360" y="36" class="text-mono" font-size="14">v3.5 // CONSOLE_MODE</text>

    <!-- Status indicator -->
    <circle cx="680" cy="32" r="5" class="status-dot" />
    <text x="695" y="37" class="text-mono text-green" font-size="14" font-weight="bold">SYSTEM ACTIVE</text>

    <!-- Left side: Core Status Bars -->
    <text x="30" y="92" class="text-neon" font-size="15">HP [COMMITS]</text>
    <text x="340" y="92" class="text-mono" font-size="14" text-anchor="end">{commits} / {max_hp}</text>
    <rect x="30" y="100" width="360" height="15" class="bar-bg" />
    <rect x="30" y="100" width="{hp_percent * 3.6}" height="15" class="bar-fill-hp" />

    <text x="30" y="147" class="text-neon" font-size="15" fill="#BD00FF">MP [STARS]</text>
    <text x="340" y="147" class="text-mono" font-size="14" text-anchor="end">{stars} / {max_mp}</text>
    <rect x="30" y="155" width="360" height="15" class="bar-bg" />
    <rect x="30" y="155" width="{mp_percent * 3.6}" height="15" class="bar-fill-mp" />

    <text x="30" y="202" class="text-neon" font-size="15" fill="#00F0FF">EXP [REPOSITORIES]</text>
    <text x="340" y="202" class="text-mono" font-size="14" text-anchor="end">{repos} / {max_exp}</text>
    <rect x="30" y="210" width="360" height="15" class="bar-bg" />
    <rect x="30" y="210" width="{exp_percent * 3.6}" height="15" class="bar-fill-exp" />

    <!-- Center Separator details -->
    <text x="445" y="92" class="text-header" font-size="14" fill="#00F0FF">LEVEL: {level}</text>
    <text x="445" y="112" class="text-mono" font-size="13" fill="#8888aa">CLASS: FULL-STACK ENGINEER</text>

    <!-- Right side: RPG Attributes -->
    <text x="445" y="150" class="text-mono" font-size="15">STR (Strength)  :</text>
    <text x="600" y="150" class="text-mono text-green" font-size="15" font-weight="bold">{strength}</text>

    <text x="445" y="175" class="text-mono" font-size="15">AGI (Agility)   :</text>
    <text x="600" y="175" class="text-mono text-green" font-size="15" font-weight="bold">{agility}</text>

    <text x="445" y="200" class="text-mono" font-size="15">INT (Intellect) :</text>
    <text x="600" y="200" class="text-mono text-green" font-size="15" font-weight="bold">{intelligence}</text>

    <text x="445" y="225" class="text-mono" font-size="15">VIT (Vitality)  :</text>
    <text x="600" y="225" class="text-mono text-green" font-size="15" font-weight="bold">{vitality}</text>

    <text x="445" y="250" class="text-mono" font-size="15">LUK (Luck)      :</text>
    <text x="600" y="250" class="text-mono text-green" font-size="15" font-weight="bold">{luck}</text>

    <!-- Bottom: Inventory / Core Arsenal -->
    <text x="30" y="290" class="text-header" font-size="14" fill="#00F0FF">EQUIPPED ARSENAL &amp; RELICS</text>

    <!-- Inventory Slots -->
    <g transform="translate(30, 305)">
        <!-- Java Slot -->
        <rect x="0" y="0" width="105" height="50" class="inv-slot" />
        <text x="12" y="30" class="text-mono" font-size="14" font-weight="bold" fill="#F89820">JAVA</text>
        <text x="93" y="17" class="text-mono" font-size="10" text-anchor="end" fill="#888">Lvl.9</text>
        <text x="93" y="40" class="text-mono" font-size="10" text-anchor="end" fill="#00FF41">MAX</text>

        <!-- Kotlin Slot -->
        <rect x="120" y="0" width="105" height="50" class="inv-slot" />
        <text x="132" y="30" class="text-mono" font-size="14" font-weight="bold" fill="#BD00FF">KOTLIN</text>
        <text x="213" y="17" class="text-mono" font-size="10" text-anchor="end" fill="#888">Lvl.8</text>
        <text x="213" y="40" class="text-mono" font-size="10" text-anchor="end" fill="#BD00FF">EPIC</text>

        <!-- TypeScript Slot -->
        <rect x="240" y="0" width="105" height="50" class="inv-slot" />
        <text x="252" y="30" class="text-mono" font-size="14" font-weight="bold" fill="#3178C6">TYPESCRIPT</text>
        <text x="333" y="17" class="text-mono" font-size="10" text-anchor="end" fill="#888">Lvl.8</text>
        <text x="333" y="40" class="text-mono" font-size="10" text-anchor="end" fill="#BD00FF">EPIC</text>

        <!-- Python Slot -->
        <rect x="360" y="0" width="105" height="50" class="inv-slot" />
        <text x="372" y="30" class="text-mono" font-size="14" font-weight="bold" fill="#3776AB">PYTHON</text>
        <text x="453" y="17" class="text-mono" font-size="10" text-anchor="end" fill="#888">Lvl.7</text>
        <text x="453" y="40" class="text-mono" font-size="10" text-anchor="end" fill="#BD00FF">EPIC</text>

        <!-- NextJS Slot -->
        <rect x="480" y="0" width="105" height="50" class="inv-slot" />
        <text x="492" y="30" class="text-mono" font-size="14" font-weight="bold" fill="#ffffff">NEXTJS</text>
        <text x="573" y="17" class="text-mono" font-size="10" text-anchor="end" fill="#888">Lvl.6</text>
        <text x="573" y="40" class="text-mono" font-size="10" text-anchor="end" fill="#00F0FF">RARE</text>

        <!-- Android Slot -->
        <rect x="600" y="0" width="138" height="50" class="inv-slot" />
        <text x="612" y="30" class="text-mono" font-size="14" font-weight="bold" fill="#3DDC84">ANDROID</text>
        <text x="728" y="17" class="text-mono" font-size="10" text-anchor="end" fill="#888">Lvl.8</text>
        <text x="728" y="40" class="text-mono" font-size="10" text-anchor="end" fill="#BD00FF">EPIC</text>
    </g>
</svg>
"""
    # Create assets folder if not exists
    os.makedirs("assets", exist_ok=True)
    with open("assets/rpg-hud.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("RPG HUD SVG rendered successfully to assets/rpg-hud.svg")

if __name__ == "__main__":
    main()
