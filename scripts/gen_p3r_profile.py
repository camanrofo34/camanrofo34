#!/usr/bin/env python3
"""
Persona 3 Reload (P3R) SVG Profile Asset Generator
Generates responsive, animated SVGs and profile assets styled after
Persona 3 Reload's water splash, midnight blue palettes, and sleek angled HUD.
"""

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

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(user['name'])} - Persona 3 Reload Profile">
  <defs>
    <style>
      {p3r_base_styles()}
      .wave1 {{ animation: waveDrift 7s ease-in-out infinite; }}
      .wave2 {{ animation: waveSlow 9s ease-in-out infinite; }}
      .dial-cw {{ transform-origin: 755px 180px; animation: dialSpinCW 45s linear infinite; }}
      .dial-ccw {{ transform-origin: 755px 180px; animation: dialSpinCCW 60s linear infinite; }}
      .r1 {{ transform-origin: 755px 180px; animation: ripplePulse 3.5s ease-out infinite; }}
      .r2 {{ transform-origin: 755px 180px; animation: ripplePulse2 4.2s ease-out infinite 1.8s; }}
      .b1 {{ animation: bubbleRise1 5s ease-in infinite; }}
      .b2 {{ animation: bubbleRise2 6.5s ease-in infinite 1.2s; }}
      .b3 {{ animation: bubbleRise1 4.5s ease-in infinite 2.5s; }}
      .b4 {{ animation: bubbleRise2 5.8s ease-in infinite 3.5s; }}
      .blink {{ animation: blinkCursor 1s steps(1) infinite; }}
      .p3r-glow {{ animation: cyanGlow 3s ease-in-out infinite; }}
    </style>

    <!-- Deep Underwater Linear Gradients -->
    <linearGradient id="abyssGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020712" />
      <stop offset="45%" stop-color="#051428" />
      <stop offset="100%" stop-color="#082346" />
    </linearGradient>

    <linearGradient id="cyanRibbonGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#004488" stop-opacity="0.9" />
      <stop offset="50%" stop-color="#00a3e0" stop-opacity="0.95" />
      <stop offset="100%" stop-color="#00e5ff" stop-opacity="1" />
    </linearGradient>

    <linearGradient id="deepWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0099ff" stop-opacity="0.3" />
      <stop offset="100%" stop-color="#041a3a" stop-opacity="0.8" />
    </linearGradient>

    <linearGradient id="hpGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00d2ff" />
      <stop offset="100%" stop-color="#55ffff" />
    </linearGradient>

    <linearGradient id="spGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#e6ff00" />
      <stop offset="100%" stop-color="#fff066" />
    </linearGradient>

    <!-- Halftone / Dot Grid Pattern -->
    <pattern id="p3rGrid" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="12" cy="12" r="1.1" fill="#00d2ff" fill-opacity="0.18" />
      <line x1="0" y1="12" x2="24" y2="12" stroke="#00d2ff" stroke-opacity="0.04" stroke-width="0.5" />
      <line x1="12" y1="0" x2="12" y2="24" stroke="#00d2ff" stroke-opacity="0.04" stroke-width="0.5" />
    </pattern>

    <clipPath id="heroFrame">
      <rect width="{w}" height="{h}" rx="12" />
    </clipPath>
  </defs>

  <g clip-path="url(#heroFrame)">
    <!-- Base Abyssal Background -->
    <rect width="{w}" height="{h}" fill="url(#abyssGrad)" />
    <rect width="{w}" height="{h}" fill="url(#p3rGrid)" />

    <!-- Ambient Dark Hour Compass & Clock Ring Elements (Right Side HUD) -->
    <g opacity="0.6">
      <circle class="r1" cx="755" cy="180" r="10" fill="none" stroke="#00e5ff" />
      <circle class="r2" cx="755" cy="180" r="10" fill="none" stroke="#00a3e0" />

      <!-- Outer Clock Gear / Ring -->
      <g class="dial-cw">
        <circle cx="755" cy="180" r="130" fill="none" stroke="#00d2ff" stroke-opacity="0.25" stroke-width="1.5" stroke-dasharray="4 8" />
        <circle cx="755" cy="180" r="115" fill="none" stroke="#ffffff" stroke-opacity="0.15" stroke-width="1" />
        <!-- Clock ticks -->
        <line x1="755" y1="45" x2="755" y2="60" stroke="#00d2ff" stroke-width="2" />
        <line x1="755" y1="300" x2="755" y2="315" stroke="#00d2ff" stroke-width="2" />
        <line x1="620" y1="180" x2="635" y2="180" stroke="#00d2ff" stroke-width="2" />
        <line x1="875" y1="180" x2="890" y2="180" stroke="#00d2ff" stroke-width="2" />
      </g>

      <!-- Inner High-Tech Dial -->
      <g class="dial-ccw">
        <circle cx="755" cy="180" r="85" fill="none" stroke="#00d2ff" stroke-opacity="0.35" stroke-width="2" stroke-dasharray="16 10 32 8" />
        <polygon points="755,100 760,112 750,112" fill="#e6ff00" opacity="0.7" />
        <polygon points="755,260 760,248 750,248" fill="#00d2ff" opacity="0.7" />
        <polygon points="675,180 687,175 687,185" fill="#00d2ff" opacity="0.7" />
        <polygon points="835,180 823,175 823,185" fill="#00d2ff" opacity="0.7" />
      </g>

      <!-- Core Seal Center -->
      <circle cx="755" cy="180" r="45" fill="#041226" stroke="#00d2ff" stroke-width="2" opacity="0.8" />
      <text x="755" y="174" text-anchor="middle" class="font-hud" font-size="11" font-weight="700" fill="#00d2ff" letter-spacing="1">DARK HOUR</text>
      <text x="755" y="192" text-anchor="middle" class="font-hud" font-size="14" font-weight="900" fill="#ffffff" letter-spacing="2">00:00</text>
    </g>

    <!-- Submerged Water Waves & Liquid Flow (Bottom and Diagonals) -->
    <g class="wave1" opacity="0.35">
      <path d="M-50,310 C120,280 260,340 440,300 C620,260 760,330 960,290 L960,380 L-50,380 Z" fill="url(#deepWaterGrad)" />
    </g>
    <g class="wave2" opacity="0.45">
      <path d="M-30,325 C150,350 310,290 520,330 C710,365 830,300 980,335 L980,380 L-30,380 Z" fill="#0066cc" />
    </g>

    <!-- Animated Water Bubbles -->
    <g transform="translate(680, 320)" class="b1"><circle r="4" fill="#00ffff" opacity="0.7" /><circle r="1.5" cx="-1" cy="-1" fill="#fff" /></g>
    <g transform="translate(730, 340)" class="b2"><circle r="6" fill="#00d2ff" opacity="0.6" /><circle r="2" cx="-1.5" cy="-1.5" fill="#fff" /></g>
    <g transform="translate(810, 310)" class="b3"><circle r="3.5" fill="#55ffff" opacity="0.7" /><circle r="1" cx="-1" cy="-1" fill="#fff" /></g>
    <g transform="translate(860, 335)" class="b4"><circle r="5" fill="#00d2ff" opacity="0.5" /><circle r="1.8" cx="-1.2" cy="-1.2" fill="#fff" /></g>

    <!-- P3R Angled Dynamic Water Splash Ribbons (Slicing Across) -->
    <g>
      <!-- Deep Blue Base Ribbon -->
      <polygon points="-20,-20 540,-20 440,380 -20,380" fill="#071b36" opacity="0.75" />
      <!-- Dark Hour Cyan Accent Slash -->
      <polygon points="536,-20 548,-20 448,380 436,380" fill="#00d2ff" opacity="0.9" />
      <polygon points="556,-20 560,-20 460,380 456,380" fill="#ffffff" opacity="0.4" />
      <!-- Thin Neon Glow Edge -->
      <line x1="542" y1="-20" x2="442" y2="380" stroke="#00ffff" stroke-width="2" class="p3r-glow" />
    </g>

    <!-- Left HUD Content: Persona 3 Reload Protagonist Profile -->
    <g transform="translate(42, 38)">
      <!-- Top System Bar -->
      <g>
        <rect x="0" y="0" width="168" height="22" fill="#00d2ff" transform="skewX(-14)" />
        <text x="14" y="15" class="font-hud" font-size="11" font-weight="900" fill="#020813" letter-spacing="1.5">P3R // RELOAD ONLINE</text>
        
        <rect x="180" y="0" width="115" height="22" fill="#0c2d54" transform="skewX(-14)" stroke="#00d2ff" stroke-width="0.8" />
        <text x="194" y="15" class="font-hud" font-size="10.5" font-weight="700" fill="#00d2ff" letter-spacing="1">SYS://LV. 99</text>

        <text x="312" y="16" class="font-hud" font-size="11" font-weight="600" fill="#7ba3c7" letter-spacing="1">ID: #CAMANROFO34</text>
      </g>

      <!-- Main Name Heading in P3R Angled Slanted Typography -->
      <g transform="translate(0, 72)">
        <!-- Name Shadow for 3D P3R Depth -->
        <text x="3" y="3" class="font-p3r" font-size="37" fill="#020b18" letter-spacing="1.2">CAMILO ANDRÉS RODRÍGUEZ</text>
        <text x="0" y="0" class="font-p3r" font-size="37" fill="#ffffff" letter-spacing="1.2">CAMILO ANDRÉS RODRÍGUEZ</text>
      </g>

      <!-- Subtitle Skewed Ribbon -->
      <g transform="translate(0, 94)">
        <polygon points="-4,-2 460,-2 450,26 -14,26" fill="url(#cyanRibbonGrad)" transform="skewX(-14)" />
        <text x="12" y="18" class="font-p3r" font-size="14.5" fill="#020814" letter-spacing="2">SOFTWARE ENGINEER // FULL-STACK &amp; CLOUD</text>
      </g>

      <!-- P3R Status Gauges (HP: GPA / SP: ICPC Excellence) -->
      <g transform="translate(0, 144)">
        <!-- HP Gauge (Academic Excellence) -->
        <g transform="translate(0, 0)">
          <text x="0" y="14" class="font-hud" font-size="12" font-weight="900" fill="#00d2ff">HP</text>
          <!-- Gauge Background Track -->
          <polygon points="32,2 250,2 244,16 26,16" fill="#0b2447" transform="skewX(-14)" stroke="#00d2ff" stroke-width="0.8" />
          <!-- Gauge Fill -->
          <polygon points="32,2 246,2 240,16 26,16" fill="url(#hpGrad)" transform="skewX(-14)" />
          <text x="260" y="14" class="font-hud" font-size="11.5" font-weight="800" fill="#ffffff">4.93 / 5.0 <tspan fill="#00d2ff" font-size="9.5">(UPB HONORS)</tspan></text>
        </g>

        <!-- SP Gauge (Algorithmic / ICPC) -->
        <g transform="translate(0, 26)">
          <text x="0" y="14" class="font-hud" font-size="12" font-weight="900" fill="#e6ff00">SP</text>
          <!-- Gauge Background Track -->
          <polygon points="32,2 250,2 244,16 26,16" fill="#0b2447" transform="skewX(-14)" stroke="#e6ff00" stroke-width="0.8" />
          <!-- Gauge Fill -->
          <polygon points="32,2 248,2 242,16 26,16" fill="url(#spGrad)" transform="skewX(-14)" />
          <text x="260" y="14" class="font-hud" font-size="11.5" font-weight="800" fill="#ffffff">2x ICPC <tspan fill="#e6ff00" font-size="9.5">(REGIONAL FINALIST)</tspan></text>
        </g>
      </g>

      <!-- Tags & Distinction Chips -->
      <g transform="translate(0, 206)">
        <!-- Chip 1: ICPC -->
        <g transform="translate(0,0)">
          <polygon points="0,0 128,0 120,22 -8,22" fill="#082348" stroke="#00d2ff" stroke-width="1" transform="skewX(-12)" />
          <text x="8" y="15" class="font-hud" font-size="10" font-weight="700" fill="#00d2ff">★ 2x ICPC FINALIST</text>
        </g>
        <!-- Chip 2: RedColSi -->
        <g transform="translate(142,0)">
          <polygon points="0,0 148,0 140,22 -8,22" fill="#082348" stroke="#00d2ff" stroke-width="1" transform="skewX(-12)" />
          <text x="8" y="15" class="font-hud" font-size="10" font-weight="700" fill="#00d2ff">🔬 REDCOLSI FINALIST</text>
        </g>
        <!-- Chip 3: Cloud -->
        <g transform="translate(304,0)">
          <polygon points="0,0 134,0 126,22 -8,22" fill="#082348" stroke="#e6ff00" stroke-width="1" transform="skewX(-12)" />
          <text x="8" y="15" class="font-hud" font-size="10" font-weight="700" fill="#e6ff00">☁️ AWS &amp; GCP CERT</text>
        </g>
      </g>

      <!-- Bottom Status Diagnostic Line -->
      <g transform="translate(0, 256)">
        <text x="0" y="12" class="font-hud" font-size="11" fill="#88b5dd">
          ARCANA: <tspan fill="#ffffff" font-weight="700">THE CHARIOT</tspan> · SPEC-DRIVEN ARCHITECTURE · BUCARAMANGA 🇨🇴 · <tspan fill="#00d2ff" font-weight="700">SYS://READY</tspan> <tspan class="blink" fill="#00d2ff">█</tspan>
        </text>
      </g>
    </g>

    <!-- Outer Sleek Border Frame -->
    <rect width="{w-2}" height="{h-2}" x="1" y="1" rx="11" fill="none" stroke="#00d2ff" stroke-opacity="0.3" stroke-width="1.5" />
    <!-- Corner Tech Brackets -->
    <path d="M1,25 L1,1 L25,1" stroke="#00e5ff" stroke-width="3" fill="none" />
    <path d="M{w-1},25 L{w-1},1 L{w-25},1" stroke="#00e5ff" stroke-width="3" fill="none" />
    <path d="M1,{h-25} L1,{h-1} L25,{h-1}" stroke="#00e5ff" stroke-width="3" fill="none" />
    <path d="M{w-1},{h-25} L{w-1},{h-1} L{w-25},{h-1}" stroke="#00e5ff" stroke-width="3" fill="none" />
  </g>
