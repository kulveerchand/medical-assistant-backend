from pydantic import BaseModel


class RoutineCreate(BaseModel):
    user_id: int
    wake_up_time: str
    exercise: str
    sleep_hours: float
    activity: str
    notes: str