from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ScreeningResult
from app.schemas import ScreeningResultOut, ScreeningHistoryItem
from app.services.pdf_parser import extract_text_from_pdf
from app.services.ai_screener import screen_resume_against_job
import logging
logger = logging.getLogger("uvicorn.error")

router = APIRouter(prefix="/api", tags=["screening"])

MAX_RESUME_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


@router.post("/screen", response_model=ScreeningResultOut)
async def screen_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    db: Session = Depends(get_db),
):
    if resume.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Please upload a PDF resume.")

    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")

    pdf_bytes = await resume.read()
    if len(pdf_bytes) > MAX_RESUME_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="Resume file is too large (max 5 MB).")

    try:
        resume_text = extract_text_from_pdf(pdf_bytes)
    except ValueError as parse_error:
        raise HTTPException(status_code=400, detail=str(parse_error))

    try:
        ai_result = screen_resume_against_job(resume_text, job_description)
    except Exception as ai_error:
        logger.exception("Groq screening call failed")
        raise HTTPException(
            status_code=502,
            detail=f"The AI screening service failed: {ai_error}",
        )

    saved_result = ScreeningResult(
        candidate_name=ai_result.get("candidate_name"),
        resume_filename=resume.filename,
        resume_text=resume_text,
        job_description=job_description,
        match_score=ai_result["match_score"],
        strengths="\n".join(ai_result["strengths"]),
        skill_gaps="\n".join(ai_result["skill_gaps"]),
        reasoning_summary=ai_result["reasoning_summary"],
    )
    db.add(saved_result)
    db.commit()
    db.refresh(saved_result)

    return _to_response(saved_result)


@router.get("/history", response_model=list[ScreeningHistoryItem])
def get_screening_history(db: Session = Depends(get_db)):
    results = (
        db.query(ScreeningResult)
        .order_by(ScreeningResult.created_at.desc())
        .limit(50)
        .all()
    )
    return results


@router.get("/screen/{result_id}", response_model=ScreeningResultOut)
def get_screening_by_id(result_id: int, db: Session = Depends(get_db)):
    result = db.query(ScreeningResult).filter(ScreeningResult.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Screening result not found.")
    return _to_response(result)


def _to_response(result: ScreeningResult) -> ScreeningResultOut:
    """Splits the newline-joined text fields back into lists for the API response."""
    return ScreeningResultOut(
        id=result.id,
        candidate_name=result.candidate_name,
        resume_filename=result.resume_filename,
        match_score=result.match_score,
        strengths=[line for line in result.strengths.split("\n") if line],
        skill_gaps=[line for line in result.skill_gaps.split("\n") if line],
        reasoning_summary=result.reasoning_summary,
        created_at=result.created_at,
    )
