import re
from typing import Dict, List, Tuple
from .models import MetricScore, CategoryScore, AnalyzeResponse

# Metric definitions and weighting
METRIC_SPECS = [
    {
        "id": "clarity",
        "name": "Clarity & Precision",
        "category": "Clarity & Intent",
        "weight": 1.1,
    },
    {
        "id": "specificity",
        "name": "Instruction Specificity",
        "category": "Clarity & Intent",
        "weight": 1.2,
    },
    {
        "id": "objective",
        "name": "Objective & Goal Definition",
        "category": "Clarity & Intent",
        "weight": 1.0,
    },
    {
        "id": "persona",
        "name": "Role & Persona Framing",
        "category": "Context & Framing",
        "weight": 0.9,
    },
    {
        "id": "context",
        "name": "Contextual Grounding",
        "category": "Context & Framing",
        "weight": 1.0,
    },
    {
        "id": "constraints",
        "name": "Constraint & Rule Definition",
        "category": "Execution & Control",
        "weight": 1.0,
    },
    {
        "id": "structure",
        "name": "Structural Formatting & Delimiters",
        "category": "Structure & Reasoning",
        "weight": 1.0,
    },
    {
        "id": "chain_of_thought",
        "name": "Reasoning & Step-by-Step Elicitation",
        "category": "Structure & Reasoning",
        "weight": 0.9,
    },
    {
        "id": "few_shot",
        "name": "Few-Shot Examples / Exemplars",
        "category": "Structure & Reasoning",
        "weight": 0.8,
    },
    {
        "id": "output_format",
        "name": "Output Format & Schema Specification",
        "category": "Execution & Control",
        "weight": 1.2,
    },
    {
        "id": "edge_cases",
        "name": "Edge-Case & Fallback Handling",
        "category": "Execution & Control",
        "weight": 0.8,
    },
    {
        "id": "hallucination_safeguards",
        "name": "Hallucination & Fact Safeguards",
        "category": "Safety & Robustness",
        "weight": 0.9,
    },
    {
        "id": "conciseness",
        "name": "Signal-to-Noise Ratio & Conciseness",
        "category": "Clarity & Intent",
        "weight": 0.8,
    },
    {
        "id": "tone_style",
        "name": "Tone, Voice & Audience Guidance",
        "category": "Context & Framing",
        "weight": 0.8,
    },
    {
        "id": "readability",
        "name": "Instruction Hierarchy & Readability",
        "category": "Structure & Reasoning",
        "weight": 0.8,
    },
    {
        "id": "injection_resistance",
        "name": "Ambiguity & Delimiter Robustness",
        "category": "Safety & Robustness",
        "weight": 0.8,
    },
]

VAGUE_TERMS = [
    r"\bgood\b", r"\bnice\b", r"\bstuff\b", r"\bthings?\b", r"\bsomething\b",
    r"\bquick(?:ly)?\b", r"\bbetter\b", r"\binteresting\b", r"\bcool\b",
    r"\bmake it work\b", r"\blike normal\b", r"\betc\b", r"\band so on\b",
    r"\bas you see fit\b", r"\bwhatever\b", r"\bsome\b", r"\ba lot\b"
]

PERSONA_PATTERNS = [
    r"\byou are\b", r"\bact as\b", r"\bas an? (?:expert|senior|lead|world-class|experienced|specialist)\b",
    r"\byour role is\b", r"\byou represent\b", r"\bpretend you are\b", r"\bassume the role\b",
    r"\bpersona\b", r"\byou will serve as\b"
]

OUTPUT_PATTERNS = [
    r"\bjson\b", r"\btable\b", r"\bmarkdown\b", r"\bbullet(?:ed)? points?\b",
    r"\bcsv\b", r"\byaml\b", r"\bformat as\b", r"\boutput format\b",
    r"\bschema\b", r"\bxml\b", r"\brespond in\b", r"\breturn only\b",
    r"\blist of\b", r"\bstep-by-step\b", r"\btemplate\b", r"\bcolumns?\b",
    r"<output_format>"
]

