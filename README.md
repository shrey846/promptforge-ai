# PromptForge AI ⚡

> **AI-Powered Prompt Optimizer** that scores prompts on **16+ metrics**, rewrites them for **ChatGPT, Gemini, Claude, and Universal LLMs**, and provides an interactive development studio.

---

## Key Capabilities

- **16+ Metric Evaluation Engine**:
  - *Clarity & Intent*: Clarity & Precision, Instruction Specificity, Objective Definition, Signal-to-Noise Ratio (Conciseness).
  - *Context & Framing*: Role & Persona Framing, Contextual Grounding, Tone, Voice & Audience Guidance.
  - *Structure & Reasoning*: Structural Delimiters & Formatting, Step-by-Step Elicitation (Chain-of-Thought), Few-Shot Examples, Instruction Hierarchy & Readability.
  - *Execution & Control*: Constraint & Negative Rule Definition, Output Format & Schema Precision, Edge-Case & Fallback Handling.
  - *Safety & Robustness*: Hallucination Safeguards & Fact Grounding, Ambiguity & Delimiter Robustness.
- **Model-Specific Rewriters**:
  - **ChatGPT (OpenAI GPT-4o / o1)**: Developer role framing, markdown headings, explicit output schemas, negative constraints, and step-by-step thinking.
  - **Google Gemini (1.5 / 2.0)**: Task-first instructional hierarchy, system directives, factual grounding rules, and delimiter blocks.
  - **Anthropic Claude (3.5 / 3.7 Sonnet)**: Official Anthropic XML tags (`<system>`, `<context>`, `<task>`, `<instructions>`, `<output_format>`) and `<thinking>` scratchpad.
  - **Universal Mega-Prompt**: Exhaustive cross-model prompt framework combining Role, Context, Task, Constraints, Exemplars, Output Schema, and Verification Checklist.
- **Interactive Studio UI**:
  - Dynamic radar chart (6 dimensions) + categorized 16-metric diagnostic grid.
  - Side-by-side prompt diff visualizer.
  - 1-Click Instant Auto-Fix Hub (patches missing components in seconds).
  - 20+ Production-Grade Curated Prompt Templates across 6 domains.
  - Guided Prompt Composer Wizard.
  - Test Sandbox (Simulated execution or live API calls to OpenAI, Gemini, Claude).
  - Session history and one-click Markdown export.

---

## Quick Start

### 1. Launch the Application
Run from the project root:
```bash
python run.py
```
This automatically starts the server at `http://127.0.0.1:8000` and opens your browser.

### 2. Run with Custom Host or Port
```bash
uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
```

---

## API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/analyze` | `POST` | Evaluates prompt and returns 16+ metrics, forge score, grade, radar data, and diagnostics. |
| `/api/optimize` | `POST` | Generates specialized versions for ChatGPT, Gemini, Claude, and Universal. |
| `/api/quick-fix` | `POST` | Applies a specific 1-click remediation (e.g. `add_persona`, `add_constraints`, `add_output_format`). |
| `/api/test` | `POST` | Executes prompt in sandbox (simulated or live API). |
| `/api/templates` | `GET` | Fetches curated production prompt library. |
| `/api/health` | `GET` | System health and version check. |

---

## Project Structure

```
promptforge-ai/
├── backend/
│   ├── app.py             # FastAPI entrypoint & REST endpoints
│   ├── metrics.py         # 16+ Scoring metric algorithms & diagnostics
│   ├── optimizers.py      # ChatGPT, Gemini, Claude, and Universal rewriters
│   ├── templates.py       # 20+ curated prompt templates across 6 domains
│   ├── live_ai.py         # Sandbox runner (simulation & live API calls)
│   └── models.py          # Pydantic data schemas
├── static/
│   ├── css/styles.css     # Dark-mode glassmorphic theme & diff styles
│   └── js/app.js          # Reactive state, Chart.js radar, diff engine, modals
├── templates/
│   └── index.html         # Responsive dashboard interface
├── requirements.txt       # Dependencies
├── run.py                 # Convenience launcher
└── README.md              # Documentation
```
