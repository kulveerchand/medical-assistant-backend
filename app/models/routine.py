from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base


class Routine(Base):
    __tablename__ = "routine"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    wake_up_time = Column(String(20))
    exercise = Column(String(255))
    sleep_hours = Column(Float)
    activity = Column(String(255))
    notes = Column(String(500))