</svg>
"""
    return svg

def gen_section_header_svg(idx, title, subtitle):
    """Generates an iconic slanted P3R menu section banner."""
    w, h = 900, 68
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(title)}">
  <defs>
    <style>
      {p3r_base_styles()}
    </style>
    <linearGradient id="secGrad_{idx}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00d2ff" />
      <stop offset="70%" stop-color="#0066cc" />
      <stop offset="100%" stop-color="#04142b" />
    </linearGradient>
    <clipPath id="secClip_{idx}">
      <rect width="{w}" height="{h}" rx="8" />
    </clipPath>
  </defs>

  <g clip-path="url(#secClip_{idx})">
    <rect width="{w}" height="{h}" fill="#040e1f" />
    
    <!-- Slanted Accent Trapeze -->
    <polygon points="-20,0 480,0 430,{h} -20,{h}" fill="url(#secGrad_{idx})" transform="skewX(-15)" />
    
    <!-- Neon Slashes -->
    <line x1="470" y1="0" x2="420" y2="{h}" stroke="#ffffff" stroke-width="2" opacity="0.8" transform="skewX(-15)" />
    <line x1="482" y1="0" x2="432" y2="{h}" stroke="#00d2ff" stroke-width="1.5" opacity="0.6" transform="skewX(-15)" />

    <!-- Index Tag -->
    <g transform="translate(34, 43)">
      <text class="font-hud" font-size="20" font-weight="900" fill="#020814">[{esc(idx)}]</text>
    </g>

    <!-- Main Title -->
    <g transform="translate(100, 44)">
      <text class="font-p3r" font-size="22" font-weight="900" fill="#ffffff" letter-spacing="2">{esc(title)}</text>
    </g>

    <!-- Subtitle / Meta HUD -->
    <g transform="translate(480, 43)">
      <text class="font-hud" font-size="11" font-weight="600" fill="#7ea7d0" letter-spacing="1.5">{esc(subtitle)}</text>
    </g>

    <!-- Frame Border -->
    <rect width="{w}" height="{h}" fill="none" stroke="#00d2ff" stroke-opacity="0.25" stroke-width="1" rx="8" />
    <!-- Left corner accent -->
    <line x1="0" y1="0" x2="0" y2="{h}" stroke="#00d2ff" stroke-width="4" />
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
