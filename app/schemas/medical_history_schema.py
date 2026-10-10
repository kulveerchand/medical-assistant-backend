from pydantic import BaseModel


class MedicalHistoryCreate(BaseModel):
    patient_id: int
    previous_diseases: str
    current_conditions: str
    allergies: str
    previous_surgeries: str
    notes: str