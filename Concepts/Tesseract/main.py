import cv2
import numpy as np
import pytesseract
import pandas as pd
import os
from typing import Tuple

# === Configuration ===
TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
INPUT_IMAGE_PATH = '1000004849.jpg'
PSM_MODE = 5  # Assume single vertical text line
LANG = "chi_tra_vert"
MIN_CONTOUR_AREA = 30
OUTPUT_TEXT_SUFFIX = "_output.txt"
DEBUG_IMAGE_NAME = "debug_output.jpg"

# Set up Tesseract path
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


def adjust_brightness_contrast(image: np.ndarray, alpha: float, beta: int) -> np.ndarray:
    """Adjusts brightness and contrast."""
    return cv2.addWeighted(image, alpha, image, 0, beta)


def preprocess_image(image: np.ndarray) -> np.ndarray:
    """Performs preprocessing including grayscale conversion, thresholding, denoising, and contour cleaning."""
    adjusted = adjust_brightness_contrast(image, alpha=0.5, beta=40)
    gray = cv2.cvtColor(adjusted, cv2.COLOR_BGR2GRAY)

    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 15, 10)
    
    kernel = np.ones((2, 2), np.uint8)
    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    blurred = cv2.medianBlur(opened, 3)

    # Remove small contours
    contours, _ = cv2.findContours(blurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.full(blurred.shape, 255, dtype=np.uint8)
    for cnt in contours:
        if cv2.contourArea(cnt) < MIN_CONTOUR_AREA:
            cv2.drawContours(mask, [cnt], -1, 0, -1)

    return cv2.bitwise_and(blurred, mask)


def extract_text_and_boxes(image: np.ndarray) -> Tuple[str, pd.DataFrame]:
    """Runs OCR to extract text and bounding box data."""
    config = f"--psm {PSM_MODE} -l {LANG}"
    data = pytesseract.image_to_data(image, config=config, output_type=pytesseract.Output.DATAFRAME)
    text = pytesseract.image_to_string(image, config=config)
    return text, data


def draw_bounding_boxes(image: np.ndarray, ocr_data: pd.DataFrame) -> np.ndarray:
    """Draws bounding boxes around detected text."""
    for _, row in ocr_data.iterrows():
        if pd.notna(row['text']):
            x, y, w, h = row['left'], row['top'], row['width'], row['height']
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return image


def main():
    filename = os.path.splitext(os.path.basename(INPUT_IMAGE_PATH))[0]
    image = cv2.imread(INPUT_IMAGE_PATH)
    if image is None:
        raise FileNotFoundError(f"Image not found: {INPUT_IMAGE_PATH}")

    processed = preprocess_image(image)
    text, data = extract_text_and_boxes(processed)

    debug_image = draw_bounding_boxes(processed.copy(), data)
    cv2.imwrite(DEBUG_IMAGE_NAME, debug_image)

    with open(f"{filename}{OUTPUT_TEXT_SUFFIX}", "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == "__main__":
    main()
