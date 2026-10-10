from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.patient_profile import PatientProfile
from app.models.user import User
from app.schemas.patient_profile_schema import PatientProfileCreate


router = APIRouter()


@router.post("/patient-profile")
def create_patient_profile(
    profile: PatientProfileCreate,
    db: Session = Depends(get_db)
):

    # Check whether user exists
    user = (
        db.query(User)
        .filter(User.id == profile.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Check whether profile already exists
    existing_profile = (
        db.query(PatientProfile)
        .filter(PatientProfile.user_id == profile.user_id)
        .first()
    )

    if existing_profile:
        raise HTTPException(
            status_code=400,
            detail="Patient profile already exists"
        )

    new_profile = PatientProfile(
        user_id=profile.user_id,
        age=profile.age,
        gender=profile.gender,
        height=profile.height,
        weight=profile.weight,
        blood_group=profile.blood_group,
        allergies=profile.allergies
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return {
        "message": "Patient profile created successfully",
        "profile_id": new_profile.id,
        "user_id": new_profile.user_id,
        "age": new_profile.age,
        "gender": new_profile.gender,
        "height": new_profile.height,
        "weight": new_profile.weight,
        "blood_group": new_profile.blood_group,
        "allergies": new_profile.allergies
    }


@router.get("/patient-profile/{user_id}")
def get_patient_profile(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    profile = (
        db.query(PatientProfile)
        .filter(PatientProfile.user_id == user_id)
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found"
        )

    return {
        "profile_id": profile.id,
        "user_id": profile.user_id,
        "age": profile.age,
        "gender": profile.gender,
        "height": profile.height,
        "weight": profile.weight,
        "blood_group": profile.blood_group,
        "allergies": profile.allergies
    }


@router.put("/patient-profile/{user_id}")
def update_patient_profile(
    user_id: int,
    profile_data: PatientProfileCreate,
    db: Session = Depends(get_db)
):

    profile = (
        db.query(PatientProfile)
        .filter(PatientProfile.user_id == user_id)
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found"
        )

    if profile_data.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="This profile does not belong to this user"
        )

    profile.age = profile_data.age
    profile.gender = profile_data.gender
    profile.height = profile_data.height
    profile.weight = profile_data.weight
    profile.blood_group = profile_data.blood_group
    profile.allergies = profile_data.allergies

    db.commit()
    db.refresh(profile)

    return {
        "message": "Patient profile updated successfully",
        "profile_id": profile.id,
        "user_id": profile.user_id,
        "age": profile.age,
        "gender": profile.gender,
        "height": profile.height,
        "weight": profile.weight,
        "blood_group": profile.blood_group,
        "allergies": profile.allergies
    }


@router.delete("/patient-profile/{user_id}")
def delete_patient_profile(
    user_id: int,
    db: Session = Depends(get_db)
):

    profile = (
        db.query(PatientProfile)
        .filter(PatientProfile.user_id == user_id)
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found"
        )

    db.delete(profile)
    db.commit()

    return {
        "message": "Patient profile deleted successfully",
        "user_id": user_id
    }