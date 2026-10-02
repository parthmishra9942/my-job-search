#!/usr/bin/env python3
"""
Generate a professional Full HD (1920x1080 @ 30fps) LinkedIn showcase video
demonstrating Parth Mishra's autonomous job search, college placement email scanner,
and automated resume tailoring & dispatch pipeline.
"""

import os
import sys
import subprocess
from PIL import Image, ImageDraw, ImageFont

OUTPUT_PATH = r"C:\Users\parth\Downloads\Parth_Mishra_Placement_Automation_Showcase.mp4"
RESUME_PNG = "resume_embed_preview-1.png"

# Color Palette (Dark Theme / Cyberpunk Tech)
BG_COLOR = (11, 15, 25)           # #0B0F19
PANEL_BG = (21, 28, 44)           # #151C2C
PANEL_BORDER = (42, 54, 79)       # #2A364F
ACCENT_CYAN = (0, 229, 255)       # #00E5FF
ACCENT_GREEN = (0, 245, 155)      # #00F59B
ACCENT_PURPLE = (168, 85, 247)    # #A855F7
ACCENT_AMBER = (255, 180, 0)      # #FFB400
ACCENT_RED = (255, 75, 75)        # #FF4B4B
TEXT_WHITE = (248, 250, 252)      # #F8FAFC
TEXT_MUTED = (148, 163, 184)      # #94A3B8

# Fonts
FONTS_DIR = r"C:\Windows\Fonts"
font_title = ImageFont.truetype(os.path.join(FONTS_DIR, "segoeuib.ttf"), 48)
font_subtitle = ImageFont.truetype(os.path.join(FONTS_DIR, "segoeui.ttf"), 25)
font_heading = ImageFont.truetype(os.path.join(FONTS_DIR, "segoeuib.ttf"), 30)
font_subheading = ImageFont.truetype(os.path.join(FONTS_DIR, "segoeuib.ttf"), 22)
font_body = ImageFont.truetype(os.path.join(FONTS_DIR, "segoeui.ttf"), 20)
font_body_bold = ImageFont.truetype(os.path.join(FONTS_DIR, "segoeuib.ttf"), 20)
font_small = ImageFont.truetype(os.path.join(FONTS_DIR, "segoeui.ttf"), 16)
font_small_bold = ImageFont.truetype(os.path.join(FONTS_DIR, "segoeuib.ttf"), 16)

# Monospace for code/terminal
font_code_lg = ImageFont.truetype(os.path.join(FONTS_DIR, "consolab.ttf"), 22)
font_code = ImageFont.truetype(os.path.join(FONTS_DIR, "consola.ttf"), 19)
font_code_sm = ImageFont.truetype(os.path.join(FONTS_DIR, "consola.ttf"), 16)

# Load and prepare resume thumbnail
resume_img = None
if os.path.exists(RESUME_PNG):
    raw_res = Image.open(RESUME_PNG)
    target_h = 680
    target_w = int(raw_res.width * (target_h / raw_res.height))
    resume_img = raw_res.resize((target_w, target_h), Image.Resampling.LANCZOS)

def draw_top_nav(draw, current_stage):
    draw.rectangle([0, 0, 1920, 70], fill=(15, 21, 34))
    draw.line([0, 70, 1920, 70], fill=PANEL_BORDER, width=2)
    
    # Left logo/badge
    draw.rounded_rectangle([40, 16, 260, 54], radius=6, fill=(26, 36, 56), outline=ACCENT_CYAN, width=1)
    draw.text((55, 24), ">> AI Placement Engine", fill=ACCENT_CYAN, font=font_small_bold)

    # Breadcrumbs / stages
    stages = [
        ("1. LinkedIn Scraper", 1),
        ("2. College T&P Scanner", 2),
        ("3. Tailor & Email Dispatch", 3),
    ]
    start_x = 380
    for name, stage_idx in stages:
        is_active = (current_stage == stage_idx)
        color = ACCENT_GREEN if is_active else TEXT_MUTED
        bg = (24, 40, 50) if is_active else (20, 26, 40)
        border = ACCENT_GREEN if is_active else PANEL_BORDER
        
        draw.rounded_rectangle([start_x, 16, start_x + 230, 54], radius=6, fill=bg, outline=border, width=1)
        draw.text((start_x + 18, 24), name, fill=color, font=font_small_bold)
        start_x += 250

    # Right user pill
    draw.rounded_rectangle([1560, 16, 1880, 54], radius=6, fill=(26, 36, 56), outline=PANEL_BORDER, width=1)
    draw.ellipse([1578, 27, 1594, 43], fill=ACCENT_GREEN)
    draw.text((1608, 24), "Parth Mishra (VIT Bhopal)", fill=TEXT_WHITE, font=font_small_bold)

