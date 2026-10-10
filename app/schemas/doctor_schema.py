from pydantic import BaseModel


class DoctorCreate(BaseModel):
    user_id: int
    full_name: str
    specialization: str
    qualification: str
    experience: int
    phone: str
    clinic_name: str
    clinic_address: str