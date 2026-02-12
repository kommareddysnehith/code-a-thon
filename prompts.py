# prompts.py

SCREENING_QUESTIONS = [
    "Tell me about yourself and why you're interested in this role.",
    "What are your salary expectations and location preferences?",
    "Are you legally authorized to work in this country?",
    "What is your current notice period and when can you join?",
    "Are you open to working in a hybrid or fully remote setup?",
    "What kind of team environment do you perform best in?",
    "Briefly describe your most recent role and why you’re looking to move on."
]

TECHNICAL_QUESTIONS = [
    "Explain the difference between REST and GraphQL APIs.",
    "How would you debug a slow database query?",
    "Walk me through your approach to writing unit tests.",
    "Describe how you would design a scalable logging and monitoring setup for a production system.",
    "Explain the difference between synchronous and asynchronous programming and when you’d use each.",
    "How do you approach code reviews, both as an author and as a reviewer?",
    "Describe a challenging technical problem you solved recently. How did you approach it?"
]

SCENARIO_QUESTIONS = [
    "Your team disagrees on a technical decision. How do you handle it?",
    "You discover a security vulnerability 2 days before launch. What do you do?",
    "A critical feature is behind schedule and the stakeholder is pressuring you to cut tests. How do you respond?",
    "You join a legacy project with very little documentation. What are your first steps?",
    "A production incident occurs outside of working hours. How do you handle communication and resolution?",
    "You realize that the solution you implemented was wrong after it’s been deployed. What do you do next?"
]

EVALUATOR_PROMPT = """You are an expert interview evaluator.

Role: {role}
Rubric: {rubric}
Interview Transcript:
{transcript}

Score each competency 1-5 based on the rubric.

Output ONLY valid JSON with this structure:
{{
  "scores": {{"<competency_name>": int, "...": int}},
  "average": float,
  "pass": boolean,
  "summary": "2-3 sentence justification"
}}
"""
