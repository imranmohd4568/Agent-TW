from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "sqlite:///db/database.db"
Base = declarative_base()


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    feedback_text = Column(String, nullable=False)
    sentiment = Column(String, nullable=True)  # Can store sentiment analysis results
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
