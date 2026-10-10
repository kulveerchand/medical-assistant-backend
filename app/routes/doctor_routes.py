from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.doctor import Doctor
from app.models.user import User
from app.schemas.doctor_schema import DoctorCreate


router = APIRouter()


@router.post("/doctor")
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.id == doctor.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    existing_doctor = (
        db.query(Doctor)
        .filter(Doctor.user_id == doctor.user_id)
        .first()
    )

    if existing_doctor:
        raise HTTPException(
            status_code=400,
            detail="Doctor profile already exists"
        )

    new_doctor = Doctor(
        user_id=doctor.user_id,
        full_name=doctor.full_name,
        specialization=doctor.specialization,
        qualification=doctor.qualification,
        experience=doctor.experience,
        phone=doctor.phone,
        clinic_name=doctor.clinic_name,
        clinic_address=doctor.clinic_address
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return {
        "message": "Doctor profile created successfully",
        "doctor_id": new_doctor.id,
        "user_id": new_doctor.user_id,
        "full_name": new_doctor.full_name,
        "specialization": new_doctor.specialization,
        "qualification": new_doctor.qualification,
        "experience": new_doctor.experience,
        "phone": new_doctor.phone,
        "clinic_name": new_doctor.clinic_name,
        "clinic_address": new_doctor.clinic_address
    }


@router.get("/doctor/{user_id}")
def get_doctor(
    user_id: int,
    db: Session = Depends(get_db)
):

    doctor = (
        db.query(Doctor)
        .filter(Doctor.user_id == user_id)
        .first()
    )

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor profile not found"
        )

    return {
        "doctor_id": doctor.id,
        "user_id": doctor.user_id,
        "full_name": doctor.full_name,
        "specialization": doctor.specialization,
        "qualification": doctor.qualification,
        "experience": doctor.experience,
        "phone": doctor.phone,
        "clinic_name": doctor.clinic_name,
        "clinic_address": doctor.clinic_address
    }


@router.put("/doctor/{user_id}")
def update_doctor(
    user_id: int,
    doctor_data: DoctorCreate,
    db: Session = Depends(get_db)
):

    doctor = (
        db.query(Doctor)
        .filter(Doctor.user_id == user_id)
        .first()
    )

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor profile not found"
        )

    if doctor_data.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="This doctor profile does not belong to this user"
        )

    doctor.full_name = doctor_data.full_name
    doctor.specialization = doctor_data.specialization
    doctor.qualification = doctor_data.qualification
    doctor.experience = doctor_data.experience
    doctor.phone = doctor_data.phone
    doctor.clinic_name = doctor_data.clinic_name
    doctor.clinic_address = doctor_data.clinic_address

    db.commit()
    db.refresh(doctor)

    return {
        "message": "Doctor profile updated successfully",
        "doctor_id": doctor.id,
        "user_id": doctor.user_id,
        "full_name": doctor.full_name,
        "specialization": doctor.specialization,
        "qualification": doctor.qualification,
        "experience": doctor.experience,
        "phone": doctor.phone,
        "clinic_name": doctor.clinic_name,
        "clinic_address": doctor.clinic_address
    }