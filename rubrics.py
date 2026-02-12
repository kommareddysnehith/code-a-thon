# rubrics.py

# Round 1 – Screening
SCREENING_RUBRIC = {
    "communication": "1=unclear, off-topic; 3=understandable, some structure; 5=very clear, structured, directly answers questions",
    "motivation": "1=weak/generic interest; 3=reasonable interest; 5=strong, role- and company-specific motivation",
    "eligibility": "1=does not meet basic requirements; 3=meets minimum; 5=clearly exceeds requirements"
}

# Round 2 – Technical
TECHNICAL_RUBRIC = {
    "technical_knowledge": "1=weak fundamentals; 3=solid basics; 5=deep, precise understanding with examples",
    "problem_solving": "1=no clear approach; 3=step-by-step reasonable; 5=structured, considers trade-offs and edge cases"
}

# Round 3 – Scenario
SCENARIO_RUBRIC = {
    "judgment": "1=unrealistic or risky; 3=practical; 5=balanced decisions considering risk, impact, context",
    "collaboration": "1=ignores others; 3=mentions team; 5=proactively aligns stakeholders, handles conflict constructively"
}

# Pass thresholds (average across competencies)
THRESHOLDS = {
    "screening": 2.5,
    "technical": 3.0,
    "scenario": 3.0,
}
