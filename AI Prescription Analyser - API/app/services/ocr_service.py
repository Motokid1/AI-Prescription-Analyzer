import cv2
import numpy as np
from functools import lru_cache
from paddleocr import PaddleOCR


FAST_TEXT_MIN_LENGTH = 80
FAST_MEDICINE_TEXT_MIN_LENGTH = 20
OCR_CONFIDENCE_THRESHOLD = 0.25


@lru_cache(maxsize=1)
def get_paddle_ocr():
    return PaddleOCR(
        use_angle_cls=True,
        lang="en",
        det_db_box_thresh=0.3,
        det_db_thresh=0.2,
        rec_batch_num=1
    )


def resize_image(image):
    height, width = image.shape[:2]

    if width < 1200:
        scale = 1200 / width
        image = cv2.resize(
            image,
            None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_CUBIC
        )

    return image


def preprocess_original(image):
    return resize_image(image.copy())


def preprocess_shadow_removed(image):
    image = resize_image(image.copy())
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    dilated = cv2.dilate(gray, np.ones((7, 7), np.uint8))
    bg = cv2.medianBlur(dilated, 21)
    diff = 255 - cv2.absdiff(gray, bg)
    norm = cv2.normalize(diff, None, 0, 255, cv2.NORM_MINMAX)

    return cv2.cvtColor(norm, cv2.COLOR_GRAY2BGR)


def preprocess_high_contrast(image):
    image = resize_image(image.copy())
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        10
    )

    return cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)


def run_paddle_ocr(image) -> list[str]:
    ocr = get_paddle_ocr()
    result = ocr.ocr(image)

    lines = []

    if not result:
        return lines

    for page in result:
        if not page:
            continue

        if isinstance(page, dict):
            texts = page.get("rec_texts", [])
            scores = page.get("rec_scores", [])

            for text, score in zip(texts, scores):
                if text and score >= OCR_CONFIDENCE_THRESHOLD:
                    lines.append(text.strip())

            continue

        for line in page:
            try:
                if (
                    isinstance(line, list)
                    and len(line) >= 2
                    and isinstance(line[1], (list, tuple))
                    and len(line[1]) >= 2
                ):
                    text = line[1][0]
                    confidence = line[1][1]

                    if text and confidence >= OCR_CONFIDENCE_THRESHOLD:
                        lines.append(text.strip())

                elif (
                    isinstance(line, (list, tuple))
                    and len(line) >= 2
                    and isinstance(line[0], str)
                ):
                    text = line[0]
                    confidence = line[1]

                    if text and confidence >= OCR_CONFIDENCE_THRESHOLD:
                        lines.append(text.strip())

                elif isinstance(line, str):
                    lines.append(line.strip())

            except Exception:
                continue

    return lines


def merge_unique_lines(lines: list[str]) -> str:
    seen = set()
    cleaned = []

    for line in lines:
        normalized = line.lower().strip()

        if not normalized:
            continue

        if len(normalized) < 2:
            continue

        if normalized not in seen:
            seen.add(normalized)
            cleaned.append(line)

    return "\n".join(cleaned).strip()


def extract_possible_medicine_lines(text: str) -> str:
    medicine_keywords = [
        "tab", "tablet", "t.", "cap", "capsule", "syp", "syrup",
        "inj", "injection", "drop", "drops", "cream", "ointment",
        "mg", "ml", "mcg", "gm",
        "od", "qd", "bd", "bid", "tds", "tid", "qid",
        "sos", "prn", "hs",
        "1-0-1", "1-1-1", "0-0-1", "1-0-0", "0-1-0",
        "before food", "after food", "empty stomach"
    ]

    possible_lines = []

    for line in text.splitlines():
        lower = line.lower()

        if any(keyword in lower for keyword in medicine_keywords):
            possible_lines.append(line)

    return "\n".join(possible_lines).strip()


def format_ocr_output(full_text: str, possible_medicines: str) -> str:
    return f"""
FULL OCR TEXT:
{full_text}

POSSIBLE MEDICINE LINES:
{possible_medicines}
""".strip()


def is_fast_ocr_good_enough(full_text: str, possible_medicines: str) -> bool:
    return (
        len(full_text.strip()) >= FAST_TEXT_MIN_LENGTH
        and len(possible_medicines.strip()) >= FAST_MEDICINE_TEXT_MIN_LENGTH
    )


def smart_ocr_pipeline(image) -> str:
    """
    Fast mode:
    - Run PaddleOCR only on original image.
    - If good enough, stop.

    Fallback mode:
    - Run shadow-removed OCR.
    - Run high-contrast OCR.
    - Merge all results.
    """

    # Fast OCR first
    fast_image = preprocess_original(image)
    fast_lines = run_paddle_ocr(fast_image)
    fast_text = merge_unique_lines(fast_lines)
    fast_possible_medicines = extract_possible_medicine_lines(fast_text)

    if is_fast_ocr_good_enough(fast_text, fast_possible_medicines):
        return format_ocr_output(fast_text, fast_possible_medicines)

    # Enhanced OCR only when needed
    all_lines = []
    all_lines.extend(fast_lines)

    enhanced_images = [
        preprocess_shadow_removed(image),
        preprocess_high_contrast(image),
    ]

    for enhanced_image in enhanced_images:
        enhanced_lines = run_paddle_ocr(enhanced_image)
        all_lines.extend(enhanced_lines)

    merged_text = merge_unique_lines(all_lines)
    possible_medicines = extract_possible_medicine_lines(merged_text)

    return format_ocr_output(merged_text, possible_medicines)


def extract_text_from_image(image_path: str) -> str:
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Unable to read image file.")

    return smart_ocr_pipeline(image)


def extract_text_from_image_array(image_array) -> str:
    if image_array is None:
        return ""

    if len(image_array.shape) == 2:
        image_array = cv2.cvtColor(image_array, cv2.COLOR_GRAY2BGR)

    return smart_ocr_pipeline(image_array)