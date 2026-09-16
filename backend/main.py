from fastapi import FastAPI
import joblib
import pandas as pd
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import SessionLocal, Application


# Load trained AI model
model = joblib.load("../complaint_priority_model.pkl")


app = FastAPI(title="Transparent India API")


# Enable frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Application request model
class ApplicationRequest(BaseModel):
    application_id: str
    citizen_name: str
    service: str
    status: str
    days_passed: int
    expected_days: int


# Create application
@app.post("/applications")
def create_application(data: ApplicationRequest):

    db = SessionLocal()

    application = Application(
        application_id=data.application_id,
        citizen_name=data.citizen_name,
        service=data.service,
        status=data.status,
        days_passed=data.days_passed,
        expected_days=data.expected_days
    )

    db.add(application)
    db.commit()
    db.refresh(application)
    db.close()

    return {
        "message": "Application created successfully",
        "application_id": application.application_id
    }


# Track application
@app.get("/applications/{application_id}")
def track_application(application_id: str):

    db = SessionLocal()

    application = (
        db.query(Application)
        .filter(
            Application.application_id == application_id
        )
        .first()
    )

    db.close()

    if not application:
        return {
            "error": "Application not found"
        }

    if application.days_passed > application.expected_days:
        delay_status = "Delayed"
    else:
        delay_status = "On Time"

    return {
        "application_id": application.application_id,
        "citizen_name": application.citizen_name,
        "service": application.service,
        "status": application.status,
        "days_passed": application.days_passed,
        "expected_days": application.expected_days,
        "delay_status": delay_status
    }


# Complaint request model
class ComplaintRequest(BaseModel):
    category: str
    department: str
    state: str
    city: str
    status: str
    pending_days: int
    escalated: str


# AI complaint priority prediction
@app.post("/predict-complaint")
def predict_complaint(data: ComplaintRequest):

    complaint = pd.DataFrame([{
        "Category": data.category,
        "Department": data.department,
        "State": data.state,
        "City": data.city,
        "Status": data.status,
        "Pending_Days": data.pending_days,
        "Escalated": data.escalated
    }])

    prediction = model.predict(complaint)

    return {
        "predicted_priority": prediction[0]
    }


# Frontend
app.mount(
    "/",
    StaticFiles(directory="../frontend", html=True),
    name="frontend"
)