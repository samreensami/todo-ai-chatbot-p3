@echo off
echo Starting Todo AI Chatbot Backend (Gemini)...
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
