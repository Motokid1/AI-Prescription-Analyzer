import re


def clean_extracted_text(text: str) -> str:
    text = text.replace("\n\n", "\n")
    text = re.sub(r"\s+", " ", text)
    return text.strip()