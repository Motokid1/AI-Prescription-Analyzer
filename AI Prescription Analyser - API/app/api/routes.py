from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.services.file_service import save_upload_file, validate_file
from app.services.pdf_service import extract_text_from_pdf
from app.services.ocr_service import extract_text_from_image
from app.services.prescription_agent import extract_prescription_details
from app.services.medicine_agent import explain_medicines
from app.services.checker_agent import check_missing_information
from app.services.schedule_agent import generate_schedule
from app.services.ocr_cleanup_agent import clean_ocr_text


router = APIRouter(tags=["Prescription Analyzer"])


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Prescription Analyzer"
    }


@router.post("/analyze")
async def analyze_prescription(
    file: Optional[UploadFile] = File(default=None),
    text: Optional[str] = Form(default=None)
):
    if not file and not text:
        raise HTTPException(
            status_code=400,
            detail="Please upload a prescription file or provide text."
        )

    raw_text = ""

    if text and text.strip():
        raw_text = text.strip()

    if file:
        validate_file(file)
        saved_path = await save_upload_file(file)

        if file.filename.lower().endswith(".pdf"):
            raw_text = extract_text_from_pdf(saved_path)
        else:
            raw_text = extract_text_from_image(saved_path)

    if not raw_text or len(raw_text.strip()) < 20:
        return {
            "raw_text": raw_text,
            "cleaned_text": None,
            "prescription_summary": "OCR could not extract enough readable text.",
            "patient_details": None,
            "medicines": [],
            "explanations": [],
            "missing_information": [],
            "daily_schedule": [],
            "tests_or_advice": [],
            "follow_up": None,
            "warnings_or_unclear_parts": [
                "OCR could not extract sufficient readable text. Please upload a clearer image or manually verify the prescription."
            ],
            "safety_disclaimer": "Consult your doctor or pharmacist before making any changes."
        }

    extracted_data = extract_prescription_details(raw_text)
    explanations = explain_medicines(extracted_data.medicines)
    missing_info = check_missing_information(extracted_data.medicines)
    schedule = generate_schedule(extracted_data.medicines)

    cleaned_text = clean_ocr_text(raw_text)

    extracted_data = extract_prescription_details(cleaned_text)
    explanations = explain_medicines(extracted_data.medicines)
    missing_info = check_missing_information(extracted_data.medicines)
    schedule = generate_schedule(extracted_data.medicines)

    return {
    "raw_text": raw_text,
    "cleaned_text": cleaned_text,
    "prescription_summary": extracted_data.prescription_summary,
    "patient_details": extracted_data.patient_details.model_dump() if extracted_data.patient_details else None,
    "medicines": [medicine.model_dump() for medicine in extracted_data.medicines],
    "explanations": [item.model_dump() for item in explanations],
    "missing_information": [item.model_dump() for item in missing_info],
    "daily_schedule": [item.model_dump() for item in schedule],
    "tests_or_advice": extracted_data.tests_or_advice,
    "follow_up": extracted_data.follow_up,
    "warnings_or_unclear_parts": extracted_data.warnings_or_unclear_parts,
    "safety_disclaimer": "Consult your doctor or pharmacist before making any changes."
}