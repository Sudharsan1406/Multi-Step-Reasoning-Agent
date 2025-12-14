# agent.py

import json
from prompts import PLANNER_PROMPT, EXECUTOR_PROMPT, VERIFIER_PROMPT

USE_REAL_LLM = False   # set True when using OpenAI


# -------------------------------------------------
# LLM Router
# -------------------------------------------------
def call_llm(prompt, input_text):
    if USE_REAL_LLM:
        return call_real_llm(prompt, input_text)
    else:
        return call_mock_llm(prompt, input_text)


# -------------------------------------------------
# Mock LLM (offline / testing)
# -------------------------------------------------
def call_mock_llm(prompt, input_text):

    # Planner
    if prompt == PLANNER_PROMPT:
        return (
            "1. Read the problem\n"
            "2. Extract relevant quantities\n"
            "3. Perform calculations\n"
            "4. Format final answer"
        )

    # Executor
    if prompt == EXECUTOR_PROMPT:
        text = input_text.lower()

        if "apple" in text:
            return json.dumps({
                "final_answer": "9 apples",
                "explanation": "Calculated total apples based on given quantities."
            })

        if "train" in text:
            return json.dumps({
                "final_answer": "3 hours 35 minutes",
                "explanation": "Computed time difference between departure and arrival."
            })

        return json.dumps({
            "final_answer": None,
            "explanation": "Unable to confidently solve this problem."
        })

    # Verifier
    if prompt == VERIFIER_PROMPT:
        if input_text:
            return json.dumps({
                "passed": True,
                "details": "Answer appears consistent with the problem."
            })

        return json.dumps({
            "passed": False,
            "details": "Answer is missing or invalid."
        })


# -------------------------------------------------
# Real LLM (OpenAI – safe & swappable)
# -------------------------------------------------
def call_real_llm(prompt, input_text):
    from openai import OpenAI
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": prompt + "\n\nIMPORTANT: Respond ONLY in valid JSON."
            },
            {"role": "user", "content": input_text}
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    # Safe JSON handling
    try:
        json.loads(content)
        return content
    except Exception:
        # Fail safely
        return json.dumps({
            "final_answer": None,
            "explanation": "LLM returned invalid JSON format."
        })


# -------------------------------------------------
# Agent Phases
# -------------------------------------------------
def planner(question):
    return call_llm(PLANNER_PROMPT, question)


def executor(question, plan):
    result = call_llm(EXECUTOR_PROMPT, question)
    return json.loads(result)


def verifier(question, answer):
    if answer is None:
        return {
            "passed": False,
            "details": "Executor did not produce a valid answer."
        }

    result = call_llm(VERIFIER_PROMPT, answer)
    return json.loads(result)


# -------------------------------------------------
# Agent Loop
# -------------------------------------------------
MAX_RETRIES = 2

def solve(question):
    retries = 0
    checks = []

    while retries <= MAX_RETRIES:
        plan = planner(question)
        execution = executor(question, plan)
        verification = verifier(question, execution["final_answer"])

        checks.append({
            "check_name": "consistency_check",
            "passed": verification["passed"],
            "details": verification["details"]
        })

        if verification["passed"]:
            return {
                "answer": execution["final_answer"],
                "status": "success",
                "reasoning_visible_to_user": execution["explanation"],
                "metadata": {
                    "plan": plan,
                    "checks": checks,
                    "retries": retries
                }
            }

        retries += 1

    return {
        "answer": None,
        "status": "failed",
        "reasoning_visible_to_user": "Unable to verify the solution.",
        "metadata": {
            "plan": plan,
            "checks": checks,
            "retries": retries
        }
    }


# -------------------------------------------------
# CLI
# -------------------------------------------------
if __name__ == "__main__":
    while True:
        q = input("Enter question (or exit): ")
        if q.lower() == "exit":
            break
        print(json.dumps(solve(q), indent=2))