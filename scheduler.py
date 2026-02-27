from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

from database import SessionLocal
from models import Application
from email_service import selection_rejection_mail


def check_pending_mails():
    db = SessionLocal()
    applications = db.query(Application).filter_by(mail_sent=False).all()

    for app in applications:
        # ✅ 24 HOURS CONDITION
        if datetime.utcnow() - app.applied_at >= timedelta(hours=24):
            selection_rejection_mail(app.candidate_email, app.score)
            app.mail_sent = True
            db.commit()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_pending_mails, 'interval', minutes=1)
    scheduler.start()