def draw_card(draw, x, y, w, h, title="", badge="", badge_color=ACCENT_CYAN):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=PANEL_BG, outline=PANEL_BORDER, width=2)
    if title:
        header_h = 55
        draw.rounded_rectangle([x, y, x + w, y + header_h], radius=12, fill=(26, 35, 54))
        draw.rectangle([x, y + header_h - 12, x + w, y + header_h], fill=(26, 35, 54))
        draw.line([x, y + header_h, x + w, y + header_h], fill=PANEL_BORDER, width=1)
        
        # Window controls
        draw.ellipse([x + 20, y + 22, x + 32, y + 34], fill=(255, 95, 86))
        draw.ellipse([x + 40, y + 22, x + 52, y + 34], fill=(255, 189, 46))
        draw.ellipse([x + 60, y + 22, x + 72, y + 34], fill=(39, 201, 63))
        
        draw.text((x + 90, y + 16), title, fill=TEXT_WHITE, font=font_subheading)
        
        if badge:
            badge_len = int(draw.textlength(badge, font=font_small_bold))
            badge_w = badge_len + 30
            bx = x + w - badge_w - 20
            draw.rounded_rectangle([bx, y + 14, bx + badge_w, y + 42], radius=6, fill=(15, 25, 35), outline=badge_color, width=1)
            draw.text((bx + 15, y + 18), badge, fill=badge_color, font=font_small_bold)

# ============================================================
# SCENE 1: Intro Card (0 - 150 frames, 5 seconds)
# ============================================================
def render_scene_1(frame_idx):
    img = Image.new("RGB", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_top_nav(draw, 0)

    for gx in range(100, 1920, 140):
        draw.line([gx, 100, gx, 1000], fill=(18, 24, 38), width=1)
    for gy in range(100, 1080, 120):
        draw.line([100, gy, 1820, gy], fill=(18, 24, 38), width=1)

    card_x, card_y, card_w, card_h = 240, 160, 1440, 780
    draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=16, fill=PANEL_BG, outline=PANEL_BORDER, width=2)
    draw.line([card_x + 40, card_y, card_x + card_w - 40, card_y], fill=ACCENT_CYAN, width=3)

    # Intro Pill
    pill_text = "FULL-STACK AGENTIC REPOSITORY SHOWCASE"
    pw = int(draw.textlength(pill_text, font=font_small_bold)) + 36
    draw.rounded_rectangle([300, 220, 300 + pw, 260], radius=8, fill=(18, 38, 55), outline=ACCENT_CYAN, width=1)
    draw.text((318, 228), pill_text, fill=ACCENT_CYAN, font=font_small_bold)

    # Headlines
    draw.text((300, 290), "How I Automated My Entire", fill=TEXT_WHITE, font=font_title)
    draw.text((300, 355), "Campus Placement & Job Search with AI", fill=ACCENT_GREEN, font=font_title)

    draw.text((300, 440), "An autonomous agentic pipeline that discovers target jobs, monitors placement cell", fill=TEXT_MUTED, font=font_subtitle)
    draw.text((300, 475), "emails, tails college assessment forms, and drafts tailored ATS resumes.", fill=TEXT_MUTED, font=font_subtitle)

    pillars = [
        ("Pillar 1: Multi-Portal Scraping", "Scrapes LinkedIn, ATS boards & aggregator APIs. Evaluates role fit & keyword density.", ACCENT_CYAN),
        ("Pillar 2: 'God Bless You' Scanner", "Monitors college T&P cell inbox. Extracts company drives, CTC, & deadlines.", ACCENT_AMBER),
        ("Pillar 3: Dynamic Resume Dispatch", "Compiles strictly 1-page LaTeX resumes & automates verified direct email submissions.", ACCENT_GREEN),
    ]

    px = 300
    for p_title, p_desc, p_col in pillars:
        draw.rounded_rectangle([px, 560, px + 400, 840], radius=10, fill=(16, 22, 36), outline=PANEL_BORDER, width=1)
        draw.line([px + 20, 560, px + 100, 560], fill=p_col, width=3)
        draw.text((px + 20, 585), p_title, fill=p_col, font=font_subheading)
        
        words = p_desc.split()
        line1 = " ".join(words[:5])
        line2 = " ".join(words[5:10])
        line3 = " ".join(words[10:])
        draw.text((px + 20, 635), line1, fill=TEXT_WHITE, font=font_body)
        draw.text((px + 20, 665), line2, fill=TEXT_WHITE, font=font_body)
        draw.text((px + 20, 695), line3, fill=TEXT_WHITE, font=font_body)
        
        draw.rounded_rectangle([px + 20, 770, px + 220, 810], radius=6, fill=(24, 32, 48))
        draw.text((px + 35, 780), "STATUS: ACTIVE [OK]", fill=ACCENT_GREEN, font=font_small_bold)

        px += 440

    return img

