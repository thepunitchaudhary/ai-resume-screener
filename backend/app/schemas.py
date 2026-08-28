from datetime import datetime
from pydantic import BaseModel


class ScreeningResultOut(BaseModel):
    id: int
    candidate_name: str | None
    resume_filename: str
    match_score: int
    strengths: list[str]
    skill_gaps: list[str]
    reasoning_summary: str
    created_at: datetime

    class Config:
        from_attributes = True


class ScreeningHistoryItem(BaseModel):
    id: int
    candidate_name: str | None
    resume_filename: str
    match_score: int
    created_at: datetime

    class Config:
        from_attributes = True
