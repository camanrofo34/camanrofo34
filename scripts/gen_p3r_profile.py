#!/usr/bin/env python3
"""
Persona 3 Reload (P3R) SVG Profile Asset Generator - Final Master Version
Generates responsive, animated SVGs styled after Persona 3 Reload:
- Clean floating slanted geometry (zero left-edge clipping, strictly positive coordinates)
- High-contrast electric cyan, phosphor yellow, and pure white P3R theme colors
- Pure vector iconography (zero emojis)
- Fully decoupled data driven by p3r.config.json
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
    @keyframes cyanGlow {
      0%, 100% { filter: drop-shadow(0 0 4px #00d2ff); opacity: 0.9; }
      50% { filter: drop-shadow(0 0 12px #00ffff); opacity: 1; }
    }
    @keyframes blinkCursor {
      0%, 49% { opacity: 1; }
      50%, 100% { opacity: 0; }
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
      *, .wave-anim, .bubble-anim {
        animation: none !important;
      }
    }
    """

def p3r_icon(icon_type, x=0, y=0, size=18):
    """Generates pure vector SVG icons in P3R theme colors (Zero emojis)."""
    if icon_type == "trophy":
        return f"""<g transform="translate({x}, {y}) scale({size/20})">
          <path d="M4,3 H16 V8 C16,11.3 13.3,14 10,14 C6.7,14 4,11.3 4,8 Z" fill="none" stroke="#e6ff00" stroke-width="2" />
          <path d="M4,5 H1 C1,7.2 2,9 4,9 M16,5 H19 C19,7.2 18,9 16,9" fill="none" stroke="#00d2ff" stroke-width="1.8" />
          <line x1="10" y1="14" x2="10" y2="18" stroke="#e6ff00" stroke-width="2" />
          <line x1="6" y1="18" x2="14" y2="18" stroke="#e6ff00" stroke-width="2" />
        </g>"""
    elif icon_type == "medal":
        return f"""<g transform="translate({x}, {y}) scale({size/20})">
          <polygon points="10,1 12.5,7 19,7.5 14,12 15.5,18.5 10,15 4.5,18.5 6,12 1,7.5 7.5,7" fill="#e6ff00" stroke="#00ffff" stroke-width="1" />
        </g>"""
    elif icon_type == "atom":
        return f"""<g transform="translate({x}, {y}) scale({size/20})">
          <ellipse cx="10" cy="10" rx="8" ry="3" fill="none" stroke="#00d2ff" stroke-width="1.5" transform="rotate(30 10 10)" />
          <ellipse cx="10" cy="10" rx="8" ry="3" fill="none" stroke="#00d2ff" stroke-width="1.5" transform="rotate(-30 10 10)" />
          <circle cx="10" cy="10" r="2.2" fill="#00ffff" />
        </g>"""
    elif icon_type == "backend":
        return f"""<g transform="translate({x}, {y}) scale({size/20})">
          <polyline points="6,4 2,10 6,16" fill="none" stroke="#00d2ff" stroke-width="2" stroke-linecap="round" />
          <polyline points="14,4 18,10 14,16" fill="none" stroke="#00d2ff" stroke-width="2" stroke-linecap="round" />
          <line x1="11" y1="4" x2="9" y2="16" stroke="#e6ff00" stroke-width="1.8" stroke-linecap="round" />
        </g>"""
    elif icon_type == "mobile":
        return f"""<g transform="translate({x}, {y}) scale({size/20})">
          <rect x="5" y="1" width="10" height="18" rx="2" fill="none" stroke="#00d2ff" stroke-width="1.8" />
          <line x1="9" y1="15" x2="11" y2="15" stroke="#00ffff" stroke-width="2" stroke-linecap="round" />
        </g>"""
    elif icon_type == "algo":
        return f"""<g transform="translate({x}, {y}) scale({size/20})">
          <polygon points="10,2 18,10 10,18 2,10" fill="none" stroke="#e6ff00" stroke-width="1.8" />
          <circle cx="10" cy="10" r="2.5" fill="#00d2ff" />
        </g>"""
    elif icon_type == "cloud":
        return f"""<g transform="translate({x}, {y}) scale({size/20})">
          <path d="M5,14 A4,4 0 0,1 5,8 A5,5 0 0,1 14,6 A4,4 0 0,1 17,14 Z" fill="none" stroke="#00d2ff" stroke-width="1.8" />
        </g>"""
    return ""

