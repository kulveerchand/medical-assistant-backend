from pydantic import BaseModel


class DietCreate(BaseModel):
    user_id: int
    breakfast: str
    lunch: str
    dinner: str
    water_intake: float