#!/usr/bin/env python3
"""
Persona 3 Reload (P3R) SVG Profile Asset Generator
Generates responsive, animated SVGs and profile assets styled after
Persona 3 Reload's water splash, midnight blue palettes, and sleek angled HUD.
"""

import base64
import json
import math
import os
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT_DIR, "p3r.config.json")
OUTPUT_DIR = os.path.join(ROOT_DIR, "assets", "p3r")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def esc(text):
    """Escape XML entities."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )

def p3r_base_styles():
    """Shared CSS animation and typography definitions for P3R SVGs."""
    return """
    @keyframes waveDrift {
      0% { transform: translateX(0px) translateY(0px); }
      50% { transform: translateX(-35px) translateY(-5px); }
      100% { transform: translateX(0px) translateY(0px); }
    }
    @keyframes waveSlow {
      0% { transform: translateX(0px) translateY(0px) scaleY(1); }
      50% { transform: translateX(25px) translateY(6px) scaleY(1.08); }
      100% { transform: translateX(0px) translateY(0px) scaleY(1); }
    }
    @keyframes ripplePulse {
      0% { r: 10px; opacity: 0.9; stroke-width: 2.5; }
      50% { r: 75px; opacity: 0.4; stroke-width: 1.5; }
      100% { r: 140px; opacity: 0; stroke-width: 0.5; }
    }
    @keyframes ripplePulse2 {
      0% { r: 5px; opacity: 0.8; stroke-width: 2; }
      50% { r: 90px; opacity: 0.3; stroke-width: 1.2; }
      100% { r: 180px; opacity: 0; stroke-width: 0.5; }
    }
    @keyframes bubbleRise1 {
      0% { transform: translateY(0px) scale(0.7); opacity: 0; }
      20% { opacity: 0.8; }
      80% { opacity: 0.6; }
      100% { transform: translateY(-160px) scale(1.2); opacity: 0; }
    }
    @keyframes bubbleRise2 {
      0% { transform: translateY(0px) scale(0.9); opacity: 0; }
      30% { opacity: 0.9; }
      85% { opacity: 0.5; }
      100% { transform: translateY(-210px) scale(1.4); opacity: 0; }
    }
    @keyframes dialSpinCW {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }
    @keyframes dialSpinCCW {
      from { transform: rotate(360deg); }
      to { transform: rotate(0deg); }
    }
    @keyframes cyanGlow {
      0%, 100% { filter: drop-shadow(0 0 4px #00d2ff); opacity: 0.9; }
      50% { filter: drop-shadow(0 0 12px #00ffff); opacity: 1; }
    }
    @keyframes blinkCursor {
      0%, 49% { opacity: 1; }
      50%, 100% { opacity: 0; }
    }
    @keyframes gaugeFill {
      0% { width: 0%; }
      100% { width: 100%; }
    }
    .font-hud {
      font-family: 'SF Mono', 'Fira Code', 'JetBrains Mono', 'Roboto Mono', Consolas, monospace;
    }
    .font-p3r {
      font-family: 'Helvetica Neue', 'Arial Black', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-weight: 900;
    }
    .font-body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    @media (prefers-reduced-motion: reduce) {
      *, .wave-anim, .ripple-anim, .bubble-anim, .dial-anim {
        animation: none !important;
      }
    }
    """

def gen_hero_svg(cfg):
    user = cfg["user"]
    w, h = 900, 360

    # Load hero background artwork
    bg_path = os.path.join(OUTPUT_DIR, "hero-bg.jpg")
    b64_img = ""
    if os.path.exists(bg_path):
        with open(bg_path, "rb") as f:
            b64_img = base64.b64encode(f.read()).decode("ascii")

    name_display = user.get("name", "Camilo Rodríguez").upper()
    title_display = user.get("title", "SOFTWARE ENGINEER").upper()
    arcana_display = user.get("arcana", "THE CHARIOT").upper()
    status_display = user.get("status", "SYS://READY").upper()

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(name_display)} - Persona 3 Reload Profile">
  <defs>
    <style>
      {p3r_base_styles()}
      @keyframes oceanSway {{
        0% {{ transform: translateY(0px) rotate(0deg); }}
        35% {{ transform: translateY(8px) rotate(-0.7deg); }}
        70% {{ transform: translateY(-5px) rotate(0.4deg); }}
        100% {{ transform: translateY(0px) rotate(0deg); }}
      }}
      .ocean-motion {{
        transform-origin: 200px 180px;
        animation: oceanSway 7.5s ease-in-out infinite;
      }}
      .b1 {{ animation: bubbleRise1 5.5s ease-in infinite; }}
      .b2 {{ animation: bubbleRise2 7s ease-in infinite 1.2s; }}
      .b3 {{ animation: bubbleRise1 4.8s ease-in infinite 2.5s; }}
      .b4 {{ animation: bubbleRise2 6.2s ease-in infinite 3.8s; }}
      .b5 {{ animation: bubbleRise1 5.2s ease-in infinite 0.7s; }}
      .caustic {{ animation: waveDrift 6s ease-in-out infinite alternate; }}
      .blink {{ animation: blinkCursor 1s steps(1) infinite; }}
      .p3r-glow {{ animation: cyanGlow 3s ease-in-out infinite; }}
    </style>

    <!-- Deep Blue Ocean Background Gradient matching P3R artwork -->
    <linearGradient id="oceanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#00efff" />
      <stop offset="8%" stop-color="#0077ff" />
      <stop offset="30%" stop-color="#003cdb" />
      <stop offset="70%" stop-color="#001882" />
      <stop offset="100%" stop-color="#000b40" />
    </linearGradient>

    <!-- Seamless Blend Mask for Artwork Edge -->
    <linearGradient id="blendMaskGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="1" />
      <stop offset="65%" stop-color="#ffffff" stop-opacity="1" />
      <stop offset="92%" stop-color="#ffffff" stop-opacity="0.1" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
    </linearGradient>
    <mask id="artMask">
      <rect x="-20" y="-20" width="672" height="{h+40}" fill="url(#blendMaskGrad)" />
    </mask>

    <linearGradient id="cyanRibbonGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#004488" stop-opacity="0.9" />
      <stop offset="50%" stop-color="#00a3e0" stop-opacity="0.95" />
      <stop offset="100%" stop-color="#00e5ff" stop-opacity="1" />
    </linearGradient>

    <clipPath id="heroFrame">
      <rect width="{w}" height="{h}" rx="12" />
    </clipPath>
  </defs>

  <g clip-path="url(#heroFrame)">
    <!-- Base Ocean Water Canvas -->
    <rect width="{w}" height="{h}" fill="url(#oceanGrad)" />

    <!-- Authentic Persona 3 Reload Makoto Yuki Submerged Artwork with Ocean Motion -->
    <g mask="url(#artMask)">
      <g class="ocean-motion">
        <image href="data:image/jpeg;base64,{b64_img}" xlink:href="data:image/jpeg;base64,{b64_img}" x="-15" y="-15" width="672" height="{h+30}" preserveAspectRatio="xMinYMid slice" />
      </g>
    </g>

    <!-- Top Water Surface Shimmer Caustics on the Right -->
    <g class="caustic" opacity="0.65">
      <path d="M420,18 C470,8 520,24 580,14 C640,6 700,22 760,12 C820,4 860,20 910,12" fill="none" stroke="#00ffff" stroke-width="2.5" />
      <path d="M460,32 C510,22 560,38 620,28 C680,18 740,34 800,24 C850,16 880,30 920,22" fill="none" stroke="#ffffff" stroke-width="1.2" opacity="0.7" />
    </g>

    <!-- Translucent Rising Water Bubbles -->
    <g transform="translate(520, 340)" class="b1"><circle r="4.5" fill="#00ffff" opacity="0.65" /><circle r="1.5" cx="-1" cy="-1" fill="#fff" /></g>
    <g transform="translate(610, 350)" class="b2"><circle r="6.5" fill="#00d2ff" opacity="0.55" /><circle r="2" cx="-1.5" cy="-1.5" fill="#fff" /></g>
    <g transform="translate(730, 330)" class="b3"><circle r="3.5" fill="#55ffff" opacity="0.75" /><circle r="1" cx="-1" cy="-1" fill="#fff" /></g>
    <g transform="translate(820, 345)" class="b4"><circle r="5.5" fill="#00d2ff" opacity="0.5" /><circle r="1.8" cx="-1.2" cy="-1.2" fill="#fff" /></g>
    <g transform="translate(865, 335)" class="b5"><circle r="3" fill="#ffffff" opacity="0.6" /></g>

    <!-- Right-Hand P3R HUD Section: Clean & Cinematic -->
    <g transform="translate(315, 115)">
      <!-- 1. System Status Tag -->
      <g>
        <polygon points="-8,-2 138,-2 126,24 -20,24" fill="#002255" stroke="#00d2ff" stroke-width="1.2" transform="skewX(-14)" />
        <polygon points="-8,-2 14,-2 2,24 -20,24" fill="#00d2ff" transform="skewX(-14)" />
        <text x="24" y="16" class="font-hud" font-size="11" font-weight="900" fill="#00ffff" letter-spacing="1.5">{esc(status_display)}</text>
        <text x="112" y="16" class="font-hud blink" font-size="11" font-weight="900" fill="#00ffff">█</text>
      </g>

      <!-- 2. Name Heading: CAMILO RODRÍGUEZ -->
      <g transform="translate(0, 68)">
        <!-- 3D Shadow for legibility over water -->
        <text x="3" y="3" class="font-p3r" font-size="37" fill="#001030" letter-spacing="1.2">{esc(name_display)}</text>
        <text x="0" y="0" class="font-p3r" font-size="37" fill="#ffffff" letter-spacing="1.2">{esc(name_display)}</text>
      </g>

      <!-- 3. Title Ribbon: SOFTWARE ENGINEER -->
      <g transform="translate(0, 92)">
        <polygon points="-6,-3 250,-3 238,27 -18,27" fill="url(#cyanRibbonGrad)" transform="skewX(-14)" />
        <text x="14" y="18" class="font-p3r" font-size="14.5" fill="#020814" letter-spacing="2">{esc(title_display)}</text>
      </g>

      <!-- 4. Arcana Tagline -->
      <g transform="translate(0, 150)">
        <text class="font-hud" font-size="12" font-weight="700" fill="#a5d8ff" letter-spacing="1.8">
          ARCANA: <tspan fill="#e6ff00" font-weight="800">{esc(arcana_display)}</tspan>
        </text>
      </g>
    </g>

    <!-- Sleek Tech Border Frame -->
    <rect width="{w-2}" height="{h-2}" x="1" y="1" rx="11" fill="none" stroke="#00d2ff" stroke-opacity="0.35" stroke-width="1.5" />
    <!-- Corner Accents -->
    <path d="M1,24 L1,1 L24,1" stroke="#00e5ff" stroke-width="3" fill="none" />
    <path d="M{w-1},24 L{w-1},1 L{w-24},1" stroke="#00e5ff" stroke-width="3" fill="none" />
    <path d="M1,{h-24} L1,{h-1} L24,{h-1}" stroke="#00e5ff" stroke-width="3" fill="none" />
    <path d="M{w-1},{h-24} L{w-1},{h-1} L{w-24},{h-1}" stroke="#00e5ff" stroke-width="3" fill="none" />
  </g>
</svg>
"""
    return svg

def gen_section_header_svg(idx, title, subtitle):
    """
    Generates an iconic, floating Persona 3 Reload section title.
    Zero background boxes or full-width lines: purely stylized slanted typography
    matching the in-game menu typography.
    """
    w, h = 900, 48
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(title)}">
  <defs>
    <style>
      {p3r_base_styles()}
      .title-glow {{
        filter: drop-shadow(0 0 6px rgba(0, 210, 255, 0.7));
      }}
    </style>
    <linearGradient id="titleLineGrad_{idx}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00d2ff" stop-opacity="0.9" />
      <stop offset="45%" stop-color="#0077cc" stop-opacity="0.5" />
      <stop offset="100%" stop-color="#00d2ff" stop-opacity="0" />
    </linearGradient>
  </defs>

  <g transform="translate(10, 0)">
    <!-- Slanted Neon Slash Accents -->
    <g transform="translate(16, 2) skewX(-16)">
      <polygon points="0,6 10,6 2,36 -8,36" fill="#00d2ff" />
      <polygon points="14,6 20,6 12,36 6,36" fill="#00ffff" />
    </g>

    <!-- Floating Slanted Title (Matching P3R Menu Screen) -->
    <g transform="translate(48, 2) skewX(-16)">
      <!-- 3D Shadow for legibility on dark & light backgrounds -->
      <text x="3" y="31" class="font-p3r" font-size="28" fill="#001433" letter-spacing="2.5">{esc(title)}</text>
      <!-- Main Electric Cyan Text with Glow -->
      <text x="0" y="28" class="font-p3r title-glow" font-size="28" fill="#00d2ff" letter-spacing="2.5">{esc(title)}</text>
      <!-- Pure White Highlight Overlay -->
      <text x="0" y="28" class="font-p3r" font-size="28" fill="#ffffff" opacity="0.35" letter-spacing="2.5">{esc(title)}</text>
    </g>

    <!-- Subtle Tapered Glow Line underneath that fades out to the right -->
    <line x1="20" y1="42" x2="440" y2="42" stroke="url(#titleLineGrad_{idx})" stroke-width="2" />
  </g>
</svg>
"""
    return svg

def gen_project_card_svg(p):
    """Generates an individual slanted P3R battle/mission tactical card."""
    w, h = 900, 136
    p_id = p["id"]
    name = p["name"]
    tag = p["tag"]
    role = p["role"]
    tech_list = p.get("tech", [])
    desc = p["description"]
    
    # Format tech pills
    tech_chips = "  ·  ".join(tech_list[:5])

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(name)}">
  <defs>
    <style>
      {p3r_base_styles()}
      .card-glow:hover {{ filter: drop-shadow(0 0 10px #00d2ff); }}
    </style>
    <linearGradient id="cardGrad_{p_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#05152d" />
      <stop offset="60%" stop-color="#081e3d" />
      <stop offset="100%" stop-color="#0a264e" />
    </linearGradient>
    <clipPath id="cardClip_{p_id}">
      <rect width="{w}" height="{h}" rx="10" />
    </clipPath>
  </defs>

  <g clip-path="url(#cardClip_{p_id})">
    <!-- Card Canvas -->
    <rect width="{w}" height="{h}" fill="url(#cardGrad_{p_id})" />
    
    <!-- Left Tactical Slanted Identifier Box -->
    <polygon points="-20,0 120,0 95,{h} -20,{h}" fill="#002d62" transform="skewX(-14)" />
    <polygon points="116,0 122,0 97,{h} 91,{h}" fill="#00d2ff" transform="skewX(-14)" opacity="0.9" />

    <!-- Mission Number Display -->
    <g transform="translate(24, 52)">
      <text class="font-hud" font-size="10" font-weight="700" fill="#00d2ff" letter-spacing="1">TACTIC</text>
      <text class="font-p3r" font-size="34" font-weight="900" fill="#ffffff" y="34">{esc(p_id)}</text>
    </g>

    <!-- Main Mission Details -->
    <g transform="translate(150, 32)">
      <!-- Project Title & Category Tag -->
      <g>
        <text class="font-p3r" font-size="18.5" font-weight="900" fill="#ffffff" letter-spacing="1">{esc(name)}</text>
        <rect x="520" y="-16" width="160" height="22" fill="#052952" stroke="#00d2ff" stroke-width="1" transform="skewX(-12)" rx="2" />
        <text x="600" y="0" text-anchor="middle" class="font-hud" font-size="10" font-weight="800" fill="#00ffff" letter-spacing="1">{esc(tag)}</text>
      </g>

      <!-- Role & Tech Stack Line -->
      <g transform="translate(0, 24)">
        <text class="font-hud" font-size="11.5" font-weight="700" fill="#e6ff00">ROLE: <tspan fill="#ffffff">{esc(role)}</tspan></text>
        <text x="320" y="0" class="font-hud" font-size="11" font-weight="600" fill="#55d4ff">STACK: <tspan fill="#b8dcfe">{esc(tech_chips)}</tspan></text>
      </g>

      <!-- Description Line (Clean wrap) -->
      <g transform="translate(0, 48)">
        <text class="font-body" font-size="12.5" fill="#cadfed">
          {esc(desc[:115])}{"..." if len(desc) > 115 else ""}
        </text>
      </g>
    </g>

    <!-- Right Interaction Button 'ENGAGE' -->
    <g transform="translate(805, 50)">
      <polygon points="0,0 72,0 60,38 -12,38" fill="#0052a3" stroke="#00d2ff" stroke-width="1.2" transform="skewX(-14)" />
      <text x="30" y="24" text-anchor="middle" class="font-hud" font-size="12" font-weight="900" fill="#ffffff" letter-spacing="1.5">OPEN ❯</text>
    </g>

    <!-- Surrounding Frame -->
    <rect width="{w}" height="{h}" fill="none" stroke="#00d2ff" stroke-opacity="0.25" stroke-width="1.2" rx="10" />
    <line x1="0" y1="0" x2="6" y2="0" stroke="#00e5ff" stroke-width="4" />
    <line x1="0" y1="{h}" x2="6" y2="{h}" stroke="#00e5ff" stroke-width="4" />
  </g>
</svg>
"""
    return svg

def gen_about_panel_svg(cfg):
    """Generates the Persona 3 Reload Character Status & Attributes sheet."""
    user = cfg["user"]
    about = cfg["about"]
    w, h = 900, 260

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="About Camilo - P3R Status">
  <defs>
    <style>
      {p3r_base_styles()}
    </style>
    <linearGradient id="aboutGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#040f22" />
      <stop offset="100%" stop-color="#081e3e" />
    </linearGradient>
    <clipPath id="aboutClip">
      <rect width="{w}" height="{h}" rx="10" />
    </clipPath>
  </defs>

  <g clip-path="url(#aboutClip)">
    <rect width="{w}" height="{h}" fill="url(#aboutGrad)" />

    <!-- Subtle Background Tech Hex Grid Lines -->
    <line x1="450" y1="0" x2="450" y2="{h}" stroke="#00d2ff" stroke-opacity="0.1" stroke-dasharray="6 4" />

    <!-- Left Column: Biography Summary -->
    <g transform="translate(36, 34)">
      <rect x="0" y="0" width="150" height="20" fill="#003b7a" transform="skewX(-14)" />
      <text x="14" y="14" class="font-hud" font-size="10.5" font-weight="900" fill="#00ffff" letter-spacing="1">SYSTEM://IDENTITY</text>

      <text x="0" y="44" class="font-p3r" font-size="20" font-weight="900" fill="#ffffff">SYSTEMS &amp; INFORMATICS ENGINEER</text>
      <text x="0" y="66" class="font-hud" font-size="12" font-weight="700" fill="#00d2ff">{esc(user['university'])}</text>

      <g transform="translate(0, 95)">
        <text class="font-body" font-size="12.5" fill="#d2e4f5">
          <tspan x="0" dy="0">Final-year Systems &amp; Informatics Engineering scholar at UPB.</tspan>
          <tspan x="0" dy="20">Combines high-level algorithmic rigor (2x ICPC Finalist) with</tspan>
          <tspan x="0" dy="20">production industry engineering across enterprise distributed systems,</tspan>
          <tspan x="0" dy="20">cloud platforms (AWS/GCP), and full-stack mobile applications.</tspan>
        </text>
      </g>

      <g transform="translate(0, 195)">
        <rect x="0" y="0" width="370" height="26" fill="#061c38" stroke="#00d2ff" stroke-width="0.8" rx="4" />
        <text x="12" y="17" class="font-hud" font-size="11" font-weight="700" fill="#e6ff00">
          MOTTO: <tspan fill="#ffffff">{esc(user['motto'])}</tspan>
        </text>
      </g>
    </g>

    <!-- Right Column: 4 Strategic Highlight Cards -->
    <g transform="translate(476, 26)">
      <!-- Highlight 1: Academic -->
      <g transform="translate(0, 0)">
        <polygon points="0,0 380,0 370,48 -10,48" fill="#062247" stroke="#00d2ff" stroke-width="0.8" transform="skewX(-10)" />
        <text x="18" y="20" class="font-hud" font-size="11" font-weight="800" fill="#e6ff00">🥇 ACADEMIC EXCELLENCE (GPA 4.93)</text>
        <text x="18" y="38" class="font-body" font-size="11" fill="#cde2f5">Top UPB Honor Scholarship recipient (GPAs 4.86 &amp; 4.93 / 5.0).</text>
      </g>

      <!-- Highlight 2: ICPC -->
      <g transform="translate(0, 56)">
        <polygon points="0,0 380,0 370,48 -10,48" fill="#062247" stroke="#00d2ff" stroke-width="0.8" transform="skewX(-10)" />
        <text x="18" y="20" class="font-hud" font-size="11" font-weight="800" fill="#00e5ff">🏆 2x ICPC REGIONAL FINALIST</text>
        <text x="18" y="38" class="font-body" font-size="11" fill="#cde2f5">South America–North Finals (2024 &amp; 2026) in C++ / Java.</text>
      </g>

      <!-- Highlight 3: AI Research -->
      <g transform="translate(0, 112)">
        <polygon points="0,0 380,0 370,48 -10,48" fill="#062247" stroke="#00d2ff" stroke-width="0.8" transform="skewX(-10)" />
        <text x="18" y="20" class="font-hud" font-size="11" font-weight="800" fill="#00e5ff">🔬 REDCOLSI 2026 NATIONAL FINALIST</text>
        <text x="18" y="38" class="font-body" font-size="11" fill="#cde2f5">Lead researcher on SEMPIA: AI &amp; Gamified Virtual Judge.</text>
      </g>

      <!-- Highlight 4: Cloud & Industry -->
      <g transform="translate(0, 168)">
        <polygon points="0,0 380,0 370,48 -10,48" fill="#062247" stroke="#00d2ff" stroke-width="0.8" transform="skewX(-10)" />
        <text x="18" y="20" class="font-hud" font-size="11" font-weight="800" fill="#00e5ff">☁️ ENTERPRISE CLOUD &amp; MOBILE</text>
        <text x="18" y="38" class="font-body" font-size="11" fill="#cde2f5">AWS &amp; GCP Certified · Kafka · Spring Boot · React Native.</text>
      </g>
    </g>

    <rect width="{w}" height="{h}" fill="none" stroke="#00d2ff" stroke-opacity="0.3" stroke-width="1.2" rx="10" />
  </g>
</svg>
"""
    return svg

def gen_skills_svg(cfg):
    """Generates the Persona Skill Tree / Arcana Affinities display."""
    skills = cfg["skills"]
    w, h = 900, 310

    cols = len(skills)
    col_w = (w - 60) / cols

    col_elements = []
    for i, s in enumerate(skills):
        cx = 30 + i * col_w
        cat = s["category"]
        icon = s.get("icon", "⚔️")
        items = s["items"]

        item_tags = []
        for j, itm in enumerate(items[:7]):
            iy = 72 + j * 31
            item_tags.append(f"""
          <g transform="translate(6, {iy})">
            <polygon points="0,0 {col_w-22},0 {col_w-30},24 -8,24" fill="#072042" stroke="#00d2ff" stroke-opacity="0.4" stroke-width="0.7" transform="skewX(-10)" />
            <circle cx="6" cy="12" r="2.5" fill="#00ffff" />
            <text x="15" y="16" class="font-hud" font-size="11" font-weight="600" fill="#e8f3ff">{esc(itm)}</text>
          </g>
            """)

        col_svg = f"""
      <!-- Column {i}: {esc(cat)} -->
      <g transform="translate({cx}, 24)">
        <polygon points="-5,-4 {col_w-15},-4 {col_w-25},32 -15,32" fill="#00356b" stroke="#00d2ff" stroke-width="1.2" transform="skewX(-12)" />
        <text x="6" y="20" class="font-hud" font-size="10.5" font-weight="900" fill="#ffffff" letter-spacing="1">
          {icon} {esc(cat.split("&")[0].strip())}
        </text>
        {''.join(item_tags)}
      </g>
        """
        col_elements.append(col_svg)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Technical Skills Arsenal - P3R Affinities">
  <defs>
    <style>
      {p3r_base_styles()}
    </style>
    <linearGradient id="skillsGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#040f24" />
      <stop offset="100%" stop-color="#081e3a" />
    </linearGradient>
    <clipPath id="skillsClip">
      <rect width="{w}" height="{h}" rx="10" />
    </clipPath>
  </defs>

  <g clip-path="url(#skillsClip)">
    <rect width="{w}" height="{h}" fill="url(#skillsGrad)" />
    
    <!-- Dividing Grid Accents -->
    {''.join(col_elements)}

    <rect width="{w}" height="{h}" fill="none" stroke="#00d2ff" stroke-opacity="0.25" stroke-width="1.2" rx="10" />
  </g>
</svg>
"""
    return svg

def gen_trophies_svg(cfg):
    """Generates the Hall of Fame & Honors display."""
    trophies = cfg["trophies"]
    w, h = 900, 260
    
    cards = []
    card_h = 42
    for i, t in enumerate(trophies[:5]):
        y = 20 + i * 46
        title = t["title"]
        year = t["year"]
        org = t["org"]
        highlight = t["highlight"]
        
        cards.append(f"""
      <g transform="translate(30, {y})">
        <polygon points="-8,0 840,0 828,{card_h} -20,{card_h}" fill="#051c3c" stroke="#00d2ff" stroke-opacity="0.5" stroke-width="1" transform="skewX(-14)" />
        <rect x="0" y="8" width="6" height="26" fill="#00d2ff" />
        <text x="18" y="26" class="font-p3r" font-size="14.5" fill="#ffffff" letter-spacing="0.5">{esc(title)}</text>
        <text x="360" y="26" class="font-hud" font-size="11.5" font-weight="700" fill="#e6ff00">[{esc(year)}]</text>
        <text x="490" y="26" class="font-hud" font-size="11.5" fill="#75c2ff">{esc(org)}</text>
      </g>
        """)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Honors &amp; Trophies Hall of Fame">
  <defs>
    <style>
      {p3r_base_styles()}
    </style>
    <linearGradient id="trophyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#030c1d" />
      <stop offset="100%" stop-color="#081a38" />
    </linearGradient>
    <clipPath id="trophyClip">
      <rect width="{w}" height="{h}" rx="10" />
    </clipPath>
  </defs>

  <g clip-path="url(#trophyClip)">
    <rect width="{w}" height="{h}" fill="url(#trophyGrad)" />
    {''.join(cards)}
    <rect width="{w}" height="{h}" fill="none" stroke="#00d2ff" stroke-opacity="0.3" stroke-width="1.2" rx="10" />
  </g>
</svg>
"""
    return svg

def gen_contact_button_svg(c):
    """Generates an individual slanted P3R Social Link button."""
    w, h = 160, 50
    lbl = c["label"]
    val = c.get("value", "")
    
    color_map = {
        "LINKEDIN": "#0077b5",
        "CREDLY": "#ff6b00",
        "EMAIL": "#d14836",
        "WHATSAPP": "#25d366",
        "GITHUB": "#00d2ff"
    }
    accent = color_map.get(lbl, "#00d2ff")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(lbl)}">
  <defs>
    <style>
      {p3r_base_styles()}
      .btn-hover:hover {{ filter: drop-shadow(0 0 6px {accent}); }}
    </style>
  </defs>
  <g class="btn-hover">
    <!-- Slanted Button Shape -->
    <polygon points="-8,2 {w-10},2 {w-22},{h-2} -20,{h-2}" fill="#051936" stroke="{accent}" stroke-width="1.5" transform="skewX(-14)" />
    <polygon points="-8,2 14,2 2,{h-2} -20,{h-2}" fill="{accent}" transform="skewX(-14)" />
    <text x="{w/2 + 2}" y="{h/2 + 5}" text-anchor="middle" class="font-p3r" font-size="13" font-weight="900" fill="#ffffff" letter-spacing="1.5">
      {esc(lbl)}
    </text>
  </g>
</svg>
"""
    return svg

def gen_footer_svg(cfg):
    """Generates the P3R deep water splash footer wave with Latin motto."""
    w, h = 900, 120
    user = cfg["user"]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Persona 3 Reload Footer">
  <defs>
    <style>
      {p3r_base_styles()}
      .wave-f1 {{ animation: waveDrift 8s ease-in-out infinite alternate; }}
      .wave-f2 {{ animation: waveSlow 10s ease-in-out infinite alternate; }}
      .b-f1 {{ animation: bubbleRise1 4s ease-in infinite; }}
      .b-f2 {{ animation: bubbleRise2 5s ease-in infinite 1.5s; }}
      .b-f3 {{ animation: bubbleRise1 4.5s ease-in infinite 2.8s; }}
    </style>
    <linearGradient id="footerAbyss" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#020815" />
      <stop offset="100%" stop-color="#00142b" />
    </linearGradient>
    <clipPath id="footerClip">
      <rect width="{w}" height="{h}" rx="10" />
    </clipPath>
  </defs>

  <g clip-path="url(#footerClip)">
    <rect width="{w}" height="{h}" fill="url(#footerAbyss)" />

    <!-- Wave 1 -->
    <g class="wave-f1" opacity="0.3">
      <path d="M-40,40 C140,80 320,10 520,50 C710,90 850,20 960,60 L960,120 L-40,120 Z" fill="#0088ff" />
    </g>
    <!-- Wave 2 -->
    <g class="wave-f2" opacity="0.45">
      <path d="M-20,60 C180,20 340,90 560,40 C740,10 880,80 980,50 L980,120 L-20,120 Z" fill="#003d80" />
    </g>

    <!-- Bubbles -->
    <g transform="translate(180, 110)" class="b-f1"><circle r="4" fill="#00ffff" opacity="0.6" /></g>
    <g transform="translate(480, 115)" class="b-f2"><circle r="5" fill="#00d2ff" opacity="0.5" /></g>
    <g transform="translate(740, 110)" class="b-f3"><circle r="3.5" fill="#55ffff" opacity="0.7" /></g>

    <!-- Center Latin Motto & Credit -->
    <g transform="translate({w/2}, 62)">
      <polygon points="-240,-16 240,-16 220,18 -260,18" fill="#031630" stroke="#00d2ff" stroke-width="1" transform="skewX(-14)" />
      <text text-anchor="middle" class="font-p3r" font-size="13" font-weight="900" fill="#ffffff" letter-spacing="3" y="3">
        MEMENTO MORI // CARPE DIEM
      </text>
      <text text-anchor="middle" class="font-hud" font-size="10" fill="#699cc8" letter-spacing="1.5" y="36">
        PERSONA 3 RELOAD THEME · CAMILO ANDRÉS RODRÍGUEZ · 2026
      </text>
    </g>

    <rect width="{w}" height="{h}" fill="none" stroke="#00d2ff" stroke-opacity="0.25" stroke-width="1" rx="10" />
  </g>
</svg>
"""
    return svg

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cfg = load_config()

    print("[P3R] Generating Persona 3 Reload SVG Suite...")

    # 1. Hero Banner
    hero_svg = gen_hero_svg(cfg)
    with open(os.path.join(OUTPUT_DIR, "hero.svg"), "w", encoding="utf-8") as f:
        f.write(hero_svg)
    print("  ✓ Created hero.svg")

    # 2. Section Headers
    headers = [
        ("01", "STATUS // IDENTITY", "SYSTEM PROFILE & ACADEMIC ATTRIBUTES", "h-about.svg"),
        ("02", "TACTICS // MISSIONS", "FEATURED PRODUCTION PLATFORMS & RESEARCH", "h-tactics.svg"),
        ("03", "SKILLS // ARSENAL", "AFFINITIES & TECHNICAL PROFICIENCIES", "h-skills.svg"),
        ("04", "TROPHIES // HONORS", "AWARDS & COMPETITIVE RECOGNITIONS", "h-trophies.svg"),
        ("05", "S-LINK // NETWORK", "DIRECT COMMS & SOCIAL CHANNELS", "h-contact.svg")
    ]
    for idx, title, subtitle, filename in headers:
        sec_svg = gen_section_header_svg(idx, title, subtitle)
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(sec_svg)
        print(f"  ✓ Created {filename}")

    # 3. Project Cards
    for i, project in enumerate(cfg.get("projects", [])):
        card_svg = gen_project_card_svg(project)
        card_name = f"target-{i}.svg"
        with open(os.path.join(OUTPUT_DIR, card_name), "w", encoding="utf-8") as f:
            f.write(card_svg)
        print(f"  ✓ Created {card_name} ({project['name']})")

    # 4. About Panel
    about_svg = gen_about_panel_svg(cfg)
    with open(os.path.join(OUTPUT_DIR, "about.svg"), "w", encoding="utf-8") as f:
        f.write(about_svg)
    print("  ✓ Created about.svg")

    # 5. Skills Sheet
    skills_svg = gen_skills_svg(cfg)
    with open(os.path.join(OUTPUT_DIR, "skills.svg"), "w", encoding="utf-8") as f:
        f.write(skills_svg)
    print("  ✓ Created skills.svg")

    # 6. Trophies Sheet
    trophies_svg = gen_trophies_svg(cfg)
    with open(os.path.join(OUTPUT_DIR, "trophies.svg"), "w", encoding="utf-8") as f:
        f.write(trophies_svg)
    print("  ✓ Created trophies.svg")

    # 7. Contact Buttons
    for i, contact in enumerate(cfg.get("contacts", [])):
        btn_svg = gen_contact_button_svg(contact)
        lbl_slug = re.sub(r'[^a-z0-9]+', '-', contact["label"].lower()).strip('-')
        btn_name = f"contact-{lbl_slug}.svg"
        with open(os.path.join(OUTPUT_DIR, btn_name), "w", encoding="utf-8") as f:
            f.write(btn_svg)
        print(f"  ✓ Created {btn_name}")

    # 8. Footer Banner
    footer_svg = gen_footer_svg(cfg)
    with open(os.path.join(OUTPUT_DIR, "footer.svg"), "w", encoding="utf-8") as f:
        f.write(footer_svg)
    print("  ✓ Created footer.svg")

    print("[P3R] All Persona 3 Reload SVG assets generated successfully!")

if __name__ == "__main__":
    main()
