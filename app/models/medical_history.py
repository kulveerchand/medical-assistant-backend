from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class MedicalHistory(Base):
    __tablename__ = "medical_history"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    previous_diseases = Column(String(500))
    current_conditions = Column(String(500))
    allergies = Column(String(500))
    previous_surgeries = Column(String(500))
    notes = Column(String(1000))