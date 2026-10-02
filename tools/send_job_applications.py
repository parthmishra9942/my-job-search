import os
import sys
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CONFIG_FILE = "personal_email_config.json"
RESUME_PATH = r"C:\Users\parth\Downloads\Parth_Mishra_Resume.pdf"

EMAILS_TO_SEND = [
    {
        "id": "lab3",
        "company": "Lab3 Asia",
        "role": "AI Agent Engineer (Full-Time Remote)",
        "to": "hradmin@lab3.asia",
        "cc": [],
        "subject": "Application for AI Agent Engineer – Parth Mishra | Oracle Certified Agentic AI | Multi-Agent & RAG Systems",
        "body": """Dear Hiring Team at Lab3,

I am writing to express my strong interest in the AI Agent Engineer (Full-Time Remote) role. As a B.Tech Computer Science (AI/ML) candidate at VIT Bhopal (CGPA: 8.67) and an Oracle Certified Foundations Associate in Agentic AI, I specialize directly in architecting multi-agent coordination workflows, deterministic RAG pipelines, and model context integration.

Why I am an exceptional fit for Lab3’s agentic systems:
• Agentic Architectures & Workflows: Deep practical experience designing autonomous routing, tool-calling loops, and multi-agent consensus mechanisms using Python, LangChain, and FastAPI.
• Retrieval & Memory Systems (RAG): Built "DocuChat" (multimodal enterprise document Q&A with Milvus vector search) and "PulseAI" (diagnostic triage agent using dynamic context window management and semantic routing).
• Protocol & Engineering Depth: Familiar with emerging agentic standards including Model Context Protocol (MCP), prompt defense guardrails, and deterministic schema outputs.
• Hands-On Software Engineering: 250+ LeetCode problems solved, clean code discipline, and scalable API backend development.

Please find attached my executive resume. You can explore my live demos and code implementations below:
• Portfolio: https://ai-portfolio-beige-xi.vercel.app/
• GitHub: https://github.com/parthmishra9942
• LeetCode: https://leetcode.com/u/parth213g

I am ready to begin immediately and commit fully to building next-generation agentic systems with Lab3.

Best regards,

Parth Mishra
Phone: +91-7985982208
Email: parthmishra9942@gmail.com
"""
    },
    {
        "id": "codehurdle",
        "company": "CodeHurdle",
        "role": "SDE Intern (Bangalore - ₹35k/mo)",
        "to": "support@codehurdle.com",
        "cc": [],
        "subject": "Application for SDE Intern – Parth Mishra | Backend Systems, PostgreSQL & DSA (250+ LeetCode)",
        "body": """Dear Engineering Team at CodeHurdle,

I am writing to apply for the SDE Intern position in Bangalore. As a Computer Science (AI/ML) student at VIT Bhopal (CGPA: 8.67), I focus heavily on resilient backend systems, database performance, and low-latency API architecture.

Why I would be an immediate contributor to CodeHurdle:
• Systems & Concurrency: Built high-throughput backend services and in-memory vector databases with sub-millisecond retrieval and structured schema designs.
• Database Depth: Extensive experience with PostgreSQL query optimization, connection pooling, and ACID-compliant transactional consistency (used in my production project, Insta Insights).
• Algorithmic Foundation: Solved 250+ algorithmic problems on LeetCode covering graph traversal, dynamic programming, sliding window, and two-pointer patterns.
• Hands-on Mindset: Comfortable with Docker containerization, REST/WebSocket paradigms, and shipping clean, maintainable code.

Please find attached my resume. You can explore my live code repositories and demos below:
• Portfolio: https://ai-portfolio-beige-xi.vercel.app/
• GitHub: https://github.com/parthmishra9942
• LeetCode: https://leetcode.com/u/parth213g

I am ready to join onsite in Electronic City, Bangalore and commit full-time to building high-scale production systems.

Best regards,

Parth Mishra
Phone: +91-7985982208
Email: parthmishra9942@gmail.com
"""
    },
    {
        "id": "aptino",
        "company": "Aptino, Inc.",
        "role": "AI Engineer - Fresher (Pune)",
        "to": "aditi.akulwar@aptino.com",
        "cc": [],
        "subject": "Application for AI Engineer (Fresher) – Parth Mishra | Oracle Certified Agentic AI | B.Tech CSE (AI/ML)",
        "body": """Dear Aditi,

I hope this email finds you well.

I am writing to express my strong interest in the AI Engineer (Fresher) position at Aptino, Inc. in Pune. As a final-year B.Tech Computer Science student specializing in Artificial Intelligence & Machine Learning at VIT Bhopal (CGPA: 8.67), I have developed hands-on experience building production-grade Generative AI systems, Agentic AI workflows, and LLM pipelines.

Key highlights of my background:
• Oracle Certified Foundations Associate – Agentic AI (Sept 2026).
• Deep hands-on experience in Python, PyTorch, LangChain, LlamaIndex, FAISS, and FastAPI.
• Built "PulseAI", an autonomous medical triaging system using multi-agent routing, RAG, and FastAPI, reducing symptom diagnostic latency by 45%.
• Architected "DocuChat", a multimodal enterprise document Q&A engine powered by Llama 3 and Milvus vector search with 92% retrieval accuracy.
• Solved 250+ algorithmic problems across LeetCode and competitive programming platforms.

I am eager to contribute to Aptino’s AI engineering initiatives and can join immediately.

Please find attached my updated executive resume for your review. You can also explore my portfolio and code repositories below:
• Portfolio: https://ai-portfolio-beige-xi.vercel.app/
• GitHub: https://github.com/parthmishra9942
• LeetCode: https://leetcode.com/u/parth213g

Thank you for your time and consideration. I look forward to speaking with you.

Warm regards,

Parth Mishra
Phone: +91-7985982208
Email: parthmishra9942@gmail.com
VIT Bhopal University
"""
    },
    {
        "id": "makonis",
        "company": "Makonis Software",
        "role": "Software Developer (Mangalagiri)",
        "to": "madhuri.s@makonissoft.com",
        "cc": ["Kishore.s@makonissoft.com"],
        "subject": "Application for Software Developer – Parth Mishra | B.Tech CSE | Strong C/C++ & DSA",
        "body": """Dear Hiring Team,

I am writing to apply for the Software Developer opening at Makonis Software in Mangalagiri. 

I am a B.Tech Computer Science student at VIT Bhopal University (CGPA: 8.67) with a rigorous foundation in C/C++ programming, core data structures, algorithms, and systems engineering.

Why I would be a great fit for Makonis Software:
• Core Systems & C Programming: Solid grasp of low-level memory management, pointers, concurrency, and algorithm optimization in C and C++.
• Problem Solving: Solved 250+ algorithmic problems on LeetCode demonstrating disciplined problem decomposition and clean code implementation.
• Software Engineering Practices: Hands-on experience developing modular microservices, REST APIs, Git workflows, and CI/CD automation pipelines.
• Work Arrangement: Completely comfortable with working on-site at Mangalagiri and ready to hit the ground running.

Please find attached my resume detailing my technical projects and academic background. 

• GitHub: https://github.com/parthmishra9942
• Portfolio: https://ai-portfolio-beige-xi.vercel.app/
• LeetCode: https://leetcode.com/u/parth213g

Thank you for your consideration. I look forward to hearing from your team regarding next steps.

Sincerely,

Parth Mishra
Phone: +91-7985982208
Email: parthmishra9942@gmail.com
VIT Bhopal University
"""
    }
]

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
    
    # Body
    msg.attach(MIMEText(item["body"], "plain", "utf-8"))
    
    # Attachment
    if os.path.exists(RESUME_PATH):
        with open(RESUME_PATH, "rb") as f:
            part = MIMEBase("application", "pdf")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f'attachment; filename="Parth_Mishra_Resume.pdf"',
            )
            msg.attach(part)
    else:
        print(f"WARNING: Resume file not found at {RESUME_PATH}!")
    
    return msg

