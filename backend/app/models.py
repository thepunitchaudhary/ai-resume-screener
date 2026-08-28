from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.database import Base


class ScreeningResult(Base):
    """One row = one resume checked against one job description."""

    __tablename__ = "screening_results"

    id = Column(Integer, primary_key=True, index=True)
    candidate_name = Column(String(255), nullable=True)
    resume_filename = Column(String(255), nullable=False)
    resume_text = Column(Text, nullable=False)
    job_description = Column(Text, nullable=False)

    match_score = Column(Integer, nullable=False)          # 0-100
    strengths = Column(Text, nullable=False)                # newline-separated bullet points
    skill_gaps = Column(Text, nullable=False)                # newline-separated bullet points
    reasoning_summary = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