CONSTRAINT_PATTERNS = [
    r"\bdo not\b", r"\bdon't\b", r"\bnever\b", r"\bonly\b", r"\blimit(?:ed)? to\b",
    r"\bmaximum\b", r"\bminimum\b", r"\bat most\b", r"\bat least\b",
    r"\bwithout\b", r"\bexclude\b", r"\bmust not\b", r"\bno more than\b",
    r"\bunder \d+ words\b", r"\bkeep it\b", r"\bstrictly\b", r"\bavoid\b",
    r"\bstrict adherence\b", r"<constraints>"
]

COT_PATTERNS = [
    r"\bstep by step\b", r"\bthink step by step\b", r"\breasoning\b",
    r"\bexplain your thought process\b", r"\bfirst,? analyze\b",
    r"\bbreak down\b", r"\bshow your work\b", r"\bscratchpad\b",
    r"<thinking>", r"\[reasoning\]", r"\bchain of thought\b"
]

FEW_SHOT_PATTERNS = [
    r"\bexample(?:s)?\s*:\b", r"\be\.g\.\b", r"\bfor instance\b",
    r"\binput\s*:\s*.*output\s*:\b", r"\bsample input\b", r"\bexemplar\b",
    r"<example>", r"```json.*```"
]

SAFEGUARD_PATTERNS = [
    r"\bif you don't know\b", r"\bdo not make up\b", r"\bcite sources\b",
    r"\brely strictly on\b", r"\bgrounded in\b", r"\bstate that you do not know\b",
    r"\bavoid hallucinating\b", r"\bdo not invent\b", r"\bonly use facts\b",
    r"\bunverified\b", r"\bif unsure\b", r"\bif (?:any|a|the) (?:detail|fact|data) is unverified\b"
]

EDGE_CASE_PATTERNS = [
    r"\bif (?:the|an?|input|data|user|any)\b.*?\b(?:then|state|return|fallback|raise)\b",
    r"\bcase of\b", r"\bin case\b", r"\bwhen missing\b", r"\bif empty\b",
    r"\bfallback\b", r"\bhandle errors?\b", r"\bif not found\b",
    r"\botherwise\b", r"\bif ambiguous\b", r"\bif (?:any|a|the) detail is unverified\b"
]

def score_clarity(text: str, words: List[str]) -> MetricScore:
    vague_matches = []
    for pattern in VAGUE_TERMS:
        found = re.findall(pattern, text, re.IGNORECASE)
        vague_matches.extend(found)
    
    word_count = len(words)
    penalty = min(len(vague_matches) * 12, 60)
    
    if word_count < 8:
        base_score = 30
    elif word_count < 15:
        base_score = 55
    else:
        base_score = 90

    final_score = max(10, min(100, base_score - penalty))
    status = "good" if final_score >= 80 else ("average" if final_score >= 50 else "poor")

    if vague_matches:
        vague_str = ", ".join(list(set(vague_matches))[:4])
        explanation = f"Detected {len(vague_matches)} ambiguous/vague words: '{vague_str}'."
        suggestion = "Replace fuzzy terms (e.g. 'good', 'quick', 'stuff') with exact quantified criteria."
    else:
        explanation = "Clear terminology with minimal ambiguity detected."
        suggestion = None

    return MetricScore(
        id="clarity",
        name="Clarity & Precision",
        category="Clarity & Intent",
        score=final_score,
        status=status,
        explanation=explanation,
        suggestion=suggestion,
        fix_action="clarify_terms"
    )

def score_specificity(text: str, words: List[str]) -> MetricScore:
    word_count = len(words)
    has_numbers = bool(re.search(r"\b\d+\b", text))
    has_quotes = bool(re.search(r"['\"`].+?['\"`]", text))
    has_specific_nouns = bool(re.search(r"\b(?:Python|JavaScript|API|SQL|CSS|JSON|Docker|AWS|React|ROI|SLA|PDF|CSV)\b", text, re.I))

    score = 25
    if word_count >= 15: score += 20
    if word_count >= 40: score += 20
    if word_count >= 80: score += 10
    if has_numbers: score += 10
    if has_quotes: score += 5
    if has_specific_nouns: score += 10

    score = max(10, min(100, score))
    status = "good" if score >= 80 else ("average" if score >= 50 else "poor")

    if score < 50:
        explanation = "The prompt is brief and lacks granular scope, parameters, and precise targets."
        suggestion = "Define explicit scope boundaries, target technologies, specific audience, and numeric thresholds."
    elif score < 80:
        explanation = "Moderate detail, but could benefit from specific numeric limits or explicit technical parameters."
        suggestion = "Specify exact lengths, technical stack versions, or clear scope boundaries."
    else:
        explanation = "High instructional specificity with detailed parameters and clear targets."
        suggestion = None

    return MetricScore(
        id="specificity",
        name="Instruction Specificity",
        category="Clarity & Intent",
        score=score,
        status=status,
        explanation=explanation,
        suggestion=suggestion,
        fix_action="add_specificity"
    )

