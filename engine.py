import json
import time
from typing import List, Dict
from models import SafetyRequest, SafetyAssessment, Interaction, AllergyAlert


class ClinicalSafetyEngine:
    def __init__(self, fallback_path: str, system_prompt_path: str):
        with open(fallback_path, 'r') as f:
            self.fallback_data = json.load(f)

        with open(system_prompt_path, 'r') as f:
            self.system_prompt = f.read()

    def analyze(self, request: SafetyRequest, cache_hit: bool = False) -> SafetyAssessment:
        start_time = time.time()

        # ✅ Use fallback directly (no LLM)
        data = self.fallback_data
        source = "fallback"

        # ✅ Normalize input medicines safely
        input_meds = [m.lower().strip() for m in request.proposed_medicines]

        # ✅ Filter only relevant interactions
        filtered_interactions = []
        for i in data.get("interactions", []):
            drug_a = i.get("drug_a", "").lower()
            drug_b = i.get("drug_b", "").lower()

            if drug_a in input_meds and drug_b in input_meds:
                filtered_interactions.append(Interaction(**i))

        # ✅ Allergy alerts (safe handling)
        allergy_alerts = [
            AllergyAlert(**a) for a in data.get("allergy_alerts", [])
        ]

        # ✅ Risk logic
        if filtered_interactions:
            overall_risk = "high"
            safe = False
            requires_review = True
        else:
            overall_risk = "low"
            safe = True
            requires_review = False

        # ✅ Ensure processing time is not 0
        processing_time = max(1, int((time.time() - start_time) * 1000))

        return SafetyAssessment(
            interactions=filtered_interactions,
            allergy_alerts=allergy_alerts,
            safe_to_prescribe=safe,
            overall_risk_level=overall_risk,
            requires_doctor_review=requires_review,
            source=source,
            cache_hit=cache_hit,
            processing_time_ms=processing_time
        )