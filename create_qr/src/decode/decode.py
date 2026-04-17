#!/usr/bin/env python3
"""
Read QR code(s) from a file or directory and write decoded raw bytes to one output file.

Usage:
    python qr_reader_to_file.py -i qr_image.png -o output.bin
    python qr_reader_to_file.py -i qr_images_dir -o output.bin

Behavior:
 - If -i points to a file: decode the first QR in that image and write its raw bytes to output file.
 - If -i points to a directory: iterate all regular files in the directory (sorted by name),
   decode the first QR in each file (if present) and append each decoded blob to the single output file
   in that sorted order.
 - Files with no QR produce a warning and are skipped.
"""
import glob
import os
from pathlib import Path
from pyzbar.pyzbar import decode
from PIL import Image
import base45
import cv2
from qreader import QReader
from qrdet.qrdet import QRDetector

from src.input_validate import validate_abs_path, validate_is_dir, validate_parent_dir, validate_exists
from src.domain_errors import ReadQRFailDE

def validate_weights_folder(weights_folder: str):
    """
    Validates that the weights folder contains the required files:
    - current_release.txt
    - at least one qrdet*.pt file

    Args:
        weights_folder (str): Path to the weights folder.

    Raises:
        FileNotFoundError: If any required file is missing.
    """
    # Check for current_release.txt
    release_file = os.path.join(weights_folder, 'current_release.txt')
    if not os.path.isfile(release_file):
        raise FileNotFoundError(f"Missing required file: {release_file}")

    # Check for any qrdet*.pt files
    pt_files = glob.glob(os.path.join(weights_folder, 'qrdet*.pt'))
    if not pt_files:
        raise FileNotFoundError(f"No 'qrdet*.pt' files found in {weights_folder}")



def read_qr_text(file_path: Path) -> str:
    """
    Decode the first QR code in file_path and return its decoded text.
    Raises ValueError if no QR code is found.
    """
    # Load image
    img_bgr = cv2.imread(str(file_path))
    if img_bgr is None:
        raise ReadQRFailDE(f"Failed to read image file {file_path}")

    img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # Initialize QReader
    weights_folder = os.path.join(os.getcwd(), "weights_for_qrdet", ".model")
    validate_weights_folder(weights_folder)

    qreader = QReader(weights_folder=weights_folder)

    decoded_text = qreader.detect_and_decode(image=img)[0]

    if not decoded_text:
        raise ReadQRFailDE(f"No QR code found in {file_path}")

    return decoded_text


def decode_base45_text(decoded_text: str) -> bytes:
    """
    Decode Base45-encoded text and return original bytes.
    Raises ValueError if decoding fails.
    """
    try:
        return base45.b45decode(decoded_text)
    except Exception as e:
        raise ValueError(
            f"Base45 decoding failed. Decoded_text={decoded_text!r}"
        ) from e






def decode_file(input_path: Path, out_f, base45_decode: bool) -> int:
    """Read one image file, decode first QR and write its bytes into open file-like out_f.
       Returns number of bytes written (0 if none)."""
    try:
        decoded_text = read_qr_text(input_path)
        data = decode_base45_text(decoded_text) if base45_decode else decoded_text.encode('utf-8')

    except Exception as e:
        raise type(e)(f"Failed to decode {input_path.name}: {e}")
    
    out_f.write(data)
    print(f"Wrote {len(data)} bytes from {input_path.name}")
    return len(data)



def encode_input_validation(input, output):
    validate_abs_path(input)
    validate_is_dir(input)
    validate_exists(input)
    validate_abs_path(output)
    validate_parent_dir(output)

def decode(input, output, base45 = True):

    encode_input_validation(input, output)

    input_path = Path(input)
    output_path = Path(output)

    # Open output file for writing (overwrite)
    with open(output_path, 'wb') as out_f:
        total = 0
        if input_path.is_file():
            total += decode_file(input_path, out_f, base45)
        else:
            # Directory: iterate regular files only, sorted by name
            entries = [p for p in sorted(input_path.iterdir()) if p.is_file()]
            if not entries:
                print(f"No files found in directory: {input_path}")
            for p in entries:
                total += decode_file(p, out_f, base45)

    print(f"Done. Total bytes written: {total}. Output file: {output_path.resolve()}")
