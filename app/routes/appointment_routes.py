from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.appointment import Appointment
from app.models.user import User
from app.models.doctor import Doctor
from app.models.doctor_availability import DoctorAvailability
from app.schemas.appointment_schema import AppointmentCreate


router = APIRouter()


@router.post("/appointments")
def book_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db)
):

    # Check patient
    patient = (
        db.query(User)
        .filter(User.id == appointment.patient_id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # Check doctor
    doctor = (
        db.query(Doctor)
        .filter(Doctor.id == appointment.doctor_id)
        .first()
    )

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    # Check doctor's availability
    availability = (
        db.query(DoctorAvailability)
        .filter(
            DoctorAvailability.doctor_id == appointment.doctor_id,
            DoctorAvailability.day == appointment.appointment_date
        )
        .first()
    )

    # For now we only check whether doctor has availability
    # for the requested day.
    if not availability:
        raise HTTPException(
            status_code=400,
            detail="Doctor is not available on this day"
        )

    # Check if same doctor already has appointment
    existing_appointment = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == appointment.doctor_id,
            Appointment.appointment_date == appointment.appointment_date,
            Appointment.appointment_time == appointment.appointment_time,
            Appointment.status == "Booked"
        )
        .first()
    )

    if existing_appointment:
        raise HTTPException(
            status_code=400,
            detail="This time slot is already booked"
        )

    # Create appointment
    new_appointment = Appointment(
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        appointment_date=appointment.appointment_date,
        appointment_time=appointment.appointment_time,
        reason=appointment.reason,
        status="Booked"
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return {
        "message": "Appointment booked successfully",
        "appointment_id": new_appointment.id,
        "patient_id": new_appointment.patient_id,
        "doctor_id": new_appointment.doctor_id,
        "appointment_date": new_appointment.appointment_date,
        "appointment_time": new_appointment.appointment_time,
        "reason": new_appointment.reason,
        "status": new_appointment.status
    }



@router.get("/appointments/patient/{patient_id}")
def get_patient_appointments(
    patient_id: int,
    db: Session = Depends(get_db)
):

    patient = (
        db.query(User)
        .filter(User.id == patient_id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    appointments = (
        db.query(Appointment)
        .filter(Appointment.patient_id == patient_id)
        .order_by(Appointment.id.desc())
        .all()
    )

    return {
        "patient_id": patient_id,
        "appointments": [
            {
                "appointment_id": item.id,
                "doctor_id": item.doctor_id,
                "appointment_date": item.appointment_date,
                "appointment_time": item.appointment_time,
                "reason": item.reason,
                "status": item.status
            }
            for item in appointments
        ]
    }


@router.get("/appointments/doctor/{doctor_id}")
def get_doctor_appointments(
    doctor_id: int,
    db: Session = Depends(get_db)
):

    doctor = (
        db.query(Doctor)
        .filter(Doctor.id == doctor_id)
        .first()
    )

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    appointments = (
        db.query(Appointment)
        .filter(Appointment.doctor_id == doctor_id)
        .order_by(Appointment.id.desc())
        .all()
    )

    return {
        "doctor_id": doctor_id,
        "appointments": [
            {
                "appointment_id": item.id,
                "patient_id": item.patient_id,
                "appointment_date": item.appointment_date,
                "appointment_time": item.appointment_time,
                "reason": item.reason,
                "status": item.status
            }
            for item in appointments
        ]
    }


@router.put("/appointments/{appointment_id}/cancel")
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):

    appointment = (
        db.query(Appointment)
        .filter(Appointment.id == appointment_id)
        .first()
    )

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    if appointment.status == "Cancelled":
        raise HTTPException(
            status_code=400,
            detail="Appointment is already cancelled"
        )

    appointment.status = "Cancelled"

    db.commit()
    db.refresh(appointment)

    return {
        "message": "Appointment cancelled successfully",
        "appointment_id": appointment.id,
        "status": appointment.status
    }