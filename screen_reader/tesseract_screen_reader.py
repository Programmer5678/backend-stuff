#!/usr/bin/env python3
import argparse
import pytesseract
from PIL import Image

def extract_text(image_path, lang="eng"):
    """Extract text from image using Tesseract OCR."""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang=lang)
    return text

def main():
    parser = argparse.ArgumentParser(description="Extract text from an image using Tesseract OCR.")
    parser.add_argument("image", help="Path to the input image")
    parser.add_argument("-l", "--lang", default="eng", help="Language for OCR (default: eng)")
    args = parser.parse_args()

    # Point to your installed tesseract binary (if needed)
    pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

    text = extract_text(args.image, args.lang)
    print("----- Extracted Text -----\n")
    print(text)

if __name__ == "__main__":
    main()
