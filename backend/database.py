from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()
engine = create_engine("sqlite:///studyapp.db")
SessionLocal = sessionmaker(bind=engine)

class UserProgress(Base):
    __tablename__ = "user_progress"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, index=True)
    subject = Column(String)
    chapter = Column(String)
    score = Column(Integer, default=0)
    streak = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
