import os
import openai
from crewai import Agent
from sqlalchemy.orm import Session
from db.models import SessionLocal, Feedback
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class FeedbackAnalyzer(Agent):  # Inheriting from CrewAI's Agent
    def __init__(self):
        super().__init__(
            name="Sentiment AI",
            role="Sentiment Analysis Expert",
            goal="Analyze patient feedback and determine sentiment",
            backstory="An AI assistant specialized in processing textual feedback to extract sentiment insights.",
        )

    def run(self, feedback_text):
        client = openai.OpenAI()  # Use the new OpenAI client instance

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze sentiment of this feedback: {feedback_text}",
                }
            ],
        )

        return response.choices[0].message.content


# Task
def analyze_feedback(feedback_id):
    db = SessionLocal()
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    db.close()

    if feedback:
        analyzer = FeedbackAnalyzer()
        sentiment = analyzer.run(feedback.feedback_text)
        return sentiment
    return "Feedback not found"
