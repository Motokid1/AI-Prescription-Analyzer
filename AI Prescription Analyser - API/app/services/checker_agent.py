import json
from typing import List

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from app.config import get_settings
from app.schemas import MedicineItem, MissingInfoItem
from app.prompts.checker_prompt import CHECKER_PROMPT


settings = get_settings()


def get_llm():
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.LLM_MODEL_NAME,
        temperature=0
    )


def check_missing_information(medicines: List[MedicineItem]) -> List[MissingInfoItem]:
    llm = get_llm()

    prompt = ChatPromptTemplate.from_template(CHECKER_PROMPT)

    chain = prompt | llm

    medicine_data = [medicine.model_dump() for medicine in medicines]

    response = chain.invoke({
        "medicines": medicine_data
    })

    try:
        parsed = json.loads(response.content)

        return [
            MissingInfoItem(**item)
            for item in parsed.get("missing_information", [])
        ]

    except Exception:
        fallback_items = []

        for medicine in medicines:
            missing = []

            if not medicine.medicine_name or medicine.medicine_name == "Unknown":
                missing.append("medicine_name")
            if not medicine.dosage:
                missing.append("dosage")
            if not medicine.frequency:
                missing.append("frequency")
            if not medicine.duration:
                missing.append("duration")
            if not medicine.instructions:
                missing.append("instructions")

            if missing:
                fallback_items.append(
                    MissingInfoItem(
                        medicine_name=medicine.medicine_name,
                        missing_fields=missing,
                        warning="Some prescription details are missing or unclear. Please confirm with your doctor or pharmacist."
                    )
                )

        return fallback_items   