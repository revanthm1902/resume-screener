import streamlit as st
import google.generativeai as genai
import pdfplumber
import pandas as pd
import json
import os
from dotenv import load_dotenv

# 1. Setup & Configuration
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Nutrabay AI Resume Screener", layout="wide")

# 2. Helper Functions
def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def analyze_resume(jd_text, resume_text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are an expert HR Recruitment Tool. 
    Analyze the Resume against the Job Description (JD).
    
    JD: {jd_text}
    Resume: {resume_text}
    
    Return ONLY a JSON object with these exact keys:
    "Candidate Name": "Extract from resume",
    "Score": (0-100 integer),
    "Strengths": ["point 1", "point 2"],
    "Gaps": ["point 1", "point 2"],
    "Recommendation": "Strong Fit" or "Moderate Fit" or "Not Fit"
    """
    
    response = model.generate_content(prompt)
    # Clean response in case AI adds markdown code blocks
    clean_json = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(clean_json)

# 3. Streamlit UI
st.title("Nutrabay AI Automation: Resume Screener")
st.markdown("Select a Problem Statement: **#1 AI Resume Screening System**")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Step 1: Paste Job Description")
    jd_input = st.text_area("Enter the JD here...", height=250)

with col2:
    st.subheader("Step 2: Upload Resumes")
    uploaded_files = st.file_uploader("Upload PDF Resumes", type="pdf", accept_multiple_files=True)

if st.button("Analyze & Rank Candidates"):
    if not jd_input or not uploaded_files:
        st.error("Please provide both a JD and at least one resume.")
    else:
        results = []
        with st.spinner("AI is analyzing resumes..."):
            for file in uploaded_files:
                resume_text = extract_text_from_pdf(file)
                try:
                    analysis = analyze_resume(jd_input, resume_text)
                    results.append(analysis)
                except Exception as e:
                    st.error(f"Error processing {file.name}: {e}")
        
        # 4. Display Results
        if results:
            df = pd.DataFrame(results)
            # Sort by Score descending
            df = df.sort_values(by="Score", ascending=False)
            
            st.subheader("📊 Candidate Ranking Leaderboard")
            st.table(df)
            
            # Option to download as CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Report as CSV", data=csv, file_name="hiring_report.csv")