def score_objective(text: str, words: List[str]) -> MetricScore:
    action_verbs = [
        r"\b(?:create|build|write|generate|summarize|analyze|explain|refactor|design|audit|evaluate|translate|convert|list|compare)\b"
    ]
    has_action = any(re.search(p, text, re.I) for p in action_verbs)
    has_goal_phrase = bool(re.search(r"\b(?:goal|objective|purpose|in order to|aim|target)\b", text, re.I))
    
    score = 30
    if has_action: score += 40
    if has_goal_phrase: score += 25
    if len(words) > 10: score += 5

    score = max(10, min(100, score))
    status = "good" if score >= 80 else ("average" if score >= 50 else "poor")

    if not has_action:
        explanation = "No primary action verb (e.g. 'Build', 'Analyze', 'Generate') clearly guiding the model."
        suggestion = "State the core mission upfront using a strong imperative verb."
    elif not has_goal_phrase and score < 80:
        explanation = "Action verb identified, but the underlying business or technical goal is not explicitly stated."
        suggestion = "Add an explicit goal: 'The goal of this output is to...'"
    else:
        explanation = "Clear objective with strong imperative action verbs and intended purpose."
        suggestion = None

    return MetricScore(
        id="objective",
        name="Objective & Goal Definition",
        category="Clarity & Intent",
        score=score,
        status=status,
        explanation=explanation,
        suggestion=suggestion,
        fix_action="add_objective"
    )

def score_persona(text: str) -> MetricScore:
    matches = []
    for p in PERSONA_PATTERNS:
        matches.extend(re.findall(p, text, re.I))
    
    has_persona = len(matches) > 0
    expert_level = bool(re.search(r"\b(?:expert|specialist|principal|senior|staff|distinguished|lead)\b", text, re.I))

    if has_persona and expert_level:
        score = 95
        explanation = "Strong expert persona established with specific domain seniority."
        suggestion = None
    elif has_persona:
        score = 80
        explanation = "Role/persona framing detected, but could be elevated with specific domain authority."
        suggestion = "Refine persona to specify years of experience, specialization, or perspective."
    else:
        score = 25
        explanation = "No system persona or role assigned. The AI will adopt generic default behavior."
        suggestion = "Assign an expert persona: 'Act as a Senior Systems Architect with 15+ years of experience...'"

    status = "good" if score >= 80 else ("average" if score >= 50 else "poor")

    return MetricScore(
        id="persona",
        name="Role & Persona Framing",
        category="Context & Framing",
        score=score,
        status=status,
        explanation=explanation,
        suggestion=suggestion,
        fix_action="add_persona"
    )

def score_context(text: str, words: List[str]) -> MetricScore:
    context_keywords = [
        r"\bcontext\b", r"\bbackground\b", r"\bgiven that\b", r"\bscenario\b",
        r"\bwe are\b", r"\bour company\b", r"\bthe user\b", r"\bcurrently\b",
        r"\bdataset\b", r"\bhere is the\b", r"\bbelow is\b"
    ]
    has_keywords = any(re.search(k, text, re.I) for k in context_keywords)
    word_count = len(words)

    score = 30
    if has_keywords: score += 35
    if word_count > 30: score += 20
    if word_count > 60: score += 15

    score = max(15, min(100, score))
    status = "good" if score >= 80 else ("average" if score >= 50 else "poor")

    if score < 50:
        explanation = "Prompt lacks background information, domain context, and situational framing."
        suggestion = "Provide background context explaining who the audience is, why this is needed, and any prerequisite knowledge."
    elif score < 80:
        explanation = "Basic context present, but more background on the operational environment would sharpen accuracy."
        suggestion = "Include industry context, target end-user profile, or existing systems."
    else:
        explanation = "Rich contextual grounding provided to anchor the AI's response."
        suggestion = None

    return MetricScore(
        id="context",
        name="Contextual Grounding",
        category="Context & Framing",
        score=score,
        status=status,
        explanation=explanation,
        suggestion=suggestion,
        fix_action="add_context"
    )

