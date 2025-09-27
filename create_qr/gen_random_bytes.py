#!/usr/bin/env python3
"""
Generate a random file of given size in binary, text, or Base64 mode.
"""

import argparse
from pathlib import Path
import os
import random
import string
import base64

def generate_binary(size: int) -> bytes:
    return os.urandom(size)

def generate_text(size: int) -> str:
    chars = string.ascii_letters + string.digits + string.punctuation + ' \n\t'
    return ''.join(random.choices(chars, k=size))

def generate_base64(size: int) -> str:
    random_bytes = os.urandom(size)
    return base64.b64encode(random_bytes).decode('ascii')

def main():
    parser = argparse.ArgumentParser(description="Generate a random file (binary, text, or Base64).")
    parser.add_argument('-o', '--output', required=True, help="Output file path")
    parser.add_argument('-s', '--size', type=int, default=10000, help="File size in bytes (default 10,000)")
    parser.add_argument('--mode', choices=['binary', 'text', 'b64'], default='binary',
                        help="File mode: binary, text, or b64 (default binary)")
    args = parser.parse_args()

    output_path = Path(args.output)

    if args.mode == 'binary':
        data = generate_binary(args.size)
        with open(output_path, 'wb') as f:
            f.write(data)
    elif args.mode == 'text':
        data = generate_text(args.size)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(data)
    else:  # Base64 mode
        data = generate_base64(args.size)
        with open(output_path, 'w', encoding='ascii') as f:
            f.write(data)

    print(f"Random {args.mode} file of {args.size} bytes saved to {output_path}")

if __name__ == "__main__":
    main()
