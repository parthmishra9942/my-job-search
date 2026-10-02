#!/usr/bin/env python3
"""College Placement Inbox Monitor, Shortlist Hunter & AI Parser.

Monitors college email (Gmail/Outlook IMAP) to filter through the ~90 daily emails:
1. Identifies placement drives, 'God bless you' hiring updates, CDC & non-CDC offers.
2. Extracts deadlines, registration links, package (CTC), and eligibility cutoffs.
3. Automatically hunts for Shortlists (Online Assessment, Interview, Final Selects):
   - Searches inline email tables and message text.
   - Inspects attached Excel (.xlsx, .xls) and CSV sheets.
   - Fetches and inspects linked Google Sheets.
   - Matches candidate on Neo PAT ID (V4V7F4Z1), Reg No (23BAI10539), and Name (Parth Mishra).
"""

import csv
import email
import email.message
import imaplib
import io
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

try:
    import openpyxl
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# Candidate Profile Defaults (Parth Mishra - VIT Bhopal)
CANDIDATE_NAME = "Parth Mishra"
CANDIDATE_REG_NO = "23BAI10539"
CANDIDATE_NEO_ID = "V4V7F4Z1"
CANDIDATE_CGPA = 8.67
CANDIDATE_BATCH = 2027
CANDIDATE_BRANCH = "CSE (AI/ML)"

# High-priority placement trigger keywords
PLACEMENT_KEYWORDS = [
    r"god\s*bless\s*you",
    r"campus\s*drive",
    r"placement\s*drive",
    r"cdc\s*offer",
    r"non[-\s]*cdc",
    r"restricted\s*offer",
    r"super\s*dream",
    r"dream\s*offer",
    r"marquee\s*offer",
    r"hiring\s*announcement",
    r"registration\s*link",
    r"recruitment\s*process",
    r"shortlist\w*",
    r"interview\s*schedule",
    r"online\s*assessment",
    r"test\s*link",
    r"lineup",
    r"selected\s*students?",
    r"neo\s*pat",
]

SHORTLIST_KEYWORDS = [
    r"shortlist\w*",
    r"selected\s*students?",
    r"shortlisted\s*candidates?",
    r"lineup",
    r"interview\s*list",
    r"assessment\s*shortlist",
    r"oa\s*shortlist",
    r"eligible\s*students?\s*list",
    r"test\s*taker\s*list",
]

# Patterns for extracting key fields
URL_PATTERN = re.compile(
    r"https?://(?:forms\.gle/[a-zA-Z0-9_\-]+|docs\.google\.com/forms/[^\s\"'>]+|forms\.office\.com/[^\s\"'>]+|[a-zA-Z0-9_\-]+\.supersetlabs\.com/[^\s\"'>]+|docs\.google\.com/spreadsheets/[^\s\"'>]+|[^\s\"'>]+)"
)
GOOGLE_SHEET_PATTERN = re.compile(
    r"https?://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9_\-]+)(?:/[^\s\"'>]*)?"
)
CTC_PATTERN = re.compile(
    r"(\b\d+(?:\.\d+)?\s*(?:LPA|Lacs|Lakhs?|CTC|k\/month|per\s*month|per\s*annum)\b)",
    re.IGNORECASE,
)
CGPA_CUTOFF_PATTERN = re.compile(
    r"(?:cgpa|pointer|percentage)\s*(?:cutoff|criterion|requirement|criteria|>=|>|minimum|min)?\s*[:\-]?\s*(\d+(?:\.\d+)?)",
    re.IGNORECASE,
)
DEADLINE_PATTERN = re.compile(
    r"(?:last\s*date\s*(?:to\s*apply)?|deadline|apply\s*before|closes\s*on|registration\s*closes?)\s*[:\-]?\s*([0-9]{1,2}[A-Za-z0-9\s,:\/\.\-]+(?:AM|PM|IST)?)",
    re.IGNORECASE,
)
BATCH_PATTERN = re.compile(r"\b(202[4-9])\b")


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
            result.append(
                fragment.decode(encoding or "utf-8", errors="replace")
            )
        else:
            result.append(str(fragment))
    return "".join(result)


