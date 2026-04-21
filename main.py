from fastapi import FastAPI, HTTPException
from models import SafetyRequest, SafetyAssessment
from engine import ClinicalSafetyEngine
from cache import SafetyCache
import time
app = FastAPI(title="EvoDoc Clinical Drug Safety Engine")
# Initialize components
cache = SafetyCache()
engine = ClinicalSafetyEngine(
    fallback_path="data/fallback_interactions.json",
    system_prompt_path="prompts/system_prompt.txt"
)
@app.post("/check-safety", response_model=SafetyAssessment)
async def check_safety(request: SafetyRequest):
    """
    Primary endpoint for drug interaction and allergy checking[cite: 22].
    """
    start_time = time.time()
     # 1. Check Caching Layer [cite: 29, 30]
    cached_data = cache.get(request.proposed_medicines, request.patient_history.current_medications)
    if cached_data:
        # Return cached result with cache_hit: true [cite: 32]
        cached_data["cache_hit"] = True
        cached_data["processing_time_ms"] = int((time.time() - start_time) * 1000)
        return SafetyAssessment(**cached_data)
    # 2. Process via Safety Engine
    # This involves LLM analysis of history and allergies [cite: 24, 28]
    assessment = engine.analyze(request, cache_hit=False)
    # 3. Calculate Risk Score (Bonus B) 
    # Simple logic: 40 points per high interaction, 60 per critical allergy, capped at 100.
    risk_score = 0
    risk_score += len([i for i in assessment.interactions if i.severity == "high"]) * 40
    risk_score += len([a for a in assessment.allergy_alerts if a.severity == "critical"]) * 60
    assessment.overall_risk_level = "high" if risk_score > 50 else "medium" if risk_score > 0 else "low"
    # 4. Save to Cache and Return
    cache.set(
        request.proposed_medicines, 
        request.patient_history.current_medications, 
        assessment.dict()
    )
    return assessment
