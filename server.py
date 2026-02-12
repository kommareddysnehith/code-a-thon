# server.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import uuid

from agent import evaluate_round
from prompts import (
    SCREENING_QUESTIONS,
    TECHNICAL_QUESTIONS,
    SCENARIO_QUESTIONS,
)
from rubrics import (
    SCREENING_RUBRIC,
    TECHNICAL_RUBRIC,
    SCENARIO_RUBRIC,
    THRESHOLDS,
)

app = FastAPI()

# CORS so your static front-end can call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # MVP: open; later lock to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store
interview_sessions: Dict[str, dict] = {}


class InterviewRequest(BaseModel):
    candidate_name: str


class AnswerSubmission(BaseModel):
    session_id: str
    round_name: str
    question_index: int
    answer: str


class SessionRequest(BaseModel):
    session_id: str


@app.post("/initialize-interview")
def initialize_interview(req: InterviewRequest):
    """Create a new interview session and return session ID."""
    session_id = str(uuid.uuid4())
    interview_sessions[session_id] = {
        "candidate_name": req.candidate_name,
        "screening_answers": [],
        "technical_answers": [],
        "scenario_answers": [],
        "screening_transcript": "",
        "technical_transcript": "",
        "scenario_transcript": "",
        "screening_result": None,
        "technical_result": None,
        "scenario_result": None,
        "final_decision": None,
    }
    return {"session_id": session_id, "message": "Interview session initialized"}


@app.get("/get-questions/{round_name}")
def get_questions(round_name: str):
    """Return questions for a given round."""
    rounds = {
        "screening": SCREENING_QUESTIONS,
        "technical": TECHNICAL_QUESTIONS,
        "scenario": SCENARIO_QUESTIONS,
    }
    if round_name not in rounds:
        return {"error": "Invalid round name"}

    return {
        "round": round_name,
        "questions": rounds[round_name],
        "total": len(rounds[round_name]),
    }


@app.post("/submit-answer")
def submit_answer(answer_data: AnswerSubmission):
    """Store an answer for a specific question and build transcript."""
    if answer_data.session_id not in interview_sessions:
        return {"error": "Invalid session ID"}

    session = interview_sessions[answer_data.session_id]
    round_name = answer_data.round_name

    if round_name not in ["screening", "technical", "scenario"]:
        return {"error": "Invalid round name"}

    answers_key = f"{round_name}_answers"
    transcript_key = f"{round_name}_transcript"

    # Save answer
    session[answers_key].append(
        {
            "question_index": answer_data.question_index,
            "answer": answer_data.answer,
        }
    )

    # Build transcript text
    round_questions_map = {
        "screening": SCREENING_QUESTIONS,
        "technical": TECHNICAL_QUESTIONS,
        "scenario": SCENARIO_QUESTIONS,
    }
    questions = round_questions_map[round_name]

    if answer_data.question_index == 0:
        session[transcript_key] = (
            f"Candidate: {session['candidate_name']}\n"
            f"Round: {round_name}\n\n"
        )

    q_idx = answer_data.question_index
    if q_idx < len(questions):
        session[transcript_key] += (
            f"Q{q_idx + 1}: {questions[q_idx]}\n"
            f"A{q_idx + 1}: {answer_data.answer}\n\n"
        )

    return {"status": "answer_saved", "question_index": answer_data.question_index}


@app.post("/evaluate-round")
def evaluate_round_endpoint(round_data: dict):
    """Evaluate one round based on the transcript."""
    session_id = round_data.get("session_id")
    round_name = round_data.get("round_name")

    if session_id not in interview_sessions:
        return {"error": "Invalid session ID"}

    session = interview_sessions[session_id]
    transcript_key = f"{round_name}_transcript"
    transcript = session.get(transcript_key)

    if not transcript:
        return {"error": "No transcript for this round"}

    rubric_map = {
        "screening": SCREENING_RUBRIC,
        "technical": TECHNICAL_RUBRIC,
        "scenario": SCENARIO_RUBRIC,
    }
    rubric = rubric_map.get(round_name)
    threshold = THRESHOLDS.get(round_name)

    if not rubric or threshold is None:
        return {"error": "Invalid round for evaluation"}

    result = evaluate_round(
        transcript=transcript,
        rubric=rubric,
        threshold=threshold,
        round_name=round_name,
    )

    result_key = f"{round_name}_result"
    session[result_key] = result

    return {
        "round": round_name,
        "passed": result.get("passed"),
        "average_score": result.get("average"),
        "summary": result.get("summary"),
    }


@app.post("/get-final-decision")
def get_final_decision(session_req: SessionRequest):
    """Combine round results into a final decision."""
    if session_req.session_id not in interview_sessions:
        return {"error": "Invalid session ID"}

    session = interview_sessions[session_req.session_id]
    screening = session.get("screening_result")
    technical = session.get("technical_result")
    scenario = session.get("scenario_result")

    screening_pass = screening and screening.get("passed", False)
    technical_pass = technical and technical.get("passed", False)
    scenario_pass = scenario and scenario.get("passed", False)

    if screening_pass and technical_pass and scenario_pass:
        decision = "✅ MOVE TO HUMAN PANEL (Passed all rounds)"
    elif not screening_pass:
        decision = "❌ REJECTED – failed screening"
    elif not technical_pass:
        decision = "❌ REJECTED – failed technical round"
    else:
        decision = "❌ REJECTED – failed scenario round"

    session["final_decision"] = decision

    return {
        "final_decision": decision,
        "screening_result": screening,
        "technical_result": technical,
        "scenario_result": scenario,
    }
