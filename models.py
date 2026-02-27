from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    recruiter_id = Column(Integer, ForeignKey("users.id"))

class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True)

    job_id = Column(Integer, ForeignKey("jobs.id"))
    candidate_id = Column(Integer, ForeignKey("users.id"))

    candidate_email = Column(String)
    score = Column(Integer)

    applied_at = Column(DateTime, default=datetime.utcnow)
    mail_sent = Column(Boolean, default=False)