def gen_hero_svg(cfg):
    user = cfg["user"]
    w, h = 900, 360

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

    <linearGradient id="oceanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#00efff" />
      <stop offset="8%" stop-color="#0077ff" />
      <stop offset="30%" stop-color="#003cdb" />
      <stop offset="70%" stop-color="#001882" />
      <stop offset="100%" stop-color="#000b40" />
    </linearGradient>

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
    <rect width="{w}" height="{h}" fill="url(#oceanGrad)" />

    <g mask="url(#artMask)">
      <g class="ocean-motion">
        <image href="data:image/jpeg;base64,{b64_img}" xlink:href="data:image/jpeg;base64,{b64_img}" x="-15" y="-15" width="672" height="{h+30}" preserveAspectRatio="xMinYMid slice" />
      </g>
    </g>

    <g class="caustic" opacity="0.65">
      <path d="M420,18 C470,8 520,24 580,14 C640,6 700,22 760,12 C820,4 860,20 910,12" fill="none" stroke="#00ffff" stroke-width="2.5" />
      <path d="M460,32 C510,22 560,38 620,28 C680,18 740,34 800,24 C850,16 880,30 920,22" fill="none" stroke="#ffffff" stroke-width="1.2" opacity="0.7" />
    </g>

    <g transform="translate(520, 340)" class="b1"><circle r="4.5" fill="#00ffff" opacity="0.65" /><circle r="1.5" cx="-1" cy="-1" fill="#fff" /></g>
    <g transform="translate(610, 350)" class="b2"><circle r="6.5" fill="#00d2ff" opacity="0.55" /><circle r="2" cx="-1.5" cy="-1.5" fill="#fff" /></g>
    <g transform="translate(730, 330)" class="b3"><circle r="3.5" fill="#55ffff" opacity="0.75" /><circle r="1" cx="-1" cy="-1" fill="#fff" /></g>
    <g transform="translate(820, 345)" class="b4"><circle r="5.5" fill="#00d2ff" opacity="0.5" /><circle r="1.8" cx="-1.2" cy="-1.2" fill="#fff" /></g>
    <g transform="translate(865, 335)" class="b5"><circle r="3" fill="#ffffff" opacity="0.6" /></g>

    <g transform="translate(315, 115)">
      <g>
        <polygon points="-8,-2 138,-2 126,24 -20,24" fill="#002255" stroke="#00d2ff" stroke-width="1.2" transform="skewX(-14)" />
        <polygon points="-8,-2 14,-2 2,24 -20,24" fill="#00d2ff" transform="skewX(-14)" />
        <text x="24" y="16" class="font-hud" font-size="11" font-weight="900" fill="#00ffff" letter-spacing="1.5">{esc(status_display)}</text>
        <text x="112" y="16" class="font-hud blink" font-size="11" font-weight="900" fill="#00ffff">█</text>
      </g>

      <g transform="translate(0, 68)">
        <text x="3" y="3" class="font-p3r" font-size="37" fill="#001030" letter-spacing="1.2">{esc(name_display)}</text>
        <text x="0" y="0" class="font-p3r" font-size="37" fill="#ffffff" letter-spacing="1.2">{esc(name_display)}</text>
      </g>

      <g transform="translate(0, 92)">
        <polygon points="-6,-3 250,-3 238,27 -18,27" fill="url(#cyanRibbonGrad)" transform="skewX(-14)" />
        <text x="14" y="18" class="font-p3r" font-size="14.5" fill="#020814" letter-spacing="2">{esc(title_display)}</text>
      </g>

      <g transform="translate(0, 150)">
        <text class="font-hud" font-size="12" font-weight="700" fill="#a5d8ff" letter-spacing="1.8">
          ARCANA: <tspan fill="#e6ff00" font-weight="800">{esc(arcana_display)}</tspan>
        </text>
      </g>
    </g>

    <rect width="{w-2}" height="{h-2}" x="1" y="1" rx="11" fill="none" stroke="#00d2ff" stroke-opacity="0.35" stroke-width="1.5" />
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
    Floating, minimalist Persona 3 Reload section title.
    Zero background boxes: purely stylized slanted typography matching P3R menu.
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
    <g transform="translate(16, 2) skewX(-16)">
      <polygon points="0,6 10,6 2,36 -8,36" fill="#00d2ff" />
      <polygon points="14,6 20,6 12,36 6,36" fill="#00ffff" />
    </g>

    <g transform="translate(48, 2) skewX(-16)">
      <text x="3" y="31" class="font-p3r" font-size="28" fill="#001433" letter-spacing="2.5">{esc(title)}</text>
      <text x="0" y="28" class="font-p3r title-glow" font-size="28" fill="#00d2ff" letter-spacing="2.5">{esc(title)}</text>
      <text x="0" y="28" class="font-p3r" font-size="28" fill="#ffffff" opacity="0.35" letter-spacing="2.5">{esc(title)}</text>
    </g>

    <line x1="20" y1="42" x2="440" y2="42" stroke="url(#titleLineGrad_{idx})" stroke-width="2" />
  </g>
