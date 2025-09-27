#!/usr/bin/env python3
"""
Compare two binary files byte by byte and print offsets where they differ.

Usage:
    python bincompare_simple.py file1.bin file2.bin
"""

import sys
from pathlib import Path

def compare_files(file_a: Path, file_b: Path):
    size_a = file_a.stat().st_size
    size_b = file_b.stat().st_size
    max_size = max(size_a, size_b)

    with file_a.open("rb") as fa, file_b.open("rb") as fb:
        diffs = 0
        for offset in range(max_size):
            byte_a = fa.read(1)
            byte_b = fb.read(1)
            if byte_a != byte_b:
                print(f"Difference at offset {offset}: {byte_a.hex() if byte_a else 'EOF'} vs {byte_b.hex() if byte_b else 'EOF'}")
                diffs += 1

    if diffs == 0:
        print("Files are identical.")
    else:
        print(f"Total differences: {diffs}")

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} file1 file2")
        sys.exit(1)

    path_a = Path(sys.argv[1])
    path_b = Path(sys.argv[2])

    if not path_a.exists() or not path_b.exists():
        print("Error: one of the files does not exist.")
        sys.exit(1)

    compare_files(path_a, path_b)

if __name__ == "__main__":
    main()
