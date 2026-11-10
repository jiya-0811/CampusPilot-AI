
import os
import requests
import streamlit as st
from pypdf import PdfReader

st.set_page_config(
    page_title="CampusPilot AI",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
.main {background: #f7f9fc;}
.hero {
    padding: 1.3rem 1.5rem;
    border-radius: 18px;
    background: linear-gradient(120deg,#14213d,#3656a8);
    color: white;
}
.hero h1 {color:white; margin-bottom:.2rem;}
.small-muted {color:#687386;}
div.stButton > button {
    border-radius:10px;
    font-weight:600;
}
</style>
""", unsafe_allow_html=True)


# Extract text from uploaded resume
def extract_resume(uploaded_file):
    if uploaded_file is None:
        return ""

    name = uploaded_file.name.lower()

    if name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    return uploaded_file.getvalue().decode(
        "utf-8", errors="ignore"
    )


# Generate response using Gemini API
def gemini_generate(prompt, api_key, model):

    url = (
        f"https://generativelanguage.googleapis.com/"
        f"v1beta/models/{model}:generateContent"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 1800
        }
    }

    response = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key
        },
        json=payload,
        timeout=60
    )

    if response.status_code != 200:
        try:
            detail = response.json().get(
                "error", {}
            ).get("message", response.text)
        except Exception:
            detail = response.text

        raise RuntimeError(
            f"Gemini API error ({response.status_code}): {detail}"
        )

    data = response.json()

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError(
            "Gemini returned an unexpected response. Please try again."
        )


# Build AI prompt
def run_ai(task, context, api_key, model):

    prompt = f"""
You are CampusPilot AI, a practical and supportive
campus placement mentor.

Give clear, structured and realistic advice
for an Indian undergraduate student.

Do not invent achievements, skills, scores or experience.
If information is missing, mention it.

TASK:
{task}

STUDENT / RESUME CONTEXT:
{context}

Output in readable Markdown.
Be specific, concise and actionable.
"""

    return gemini_generate(prompt, api_key, model)


# Application Header
st.markdown("""
<div class="hero">
    <h1>🎓 CampusPilot AI</h1>
    <p>Your GenAI-powered placement preparation companion</p>
</div>
""", unsafe_allow_html=True)


# Sidebar configuration
with st.sidebar:

    st.header("⚙️ Configuration")

    try:
        default_api_key = st.secrets.get(
            "GEMINI_API_KEY",
            os.getenv("GEMINI_API_KEY", "")
        )
    except Exception:
        default_api_key = os.getenv(
            "GEMINI_API_KEY", ""
        )

    api_key = st.text_input(
        "Google Gemini API key",
        value=default_api_key,
        type="password",
        help="Enter your Google AI Studio API key."
    )

    model = st.selectbox(
        "Gemini model",
        ["gemini-3.8-flash"],
        index=0
    )

    st.caption(
        "Your API key is not saved by this app. "
        "Use Streamlit Secrets for deployment."
    )

    st.divider()

    st.markdown("**How to use**")
    st.write("1. Add your Gemini API key.")
    st.write("2. Upload a PDF or TXT resume.")
    st.write("3. Choose an AI tool.")
    st.write("4. Generate your results.")


# User Profile
col1, col2 = st.columns([1.25, 1])

with col1:

    st.subheader("📄 Your Profile")

    uploaded = st.file_uploader(
        "Upload resume (PDF or TXT)",
        type=["pdf", "txt"]
    )

    try:
        resume_text = extract_resume(uploaded)
    except Exception as e:
        resume_text = ""
        st.error(f"Could not read resume: {e}")

    if resume_text:
        st.success(
            f"Resume loaded: {len(resume_text)} characters"
        )

        with st.expander("Preview extracted resume text"):
            st.text(resume_text[:5000])

    else:
        st.info(
            "No resume uploaded? You can still use "
            "the interview generator by entering your role."
        )


with col2:

    st.subheader("🎯 Target Role")

    role = st.text_input(
        "Role you're preparing for",
        placeholder="e.g. Java Full Stack Developer"
    )

    jd = st.text_area(
        "Paste job description (optional)",
        height=145,
        placeholder="Paste the job description here..."
    )


st.divider()

# Five AI Modules
tabs = st.tabs([
    "Resume Analyzer",
    "JD Skill Matcher",
    "Interview Questions",
    "Answer Evaluator",
    "Study Planner"
])


# Common AI generation function
def generate_button(label, task, context, key):

    if st.button(
        label,
        key=key,
        use_container_width=True
    ):

        if not api_key:
            st.error(
                "Please add your Gemini API key in the sidebar."
            )

        elif not context.strip():
            st.warning(
                "Please provide your resume or relevant information."
            )

        else:
            with st.spinner("CampusPilot AI is thinking..."):

                try:
                    result = run_ai(
                        task,
                        context,
                        api_key,
                        model
                    )

                    st.markdown(result)

                except Exception as e:
                    st.error(str(e))


# Module 1: Resume Analyzer
with tabs[0]:

    st.markdown(
        "Identify strengths, gaps and improvements in your resume."
    )

    context = f"""
Target role: {role}

Resume:
{resume_text}
"""

    generate_button(
        "Analyze my resume",
        """
Review this resume for campus placement.

Give:
1. Overall assessment
2. Strongest points
3. Missing or weak sections
4. ATS-friendly improvements
5. Three prioritized actions

Do not fabricate details.
""",
        context,
        "resume_btn"
    )


# Module 2: JD Matcher
with tabs[1]:

    st.markdown(
        "Compare your resume with a job description."
    )

    context = f"""
Target role: {role}

Resume:
{resume_text}

Job description:
{jd}
"""

    generate_button(
        "Match resume with job description",
        """
Compare the resume with the job description.

Provide:
1. Matching skills
2. Missing skills
3. Evidence from resume
4. Priority learning gaps
5. Truthful tailored summary suggestion

Do not invent experience.
""",
        context,
        "match_btn"
    )


# Module 3: Interview Questions
with tabs[2]:

    st.markdown(
        "Generate role-specific technical questions with answers."
    )

    difficulty = st.select_slider(
        "Difficulty",
        options=[
            "Beginner",
            "Intermediate",
            "Advanced"
        ],
        value="Intermediate"
    )

    count = st.selectbox(
        "Number of questions",
        [5, 10, 15],
        index=1
    )

    context = f"""
Role: {role}
Difficulty: {difficulty}
Number of questions: {count}

Resume:
{resume_text}

Job description:
{jd}
"""

    generate_button(
        "Generate interview set",
        f"""
Create {count} likely technical interview questions
for the target role at {difficulty} level.

Include:
1. Interview question
2. Concise model answer
3. What the interviewer is testing
4. One follow-up question

Prioritize skills relevant to the role.
""",
        context,
        "questions_btn"
    )


# Module 4: Answer Evaluator
with tabs[3]:

    st.markdown(
        "Get constructive feedback on your interview answer."
    )

    question = st.text_area(
        "Interview question",
        placeholder="Explain HashMap and HashSet."
    )

    answer = st.text_area(
        "Your answer",
        placeholder="Type your answer here..."
    )

    context = f"""
Role: {role}

Question:
{question}

Candidate answer:
{answer}

Resume:
{resume_text}
"""

    generate_button(
        "Evaluate my answer",
        """
Evaluate this candidate answer.

Give:
1. Score out of 10 with reasons
2. What was correct
3. What was missing or inaccurate
4. A stronger interview-ready answer in simple English
5. One practice tip

Be encouraging but honest.
""",
        context,
        "evaluate_btn"
    )


# Module 5: Study Planner
with tabs[4]:

    st.markdown(
        "Create a realistic personalized preparation plan."
    )

    days = st.slider(
        "Preparation days available",
        1, 30, 7
    )

    hours = st.slider(
        "Study hours per day",
        1, 10, 4
    )

    context = f"""
Role: {role}

Days available: {days}
Hours per day: {hours}

Resume:
{resume_text}

Job description:
{jd}
"""

    generate_button(
        "Create my study roadmap",
        """
Build a day-wise placement preparation plan.

Include:
1. Daily topics
2. Hands-on coding tasks
3. Revision schedule
4. Mock interview checkpoints
5. Priority skill improvements

Keep the workload within the stated hours.
""",
        context,
        "plan_btn"
    )


# Footer
st.divider()

st.caption(
    "CampusPilot AI | Built using Python, Streamlit, "
    "Google Gemini API and PyPDF. "
    "AI output may contain inaccuracies; verify important facts."
)
