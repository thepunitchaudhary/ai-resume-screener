"""
Talks to Groq's chat completion API to compare a resume against a job
description and get back a structured match score + reasoning.
"""
import json
from groq import Groq
from app.config import groq_api_key, groq_model

client = Groq(api_key=groq_api_key)

SYSTEM_PROMPT = """You are an experienced technical recruiter. You will be given
a candidate's resume text and a job description. Compare them carefully and
respond with ONLY a JSON object (no markdown, no extra text) in this exact shape:

{
  "candidate_name": "string or null if you cannot find a name",
  "match_score": integer from 0 to 100,
  "strengths": ["short bullet point", "short bullet point", ...],
  "skill_gaps": ["short bullet point", "short bullet point", ...],
  "reasoning_summary": "2-4 sentence explanation of the score"
}

Scoring guide:
- 80-100: strong match, candidate meets nearly all key requirements
- 50-79: partial match, some important gaps
- 0-49: weak match, missing most core requirements

Be specific and reference actual skills/tools/experience from the resume,
not generic statements."""


def screen_resume_against_job(resume_text: str, job_description: str) -> dict:
    user_prompt = f"""RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return the JSON object described in your instructions."""

    response = client.chat.completions.create(
        model=groq_model,
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    raw_reply = response.choices[0].message.content
    parsed_result = json.loads(raw_reply)

    # Fill in safe defaults in case the model skips an optional field
    parsed_result.setdefault("candidate_name", None)
    parsed_result.setdefault("strengths", [])
    parsed_result.setdefault("skill_gaps", [])
    parsed_result.setdefault("reasoning_summary", "")

    return parsed_result