def score_constraints(text: str) -> MetricScore:
    matches = []
    for p in CONSTRAINT_PATTERNS:
        matches.extend(re.findall(p, text, re.I))
    
    count = len(matches)
    if count >= 3:
        score = 95
        explanation = f"Excellent constraint definition with {count} explicit boundaries/negative instructions."
        suggestion = None
    elif count >= 1:
        score = 75
        explanation = f"Found {count} constraint directives. Adding explicit negative constraints ('Do NOT...') improves reliability."
        suggestion = "Add boundary rules such as max word count, forbidden topics, or strict formatting exclusions."
    else:
        score = 25
        explanation = "No constraints found. The model is free to hallucinate, over-explain, or drift out of scope."
        suggestion = "Add explicit constraints: 'Do NOT use jargon', 'Limit output to 300 words', 'Exclude introductory chatter'."

    status = "good" if score >= 80 else ("average" if score >= 50 else "poor")

    return MetricScore(
        id="constraints",
        name="Constraint & Rule Definition",
        category="Execution & Control",
        score=score,
        status=status,
        explanation=explanation,
        suggestion=suggestion,
        fix_action="add_constraints"
    )

def score_structure(text: str) -> MetricScore:
    has_markdown_headers = bool(re.search(r"^#{1,4}\s+.+", text, re.M)) or bool(re.search(r"^<[a-zA-Z_-]+>", text, re.M))
    has_delimiters = bool(re.search(r"(?:---|```|===|<[a-zA-Z_-]+>)", text))
    has_bullet_or_number = bool(re.search(r"^\s*(?:[-*]|\d+\.)\s+", text, re.M))
    has_sections = bool(re.search(r"(?:Instructions?|Context|Format|Constraints?|Examples?|Task):\s*", text, re.I)) or bool(re.search(r"<(?:instructions?|context|format|constraints?|examples?|task|role|output_format)>", text, re.I))

    score = 25
    if has_markdown_headers: score += 25
    if has_delimiters: score += 25
    if has_bullet_or_number: score += 15
    if has_sections: score += 15

    score = max(20, min(100, score))
    status = "good" if score >= 80 else ("average" if score >= 50 else "poor")

    if score < 50:
        explanation = "Prompt is an unformatted block of text without clear sections, bullet points, or delimiters."
        suggestion = "Use markdown headings (### Section), bullet points, and delimiters (``` or XML tags) to parse easily."
    elif score < 80:
        explanation = "Partial formatting detected. Adding distinct delimiter blocks makes parsing bulletproof across models."
        suggestion = "Organize into distinct tagged sections: ### Context, ### Task, ### Output Rules."
    else:
        explanation = "Clean structural hierarchy with clear headings, delimiters, and list elements."
        suggestion = None

    return MetricScore(
        id="structure",
        name="Structural Formatting & Delimiters",
        category="Structure & Reasoning",
        score=score,
        status=status,
        explanation=explanation,
        suggestion=suggestion,
        fix_action="add_structure"
    )

def score_cot(text: str) -> MetricScore:
    matches = []
    for p in COT_PATTERNS:
        matches.extend(re.findall(p, text, re.I))
    
    if len(matches) >= 2:
        score = 95
        explanation = "Explicit multi-step thinking or scratchpad instructions provided."
        suggestion = None
    elif len(matches) == 1:
        score = 80
        explanation = "Found basic reasoning directive ('step by step')."
        suggestion = "Structure into clear phases: '1. Analyze requirements, 2. Draft architecture, 3. Validate against constraints'."
    else:
        score = 30
        explanation = "No reasoning or step-by-step elicitation. Complex queries may produce rushed conclusions."
        suggestion = "Instruct the model to think step-by-step or conduct an initial evaluation before providing the final answer."

    status = "good" if score >= 80 else ("average" if score >= 50 else "poor")

    return MetricScore(
        id="chain_of_thought",
        name="Reasoning & Step-by-Step Elicitation",
        category="Structure & Reasoning",
        score=score,
        status=status,
        explanation=explanation,
        suggestion=suggestion,
        fix_action="add_cot"
    )

