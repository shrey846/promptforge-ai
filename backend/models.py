from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    prompt: str = Field(..., description="The prompt text to evaluate")
    target_model: Optional[str] = Field("general", description="Target model: general, chatgpt, gemini, claude")

class MetricScore(BaseModel):
    id: str
    name: str
    category: str
    score: int = Field(..., ge=0, le=100)
    status: str = Field("good", description="good, average, poor")
    explanation: str
    suggestion: Optional[str] = None
    fix_action: Optional[str] = None

class CategoryScore(BaseModel):
    name: str
    score: int
    metrics: List[MetricScore]

class AnalyzeResponse(BaseModel):
    forge_score: int = Field(..., ge=0, le=100)
    grade: str
    grade_color: str
    summary: str
    word_count: int
    char_count: int
    estimated_tokens: int
    categories: List[CategoryScore]
    all_metrics: List[MetricScore]
    radar_labels: List[str]
    radar_scores: List[int]
    top_strengths: List[str]
    critical_weaknesses: List[str]
    recommended_fixes: List[Dict[str, str]]

class OptimizeRequest(BaseModel):
    prompt: str
    model_type: str = Field("all", description="all, chatgpt, gemini, claude, universal")
    options: Optional[Dict[str, Any]] = None

class OptimizedPrompt(BaseModel):
    model: str
    model_name: str
    badge_color: str
    prompt: str
    changes: List[str]
    score_before: int
    score_after: int
    key_enhancements: List[str]

class OptimizeResponse(BaseModel):
    original_score: int
    results: Dict[str, OptimizedPrompt]

class QuickFixRequest(BaseModel):
    prompt: str
    fix_id: str
    extra_context: Optional[str] = None

class QuickFixResponse(BaseModel):
    fixed_prompt: str
    fix_applied: str
    explanation: str
    new_score: int

class TestPromptRequest(BaseModel):
    prompt: str
    model: str = "chatgpt" # chatgpt, gemini, claude
    api_key: Optional[str] = None
    provider: Optional[str] = "simulation" # simulation, openai, gemini, anthropic

class TestPromptResponse(BaseModel):
    model: str
    response: str
    latency_ms: int
    tokens_used: Optional[int] = None
    is_simulated: bool = True
