# CareerBridge — SIH26044

Academia–Industry Collaboration Portal for Skill Mapping, Internships, and Placement.

## Quick Start (Local)

### 1. Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Seed demo data (first run)
```bash
curl -X POST http://127.0.0.1:8000/seed
```

### 3. Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## Demo Accounts

| Role | Credentials |
|------|-------------|
| Institution (AIIA) | admin@aiia.edu.in / aiia12345 |
| Institution (NIT) | admin@nit.edu.in / nit12345 |
| Industry | hr@dabur.com / industry123 |
| Academician | priya@aiia.edu.in / faculty123 |
| Student | Roll BAMS2024001, Name Arjun Verma, AIIA |
| Student | Roll CSE2021001, Name Ananya Rao, NIT |

## Production Deploy

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Set environment variable:
```
CAREERBRIDGE_AUTH_SECRET=your-production-secret
```

### Frontend
```bash
cd frontend
npm install
VITE_API_URL=https://your-api-domain.com npm run build
```
Serve `frontend/dist` with any static host (Nginx, Vercel, Netlify).

## Tech Stack
- **Frontend:** React + Vite + React Router
- **Backend:** FastAPI + SQLAlchemy
- **Database:** SQLite (careerbridge.db)

## Features
- Institute roster-verified student login
- Skill assessment questionnaire + gap analysis
- Weighted match-score internship & job matching
- Application tracking (applied → shortlisted → interview → hired)
- Industry hiring pipeline with ranked applicants
- Course & learning program recommendations
- Institution curriculum vs industry demand analytics
- Academician portal (FDPs, workshops, mentorship, research)
- Digital portfolio with document uploads
