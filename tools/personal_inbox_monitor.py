#!/usr/bin/env python3
"""Personal Email Application & Meeting Monitor.

Monitors personal Gmail (parthmishra9942@gmail.com) for:
1. LinkedIn Application updates, recruiter messages, and invitations.
2. Interview and Meeting Invites (Google Meet, Zoom, MS Teams, Calendly).
3. Online Assessments and Coding Challenges (HackerRank, CodeSignal, Mettl, TestGorilla).
4. Cross-over messages from College Placement Companies (e.g., Deloitte, InboxKit/Enrich Labs,
   Axxela, Micro Green, Cisco) asking to fill Google Forms, confirm attendance, or submit details.
5. Selection and Offer letters.
"""

import email
import email.message
import imaplib
import json
import os
import re
import sys
from datetime import datetime
from email.header import decode_header
from pathlib import Path

# Safe terminal encoding on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CANDIDATE_NAME = "Parth Mishra"
PERSONAL_EMAIL_DEFAULT = "parthmishra9942@gmail.com"

# Signal detection patterns
MEETING_URL_PATTERN = re.compile(
    r"https?://(?:meet\.google\.com/[a-zA-Z0-9_\-]+|zoom\.us/j/[0-9]+[^\s\"'>]*|teams\.microsoft\.com/[^\s\"'>]+|calendly\.com/[^\s\"'>]+)",
    re.IGNORECASE,
)
ASSESSMENT_URL_PATTERN = re.compile(
    r"https?://(?:[a-zA-Z0-9_\-]+\.hackerrank\.com/[^\s\"'>]+|app\.codesignal\.com/[^\s\"'>]+|tests\.mettl\.com/[^\s\"'>]+|app\.testgorilla\.com/[^\s\"'>]+|app\.glider\.ai/[^\s\"'>]+|app\.codility\.com/[^\s\"'>]+)",
    re.IGNORECASE,
)
FORM_URL_PATTERN = re.compile(
    r"https?://(?:forms\.gle/[a-zA-Z0-9_\-]+|docs\.google\.com/forms/[^\s\"'>]+|forms\.office\.com/[^\s\"'>]+)",
    re.IGNORECASE,
)
ALL_URL_PATTERN = re.compile(r"https?://[^\s\"'>]+")

INTERVIEW_KEYWORDS = [
    r"interview\s*invit\w*",
    r"schedule\s*a\s*call",
    r"phone\s*screen",
    r"technical\s*interview",
    r"technical\s*round",
    r"next\s*round",
    r"invitation:\s*",
    r"discuss\s*your\s*application",
    r"video\s*call",
    r"hiring\s*manager\s*round",
]

ASSESSMENT_KEYWORDS = [
    r"online\s*assessment",
    r"coding\s*challenge",
    r"technical\s*assessment",
    r"complete\s*your\s*test",
    r"hackerrank",
    r"codesignal",
    r"mettl",
    r"testgorilla",
    r"test\s*link",
]

ACTION_FORM_KEYWORDS = [
    r"action\s*required",
    r"fill\s*(?:out|in)?\s*(?:the|this)?\s*form",
    r"submit\s*your\s*details",
    r"candidate\s*information\s*form",
    r"background\s*check",
    r"confirm\s*your\s*attendance",
    r"document\s*submission",
    r"registration\s*details",
]

OFFER_KEYWORDS = [
    r"pleased\s*to\s*offer",
    r"extend\s*an\s*offer",
    r"offer\s*letter",
    r"congratulations.*selected",
]


def clean_text(raw_str: str) -> str:
    """Normalize whitespace and strip HTML remnants."""
    text = re.sub(r"<[^>]+>", " ", raw_str)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def decode_mime_header(header_value: str) -> str:
    """Safely decode MIME encoded email headers."""
    if not header_value:
        return ""
    decoded_fragments = decode_header(header_value)
    result = []
    for fragment, encoding in decoded_fragments:
        if isinstance(fragment, bytes):
            result.append(fragment.decode(encoding or "utf-8", errors="replace"))
        else:
            result.append(str(fragment))
    return "".join(result)