</svg>
"""
    return svg

def gen_about_panel_svg(cfg):
    """
    Persona 3 Reload Status & Identity sheet.
    Separated panels with zero overlapping, ample vertical spacing, and safe margins.
    """
    user = cfg["user"]
    about = cfg["about"]
    w, h = 900, 220

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Status Identity - Camilo Rodríguez">
  <defs>
    <style>
      {p3r_base_styles()}
    </style>
  </defs>

  <g>
    <!-- Left Column: Software Engineer Identity -->
    <g transform="translate(24, 12)">
      <polygon points="12,0 216,0 204,24 0,24" fill="#00356b" stroke="#00d2ff" stroke-width="1" />
      <text x="24" y="16" class="font-hud" font-size="11" font-weight="900" fill="#00ffff" letter-spacing="1.5">SOFTWARE ENGINEER</text>

      <text x="4" y="52" class="font-p3r" font-size="21" font-weight="900" fill="#ffffff" letter-spacing="1">IN SEARCH OF NEW CHALLENGES</text>
      <text x="4" y="74" class="font-hud" font-size="11.5" font-weight="700" fill="#00d2ff">{esc(user['university'])}</text>

      <g transform="translate(4, 96)">
        <text class="font-body" font-size="12" fill="#cbe3f7">
          <tspan x="0" dy="0">Specialized in Java &amp; Spring Boot microservices, distributed architectures,</tspan>
          <tspan x="0" dy="19">Node.js, and high-performance mobile applications with React Native.</tspan>
        </text>
      </g>

      <!-- Motto Panel (Safely separated with its own dedicated box and clear padding) -->
      <g transform="translate(4, 150)">
        <polygon points="12,0 435,0 423,32 0,32" fill="#04162e" fill-opacity="0.9" stroke="#00d2ff" stroke-width="1" />
        <text x="18" y="14" class="font-hud" font-size="9.5" font-weight="800" fill="#00ffff" letter-spacing="1">MOTTO</text>
        <text x="18" y="26" class="font-hud" font-size="10" font-weight="700" fill="#e6ff00">
          {esc(user['motto'])}
        </text>
      </g>
    </g>

    <!-- Right Column: 3 Distinct Highlight Cards with P3R Vector Icons -->
    <g transform="translate(480, 10)">
      <!-- Highlight 1: Academic -->
      <g transform="translate(0, 0)">
        <polygon points="14,0 395,0 383,48 2,48" fill="#052144" fill-opacity="0.85" stroke="#00d2ff" stroke-width="1" />
        {p3r_icon("medal", x=16, y=14, size=18)}
        <text x="42" y="20" class="font-hud" font-size="11" font-weight="800" fill="#e6ff00">ACADEMIC EXCELLENCE (GPA 4.93 / 5.0)</text>
        <text x="42" y="38" class="font-body" font-size="11" fill="#cde2f5">Top UPB Honor Scholarship recipient (GPAs 4.86 &amp; 4.93 / 5.0).</text>
      </g>

      <!-- Highlight 2: ICPC -->
      <g transform="translate(0, 58)">
        <polygon points="14,0 395,0 383,48 2,48" fill="#052144" fill-opacity="0.85" stroke="#00d2ff" stroke-width="1" />
        {p3r_icon("trophy", x=16, y=14, size=18)}
        <text x="42" y="20" class="font-hud" font-size="11" font-weight="800" fill="#00e5ff">2x ICPC REGIONAL FINALIST</text>
        <text x="42" y="38" class="font-body" font-size="11" fill="#cde2f5">South America–North Finals (2024 &amp; 2026) in C++ &amp; Java.</text>
      </g>

      <!-- Highlight 3: AI Research -->
      <g transform="translate(0, 116)">
        <polygon points="14,0 395,0 383,48 2,48" fill="#052144" fill-opacity="0.85" stroke="#00d2ff" stroke-width="1" />
        {p3r_icon("atom", x=16, y=14, size=18)}
        <text x="42" y="20" class="font-hud" font-size="11" font-weight="800" fill="#00e5ff">REDCOLSI NATIONAL FINALIST</text>
        <text x="42" y="38" class="font-body" font-size="11" fill="#cde2f5">Lead researcher on SEMPIA: AI &amp; Gamified Virtual Judge.</text>
      </g>
    </g>
  </g>
</svg>
"""
    return svg

