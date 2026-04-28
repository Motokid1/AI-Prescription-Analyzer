import json
import re
from typing import List

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from app.config import get_settings
from app.schemas import MedicineItem, MedicineExplanation
from app.prompts.medicine_prompt import MEDICINE_EXPLANATION_PROMPT


settings = get_settings()


def get_llm():
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.LLM_MODEL_NAME,
        temperature=0
    )


def extract_json_from_llm_response(content: str) -> dict:
    content = content.strip()
    content = content.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(content)
    except Exception:
        pass

    match = re.search(r"\{.*\}", content, re.DOTALL)
    if match:
        return json.loads(match.group())

    raise ValueError("No valid JSON found in medicine explanation response")


def explain_medicines(medicines: List[MedicineItem]) -> List[MedicineExplanation]:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(MEDICINE_EXPLANATION_PROMPT)
    chain = prompt | llm

    medicine_data = [medicine.model_dump() for medicine in medicines]

    response = chain.invoke({
        "medicines": medicine_data
    })

    try:
        parsed = extract_json_from_llm_response(response.content)

        return [
            MedicineExplanation(
                medicine_name=item.get("medicine_name") or "Unknown",
                simple_explanation=item.get("simple_explanation")
                or "Could not confidently explain this medicine.",
                safety_note=item.get("safety_note")
                or "Please confirm this medicine with your doctor or pharmacist."
            )
            for item in parsed.get("explanations", [])
        ]

    except Exception as e:
        print("MEDICINE EXPLANATION PARSE ERROR:", str(e))
        print("LLM RAW RESPONSE:", response.content)

        return [
            MedicineExplanation(
                medicine_name=medicine.medicine_name or "Unknown",
                simple_explanation="Could not confidently explain this medicine.",
                safety_note="Please confirm this medicine with your doctor or pharmacist."
            )
            for medicine in medicines
        ]