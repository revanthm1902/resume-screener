# Hybrid ATS Resume Screening System 🚀

**Live Demo:** [https://resume-screeningsystem-ai.streamlit.app/](https://resume-screeningsystem-ai.streamlit.app/)

A powerful, dual-engine Recruiter Dashboard built with Streamlit. This tool combines Traditional Applicant Tracking System (ATS) keyword matching with advanced AI contextual analysis—powered by Google's Gemini models—to help recruiters find the strongest candidate fits in a fraction of the time.

## ✨ Key Features
* **Dual-Engine Analysis**: Evaluates resumes using both deterministic keyword matching (Traditional ATS) and deep semantic contextual evaluations (AI Evaluator).
* **Multimodal Fallback**: Automatically senses non-standard or graphics-heavy PDF resumes natively using Gemini's multimodal vision features.
* **Interactive Leaderboard**: Visualizes candidates via a ranked DataFrame with an AI contextual fit score gradient.
* **Detailed Expandable Profiles**: Generates an exhaustive list of strengths, potential gaps, successfully matched skills, and missing skills.
* **Downloadable Reports**: One-click export of the AI leaderboard to an `.xlsx` Excel spreadsheet.

## 🛠️ Tech Stack
* **Frontend UI Framework**: [Streamlit](https://streamlit.io/)
* **AI & LLM Integration**: [Google Generative AI (Gemini 2.5 Flash)](https://ai.google.dev/)
* **PDF Extraction**: [PyMuPDF (fitz) ](https://pymupdf.readthedocs.io/en/latest/)
* **Data Manipulation**: [Pandas](https://pandas.pydata.org/)
* **Dummy Data Generator**: FPDF

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/ResumeScreening.git
cd ResumeScreening
```

### 2. Install dependencies
Ensure you are using Python 3.8+ and install the necessary libraries:
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
To authenticate with Google Gemini, you need an API key. Create a `.env` file in the root of the project:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
> Get your API key from [Google AI Studio](https://aistudio.google.com/).

### 4. Optional: Generate Mock Resumes
To test the ATS out of the box seamlessly, generate the mockup Indian resumes by running:
```bash
python make_resumes.py
```
This will generate PDF files directly in your workspace.

### 5. Run the Application
Start the Streamlit development server:
```bash
streamlit run app.py
```
Navigate to the `localhost` link provided in the terminal to view and interact with the application.

## 📁 Repository Structure
* `app.py`: Main Streamlit web application & logic.
* `make_resumes.py`: Script to generate fake PDFs for testing.
* `requirements.txt`: Python package dependencies.
* `.env`: (Not tracked) API keys.