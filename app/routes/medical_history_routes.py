from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.medical_history import MedicalHistory
from app.models.user import User
from app.schemas.medical_history_schema import MedicalHistoryCreate


router = APIRouter()




@router.post("/medical-history")
def create_medical_history(
    history: MedicalHistoryCreate,
    db: Session = Depends(get_db)
):

    patient = (
        db.query(User)
        .filter(User.id == history.patient_id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    new_history = MedicalHistory(
        patient_id=history.patient_id,
        previous_diseases=history.previous_diseases,
        current_conditions=history.current_conditions,
        allergies=history.allergies,
        previous_surgeries=history.previous_surgeries,
        notes=history.notes
    )

    db.add(new_history)
    db.commit()
    db.refresh(new_history)

    return {
        "message": "Medical history saved successfully",
        "history_id": new_history.id,
        "patient_id": new_history.patient_id,
        "previous_diseases": new_history.previous_diseases,
        "current_conditions": new_history.current_conditions,
        "allergies": new_history.allergies,
        "previous_surgeries": new_history.previous_surgeries,
        "notes": new_history.notes
    }



@router.get("/medical-history/{patient_id}")
def get_medical_history(
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

    history = (
        db.query(MedicalHistory)
        .filter(MedicalHistory.patient_id == patient_id)
        .order_by(MedicalHistory.id.desc())
        .all()
    )

    return {
        "patient_id": patient_id,
        "medical_history": [
            {
                "history_id": item.id,
                "previous_diseases": item.previous_diseases,
                "current_conditions": item.current_conditions,
                "allergies": item.allergies,
                "previous_surgeries": item.previous_surgeries,
                "notes": item.notes
            }
            for item in history
        ]
    }



@router.put("/medical-history/{history_id}")
def update_medical_history(
    history_id: int,
    history_data: MedicalHistoryCreate,
    db: Session = Depends(get_db)
):

    history = (
        db.query(MedicalHistory)
        .filter(MedicalHistory.id == history_id)
        .first()
    )

    if not history:
        raise HTTPException(
            status_code=404,
            detail="Medical history not found"
        )

    if history.patient_id != history_data.patient_id:
        raise HTTPException(
            status_code=403,
            detail="This medical history does not belong to this patient"
        )

    history.previous_diseases = history_data.previous_diseases
    history.current_conditions = history_data.current_conditions
    history.allergies = history_data.allergies
    history.previous_surgeries = history_data.previous_surgeries
    history.notes = history_data.notes

    db.commit()
    db.refresh(history)

    return {
        "message": "Medical history updated successfully",
        "history_id": history.id,
        "patient_id": history.patient_id,
        "previous_diseases": history.previous_diseases,
        "current_conditions": history.current_conditions,
        "allergies": history.allergies,
        "previous_surgeries": history.previous_surgeries,
        "notes": history.notes
    }


@router.delete("/medical-history/{history_id}")
def delete_medical_history(
    history_id: int,
    db: Session = Depends(get_db)
):

    history = (
        db.query(MedicalHistory)
        .filter(MedicalHistory.id == history_id)
        .first()
    )

    if not history:
        raise HTTPException(
            status_code=404,
            detail="Medical history not found"
        )

    db.delete(history)
    db.commit()

    return {
        "message": "Medical history deleted successfully",
        "history_id": history_id
    }