def is_placement_email(subject: str, body: str) -> bool:
    """Determine if email is a relevant placement notification rather than campus spam."""
    combined = f"{subject}\n{body}".lower()
    for kw in PLACEMENT_KEYWORDS:
        if re.search(kw, combined, re.IGNORECASE):
            return True
    return False


def is_shortlist_email(subject: str, body: str) -> bool:
    """Determine if email is specifically announcing a student shortlist or test lineup."""
    combined = f"{subject}\n{body}".lower()
    for kw in SHORTLIST_KEYWORDS:
        if re.search(kw, combined, re.IGNORECASE):
            return True
    return False


def check_candidate_match(text: str) -> tuple[bool, str]:
    """Check if candidate's Neo ID, Reg No, or Name appears in text."""
    lower_text = text.lower()
    if CANDIDATE_NEO_ID.lower() in lower_text:
        return True, f"Neo PAT ID: {CANDIDATE_NEO_ID}"
    if CANDIDATE_REG_NO.lower() in lower_text:
        return True, f"Registration No: {CANDIDATE_REG_NO}"
    if CANDIDATE_NAME.lower() in lower_text:
        return True, f"Name: {CANDIDATE_NAME}"
    return False, ""


def search_excel_bytes(file_bytes: bytes, filename: str) -> tuple[bool, str, str]:
    """Scan in-memory Excel workbook (.xlsx) for candidate identifiers."""
    if not OPENPYXL_AVAILABLE:
        return False, "", "openpyxl not available"
    try:
        wb = openpyxl.load_workbook(io.BytesIO(file_bytes), data_only=True, read_only=True)
        for sheetname in wb.sheetnames:
            sheet = wb[sheetname]
            for row in sheet.iter_rows(values_only=True):
                for cell in row:
                    if cell is not None:
                        cell_str = str(cell).strip()
                        matched, identifier = check_candidate_match(cell_str)
                        if matched:
                            return True, identifier, f"Excel ({filename} -> Sheet: '{sheetname}')"
    except Exception as exc:
        return False, "", f"Error reading Excel {filename}: {exc}"
    return False, "", ""


def search_csv_content(csv_text: str, source_label: str) -> tuple[bool, str, str]:
    """Scan CSV text for candidate identifiers."""
    reader = csv.reader(io.StringIO(csv_text))
    for row in reader:
        for cell in row:
            matched, identifier = check_candidate_match(cell)
            if matched:
                return True, identifier, f"CSV ({source_label})"
    return False, "", ""


def inspect_google_sheet(url: str) -> tuple[bool, str, str]:
    """Attempt to fetch and inspect a public / domain-accessible Google Sheet for shortlisting."""
    if not REQUESTS_AVAILABLE:
        return False, "", "requests library not available"

    match = GOOGLE_SHEET_PATTERN.search(url)
    if not match:
        return False, "", "Not a recognized Google Sheet URL"

    sheet_id = match.group(1)
    gid_match = re.search(r"[#&]gid=([0-9]+)", url)
    gid_param = f"&gid={gid_match.group(1)}" if gid_match else ""
    export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv{gid_param}"

    try:
        resp = requests.get(export_url, timeout=10)
        if resp.status_code == 200 and ("csv" in resp.headers.get("Content-Type", "") or resp.text.count(",") > 5):
            matched, identifier, location = search_csv_content(resp.text, f"Google Sheet: {sheet_id}")
            if matched:
                return True, identifier, location
    except Exception:
        pass

    return False, "", ""


