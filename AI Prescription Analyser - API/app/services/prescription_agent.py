import json
import re

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from app.config import get_settings
from app.schemas import (
    PrescriptionExtractionResponse,
    MedicineItem,
    PatientDetails,
)
from app.prompts.extraction_prompt import EXTRACTION_PROMPT


settings = get_settings()


def get_llm():
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.LLM_MODEL_NAME,
        temperature=0
    )


def extract_json_from_llm_response(content: str) -> dict:
    """
    Handles cases where LLM returns:
    - valid JSON
    - ```json ... ```
    - extra text before/after JSON
    """

    content = content.strip()

    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    try:
        return json.loads(content)
    except Exception:
        pass

    match = re.search(r"\{.*\}", content, re.DOTALL)

    if match:
        return json.loads(match.group())

    raise ValueError("No valid JSON found in LLM response")


def extract_prescription_details(raw_text: str) -> PrescriptionExtractionResponse:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(EXTRACTION_PROMPT)
    chain = prompt | llm

    response = chain.invoke({
        "prescription_text": raw_text
    })

    try:
        parsed = extract_json_from_llm_response(response.content)

        medicines = [
            MedicineItem(**item)
            for item in parsed.get("medicines", [])
        ]

        patient_details = parsed.get("patient_details")

        return PrescriptionExtractionResponse(
            prescription_summary=parsed.get("prescription_summary"),
            patient_details=PatientDetails(**patient_details) if patient_details else None,
            medicines=medicines,
            tests_or_advice=parsed.get("tests_or_advice", []),
            follow_up=parsed.get("follow_up"),
            warnings_or_unclear_parts=parsed.get("warnings_or_unclear_parts", []),
            raw_text=raw_text
        )

    except Exception as e:
        print("LLM JSON PARSE ERROR:", str(e))
        print("LLM RAW RESPONSE:", response.content)

        return PrescriptionExtractionResponse(
            prescription_summary="Could not confidently structure the prescription.",
            patient_details=None,
            medicines=[
                MedicineItem(
                    medicine_name="Unknown",
                    dosage=None,
                    frequency=None,
                    duration=None,
                    instructions=None,
                    original_text=raw_text[:300],
                    confidence="low"
                )
            ],
            tests_or_advice=[],
            follow_up=None,
            warnings_or_unclear_parts=[
                "Could not parse the prescription output reliably."
            ],
            raw_text=raw_text
        )