def load_tracked_companies() -> list[str]:
    """Load list of known companies from tracker and college history for cross-referencing."""
    companies = set()
    tracker_file = Path("job_search_tracker.csv")
    if tracker_file.exists():
        try:
            with open(tracker_file, "r", encoding="latin-1") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) > 1 and parts[1] and parts[1] != "company":
                        c = parts[1].strip()
                        if len(c) > 2:
                            companies.add(c)
        except Exception:
            pass

    college_history_file = Path("college_placement_history.json")
    if college_history_file.exists():
        try:
            with open(college_history_file, "r", encoding="utf-8") as f:
                drives = json.load(f)
                for d in drives:
                    c = d.get("company", "")
                    if c and len(c) > 2 and "Announcement" not in c and "Meeting" not in c:
                        companies.add(c)
        except Exception:
            pass

    # Known campus recruiters & targeted applications
    extra_known = [
        "Enrich Labs", "InboxKit", "Deloitte", "Axxela", "Micro Green", "Shell",
        "Cisco", "Euler Motors", "Epsilon", "Unthinkable", "Chubb", "RFPIO",
        "Responsive", "Goldman Sachs", "American Express", "Unilever", "Infosys",
        "Honeywell", "BlackRock", "Amazon", "PAR Technology", "Gowitek", "AssetMark",
        "Droisys", "PIXIE", "Opticent", "404Minds", "Recruit CRM", "Zepto", "UBS"
    ]
    for k in extra_known:
        companies.add(k)

    return sorted(list(companies), key=lambda x: -len(x))


def is_job_related_email(subject: str, sender: str, body: str) -> bool:
    """Detect if an incoming email is related to job applications, interviews, tests, or recruiters."""
    combined = f"{subject}\n{sender}\n{body}".lower()
    
    # Check ATS domains
    ats_domains = [
        "linkedin.com", "greenhouse.io", "lever.co", "myworkday.com",
        "ashbyhq.com", "smartrecruiters.com", "icims.com", "bamboohr.com",
        "mettl.com", "hackerrank.com", "codesignal.com", "calendly.com", "zoom.us",
        "unstop.com", "indeed.com", "naukri.com"
    ]
    if any(d in sender.lower() for d in ats_domains):
        return True

    # Check signal keywords
    all_kws = INTERVIEW_KEYWORDS + ASSESSMENT_KEYWORDS + ACTION_FORM_KEYWORDS + OFFER_KEYWORDS
    for kw in all_kws:
        if re.search(kw, combined, re.IGNORECASE):
            return True

    return False


