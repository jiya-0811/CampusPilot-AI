# CampusPilot AI – GenAI Placement Preparation Assistant

CampusPilot AI is a Generative AI web application that helps students prepare for campus placements. It uses Google's Gemini API to analyze resumes, compare resumes with job descriptions, generate role-specific interview questions, evaluate practice answers, and create study plans.

## Features
- Resume analysis with actionable improvement suggestions
- Resume vs. job description skill matching
- Role-specific interview questions and model answers
- Interview answer evaluation with score and improved answer
- Personalized day-wise study roadmap

## Tech stack
- Python
- Streamlit
- Google Gemini API (REST)
- PyPDF
- Requests

## Run locally
1. Install Python 3.10 or newer.
2. Extract this ZIP and open a terminal in the project folder.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run:
   ```bash
   streamlit run app.py
   ```
5. Get a Gemini API key from https://aistudio.google.com/app/apikey and enter it in the app sidebar.

## Deploy on Streamlit Community Cloud
1. Create a GitHub repository named `CampusPilot-AI`.
2. Upload `app.py`, `requirements.txt`, `README.md`, and `.gitignore` (the report can also be included).
3. Visit https://share.streamlit.io/ and sign in with GitHub.
4. Select **Create app**, choose your repository, branch `main`, and main file `app.py`.
5. Deploy. Open **App settings → Secrets** and add:
   ```toml
   GEMINI_API_KEY = "your_key_here"
   ```
   (The current app also accepts a key through its sidebar. Do not commit API keys to GitHub.)
6. Share the generated Streamlit app URL.

## Security
- Never commit your API key.
- For a public deployment, prefer Streamlit Secrets or environment variables.
- Do not upload sensitive personal information unless you have permission.
- AI-generated advice may be inaccurate and should be reviewed.

## Project structure
```
CampusPilot_AI/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── Project_Report.pdf
```

## Important
This is a working starter project. Actual AI generation requires a valid Gemini API key and internet access. Google API model availability and quotas may vary by account and region.
