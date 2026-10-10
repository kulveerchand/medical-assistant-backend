from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base


class PatientProfile(Base):
    __tablename__ = "patient_profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    age = Column(Integer)
    gender = Column(String(20))
    height = Column(Float)
    weight = Column(Float)
    blood_group = Column(String(10))
    allergies = Column(String(500))