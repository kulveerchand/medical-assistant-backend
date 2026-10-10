from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id"),
        nullable=False
    )

    appointment_date = Column(String(20), nullable=False)
    appointment_time = Column(String(20), nullable=False)

    reason = Column(String(500))

    status = Column(
        String(20),
        default="Booked"
    )