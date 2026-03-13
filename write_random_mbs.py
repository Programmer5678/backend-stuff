#!/usr/bin/env python3
import sys
import os
import random
import string
import argparse

CHUNK_SIZE = 1024 * 1024  # 1 MB
CHARS = string.ascii_letters + string.digits + string.punctuation + ' '

def write_text(size_mb):
    for _ in range(size_mb):
        chunk = ''.join(random.choices(CHARS, k=CHUNK_SIZE))
        sys.stdout.write(chunk)

def write_binary(size_mb):
    stdout = sys.stdout.buffer
    for _ in range(size_mb):
        chunk = os.urandom(CHUNK_SIZE)
        stdout.write(chunk)

def main():
    parser = argparse.ArgumentParser(
        description="Generate random text or binary data of a given size (in MB)."
    )
    parser.add_argument("size", type=int, help="Size in MB (positive integer)")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["text", "binary"],
        help="Output mode: 'text' or 'binary'"
    )

    args = parser.parse_args()

    if args.size <= 0:
        parser.error("size must be a positive integer")

    if args.mode == "text":
        write_text(args.size)
    elif args.mode == "binary":
        write_binary(args.size)

if __name__ == "__main__":
    main()
