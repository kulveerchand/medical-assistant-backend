from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.routine import Routine
from app.models.user import User
from app.schemas.routine_schema import RoutineCreate

router = APIRouter()

@router.post("/routine")
def create_routine(
    routine: RoutineCreate,
    db: Session = Depends(get_db)
):
    # Check whether user exists
    user = (
        db.query(User)
        .filter(User.id == routine.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    new_routine = Routine(
        user_id=routine.user_id,
        wake_up_time=routine.wake_up_time,
        exercise=routine.exercise,
        sleep_hours=routine.sleep_hours,
        activity=routine.activity,
        notes=routine.notes
    )

    db.add(new_routine)
    db.commit()
    db.refresh(new_routine)

    return {
        "message": "Daily routine saved successfully",
        "routine_id": new_routine.id,
        "user_id": new_routine.user_id,
        "wake_up_time": new_routine.wake_up_time,
        "exercise": new_routine.exercise,
        "sleep_hours": new_routine.sleep_hours,
        "activity": new_routine.activity,
        "notes": new_routine.notes
    }

@router.get("/routine/{user_id}")
def get_routine(
    user_id: int,
    db: Session = Depends(get_db)
):
    # Check whether user exists
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

    routine = (
        db.query(Routine)
        .filter(Routine.user_id == user_id)
        .order_by(Routine.id.desc())
        .first()
    )

    if not routine:
        raise HTTPException(
            status_code=404,
            detail="No routine found for this user"
        )

    return {
        "routine_id": routine.id,
        "user_id": routine.user_id,
        "wake_up_time": routine.wake_up_time,
        "exercise": routine.exercise,
        "sleep_hours": routine.sleep_hours,
        "activity": routine.activity,
        "notes": routine.notes
    }
@router.put("/routine/{routine_id}")
def update_routine(
    routine_id: int,
    routine_data: RoutineCreate,
    db: Session = Depends(get_db)
):
    routine = (
        db.query(Routine)
        .filter(Routine.id == routine_id)
        .first()
    )

    if not routine:
        raise HTTPException(
            status_code=404,
            detail="Routine not found"
        )

    # Check whether user exists
    user = (
        db.query(User)
        .filter(User.id == routine_data.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if routine.user_id != routine_data.user_id:
        raise HTTPException(
            status_code=403,
            detail="This routine does not belong to this user"
        )

    routine.wake_up_time = routine_data.wake_up_time
    routine.exercise = routine_data.exercise
    routine.sleep_hours = routine_data.sleep_hours
    routine.activity = routine_data.activity
    routine.notes = routine_data.notes

    db.commit()
    db.refresh(routine)

    return {
        "message": "Daily routine updated successfully",
        "routine_id": routine.id,
        "user_id": routine.user_id,
        "wake_up_time": routine.wake_up_time,
        "exercise": routine.exercise,
        "sleep_hours": routine.sleep_hours,
        "activity": routine.activity,
        "notes": routine.notes
    }

@router.delete("/routine/{routine_id}")
def delete_routine(
    routine_id: int,
    db: Session = Depends(get_db)
):
    routine = (
        db.query(Routine)
        .filter(Routine.id == routine_id)
        .first()
    )

    if not routine:
        raise HTTPException(
            status_code=404,
            detail="Routine not found"
        )

    db.delete(routine)
    db.commit()

    return {
        "message": "Daily routine deleted successfully",
        "routine_id": routine_id
    }