# AI Resume Screener

A small full-stack app: upload a resume (PDF), paste a job description, and get
back an AI-generated match score with strengths, skill gaps, and reasoning.

**Stack:** React (Vite) · FastAPI · PostgreSQL (SQLAlchemy) · Groq API (Llama 3.3 70B)

## How it works

1. The React frontend sends the resume file + job description to the backend as `multipart/form-data`.
2. FastAPI extracts text from the PDF using `pdfplumber`.
3. The extracted resume text and job description are sent to Groq's chat completions API with a prompt that forces a structured JSON reply (score, strengths, gaps, reasoning).
4. The result is saved to PostgreSQL and returned to the frontend.
5. Past screenings are listed in a sidebar, pulled from the `/api/history` endpoint.

## Project structure

```
resume-screener/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app + CORS setup
│   │   ├── config.py             # loads env vars
│   │   ├── database.py           # SQLAlchemy engine/session
│   │   ├── models.py             # ScreeningResult table
│   │   ├── schemas.py            # Pydantic response models
│   │   ├── routers/screening.py  # /api/screen, /api/history endpoints
│   │   └── services/
│   │       ├── pdf_parser.py     # PDF -> text
│   │       └── ai_screener.py    # Groq API call + prompt
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── api.js
    │   └── components/ (UploadForm, ResultCard, HistoryList)
    ├── package.json
    └── .env.example
```

## Setup

### 1. Database

Get a free PostgreSQL instance at [neon.tech](https://neon.tech) (or run Postgres locally) and grab the connection string.

### 2. Groq API key

Sign up free at [console.groq.com](https://console.groq.com/keys) and generate an API key.

### 3. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # then fill in GROQ_API_KEY and DATABASE_URL
uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### 4. Frontend

```bash
cd frontend
npm install
cp .env.example .env          # defaults to localhost:8000, fine for local dev
npm run dev
```

Frontend runs at `http://localhost:5173`.

## Deployment

- **Backend:** Render or Railway (set the same env vars from `.env`)
- **Frontend:** Vercel (set `VITE_API_BASE_URL` to the deployed backend URL)

## Key decisions

- **Groq over OpenAI/Gemini:** fast inference, generous free tier, good for a take-home timeline.
- **`response_format: json_object`:** forces the model to return valid JSON instead of parsing free text, which is far more reliable.
- **Storing raw resume text in the DB:** makes it possible to re-run or audit a screening later without re-uploading the PDF.
- **SQLAlchemy over raw SQL:** keeps the schema in one place (`models.py`) and makes the code portable if the DB engine changes.

## Known limitations / what I'd improve with more time

- No authentication — anyone with the URL can use it.
- No support for scanned/image-based PDFs (would need OCR, e.g. `pytesseract`).
- No retry/backoff on Groq API failures.
- No pagination on the history endpoint (currently capped at 50 rows).
- Could add streaming of the AI response for a more interactive UX.