def parse_placement_email(subject: str, sender: str, body: str, date_str: str = "", attachments: list = None) -> dict:
    """Extract structured data and check for candidate shortlisting."""
    attachments = attachments or []

    # Find links
    all_links = URL_PATTERN.findall(body)
    priority_links = [
        l for l in all_links if any(x in l.lower() for x in ["form", "superset", "apply", "register", "survey", "sheet"])
    ]
    primary_link = priority_links[0] if priority_links else (all_links[0] if all_links else "Check email body")

    # Extract CTC
    ctc_matches = CTC_PATTERN.findall(body)
    ctc = ctc_matches[0] if ctc_matches else "Not stated"

    # Extract CGPA Cutoff
    cgpa_match = CGPA_CUTOFF_PATTERN.search(body)
    cgpa_cutoff = float(cgpa_match.group(1)) if cgpa_match else None

    # Check eligibility
    eligible = True
    eligibility_note = "Eligible"
    if cgpa_cutoff:
        if CANDIDATE_CGPA >= cgpa_cutoff:
            eligibility_note = f"Eligible (CGPA {CANDIDATE_CGPA} >= {cgpa_cutoff})"
        else:
            eligible = False
            eligibility_note = f"Ineligible (Cutoff {cgpa_cutoff} > {CANDIDATE_CGPA})"

    # Batch check
    batches = BATCH_PATTERN.findall(body)
    if batches and str(CANDIDATE_BATCH) not in batches and len(batches) <= 2:
        eligibility_note += f" (Note: Mentions batches {', '.join(set(batches))})"

    # Extract Deadline
    deadline_match = DEADLINE_PATTERN.search(body)
    deadline = deadline_match.group(1).strip() if deadline_match else "Check announcement"

    # Classify Drive Type
    drive_type = "Standard Drive"
    is_shortlist = is_shortlist_email(subject, body)
    if is_shortlist:
        drive_type = "Shortlist Announcement / Candidate Lineup"
    elif re.search(r"non[-\s]*cdc", f"{subject} {body}", re.IGNORECASE):
        drive_type = "Non-CDC / Off-Campus Offer"
    elif re.search(r"restricted", f"{subject} {body}", re.IGNORECASE):
        drive_type = "Restricted Offer"
    elif re.search(r"super\s*dream", f"{subject} {body}", re.IGNORECASE):
        drive_type = "Super Dream (>= 10 LPA)"
    elif re.search(r"dream", f"{subject} {body}", re.IGNORECASE):
        drive_type = "Dream (>= 5-9 LPA)"
    elif re.search(r"god\s*bless\s*you", f"{subject} {body}", re.IGNORECASE):
        drive_type = "Placement Cell Mass Drive ('God Bless You')"

    # Extract likely company name from subject or top of body
    company_name = "Placement Announcement"
    subject_cleaned = re.sub(
        r"(?i)(fwd:|re:|announcement|placement|drive|vit|bhopal|may god bless you|urgent|notice|shortlist(ed)?|candidates?|lineup)",
        "",
        subject,
    )
    subject_cleaned = clean_text(subject_cleaned)
    if subject_cleaned:
        tokens = [t for t in subject_cleaned.split() if len(t) > 2 and t.lower() not in ["for", "the", "with", "batch", "round", "technical", "interview"]]
        if tokens:
            company_name = " ".join(tokens[:4])

    # ========================================================
    # Shortlist Matching Engine
    # ========================================================
    is_candidate_shortlisted = False
    shortlist_evidence = ""

    # 1. Search email body / inline tables
    matched_inline, ident = check_candidate_match(body)
    if matched_inline:
        is_candidate_shortlisted = True
        shortlist_evidence = f"Inline Email Body / Table ({ident})"

    # 2. Search attached files (Excel / CSV)
    if not is_candidate_shortlisted and attachments:
        for att_name, att_bytes in attachments:
            if att_name.lower().endswith((".xlsx", ".xls")):
                matched_xl, ident, loc = search_excel_bytes(att_bytes, att_name)
                if matched_xl:
                    is_candidate_shortlisted = True
                    shortlist_evidence = f"{loc} ({ident})"
                    break
            elif att_name.lower().endswith(".csv"):
                try:
                    csv_str = att_bytes.decode("utf-8", errors="replace")
                    matched_csv, ident, loc = search_csv_content(csv_str, att_name)
                    if matched_csv:
                        is_candidate_shortlisted = True
                        shortlist_evidence = f"{loc} ({ident})"
                        break
                except Exception:
                    pass

    # 3. Search Google Sheet links
    if not is_candidate_shortlisted:
        for link in all_links:
            if "docs.google.com/spreadsheets" in link:
                matched_gs, ident, loc = inspect_google_sheet(link)
                if matched_gs:
                    is_candidate_shortlisted = True
                    shortlist_evidence = f"{loc} ({ident})"
                    break

    return {
        "subject": subject,
        "sender": sender,
        "date": date_str or datetime.now().strftime("%Y-%m-%d %H:%M"),
        "company": company_name,
        "drive_type": drive_type,
        "is_shortlist_announcement": is_shortlist,
        "is_candidate_shortlisted": is_candidate_shortlisted,
        "shortlist_evidence": shortlist_evidence,
        "ctc": ctc,
        "cgpa_cutoff": cgpa_cutoff,
        "eligible": eligible,
        "eligibility_note": eligibility_note,
        "deadline": deadline,
        "registration_link": primary_link,
    }


