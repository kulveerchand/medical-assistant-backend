from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.doctor import Doctor
from app.models.doctor_availability import DoctorAvailability
from app.schemas.doctor_availability_schema import DoctorAvailabilityCreate


router = APIRouter()


@router.post("/doctor-availability")
def create_availability(
    availability: DoctorAvailabilityCreate,
    db: Session = Depends(get_db)
):

    doctor = (
        db.query(Doctor)
        .filter(Doctor.id == availability.doctor_id)
        .first()
    )

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    new_availability = DoctorAvailability(
        doctor_id=availability.doctor_id,
        day=availability.day,
        start_time=availability.start_time,
        end_time=availability.end_time
    )

    db.add(new_availability)
    db.commit()
    db.refresh(new_availability)

    return {
        "message": "Doctor availability added successfully",
        "availability_id": new_availability.id,
        "doctor_id": new_availability.doctor_id,
        "day": new_availability.day,
        "start_time": new_availability.start_time,
        "end_time": new_availability.end_time
    }


@router.get("/doctor-availability/{doctor_id}")
def get_availability(
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

    availability = (
        db.query(DoctorAvailability)
        .filter(DoctorAvailability.doctor_id == doctor_id)
        .all()
    )

    return {
        "doctor_id": doctor_id,
        "availability": [
            {
                "availability_id": item.id,
                "day": item.day,
                "start_time": item.start_time,
                "end_time": item.end_time
            }
            for item in availability
        ]
    }


@router.put("/doctor-availability/{availability_id}")
def update_availability(
    availability_id: int,
    availability_data: DoctorAvailabilityCreate,
    db: Session = Depends(get_db)
):

    availability = (
        db.query(DoctorAvailability)
        .filter(DoctorAvailability.id == availability_id)
        .first()
    )

    if not availability:
        raise HTTPException(
            status_code=404,
            detail="Availability not found"
        )

    if availability.doctor_id != availability_data.doctor_id:
        raise HTTPException(
            status_code=403,
            detail="This availability does not belong to this doctor"
        )

    availability.day = availability_data.day
    availability.start_time = availability_data.start_time
    availability.end_time = availability_data.end_time

    db.commit()
    db.refresh(availability)

    return {
        "message": "Doctor availability updated successfully",
        "availability_id": availability.id,
        "doctor_id": availability.doctor_id,
        "day": availability.day,
        "start_time": availability.start_time,
        "end_time": availability.end_time
    }