#!/usr/bin/env python3
"""Unified Inbox Monitor Runner for Job Applications & Placement Drives.

Executes both monitors sequentially:
1. College Placement Monitor (VIT Bhopal institutional email: parth.23bai10539@vitbhopal.ac.in)
   - Filters ~90 daily campus emails
   - Scans for CDC/non-CDC offers, drives, 'God Bless You' meetings
   - Hunts for shortlists matching Neo PAT ID (V4V7F4Z1), Reg No (23BAI10539), Parth Mishra
2. Personal Career Inbox Monitor (parthmishra9942@gmail.com)
   - LinkedIn application updates & recruiter communications
   - Interview/meeting invites (Google Meet, Zoom, MS Teams, Calendly)
   - Coding assessments & test links (HackerRank, CodeSignal, Mettl)
   - Cross-over communications from campus placement companies
"""

import os
import subprocess
import sys
from pathlib import Path

# Safe terminal encoding on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def run_command(cmd_args: list[str], title: str) -> int:
    print(f"\n{'='*74}")
    print(f"▶ {title}")
    print(f"{'='*74}")
    try:
        res = subprocess.run(cmd_args, capture_output=False, text=True, check=False)
        return res.returncode
    except Exception as exc:
        print(f"[ERROR] Failed to execute {cmd_args}: {exc}")
        return 1


def main():
    repo_root = Path(__file__).resolve().parent.parent
    os.chdir(repo_root)

    print(f"\n==========================================================================")
    print(f"🎯 UNIFIED INBOX MONITOR: PARTH MISHRA")
    print(f"   College Email:  parth.23bai10539@vitbhopal.ac.in (Reg: 23BAI10539 | Neo: V4V7F4Z1)")
    print(f"   Personal Email: parthmishra9942@gmail.com")
    print(f"==========================================================================")

    # 1. College Placement Monitor
    college_script = repo_root / "tools" / "college_placement_inbox_monitor.py"
    if college_script.exists():
        run_command([sys.executable, str(college_script), "--check"], "College Placement & Shortlist Monitor")
    else:
        print(f"[MISSING] {college_script} not found.")

    # 2. Personal Career Inbox Monitor
    personal_script = repo_root / "tools" / "personal_inbox_monitor.py"
    personal_config = repo_root / "personal_email_config.json"
    if personal_script.exists():
        if personal_config.exists():
            run_command([sys.executable, str(personal_script), "--check"], "Personal Career Inbox Monitor")
        else:
            print(f"\n{'='*74}")
            print(f"▶ Personal Career Inbox Monitor (parthmishra9942@gmail.com)")
            print(f"{'='*74}")
            print("Status: Personal monitor ready, awaiting 16-character Google App Password.")
            print("Once provided, `personal_email_config.json` will be initialized to monitor from that exact moment forward.")
    else:
        print(f"[MISSING] {personal_script} not found.")


if __name__ == "__main__":
    main()
