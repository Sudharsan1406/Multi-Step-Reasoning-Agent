import streamlit as st
import json
from agent import solve

st.set_page_config(page_title="Multi-Step Reasoning Agent", layout="centered")

st.title("🧠 Multi-Step Reasoning Agent")
st.write("Enter a question. The agent will plan, solve, verify, and respond.")

question = st.text_area(
    "Enter your question:",
    placeholder="Example: If a train leaves at 14:30 and arrives at 18:05, how long is the journey?"
)

if st.button("Solve"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        result = solve(question)

        st.subheader("✅ Final Answer")
        st.write(result["answer"])

        st.subheader("🧾 Explanation")
        st.write(result["reasoning_visible_to_user"])

        with st.expander("🔍 Metadata (Debug Info)"):
            st.json(result["metadata"])