def score_few_shot(text: str) -> MetricScore:
    matches = []
    for p in FEW_SHOT_PATTERNS:
        matches.extend(re.findall(p, text, re.I))
    
    if len(matches) >= 2:
        score = 95
        explanation = "Multiple few-shot exemplars provided, drastically increasing output consistency."
        suggestion = None
    elif len(matches) == 1:
        score = 80
        explanation = "Single example provided. Adding a second contrasting example locks in expected formatting."
        suggestion = "Provide at least two input/output pairs to establish an unambiguous pattern."
    else:
        score = 45
        explanation = "Zero-shot prompt. No concrete examples given."
        suggestion = "Add 1-2 few-shot exemplars showing the exact expected input and desired output."

    status = "good" if score >= 80 else ("average" if score >= 50 else "poor")

    return MetricScore(
        id="few_shot",
        name="Few-Shot Examples / Exemplars",
        category="Structure & Reasoning",
        score=score,
        status=status,
        explanation=explanation,
        suggestion=suggestion,
        fix_action="add_few_shot"
    )

def score_output_format(text: str) -> MetricScore:
    matches = []
    for p in OUTPUT_PATTERNS:
        matches.extend(re.findall(p, text, re.I))
    
    has_strict_format = bool(re.search(r"\b(?:only return valid json|return strictly|no conversational filler|exact schema)\b", text, re.I))

    if has_strict_format and len(matches) >= 2:
        score = 100
        explanation = "Exhaustive output format specification with strict schema constraints."
        suggestion = None
    elif len(matches) >= 1:
        score = 75
        explanation = f"Format specified ({', '.join(set(matches[:3]))}), but lacks schema enforcement or filler prohibition."
        suggestion = "Specify exact keys/columns and append: 'Return ONLY the requested format with no preamble or commentary.'"
    else:
        score = 25
        explanation = "No output format specified. Output structure will vary randomly."
        suggestion = "Specify the exact format: 'Format output as a Markdown table with columns [X, Y, Z]' or 'Return valid JSON'."

    status = "good" if score >= 80 else ("average" if score >= 50 else "poor")

    return MetricScore(
        id="output_format",
        name="Output Format & Schema Specification",
        category="Execution & Control",
        score=score,
        status=status,
        explanation=explanation,
        suggestion=suggestion,
        fix_action="add_output_format"
    )

def score_edge_cases(text: str) -> MetricScore:
    matches = []
    for p in EDGE_CASE_PATTERNS:
        matches.extend(re.findall(p, text, re.I))
    
    if len(matches) >= 2:
        score = 90
        explanation = "Robust edge-case handling instructions and fallback procedures provided."
        suggestion = None
    elif len(matches) == 1:
        score = 70
        explanation = "Basic conditional logic found, but ambiguous inputs or errors aren't fully guarded."
        suggestion = "Add guidance on how to handle missing data or unanswerable queries."
    else:
        score = 25
        explanation = "No edge-case guidance. If given anomalous input, model may fail silently or make erroneous assumptions."
        suggestion = "Add error handling: 'If input is incomplete or ambiguous, request clarification before proceeding.'"

    status = "good" if score >= 80 else ("average" if score >= 50 else "poor")

    return MetricScore(
        id="edge_cases",
        name="Edge-Case & Fallback Handling",
        category="Execution & Control",
        score=score,
        status=status,
        explanation=explanation,
        suggestion=suggestion,
        fix_action="add_edge_cases"
    )