def format_notification(parsed: dict) -> str:
    """Format structured email into a high-visibility terminal alert."""
    if parsed["is_candidate_shortlisted"]:
        return (
            f"\n{'#'*74}\n"
            f"🎉🎉🎉 [SHORTLISTED!] PARTH MISHRA IS SHORTLISTED FOR {parsed['company'].upper()}! 🎉🎉🎉\n"
            f"{'#'*74}\n"
            f"• Candidate:        Parth Mishra | Reg: {CANDIDATE_REG_NO} | Neo ID: {CANDIDATE_NEO_ID}\n"
            f"• Found In:         {parsed['shortlist_evidence']}\n"
            f"• Drive / Subject:  {parsed['subject']}\n"
            f"• Links / Info:     {parsed['registration_link']}\n"
            f"• Action Required:  Check next round schedule (Assessment / Technical Interview)!\n"
            f"{'#'*74}\n"
        )

    status_icon = "[ELIGIBLE]" if parsed["eligible"] else "[INELIGIBLE]"
    return (
        f"\n{'='*70}\n"
        f"*** {status_icon} CAMPUS PLACEMENT ALERT: {parsed['company']} ***\n"
        f"{'='*70}\n"
        f"• Drive Type:       {parsed['drive_type']}\n"
        f"• Package (CTC):    {parsed['ctc']}\n"
        f"• Eligibility:      {parsed['eligibility_note']}\n"
        f"• Deadline:         {parsed['deadline']}\n"
        f"• Apply / Register: {parsed['registration_link']}\n"
        f"• Email Subject:    {parsed['subject']}\n"
        f"{'='*70}\n"
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


def extract_attachments_from_msg(msg: email.message.Message) -> list[tuple[str, bytes]]:
    """Extract file attachments from email message."""
    attachments = []
    if msg.is_multipart():
        for part in msg.walk():
            content_disposition = str(part.get("Content-Disposition"))
            filename = part.get_filename()
            if filename and ("attachment" in content_disposition or "inline" in content_disposition):
                filename = decode_mime_header(filename)
                payload = part.get_payload(decode=True)
                if payload:
                    attachments.append((filename, payload))
    return attachments


def check_live_inbox(config: dict, limit: int = 40, mark_seen: bool = False):
    """Connect to college IMAP server and filter through recent emails with 2-stage fast scanning."""
    host = config.get("imap_server", "imap.gmail.com")
    port = config.get("imap_port", 993)
    user = config.get("email")
    password = config.get("password")

    if not user or not password:
        print("[ERROR] Email or password not configured.", flush=True)
        print("Run `python tools/college_placement_inbox_monitor.py --setup` to configure your credentials.", flush=True)
        return []

    print(f"Connecting securely to {host} for {user}...", flush=True)
    try:
        mail = imaplib.IMAP4_SSL(host, port, timeout=20)
        mail.login(user, password)
    except Exception as exc:
        print(f"[AUTH ERROR] Could not log in to {host}: {exc}", flush=True)
        print("\nTip for Google Workspace (Gmail):", flush=True)
        print("1. Enable 2-Step Verification in your Google Account.", flush=True)
        print("2. Generate a 16-character App Password at: https://myaccount.google.com/apppasswords", flush=True)
        print("3. Use the App Password instead of your college portal password.", flush=True)
        return []

    folder = config.get("folder", "INBOX")
    mail.select(folder, readonly=True)

    state_file = Path("college_email_state.json")
    last_seen_uid = 0
    if state_file.exists():
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                st = json.load(f)
                last_seen_uid = int(st.get("last_seen_uid", 0))
        except Exception:
            pass

    # If no checkpoint exists, initialize checkpoint to current highest UID
    if last_seen_uid == 0:
        status, data = mail.uid("search", None, "ALL")
        uids = [int(u) for u in data[0].split()] if data and data[0] else []
        last_seen_uid = max(uids) if uids else 0
        state = {
            "checkpoint_time": datetime.now().isoformat(),
            "last_seen_uid": last_seen_uid,
            "description": "Baseline checkpoint set. All prior emails ignored.",
        }
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        print(f"Baseline checkpoint set at UID {last_seen_uid}. Previous emails ignored. Monitoring from now forward!", flush=True)
        mail.close()
        mail.logout()
        return []

    # Search strictly for NEW emails with UID > last_seen_uid
    status, data = mail.uid("search", None, f"UID {last_seen_uid + 1}:*")
    raw_uids = [int(u) for u in data[0].split()] if data and data[0] else []
    new_uids = sorted([u for u in raw_uids if u > last_seen_uid])

    if not new_uids:
        print(f"[INBOX UP TO DATE] No new emails received since checkpoint (UID {last_seen_uid}). All prior emails skipped.", flush=True)
        mail.close()
        mail.logout()
        return []

    print(f"Detected {len(new_uids)} NEW email(s) since last check (UIDs: {min(new_uids)} - {max(new_uids)}). Scanning...", flush=True)

    found_drives = []
    history_file = Path("college_placement_history.json")

    # Pass 1: Quick Header Pre-filter on new UIDs
    placement_candidates = []
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

        is_sender_placement = any(x in sender.lower() for x in ["placement", "cdc", "pat", "vitlions", "carrier", "careers"])
        if is_sender_placement or is_placement_email(subj, "") or is_shortlist_email(subj, ""):
            placement_candidates.append((uid, subj, sender, raw_date))

    if not placement_candidates:
        print(f"Checked {len(new_uids)} new email(s): None were placement notices (campus noise filtered out).", flush=True)
    else:
        print(f"Found {len(placement_candidates)} new placement/career notice(s)! Inspecting details and attachments...", flush=True)
        for uid, subj, sender, date_str in placement_candidates:
            status, data = mail.uid("fetch", str(uid), "(BODY.PEEK[])")
            if status != "OK" or not data:
                continue

            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            body = extract_body_from_msg(msg)
            attachments = extract_attachments_from_msg(msg)

            parsed = parse_placement_email(subj, sender, body, date_str, attachments)
            print(format_notification(parsed), flush=True)
            found_drives.append(parsed)

    # Advance checkpoint to highest seen UID
    new_max_uid = max(new_uids)
    state = {
        "checkpoint_time": datetime.now().isoformat(),
        "last_seen_uid": new_max_uid,
        "description": "Updated checkpoint after scanning new emails.",
    }
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    mail.close()
    mail.logout()

    if found_drives:
        print(f"\nProcessed and saved {len(found_drives)} new placement notice(s)!")
    return found_drives


def test_mock_email():
    """Run parser on a simulated VIT Bhopal placement email."""
    sample_subject = "May God Bless You: Campus Drive by Cisco Systems for 2027 Batch"
    sample_sender = "placement@vitbhopal.ac.in"
    sample_body = """
    Dear Students,
    May God Bless You.
    
    We are pleased to announce that Cisco Systems is visiting our campus for the 2027 Graduating Batch
    for the role of Software Engineer I (CDC Drive).
    
    Eligibility Criteria:
    - B.Tech (CSE / AIML / ECE)
    - CGPA Cutoff: 8.00 and above (No active standing arrears)
    - Batch: 2027
    
    Package Details:
    - CTC: 15.0 LPA (Fixed + Stocks)
    - Internship Stipend: 75,000 per month
    
    Deadline for Registration:
    - Last date to apply: 02 October 2026, 11:59 PM IST (Strict deadline)
    
    Registration Form Link:
    https://forms.gle/xYz987CiscoVITBhopal2027
    
    Best Regards,
    Placement & Training Cell
    VIT Bhopal University
    """
    parsed = parse_placement_email(sample_subject, sample_sender, sample_body)
    print(format_notification(parsed))


def test_mock_shortlist():
    """Demonstrate shortlist matching on Neo ID V4V7F4Z1 and Reg No 23BAI10539."""
    print("\n--- Testing Shortlist Detection: Attached Excel Sheet ---")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Shortlisted_Candidates"
    ws.append(["S.No", "Neo PAT ID", "Registration No", "Student Name", "Branch", "Status"])
    ws.append([1, "V8N2K1A4", "23BCE10101", "Aarav Sharma", "CSE", "Shortlisted for Interview"])
    ws.append([2, "V4V7F4Z1", "23BAI10539", "Parth Mishra", "CSE (AI/ML)", "Shortlisted for Interview"])
    ws.append([3, "V1P9L5X2", "23BME10342", "Rohan Verma", "ME", "Shortlisted for Interview"])
    
    buf = io.BytesIO()
    wb.save(buf)
    excel_bytes = buf.getvalue()

    sample_subject = "Urgent: Oracle Cloud SDE Drive - Shortlisted Candidates for Technical Interview Round 1"
    sample_sender = "placement.drive@vitbhopal.ac.in"
    sample_body = """
    Dear Students,
    
    Please find attached the list of students shortlisted for the Round 1 Technical Interview
    for Oracle Cloud SDE Drive.
    
    Interviews are scheduled for tomorrow from 10:00 AM onwards.
    Check the attached Excel file for your interview time slot and meeting link.
    
    Regards,
    Neo PAT Cell, VIT Bhopal
    """
    parsed = parse_placement_email(
        sample_subject, sample_sender, sample_body, attachments=[("Oracle_SDE_Shortlist.xlsx", excel_bytes)]
    )
    print(format_notification(parsed))


def run_setup():
    """Interactive wizard to configure college email credentials safely."""
    config_file = Path("college_email_config.json")
    print("\n--- College Email Monitoring Setup ---")
    email_addr = input("Enter your college email (e.g. parth.mishra2023@vitbhopal.ac.in): ").strip()
    print("\nPassword Note: For Google Workspace / Gmail, do NOT enter your portal password.")
    print("Use a 16-character Google App Password (https://myaccount.google.com/apppasswords)")
    password = input("Enter App Password: ").strip()
    imap_server = input("IMAP Server [default: imap.gmail.com]: ").strip() or "imap.gmail.com"

    config = {
        "email": email_addr,
        "password": password,
        "imap_server": imap_server,
        "imap_port": 993,
        "folder": "INBOX",
        "search_query": "UNSEEN",
    }
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    print(f"\nConfiguration saved to {config_file.resolve()}")
    print("Run `python tools/college_placement_inbox_monitor.py --check` to scan your inbox.")


if __name__ == "__main__":
    config_file = Path("college_email_config.json")
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Running mock placement drive test...")
        test_mock_email()
    elif len(sys.argv) > 1 and sys.argv[1] == "--test-shortlist":
        print("Running mock shortlist detection test...")
        test_mock_shortlist()
    elif len(sys.argv) > 1 and sys.argv[1] == "--reset-checkpoint":
        state_file = Path("college_email_state.json")
        if state_file.exists():
            state_file.unlink()
        print("Checkpoint reset. Run --check to initialize baseline to this exact moment.", flush=True)
    elif len(sys.argv) > 1 and sys.argv[1] == "--setup":
        run_setup()
    elif len(sys.argv) > 1 and sys.argv[1] == "--check":
        if not config_file.exists():
            print("Configuration file not found.")
            run_setup()
        else:
            with open(config_file, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            check_live_inbox(cfg)
    else:
        print("College Placement Inbox Monitor & Shortlist Hunter.")
        print("Options:")
        print("  python tools/college_placement_inbox_monitor.py --test               # Test on simulated drive email")
        print("  python tools/college_placement_inbox_monitor.py --test-shortlist     # Test shortlist detection in Excel/Sheets")
        print("  python tools/college_placement_inbox_monitor.py --setup              # Configure college email & App Password")
        print("  python tools/college_placement_inbox_monitor.py --check              # Scan ONLY new incoming emails from now forward")
        print("  python tools/college_placement_inbox_monitor.py --reset-checkpoint   # Reset baseline checkpoint to current moment")
