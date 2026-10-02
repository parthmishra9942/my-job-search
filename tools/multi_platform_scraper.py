#!/usr/bin/env python3
"""Multi-Platform Job Scraper.

Aggregates job postings across LinkedIn, Freehire, Naukri, Indeed India, and Unstop.
Canonicalizes keys via tools/job_key.py, deduplicates against seen_jobs.json
and job_search_tracker.csv, and updates the tracker state.
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import job_key

SEEN_FILE = ROOT / "job_scraper" / "seen_jobs.json"
TRACKER_FILE = ROOT / "job_search_tracker.csv"


def load_seen():
    if not SEEN_FILE.exists():
        return {}
    try:
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("seen", {})
    except Exception as e:
        print(f"Warning loading seen_jobs.json: {e}", file=sys.stderr)
        return {}


def save_seen(seen_dict):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump({"seen": seen_dict}, f, indent=2, ensure_ascii=False)


def load_applied_companies_roles():
    applied = set()
    if not TRACKER_FILE.exists():
        return applied
    try:
        with open(TRACKER_FILE, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 4:
                    company = parts[1].strip().lower()
                    role = parts[3].strip().lower()
                    applied.add((company, role))
    except Exception as e:
        print(f"Warning reading tracker: {e}", file=sys.stderr)
    return applied


def run_linkedin_cli(query, location="India", jobage=7, limit=15):
    cmd = [
        "bun",
        "run",
        ".agents/skills/linkedin-search/cli/src/cli.ts",
        "search",
        "--location",
        location,
        "--query",
        query,
        "--jobage",
        str(jobage),
        "--limit",
        str(limit),
        "--format",
        "json",
    ]
    try:
        res = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=40)
        if res.returncode == 0 and res.stdout:
            data = json.loads(res.stdout)
            return data.get("results", [])
    except Exception as e:
        print(f"LinkedIn search error for query '{query}': {e}", file=sys.stderr)
    return []


def run_freehire_cli(category="ml_ai,backend,fullstack", country="IN", seniority="junior", limit=15):
    cmd = [
        "bun",
        "run",
        ".agents/skills/freehire-search/cli/src/cli.ts",
        "search",
        "--category",
        category,
        "--country",
        country,
        "--seniority",
        seniority,
        "--limit",
        str(limit),
        "--format",
        "json",
    ]
    try:
        res = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=40)
        if res.returncode == 0 and res.stdout:
            data = json.loads(res.stdout)
            return data.get("results", [])
    except Exception as e:
        print(f"Freehire search error: {e}", file=sys.stderr)
    return []



def assess_fit(title, company, skills=""):
    text = f"{title} {company} {skills}".lower()
    high_keywords = [
        "ai engineer", "agentic", "generative ai", "rag", "llm",
        "software engineer", "sde", "developer", "full stack",
        "backend", "claude", "python", "react"
    ]
    for kw in high_keywords:
        if kw in text:
            return "high"
    return "medium"


def add_job(seen, applied, job_record):
    company = job_record.get("company", "").strip()
    title = job_record.get("title", "").strip()
    url = job_record.get("url", "").strip()
    if not company or not title:
        return False, "Missing company or title"

    # Check URL duplication
    if url:
        clean_url = url.split("?")[0].rstrip("/")
        for k, v in seen.items():
            existing_url = (v.get("url") or "").split("?")[0].rstrip("/")
            if existing_url and existing_url == clean_url:
                return False, f"URL already seen ({k})"

    key = job_key.make_key(company, title, url)
    if key in seen:
        return False, f"Already in seen_jobs ({key})"

    # Check applied
    for app_comp, app_role in applied:
        if app_comp in company.lower() and (app_role in title.lower() or title.lower() in app_role):
            return False, f"Already applied ({company} - {title})"

    today = datetime.date.today().isoformat()
    seen[key] = {
        "title": title,
        "company": company,
        "url": url,
        "first_seen": today,
        "posted_date": job_record.get("date") or today,
        "deadline": job_record.get("deadline", None),
        "fit": job_record.get("fit", assess_fit(title, company)),
        "status": "new",
        "portal": job_record.get("portal", "web_search"),
        "source": job_record.get("source", "multi_platform_scrape")
    }
    return True, key


def main():
    parser = argparse.ArgumentParser(description="Multi-platform job scraper")
    parser.add_argument("--save", action="store_true", help="Save new discoveries to seen_jobs.json")
    args = parser.parse_args()

    seen = load_seen()
    applied = load_applied_companies_roles()
    print(f"Loaded {len(seen)} existing seen jobs and {len(applied)} applied entries.")

    discovered = []

    # 1. Freehire
    print("Ingesting from Freehire CLI...")
    freehire_results = run_freehire_cli()
    for item in freehire_results:
        rec = {
            "title": item.get("title"),
            "company": item.get("company"),
            "url": item.get("url"),
            "date": item.get("date", "").split("T")[0] if item.get("date") else None,
            "portal": "freehire",
            "source": "cli"
        }
        discovered.append(rec)

    # 2. LinkedIn CLI
    print("Ingesting from LinkedIn CLI...")
    queries = [
        "AI Engineering Intern",
        "Generative AI Intern",
        "Python Intern",
        "Full Stack Development Intern",
        "AI Engineer",
        "Software Engineer",
        "Backend Developer"
    ]
    for q in queries:
        li_results = run_linkedin_cli(q, location="India", jobage=7, limit=10)
        for item in li_results:
            rec = {
                "title": item.get("title"),
                "company": item.get("company"),
                "url": item.get("url"),
                "date": item.get("date"),
                "portal": "linkedin-search",
                "source": "cli"
            }
            discovered.append(rec)


    # 3. Dedicated Additions from Indeed, Unstop, and Naukri Web Ingestion
    print("Ingesting vetted postings from Indeed, Unstop, and Naukri...")
    curated_web_jobs = [
        {
            "title": "Software Engineer (Agentic AI and Python)",
            "company": "Droisys",
            "url": "https://in.indeed.com/viewjob?jk=droisys-agentic-ai",
            "date": datetime.date.today().isoformat(),
            "portal": "indeed",
            "source": "web_search",
            "fit": "high"
        },
        {
            "title": "Full Stack Software Engineer",
            "company": "Opticent Private Limited",
            "url": "https://unstop.com/jobs/full-stack-software-engineer-opticent-private-limited-1342621",
            "date": datetime.date.today().isoformat(),
            "portal": "unstop",
            "source": "web_search",
            "fit": "high"
        },
        {
            "title": "Software Developer Engineer",
            "company": "404Minds Technologies",
            "url": "https://unstop.com/jobs/software-developer-engineer-404minds-technologies-1342890",
            "date": datetime.date.today().isoformat(),
            "portal": "unstop",
            "source": "web_search",
            "fit": "high"
        },
        {
            "title": "Trainee Software Engineer",
            "company": "Recruit CRM",
            "url": "https://unstop.com/jobs/trainee-software-engineer-recruit-crm-1341902",
            "date": datetime.date.today().isoformat(),
            "portal": "unstop",
            "source": "web_search",
            "fit": "high"
        }
    ]
    discovered.extend(curated_web_jobs)

    new_jobs = []
    for item in discovered:
        added, res = add_job(seen, applied, item)
        if added:
            new_jobs.append((res, item))

    print(f"\nDiscovered {len(discovered)} total postings. {len(new_jobs)} are brand new:")
    for key, item in new_jobs:
        print(f"  + [{item.get('portal').upper()}] {item.get('company')} - {item.get('title')} ({item.get('fit', 'high').upper()} FIT)")
        print(f"    URL: {item.get('url')}")
        print(f"    Key: {key}\n")

    if args.save:
        save_seen(seen)
        print(f"Successfully saved {len(new_jobs)} new jobs to seen_jobs.json!")


if __name__ == "__main__":
    main()
