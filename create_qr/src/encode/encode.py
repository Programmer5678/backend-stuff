#!/usr/bin/env python3
"""
Encode an input file into chunks that fit QR-40 alphanumeric capacity,
Base45-encode each chunk, and write one QR (Version 40) PNG per chunk.

Usage:
    python create_qr_from_file_base45_blocks.py -i input.bin -o qr_output_folder [--ecc L|M|Q|H]

Notes:
 - Instead of encoding the entire file to Base45 at once, this splits
   the raw bytes into chunks sized to fit after Base45 encoding into QR-40.
 - Each chunk is Base45-encoded separately so it can be decoded independently.
"""


from pathlib import Path
import shutil
import qrcode
import base45

from src.input_validate.input_validate import validate_abs_path, validate_is_file, validate_parent_dir, validate_exists


# QR-40 **alphanumeric** capacities (characters)
QR40_ALNUM_CAPACITY = {
    'L': 4296,
    'M': 3391,
    'Q': 2420,
    'H': 1852,
}

def max_bytes_for_base45_capacity(char_capacity: int) -> int:
    """
    Returns the largest number of raw bytes that can be Base45-encoded
    into a string <= char_capacity characters.
    Base45 encodes 2 bytes -> 3 chars. So floor(char_capacity / 3) * 2 bytes
    """
    return (char_capacity // 3) * 2

def chunk_bytes(data: bytes, chunk_size: int):
    """Yield consecutive slices of `data` of at most chunk_size bytes."""
    for i in range(0, len(data), chunk_size):
        yield data[i:i+chunk_size]

def create_qr_from_text(text: str, index: int, out_folder: Path, ecc: str, box_size: int, border: int):
    """Create a single Version 40 QR containing the provided alphanumeric text."""
    qr = qrObject(border, box_size, ecc)
    qr.add_data(text)
    make_qr(qr, index, ecc, text)
    img = as_img(qr)

    out_path = out_folder / f"qr_chunk_{index:03d}.png"
    img.save(out_path)
    print(f"Saved chunk {index:03d}: {len(text)} chars -> {out_path}")


def qrObject(border, box_size, ecc):
    return qrcode.QRCode(
        version=40,
        error_correction={
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H,
        }[ecc],
        box_size=box_size,
        border=border
    )


def as_img(qr) :
    return qr.make_image(fill_color="black", back_color="white")

def raise_chunk_too_large_exception(e, ecc, index, text):
    raise Exception(
        f"Chunk {index}, too long for qr code (Base45 chars={len(text)}) overflowed Version 40 ECC {ecc}. "
        f"Original error: {e}"
    ) from e


def make_qr(qr, index, ecc, text):

    CHUNK_TOO_LARGE_EXCEPTION = qrcode.exceptions.DataOverflowError

    try:
        qr.make(fit=False)  # force Version 40
    except CHUNK_TOO_LARGE_EXCEPTION as e:
        raise_chunk_too_large_exception(e, ecc, index, text)


def get_chunks(ecc, input_path) :
    # Read input bytes
    data = input_path.read_bytes()
    capacity_chars = QR40_ALNUM_CAPACITY[ecc]
    chunk_size_bytes = max_bytes_for_base45_capacity(capacity_chars)

    print(f"Input size: {len(data)} bytes")
    print(f"QR-40 alphanumeric capacity (ECC {ecc}): {capacity_chars} chars")
    estimated_b45_chars = (chunk_size_bytes * 3) // 2  # 2 bytes -> 3 chars
    print(
        f"Chunking raw bytes into {chunk_size_bytes}-byte blocks for Base45 (~{estimated_b45_chars} Base45 chars per chunk)...")

    chunks = list(chunk_bytes(data, chunk_size_bytes))
    print(f"Total QR chunks to generate: {len(chunks)}")
    return chunks


def create_dir(out_folder):
    # wipe output folder if it exists
    if out_folder.exists() and out_folder.is_dir():
        shutil.rmtree(out_folder)
    out_folder.mkdir(parents=True, exist_ok=True)

def encode_input_validation(input, output):

    validate_exists(input)
    validate_abs_path(input)
    validate_is_file(input)

    validate_abs_path(output)
    validate_parent_dir(output)

def encode(input, output, ecc='Q', box_size=8, border=4):

    encode_input_validation(input, output)

    input_path = Path(input)
    out_folder = Path(output)

    create_dir(out_folder)

    chunks = get_chunks(ecc, input_path)

    for idx, chunk_bytes_data in enumerate(chunks):
        b45_text = base45.b45encode(chunk_bytes_data)
        create_qr_from_text(b45_text, idx, out_folder, ecc, box_size, border)


    print(f"Done. {len(chunks)} QR code(s) written to {out_folder.resolve()}")


