from typing import List, Optional
from pydantic import BaseModel, Field


class PatientDetails(BaseModel):
    name: Optional[str] = None
    age: Optional[str] = None
    gender: Optional[str] = None
    date: Optional[str] = None
    doctor_name: Optional[str] = None


class MedicineItem(BaseModel):
    medicine_name: Optional[str] = "Unknown"
    medicine_type: Optional[str] = None
    strength: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None
    route: Optional[str] = None
    timing: Optional[str] = None
    instructions: Optional[str] = None
    special_instructions: Optional[str] = None
    refills: Optional[str] = None   # 👈 ADD THIS
    original_text: Optional[str] = None
    confidence: Optional[str] = "medium"


class PrescriptionExtractionResponse(BaseModel):
    prescription_summary: Optional[str] = None
    patient_details: Optional[PatientDetails] = None
    medicines: List[MedicineItem] = Field(default_factory=list)
    tests_or_advice: List[str] = Field(default_factory=list)
    follow_up: Optional[str] = None
    warnings_or_unclear_parts: List[str] = Field(default_factory=list)
    raw_text: str


class MedicineExplanation(BaseModel):
    medicine_name: Optional[str] = "Unknown"
    simple_explanation: str
    safety_note: str


class MissingInfoItem(BaseModel):
    medicine_name: Optional[str] = "Unknown"
    missing_fields: List[str]
    warning: str


class ScheduleItem(BaseModel):
    time: str
    medicine_name: Optional[str] = "Unknown"
    dosage: Optional[str] = None
    instructions: Optional[str] = None


class FinalPrescriptionResponse(BaseModel):
    raw_text: str
    prescription_summary: Optional[str]
    patient_details: Optional[PatientDetails]
    medicines: List[MedicineItem]
    explanations: List[MedicineExplanation]
    missing_information: List[MissingInfoItem]
    daily_schedule: List[ScheduleItem]
    tests_or_advice: List[str]
    follow_up: Optional[str]
    warnings_or_unclear_parts: List[str]
    safety_disclaimer: str