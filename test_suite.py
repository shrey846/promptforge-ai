"""
Automated Test Suite for PromptForge AI
"""
import sys
from pathlib import Path

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from backend.metrics import evaluate_prompt
from backend.optimizers import optimize_all_models, apply_quick_fix
from backend.templates import get_all_templates
from backend.live_ai import execute_prompt_test

def test_metrics_empty():
    res = evaluate_prompt("")
    assert res.forge_score == 0
    assert res.grade == "F"
    print("[OK] Empty prompt evaluation passed.")

def test_metrics_vague_prompt():
    prompt = "write a script that takes our logs and looks for errors and sends alerts somewhere"
    res = evaluate_prompt(prompt)
    assert res.forge_score < 60
    assert len(res.all_metrics) == 16
    assert len(res.radar_scores) == 6
    assert any(m.id == "clarity" for m in res.all_metrics)
    assert any(m.id == "constraints" for m in res.all_metrics)
    assert any(m.id == "output_format" for m in res.all_metrics)
    print(f"[OK] Vague prompt evaluation passed (Score: {res.forge_score}, Grade: {res.grade}).")

def test_metrics_high_grade_prompt():
    prompt = """<role>
You are a Principal Software Architect and Security Specialist.
</role>

<context>
We have a distributed Python FastAPI backend running in Kubernetes processing payment transactions.
</context>

<task>
Audit the authentication middleware for race conditions and token replay vulnerabilities.
</task>

<instructions>
1. Analyze the token revocation check step by step.
2. Outline 3 potential exploit scenarios.
3. If any detail is unverified, state "Requires external log review".
</instructions>

<constraints>
- Strict adherence to RFC 6749 OAuth 2.0.
- Do not output generic boilerplate or pleasantries.
- Keep response under 500 words.
</constraints>

<output_format>
- Executive Summary table with columns [Vulnerability, Severity, Exploitability].
- Concrete remediation code diff.
</output_format>"""
    res = evaluate_prompt(prompt)
    assert res.forge_score >= 80
    assert res.grade in ["A", "A+", "B"]
    print(f"[OK] High-grade prompt evaluation passed (Score: {res.forge_score}, Grade: {res.grade}).")

def test_optimizers():
    prompt = "write a python script to parse logs and send alerts if there are errors"
    res = optimize_all_models(prompt)
    
    assert "chatgpt" in res.results
    assert "gemini" in res.results
    assert "claude" in res.results
    assert "universal" in res.results
    
    chatgpt = res.results["chatgpt"]
    gemini = res.results["gemini"]
    claude = res.results["claude"]
    universal = res.results["universal"]
    
    # Assert model-specific features exist in the prompts
    assert "### Role & Persona" in chatgpt.prompt
    assert "--- SYSTEM INSTRUCTION ---" in gemini.prompt
    assert "<system>" in claude.prompt and "<thinking>" in claude.prompt
    assert "# ROLE & IDENTITY" in universal.prompt
    
    # Assert score improvements
    assert chatgpt.score_after > res.original_score
    assert gemini.score_after > res.original_score
    assert claude.score_after > res.original_score
    assert universal.score_after > res.original_score
    
    print(f"[OK] Optimizers passed. Original: {res.original_score} -> ChatGPT: {chatgpt.score_after}, Gemini: {gemini.score_after}, Claude: {claude.score_after}, Universal: {universal.score_after}")

def test_quick_fixes():
    base_prompt = "build an app"
    
    fixes = ["add_persona", "add_constraints", "add_output_format", "add_cot", "add_safeguards", "clean_fluff"]
    for f in fixes:
        fixed_text, label, exp = apply_quick_fix(base_prompt, f)
        assert len(fixed_text) > 0
        assert len(label) > 0
    print(f"[OK] Quick fixes passed ({len(fixes)} fixers verified).")

def test_templates():
    templates = get_all_templates()
    assert len(templates) >= 10
    assert any(t["domain"] == "software" for t in templates)
    assert any(t["domain"] == "marketing" for t in templates)
    assert any(t["domain"] == "business" for t in templates)
    print(f"[OK] Templates verified ({len(templates)} templates loaded).")

def test_simulation_sandbox():
    test_res = execute_prompt_test("Summarize system logs", "claude", "simulation")
    assert test_res.is_simulated is True
    assert "<thinking>" in test_res.response
    assert test_res.latency_ms >= 0
    print("[OK] Sandbox simulation passed.")

if __name__ == "__main__":
    print("\nRunning PromptForge AI Verification Suite...")
    test_metrics_empty()
    test_metrics_vague_prompt()
    test_metrics_high_grade_prompt()
    test_optimizers()
    test_quick_fixes()
    test_templates()
    test_simulation_sandbox()
    print("\n>>> ALL TESTS PASSED SUCCESSFULLY! <<<\n")
