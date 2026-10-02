# Parth Mishra — Autonomous Career & Placement Workflow Engine 🚀

> **Portfolio & Architectural Documentation**  
> **Author:** [Parth Mishra](https://github.com/parthmishra9942)  
> *Final-Year B.Tech Computer Science Engineering (Specialization in AI/ML) @ VIT Bhopal University (2023–2027)*  
> **Direct Contact:** [Email](mailto:parthmishra9942@gmail.com) | [LinkedIn](https://linkedin.com/in/parth-mishra-4b7578242) | [Portfolio](https://ai-portfolio-beige-xi.vercel.app/) | [LeetCode](https://leetcode.com/u/parth213g)

---

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![LaTeX Engine](https://img.shields.io/badge/LaTeX-XeTeX-navy.svg)](https://miktex.org)
[![Agentic AI](https://img.shields.io/badge/AI-Antigravity%20%7C%20Claude-orange.svg)](https://github.com/parthmishra9942/my-job-search)
[![ATS Compliant](https://img.shields.io/badge/ATS-Strictly%201--Page-green.svg)](documents/cv/Parth_Mishra_Resume.pdf)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Executive Summary

This repository houses the personal, autonomous career and campus placement workflow engine built by **Parth Mishra**. Designed to solve the real-world operational friction faced by top-tier engineering students during placement season, the system automates:

1. **Campus Placement Notice Extraction:** Monitoring college placement inboxes (PAT) for high-urgency announcements, shortlists, and eligibility criteria (e.g. Neo PAT, Super Dream 11 LPA drives).
2. **Multi-Portal Job Discovery:** Scraping and filtering live SDE, Backend, and AI/ML openings from LinkedIn and aggregator networks with semantic ATS matching.
3. **Deterministic XeLaTeX Resume Compilation:** Programmatically rendering strictly **1-page**, ATS-optimized resumes with perfect vertical alignment, zero page overflow, and dynamic project tailoring.
4. **Verified Dispatch & Real-Time Alerts:** Generating personalized cover letters, tracking application status in CSV pipelines, and alerting the candidate of impending deadlines.

---

## 🏗️ Architecture & Component Flow

```
                      +-------------------------------------------------------+
                      |         AUTONOMOUS CAREER OPERATIONS ENGINE           |
                      |                 (Parth Mishra)                        |
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

## ⚡ Technical Modules

### 1. Campus Placement "God Bless You" Monitor (`tools/college_placement_inbox_monitor.py`)
- **IMAP Protocol Daemon:** Establishes secure SSL connections to the college email infrastructure.
- **Pattern Matching:** Filters through hundreds of circulars to flag authentic placement notifications signed with standard departmental sign-offs (*"God Bless You"*, *"Best Wishes"*, *"PAT Office"*).
- **Eligibility & Shortlist Verification:** Automatically cross-references eligibility cutoffs against Parth's credentials (CGPA 8.67, B.Tech CSE AI/ML) and parses attached `.xlsx` / Google Sheets for registration number `23BAI10539`.
- **Urgent Link Extraction:** Surfaces mandatory registration forms (e.g., Neo PAT links) before 2-to-4 hour closing deadlines.

### 2. Multi-Platform Job Scraper (`tools/multi_platform_scraper.py`)
- Searches and extracts live vacancies across LinkedIn and developer-focused aggregators.
- Targets roles aligned with Parth's core stack: Python Developer, SDE Intern, Backend Engineer (FastAPI/Node.js), and AI/ML Engineer.
- Computes ATS match scores based on technology keywords and domain requirements.

### 3. XeLaTeX Resume Production Pipeline (`documents/cv/Parth_Mishra_Resume.tex`)
- Compiled with **XeLaTeX** using the Latin Modern Roman typeface with custom navy-accented section rules (`RGB{20, 50, 125}`).
- Implements exact geometry (`0.45in` margins, `1.03` line spread, `2.3pt` item separation) to fill 100% of standard A4 vertically without blank margins or spilling to a 2nd page.
- Automated validation via `tools/verify_pdf.py` guarantees 1-page length and machine-readable text layers.

### 4. LinkedIn Showcase Generator (`tools/generate_linkedin_video.py`)
- Generates high-definition (1080p @ 30 FPS) MP4 demonstration videos of the autonomous pipeline in action using Python, Pillow, and FFmpeg.

---

## 👤 About Parth Mishra

- **Degree:** B.Tech in Computer Science & Engineering (Specialization: AI/ML)
- **Institution:** VIT Bhopal University (Batch 2023–2027)
- **Academic Standing:** CGPA 8.67 / 10.0
- **Algorithmic Problem Solving:** 200+ problems solved across LeetCode, GeeksforGeeks, and HackerRank (Two Pointers, Sliding Window, Trees, Graphs, DP).
- **Certifications:**
  - *Oracle Certified Foundations Associate — Agentic AI* (Oracle University, 2026)
  - *Applied Machine Learning in Python* (University of Michigan / Coursera, Credential: `G1Q6ZYPKPWP4`)
- **Featured Projects:**
  - [VectorDB](https://github.com/parthmishra9942/vectordb-python): In-memory vector database with HNSW graph indexing, Cosine / Euclidean distance metrics, and RAG integration.
  - [Insta Insights](https://github.com/parthmishra9942/insta-insights-api): Full-stack analytics & license verification platform built with React Native, Node.js, and PostgreSQL.
  - [Autonomous Placement Engine](https://github.com/parthmishra9942/my-job-search): This automated career workflow system.

---

## 📜 Repository Management

- **GitHub Repository:** [parthmishra9942/my-job-search](https://github.com/parthmishra9942/my-job-search)
- **License:** MIT License
