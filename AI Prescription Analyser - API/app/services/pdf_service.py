import fitz
import cv2
import numpy as np

from app.services.ocr_service import extract_text_from_image_array


def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)

    extracted_text = ""

    for page in doc:
        page_text = page.get_text()
        extracted_text += page_text + "\n"

    if extracted_text.strip():
        return extracted_text.strip()

    ocr_text = ""

    for page in doc:
        pix = page.get_pixmap(dpi=300)

        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
            pix.height,
            pix.width,
            pix.n
        )

        if pix.n == 4:
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

        if pix.n == 1:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        page_ocr_text = extract_text_from_image_array(img)
        ocr_text += page_ocr_text + "\n"

    return ocr_text.strip()