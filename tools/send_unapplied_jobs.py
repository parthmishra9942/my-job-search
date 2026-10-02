import os
import sys
import json
import smtplib
import imaplib
import re
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CONFIG_FILE = "personal_email_config.json"
RESUME_PATH = r"C:\Users\parth\Downloads\Parth_Mishra_Resume.pdf"

CANDIDATE_APPLICATIONS = [
    {
        "id": "hackelite",
        "company": "HackElite",
        "role": "AI Engineer Intern (Noida)",
        "to": "careers@hack-elite.com",
        "cc": [],
        "subject": "Application for AI Engineer Intern – Parth Mishra | Oracle Certified Agentic AI | RAG & FastAPIs",
        "body": """Dear Hiring Team at HackElite,

I am writing to apply for the AI Engineer Intern position at HackElite in Noida. As a B.Tech Computer Science (AI/ML) candidate at VIT Bhopal (CGPA: 8.67) and an Oracle Certified Foundations Associate in Agentic AI, my technical focus aligns precisely with your work on LLMs, RAG pipelines, and AI Agents.

Key highlights of my technical background:
• Agentic & RAG Architectures: Built "DocuChat" (multimodal enterprise document Q&A engine with Milvus vector search) and "PulseAI" (diagnostic triage agent using dynamic context window management, FAISS vector embeddings, and LangChain routing).
• High-Performance APIs: Proficient in building modular, low-latency REST APIs using Python and FastAPI with strict Pydantic data schemas.
• Vector Databases & Embeddings: Hands-on experience optimizing semantic similarity searches, hybrid retrieval strategies, and chunking configurations.
• Problem Solving: Solved 250+ algorithmic problems across LeetCode demonstrating clean coding practices and strong algorithmic logic.

I am eager to contribute directly to HackElite's production AI solutions and am available to work onsite in Noida.

Please find attached my executive resume. You can explore my live demos and project repositories below:
• Portfolio: https://ai-portfolio-beige-xi.vercel.app/
• GitHub: https://github.com/parthmishra9942
• LeetCode: https://leetcode.com/u/parth213g

Thank you for your time and consideration. I look forward to speaking with your engineering team.

Best regards,

Parth Mishra
Phone: +91-7985982208
Email: parthmishra9942@gmail.com
VIT Bhopal University
"""
    },
    {
        "id": "greenpoint",
        "company": "Greenpoint Global",
        "role": "Software Developer Intern (Navi Mumbai)",
        "to": "Shruti.Mhatre@greenpointglobal.com",
        "cc": [],
        "subject": "Application for Software Developer Intern – Parth Mishra | B.Tech CSE (AI/ML) | Python & Systems",
        "body": """Dear Shruti,

I hope you are having a great day.

I am writing to express my interest in the Software Developer Intern role at Greenpoint Global in Belapur, Navi Mumbai. I am a B.Tech Computer Science (AI/ML) student at VIT Bhopal University (CGPA: 8.67) with strong foundations in software development, databases, version control, and modern AI productivity workflows.

Why I would be a great fit for Greenpoint Global:
• Programming & Systems: Strong hands-on coding in Python, JavaScript, and C, with solid grasp of OOP principles, SDLC, and relational databases (PostgreSQL, SQL).
• Modern Engineering Practices: Experienced with Git version control, CI/CD pipeline automation, and leveraging AI-native developer tooling to accelerate development velocity.
• Problem Solving: Solved 250+ problems on LeetCode demonstrating strong analytical rigor and structured debugging skills.
• Eager Learner: Adaptable, disciplined, and ready to learn new enterprise frameworks as needed.

Please find attached my resume for your review. My technical portfolio and GitHub repositories are linked below:
• GitHub: https://github.com/parthmishra9942
• Portfolio: https://ai-portfolio-beige-xi.vercel.app/

Thank you for your time and consideration. I look forward to hearing from you regarding the next steps.

Best regards,

Parth Mishra
Phone: +91-7985982208
Email: parthmishra9942@gmail.com
"""
    },
    {
        "id": "devlabs",
        "company": "DevLabs Technology",
        "role": "QA & Automation Testing Intern (Noida)",
        "to": "jahnavi.mishra@devlabstechnology.com",
        "cc": [],
        "subject": "Application for QA & Automation Intern – Parth Mishra | Strong SQL, Java & Testing Fundamentals",
        "body": """Dear Jahnavi,

I hope this email finds you well.

I am writing to apply for the QA & Automation Testing position at DevLabs Technology in Noida. As a B.Tech Computer Science student at VIT Bhopal (CGPA: 8.67), I have built strong competencies in core programming, SQL query validation, test case design, and software lifecycle methodologies.

Key qualifications:
• Database & Validation: Proficient in writing structured SQL queries for back-end data verification and edge-case validation.
• Systems & Core Concepts: Strong grounding in Object-Oriented Programming (Java/Python), SDLC, STLC, and test automation patterns.
• Problem Solving & Attention to Detail: Solved 250+ algorithmic problems on LeetCode, giving me a disciplined eye for boundary cases, regression risks, and code defects.
• Work Arrangement: Completely comfortable working onsite in Noida 5 days a week.

Please find attached my updated resume for your review.

• GitHub: https://github.com/parthmishra9942
• Portfolio: https://ai-portfolio-beige-xi.vercel.app/

Thank you for your consideration. I look forward to the opportunity to discuss my qualifications with your team.

Warm regards,

Parth Mishra
Phone: +91-7985982208
Email: parthmishra9942@gmail.com
VIT Bhopal University
"""
    },
    {
        "id": "blackbucks",
        "company": "Blackbucks Education",
        "role": "AI & Management Intern (Hyderabad)",
        "to": "Hr@blackbucks.me",
        "cc": [],
        "subject": "Application for AI & Management Intern – Parth Mishra | Oracle Certified Agentic AI | GenAI Workflows",
        "body": """Dear Hiring Team at Blackbucks Education,

I am writing to express my interest in the AI & Management Intern position in Hyderabad to support your leadership team in testing AI tools and building high-impact workflows.

As a B.Tech Computer Science (AI/ML) candidate at VIT Bhopal (CGPA: 8.67) and an Oracle Certified Foundations Associate in Agentic AI, I actively use and build with cutting-edge AI systems daily (Claude, ChatGPT, Gemini, LangChain, API workflows).

What I bring to the role:
• Practical AI Tool Mastery: Deep proficiency in prompt engineering, automated AI research pipelines, and structuring multi-agent workflows.
• Analytical & Synthesis Skills: Experience translating complex technical research into executive summaries, documentation, and data-driven presentations.
• High Ownership: Proactive self-starter with excellent communication skills, comfortable interacting directly with executive leadership.

Please find attached my resume for your consideration. You can explore my live AI projects at:
• Portfolio: https://ai-portfolio-beige-xi.vercel.app/
• GitHub: https://github.com/parthmishra9942

Thank you, and I look forward to discussing how I can support Blackbucks Education's AI initiatives.

Best regards,

Parth Mishra
Phone: +91-7985982208
Email: parthmishra9942@gmail.com
"""
    }
]

