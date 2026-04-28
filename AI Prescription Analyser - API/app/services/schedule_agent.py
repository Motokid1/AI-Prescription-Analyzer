import json
from typing import List

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from app.config import get_settings
from app.schemas import MedicineItem, ScheduleItem
from app.prompts.schedule_prompt import SCHEDULE_PROMPT


settings = get_settings()


def get_llm():
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.LLM_MODEL_NAME,
        temperature=0
    )


def generate_schedule(medicines: List[MedicineItem]) -> List[ScheduleItem]:
    llm = get_llm()

    prompt = ChatPromptTemplate.from_template(SCHEDULE_PROMPT)

    chain = prompt | llm

    medicine_data = [medicine.model_dump() for medicine in medicines]

    response = chain.invoke({
        "medicines": medicine_data
    })

    try:
        parsed = json.loads(response.content)

        return [
            ScheduleItem(**item)
            for item in parsed.get("daily_schedule", [])
        ]

    except Exception:
        return [
            ScheduleItem(
                time="Unknown",
                medicine_name=medicine.medicine_name,
                dosage=medicine.dosage,
                instructions=medicine.instructions
            )
            for medicine in medicines
        ]