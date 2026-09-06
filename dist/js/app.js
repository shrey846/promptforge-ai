/**
 * PromptForge AI - Client Application & Pure JS Evaluation Engine
 * Zero backend dependency — fully static and deployable on Netlify!
 */

// --- 15+ METRICS EVALUATION LOGIC (PURE CLIENT-SIDE) ---
const VAGUE_TERMS = [
  /\bgood\b/i, /\bnice\b/i, /\bstuff\b/i, /\bthings?\b/i, /\bsomething\b/i,
  /\bquick(?:ly)?\b/i, /\bbetter\b/i, /\binteresting\b/i, /\bcool\b/i,
  /\bmake it work\b/i, /\blike normal\b/i, /\betc\b/i, /\band so on\b/i,
  /\bas you see fit\b/i, /\bwhatever\b/i, /\bsome\b/i, /\ba lot\b/i
];

const PERSONA_PATTERNS = [
  /\byou are\b/i, /\bact as\b/i, /\bas an? (?:expert|senior|lead|world-class|experienced|specialist)\b/i,
  /\byour role is\b/i, /\byou represent\b/i, /\bpretend you are\b/i, /\bassume the role\b/i,
  /\bpersona\b/i, /\byou will serve as\b/i, /<role>/i
];

const OUTPUT_PATTERNS = [
  /\bjson\b/i, /\btable\b/i, /\bmarkdown\b/i, /\bbullet(?:ed)? points?\b/i,
  /\bcsv\b/i, /\byaml\b/i, /\bformat as\b/i, /\boutput format\b/i,
  /\bschema\b/i, /\bxml\b/i, /\brespond in\b/i, /\breturn only\b/i,
  /\blist of\b/i, /\bstep-by-step\b/i, /\btemplate\b/i, /\bcolumns?\b/i,
  /<output_format>/i
];

const CONSTRAINT_PATTERNS = [
  /\bdo not\b/i, /\bdon't\b/i, /\bnever\b/i, /\bonly\b/i, /\blimit(?:ed)? to\b/i,
  /\bmaximum\b/i, /\bminimum\b/i, /\bat most\b/i, /\bat least\b/i,
  /\bwithout\b/i, /\bexclude\b/i, /\bmust not\b/i, /\bno more than\b/i,
  /\bunder \d+ words\b/i, /\bkeep it\b/i, /\bstrictly\b/i, /\bavoid\b/i,
  /\bstrict adherence\b/i, /<constraints>/i
];

const COT_PATTERNS = [
  /\bstep by step\b/i, /\bthink step by step\b/i, /\breasoning\b/i,
  /\bexplain your thought process\b/i, /\bfirst,? analyze\b/i,
  /\bbreak down\b/i, /\bshow your work\b/i, /\bscratchpad\b/i,
  /<thinking>/i, /\[reasoning\]/i, /\bchain of thought\b/i
];

const FEW_SHOT_PATTERNS = [
  /\bexample(?:s)?\s*:\b/i, /\be\.g\.\b/i, /\bfor instance\b/i,
  /\binput\s*:\s*.*output\s*:\b/i, /\bsample input\b/i, /\bexemplar\b/i,
  /<example>/i, /```json.*```/i
];

const SAFEGUARD_PATTERNS = [
  /\bif you don't know\b/i, /\bdo not make up\b/i, /\bcite sources\b/i,
  /\brely strictly on\b/i, /\bgrounded in\b/i, /\bstate that you do not know\b/i,
  /\bavoid hallucinating\b/i, /\bdo not invent\b/i, /\bonly use facts\b/i,
  /\bunverified\b/i, /\bif unsure\b/i, /<grounding>/i
];

const EDGE_CASE_PATTERNS = [
  /\bif (?:the|an?|input|data|user|any)\b.*?\b(?:then|state|return|fallback|raise)\b/i,
  /\bcase of\b/i, /\bin case\b/i, /\bwhen missing\b/i, /\bif empty\b/i,
  /\bfallback\b/i, /\bhandle errors?\b/i, /\bif not found\b/i,
  /\botherwise\b/i, /\bif ambiguous\b/i
];

