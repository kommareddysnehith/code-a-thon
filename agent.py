# agent.py

import os
import json

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

from prompts import EVALUATOR_PROMPT
from rubrics import THRESHOLDS

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",   # or another Groq model
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY"),
)


def evaluate_round(transcript: str, rubric: dict, threshold: float, round_name: str) -> dict:
    """
    Use Groq LLM to evaluate a round's transcript against a rubric.
    Returns a dict with scores, average, pass, summary, passed flag, and round name.
    """
    prompt = EVALUATOR_PROMPT.format(
        role="Backend Engineer",
        rubric=json.dumps(rubric, indent=2),
        transcript=transcript,
    )

    response = llm.invoke(
        [
            SystemMessage(content="You are a strict but fair interview evaluator."),
            HumanMessage(content=prompt),
        ]
    )

    result = json.loads(response.content)
    result["passed"] = result["average"] >= threshold
    result["round"] = round_name
    return result
