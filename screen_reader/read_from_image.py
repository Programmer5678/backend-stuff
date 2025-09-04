import argparse
import os
from google.cloud import vision
import string

# Simple conservative map of common visual lookalikes -> ASCII
LOOKALIKE_MAP = {
    # Cyrillic -> Latin (common confusables)
    "а": "a", "А": "A",
    "в": "b", "В": "B",
    "с": "c", "С": "C",
    "е": "e", "Е": "E",
    "о": "o", "О": "O",
    "р": "p", "Р": "P",
    "к": "k", "К": "K",
    "м": "m", "М": "M",
    "н": "n", "Н": "H",  # uppercase Н looks like Latin H
    "т": "t", "Т": "T",
    "х": "x", "Х": "X",
    "у": "y", "У": "Y",
    "г": "r",             # your problematic case: Cyrillic г -> Latin r
    "і": "i",             # Ukrainian i
    "ј": "j",             # Cyrillic small je -> j

    # Greek -> Latin (some common ones)
    "ο": "o", "О": "O",
    "α": "a", "Α": "A",
    "ρ": "p", "Ρ": "P",
    "ι": "i", "Ι": "I",
    "κ": "k", "Κ": "K",
    "τ": "t", "Τ": "T",
    "ν": "v", "Ν": "N",
    "μ": "m", "Μ": "M",

    # Fullwidth digits/punct you might see
    "０": "0", "１": "1", "２": "2", "３": "3", "４": "4",
    "５": "5", "６": "6", "７": "7", "８": "8", "９": "9",
    "＃": "#", "＄": "$", "＠": "@",
    "，": ",", "．": ".", "：": ":", "；": ";", "！": "!", "？": "?"
}

def normalize_lookalikes(s: str) -> str:
    """
    Very simple char-by-char normalization: replace any character that appears
    in LOOKALIKE_MAP with its ASCII equivalent, otherwise keep the character.
    """
    if not s:
        return s
    return "".join(LOOKALIKE_MAP.get(ch, ch) for ch in s)

def is_english(s: str) -> bool:
    """
    Check if a string contains only English characters (ASCII letters, digits,
    punctuation) and all whitespace characters. Prints any non-English characters found.
    """
    allowed_chars = string.ascii_letters + string.digits + string.punctuation + string.whitespace
    non_english_chars = [c for c in s if c not in allowed_chars]

    if non_english_chars:
        print("Non-English characters found:", repr("".join(non_english_chars)))

    return len(non_english_chars) == 0

def detect_text(path: str):
    """Detects text in the file with language hints and validates English characters."""
    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Add language hint
    image_context = {"language_hints": ["en"]}

    response = client.text_detection(image=image, image_context=image_context)
    texts = response.text_annotations

    if not texts:
        print("No text detected.")
        return

    # normalize before using
    raw_text = texts[0].description
    full_text = normalize_lookalikes(raw_text)

    # print("OCR Text (normalized):")
    # print(full_text)

    # Validate if English
    if is_english(full_text):
        pass
        # print("\nText appears to be English.")
        
    else:
        raise Exception(f"\nText in file {path} contains non-English characters.")

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
        
        
    return full_text
        
        
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect text in an image using Google Cloud Vision API.")
    parser.add_argument(
        "--path",
        required=True,
        help="Path to the image file (local path or GCS URI)."
    )
    args = parser.parse_args()

    if os.path.isdir(args.path):
        # Create results directory
        results_dir = args.path.rstrip("/\\") + "_results"
        os.makedirs(results_dir, exist_ok=True)

        # Process each file in the directory
        for fname in os.listdir(args.path):
            fpath = os.path.join(args.path, fname)
            if os.path.isfile(fpath):
                res = detect_text(fpath)
                out_name = os.path.splitext(fname)[0] + ".txt"
                out_path = os.path.join(results_dir, out_name)
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(res)
    else:
        # Single file case
        res = detect_text(args.path)
        out_path = os.path.splitext(args.path)[0] + ".txt"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(res)



