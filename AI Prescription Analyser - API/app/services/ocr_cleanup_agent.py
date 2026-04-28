from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from app.config import get_settings

settings = get_settings()


def get_llm():
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.LLM_MODEL_NAME,
        temperature=0
    )


OCR_CLEANUP_PROMPT = """
You are an OCR cleanup assistant for medical prescriptions.

The OCR text may contain two sections:
1. FULL OCR TEXT
2. POSSIBLE MEDICINE LINES

Use both sections carefully.

Your task:
Clean the OCR text and keep only useful prescription information.

Return only cleaned readable text, not JSON.

Rules:
- Give highest priority to POSSIBLE MEDICINE LINES.
- Preserve medicine names exactly when readable.
- Do not invent medicine names.
- Keep dosage, strength, frequency, duration, timing, and refills.
- Keep patient name, age, date, doctor name if available.
- Remove watermark text, repeated garbage, phone numbers, license numbers, unrelated address text.
- Preserve medical shorthand like T., Tab, Cap, Syp, Inj, OD, BD, BID, TDS, TID, SOS, PRN, HS.
- If a word is unclear, write [unclear].
- Keep each medicine on a separate line.

OCR text:
{ocr_text}
"""


def clean_ocr_text(raw_text: str) -> str:
    """
    Cleans OCR text using LLM
    """

    if not raw_text or len(raw_text.strip()) < 10:
        return raw_text

    prompt = ChatPromptTemplate.from_template(OCR_CLEANUP_PROMPT)
    chain = prompt | get_llm()

    response = chain.invoke({
        "ocr_text": raw_text
    })

    return response.content.strip()