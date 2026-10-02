# Search Queries for Job Scraper

## Installed portal CLIs (primary for `/scrape`)

`/scrape` discovers every portal skill under `.agents/skills/*/SKILL.md` and runs its CLI first. Shipped country-agnostic CLIs include `linkedin-search` and `freehire-search`.
(Danish demo portals Jobindex, Jobbank, Jobdanmark, and Jobnet remain disabled by default).

The `site:` query templates in this file are the **WebSearch fallback** — for portals without a dedicated CLI (such as Naukri, Indeed, and Unstop), company career pages, or when a CLI fails.

**Language scope:** English is the primary language for technical job postings and search queries.

## Search Sites

Primary:
- **linkedin.com/jobs** - LinkedIn job listings (filtered for India and Remote; covered directly by `linkedin-search` CLI)
- **naukri.com** - Leading job board in India for Software Engineering, SDE, and Tech roles
- **indeed.com / in.indeed.com** - Global & India tech listings
- **unstop.com** - Early-career, graduate, tech internships, and hackathons in India
- **freehire.me** - Aggregated developer and engineering listings (covered by `freehire-search` CLI)

Secondary:
- Direct Google searches with `site:` filters for high-growth tech startups and product companies

## Query Categories

Queries are grouped by priority, organized by function rather than rigid titles.

### Priority 1: Software Development Engineer (SDE) & Full-Stack Development

These match Parth's strongest core capability: building end-to-end applications across React, Node.js, and modern databases with strong DSA fundamentals.

```
# Multi-Platform Queries:
site:naukri.com "Software Development Engineer" OR "SDE" "Python" OR "Node.js" "India"
site:naukri.com "Full Stack Developer" "React" "Node.js" "PostgreSQL"
site:in.indeed.com "Software Development Engineer" OR "SDE 1" ("Python" OR "Node.js")
site:in.indeed.com "Junior Software Engineer" OR "Graduate Engineer Trainee" ("Python" OR "React")
site:unstop.com/jobs "Software Engineer" OR "SDE" "2026" OR "2027" OR "Fresher"
site:unstop.com/internships "Software Development" OR "Full Stack" "Intern"
site:linkedin.com/jobs "Software Engineer" ("React" OR "Node.js") India
site:linkedin.com/jobs "Full Stack Engineer" ("React Native" OR "Node") Remote
```

### Priority 2: Generative AI, RAG & Agentic AI Engineering

These leverage Parth's AI/ML specialization, Oracle Agentic AI certification, RAG pipeline building, and Claude API integration experience.

```
# Multi-Platform Queries:
site:naukri.com "AI Engineer" OR "Generative AI Engineer" "Python" ("RAG" OR "LLM")
site:naukri.com "AI Agent Developer" OR "LLM Engineer" Python
site:in.indeed.com "AI Engineer" OR "Generative AI Engineer" ("Python" OR "LLM")
site:in.indeed.com "Machine Learning Engineer" "Python" ("Ollama" OR "LangChain" OR "RAG")
site:unstop.com/jobs "AI Engineer" OR "Machine Learning Engineer" India
site:unstop.com/internships "AI" OR "GenAI" OR "LLM" "Intern"
site:linkedin.com/jobs "AI Engineer" OR "Generative AI Engineer" "RAG" OR "LLM" India
site:linkedin.com/jobs "Conversational AI Developer" OR "Prompt Engineer" "LLM"
```

### Priority 3: Backend & Systems Engineering

These target backend API services, database architecture, and network/systems programming roles.

```
# Multi-Platform Queries:
site:naukri.com "Backend Developer" ("Node.js" OR "Express" OR "Python") "PostgreSQL"
site:naukri.com "API Developer" "REST API" "JWT" "SQL"
site:in.indeed.com "Backend Engineer" OR "Python Developer" "FastAPI" OR "Django"
site:in.indeed.com "Systems Engineer" OR "Network Software Engineer" "Python" "C++"
site:unstop.com/jobs "Backend Developer" OR "Python Developer" India
site:linkedin.com/jobs "Python Backend Developer" "Flask" OR "FastAPI" India
```

### Priority 4: Frontend & Mobile Development

These highlight cross-browser UI development (demonstrated at Craftedge Academy) and mobile app engineering (React Native).

```
site:naukri.com "Frontend Developer" "React" "TypeScript" "Vite"
site:linkedin.com/jobs "React Native Developer" "Mobile App Developer" India OR Remote
site:in.indeed.com "Frontend Engineer" "HTML5" "CSS3" "JavaScript" Responsive UI
```

## Location Filter

When evaluating results, classify job locations into the following tiers:
- **Ideal:** Remote (worldwide or India), Bhopal
- **Acceptable:** Bangalore, Pune, Hyderabad, Gurgaon / Delhi NCR, Noida, Mumbai, Chennai (On-site or Hybrid)
- **Borderline:** Other tier-1 / tier-2 cities across India with relocation support
- **Too Far / Exclude:** Uncompensated on-site positions in remote locations, international roles without visa sponsorship/remote option

## Compensation & Quality Filter

- **Unpaid Internships:** FAIL — hard deal-breaker. Do not draft or recommend.
- **Non-Technical Roles:** FAIL — must involve software development, AI engineering, or technical problem solving.

## Language Filter

Apply the Language Gate from `04-job-evaluation.md`:
- English: Fluent / Professional working proficiency (PASS for all English-medium postings)
- Hindi: Intermediate (conversational)
- Postings requiring any other undeclared language as a mandatory job condition: FAIL

## Date Filter

Only include jobs posted within the last 14 days, or with an application deadline that has not yet passed. If a posting date cannot be determined, include it but flag as "date unknown".

## Adapting Queries

If the user specifies a focus area, select queries from the matching category and also generate 2-3 custom queries for that focus. For example:
- `/scrape SDE` -> Priority 1 queries + specific SDE 1 / Entry-Level SDE terms
- `/scrape GenAI` -> Priority 2 queries + LLM / Agentic AI focus