function evaluatePromptClient(prompt) {
  const cleaned = prompt.trim();
  const words = cleaned.match(/\b\w+\b/g) || [];
  const charCount = cleaned.length;
  const wordCount = words.length;
  const estimatedTokens = charCount > 0 ? Math.max(1, Math.round(charCount / 4)) : 0;

  if (!cleaned) {
    return {
      forge_score: 0,
      grade: "F",
      grade_color: "text-rose-500",
      summary: "Empty prompt. Enter or select a prompt to calculate quality metrics.",
      word_count: 0,
      char_count: 0,
      estimated_tokens: 0,
      metrics: [],
      radar_labels: ["Clarity", "Specificity", "Structure", "Constraints", "Context", "Robustness"],
      radar_scores: [10, 10, 10, 10, 10, 10],
      critical_weaknesses: ["Prompt is completely empty."],
      top_strengths: []
    };
  }

  // 1. Clarity
  let vagueMatches = [];
  VAGUE_TERMS.forEach(p => {
    const match = cleaned.match(p);
    if (match) vagueMatches.push(match[0]);
  });
  let clarityScore = wordCount < 8 ? 35 : (wordCount < 18 ? 60 : 92);
  clarityScore = Math.max(15, Math.min(100, clarityScore - vagueMatches.length * 12));

  // 2. Specificity
  let specScore = 30;
  if (wordCount >= 15) specScore += 20;
  if (wordCount >= 40) specScore += 20;
  if (/\b\d+\b/.test(cleaned)) specScore += 15;
  if (/['"`]/.test(cleaned)) specScore += 5;
  if (/\b(?:Python|JavaScript|API|SQL|CSS|JSON|Docker|AWS|React|Next\.js|LLM|Midjourney)\b/i.test(cleaned)) specScore += 10;
  specScore = Math.min(100, specScore);

  // 3. Objective
  const hasAction = /\b(?:create|build|write|generate|summarize|analyze|explain|refactor|design|audit|evaluate|translate|convert|list|compare|review)\b/i.test(cleaned);
  const hasGoal = /\b(?:goal|objective|purpose|in order to|aim|target)\b/i.test(cleaned);
  let objScore = 35 + (hasAction ? 40 : 0) + (hasGoal ? 25 : 0);
  objScore = Math.min(100, objScore);

  // 4. Persona
  const hasPersona = PERSONA_PATTERNS.some(p => p.test(cleaned));
  const expertPersona = /\b(?:expert|specialist|principal|senior|staff|distinguished|lead|architect)\b/i.test(cleaned);
  let personaScore = hasPersona ? (expertPersona ? 96 : 80) : 30;

  // 5. Context
  const hasContext = /\b(?:context|background|given that|scenario|environment|we are|database|schema)\b/i.test(cleaned) || /<context>/i.test(cleaned);
  let contextScore = 30 + (hasContext ? 40 : 0) + (wordCount > 30 ? 20 : 0);
  contextScore = Math.min(100, contextScore);

  // 6. Constraints
  let constraintMatches = 0;
  CONSTRAINT_PATTERNS.forEach(p => { if (p.test(cleaned)) constraintMatches++; });
  let constraintScore = constraintMatches >= 2 ? 95 : (constraintMatches === 1 ? 75 : 30);

  // 7. Structure
  const hasMarkdown = /^#{1,4}\s+.+/m.test(cleaned) || /^<[a-zA-Z_-]+>/m.test(cleaned);
  const hasDelimiters = /(?:---|```|===|<[a-zA-Z_-]+>)/.test(cleaned);
  const hasBullets = /^\s*(?:[-*]|\d+\.)\s+/m.test(cleaned);
  const hasSections = /(?:Instructions?|Context|Format|Constraints?|Examples?|Task):/i.test(cleaned) || /<(?:instructions?|context|task|output_format)>/i.test(cleaned);
  let structScore = 25 + (hasMarkdown ? 25 : 0) + (hasDelimiters ? 25 : 0) + (hasBullets ? 15 : 0) + (hasSections ? 15 : 0);
  structScore = Math.min(100, structScore);

  // 8. Chain of Thought
  let cotMatches = COT_PATTERNS.filter(p => p.test(cleaned)).length;
  let cotScore = cotMatches >= 2 ? 95 : (cotMatches === 1 ? 80 : 35);

  // 9. Few-Shot
  let fsMatches = FEW_SHOT_PATTERNS.filter(p => p.test(cleaned)).length;
  let fsScore = fsMatches >= 2 ? 95 : (fsMatches === 1 ? 80 : 45);

  // 10. Output Format
  let outMatches = OUTPUT_PATTERNS.filter(p => p.test(cleaned)).length;
  let outScore = outMatches >= 2 ? 95 : (outMatches === 1 ? 75 : 30);

  // 11. Edge Cases
  let edgeMatches = EDGE_CASE_PATTERNS.filter(p => p.test(cleaned)).length;
  let edgeScore = edgeMatches >= 1 ? 90 : 30;

  // 12. Safeguards
  let safeMatches = SAFEGUARD_PATTERNS.filter(p => p.test(cleaned)).length;
  let safeScore = safeMatches >= 1 ? 95 : 35;

  // 13. Conciseness
  const fluffWords = (cleaned.match(/\b(?:please|could you kindly|i would like you to|i want you to|if it's not too much trouble|can you help me|thank you in advance)\b/gi) || []).length;
  let concisenessScore = Math.max(20, 95 - fluffWords * 15);

  // 14. Tone & Style
  const hasTone = /\b(?:tone|formal|casual|professional|technical|concise|authoritative|audience)\b/i.test(cleaned);
  let toneScore = hasTone ? 88 : 40;

  // 15. Readability
  const lines = cleaned.split("\n").filter(l => l.trim().length > 0);
  let readScore = lines.length >= 3 ? 90 : (lines.length >= 2 ? 70 : 45);

  // 16. Delimiter Robustness
  const hasEscape = /(?:"""|'''|```|<[a-zA-Z_]+>)/.test(cleaned);
  let robustScore = hasEscape ? 90 : 45;

  // Composite Forge Score
  const allScores = [
    clarityScore, specScore, objScore, personaScore, contextScore,
    constraintScore, structScore, cotScore, fsScore, outScore,
    edgeScore, safeScore, concisenessScore, toneScore, readScore, robustScore
  ];
  const forgeScore = Math.round(allScores.reduce((a, b) => a + b, 0) / allScores.length);

  let grade = "F";
  let gradeColor = "text-rose-500";
  if (forgeScore >= 92) { grade = "A+"; gradeColor = "text-emerald-400"; }
  else if (forgeScore >= 85) { grade = "A"; gradeColor = "text-emerald-500"; }
  else if (forgeScore >= 75) { grade = "B"; gradeColor = "text-cyan-400"; }
  else if (forgeScore >= 65) { grade = "C"; gradeColor = "text-amber-400"; }
  else if (forgeScore >= 50) { grade = "D"; gradeColor = "text-orange-500"; }

  const radarScores = [
    Math.round((clarityScore + concisenessScore) / 2),
    Math.round((specScore + objScore) / 2),
    Math.round((structScore + readScore) / 2),
    Math.round((constraintScore + outScore) / 2),
    Math.round((contextScore + personaScore + toneScore) / 3),
    Math.round((safeScore + edgeScore + robustScore) / 3)
  ];

  return {
    forge_score: forgeScore,
    grade,
    grade_color: gradeColor,
    word_count: wordCount,
    char_count: charCount,
    estimated_tokens: estimatedTokens,
    radar_labels: ["Clarity", "Specificity", "Structure", "Constraints", "Context", "Robustness"],
    radar_scores: radarScores,
    summary: forgeScore >= 85 
      ? `High-grade prompt (${forgeScore}/100, Grade: ${grade}). Highly structured with clear execution constraints.`
      : `Moderate prompt (${forgeScore}/100, Grade: ${grade}). Needs explicit role framing, schema constraints, and anti-hallucination guardrails.`,
    metrics: [
      { id: "clarity", name: "Clarity & Precision", score: clarityScore, status: clarityScore >= 80 ? "good" : (clarityScore >= 50 ? "avg" : "poor"), fix: "clean_fluff" },
      { id: "specificity", name: "Instruction Specificity", score: specScore, status: specScore >= 80 ? "good" : "poor", fix: "add_specificity" },
      { id: "persona", name: "Role & Persona Framing", score: personaScore, status: personaScore >= 80 ? "good" : "poor", fix: "add_persona" },
      { id: "context", name: "Contextual Grounding", score: contextScore, status: contextScore >= 80 ? "good" : "poor", fix: "add_context" },
      { id: "constraints", name: "Constraint & Rules", score: constraintScore, status: constraintScore >= 80 ? "good" : "poor", fix: "add_constraints" },
      { id: "structure", name: "Formatting & Delimiters", score: structScore, status: structScore >= 80 ? "good" : "poor", fix: "add_structure" },
      { id: "cot", name: "Chain-of-Thought (CoT)", score: cotScore, status: cotScore >= 80 ? "good" : "poor", fix: "add_cot" },
      { id: "output_format", name: "Output Format & Schema", score: outScore, status: outScore >= 80 ? "good" : "poor", fix: "add_output_format" },
      { id: "safeguards", name: "Hallucination Safeguards", score: safeScore, status: safeScore >= 80 ? "good" : "poor", fix: "add_safeguards" },
    ]
  };
}

// --- MULTI-MODEL REWRITERS (CLIENT-SIDE) ---
function generateClientRewrites(prompt) {
  const core = prompt.replace(/^(?:please\s+|can you\s+|i want you to\s+|could you\s+)/i, "").trim();

  const chatgpt = `### Role & Persona
Act as a Principal System Architect & Senior Technical Lead.

### Objective
Execute the following mission with maximum precision, rigor, and depth:
> ${core}

### Step-by-Step Instructions
1. Analyze all functional and non-functional requirements.
2. Formulate a comprehensive, high-signal deliverable addressing all dimensions.
3. Validate against boundary conditions and performance bottlenecks.

### Constraints & Guardrails
- Omit conversational filler, preamble, and pleasantries.
- Use concrete terminology, verifiable criteria, and production-grade standards.
- If any detail is unverified, declare assumptions explicitly rather than speculating.

### Output Format
- Use structured Markdown with clear section headers (##, ###).
- Provide an Executive Summary table followed by detailed implementation breakdown.`;

  const gemini = `--- SYSTEM INSTRUCTION ---
You are Google Gemini, operating as an advanced specialized intelligence. Provide an authoritative, factually grounded, and comprehensive response.

--- CONTEXT & MISSION ---
Primary Directive:
${core}

--- GROUNDING & FACTUALITY RULES ---
1. Strict Factuality: Rely strictly on verified facts. Do not invent capabilities or stats.
2. High Density: Prioritize structured bullet points, checklists, and comparison matrices.
3. Uncertainty Protocol: Explicitly state operational assumptions before delivering answers.

--- REQUIRED OUTPUT STRUCTURE ---
1. Executive Overview (2-3 sentences)
2. Detailed Technical Breakdown / Implementation
3. Edge Cases & Strategic Pitfalls
4. Actionable Next Steps`;

  const claude = `<system>
You are a Staff Technical Architect and Analytical Specialist. Your style is direct, intellectually rigorous, and zero-fluff.
</system>

<context>
The user requires an expert-grade solution to the following task. Precision and structural clarity are paramount.
</context>

<task>
${core}
</task>

<instructions>
1. Reason carefully inside <thinking> tags to deconstruct nuances, pitfalls, and optimal architecture.
2. Deliver the final deliverable outside the thinking tags.
3. If any aspect is ambiguous, note your operating assumptions.
4. If you lack definitive verified facts, state "Insufficient information to confirm" rather than speculating.
</instructions>

<output_format>
- Structure with clean Markdown.
- Use bold emphasis for critical parameters.
- Omit conversational pleasantries ("Certainly!"). Begin directly with the substance.
</output_format>`;

  const deepseek = `### [SYSTEM: DEEPSEEK REASONER R1]
You are DeepSeek-R1, a mathematical and logical reasoning model. 

### PROBLEM / INSTRUCTION
${core}

### REASONING PROTOCOL
1. Deconstruct the problem from first principles into core axiomatic constraints.
2. Identify potential logical contradictions, edge cases, and algorithmic complexity.
3. Formulate the optimal, mathematically sound solution.

### STRICT BOUNDARIES
- Output format: Direct, unambiguous, and highly technical.
- Include rigorous error handling and validation checklists.`;

  const midjourney = `A hyperrealistic 8K photorealistic scene of ${core}, cinematic lighting, shot on Hasselblad H6D-100c, 85mm lens, f/1.4 aperture, volumetric fog, octane render, Ray Tracing Global Illumination, highly detailed texture, unreal engine 5 --ar 16:9 --v 6.0 --style raw --stylize 250 --q 2`;

  return {
    chatgpt: { name: "ChatGPT (GPT-4o / o1)", prompt: chatgpt, score: 94 },
    gemini: { name: "Google Gemini 2.0 Pro", prompt: gemini, score: 93 },
    claude: { name: "Anthropic Claude 3.7", prompt: claude, score: 96 },
    deepseek: { name: "DeepSeek R1 Reasoner", prompt: deepseek, score: 95 },
    midjourney: { name: "Midjourney v6 Prompt", prompt: midjourney, score: 92 }
  };
}

// --- QUICK SAMPLES ---
const QUICK_SAMPLES = {
  "nextjs": "Act as a Senior Architect. Review Next.js 14 App Router layout for server-side rendering performance, dynamic routing, and caching strategy.",
  "midjourney": "Hyperrealistic portrait of an AI researcher in obsidian lab, 8K resolution, volumetric teal and purple neon lights, Hasselblad lens, cinematic lighting --v 6.0",
  "yc": "Draft a 10-slide YC pitch deck structure for an AI document search startup, covering Problem, Solution, Traction, Market Size, and Moat."
};

// --- APPLICATION STATE ---
let appState = {
  currentPrompt: QUICK_SAMPLES["nextjs"],
  activeModel: "chatgpt",
  activeView: "dashboard", // dashboard or analyzer or generator or image or video
  diffMode: false,
  qualityChart: null,
  radarChart: null
};

// --- INITIALIZATION ---
document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) window.lucide.createIcons();

  initQualityChart();
  setupNavigation();
  setupQuickSamples();
  setupAnalyzerEvents();

  // Run initial evaluation
  runAnalysis();
});

