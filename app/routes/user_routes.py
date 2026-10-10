import bcrypt

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin

router = APIRouter(prefix="/users", tags=["Users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    # Check username
    existing_username = (
        db.query(User)
        .filter(User.username == user.username)
        .first()
    )

    if existing_username:
        return {
            "message": "Username already registered"
        }

    # Check email
    existing_email = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_email:
        return {
            "message": "Email already registered"
        }

    # Hash password
    hashed_password = bcrypt.hashpw(
        user.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    # Create user
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)

    except Exception as e:
        db.rollback()

        print("REGISTER ERROR:", str(e))

        return {
            "message": "Registration failed",
            "error": str(e)
        }

    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }


@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):

    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if not existing_user:
        return {
            "message": "User not found"
        }

    password_correct = bcrypt.checkpw(
        user.password.encode("utf-8"),
        existing_user.hashed_password.encode("utf-8")
    )

    if not password_correct:
        return {
            "message": "Incorrect password"
        }

    return {
        "message": "Login successful",
        "user_id": existing_user.id,
        "username": existing_user.username,
        "email": existing_user.email
    }