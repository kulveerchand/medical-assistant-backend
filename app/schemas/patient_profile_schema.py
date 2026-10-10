from pydantic import BaseModel


class PatientProfileCreate(BaseModel):
    user_id: int
    age: int
    gender: str
    height: float
    weight: float
    blood_group: str
    allergies: str