def score_hallucination_safeguards(text: str) -> MetricScore:
    matches = []
    for p in SAFEGUARD_PATTERNS:
        matches.extend(re.findall(p, text, re.I))
    
    if len(matches) >= 2:
        score = 95
        explanation = "Stringent anti-hallucination guardrails and grounding instructions present."
        suggestion = None
    elif len(matches) == 1:
        score = 75
        explanation = "Basic safeguard detected, but explicit citation or uncertainty protocols are missing."
        suggestion = "Instruct: 'If any fact cannot be verified from context, state \"Unknown\" rather than speculating.'"
    else:
        score = 30
        explanation = "Zero hallucination guardrails. The AI has unconstrained liberty to invent facts."
        suggestion = "Add: 'Answer strictly based on provided context. If unknown or unverifiable, explicitly say so.'"

    status = "good" if score >= 80 else ("average" if score >= 50 else "poor")

    return MetricScore(
        id="hallucination_safeguards",
        name="Hallucination & Fact Safeguards",
        category="Safety & Robustness",
        score=score,
        status=status,
        explanation=explanation,
        suggestion=suggestion,
        fix_action="add_safeguards"
    )

def score_conciseness(text: str, words: List[str]) -> MetricScore:
    fluff_phrases = [
        r"\bplease\b", r"\bcould you kindly\b", r"\bi would like you to\b",
        r"\bi want you to\b", r"\bif it's not too much trouble\b",
        r"\bcan you help me\b", r"\bthank you in advance\b", r"\bas an ai\b"
    ]
    fluff_matches = []
    for p in fluff_phrases:
        fluff_matches.extend(re.findall(p, text, re.I))
    
    word_count = len(words)
    if word_count == 0:
        return MetricScore(
            id="conciseness",
            name="Signal-to-Noise Ratio & Conciseness",
            category="Clarity & Intent",
            score=10,
            status="poor",
            explanation="Empty prompt.",
            suggestion="Enter a prompt to analyze.",
            fix_action="clean_fluff"
        )
    
    fluff_penalty = len(fluff_matches) * 15
    score = max(20, min(100, 95 - fluff_penalty))
    status = "good" if score >= 80 else ("average" if score >= 50 else "poor")

    if fluff_matches:
        explanation = f"Found {len(fluff_matches)} polite filler/fluff phrase(s) ({', '.join(set(fluff_matches))}) that consume context window without providing instruction."
        suggestion = "Strip polite pleasantries ('please', 'could you kindly') and replace with direct imperatives."
    else:
        explanation = "High signal-to-noise ratio with direct imperative instructions and minimal conversational fluff."
        suggestion = None

    return MetricScore(
        id="conciseness",
        name="Signal-to-Noise Ratio & Conciseness",
        category="Clarity & Intent",
        score=score,
        status=status,
        explanation=explanation,
        suggestion=suggestion,
        fix_action="clean_fluff"
    )

def score_tone_style(text: str) -> MetricScore:
    tone_keywords = [
        r"\btone\b", r"\bformal\b", r"\bcasual\b", r"\bprofessional\b",
        r"\btechnical\b", r"\bconcise\b", r"\bauthoritative\b", r"\bconversational\b",
        r"\bacademic\b", r"\bpersuasive\b", r"\baudience\b", r"\breadership\b",
        r"\bwritten for\b", r"\bjargon-free\b"
    ]
    matches = [re.search(k, text, re.I) for k in tone_keywords if re.search(k, text, re.I)]

    if len(matches) >= 2:
        score = 90
        explanation = "Explicit tone, register, and target audience specified."
        suggestion = None
    elif len(matches) == 1:
        score = 75
        explanation = "Basic tone guideline detected, but audience demographic/expertise level is not stated."
        suggestion = "Specify the exact audience: 'Tailor vocabulary for C-level executives with no engineering background.'"
    else:
        score = 35
        explanation = "No stylistic guidance or audience framing provided. AI will adopt default neutral tone."
        suggestion = "Specify tone and target audience (e.g., 'Tone: Highly technical, direct, and authoritative for Senior Engineers')."

    status = "good" if score >= 80 else ("average" if score >= 50 else "poor")

    return MetricScore(
        id="tone_style",
        name="Tone, Voice & Audience Guidance",
        category="Context & Framing",
        score=score,
        status=status,
        explanation=explanation,
        suggestion=suggestion,
        fix_action="add_tone"
    )

