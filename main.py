# =========================
# main.py - Resume Screening + Gmail Email
# SSL fix included for Windows/Anaconda
# =========================

import os
import certifi
import ssl
import smtplib
from email.message import EmailMessage
import pdfplumber
import spacy
import re

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

# =========================
# CONFIGURATION
# =========================
GMAIL_EMAIL = "suji270306@gmail.com"  # Your Gmail account
GMAIL_APP_PASSWORD = "cerx autf vvni ltal"  # 16-character App Password you generated
THRESHOLD = 70  # Match percentage threshold

# Predefined skills list
skills_list = [
    "python",
    "sql",
    "machine learning",
    "data analysis",
    "excel",
    "tableau",
    "powerbi"
]

# -------------------------
# Extract text from resume
# -------------------------
def extract_resume_text(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    return text.strip()

# -------------------------
# Extract email from resume
# -------------------------
def extract_email(text):
    pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    emails = re.findall(pattern, text)
    return emails[0] if emails else None

# -------------------------
# Skill-based matching
# -------------------------
def match_skills(resume_text, job_desc_text):
    resume_text = resume_text.lower()
    job_desc_text = job_desc_text.lower()

    matched_skills = []
    missing_skills = []

    for skill in skills_list:
        if skill in job_desc_text:
            if skill in resume_text:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

    total_required = len(matched_skills) + len(missing_skills)
    score = (len(matched_skills) / total_required * 100) if total_required > 0 else 0
    return score, matched_skills, missing_skills

# -------------------------
# Send email function using Gmail SMTP
# -------------------------
def send_email(receiver_email, status, score):
    if not receiver_email:
        print("No valid email found. Skipping email.")
        return

    if status == "SHORTLISTED":
        subject = "Interview Shortlisting Result"
        content = (
            f"Congratulations!\n\n"
            f"Your resume matched {score:.2f}% with our job requirements.\n"
            f"You have been shortlisted for the next round.\n\n"
            f"Best Regards,\nHR Team"
        )
    else:
        subject = "Application Status"
        content = (
            f"Thank you for applying.\n\n"
            f"Your resume match score was {score:.2f}%.\n"
            f"Unfortunately, you were not shortlisted this time.\n\n"
            f"Best Regards,\nHR Team"
        )

    # Create email message
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = GMAIL_EMAIL
    msg['To'] = receiver_email
    msg.set_content(content)

    try:
        # Connect to Gmail SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)
        print("Email sent successfully via Gmail SMTP")
    except Exception as e:
        print(f"Error sending email: {e}")

# =========================
# MAIN PROGRAM
# =========================

resume_file = "resumes/sample_resume.pdf"
job_desc_file = "job_description.txt"

# Read resume text
resume_text = extract_resume_text(resume_file)

# Read job description
with open(job_desc_file, "r", encoding="utf-8") as f:
    job_desc_text = f.read()

# Extract candidate email
email = extract_email(resume_text)

# Calculate match percentage
score, matched, missing = match_skills(resume_text, job_desc_text)

# Decide status
status = "SHORTLISTED" if score >= THRESHOLD else "REJECTED"

# Display results
print(f"Candidate Email: {email}")
print(f"Resume Match Score: {score:.2f}%")
print(f"Matched Skills: {matched}")
print(f"Missing Skills: {missing}")
print(f"Status: {status}")

# Send email if valid email exists
send_email(email, status, score)