# Multi-Step Reasoning Agent with Self-Checking

## Overview
This project implements a simple multi-step reasoning agent that solves structured word problems using a Planner–Executor–Verifier architecture.  
The agent reasons internally in multiple phases, validates its own solution, and only exposes a concise final answer and explanation to the user.

The focus is on agent logic and reasoning flow, not UI complexity.

---

## Architecture

The agent consists of three core phases:

### 1. Planner
- Reads the user question
- Produces a concise step-by-step plan
- Does NOT solve the problem

Example plan:
1. Read the problem  
2. Extract relevant quantities  
3. Perform calculations  
4. Format final answer  

---

### 2. Executor
- Follows the planner’s steps
- Computes intermediate results
- Produces:
  - Final answer
  - Short user-facing explanation

---

### 3. Verifier
- Checks whether the proposed answer satisfies problem constraints
- Approves or rejects the solution
- If verification fails, the agent retries planning and execution

---

## Retry Logic
- Maximum retries: 2
- If verification fails, the agent re-runs planner and executor
- If all retries fail, the agent returns status = "failed"

---

## Reasoning Safety
- Full chain-of-thought is NOT exposed to the user
- Only a short explanation is returned
- Internal plan and verification checks are included in metadata for debugging

---

## Mock LLM Design
This implementation uses a mock LLM (`call_llm`) to simulate model behavior.
The architecture is fully swappable with real LLM APIs (OpenAI, Gemini, Anthropic)
by replacing the `call_llm` function.

---

## How to Run

```bash
python agent.py