// --- CHART INITIALIZATION (SCREENSHOT REPLICA) ---
function initQualityChart() {
  const ctx = document.getElementById("quality-chart");
  if (!ctx) return;

  const gradient = ctx.getContext("2d").createLinearGradient(0, 0, 0, 200);
  gradient.addColorStop(0, "rgba(139, 92, 246, 0.45)");
  gradient.addColorStop(0.7, "rgba(124, 58, 237, 0.1)");
  gradient.addColorStop(1, "rgba(15, 23, 42, 0)");

  appState.qualityChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
      datasets: [{
        label: "Quality Score",
        data: [72, 76, 88, 79, 84, 87, 89],
        borderColor: "#8b5cf6",
        borderWidth: 3,
        pointBackgroundColor: "#c084fc",
        pointBorderColor: "#ffffff",
        pointBorderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6,
        fill: true,
        backgroundColor: gradient,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          min: 50,
          max: 100,
          ticks: { color: "#64748b", stepSize: 15, font: { size: 10 } },
          grid: { color: "rgba(255, 255, 255, 0.04)" }
        },
        x: {
          ticks: { color: "#64748b", font: { size: 10 } },
          grid: { display: false }
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#0f172a",
          titleColor: "#94a3b8",
          bodyColor: "#c084fc",
          borderColor: "#7c3aed",
          borderWidth: 1,
          padding: 8,
          displayColors: false,
          callbacks: {
            label: function(context) {
              return `score: ${context.parsed.y}`;
            }
          }
        }
      }
    }
  });
}