def classify_personal_email(subject: str, sender: str, body: str, date_str: str = "") -> dict:
    """Classify email type, match company, detect meeting links, test keys, and action items."""
    combined = f"{subject}\n{body}".lower()
    tracked_companies = load_tracked_companies()

    # Detect Company Name
    matched_company = "External Organization / Recruiter"
    is_college_crossover = False

    for c in tracked_companies:
        if c.lower() in combined or c.lower() in sender.lower():
            matched_company = c
            is_college_crossover = True
            break

    if not is_college_crossover:
        # Try to infer company from sender display name
        sender_match = re.search(r"([^<@]+)<", sender)
        if sender_match:
            cand = clean_text(sender_match.group(1))
            if cand and not any(x in cand.lower() for x in ["notification", "noreply", "no-reply", "alert", "invitation"]):
                matched_company = cand

    # Detect Signal Type
    signal_type = "Application Update"
    priority_level = "NORMAL"
    action_required = False
    action_note = ""

    # Check Offers
    if any(re.search(kw, combined, re.IGNORECASE) for kw in OFFER_KEYWORDS):
        signal_type = "🎉 JOB OFFER / FINAL SELECTION"
        priority_level = "CRITICAL - HIGHEST"
        action_required = True
        action_note = "Review offer letter & terms!"

    # Check Meeting / Interview
    elif any(re.search(kw, combined, re.IGNORECASE) for kw in INTERVIEW_KEYWORDS) or MEETING_URL_PATTERN.search(body):
        signal_type = "📅 INTERVIEW / MEETING INVITATION"
        priority_level = "CRITICAL - URGENT"
        action_required = True
        action_note = "Confirm interview slot & prepare!"

    # Check Online Assessment
    elif any(re.search(kw, combined, re.IGNORECASE) for kw in ASSESSMENT_KEYWORDS) or ASSESSMENT_URL_PATTERN.search(body):
        signal_type = "💻 ONLINE ASSESSMENT / CODING TEST"
        priority_level = "HIGH PRIORITY"
        action_required = True
        action_note = "Complete test before deadline expires!"

    # Check Action Form to fill
    elif any(re.search(kw, combined, re.IGNORECASE) for kw in ACTION_FORM_KEYWORDS) or FORM_URL_PATTERN.search(body):
        signal_type = "📝 ACTION REQUIRED: FORM TO FILL"
        priority_level = "HIGH PRIORITY"
        action_required = True
        action_note = "Fill out candidate information / confirmation form!"

    # Check LinkedIn signals
    elif "linkedin" in sender.lower() or "linkedin" in subject.lower():
        signal_type = "💼 LINKEDIN APPLICATION UPDATE"
        priority_level = "NORMAL"

    # Extract Links
    meeting_links = MEETING_URL_PATTERN.findall(body)
    assessment_links = ASSESSMENT_URL_PATTERN.findall(body)
    form_links = FORM_URL_PATTERN.findall(body)
    all_links = ALL_URL_PATTERN.findall(body)

    primary_link = "Check email body"
    if meeting_links:
        primary_link = meeting_links[0]
    elif assessment_links:
        primary_link = assessment_links[0]
    elif form_links:
        primary_link = form_links[0]
    elif all_links:
        priority_candidates = [l for l in all_links if any(x in l.lower() for x in ["apply", "job", "career", "interview", "schedule", "mettl", "form"])]
        primary_link = priority_candidates[0] if priority_candidates else all_links[0]

    return {
        "subject": subject,
        "sender": sender,
        "date": date_str or datetime.now().strftime("%Y-%m-%d %H:%M"),
        "company": matched_company,
        "signal_type": signal_type,
        "priority_level": priority_level,
        "is_college_crossover": is_college_crossover,
        "action_required": action_required,
        "action_note": action_note,
        "primary_link": primary_link,
        "body_preview": clean_text(body)[:250],
    }


def format_personal_notification(parsed: dict) -> str:
    """Format structured email into a prominent terminal alert."""
    crossover_banner = ""
    if parsed["is_college_crossover"]:
        crossover_banner = f"🔗 [CAMPUS PLACEMENT CROSS-OVER] Sent to Personal Mail by: {parsed['company']}\n"

    return (
        f"\n{'*'*74}\n"
        f"🚨 [{parsed['priority_level']}] {parsed['signal_type']}\n"
        f"Company / Sender:   {parsed['company']}\n"
        f"{crossover_banner}"
        f"Subject:            {parsed['subject']}\n"
        f"Action Note:        {parsed['action_note'] if parsed['action_note'] else 'Review message'}\n"
        f"Link / Meeting:     {parsed['primary_link']}\n"
        f"Received:           {parsed['date']}\n"
        f"{'*'*74}\n"
    )


def extract_body_from_msg(msg: email.message.Message) -> str:
    """Extract plain text or cleaned HTML body from an email Message object."""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                payload = part.get_payload(decode=True)
                if payload:
                    body += payload.decode("utf-8", errors="replace") + "\n"
            elif content_type == "text/html" and "attachment" not in content_disposition and not body:
                payload = part.get_payload(decode=True)
                if payload:
                    body += clean_text(payload.decode("utf-8", errors="replace")) + "\n"
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            raw = payload.decode("utf-8", errors="replace")
            body = clean_text(raw) if "<html" in raw.lower() else raw
    return body.strip()


