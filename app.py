import streamlit as st
import re

from database import Base, engine, SessionLocal
from models import User, Job, Application
from auth import hash_pass, verify_pass
from resume_parser import extract_text
from matcher import calculate_match
from email_service import application_received_mail
from scheduler import start_scheduler

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Resume Screening", layout="wide")

# ---------- START SCHEDULER ----------
start_scheduler()

# ---------- UI STYLE ----------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #1f4037, #99f2c8);
}
.main {
    background-color: rgba(0,0,0,0.75);
    padding: 30px;
    border-radius: 15px;
}
h1, h2, h3, label {
    color: white !important;
}
input, textarea {
    color: black !important;
    background-color: white !important;
}
.stButton>button {
    background-color: #00c9a7;
    color: white;
    border-radius: 8px;
    height: 45px;
    width: 100%;
    font-weight: bold;
}
section[data-testid="stSidebar"] {
    background-color: #0f2027;
}
section[data-testid="stSidebar"] * {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- DB ----------
Base.metadata.create_all(engine)
db = SessionLocal()

st.markdown("<h1 style='text-align:center;'>🤖 AI Resume Screening System</h1>", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
portal = st.sidebar.selectbox("Select Portal", ["Recruiter", "Candidate"])
action = st.sidebar.selectbox("Action", ["Login", "Signup"])

# ================= SIGNUP =================
if action == "Signup":
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.subheader(f"{portal} Signup")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):
        db.add(User(email=email, password=hash_pass(password), role=portal.lower()))
        db.commit()
        st.success("Account created successfully!")

    st.markdown('</div>', unsafe_allow_html=True)

# ================= LOGIN =================
if action == "Login":
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.subheader(f"{portal} Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = db.query(User).filter_by(email=email, role=portal.lower()).first()
        if user and verify_pass(password, user.password):
            st.session_state.user = user
            st.success("Logged in successfully!")
        else:
            st.error("Invalid credentials")

    st.markdown('</div>', unsafe_allow_html=True)

# ================= AFTER LOGIN =================
if "user" in st.session_state:
    user = st.session_state.user
    st.sidebar.write(f"Logged in as: {user.role}")

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    # -------- RECRUITER DASHBOARD --------
    if user.role == "recruiter":
        st.markdown('<div class="main">', unsafe_allow_html=True)
        st.header("Recruiter Dashboard")

        st.subheader("Post a Job")
        title = st.text_input("Job Title")
        desc = st.text_area("Job Description")

        if st.button("Post Job"):
            db.add(Job(title=title, description=desc, recruiter_id=user.id))
            db.commit()
            st.success("Job Posted Successfully!")

        st.subheader("Applicants for Your Jobs")
        jobs = db.query(Job).filter_by(recruiter_id=user.id).all()

        for job in jobs:
            st.markdown(f"### 📌 {job.title}")
            apps = db.query(Application).filter_by(job_id=job.id).all()

            if apps:
                for a in apps:
                    st.info(f"Candidate: {a.candidate_email} | Match Score: {a.score}%")
            else:
                st.warning("No applicants yet.")

            st.divider()

        st.markdown('</div>', unsafe_allow_html=True)

    # -------- CANDIDATE DASHBOARD --------
    if user.role == "candidate":
        st.markdown('<div class="main">', unsafe_allow_html=True)
        st.header("Candidate Dashboard")

        st.subheader("Available Jobs")
        jobs = db.query(Job).all()

        for j in jobs:
            st.markdown(f"### {j.title}")
            st.write(j.description)

            resume = st.file_uploader(
                "Upload Resume (PDF)",
                type="pdf",
                key=f"resume_{j.id}"
            )

            if st.button("Apply", key=f"apply_{j.id}"):
                if resume:
                    text = extract_text(resume)
                    score = calculate_match(j.description, text)
                    email_match = re.findall(r'\S+@\S+', text)

                    if email_match:
                        email = email_match[0]

                        db.add(Application(
                            job_id=j.id,
                            candidate_id=user.id,
                            candidate_email=email,
                            score=score
                        ))
                        db.commit()

                        application_received_mail(email)
                        st.success("Applied Successfully!")
                    else:
                        st.error("No email found in resume.")
                else:
                    st.error("Please upload resume.")

            st.divider()

        st.subheader("Jobs You Applied")
        apps = db.query(Application).filter_by(candidate_id=user.id).all()
        for a in apps:
            job = db.query(Job).filter_by(id=a.job_id).first()
            st.write(job.title)

        st.markdown('</div>', unsafe_allow_html=True)