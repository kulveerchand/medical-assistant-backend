from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    full_name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)
    qualification = Column(String(255))
    experience = Column(Integer)
    phone = Column(String(20))
    clinic_name = Column(String(150))
    clinic_address = Column(String(500))