def send_all(dry_run=True, target_ids=None):
    sender_email, app_password = load_credentials()
    targets = [m for m in EMAILS_TO_SEND if not target_ids or m["id"] in target_ids]
    
    print(f"\nTargeting {len(targets)} email(s) | Dry Run: {dry_run}")
    print(f"Sender: {sender_email}")
    print(f"Attachment: {RESUME_PATH} (Exists: {os.path.exists(RESUME_PATH)})")
    print("=" * 60)
    
    for item in targets:
        print(f"\n[COMPANY]   : {item['company']}")
        print(f"[ROLE]      : {item['role']}")
        print(f"[TO]        : {item['to']}")
        if item.get("cc"):
            print(f"[CC]        : {', '.join(item['cc'])}")
        print(f"[SUBJECT]   : {item['subject']}")
        
        if dry_run:
            print(">>> [DRY RUN] Message built successfully. Not sending.")
            continue
            
        print(">>> Connecting to smtp.gmail.com:465...")
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, app_password)
                msg = build_message(sender_email, item)
                recipients = [item["to"]] + item.get("cc", [])
                server.sendmail(sender_email, recipients, msg.as_string())
                print(f">>> [SUCCESS] Email sent to {item['to']}!")
        except Exception as e:
            print(f">>> [ERROR] Failed to send to {item['to']}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--send":
        send_all(dry_run=False)
    elif len(sys.argv) > 1 and sys.argv[1] == "--send-ai":
        send_all(dry_run=False, target_ids=["lab3", "codehurdle"])
    else:
        send_all(dry_run=True)
