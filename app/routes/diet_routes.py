from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.diet import Diet
from app.models.user import User
from app.schemas.diet_schema import DietCreate

router = APIRouter()


@router.post("/diet")
def create_diet(
    diet: DietCreate,
    db: Session = Depends(get_db)
):
    # Check whether user exists
    user = (
        db.query(User)
        .filter(User.id == diet.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    new_diet = Diet(
        user_id=diet.user_id,
        breakfast=diet.breakfast,
        lunch=diet.lunch,
        dinner=diet.dinner,
        water_intake=diet.water_intake
    )

    db.add(new_diet)
    db.commit()
    db.refresh(new_diet)

    return {
        "message": "Daily diet saved successfully",
        "diet_id": new_diet.id,
        "user_id": new_diet.user_id,
        "breakfast": new_diet.breakfast,
        "lunch": new_diet.lunch,
        "dinner": new_diet.dinner,
        "water_intake": new_diet.water_intake
    }

@router.get("/diet/{user_id}")
def get_diet(
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

    diet = (
        db.query(Diet)
        .filter(Diet.user_id == user_id)
        .order_by(Diet.id.desc())
        .first()
    )

    if not diet:
        raise HTTPException(
            status_code=404,
            detail="No diet found for this user"
        )

    return {
        "diet_id": diet.id,
        "user_id": diet.user_id,
        "breakfast": diet.breakfast,
        "lunch": diet.lunch,
        "dinner": diet.dinner,
        "water_intake": diet.water_intake
    }

@router.put("/diet/{diet_id}")
def update_diet(
    diet_id: int,
    diet_data: DietCreate,
    db: Session = Depends(get_db)
):
    diet = (
        db.query(Diet)
        .filter(Diet.id == diet_id)
        .first()
    )

    if not diet:
        raise HTTPException(
            status_code=404,
            detail="Diet not found"
        )

    # Check whether user exists
    user = (
        db.query(User)
        .filter(User.id == diet_data.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if diet.user_id != diet_data.user_id:
        raise HTTPException(
            status_code=403,
            detail="This diet does not belong to this user"
        )

    diet.breakfast = diet_data.breakfast
    diet.lunch = diet_data.lunch
    diet.dinner = diet_data.dinner
    diet.water_intake = diet_data.water_intake

    db.commit()
    db.refresh(diet)

    return {
        "message": "Daily diet updated successfully",
        "diet_id": diet.id,
        "user_id": diet.user_id,
        "breakfast": diet.breakfast,
        "lunch": diet.lunch,
        "dinner": diet.dinner,
        "water_intake": diet.water_intake
    }
@router.delete("/diet/{diet_id}")
def delete_diet(
    diet_id: int,
    db: Session = Depends(get_db)
):
    diet = (
        db.query(Diet)
        .filter(Diet.id == diet_id)
        .first()
    )

    if not diet:
        raise HTTPException(
            status_code=404,
            detail="Diet not found"
        )

    db.delete(diet)
    db.commit()

    return {
        "message": "Daily diet deleted successfully",
        "diet_id": diet_id
    }