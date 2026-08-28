from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import screening

# Creates the screening_results table if it doesn't exist yet.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Resume Screener")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to your frontend's domain before production use
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(screening.router)


@app.get("/")
def health_check():
    return {"status": "ok", "service": "ai-resume-screener"}