def gen_project_card_svg(p):
    """
    Floating slanted P3R mission card.
    Safe margins: Button is completely enclosed inside the card boundary,
    zero text overlap, zero left-edge clipping.
    """
    w, h = 900, 118
    p_id = p["id"]
    name = p["name"]
    tag = p["tag"]
    role = p["role"]
    tech_list = p.get("tech", [])
    desc = p["description"]
    
    tech_chips = "  ·  ".join(tech_list[:5])

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(name)}">
  <defs>
    <style>
      {p3r_base_styles()}
      .card-hover:hover {{ filter: drop-shadow(0 0 8px #00d2ff); }}
    </style>
  </defs>

  <g class="card-hover">
    <!-- Main Card Body (Explicit slanted points: Left-most point is x=6 > 0, Right-most is x=885 <= 900) -->
    <polygon points="26,2 885,2 865,{h-2} 6,{h-2}" fill="#04152c" fill-opacity="0.85" stroke="#00d2ff" stroke-width="1.2" stroke-opacity="0.45" />
    
    <!-- Left Tactical Identifier Banner -->
    <polygon points="26,2 110,2 90,{h-2} 6,{h-2}" fill="#00356b" />
    <polygon points="106,2 112,2 92,{h-2} 86,{h-2}" fill="#00d2ff" opacity="0.9" />

    <!-- Mission Number Display -->
    <g transform="translate(24, 44)">
      <text class="font-hud" font-size="10" font-weight="700" fill="#00d2ff" letter-spacing="1">TACTIC</text>
      <text class="font-p3r" font-size="34" font-weight="900" fill="#ffffff" y="34">{esc(p_id)}</text>
    </g>

    <!-- Main Mission Details -->
    <g transform="translate(136, 26)">
      <!-- Row 1: Name and Tag -->
      <g>
        <text class="font-p3r" font-size="17" font-weight="900" fill="#ffffff" letter-spacing="1">{esc(name)}</text>
        <polygon points="460,-15 615,-15 605,7 450,7" fill="#002d5a" stroke="#00d2ff" stroke-width="0.8" />
        <text x="532" y="-1" text-anchor="middle" class="font-hud" font-size="9.5" font-weight="800" fill="#00ffff" letter-spacing="1">{esc(tag)}</text>
      </g>

      <!-- Row 2: Role & Stack -->
      <g transform="translate(0, 24)">
        <text class="font-hud" font-size="11" font-weight="700" fill="#e6ff00">ROLE: <tspan fill="#ffffff">{esc(role)}</tspan></text>
        <text x="270" y="0" class="font-hud" font-size="11" font-weight="600" fill="#55d4ff">STACK: <tspan fill="#b8dcfe">{esc(tech_chips)}</tspan></text>
      </g>

      <!-- Row 3: Description -->
      <g transform="translate(0, 48)">
        <text class="font-body" font-size="12" fill="#cadfed">
          {esc(desc[:115])}{"..." if len(desc) > 115 else ""}
        </text>
      </g>
    </g>

    <!-- Right Interaction Button 'OPEN ❯' (Comfortably inside the card boundary: 760 + 85 = 845 < 865) -->
    <g transform="translate(760, 40)">
      <polygon points="12,0 90,0 78,38 0,38" fill="#00488f" stroke="#00d2ff" stroke-width="1.2" />
      <text x="45" y="24" text-anchor="middle" class="font-hud" font-size="12" font-weight="900" fill="#ffffff" letter-spacing="1.5">OPEN ❯</text>
    </g>
  </g>
</svg>
"""
    return svg

def gen_skills_svg(cfg):
    """
    Focused, minimalist technical skills sheet.
    Pure vector iconography (no emojis), transparent floating canvas.
    """
    skills = cfg["skills"]
    w, h = 900, 240

    cols = len(skills)
    col_w = (w - 40) / cols

    col_elements = []
    for i, s in enumerate(skills):
        cx = 20 + i * col_w
        cat = s["category"]
        icon_type = s.get("icon_type", "backend")
        items = s["items"]

        item_tags = []
        for j, itm in enumerate(items[:6]):
            iy = 56 + j * 30
            item_tags.append(f"""
          <g transform="translate(6, {iy})">
            <polygon points="8,0 {col_w-16},0 {col_w-24},24 0,24" fill="#051c38" fill-opacity="0.8" stroke="#00d2ff" stroke-opacity="0.35" stroke-width="0.8" />
            <circle cx="10" cy="12" r="2.5" fill="#00ffff" />
            <text x="20" y="16" class="font-hud" font-size="11" font-weight="600" fill="#e8f3ff">{esc(itm)}</text>
          </g>
            """)

        col_svg = f"""
      <g transform="translate({cx}, 10)">
        <polygon points="8,-2 {col_w-10},-2 {col_w-20},30 -2,30" fill="#00356b" stroke="#00d2ff" stroke-width="1.2" />
        {p3r_icon(icon_type, x=8, y=5, size=18)}
        <text x="32" y="19" class="font-hud" font-size="10.5" font-weight="900" fill="#ffffff" letter-spacing="1">
          {esc(cat)}
        </text>
        {''.join(item_tags)}
      </g>
        """
        col_elements.append(col_svg)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Technical Skills Arsenal">
  <defs>
    <style>
      {p3r_base_styles()}
    </style>
  </defs>

  <g>
    {''.join(col_elements)}
  </g>
</svg>
"""
    return svg

def gen_trophies_svg(cfg):
    """
    Honors & Awards showcase.
    Pure vector iconography (no emojis), strictly positive coordinates (no left cut).
    """
    trophies = cfg["trophies"]
    w, h = 900, 160
    
    cards = []
    card_h = 42
    for i, t in enumerate(trophies[:3]):
        y = 10 + i * 48
        title = t["title"]
        year = t["year"]
        org = t["org"]
        icon_type = t.get("icon_type", "medal")
        
        cards.append(f"""
      <g transform="translate(16, {y})">
        <!-- Strictly positive coordinates: Left edge is x=8 > 0 -->
        <polygon points="18,0 864,0 854,{card_h} 8,{card_h}" fill="#041936" fill-opacity="0.85" stroke="#00d2ff" stroke-opacity="0.5" stroke-width="1" />
        <rect x="18" y="8" width="5" height="26" fill="#00d2ff" />
        {p3r_icon(icon_type, x=30, y=11, size=18)}
        <text x="56" y="26" class="font-p3r" font-size="14.5" fill="#ffffff" letter-spacing="0.5">{esc(title)}</text>
        <text x="380" y="26" class="font-hud" font-size="11.5" font-weight="700" fill="#e6ff00">[{esc(year)}]</text>
        <text x="510" y="26" class="font-hud" font-size="11.5" fill="#75c2ff">{esc(org)}</text>
      </g>
        """)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Honors &amp; Trophies Showcase">
  <defs>
    <style>
      {p3r_base_styles()}
    </style>
  </defs>

  <g>
    {''.join(cards)}
  </g>
</svg>
"""
    return svg

def gen_contact_button_svg(c):
    """
    Individual slanted P3R Social Link button with authentic vector logos.
    Strictly positive coordinates: zero left-edge clipping.
    """
    w, h = 210, 50
    lbl = c["label"]
    
    if lbl == "LINKEDIN":
        accent = "#0077b5"
        icon_path = """
        <g transform="translate(30, 16) scale(0.85)">
          <path d="M0,0 H4 V14 H0 Z M2, -3.5 C0.7,-3.5 0,-4.4 0,-5.4 C0,-6.5 0.7,-7.3 2,-7.3 C3.3,-7.3 4,-6.5 4,-5.4 C4,-4.4 3.3,-3.5 2,-3.5 Z" fill="#ffffff" />
          <path d="M7,0 H11 V2.2 C11.6,1.2 12.8,0 14.8,0 C18.2,0 19.5,2.2 19.5,6.5 V14 H15.5 V7.2 C15.5,5.2 14.8,4 13.2,4 C11.8,4 11,5.1 11,6.8 V14 H7 Z" fill="#ffffff" />
        </g>
        """
    elif lbl == "CREDLY":
        accent = "#ff6b00"
        icon_path = """
        <g transform="translate(34, 26) scale(0.9)">
          <polygon points="0,-10 6,-8 10,-3 9,4 5,9 0,11 -5,9 -9,4 -10,-3 -6,-8" fill="#ff6b00" />
          <polyline points="-3,0 -1,3 4,-3" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        """
    else: # EMAIL
        accent = "#00d2ff"
        icon_path = """
        <g transform="translate(28, 18) scale(0.9)">
          <rect x="0" y="0" width="18" height="13" rx="2" fill="none" stroke="#00ffff" stroke-width="1.8" />
          <polyline points="1,1 9,8 17,1" fill="none" stroke="#00ffff" stroke-width="1.8" />
        </g>
        """

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(lbl)}">
  <defs>
    <style>
      {p3r_base_styles()}
      .btn-hover:hover {{ filter: drop-shadow(0 0 8px {accent}); }}
    </style>
  </defs>
  <g class="btn-hover">
    <!-- Strictly positive coordinates: Left-most point is x=8 > 0 -->
    <polygon points="20,2 204,2 192,48 8,48" fill="#04162e" stroke="{accent}" stroke-width="1.5" />
    <polygon points="20,2 40,2 28,48 8,48" fill="{accent}" />
    {icon_path}
    <text x="122" y="30" text-anchor="middle" class="font-p3r" font-size="13.5" font-weight="900" fill="#ffffff" letter-spacing="1.5">
      {esc(lbl)}
    </text>
  </g>
</svg>
"""
    return svg

def gen_footer_svg(cfg):
    """
    Persona 3 Reload footer.
    Motto box is 740px wide so the Latin phrase never overflows,
    with strictly positive coordinates.
    """
    w, h = 900, 100
    user = cfg["user"]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Persona 3 Reload Footer">
  <defs>
    <style>
      {p3r_base_styles()}
      .b-f1 {{ animation: bubbleRise1 4s ease-in infinite; }}
      .b-f2 {{ animation: bubbleRise2 5s ease-in infinite 1.5s; }}
    </style>
    <linearGradient id="footerLineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00d2ff" stop-opacity="0" />
      <stop offset="25%" stop-color="#00d2ff" stop-opacity="0.8" />
      <stop offset="75%" stop-color="#00d2ff" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#00d2ff" stop-opacity="0" />
    </linearGradient>
  </defs>

  <g>
    <g transform="translate(180, 80)" class="b-f1"><circle r="3.5" fill="#00ffff" opacity="0.6" /></g>
    <g transform="translate(720, 80)" class="b-f2"><circle r="4" fill="#00d2ff" opacity="0.5" /></g>

    <!-- Motto Box: 740px wide, centered at x=450, completely enclosing the 540px phrase -->
    <g transform="translate({w/2}, 38)">
      <polygon points="-370,-16 370,-16 355,18 -385,18" fill="#041834" fill-opacity="0.9" stroke="#00d2ff" stroke-width="1" />
      <text text-anchor="middle" class="font-p3r" font-size="11" font-weight="900" fill="#ffffff" letter-spacing="1.5" y="2">
        {esc(user['motto'].upper())}
      </text>
      <text text-anchor="middle" class="font-hud" font-size="10" fill="#69a3d4" letter-spacing="1.5" y="32">
        PERSONA 3 RELOAD THEME · CAMILO RODRÍGUEZ · 2026
      </text>
    </g>

    <line x1="80" y1="88" x2="820" y2="88" stroke="url(#footerLineGrad)" stroke-width="1.5" />
  </g>
</svg>
"""
    return svg

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cfg = load_config()

    print("[P3R] Generating Master Persona 3 Reload SVG Suite...")

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

    # 3. Project Cards (4 Public Repos)
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

    # 7. Contact Buttons (LinkedIn, Credly, Email)
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

    print("[P3R] All Master Persona 3 Reload SVG assets generated successfully!")

if __name__ == "__main__":
    main()