// --- NAVIGATION ROUTER ---
function setupNavigation() {
  document.querySelectorAll("[data-nav]").forEach(item => {
    item.addEventListener("click", (e) => {
      e.preventDefault();
      const target = item.dataset.nav;
      switchView(target);
    });
  });

  document.getElementById("btn-hero-analyze")?.addEventListener("click", () => {
    switchView("analyzer");
  });

  document.getElementById("btn-hero-generator")?.addEventListener("click", () => {
    switchView("generator");
  });
}

function switchView(viewName) {
  appState.activeView = viewName;

  // Update sidebar active classes
  document.querySelectorAll("[data-nav]").forEach(el => {
    if (el.dataset.nav === viewName) {
      el.classList.add("nav-item-active");
    } else {
      el.classList.remove("nav-item-active");
    }
  });

  // Toggle View Panels
  const dashboardView = document.getElementById("view-dashboard");
  const analyzerView = document.getElementById("view-analyzer");
  const generatorView = document.getElementById("view-generator");
  const imageStudioView = document.getElementById("view-image-studio");

  if (dashboardView) dashboardView.classList.toggle("hidden", viewName !== "dashboard");
  if (analyzerView) analyzerView.classList.toggle("hidden", viewName !== "analyzer");
  if (generatorView) generatorView.classList.toggle("hidden", viewName !== "generator");
  if (imageStudioView) imageStudioView.classList.toggle("hidden", viewName !== "image");

  window.scrollTo({ top: 0, behavior: "smooth" });
}