# ============================================================
# SCENE 2: LinkedIn Job Scraping (150 - 450 frames, 10 seconds)
# ============================================================
def render_scene_2(frame_idx):
    img = Image.new("RGB", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_top_nav(draw, 1)

    t = (frame_idx - 150) / 300.0

    # Left: Terminal Card
    draw_card(draw, 80, 120, 960, 880, title="bash: ~/my-job-search/tools", badge="SCRAPER RUNNING", badge_color=ACCENT_CYAN)

    cmd_text = "python tools/multi_platform_scraper.py --target linkedin --role 'SDE Intern'"
    draw.text((110, 200), "$ " + cmd_text[:int(len(cmd_text) * min(t * 3, 1.0))], fill=ACCENT_CYAN, font=font_code_lg)

    terminal_lines = [
        (0.12, "[INIT] Connecting to LinkedIn Job Search & Aggregator Engine...", TEXT_MUTED),
        (0.22, "[CONFIG] Query: Software Development Engineer | Target: Pan-India & Remote", TEXT_WHITE),
        (0.32, "[FETCH] HTTP GET /jobs/search?keywords=Python+FastAPI+React -> 200 OK", ACCENT_GREEN),
        (0.42, "[PARSE] Discovered 28 live listings matching candidate parameters", TEXT_WHITE),
        (0.52, "[FILTER] Filtering out senior roles (>2 yrs req) -> 12 entry/intern roles isolated", TEXT_MUTED),
        (0.62, "[ANALYZE] Running ATS keyword extractor across Job Descriptions...", ACCENT_AMBER),
        (0.72, "[MATCH] Evaluating candidate profile against EVE Healthcare (SDE Intern)...", TEXT_WHITE),
        (0.82, "[SUCCESS] Extracted verified hiring contact: careers@eve-healthcare.com", ACCENT_GREEN),
        (0.90, "[STORAGE] Saved candidate listings to seen_jobs.json & job_search_tracker.csv", ACCENT_CYAN),
    ]

    ly = 260
    for threshold, line, col in terminal_lines:
        if t >= threshold:
            draw.text((110, ly), line, fill=col, font=font_code)
            ly += 42

    # Right: Matched Job Card
    draw_card(draw, 1080, 120, 760, 880, title="Live Job Opportunity Match", badge="ATS SCORE: 96%", badge_color=ACCENT_GREEN)

    # Job Header Box
    draw.rounded_rectangle([1120, 200, 1800, 360], radius=10, fill=(28, 38, 58), outline=PANEL_BORDER, width=1)
    draw.text((1150, 225), "EVE Healthcare Systems", fill=ACCENT_CYAN, font=font_heading)
    draw.text((1150, 275), "Software Development Engineer (Backend Intern)", fill=TEXT_WHITE, font=font_subheading)
    draw.text((1150, 315), "Location: Remote / Gurgaon  |  Stipend: Paid  |  Closes: Tonight 11:59 PM", fill=TEXT_MUTED, font=font_body)

    # ATS Match Progress Bar
    draw.text((1120, 400), "Candidate Profile Compatibility Match", fill=TEXT_WHITE, font=font_subheading)
    draw.rounded_rectangle([1120, 440, 1800, 475], radius=8, fill=(18, 24, 38))
    
    score_pct = min(t * 1.3, 0.96)
    bar_w = int((1800 - 1120) * score_pct)
    draw.rounded_rectangle([1120, 440, 1120 + bar_w, 475], radius=8, fill=ACCENT_GREEN)
    draw.text((1120 + bar_w - 75, 447), f"{int(score_pct*100)}%", fill=(10, 20, 30), font=font_small_bold)

    # Keywords matched chips
    draw.text((1120, 520), "Extracted Key Requirements vs. Verified Profile:", fill=TEXT_MUTED, font=font_body_bold)
    
    chips = [
        ("FastAPI / REST APIs", True),
        ("Python (Proficient)", True),
        ("PostgreSQL Schemas", True),
        ("Clean Architecture", True),
        ("Agentic AI / Claude", True),
        ("Docker & Linux", True),
    ]
    cx, cy = 1120, 565
    for name, matched in chips:
        bg = (18, 48, 36) if matched else (40, 25, 25)
        border = ACCENT_GREEN if matched else ACCENT_RED
        col = ACCENT_GREEN if matched else ACCENT_RED
        draw.rounded_rectangle([cx, cy, cx + 200, cy + 45], radius=6, fill=bg, outline=border, width=1)
        draw.text((cx + 15, cy + 12), f"[OK] {name}", fill=col, font=font_small_bold)
        cx += 220
        if cx > 1650:
            cx = 1120
            cy += 60

    # Decision Box
    draw.rounded_rectangle([1120, 720, 1800, 850], radius=10, fill=(18, 34, 48), outline=ACCENT_CYAN, width=1)
    draw.text((1150, 745), ">> Autonomous Agent Action:", fill=ACCENT_CYAN, font=font_subheading)
    draw.text((1150, 790), "* Role queued for Stage 3 tailored LaTeX application", fill=TEXT_WHITE, font=font_body)
    draw.text((1150, 820), "* Auto-generated verified GitHub portfolio references", fill=TEXT_MUTED, font=font_body)

    return img

# ============================================================
# SCENE 3: T&P College Mail Scanner (450 - 750 frames, 10 seconds)
# ============================================================
def render_scene_3(frame_idx):
    img = Image.new("RGB", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_top_nav(draw, 2)

    t = (frame_idx - 450) / 300.0

    # Left: Incoming College Email
    draw_card(draw, 80, 120, 920, 880, title="T&P Inbox: PAT Placement Cell", badge="LIVE INBOX SCAN", badge_color=ACCENT_AMBER)

    draw.rounded_rectangle([110, 200, 970, 330], radius=8, fill=(28, 36, 54), outline=PANEL_BORDER, width=1)
    draw.text((130, 215), "From: VIT Bhopal Placement Office <pat@vitbhopal.ac.in>", fill=TEXT_WHITE, font=font_body_bold)
    draw.text((130, 250), "Subject: Campus Drive 2026: VComply Technologies (Super Dream 11 LPA)", fill=ACCENT_AMBER, font=font_subheading)
    draw.text((130, 290), "Date: Friday, Oct 2, 2026 | Priority: HIGH (Action Required Today)", fill=TEXT_MUTED, font=font_small)

    draw.rounded_rectangle([110, 360, 970, 720], radius=8, fill=(18, 24, 38), outline=PANEL_BORDER, width=1)
    
    email_text = [
        "Dear Students,",
        "",
        "Greetings from Career Development & Placement Cell!",
        "",
        "We are pleased to announce the campus recruitment drive for",
        "VComply Technologies (11 LPA Super Dream Category).",
        "",
        "- Eligible Branches: B.Tech CSE, AI/ML (CGPA >= 8.5)",
        "- Mandatory Registration on Neo PAT Portal: https://neopat.in/",
        "- Registration Window Closes: TODAY, October 2 @ 5:00 PM Sharp!",
        "",
        "Students failing to register before the deadline will not be permitted.",
        "",
        "Best Wishes & God Bless You!",
        "Placement & Training Cell"
    ]
    ey = 385
    for l in email_text:
        col = ACCENT_AMBER if "God Bless You" in l or "11 LPA" in l or "5:00 PM" in l else TEXT_MUTED
        if "God Bless You" in l:
            col = ACCENT_GREEN
            draw.text((130, ey), l, fill=col, font=font_body_bold)
        else:
            draw.text((130, ey), l, fill=col, font=font_body)
        ey += 22

    draw.rounded_rectangle([110, 750, 970, 850], radius=8, fill=(24, 32, 48), outline=PANEL_BORDER, width=1)
    draw.text((130, 775), ">> Mail Signature Parser:", fill=TEXT_WHITE, font=font_body_bold)
    draw.text((130, 810), "Identified authentic Placement Cell notice via 'God Bless You' signoff token.", fill=ACCENT_GREEN, font=font_small)

    # Right: AI Extraction Card
    draw_card(draw, 1040, 120, 800, 880, title="Autonomous Placement Intelligence", badge="DEADLINE DETECTED", badge_color=ACCENT_RED)

    metrics = [
        ("Company Name", "VComply Technologies", ACCENT_CYAN),
        ("Role Category", "11 LPA (Super Dream)", ACCENT_AMBER),
        ("Eligibility Cutoff", "CGPA 8.5+ (Parth: 8.67 CGPA -> ELIGIBLE [PASS])", ACCENT_GREEN),
        ("Registration Link", "https://neopat.in/placement/drive/vcomply", TEXT_WHITE),
        ("Strict Deadline", "TODAY @ 5:00 PM IST (Mandatory)", ACCENT_RED),
    ]

    my = 200
    for label, val, col in metrics:
        draw.rounded_rectangle([1070, my, 1810, my + 80], radius=8, fill=(24, 32, 50), outline=PANEL_BORDER, width=1)
        draw.text((1090, my + 15), label.upper(), fill=TEXT_MUTED, font=font_small_bold)
        draw.text((1090, my + 42), val, fill=col, font=font_subheading)
        my += 95

    # Countdown Box
    draw.rounded_rectangle([1070, 690, 1810, 850], radius=10, fill=(35, 20, 25), outline=ACCENT_RED, width=2)
    draw.text((1100, 715), "[URGENT] ACTION DISPATCHED:", fill=ACCENT_RED, font=font_heading)
    draw.text((1100, 765), "- Neo PAT Form link surfaced directly to candidate dashboard", fill=TEXT_WHITE, font=font_body)
    draw.text((1100, 805), "- Spoken audio alert scheduled 1 hour before cutoff via TTS Daemon", fill=ACCENT_AMBER, font=font_body)

    return img

# ============================================================
# SCENE 4: Resume Tailoring & Dispatch (750 - 1050 frames, 10 seconds)
# ============================================================
def render_scene_4(frame_idx):
    img = Image.new("RGB", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_top_nav(draw, 3)

    t = (frame_idx - 750) / 300.0

    # Left: Actual 1-Page Resume Rendering
    draw_card(draw, 80, 120, 840, 880, title="ATS Resume Engine (Strictly 1-Page)", badge="LATEX COMPILED", badge_color=ACCENT_GREEN)

    if resume_img:
        rx = 120
        ry = 190
        draw.rectangle([rx - 6, ry - 6, rx + resume_img.width + 6, ry + resume_img.height + 6], fill=(40, 60, 100))
        img.paste(resume_img, (rx, ry))

    draw.rounded_rectangle([120, 890, 880, 960], radius=8, fill=(16, 28, 44), outline=ACCENT_CYAN, width=1)
    draw.text((140, 905), "[PASS] XeLaTeX Output - 1 Page Zero Overflows - VectorDB & ML Certs", fill=ACCENT_CYAN, font=font_small_bold)

    # Right: Direct Application Dispatch Card
    draw_card(draw, 960, 120, 880, 880, title="Verified Application Dispatch Engine", badge="SMTP DISPATCHED", badge_color=ACCENT_GREEN)

    draw.rounded_rectangle([1000, 200, 1800, 600], radius=10, fill=(22, 30, 48), outline=PANEL_BORDER, width=1)
    
    draw.text((1030, 230), "To:", fill=TEXT_MUTED, font=font_body_bold)
    draw.text((1150, 230), "careers@eve-healthcare.com (SDE Intern Hiring Team)", fill=TEXT_WHITE, font=font_body)
    draw.line([1030, 270, 1770, 270], fill=PANEL_BORDER, width=1)

    draw.text((1030, 290), "Subject:", fill=TEXT_MUTED, font=font_body_bold)
    draw.text((1150, 290), "Application: SDE Intern (Backend) - Parth Mishra", fill=ACCENT_CYAN, font=font_body_bold)
    draw.line([1030, 330, 1770, 330], fill=PANEL_BORDER, width=1)

    draw.text((1030, 350), "Attachment:", fill=TEXT_MUTED, font=font_body_bold)
    draw.rounded_rectangle([1150, 345, 1550, 385], radius=6, fill=(18, 40, 60), outline=ACCENT_CYAN, width=1)
    draw.text((1165, 355), "[PDF] Parth_Mishra_Resume.pdf (35.8 KB)", fill=ACCENT_CYAN, font=font_small_bold)
    draw.line([1030, 405, 1770, 405], fill=PANEL_BORDER, width=1)

    draw.text((1030, 425), "Body Preview:", fill=TEXT_MUTED, font=font_body_bold)
    body_lines = [
        "Dear Hiring Team at EVE Healthcare,",
        "",
        "I am writing to express my strong interest in the SDE Intern (Backend) role.",
        "As a B.Tech CSE (AI/ML) student at VIT Bhopal (CGPA 8.67), I have engineered",
        "vector database indexing (HNSW) from first principles and full-stack PostgreSQL APIs.",
        "",
        "My ATS-tailored resume is attached for your review.",
    ]
    by = 460
    for bl in body_lines:
        draw.text((1030, by), bl, fill=TEXT_MUTED, font=font_small)
        by += 20

    # Dispatch Status Banner
    draw.rounded_rectangle([1000, 640, 1800, 830], radius=10, fill=(16, 40, 30), outline=ACCENT_GREEN, width=2)
    draw.text((1030, 670), "APPLICATION DISPATCH STATUS: SUCCESSFUL [OK]", fill=ACCENT_GREEN, font=font_heading)
    draw.text((1030, 725), "- SMTP Handshake Verified with Gmail TLS Endpoint", fill=TEXT_WHITE, font=font_body)
    draw.text((1030, 760), "- Application recorded in job_search_tracker.csv with timestamp", fill=TEXT_MUTED, font=font_body)
    draw.text((1030, 795), "- Follow-up reminder scheduled automatically in 5 business days", fill=TEXT_MUTED, font=font_body)

    return img

# ============================================================
# SCENE 5: Architecture & Outro (1050 - 1200 frames, 5 seconds)
# ============================================================
def render_scene_5(frame_idx):
    img = Image.new("RGB", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_top_nav(draw, 3)

    card_x, card_y, card_w, card_h = 240, 150, 1440, 800
    draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=16, fill=PANEL_BG, outline=PANEL_BORDER, width=2)
    draw.line([card_x + 40, card_y, card_x + card_w - 40, card_y], fill=ACCENT_GREEN, width=3)

    pw = int(draw.textlength("END-TO-END AUTOMATION COMPLETE", font=font_small_bold)) + 36
    draw.rounded_rectangle([300, 210, 300 + pw, 250], radius=8, fill=(18, 38, 35), outline=ACCENT_GREEN, width=1)
    draw.text((318, 218), "END-TO-END AUTOMATION COMPLETE", fill=ACCENT_GREEN, font=font_small_bold)

    draw.text((300, 280), "Deterministic Velocity.", fill=TEXT_WHITE, font=font_title)
    draw.text((300, 345), "Zero Manual Redundancy.", fill=ACCENT_CYAN, font=font_title)

    draw.text((300, 440), "By integrating autonomous portal scrapers, college placement inbox watchers,", fill=TEXT_MUTED, font=font_subtitle)
    draw.text((300, 480), "and dynamic LaTeX compilers, every application is tailored, tracked, and verified.", fill=TEXT_MUTED, font=font_subtitle)

    # Dynamic Tech Stack Pills
    draw.text((300, 560), "BUILT WITH:", fill=TEXT_WHITE, font=font_subheading)
    tech_stack = [
        "Python 3.12", "XeLaTeX Engine", "Antigravity & Gemini CLI",
        "FastAPI & PostgreSQL", "FFmpeg", "Edge-TTS Voice"
    ]
    tx, ty = 300, 610
    for t_item in tech_stack:
        w_pill = int(draw.textlength(t_item, font=font_small_bold)) + 36
        draw.rounded_rectangle([tx, ty, tx + w_pill, ty + 46], radius=8, fill=(24, 34, 52), outline=PANEL_BORDER, width=1)
        draw.text((tx + 18, ty + 14), t_item, fill=ACCENT_CYAN, font=font_small_bold)
        tx += w_pill + 20

    # Links Card
    draw.rounded_rectangle([300, 700, 1620, 870], radius=12, fill=(16, 24, 38), outline=ACCENT_GREEN, width=1)
    draw.text((340, 735), "Parth Mishra  |  B.Tech Computer Science (AI/ML)  |  VIT Bhopal", fill=TEXT_WHITE, font=font_subheading)
    draw.text((340, 780), "GitHub: github.com/parthmishra9942/my-job-search", fill=ACCENT_CYAN, font=font_body)
    draw.text((340, 815), "Portfolio: ai-portfolio-beige-xi.vercel.app  •  LinkedIn: in/parth-mishra-4b7578242", fill=TEXT_MUTED, font=font_body)

    return img

def main():
    print(f"Generating LinkedIn Video: {OUTPUT_PATH}")
    print("Canvas: 1920x1080 @ 30 FPS | Total: 1200 frames (40 seconds)")

    ffmpeg_cmd = [
        r"C:\ffmpeg\bin\ffmpeg.exe", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", "1920x1080",
        "-pix_fmt", "rgb24",
        "-r", "30",
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "medium",
        "-crf", "18",
        OUTPUT_PATH
    ]

    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    TOTAL_FRAMES = 1200

    try:
        for f in range(TOTAL_FRAMES):
            if f < 150:
                frame = render_scene_1(f)
            elif f < 450:
                frame = render_scene_2(f)
            elif f < 750:
                frame = render_scene_3(f)
            elif f < 1050:
                frame = render_scene_4(f)
            else:
                frame = render_scene_5(f)

            proc.stdin.write(frame.tobytes())

            if (f + 1) % 150 == 0 or f == TOTAL_FRAMES - 1:
                print(f"Rendered frame {f + 1}/{TOTAL_FRAMES} ({(f + 1)/TOTAL_FRAMES*100:.1f}%)")

        proc.stdin.close()
        proc.wait()
        print(f"\nSUCCESS! Video generated and saved to:\n{OUTPUT_PATH}")
        print(f"File size: {os.path.getsize(OUTPUT_PATH) / (1024*1024):.2f} MB")
    except Exception as e:
        print(f"Error during video generation: {e}")
        proc.kill()
        sys.exit(1)

if __name__ == "__main__":
    main()
