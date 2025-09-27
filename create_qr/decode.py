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
import argparse
from pathlib import Path
from pyzbar.pyzbar import decode
from PIL import Image
import base45
import cv2

def read_qr_base45_bytes(file_path: Path) -> bytes:
    """
    Decode the first QR in file_path as Base45 and return the original bytes.
    Raises ValueError if no QR code or decoding fails.
    """
    from qreader import QReader
    
    # Open the image file
    img = cv2.cvtColor(cv2.imread( str(file_path) ), cv2.COLOR_BGR2RGB)

    # Initialize QReader and decode the image
    qreader = QReader()
    decoded_text = qreader.detect_and_decode(image=img)[0]

    if not decoded_text:
        raise ValueError(f"No QR code found in {file_path}")

    try:
        # Decode the Base45-encoded text
        return base45.b45decode(decoded_text)
    except Exception as e:
        raise ValueError(f"Base45 decoding failed for {file_path}: {e}. Decoded_text = {decoded_text}")

# def read_qr_base45_bytes(file_path: Path) -> bytes:
#     """
#     Decode the first QR in file_path as Base45 and return the original bytes.
#     Raises ValueError if no QR code or decoding fails.
#     """
#     img = Image.open(file_path)
#     decoded_objs = decode(img)
#     if not decoded_objs:
#         raise ValueError(f"No QR code found in {file_path}")
#     if len(decoded_objs) > 1:
#         print(f"Warning: Multiple QR codes found in {file_path}. Using the first one.")

#     qr_text = decoded_objs[0].data.decode('utf-8')  # QR data is Base45-encoded text
#     try:
#         return base45.b45decode(qr_text)
#     except Exception as e:
#         raise ValueError(f"Base45 decoding failed for {file_path}: {e}")


# def read_qr_raw_bytes(file_path: Path) -> bytes:
#     """
#     Return raw bytes of the first decoded QR code in file_path.
#     Raises ValueError if none found.
#     """
#     import cv2
#     import zxingcpp

#     # Load image with OpenCV
#     img = cv2.imread(str(file_path))
#     if img is None:
#         raise FileNotFoundError(f"Image not found: {file_path}")

#     # Decode all barcodes in the image
#     results = zxingcpp.read_barcodes(img)

#     if not results:
#         raise ValueError(f"No QR code found in {file_path}")

#     # Pick the first QR code found
#     first = results[0]

#     # if first.format != "QR_CODE":
#     #     raise ValueError(f"Barcode found but it's not a QR code: {first.format}")

#     # ZXing-C++ provides raw bytes as a list of integers (0-255)
#     raw_bytes = bytes(first.bytes)
#     print(raw_bytes.encode('latin-1'))
    
#     raise Exception("Shit")
    
#     return raw_bytes




def process_file(input_path: Path, out_f):
    """Read one image file, decode first QR and write its bytes into open file-like out_f.
       Returns number of bytes written (0 if none)."""
    try:
        data = read_qr_base45_bytes(input_path)
    except Exception as e:
        print(f"Skipping {input_path.name}: {e}")
        return 0
    
    out_f.write(data)
    print(f"Wrote {len(data)} bytes from {input_path.name}")
    return len(data)

def main():
    parser = argparse.ArgumentParser(description="Read QR image(s) and write raw bytes to a single output file.")
    parser.add_argument('-i', '--input', required=True, help="Input file or directory containing image files")
    parser.add_argument('-o', '--output', required=True, help="Output file path (binary, will be overwritten)")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(f"Input does not exist: {input_path}")

    # Open output file for writing (overwrite)
    with open(output_path, 'wb') as out_f:
        total = 0
        if input_path.is_file():
            total += process_file(input_path, out_f)
        else:
            # Directory: iterate regular files only, sorted by name
            entries = [p for p in sorted(input_path.iterdir()) if p.is_file()]
            if not entries:
                print(f"No files found in directory: {input_path}")
            for p in entries:
                total += process_file(p, out_f)

    print(f"Done. Total bytes written: {total}. Output file: {output_path.resolve()}")

if __name__ == "__main__":
    main()
