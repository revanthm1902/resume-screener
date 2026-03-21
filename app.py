import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
import pandas as pd
import json
import re
import os
import io
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Nutrabay Hybrid ATS System", layout="wide")

# --- ENGINE 1: TRADITIONAL ATS (DETERMINISTIC) ---
def traditional_ats_match(jd_text, resume_text):
    jd_words = set(re.findall(r'\b[a-zA-Z0-9.-]+\b', jd_text.lower()))
    resume_words = set(re.findall(r'\b[a-zA-Z0-9.-]+\b', resume_text.lower()))
    skill_bank = {'react', 'node', 'express', 'mongodb', 'python', 'sql', 'seo', 'marketing', 'java', 'next.js', 'vercel', 'aws', 'api'}
    jd_skills = jd_words.intersection(skill_bank)
    if not jd_skills:
        return 0, [], []
        
    matched_skills = jd_skills.intersection(resume_words)
    missing_skills = jd_skills - resume_words
    score = int((len(matched_skills) / len(jd_skills)) * 100)
    return score, list(matched_skills), list(missing_skills)

# --- ENGINE 2: STANDARD AI RECRUITER (TEXT-BASED) ---
def ai_contextual_analysis(jd_text, resume_text):
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"""
    You are an expert HR Recruiter. Analyze this Resume text against the Job Description.
    Focus on CONTEXT. Does their experience level and actual work match the JD?
    
    JD: {jd_text}
    Resume: {resume_text}
    Return ONLY a JSON object with these exact keys:
    "Candidate Name": "Extract from resume",
    "AI Score": (0-100 integer representing contextual fit),
    "Strengths": ["point 1", "point 2"],
    "Gaps": ["point 1", "point 2"],
    "Recommendation": "Strong Fit" or "Moderate Fit" or "Not Fit"
    """
    response = model.generate_content(prompt)
    clean_json = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(clean_json)

# --- ENGINE 3: MULTIMODAL FALLBACK (FOR GRAPHIC RESUMES) ---
def ai_multimodal_fallback(jd_text, pdf_bytes):
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"""
    You are an expert HR Recruiter. The attached PDF is a graphical resume. 
    Read it natively and analyze it against this Job Description.

    JD: {jd_text}
    Return ONLY a JSON object with these exact keys:
    "Candidate Name": "Extract from resume",
    "AI Score": (0-100 integer representing contextual fit),
    "Strengths": ["point 1", "point 2"],
    "Gaps": ["point 1", "point 2"],
    "Recommendation": "Strong Fit" or "Moderate Fit" or "Not Fit"
    """
    response = model.generate_content([
        {'mime_type': 'application/pdf', 'data': pdf_bytes},
        prompt
    ])
    clean_json = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(clean_json)

# --- PDF EXTRACTION ---
def extract_text(file_bytes):
    text = ""
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text() + "\n"
    except Exception as e:
        pass
    return text

# --- DASHBOARD ---
st.title("Hybrid Resume Screener: ATS + AI")
st.markdown("**Combines traditional Keyword Parsing with Gemini Contextual Analysis. Features Multimodal Fallback for complex PDFs.**")

col1, col2 = st.columns([1, 1])
with col1:
    jd_input = st.text_area("Step 1: Paste Job Description", height=200)
with col2:
    uploaded_files = st.file_uploader("Step 2: Upload Resumes", type="pdf", accept_multiple_files=True)

if st.button("Run Hybrid Analysis"):
    if jd_input and uploaded_files:
        results = []
        with st.spinner("Running Dual-Engine Analysis..."):
            for file in uploaded_files:
                try:
                    file.seek(0)
                    raw_bytes = file.read()
                    extracted_text = extract_text(raw_bytes)
                
                    # FALLBACK LOGIC
                    if len(extracted_text.strip()) < 50:
                        st.toast(f"Graphic Resume detected for {file.name}. Routing to Multimodal AI...", icon="⚠️")
                        ai_data = ai_multimodal_fallback(jd_input, raw_bytes)
                        ai_data["ATS Keyword Score"] = "N/A (Graphic)"
                        ai_data["Matched Keywords"] = "N/A"
                        ai_data["Missing Keywords"] = "N/A"
                        results.append(ai_data)
                    else:
                        ats_score, matched, missing = traditional_ats_match(jd_input, extracted_text)
                        ai_data = ai_contextual_analysis(jd_input, extracted_text)
                        ai_data["ATS Keyword Score"] = f"{ats_score}%"
                        ai_data["Matched Keywords"] = ", ".join(matched) if matched else "None"
                        ai_data["Missing Keywords"] = ", ".join(missing) if missing else "None"
                        results.append(ai_data)
                except Exception as e:
                    st.error(f"Processing Error on {file.name}: {e}")
        
        if results:
            df = pd.DataFrame(results)
            cols = ["Candidate Name", "ATS Keyword Score", "AI Score", "Recommendation", "Matched Keywords", "Missing Keywords", "Strengths", "Gaps"]
            for col in cols:
                if col not in df.columns:
                    df[col] = "N/A"
            df = df[cols].sort_values(by="AI Score", ascending=False).reset_index(drop=True)
            df.index = df.index + 1
            df.index.name = "Candidate Ranking"
            st.markdown("---")
            st.subheader("🏆 Dual-Engine Leaderboard Overview")
            st.dataframe(
                df,
                column_config={
                    "AI Score": st.column_config.ProgressColumn(
                        "AI Score",
                        help="Gemini's contextual fit score",
                        format="%d",
                        min_value=0,
                        max_value=100,
                    ),
                },
                use_container_width=True
            )
            # Download to Excel
            buffer = io.BytesIO()
            df.to_excel(buffer, sheet_name='Leaderboard')
            st.download_button(
                label="📥 Download Excel Leaderboard",
                data=buffer.getvalue(),
                file_name="Candidate_Leaderboard.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            st.markdown("---")
            st.subheader("📋 Detailed Candidate Profiles")
            
            for idx, row in df.iterrows():
                fit_icon = "🟢" if "Strong" in str(row['Recommendation']) else "🟡" if "Moderate" in str(row['Recommendation']) else "🔴"
                with st.expander(f"Rank #{idx} | {fit_icon} {row['Candidate Name']} | AI Score: {row['AI Score']}/100"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown("#### ✅ Strengths")
                        if isinstance(row['Strengths'], list):
                            for s in row['Strengths']: st.markdown(f"- {s}")
                        else:
                            st.write(row['Strengths'])
                        st.markdown("#### 🎯 Matched Keywords")
                        if row['Matched Keywords'] and row['Matched Keywords'] != "None" and row['Matched Keywords'] != "N/A":
                            st.success(row['Matched Keywords'])
                        else:
                            st.info("None or N/A")
                            
                    with col_b:
                        st.markdown("#### ⚠️ Potential Gaps")
                        if isinstance(row['Gaps'], list):
                            for g in row['Gaps']: st.markdown(f"- {g}")
                        else:
                            st.write(row['Gaps'])
                            
                        st.markdown("#### 🔍 Missing Keywords")
                        if row['Missing Keywords'] and row['Missing Keywords'] != "None" and row['Missing Keywords'] != "N/A":
                            st.warning(row['Missing Keywords'])
                        else:
                            st.info("None or N/A")