import time
import requests
from typing import Dict, Any, Tuple
from .models import TestPromptResponse

def simulate_response(prompt: str, model: str) -> str:
    prompt_snippet = prompt[:120].replace('\n', ' ')
    
    if model == "claude":
        return f"""<thinking>
1. Analyzing user input: The request focuses on "{prompt_snippet}..."
2. Structure: Identified key parameters. I will deliver a concise, high-signal response adhering to analytical best practices.
3. Edge cases: Checked for potential ambiguity; addressing primary requirements directly.
</thinking>

### Analysis & Resolution

Based on the parameters provided, here is the structured solution:

1. **Core Strategic Assessment**:
   The objective requires addressing fundamental constraints and maintaining high execution fidelity.

2. **Key Actionable Pillars**:
   - **Pillar 1: Structural Rigor** — Enforce explicit interfaces and eliminate implicit assumptions.
   - **Pillar 2: Execution Quality** — Validate intermediate states and handle boundary conditions cleanly.
   - **Pillar 3: Continuous Verification** — Implement automated feedback loops to guarantee output stability.

3. **Synthesis**:
   By aligning these factors, the operational workflow produces consistent, verifiable outcomes without unnecessary complexity."""

    elif model == "gemini":
        return f"""**Executive Summary**
Analysis of: "{prompt_snippet}..."

**Grounded Insights & Execution**
1. **Core Assessment**: The requirements have been mapped to operational goals with high factual fidelity.
2. **Implementation Strategy**:
   - *Phase 1: Architecture & Setup* — Establish baseline parameters and isolate data inputs.
   - *Phase 2: Systematic Delivery* — Process the core instructions following explicit constraints.
   - *Phase 3: Validation & Safeguards* — Ensure edge cases and boundary limits are verified.

**Next Steps & Recommendations**
- Confirm operational assumptions.
- Execute deployment phase with telemetry monitoring."""

    else: # chatgpt
        return f"""### Executive Overview
Here is the structured solution for your request:

> **Focus Area**: {prompt_snippet}...

### Key Findings & Recommendations
1. **Direct Action Plan**:
   - Step 1: Establish clear baseline parameters and eliminate ambiguous criteria.
   - Step 2: Implement the core methodology focusing on highest-impact deliverables first.
   - Step 3: Run comprehensive verification against the stated constraints.

2. **Important Considerations**:
   - Maintain rigorous documentation of key assumptions.
   - Ensure edge cases are handled before finalizing production rollout.

*Generated with simulated model environment.*"""

def execute_prompt_test(prompt: str, model: str, provider: str = "simulation", api_key: str = None) -> TestPromptResponse:
    start_time = time.time()
    
    if provider == "simulation" or not api_key:
        # Realistic slight delay to feel like a real model call
        time.sleep(0.4)
        latency = int((time.time() - start_time) * 1000)
        simulated_text = simulate_response(prompt, model)
        return TestPromptResponse(
            model=model,
            response=simulated_text,
            latency_ms=latency,
            tokens_used=len(simulated_text.split()) * 2,
            is_simulated=True
        )

    # If live API key is supplied
    try:
        if provider == "openai":
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 800
            }
            resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=20)
            data = resp.json()
            if "error" in data:
                return TestPromptResponse(
                    model=model,
                    response=f"OpenAI API Error: {data['error'].get('message', 'Unknown error')}",
                    latency_ms=int((time.time() - start_time) * 1000),
                    is_simulated=False
                )
            content = data["choices"][0]["message"]["content"]
            tokens = data.get("usage", {}).get("total_tokens", 0)
            return TestPromptResponse(
                model=model,
                response=content,
                latency_ms=int((time.time() - start_time) * 1000),
                tokens_used=tokens,
                is_simulated=False
            )

        elif provider == "gemini":
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            resp = requests.post(url, json=payload, timeout=20)
            data = resp.json()
            if "error" in data:
                return TestPromptResponse(
                    model=model,
                    response=f"Gemini API Error: {data['error'].get('message', 'Unknown error')}",
                    latency_ms=int((time.time() - start_time) * 1000),
                    is_simulated=False
                )
            content = data["candidates"][0]["content"]["parts"][0]["text"]
            return TestPromptResponse(
                model=model,
                response=content,
                latency_ms=int((time.time() - start_time) * 1000),
                tokens_used=len(content.split()) * 2,
                is_simulated=False
            )

        elif provider == "anthropic":
            headers = {
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            payload = {
                "model": "claude-3-5-haiku-20241022",
                "max_tokens": 800,
                "messages": [{"role": "user", "content": prompt}]
            }
            resp = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload, timeout=20)
            data = resp.json()
            if "error" in data:
                return TestPromptResponse(
                    model=model,
                    response=f"Anthropic API Error: {data['error'].get('message', 'Unknown error')}",
                    latency_ms=int((time.time() - start_time) * 1000),
                    is_simulated=False
                )
            content = data["content"][0]["text"]
            tokens = data.get("usage", {}).get("output_tokens", 0)
            return TestPromptResponse(
                model=model,
                response=content,
                latency_ms=int((time.time() - start_time) * 1000),
                tokens_used=tokens,
                is_simulated=False
            )

    except Exception as e:
        return TestPromptResponse(
            model=model,
            response=f"Connection Error: {str(e)}. Falling back to simulation.",
            latency_ms=int((time.time() - start_time) * 1000),
            is_simulated=True
        )

    # Fallback to simulation
    simulated_text = simulate_response(prompt, model)
    return TestPromptResponse(
        model=model,
        response=simulated_text,
        latency_ms=int((time.time() - start_time) * 1000),
        tokens_used=len(simulated_text.split()) * 2,
        is_simulated=True
    )
