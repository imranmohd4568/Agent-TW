from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db.models import SessionLocal, Feedback
from agent.feedback_agent import analyze_feedback
from prometheus_client import generate_latest
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry import trace

app = FastAPI()

# # Initialize OpenTelemetry Tracing
# tracer = TracerProvider()
# tracer.add_span_processor(
#     SimpleSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4317"))
# )
# FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)
tracer = TracerProvider()
try:
    tracer.add_span_processor(
        SimpleSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4317"))
    )
    trace.set_tracer_provider(tracer)
    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)
except Exception as e:
    print(f"Failed to initialize OpenTelemetry: {e}")

Instrumentator().instrument(app).expose(app)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/feedback/")
def submit_feedback(
    patient_name: str, feedback_text: str, db: Session = Depends(get_db)
):
    feedback = Feedback(patient_name=patient_name, feedback_text=feedback_text)
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return {"message": "Feedback submitted successfully!", "id": feedback.id}


@app.get("/feedback/{feedback_id}/analyze")
def get_feedback_analysis(feedback_id: int):
    sentiment = analyze_feedback(feedback_id)
    return {"feedback_id": feedback_id, "sentiment_analysis": sentiment}


@app.get("/metrics")
def metrics():
    """Expose Prometheus metrics"""
    return generate_latest()
