import argparse
import os
import shutil
from google.cloud import vision
import string
from constants import *

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
            # print(f"Non-base64 character at position {i}: {repr(c)}")
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


def detect_text(path: str, check_english_chars) -> str:
    """Detects text in the file with language hints and validates English characters."""
    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Add language hint
    image_context = {"language_hints": ["en"]}
    
    
    
    # def print_low_conf_chars_with_alternatives(full_text_annotation, threshold=0.75):
    #     for page in full_text_annotation.pages:
    #         for block in page.blocks:
    #             for paragraph in block.paragraphs:
    #                 for word in paragraph.words:
    #                     for symbol in word.symbols:
    #                         if symbol.confidence < threshold:
    #                             # Get alternatives if available
    #                             alt_chars = []
    #                             if hasattr(symbol.property, "detected_alternatives"):
    #                                 alt_chars = [alt.text for alt in symbol.property.detected_alternatives]
    #                             print(
    #                                 f"Low-confidence char: '{symbol.text}' "
    #                                 f"(confidence: {symbol.confidence}), alternatives: {alt_chars}"
    #                             )

    # print_low_conf_chars_with_alternatives(client.document_text_detection(image=image).full_text_annotation)    
    
    
    def replace_low_conf_chars(full_text_annotation, threshold=0.55, replace_char=ERASURE_CHAR, do_print=True):

        result = []

        for page in full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        for symbol in word.symbols:
                            char_to_add = symbol.text
                            if symbol.confidence < threshold and not char_to_add in ["#", "%"] :
                                char_to_add = replace_char

                            result.append(char_to_add)

        return "".join(result)


    # Usage
    response = client.document_text_detection(image=image, image_context=image_context)
    full_text_annotation = response.full_text_annotation

    if not full_text_annotation.pages:
        print("No text detected.")
        return
    
    clean_text = replace_low_conf_chars(full_text_annotation)
    print(clean_text)

    # raw_text = full_text_annotation.text  # similar to texts[0].description

    full_text = normalize_lookalikes(clean_text)

    # print("OCR Text (normalized):")
    # print(full_text)

    # Validate if English
    if not check_english_chars or highlight_non_base64(full_text) :
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
        
        
def read_from_image_file(input_path: str, output_path: str, check_english_chars):
    
    print(f"Reading file: {input_path}")
    # Single file case
    res = detect_text(input_path, check_english_chars)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write( remove_all_whitespace(res) )
        
    print(f"Wrote results to: {output_path}\n")


def str_to_bool(value):
    value = value.lower()
    if value == 'true':
        return True
    elif value == 'false':
        return False
    else:
        raise argparse.ArgumentTypeError("Value must be True or False")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Detect text in an image using Google Cloud Vision API.")
    
    parser.add_argument(
        "--path",
        required=True,
        help="Path to the image file (local path or GCS URI)."
    )
    
    parser.add_argument(
        "--check",
        required=True,
        help="Check for non-English characters (True/False).",
        type=str_to_bool
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
                read_from_image_file( input_path, output_path, args.check )
                
    else:
        read_from_image_file(args.path, os.path.splitext(args.path)[0] + "_results.txt" , args.check )