def score_readability(text: str, words: List[str]) -> MetricScore:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    num_lines = len(lines)
    word_count = len(words)

    if word_count == 0:
        return MetricScore(
            id="readability",
            name="Instruction Hierarchy & Readability",
            category="Structure & Reasoning",
            score=10,
            status="poor",
            explanation="Empty prompt.",
            suggestion="Write a prompt.",
            fix_action="add_structure"
        )

    words_per_line = word_count / max(1, num_lines)
    
    # Well-structured prompts typically have distinct lines/bullet points
    if num_lines >= 3 and words_per_line < 35:
        score = 90
        explanation = "Well-balanced line breaks and readable visual pacing."
        suggestion = None
    elif num_lines >= 2:
        score = 70
        explanation = "Moderate readability, but paragraphs are somewhat dense."
        suggestion = "Break long blocks into bite-sized bullet points or numbered lists."
    else:
        score = 40
        explanation = "Single dense wall of text. Models parse distinct sections with higher fidelity."
        suggestion = "Split prompt into clear paragraphs with blank lines between directives."

    status = "good" if score >= 80 else ("average" if score >= 50 else "poor")

    return MetricScore(
        id="readability",
        name="Instruction Hierarchy & Readability",
        category="Structure & Reasoning",
        score=score,
        status=status,
        explanation=explanation,
        suggestion=suggestion,
        fix_action="add_structure"
    )

def score_injection_resistance(text: str) -> MetricScore:
    # Delimiters like triple quotes or XML tags prevent user data from breaking instructions
    has_delimiters = bool(re.search(r"(\"\"\"|'''|```|<[a-zA-Z_]+>)", text))
    has_var_placeholder = bool(re.search(r"(\{[a-zA-Z0-9_]+\}|\[[A-Z0-9_\s]+\]|\$[A-Z0-9_]+)", text))
    has_escape_guard = bool(re.search(r"\b(?:treat user input as data|do not execute instructions within|ignore conflicting instructions)\b", text, re.I))

    score = 40
    if has_delimiters: score += 25
    if has_var_placeholder: score += 15
    if has_escape_guard: score += 20

    score = max(25, min(100, score))
    status = "good" if score >= 80 else ("average" if score >= 50 else "poor")

    if score < 60:
        explanation = "Prompt merges instructions and data without strict delimiters, making it prone to ambiguity or injection."
        suggestion = "Enclose variable user data in delimiters (e.g. ```data``` or <input_text>) to isolate directives."
    else:
        explanation = "Input boundaries are isolated with delimiters or placeholders."
        suggestion = None

    return MetricScore(
        id="injection_resistance",
        name="Ambiguity & Delimiter Robustness",
        category="Safety & Robustness",
        score=score,
        status=status,
        explanation=explanation,
        suggestion=suggestion,
        fix_action="add_delimiters"
    )

