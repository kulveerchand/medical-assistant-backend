from pydantic import BaseModel


class DoctorAvailabilityCreate(BaseModel):
    doctor_id: int
    day: str
    start_time: str
    end_time: str