def get_sent_recipients():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    m = imaplib.IMAP4_SSL(cfg["imap_server"])
    m.login(cfg["email"], cfg["password"])
    status, _ = m.select('"[Gmail]/Sent Mail"', readonly=True)
    if status != "OK":
        return set()
    _, data = m.uid("search", None, "ALL")
    uids = data[0].split()
    sent_emails = set()
    for u in uids[-100:]:
        _, d = m.uid("fetch", u, "(BODY.PEEK[HEADER.FIELDS (TO CC)])")
        if d and d[0] and isinstance(d[0], tuple):
            hdr = email.message_from_bytes(d[0][1])
            found = re.findall(r'[\w\.-]+@[\w\.-]+', str(hdr.get("To", "")) + " " + str(hdr.get("Cc", "")))
            for e in found:
                sent_emails.add(e.lower())
    m.logout()
    return sent_emails

def load_credentials():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    return cfg["email"], cfg["password"]

def build_message(sender_email, item):
    msg = MIMEMultipart()
    msg["From"] = f"Parth Mishra <{sender_email}>"
    msg["To"] = item["to"]
    if item.get("cc"):
        msg["Cc"] = ", ".join(item["cc"])
    msg["Subject"] = item["subject"]
    msg.attach(MIMEText(item["body"], "plain", "utf-8"))
    
    if os.path.exists(RESUME_PATH):
        with open(RESUME_PATH, "rb") as f:
            part = MIMEBase("application", "pdf")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                'attachment; filename="Parth_Mishra_Resume.pdf"',
            )
            msg.attach(part)
    return msg

def process_applications(dry_run=True):
    sent_set = get_sent_recipients()
    print(f"Loaded {len(sent_set)} previously contacted email addresses from Sent Mail.")
    
    sender_email, app_password = load_credentials()
    
    eligible = []
    skipped = []
    
    for app in CANDIDATE_APPLICATIONS:
        to_addr = app["to"].lower()
        if to_addr in sent_set:
            skipped.append((app["company"], app["to"], "ALREADY IN SENT MAIL"))
        else:
            eligible.append(app)
            
    print("\n--- DUPLICATE CHECK RESULTS ---")
    if skipped:
        print("PREVENTED DUPLICATES:")
        for comp, addr, reason in skipped:
            print(f"  [X BLOCKED] {comp} ({addr}) -> {reason}")
    else:
        print("No duplicates detected among candidate applications.")
        
    print(f"\nVERIFIED UNAPPLIED TARGETS: {len(eligible)}")
    for app in eligible:
        print(f"  [OK READY] {app['company']} ({app['role']}) -> {app['to']}")
        
    if dry_run:
        print("\n>>> [DRY RUN COMPLETE] Zero emails sent. Ready to dispatch on confirmation.")
        return eligible
        
    if not eligible:
        print("No new eligible emails to send.")
        return []
        
    print(f"\n>>> Connecting to smtp.gmail.com:465 to send {len(eligible)} emails...")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        for app in eligible:
            try:
                msg = build_message(sender_email, app)
                recipients = [app["to"]] + app.get("cc", [])
                server.sendmail(sender_email, recipients, msg.as_string())
                print(f">>> [SUCCESS] Application dispatched to {app['company']} ({app['to']})")
            except Exception as e:
                print(f">>> [ERROR] Failed to send to {app['to']}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--send":
        process_applications(dry_run=False)
    else:
        process_applications(dry_run=True)
