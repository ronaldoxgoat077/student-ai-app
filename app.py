import json
import os
from groq import Groq
import streamlit as st

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Student AI Study Pack", page_icon="📚")
st.title("📚 AI Exam Study Pack Generator")
st.write(
    "Select your board, class, and enter any chapter to get instant notes and a"
    " quiz."
)

col1, col2 = st.columns(2)
with col1:
    board = st.selectbox("Select Board", ["SSC", "CBSE", "ICSE"])
with col2:
    student_class = st.selectbox(
        "Select Class", ["6th", "7th", "8th", "9th", "10th", "11th", "12th"]
    )

chapter = st.text_input(
    "Enter Chapter Name", placeholder="e.g., Heredity and Evolution"
)

if st.button("Generate Study Pack 🚀", type="primary"):
  if not chapter.strip():
    st.warning("Please enter a chapter name first!")
  else:
    with st.spinner("Generating your custom study pack..."):
      prompt = f"""
            You are an expert Indian school teacher for {board} board, Class {student_class}.
            Create a detailed study pack for the chapter: "{chapter}".
            Return ONLY a valid JSON object with these exact 3 keys:
            1. "revision_notes": a list of 6 crisp bullet points.
            2. "important_questions": a list of 4 objects, each with "question" and "answer".
            3. "quiz": a list of 5 MCQs, each with "question", "options" (list of 4), and "correct_answer".
            """

      response = client.chat.completions.create(
          model="openai/gpt-oss-120b",
          messages=[{"role": "user", "content": prompt}],
          response_format={"type": "json_object"},
      )

      data = json.loads(response.choices[0].message.content)

      tab1, tab2, tab3 = st.tabs(
          ["📝 Revision Notes", "❓ Important Q&A", "🎯 Practice Quiz"]
      )

      with tab1:
        for note in data["revision_notes"]:
          st.markdown(f"- {note}")

      with tab2:
        for i, item in enumerate(data["important_questions"], 1):
          st.markdown(f"**Q{i}: {item['question']}**")
          st.info(item["answer"])

      with tab3:
        for i, q in enumerate(data["quiz"], 1):
          st.markdown(f"**{i}. {q['question']}**")
          for opt in q["options"]:
            st.write(f"• {opt}")
          with st.expander("Show Answer"):
            st.success(f"Correct Answer: {q['correct_answer']}")
