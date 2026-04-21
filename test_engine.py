import pytest
from engine import ClinicalSafetyEngine
from models import SafetyRequest, PatientHistory

def test_fallback_mechanism():
    # Initialize engine with an invalid Ollama URL to force fallback
    engine = ClinicalSafetyEngine(
        fallback_path="data/fallback_interactions.json",
        system_prompt_path="prompts/system_prompt.txt"
    )
    engine.ollama_url = "http://localhost:9999/invalid" # Force error
    
    request = SafetyRequest(
        proposed_medicines=["Warfarin", "Aspirin"],
        patient_history=PatientHistory(
            current_medications=[],
            known_allergies=[],
            conditions=[],
            age=45,
            weight=75.0
        )
    )
    
    result = engine.analyze(request)
    assert result.source == "fallback" [cite: 53]
    assert len(result.interactions) > 0
    assert result.interactions[0].drug_a == "Warfarin"

def test_allergy_detection_logic():
    # This tests if your prompt/engine correctly identifies class-based allergies
    # e.g., Penicillin allergy vs Amoxicillin prescription
    pass