def check_live_personal_inbox(config: dict):
    """Connect to personal Gmail over IMAP and check for new application messages from baseline."""
    host = config.get("imap_server", "imap.gmail.com")
    port = config.get("imap_port", 993)
    user = config.get("email", PERSONAL_EMAIL_DEFAULT)
    password = config.get("password")

    if not user or not password or "YOUR_16" in password:
        print("[ERROR] Personal email password not configured.", flush=True)
        print("Run `python tools/personal_inbox_monitor.py --setup` to configure your App Password.", flush=True)
        return []

    print(f"Connecting securely to personal Gmail for {user}...", flush=True)
    try:
        mail = imaplib.IMAP4_SSL(host, port, timeout=20)
        mail.login(user, password)
    except Exception as exc:
        print(f"[AUTH ERROR] Could not log in to {host} for {user}: {exc}", flush=True)
        print("\nTip for Google Account (Gmail):", flush=True)
        print("1. Enable 2-Step Verification in your personal Google Account.")
        print("2. Generate a 16-character App Password at: https://myaccount.google.com/apppasswords")
        print("3. Use the App Password instead of your regular password.", flush=True)
        return []

    folder = config.get("folder", "INBOX")
    mail.select(folder, readonly=True)

    state_file = Path("personal_email_state.json")
    last_seen_uid = 0
    if state_file.exists():
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                st = json.load(f)
                last_seen_uid = int(st.get("last_seen_uid", 0))
        except Exception:
            pass

    # If no checkpoint exists, initialize baseline checkpoint to current highest UID
    if last_seen_uid == 0:
        status, data = mail.uid("search", None, "ALL")
        uids = [int(u) for u in data[0].split()] if data and data[0] else []
        last_seen_uid = max(uids) if uids else 0
        state = {
            "checkpoint_time": datetime.now().isoformat(),
            "last_seen_uid": last_seen_uid,
            "description": "Baseline checkpoint set. All prior personal emails ignored.",
        }
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        print(f"Personal baseline checkpoint set at UID {last_seen_uid}. Previous emails ignored. Monitoring from now forward!", flush=True)
        mail.close()
        mail.logout()
        return []

    # Search strictly for NEW emails with UID > last_seen_uid
    status, data = mail.uid("search", None, f"UID {last_seen_uid + 1}:*")
    raw_uids = [int(u) for u in data[0].split()] if data and data[0] else []
    new_uids = sorted([u for u in raw_uids if u > last_seen_uid])

    if not new_uids:
        print(f"[PERSONAL INBOX UP TO DATE] No new emails received since checkpoint (UID {last_seen_uid}). All prior emails skipped.", flush=True)
        mail.close()
        mail.logout()
        return []

    print(f"Detected {len(new_uids)} NEW email(s) in personal inbox (UIDs: {min(new_uids)} - {max(new_uids)}). Scanning...", flush=True)

    found_notifications = []
    history_file = Path("personal_application_history.json")

    # Pass 1: Quick Header Pre-filter
    candidates = []
    for uid in new_uids:
        status, data = mail.uid("fetch", str(uid), "(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE)])")
        if status != "OK" or not data:
            continue
        header_text = data[0][1].decode("utf-8", errors="replace")
        subj_match = re.search(r"Subject:\s*(.*)", header_text, re.IGNORECASE)
        from_match = re.search(r"From:\s*(.*)", header_text, re.IGNORECASE)
        date_match = re.search(r"Date:\s*(.*)", header_text, re.IGNORECASE)

        raw_subj = subj_match.group(1).strip() if subj_match else ""
        raw_sender = from_match.group(1).strip() if from_match else ""
        raw_date = date_match.group(1).strip() if date_match else ""

        subj = decode_mime_header(raw_subj)
        sender = decode_mime_header(raw_sender)

        if is_job_related_email(subj, sender, ""):
            candidates.append((uid, subj, sender, raw_date))

    if not candidates:
        print(f"Checked {len(new_uids)} new email(s): None were job/recruiter related (personal noise filtered out).", flush=True)
    else:
        print(f"Found {len(candidates)} application/career message(s)! Inspecting details...", flush=True)
        for uid, subj, sender, date_str in candidates:
            status, data = mail.uid("fetch", str(uid), "(BODY.PEEK[])")
            if status != "OK" or not data:
                continue

            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            body = extract_body_from_msg(msg)

            parsed = classify_personal_email(subj, sender, body, date_str)
            print(format_personal_notification(parsed), flush=True)
            found_notifications.append(parsed)

    # Advance checkpoint to highest seen UID
    new_max_uid = max(new_uids)
    state = {
        "checkpoint_time": datetime.now().isoformat(),
        "last_seen_uid": new_max_uid,
        "description": "Updated personal checkpoint after scanning new emails.",
    }
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    mail.close()
    mail.logout()

    if found_notifications:
        print(f"\nProcessed and saved {len(found_notifications)} job update(s)!")
    return found_notifications


