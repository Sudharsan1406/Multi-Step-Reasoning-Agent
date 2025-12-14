# Multi-Step Reasoning Agent with Self-Checking

## Overview
This project implements a **Multi-Step Reasoning Agent** that solves structured word problems using a **Planner → Executor → Verifier** architecture.  
The agent reasons internally in multiple steps, validates its own solution, and exposes only a concise final answer and short explanation to the user.

The focus of this assignment is **agent design, reasoning flow, verification, and robustness**, not UI complexity.

---

## Project Structure

```
TASK-4/
│
├── agent.py        # Core agent logic (planner, executor, verifier, retry loop)
├── prompts.py      # All system prompts used by the agent
├── tests.py        # Test suite with easy and tricky cases
├── README.md       # Project documentation (this file)
```

---

## How to Run

### 1. Setup Environment
Ensure Python 3.8+ is installed.

(Optional – only if using real LLM)
```bash
pip install openai
```

### 2. Run the Agent (CLI)
```bash
python agent.py
```

Enter a question and press Enter.  
Type `exit` to quit.

### 3. Run Tests
```bash
python tests.py
```

This runs:
- Easy test cases
- Tricky / edge-case test cases  
and logs:
- Question
- Final JSON output
- Verifier result
- Retry count

---

## Where Prompts Live

All prompts are defined in **`prompts.py`**:

- `PLANNER_PROMPT` – Generates a step-by-step plan (no solving)
- `EXECUTOR_PROMPT` – Executes the plan and produces an answer
- `VERIFIER_PROMPT` – Checks correctness and constraints

Prompts are kept separate to:
- Avoid duplication
- Improve clarity
- Make the system easily swappable with real LLMs

---

## Agent Architecture

### 1. Planner
- Reads the question
- Produces a concise plan
- Does NOT solve the problem

Example:
1. Read the problem  
2. Extract relevant quantities  
3. Perform calculations  
4. Format final answer  

### 2. Executor
- Follows the planner output
- Performs calculations
- Returns:
  - Final answer
  - Short user-facing explanation

### 3. Verifier
- Re-checks the proposed answer
- Validates constraints and consistency
- Approves or rejects the solution

### Retry Logic
- Maximum retries: **2**
- If verification fails, planner and executor are retried
- If all retries fail, the agent returns `status = "failed"`

---

## Mock vs Real LLM Design

The agent supports both **mock** and **real** LLM usage.

```python
USE_REAL_LLM = False
```

- `False` → Uses mock LLM (default, safe for evaluation)
- `True` → Uses real OpenAI API

The switch happens in a single place (`call_llm`), making the design realistic and production-ready.

---

## Assumptions

- Input questions are plain English word problems
- Executor may fail on unsupported domains (handled gracefully)
- Verifier prioritizes safety over hallucination
- Not all tricky questions must succeed; failure is acceptable if handled cleanly

---

## Prompt Design Rationale

### Why this design?
- Clear separation of responsibilities
- Prevents chain-of-thought leakage
- Easier debugging and evaluation

### What didn’t work well?
- Single-step LLM calls without verification caused silent errors
- Hardcoding logic inside the main loop reduced clarity

### What would improve with more time?
- Deterministic math/time solvers in Python
- Stronger verifier with independent recomputation
- Broader domain coverage
- Better ambiguity handling

---

## Example Run Logs

### Example 1
**Question:**  
Alice has 3 red apples and twice as many green apples as red. How many apples does she have?

**Output:**
```json
{
  "answer": "9 apples",
  "status": "success",
  "reasoning_visible_to_user": "Alice has 3 red apples and 6 green apples, totaling 9.",
  "metadata": {
    "plan": "1. Read the problem\n2. Extract relevant quantities\n3. Perform calculations\n4. Format final answer",
    "checks": [
      {
        "check_name": "consistency_check",
        "passed": true,
        "details": "Answer satisfies the problem constraints."
      }
    ],
    "retries": 0
  }
}
```

---

### Example 2
**Question:**  
If a train leaves at 14:30 and arrives at 18:05, how long is the journey?

**Output:**
```json
{
  "answer": "3 hours 35 minutes",
  "status": "success",
  "reasoning_visible_to_user": "The difference between 14:30 and 18:05 is 3 hours 35 minutes.",
  "metadata": {
    "plan": "1. Read the problem\n2. Extract relevant quantities\n3. Perform calculations\n4. Format final answer",
    "checks": [
      {
        "check_name": "consistency_check",
        "passed": true,
        "details": "Answer satisfies the problem constraints."
      }
    ],
    "retries": 0
  }
}
```

---

## Final Notes
This implementation satisfies all requirements in the assignment PDF:
- Multi-step reasoning
- Self-checking verifier
- Retry mechanism
- Prompt separation
- Test coverage
- Safe reasoning exposure

The project is intentionally simple, robust, and interview-ready.
