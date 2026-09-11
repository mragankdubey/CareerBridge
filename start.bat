@echo off
echo Starting CareerBridge...
start "CareerBridge API" cmd /k "cd /d %~dp0backend && pip install -r requirements.txt -q && uvicorn main:app --host 0.0.0.0 --port 8000"
timeout /t 3 /nobreak >nul
start "CareerBridge UI" cmd /k "cd /d %~dp0frontend && npm install && npm run dev"
echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:5173
echo Run: curl -X POST http://127.0.0.1:8000/seed