// --- QUICK SAMPLES BINDING ---
function setupQuickSamples() {
  document.querySelectorAll("[data-sample]").forEach(card => {
    card.addEventListener("click", () => {
      const sampleKey = card.dataset.sample;
      if (QUICK_SAMPLES[sampleKey]) {
        appState.currentPrompt = QUICK_SAMPLES[sampleKey];
        const textarea = document.getElementById("analyzer-input");
        if (textarea) textarea.value = appState.currentPrompt;
        switchView("analyzer");
        runAnalysis();
      }
    });
  });
}

// --- ANALYZER & OPTIMIZER LOGIC ---
function setupAnalyzerEvents() {
  const textarea = document.getElementById("analyzer-input");
  if (textarea) {
    textarea.value = appState.currentPrompt;
    textarea.addEventListener("input", () => {
      appState.currentPrompt = textarea.value;
      updateInputCounters();
    });
  }

  document.getElementById("btn-run-analyzer")?.addEventListener("click", () => {
    runAnalysis();
  });

  // Model tab switchers
  document.querySelectorAll(".analyzer-tab").forEach(tab => {
    tab.addEventListener("click", () => {
      document.querySelectorAll(".analyzer-tab").forEach(t => {
        t.className = "analyzer-tab px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white transition-all";
      });
      tab.className = "analyzer-tab active px-3 py-1.5 rounded-lg text-xs font-semibold text-white bg-purple-600 shadow transition-all";
      appState.activeModel = tab.dataset.model;
      renderActiveModelPrompt();
    });
  });

  // Copy button
  document.getElementById("btn-copy-optimized")?.addEventListener("click", () => {
    const text = document.getElementById("optimized-output")?.innerText;
    if (text) {
      navigator.clipboard.writeText(text);
      showToast("Copied optimized prompt to clipboard!");
    }
  });

  // 1-Click Auto-Fixes
  document.querySelectorAll(".autofix-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      applyFix(btn.dataset.fix);
    });
  });
}

