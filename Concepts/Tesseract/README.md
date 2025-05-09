# OCR Tool for LLM Function Use (Concept)

This is a **concept-stage OCR utility** designed to demonstrate how local image preprocessing and text extraction can be integrated into LLM-based systems as a callable tool.

The goal is to enable **LLMs to extract text from local image files** (e.g., scanned documents, screenshots) **without relying on cloud APIs**. It uses Tesseract OCR with preprocessing to improve recognition accuracy, especially for vertical Traditional Chinese text.

## What It Does

- Loads an image and applies a simple preprocessing pipeline (contrast, thresholding, denoising).
- Uses Tesseract to extract text (with support for vertical Chinese layout).
- Optionally draws bounding boxes for OCR debug visualization.
- Outputs a `.txt` file with the extracted content.

## Why It Exists

This project explores how **LLMs can interact with local OCR tools** as part of a hybrid system:
- Useful for building assistants that process invoices, IDs, screenshots, or forms.
- Keeps data local — no API keys or cloud processing required.
- Easily modifiable and extensible as LLM tooling evolves.

## Status

This is a **work-in-progress prototype** — not a finished package or API.
- Error handling is minimal
- Hardcoded paths (configurable manually)
- Not packaged or abstracted for reuse yet

## Dependencies

- Python 3.8+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (must be installed locally)
- Python packages:
  - `opencv-python`
  - `numpy`
  - `pytesseract`
  - `pandas`

## How to Try It

1. Set your image path and Tesseract path in `main.py`.
2. Run the script:

```bash
python main.py