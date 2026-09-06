"""
Curated Library of 20+ Production-Grade Prompt Templates
"""
from typing import List, Dict, Any

TEMPLATES: List[Dict[str, Any]] = [
    # --- Software Engineering ---
    {
        "id": "code-review",
        "title": "Production Code Review & Security Audit",
        "domain": "software",
        "category": "Software Engineering",
        "description": "Exhaustive code audit focusing on memory safety, security vulnerabilities, edge cases, and architectural clean code principles.",
        "tags": ["Code Review", "Security", "Clean Code", "Engineering"],
        "recommended_model": "claude",
        "prompt": """<role>
You are a Principal Software Architect and Security Auditor specializing in production-grade code reviews.
</role>

<context>
The following code is under review for merge into a mission-critical production service.
Language/Framework: [e.g., Python / FastAPI / PostgreSQL]
</context>

<instructions>
Conduct a rigorous code review examining the code below:
1. Identify any critical security vulnerabilities (OWASP Top 10, injection, memory leaks, unhandled exceptions).
2. Evaluate adherence to clean code, SOLID principles, and idiomatic practices.
3. Suggest concrete performance optimizations with time/space complexity implications.
4. For each flagged issue, provide:
   - Location / Line reference
   - Severity: [Critical / High / Medium / Low]
   - Why it is problematic
   - The exact refactored replacement code snippet
</instructions>

<code_to_review>
[INSERT CODE HERE]
</code_to_review>

<output_format>
- Table summary of all findings ranked by severity.
- Detailed breakdown with diff/snippets.
- Final merge recommendation: [Approve / Approve with Minor Changes / Reject & Block].
</output_format>"""
    },
    {
        "id": "system-design",
        "title": "Distributed System Architecture Designer",
        "domain": "software",
        "category": "Software Engineering",
        "description": "End-to-end distributed system design covering data flow, database selection, caching, failure modes, and scalability bottlenecks.",
        "tags": ["Architecture", "Scalability", "Distributed Systems", "Backend"],
        "recommended_model": "chatgpt",
        "prompt": """### Role & Persona
Act as a Distinguished Systems Architect who designs high-scale distributed backends handling 100k+ QPS with 99.99% availability.

### Objective
Design a distributed system architecture for: [e.g., Global Real-time Notification System / Scalable URL Shortener].

### System Requirements & Parameters
- Target Scale: [e.g., 50M DAU, 150k read QPS, 10k write QPS]
- Latency SLA: [e.g., p99 < 50ms for reads]
- Consistency Model: [e.g., Eventual consistency acceptable for notifications]

### Required Architecture Sections
1. **High-Level Topology**: Core components, API gateway, microservices, messaging queues, and persistent storage.
2. **Data Model & Storage Strategy**: DB selection (SQL vs NoSQL), schema definitions, sharding/partitioning key strategy.
3. **Caching & Concurrency Control**: Cache invalidation policies, Redis/Memcached usage, rate limiting.
4. **Reliability & Disaster Recovery**: Circuit breakers, dead letter queues, multi-region replication.
5. **Trade-off Analysis**: State 3 crucial architectural trade-offs made and justify them.

### Output Rules
Use clean ASCII or Mermaid diagrams to illustrate data flow. Avoid generic boilerplate."""
    },
    {
        "id": "bug-investigator",
        "title": "RCA & Bug Post-Mortem Investigator",
        "domain": "software",
        "category": "Software Engineering",
        "description": "Systematic root cause analysis of intermittent bugs, memory leaks, or production crash reports.",
        "tags": ["Debugging", "RCA", "Post-Mortem", "SRE"],
        "recommended_model": "gemini",
        "prompt": """--- SYSTEM INSTRUCTION ---
You are a Senior Site Reliability Engineer and Systems Debugger. Perform a forensic Root Cause Analysis (RCA) on the following incident.

--- INCIDENT TELEMETRY & LOGS ---
Error Message / Traceback:
```
[INSERT TRACEBACK / LOG DUMP HERE]
```
Environmental Context: [e.g., Kubernetes pod OOMKilled during peak traffic spike]

--- INVESTIGATION DIRECTIVES ---
1. **Immediate Root Cause**: Identify the exact failure trigger in the stack trace.
2. **Contributing Factors**: Secondary conditions that allowed this failure to cascade.
3. **Hypothesis Verification**: Outline 2-3 hypotheses and how an engineer can verify each using specific CLI commands or logs.
4. **Permanent Remediation**: Provide code patch and infrastructure configuration to prevent recurrence.

--- OUTPUT FORMAT ---
Deliver the RCA in standard blameless post-mortem format with clear code diffs."""
    },
    {
        "id": "sql-optimizer",
        "title": "SQL Query & Index Optimizer",
        "domain": "data",
        "category": "Data Science & Analytics",
        "description": "Deconstruct slow SQL queries, explain execution plans, and recommend composite indexes and partition keys.",
        "tags": ["SQL", "Database", "Performance", "Indexing"],
        "recommended_model": "chatgpt",
        "prompt": """### Role
Senior Database Administrator (DBA) and PostgreSQL/MySQL Performance Tuning Specialist.

### Task
Analyze the slow query below, analyze potential bottlenecks in execution, and rewrite it for maximum throughput:

```sql
[INSERT SLOW SQL QUERY HERE]
```

### Context & Schema
- Database Engine: [e.g., PostgreSQL 15]
- Table Size: [e.g., 25 million rows]
- Existing Indexes: [e.g., Primary key on id, index on created_at]

### Deliverables
1. **Bottleneck Diagnosis**: Explain why the current query triggers sequential scans or inefficient joins.
2. **Optimized SQL**: Provide the rewritten query utilizing CTEs, window functions, or subqueries where beneficial.
3. **Index Recommendations**: Exact `CREATE INDEX` statements with composite column ordering explained.
4. **Execution Plan Benchmark**: Explain how the estimated EXPLAIN ANALYZE cost will shift."""
    },

    # --- Marketing & Content ---
    {
        "id": "saas-landing-copy",
        "title": "High-Converting SaaS Landing Page Copy",
        "domain": "marketing",
        "category": "Marketing & Copywriting",
        "description": "Conversion-focused landing page copy using proven copywriting frameworks (PAS, AIDA, Hook-Story-Offer).",
        "tags": ["Copywriting", "SaaS", "Conversion Rate", "Landing Page"],
        "recommended_model": "claude",
        "prompt": """<role>
You are an elite Direct-Response Copywriter who has written landing pages generating over $50M in ARR for B2B SaaS companies.
</role>

<product_context>
Product Name: [Product Name]
Value Proposition: [Core Promise / Unique Selling Proposition]
Target Audience: [e.g., VP of Engineering at Series B-D Startups]
Primary Pain Point: [e.g., Deployments take 45 minutes and break on Fridays]
</product_context>

<instructions>
Write complete, high-converting copy for the landing page following this structure:
1. **Hero Section**:
   - Compelling curiosity/pain hook headline (under 10 words).
   - High-clarity sub-headline explaining the exact mechanism and outcome.
   - Primary and secondary CTA button micro-copy.
   - Social proof ticker snippet.
2. **Problem/Agitation (The Villain)**:
   - 3 bullet points depicting the current painful, costly status quo.
3. **The Solution (The Hero Feature Stack)**:
   - 3 feature-benefit pairs translated into quantifiable outcomes (e.g. 'Deploy in 3 minutes instead of 45').
4. **FAQ Section**:
   - Address the top 3 buying objections (Security/Compliance, Migration Effort, Pricing).
</instructions>

<constraints>
- Avoid buzzwords like 'revolutionary', 'game-changing', 'synergy', or 'all-in-one'.
- Speak directly in the customer's native vocabulary.
</constraints>"""
    },
    {
        "id": "email-launch-sequence",
        "title": "5-Day Product Launch Email Sequence",
        "domain": "marketing",
        "category": "Marketing & Copywriting",
        "description": "Psychologically calibrated 5-part email launch sequence to nurture leads and drive urgency.",
        "tags": ["Email Marketing", "Launches", "Drip Campaign", "Sales"],
        "recommended_model": "chatgpt",
        "prompt": """### Role
Master Email Copywriter specializing in launch campaigns with 40%+ open rates and 8%+ click-through rates.

### Product & Offer
- Launch Offer: [Describe Product & Special Launch Incentive]
- Deadline/Urgency: [e.g., 5-day window, early-bird 30% discount]
- Target Reader: [Describe ideal subscriber profile]

### Sequence Architecture
Generate a complete 5-email sequence:
- **Email 1 (Teaser / The Shift)**: Introduce the paradigm shift, break a common myth, and tease the solution.
- **Email 2 (The Origin / Case Study)**: Relatable transformation story showing before/after results.
- **Email 3 (The Cart Opens)**: Full reveal, clear feature breakdown, and primary call to action.
- **Email 4 (Objection Annihilation)**: Answering the 3 biggest reasons someone might hesitate.
- **Email 5 (Closing Hours / Urgency)**: Final countdown, scarcity reminder, and clean summary.

### Requirements for Each Email
- Provide 3 punchy Subject Line variations (Curiosity, Benefit, Urgency).
- 1 Preview text line.
- Full email body with strategically placed CTAs.
- P.S. line reinforcing FOMO or social proof."""
    },

    # --- Data Science & Analytics ---
    {
        "id": "eda-framework",
        "title": "Comprehensive Exploratory Data Analysis (EDA) Blueprint",
        "domain": "data",
        "category": "Data Science & Analytics",
        "description": "Production-ready Python EDA script and statistical analysis plan for any structured dataset.",
        "tags": ["Data Science", "Python", "EDA", "Statistics"],
        "recommended_model": "chatgpt",
        "prompt": """### Role & Persona
Principal Data Scientist and Quantitative Researcher with deep expertise in Pandas, Seaborn, and statistical hypothesis testing.

### Objective
Create a structured Exploratory Data Analysis (EDA) framework in Python for the following dataset:
- Dataset Description: [e.g., E-commerce customer transactions with churn flags]
- Target Variable: [e.g., `is_churned` (binary 0/1)]
- Key Dimensions: [e.g., user demographics, transaction recency, frequency, monetary value]

### Required Methodology
1. **Data Hygiene & Integrity Check**: Code to detect missing value patterns, anomalies, duplicates, and data type mismatches.
2. **Univariate & Bivariate Distributions**: Visualizations for skewness, kurtosis, and correlation with the target variable.
3. **Feature Engineering Ideation**: 4 novel derived features that capture non-linear behavioral signals.
4. **Outlier Mitigation Strategy**: Comparison of IQR trimming vs Robust Scaling.
5. **Statistical Significance Tests**: Appropriate hypothesis test (e.g. Mann-Whitney U or Chi-Square) to validate feature variance.

### Constraints
Deliver clean, modular, production-ready Python code with docstrings and type annotations."""
    },

    # --- Business & Strategy ---
    {
        "id": "executive-memo",
        "title": "Amazon-Style 6-Page Narrative Memo",
        "domain": "business",
        "category": "Business & Strategy",
        "description": "Rigorous narrative memo framework modeled after Amazon's famous backward-working memo format.",
        "tags": ["Executive Memo", "Strategy", "Amazon 6-Pager", "Decision Making"],
        "recommended_model": "claude",
        "prompt": """<system>
You are an Executive Strategy Consultant who trains Fortune 100 executives on the Amazon 6-Page Narrative memo methodology.
</system>

<context>
Proposal Topic: [e.g., Expanding our B2B SaaS platform into the APAC enterprise market]
Owner: [Department / Champion]
Decision to Be Made: [Approve $2.5M initial pilot budget]
</context>

<memo_structure>
Draft the executive memo following the rigorous 6-pager structure:
1. **Introduction & Strategic Context**: The fundamental business thesis and market dynamics.
2. **Goals & Tenets**: Clear metrics (Input metrics vs Output metrics) and operating principles.
3. **Current State & The Problem**: Why status quo is unacceptable with supporting data points.
4. **Proposed Solution & Mechanism**: How the new initiative works, step-by-step.
5. **Risks, Unknowns & Mitigations**: Honest assessment of failure modes and kill criteria.
6. **Financials & Resource Allocation**: P&L assumptions and headcount requirements.
</memo_structure>

<rules>
- Eliminate corporate clichés and adjectives. Use empirical facts and clear numbers.
- Ensure the tone is objective, humble, and analytical.
</rules>"""
    },
    {
        "id": "competitive-battlecard",
        "title": "Competitor Sales Battlecard & Moat Analysis",
        "domain": "business",
        "category": "Business & Strategy",
        "description": "Tactical sales battlecard detailing competitor vulnerabilities, landmine questions, and feature differentiators.",
        "tags": ["Competitor Analysis", "Sales Battlecard", "Product Marketing", "Strategy"],
        "recommended_model": "gemini",
        "prompt": """--- SYSTEM INSTRUCTION ---
Act as a VP of Product Marketing and Competitive Intelligence. Build a field-ready Sales Battlecard.

--- COMPETITIVE MATRIX ---
Our Company/Product: [Your Product]
Competitor: [Competitor Name]
Target Deal Profile: [e.g., Enterprise Deals $100k+ ACV]

--- BATTLECARD MODULES ---
1. **Quick Pitch & Positioning**: 30-second elevator soundbite explaining why we win against them.
2. **Competitor Strengths (Fair Assessment)**: Where they genuinely excel and how our sales reps should concede gracefully.
3. **Competitor Landmines & Fatal Flaws**: Known technical debt, hidden pricing fees, or compliance gaps.
4. **Silver Bullet Discovery Questions**: 3 questions our AE can ask the buyer that expose the competitor's biggest weakness.
5. **Feature Showdown Table**: Direct comparison of 4 critical workflow capabilities with our clear edge highlighted.

--- FORMATTING ---
Use concise bullet points, bold key phrases, and high-impact callout boxes."""
    },

    # --- Academic & Research ---
    {
        "id": "literature-review",
        "title": "Academic Literature Review Synthesizer",
        "domain": "research",
        "category": "Academic & Research",
        "description": "Synthesize diverse research papers into a coherent literature review identifying theoretical consensus and research gaps.",
        "tags": ["Research", "Literature Review", "Academia", "Synthesis"],
        "recommended_model": "claude",
        "prompt": """<role>
You are an Academic Research Fellow and Senior Journal Editor.
</role>

<task>
Synthesize the state of research regarding: [e.g., Impact of Retrieval-Augmented Generation on LLM Hallucination Rates].
</task>

<instructions>
Structure the literature synthesis as follows:
1. **Theoretical Foundations**: The core conceptual frameworks underpinning the subject.
2. **Thematic Consensus**: Areas where current empirical studies converge and agree.
3. **Scholarly Contradictions & Debate**: Conflicting findings between leading methodologies.
4. **Methodological Critiques**: Limitations of current experimental setups (e.g. sample sizes, benchmark saturation).
5. **Identified Research Gaps**: 3 specific unanswered research questions ripe for novel contribution.
</instructions>

<constraints>
- Maintain strict scholarly tone.
- Distinguish between theoretical speculation and empirically replicated findings.
</constraints>"""
    },

    # --- General Power Prompts ---
    {
        "id": "universal-problem-solver",
        "title": "First-Principles Root Problem Solver",
        "domain": "general",
        "category": "General & Problem Solving",
        "description": "Deconstruct any complex, multi-variable dilemma from fundamental first principles to breakthrough solutions.",
        "tags": ["First Principles", "Strategy", "Problem Solving", "Frameworks"],
        "recommended_model": "universal",
        "prompt": """# ROLE & FRAMEWORK
You are a First-Principles Problem Solver who strip away analogies, historical baggage, and conventions to analyze problems from foundational physical and logical truths.

# PROBLEM STATEMENT
[Describe the complex problem or deadlock you are trying to solve]

# METHODOLOGY
1. **Deconstruct Assumptions**: List all implicit beliefs and assumptions surrounding this problem, then test which ones are actually immutable facts versus mere conventions.
2. **Fundamental Truths**: What are the irreducible, non-negotiable axioms at play here?
3. **Combinatorial Synthesis**: Rebuild a novel solution from the ground up using only verified truths.
4. **Stress Testing**: How could this solution fail? What is the single biggest bottleneck?
5. **Execution Blueprint**: The simplest, lowest-friction experiment to test this hypothesis in 48 hours."""
    }
]

def get_all_templates() -> List[Dict[str, Any]]:
    return TEMPLATES

def get_template_by_id(template_id: str) -> Dict[str, Any]:
    for t in TEMPLATES:
        if t["id"] == template_id:
            return t
    return TEMPLATES[0]
