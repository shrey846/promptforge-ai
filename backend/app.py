import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from .models import (
    AnalyzeRequest, AnalyzeResponse,
    OptimizeRequest, OptimizeResponse,
    QuickFixRequest, QuickFixResponse,
    TestPromptRequest, TestPromptResponse
)
from .metrics import evaluate_prompt
from .optimizers import optimize_all_models, apply_quick_fix
from .templates import get_all_templates, get_template_by_id
from .live_ai import execute_prompt_test

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="PromptForge AI API",
    description="AI-Powered Prompt Optimizer scoring on 16+ metrics with multi-model rewrites",
    version="1.0.0"
)

# Enable CORS for development flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory
static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = BASE_DIR / "templates" / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Dashboard template not found.")
    return FileResponse(str(index_file))

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "service": "PromptForge AI",
        "version": "1.0.0",
        "metrics_count": 16
    }

@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_prompt_endpoint(req: AnalyzeRequest):
    return evaluate_prompt(req.prompt, req.target_model)

@app.post("/api/optimize", response_model=OptimizeResponse)
async def optimize_prompt_endpoint(req: OptimizeRequest):
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Cannot optimize an empty prompt.")
    return optimize_all_models(req.prompt)

@app.post("/api/quick-fix", response_model=QuickFixResponse)
async def quick_fix_endpoint(req: QuickFixRequest):
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")
    fixed_text, fix_applied, explanation = apply_quick_fix(req.prompt, req.fix_id, req.extra_context)
    eval_result = evaluate_prompt(fixed_text)
    return QuickFixResponse(
        fixed_prompt=fixed_text,
        fix_applied=fix_applied,
        explanation=explanation,
        new_score=eval_result.forge_score
    )

@app.post("/api/test", response_model=TestPromptResponse)
async def test_prompt_endpoint(req: TestPromptRequest):
    return execute_prompt_test(
        prompt=req.prompt,
        model=req.model,
        provider=req.provider or "simulation",
        api_key=req.api_key
    )

@app.get("/api/templates")
async def list_templates(domain: str = None):
    templates = get_all_templates()
    if domain:
        templates = [t for t in templates if t.get("domain") == domain]
    return {"templates": templates}

@app.get("/api/templates/{template_id}")
async def get_template(template_id: str):
    t = get_template_by_id(template_id)
    if not t:
        raise HTTPException(status_code=404, detail="Template not found")
    return t
