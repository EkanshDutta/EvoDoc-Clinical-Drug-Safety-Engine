# EvoDoc-Clinical-Drug-Safety-Engine
This project is a backend system that analyzes drug interactions and patient safety.  It takes patient data and proposed medicines as input and returns: - drug interactions - allergy alerts - risk level - prescription safety
This project is a backend system that analyzes drug interactions and patient safety.

Description
It takes patient data and proposed medicines as input and returns:
- drug interactions
- allergy alerts
- risk level
- prescription safety

features
- Drug interaction detection
- Risk scoring system
- Deterministic fallback mechanism
- FastAPI backend
- Caching for performance

tech 
- Python
- FastAPI
- Pydantic

 note
 This system avoids using generic LLM APIs (GPT, Gemini, Claude) as per instructions.
Instead, it uses a deterministic fallback-based approach for reliable and explainable medical safety analysis.

how to run
uvicorn main:app --reload
then open
http://127.0.0.1:8000/docs