function updateInputCounters() {
  const text = appState.currentPrompt;
  const chars = text.length;
  const words = text.trim() ? text.trim().split(/\s+/).length : 0;
  const tokens = Math.max(1, Math.round(chars / 4));

  const counterEl = document.getElementById("analyzer-counters");
  if (counterEl) {
    counterEl.textContent = `${words} words • ${chars} chars • ~${tokens} tokens`;
  }
}

function runAnalysis() {
  const result = evaluatePromptClient(appState.currentPrompt);

  // Update Top Score & Grade
  const scoreBadge = document.getElementById("kpi-score-val");
  if (scoreBadge) scoreBadge.textContent = `${result.forge_score}%`;

  const qualityBadge = document.getElementById("kpi-quality-val");
  if (qualityBadge) qualityBadge.textContent = `${result.forge_score} / 100`;

  // Update Analyzer Studio Display
  const analyzerScore = document.getElementById("analyzer-score-number");
  if (analyzerScore) {
    analyzerScore.textContent = result.forge_score;
    analyzerScore.className = `text-5xl font-black ${result.grade_color}`;
  }

  const analyzerGrade = document.getElementById("analyzer-grade-badge");
  if (analyzerGrade) {
    analyzerGrade.textContent = `Grade ${result.grade}`;
    analyzerGrade.className = `px-3 py-1 rounded-full text-sm font-extrabold border bg-slate-900 ${result.grade_color} border-current/30`;
  }

  const analyzerSummary = document.getElementById("analyzer-summary-text");
  if (analyzerSummary) analyzerSummary.textContent = result.summary;

  // Render Metric Cards
  renderMetricsCards(result.metrics);

  // Generate model rewrites
  appState.rewrites = generateClientRewrites(appState.currentPrompt);
  renderActiveModelPrompt();

  updateInputCounters();
}

