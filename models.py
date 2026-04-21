from pydantic import BaseModel
from typing import List

class PatientHistory(BaseModel):
    current_medications: List[str]
    known_allergies: List[str]
    conditions: List[str]
    age: int
    weight: float

class SafetyRequest(BaseModel):
    proposed_medicines: List[str]
    patient_history: PatientHistory

class Interaction(BaseModel):
    drug_a: str
    drug_b: str
    severity: str
    mechanism: str
    clinical_recommendation: str
    source_confidence: str

class AllergyAlert(BaseModel):
    medicine: str
    reason: str
    severity: str

class SafetyAssessment(BaseModel):
    interactions: List[Interaction]
    allergy_alerts: List[AllergyAlert]
    safe_to_prescribe: bool
    overall_risk_level: str
    requires_doctor_review: bool
    source: str
    cache_hit: bool
    processing_time_ms: int