import smtplib
import time
from email.mime.text import MIMEText

# ---------- CHANGE THESE ----------
SENDER_EMAIL = "suji270306@gmail.com"
APP_PASSWORD = "cerx autf vvni ltal"
# ----------------------------------

def send_email(to_email, subject, body):
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER_EMAIL, APP_PASSWORD)
    server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
    server.quit()


# ---------- EMAIL TEMPLATES ----------

def application_received_mail(candidate_email):
    subject = "✅ Application Received – AI Resume Screening System"

    body = f"""
    <h2>Dear Candidate,</h2>

    <p>Thank you for applying through the <b>AI Resume Screening System</b>.</p>

    <p>Your application has been successfully received and is currently under automated review by our AI screening process.</p>

    <p>You will receive another email within 24 hours regarding your application status.</p>

    <br>
    <p>Best Regards,<br>
    Recruitment Team</p>
    """

    send_email(candidate_email, subject, body)


def selected_mail(candidate_email):
    subject = "🎉 Congratulations! You are Shortlisted"

    body = f"""
    <h2>Congratulations!</h2>

    <p>We are pleased to inform you that your profile has been <b>shortlisted</b> based on our AI resume screening process.</p>

    <p>Our recruitment team will contact you soon for the next steps in the hiring process.</p>

    <br>
    <p>Best Regards,<br>
    Recruitment Team</p>
    """

    send_email(candidate_email, subject, body)


def rejected_mail(candidate_email):
    subject = "Application Update – AI Resume Screening"

    body = f"""
    <h2>Dear Candidate,</h2>

    <p>Thank you for taking the time to apply.</p>

    <p>After careful evaluation by our AI screening system, your profile does not match the current job requirements.</p>

    <p>We encourage you to apply for future opportunities that match your skills.</p>

    <br>
    <p>We wish you all the best in your career journey.</p>

    <p>Best Regards,<br>
    Recruitment Team</p>
    """

    send_email(candidate_email, subject, body)


# ---------- DELAYED MAIL LOGIC ----------

def delayed_email(candidate_email, score):
    # wait 24 hours
    time.sleep(86400)

    if score >= 70:
        selected_mail(candidate_email)
    else:
        rejected_mail(candidate_email)