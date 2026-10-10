from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models.user import User
from app.models.diet import Diet
from app.models.routine import Routine
from app.models.chat_history import ChatHistory
from app.models.doctor import Doctor
from app.models.patient_profile import PatientProfile
from app.models.doctor_availability import DoctorAvailability
from app.models.appointment import Appointment
from app.models.medical_history import MedicalHistory

from app.routes.user_routes import router as user_router
from app.routes.diet_routes import router as diet_router
from app.routes.routine_routes import router as routine_router
from app.routes.chat_routes import router as chat_router
from app.routes.doctor_routes import router as doctor_router
from app.routes.patient_profile_routes import router as patient_profile_router
from app.routes.doctor_availability_routes import router as doctor_availability_router
from app.routes.appointment_routes import router as appointment_router
from app.routes.medical_history_routes import router as medical_history_router

# Create FastAPI application
app = FastAPI(title="Medical Assistant API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(user_router)
app.include_router(diet_router)
app.include_router(routine_router)
app.include_router(chat_router)
app.include_router(doctor_router)
app.include_router(patient_profile_router)
app.include_router(doctor_availability_router)
app.include_router(appointment_router)
app.include_router(medical_history_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to the Medical Assistant API"
    }