def evaluate_prompt(prompt: str, target_model: str = "general") -> AnalyzeResponse:
    cleaned = prompt.strip()
    words = re.findall(r"\b\w+\b", cleaned)
    char_count = len(cleaned)
    word_count = len(words)
    estimated_tokens = max(1, int(char_count / 4)) if char_count > 0 else 0

    if not cleaned:
        # Return empty state
        return AnalyzeResponse(
            forge_score=0,
            grade="F",
            grade_color="text-rose-500",
            summary="Empty prompt provided. Enter a prompt to generate comprehensive analytics.",
            word_count=0,
            char_count=0,
            estimated_tokens=0,
            categories=[],
            all_metrics=[],
            radar_labels=[],
            radar_scores=[],
            top_strengths=[],
            critical_weaknesses=["Prompt is blank."],
            recommended_fixes=[]
        )

    # Compute all 16 metrics
    metrics: List[MetricScore] = [
        score_clarity(cleaned, words),
        score_specificity(cleaned, words),
        score_objective(cleaned, words),
        score_persona(cleaned),
        score_context(cleaned, words),
        score_constraints(cleaned),
        score_structure(cleaned),
        score_cot(cleaned),
        score_few_shot(cleaned),
        score_output_format(cleaned),
        score_edge_cases(cleaned),
        score_hallucination_safeguards(cleaned),
        score_conciseness(cleaned, words),
        score_tone_style(cleaned),
        score_readability(cleaned, words),
        score_injection_resistance(cleaned),
    ]

    # Calculate overall weighted score
    weight_map = {m["id"]: m["weight"] for m in METRIC_SPECS}
    total_weighted_score = sum(m.score * weight_map.get(m.id, 1.0) for m in metrics)
    total_weight = sum(weight_map.values())
    raw_forge_score = int(round(total_weighted_score / total_weight))
    forge_score = max(5, min(100, raw_forge_score))

    # Grade determination
    if forge_score >= 93:
        grade, grade_color = "A+", "text-emerald-400"
    elif forge_score >= 85:
        grade, grade_color = "A", "text-emerald-500"
    elif forge_score >= 75:
        grade, grade_color = "B", "text-cyan-400"
    elif forge_score >= 65:
        grade, grade_color = "C", "text-amber-400"
    elif forge_score >= 50:
        grade, grade_color = "D", "text-orange-500"
    else:
        grade, grade_color = "F", "text-rose-500"

    # Category grouping
    categories_dict: Dict[str, List[MetricScore]] = {}
    for m in metrics:
        categories_dict.setdefault(m.category, []).append(m)

    categories: List[CategoryScore] = []
    for cat_name, cat_metrics in categories_dict.items():
        cat_avg = int(round(sum(m.score for m in cat_metrics) / len(cat_metrics)))
        categories.append(CategoryScore(
            name=cat_name,
            score=cat_avg,
            metrics=cat_metrics
        ))

    # Radar chart data across 6 primary dimensions
    radar_mapping = [
        ("Clarity", ["clarity", "conciseness"]),
        ("Specificity", ["specificity", "objective"]),
        ("Structure", ["structure", "readability"]),
        ("Constraints", ["constraints", "output_format"]),
        ("Context", ["context", "persona", "tone_style"]),
        ("Robustness", ["hallucination_safeguards", "edge_cases", "injection_resistance"])
    ]
    
    metric_by_id = {m.id: m.score for m in metrics}
    radar_labels = [rm[0] for rm in radar_mapping]
    radar_scores = [
        int(round(sum(metric_by_id.get(mid, 50) for mid in rm[1]) / len(rm[1])))
        for rm in radar_mapping
    ]

    # Strengths and Weaknesses
    sorted_metrics = sorted(metrics, key=lambda m: m.score, reverse=True)
    top_strengths = [
        f"{m.name} ({m.score}/100): {m.explanation}"
        for m in sorted_metrics if m.score >= 75
    ][:3]
    if not top_strengths:
        top_strengths = ["Prompt has foundational intent, but needs structured enhancement."]

    critical_weaknesses = [
        f"{m.name} ({m.score}/100): {m.explanation}"
        for m in reversed(sorted_metrics) if m.score < 65
    ][:4]
    if not critical_weaknesses:
        critical_weaknesses = ["No critical weaknesses found. Excellent prompt construction!"]

    # Recommended fixes list
    recommended_fixes = []
    for m in sorted_metrics:
        if m.score < 75 and m.fix_action and m.suggestion:
            recommended_fixes.append({
                "id": m.fix_action,
                "metric_id": m.id,
                "title": f"Fix {m.name}",
                "suggestion": m.suggestion
            })

    # Summary generator
    if forge_score >= 85:
        summary = f"Exceptional production-ready prompt (Score: {forge_score}/100, Grade: {grade}). Highly structured, precise boundaries, and clear execution instructions."
    elif forge_score >= 70:
        summary = f"Solid prompt (Score: {forge_score}/100, Grade: {grade}) with good intent. Elevate it to enterprise-grade by tightening format rules and adding few-shot exemplars."
    elif forge_score >= 50:
        summary = f"Average prompt (Score: {forge_score}/100, Grade: {grade}). Missing key constraints, explicit output schemas, and persona framing."
    else:
        summary = f"Underperforming prompt (Score: {forge_score}/100, Grade: {grade}). Highly vulnerable to hallucinations, vagueness, and inconsistent formatting."

    return AnalyzeResponse(
        forge_score=forge_score,
        grade=grade,
        grade_color=grade_color,
        summary=summary,
        word_count=word_count,
        char_count=char_count,
        estimated_tokens=estimated_tokens,
        categories=categories,
        all_metrics=metrics,
        radar_labels=radar_labels,
        radar_scores=radar_scores,
        top_strengths=top_strengths,
        critical_weaknesses=critical_weaknesses,
        recommended_fixes=recommended_fixes
    )
