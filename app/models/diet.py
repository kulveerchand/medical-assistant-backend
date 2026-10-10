from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base


class Diet(Base):
    __tablename__ = "diet"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    breakfast = Column(String(255))
    lunch = Column(String(255))
    dinner = Column(String(255))
    water_intake = Column(Float)