def test_mock_personal():
    """Test classification on simulated personal job emails."""
    print("\n--- Test 1: Interview Invitation (Google Meet / Calendly) ---")
    p1 = classify_personal_email(
        subject="Interview Invitation: Software Engineer at Enrich Labs",
        sender="Hiring Team <careers@enrichlabs.com>",
        body="Hi Parth, We were impressed with your background. We would like to schedule a 45-minute technical interview. Please pick a slot here: https://calendly.com/enrich-labs/tech-round-parth",
    )
    print(format_personal_notification(p1))

    print("\n--- Test 2: College Placement Cross-over Form Request ---")
    p2 = classify_personal_email(
        subject="Urgent: Deloitte India Candidate Registration Form",
        sender="Campus Recruitment <deloitte.campus@deloitte.com>",
        body="Dear Parth Mishra, As part of the campus placement drive at VIT Bhopal, please fill out this mandatory candidate details form before 5 PM: https://forms.gle/DeloitteCandidateDetails2027",
    )
    print(format_personal_notification(p2))

    print("\n--- Test 3: Online Coding Assessment ---")
    p3 = classify_personal_email(
        subject="HackerRank Coding Challenge: PIXIE Full Stack Engineer",
        sender="PIXIE Talent <talent@pixie.ai>",
        body="Hello Parth, Please complete your online technical assessment within 48 hours. Assessment link: https://www.hackerrank.com/tests/pixie-fullstack-2026",
    )
    print(format_personal_notification(p3))


def run_setup():
    """Interactive wizard to configure personal email credentials safely."""
    config_file = Path("personal_email_config.json")
    print("\n--- Personal Email Monitoring Setup ---")
    email_addr = input(f"Enter your personal email [default: {PERSONAL_EMAIL_DEFAULT}]: ").strip() or PERSONAL_EMAIL_DEFAULT
    print("\nPassword Note: For Gmail, do NOT enter your Google account password.")
    print("Use a 16-character Google App Password (https://myaccount.google.com/apppasswords)")
    password = input("Enter 16-character App Password: ").strip()

    config = {
        "email": email_addr,
        "password": password.replace(" ", ""),
        "imap_server": "imap.gmail.com",
        "imap_port": 993,
        "folder": "INBOX",
    }
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    print(f"\nConfiguration saved to {config_file.resolve()}")
    print("Run `python tools/personal_inbox_monitor.py --init-checkpoint` to set your baseline.")


if __name__ == "__main__":
    config_file = Path("personal_email_config.json")
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_mock_personal()
    elif len(sys.argv) > 1 and sys.argv[1] == "--init-checkpoint":
        if not config_file.exists():
            print("Configuration file not found. Run --setup first.")
        else:
            state_file = Path("personal_email_state.json")
            if state_file.exists():
                state_file.unlink()
            with open(config_file, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            check_live_personal_inbox(cfg)
    elif len(sys.argv) > 1 and sys.argv[1] == "--setup":
        run_setup()
    elif len(sys.argv) > 1 and sys.argv[1] == "--check":
        if not config_file.exists():
            print("Configuration file not found. Run --setup first.")
        else:
            with open(config_file, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            check_live_personal_inbox(cfg)
    else:
        print("Personal Email Application & Meeting Monitor.")
        print("Options:")
        print("  python tools/personal_inbox_monitor.py --test              # Test on simulated interview/assessment emails")
        print("  python tools/personal_inbox_monitor.py --setup             # Configure personal Gmail & App Password")
        print("  python tools/personal_inbox_monitor.py --init-checkpoint   # Set baseline to ignore past personal emails")
        print("  python tools/personal_inbox_monitor.py --check             # Check new incoming emails from baseline forward")
