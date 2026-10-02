# Parth Mishra — Autonomous Placement & Job Search Workflow Engine 🚀

> **Engineered by [Parth Mishra](https://github.com/parthmishra9942)**  
> *Final-Year B.Tech Computer Science Engineering (AI/ML) @ VIT Bhopal University*  
> **Connect:** [LinkedIn](https://linkedin.com/in/parth-mishra-4b7578242) | [Portfolio](https://ai-portfolio-beige-xi.vercel.app/) | [LeetCode](https://leetcode.com/u/parth213g) | [Email](mailto:parthmishra9942@gmail.com)

<p align="center">
  <img src="assets/mascot/pip_flight_loop.gif" alt="Autonomous Career Engine Mascot" width="160">
</p>

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![LaTeX Engine](https://img.shields.io/badge/LaTeX-XeTeX-navy.svg)](https://miktex.org)
[![Agentic AI](https://img.shields.io/badge/AI-Antigravity%20%7C%20Claude-orange.svg)](https://github.com/parthmishra9942/my-job-search)
[![ATS Compliant](https://img.shields.io/badge/ATS-Strictly%201--Page-green.svg)](documents/cv/Parth_Mishra_Resume.pdf)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An end-to-end autonomous career operations engine engineered by **Parth Mishra** to automate high-velocity campus placement workflows and off-campus tech applications without compromising quality, authenticity, or ATS compliance.

---

## 💡 The Problem & Genesis

As a final-year Computer Science (AI/ML) undergrad at VIT Bhopal, managing college placement drives alongside external tech applications created extreme operational friction:

1. **Information Overload:** Over 80+ daily campus emails containing announcements, eligibility lists, and Google Forms with tight 2-to-4 hour closing windows.
2. **Missing Crucial Windows:** Urgent registration links (e.g. Neo PAT, Super Dream 11 LPA drives) easily buried under general student correspondence.
3. **Application Fatigue:** Manually adjusting resumes, calculating ATS compatibility, and attaching PDFs across dozens of portals led to human error or generic submissions.

**The Solution:** Rather than relying on fragile third-party mass-apply bots that spam generic resumes, this repository implements a **deterministic agentic architecture** running locally on Python, IMAP/SMTP protocols, and XeLaTeX.

---

## 🏗️ System Architecture

```
                  +-------------------------------------------------------+
                  |         AUTONOMOUS CAREER OPERATIONS ENGINE           |
                  |                   (Parth Mishra)                      |
                  +-------------------------------------------------------+
                                              |
     +----------------------------------------+----------------------------------------+
     |                                        |                                        |
     v                                        v                                        v
+------------------------+       +------------------------+       +------------------------+
| 1. MULTI-PORTAL        |       | 2. T&P "GOD BLESS YOU" |       | 3. DETERMINISTIC ATS   |
|    JOB SCRAPER         |       |    INBOX MONITOR       |       |    RESUME COMPILER     |
+------------------------+       +------------------------+       +------------------------+
| - LinkedIn Search API  |       | - IMAP SSL Mail Daemon |       | - XeLaTeX Build Engine |
| - Freehire Aggregator  |       | - Pattern & CTC Parser |       | - Strictly 1-Page      |
| - Semantic ATS Matcher |       | - Neo PAT Link Extractor|       | - Zero Text Overflow   |
| - Duplicate Filter     |       | - CGPA Cutoff Checker  |       | - PDF Text Layer Check |
+------------------------+       +------------------------+       +------------------------+
             |                                |                                |
             +--------------------------------+--------------------------------+
                                              |
                                              v
                              +-------------------------------+
                              | 4. VERIFIED DISPATCH & TRACK  |
                              +-------------------------------+
                              | - SMTP TLS Handshake          |
                              | - Tailored Cover Letters      |
                              | - CSV Timestamped Logging     |
                              | - Proactive TTS Audio Alerts  |
                              +-------------------------------+
```

---

## ⚡ Core Modules

### 1. Autonomous Job Scraper (`tools/multi_platform_scraper.py`)
- Searches live roles across LinkedIn, Freehire, and tech boards.
- Targets roles tailored to: SDE Intern, Python Developer, FastAPI Backend Engineer, AI/ML Specialist.
- Evaluates candidate profile alignment using automated keyword density and semantic scoring.

### 2. Campus Placement "God Bless You" Mail Scanner (`tools/college_placement_inbox_monitor.py`)
- Connects securely to college email via IMAP SSL.
- Identifies official Placement & Training (PAT) notices using sign-off signatures (*"God Bless You"*, *"Best Wishes"*).
- Extracts critical parameters:
  - **Company & Role:** e.g., VComply Technologies (11 LPA Super Dream).
  - **Eligibility Verification:** Compares cutoff requirements against candidate credentials (CGPA 8.67).
  - **Deadline Extraction:** Flags time-sensitive registration windows (e.g. *"Today by 5:00 PM"*).
  - **Shortlist Hunter:** Automatically inspects attached `.xlsx` sheets and Google Sheets for student registration numbers (`23BAI10539`) and Neo PAT IDs.

### 3. Strictly 1-Page XeLaTeX Resume Engine (`documents/cv/Parth_Mishra_Resume.tex`)
- High-performance, clean typographic layout built with Latin Modern fonts and deep navy blue styling (`RGB{20, 50, 125}`).
- Symmetrical geometry (`0.45in` margins) engineered to fill 100% of the page vertical space with zero awkward bottom gaps.
- Automated verification via `tools/verify_pdf.py` guaranteeing exact 1-page compliance and extractable ATS text layer.

### 4. Application Dispatch & Real-Time Alert Engine (`tools/personal_inbox_monitor.py` & `tools/run_all_monitors.py`)
- Background monitors that keep track of application responses, interview invitations, and Google Meet/Zoom links.
- Logs all submitted applications to `job_search_tracker.csv`.
- Optional Edge-TTS voice daemon that provides audible J.A.R.V.I.S.-style reminders when deadlines approach.

---

## 🛠️ Tech Stack

- **Core Runtime:** Python 3.12 (Standard Library, IMAP, SMTP, BeautifulSoup, OpenPyXL, Pillow)
- **Typesetting & PDF Engine:** MiKTeX / XeLaTeX
- **Agentic Workflow Framework:** Google Antigravity & Claude Code Agent Skills
- **Audio & Media Production:** Microsoft Edge-TTS, FFmpeg 8.1.2
- **Data & APIs:** RESTful JSON APIs, PostgreSQL, CSV Logging

---

## 🚀 Quickstart Guide

### 1. Fork and clone

```bash
gh repo fork parthmishra9942/my-job-search --clone
cd my-job-search
```

> [!IMPORTANT]
> **A fork of this repo is always public** — GitHub does not allow private forks of
> public repositories — and `/setup` writes your real personal data (name,
> contact details, employment history) into **tracked** files.
> If this copy is for your own job search rather than for contributing changes back,
> follow [SETUP.md section 8](SETUP.md#8-pulling-upstream-updates-into-your-fork) to configure a private remote.

### 2. Set Up Environment
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Compile the 1-Page ATS Resume
```bash
cd documents/cv
xelatex -interaction=nonstopmode Parth_Mishra_Resume.tex
python ../../tools/verify_pdf.py Parth_Mishra_Resume.pdf
```

### 4. Run the Placement Inbox Scanner
```bash
# Set up secure IMAP credentials (stored locally in gitignored config)
python tools/college_placement_inbox_monitor.py --setup

# Execute live scan
python tools/college_placement_inbox_monitor.py
```

### 5. Run the Multi-Platform Scraper
```bash
python tools/multi_platform_scraper.py --target linkedin --role "SDE Intern"
```

### 6. Generate the LinkedIn Showcase Video
```bash
python tools/generate_linkedin_video.py
```

---

## 👤 Candidate Profile & Credentials

This repository is configured for **Parth Mishra**:
- **Education:** B.Tech Computer Science & Engineering (AI/ML), VIT Bhopal University (2023–2027) | **CGPA: 8.67**
- **Competitive Programming:** 200+ algorithmic problems solved across LeetCode, GeeksforGeeks, and HackerRank (Two Pointers, Sliding Window, Trees, Graphs, Dynamic Programming).
- **Verified Certifications:**
  - *Oracle Certified Foundations Associate — Agentic AI* (Oracle University, 2026)
  - *Applied Machine Learning in Python* (University of Michigan / Coursera, Credential: `G1Q6ZYPKPWP4`)
- **Key Projects:**
  - [VectorDB](https://github.com/parthmishra9942/vectordb-python): In-memory vector database with HNSW graph traversal and RAG pipeline.
  - [Insta Insights](https://github.com/parthmishra9942/insta-insights-api): Full-stack mobile analytics and license manager (React Native, Node.js, PostgreSQL).
  - [Autonomous Placement Engine](https://github.com/parthmishra9942/my-job-search): This automated career workflow system.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
