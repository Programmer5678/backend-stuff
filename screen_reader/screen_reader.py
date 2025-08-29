#!/usr/bin/env python3
import argparse
import sys

import cv2
import easyocr

def main():
    p = argparse.ArgumentParser(description="Read all text from an image using EasyOCR.")
    p.add_argument("image", nargs="?", default="image.jpg", help="Path to image (default: image.jpg)")
    args = p.parse_args()

    # Load the image
    img = cv2.imread(args.image)
    if img is None:
        print(f"Can't read image: {args.image}", file=sys.stderr)
        sys.exit(2)

    # -----------------------------
    # 1. Optional Upscaling
    # -----------------------------
    # If text is small, enlarging the image helps OCR detect each character more accurately
    scale_factor = 2  # you can adjust this
    img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

    # -----------------------------
    # 2. Grayscale conversion
    # -----------------------------
    # Converts image to shades of gray, simplifying processing and removing color info
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # -----------------------------
    # 3. Thresholding / Binarization
    # -----------------------------
    # Forces each pixel to be either black or white
    # Removes anti-aliasing and ensures crisp edges for OCR
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Use THRESH_BINARY_INV if your text is white on black:
    # _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # -----------------------------
    # 4. OCR
    # -----------------------------
    # detail=1 -> get bounding boxes and confidence
    # paragraph=False -> preserve line structure
    reader = easyocr.Reader(["en"], gpu=False)
    results = reader.readtext(thresh, detail=1, paragraph=False)

    # -----------------------------
    # 5. Optional character-level correction
    # -----------------------------
    # Base64 often confuses O->0, l->1, I->1 etc.
    corrections = {"O":"0", "l":"1", "I":"1"}
    for bbox, line_text, conf in results:
        # Apply corrections to each line
        corrected = "".join(corrections.get(c, c) for c in line_text)
        print(corrected)

if __name__ == "__main__":
    main()
