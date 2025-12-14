import json
from agent import solve

# -------------------------------
# Easy Test Cases (5–10)
# -------------------------------
easy_questions = [
    "Alice has 3 red apples and twice as many green apples as red. How many apples does she have?",
    "If a train leaves at 14:30 and arrives at 18:05, how long is the journey?",
    "Bob has 10 candies and gives away 4. How many does he have left?",
    "A meeting lasts 60 minutes. If it starts at 09:00, when does it end?",
    "There are 5 boxes with 2 balls in each box. How many balls are there?"
]

# -------------------------------
# Tricky Test Cases (3–5)
# -------------------------------
tricky_questions = [
    # Ambiguous / multi-step
    "Alice has 5 apples. Bob has twice as many as Alice. Together, how many apples do they have?",

    # Time boundary
    "A train leaves at 23:30 and arrives at 01:00 the next day. How long is the journey?",

    # Multi-step arithmetic
    "A shop sells pens at 10 each. You buy 3 pens and pay with 50. How much change do you get?"
]

def run_tests(questions, label):
    print(f"\n===== {label} TESTS =====\n")

    for q in questions:
        result = solve(q)

        print("Question:")
        print(q)

        print("\nFinal JSON:")
        print(json.dumps(result, indent=2))

        print("\nVerifier Passed:")
        print(result["metadata"]["checks"][-1]["passed"])

        print("Retries:")
        print(result["metadata"]["retries"])

        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    run_tests(easy_questions, "EASY")
    run_tests(tricky_questions, "TRICKY")