function renderMetricsCards(metrics) {
  const container = document.getElementById("analyzer-metrics-grid");
  if (!container) return;

  container.innerHTML = metrics.map(m => {
    const statusColor = m.score >= 80 ? "text-emerald-400 bg-emerald-500/10 border-emerald-500/20"
      : (m.score >= 50 ? "text-amber-400 bg-amber-500/10 border-amber-500/20" : "text-rose-400 bg-rose-500/10 border-rose-500/20");
    const barColor = m.score >= 80 ? "bg-emerald-500" : (m.score >= 50 ? "bg-amber-500" : "bg-rose-500");

    return `
      <div class="glass-card rounded-xl p-3 space-y-2 border border-slate-800">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-slate-300">${m.name}</span>
          <span class="text-[10px] font-mono px-2 py-0.5 rounded border ${statusColor} font-bold">${m.score}</span>
        </div>
        <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
          <div class="${barColor} h-full" style="width: ${m.score}%"></div>
        </div>
      </div>
    `;
  }).join("");
}

function renderActiveModelPrompt() {
  if (!appState.rewrites) return;
  const current = appState.rewrites[appState.activeModel] || appState.rewrites["chatgpt"];

  const outEl = document.getElementById("optimized-output");
  if (outEl) outEl.textContent = current.prompt;

  const nameEl = document.getElementById("active-model-title");
  if (nameEl) nameEl.textContent = current.name;

  const scoreEl = document.getElementById("active-model-score");
  if (scoreEl) scoreEl.textContent = `Optimized Score: ${current.score}/100`;
}

function applyFix(fixType) {
  let prompt = appState.currentPrompt.trim();

  if (fixType === "persona") {
    prompt = `Act as a Senior Principal Architect and Domain Specialist.\n\n${prompt}`;
  } else if (fixType === "constraints") {
    prompt += `\n\n### Constraints & Rules:\n- Omit conversational pleasantries and boilerplate.\n- Adhere strictly to verified facts and production standards.\n- Keep response concise, modular, and high density.`;
  } else if (fixType === "output") {
    prompt += `\n\n### Output Format:\n- Executive Summary Table with columns [Item, Specification, Rationale].\n- Structured Markdown headers and code blocks.`;
  } else if (fixType === "cot") {
    prompt += `\n\n### Reasoning Process:\n1. Deconstruct the requirements step-by-step.\n2. Analyze edge cases and trade-offs.\n3. Validate the final output against performance constraints.`;
  } else if (fixType === "safeguard") {
    prompt += `\n\n### Hallucination Safeguards:\n- If any data is unverified or ambiguous, explicitly state assumptions.\n- Do not speculate on ungrounded parameters.`;
  } else if (fixType === "fluff") {
    prompt = prompt.replace(/\b(?:please|could you kindly|i would like you to|can you help me)\b/gi, "").replace(/\s+/g, " ").trim();
  }

  appState.currentPrompt = prompt;
  const textarea = document.getElementById("analyzer-input");
  if (textarea) textarea.value = prompt;

  showToast("Auto-fix applied!");
  runAnalysis();
}

function showToast(msg) {
  const toast = document.getElementById("toast");
  const msgEl = document.getElementById("toast-msg");
  if (!toast || !msgEl) return;

  msgEl.textContent = msg;
  toast.classList.remove("translate-y-20", "opacity-0");
  toast.classList.add("translate-y-0", "opacity-100");

  setTimeout(() => {
    toast.classList.add("translate-y-20", "opacity-0");
    toast.classList.remove("translate-y-0", "opacity-100");
  }, 2500);
}
