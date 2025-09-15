import argparse
import os
import shutil
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
    "，": ",", "．": ".", "：": ":", "；": ";", "！": "!", "？": "?",
    
    
    "|" : "l",  # common substitution
    "¡" : "i",  # upside-down i
    "Ｉ" : "I", # fullwidth I    
    
    
       # -----------------------
    # Latin letters with diacritics -> ASCII
    # Uppercase
    # -----------------------
    "Ā": "A", "Ă": "A", "Ą": "A", "Á": "A", "À": "A", "Â": "A", "Ä": "A", "Ã": "A", "Å": "A",
    "Ć": "C", "Ĉ": "C", "Ċ": "C", "Č": "C",
    "Ď": "D", "Đ": "D",
    "Ē": "E", "Ĕ": "E", "Ė": "E", "Ę": "E", "Ě": "E", "É": "E", "È": "E", "Ê": "E", "Ë": "E",
    "Ĝ": "G", "Ğ": "G", "Ġ": "G", "Ģ": "G",
    "Ĥ": "H", "Ħ": "H",
    "Ĩ": "I", "Ī": "I", "Į": "I", "İ": "I", "Í": "I", "Ì": "I", "Î": "I", "Ï": "I",
    "Ĵ": "J",
    "Ķ": "K",
    "Ĺ": "L", "Ļ": "L", "Ľ": "L", "Ł": "L",
    "Ń": "N", "Ņ": "N", "Ň": "N", "Ñ": "N",
    "Ō": "O", "Ŏ": "O", "Ő": "O", "Ó": "O", "Ò": "O", "Ô": "O", "Ö": "O", "Õ": "O",
    "Ŕ": "R", "Ŗ": "R", "Ř": "R",
    "Ś": "S", "Ŝ": "S", "Ş": "S", "Š": "S",
    "Ť": "T", "Ţ": "T", "Ŧ": "T",
    "Ũ": "U", "Ū": "U", "Ů": "U", "Ű": "U", "Ų": "U", "Ú": "U", "Ù": "U", "Û": "U", "Ü": "U",
    "Ŵ": "W",
    "Ŷ": "Y", "Ÿ": "Y",
    "Ź": "Z", "Ż": "Z", "Ž": "Z",

    # -----------------------
    # Lowercase
    # -----------------------
    "ā": "a", "ă": "a", "ą": "a", "á": "a", "à": "a", "â": "a", "ä": "a", "ã": "a", "å": "a", "ċ": "c",
    "ć": "c", "ĉ": "c", "č": "c", "ç": "c",
    "ď": "d", "đ": "d",
    "ē": "e", "ĕ": "e", "ė": "e", "ę": "e", "ě": "e", "é": "e", "è": "e", "ê": "e", "ë": "e",
    "ĝ": "g", "ğ": "g", "ġ": "g", "ģ": "g",
    "ĥ": "h", "ħ": "h",
    "ĩ": "i", "ī": "i", "į": "i", "ı": "i", "í": "i", "ì": "i", "î": "i", "ï": "i",
    "ĵ": "j",
    "ķ": "k",
    "ĺ": "l", "ļ": "l", "ľ": "l", "ł": "l",
    "ń": "n", "ņ": "n", "ň": "n", "ñ": "n",
    "ō": "o", "ŏ": "o", "ő": "o", "ó": "o", "ò": "o", "ô": "o", "ö": "o", "õ": "o",
    "ŕ": "r", "ŗ": "r", "ř": "r",
    "ś": "s", "ŝ": "s", "ş": "s", "š": "s",
    "ť": "t", "ţ": "t", "ŧ": "t",
    "ũ": "u", "ū": "u", "ů": "u", "ű": "u", "ų": "u", "ú": "u", "ù": "u", "û": "u", "ü": "u",
    "ŵ": "w",
    "ŷ": "y", "ÿ": "y",
    "ź": "z", "ż": "z", "ž": "z",
    
    
    "$": "S",  # common substitution
    "@": "a",  # common substitution
    "Ạ" : "A",  # A with dot below
    "ạ" : "a",  # a with dot below
    # "Ĳ" : "IJ", # ligature
    # "ĳ" : "ij", # ligature
    
    "%" : "#"
}


def normalize_lookalikes(s: str) -> str:
    """
    Very simple char-by-char normalization: replace any character that appears
    in LOOKALIKE_MAP with its ASCII equivalent, otherwise keep the character.
    """
    if not s:
        return s
    return "".join(LOOKALIKE_MAP.get(ch, ch) for ch in s)


def highlight_non_base64(s: str) -> str:
    
    """
    Splits the string by non-base64 characters and adds newlines where they appear.
    Returns the modified string and prints the positions and characters.
    """
    
    allowed_chars = string.ascii_letters + string.digits + "+/#" + string.whitespace
    
    result = []
    non_base64_chars = []
    last = 0
    for i, c in enumerate(s):
        if c not in allowed_chars:
            # Print position and character
            print(f"Non-base64 character at position {i}: {repr(c)}")
            # Add everything up to this character, then a newline
            if last < i:
                result.append( s[last:i] )
            result.append(f"Char {repr(c)}")
            last = i + 1
            
            non_base64_chars.append(c)
            
    # Add the rest of the string
    if last < len(s):
        result.append(s[last:])
        
        
    success = len(non_base64_chars) == 0
    if not success:
        print("\n\n\n".join(result))
    
    return success


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
    if highlight_non_base64(full_text):
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
        
        
def remove_all_whitespace(s: str) -> str:
    return "".join(s.split())
        
        
def read_from_image_file(input_path: str, output_path: str):
    
    print(f"Reading file: {input_path}")
    # Single file case
    res = detect_text(input_path)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write( remove_all_whitespace(res) )
        
    print(f"Wrote results to: {output_path}\n")

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
        
        if os.path.exists(results_dir): # remove if exists 
            shutil.rmtree(results_dir)
        os.makedirs(results_dir, exist_ok=True)

        # Process each file in the directory
        for fname in sorted(os.listdir(args.path)):
            
            input_path = os.path.join(args.path, fname)
            
            if os.path.isfile(input_path):
                out_fname = os.path.splitext(fname)[0] + ".txt"
                output_path = os.path.join(results_dir, out_fname)
                read_from_image_file( input_path, output_path )
                
    else:
        read_from_image_file(args.path, os.path.splitext(args.path)[0] + "_results.txt" )



