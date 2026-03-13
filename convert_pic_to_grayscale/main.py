#!/usr/bin/env python3

import argparse
from pathlib import Path
import cv2


def convert_to_bw(input_path: Path, output_path: Path, threshold: int = 128):
    # Read the image
    img = cv2.imread(str(input_path))
    if img is None:
        raise ValueError(f"Failed to read image: {input_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply global threshold
    _, bw = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    # Save the result
    cv2.imwrite(str(output_path), bw)
    print(f"Saved black & white image to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Convert image to black & white (global threshold)")
    parser.add_argument("input", type=Path, help="Input image path")
    parser.add_argument(
        "-o", "--output", type=Path, help="Output image path (default: <input>_bw.png)"
    )
    parser.add_argument(
        "-t", "--threshold", type=int, default=128, help="Threshold value (0–255)"
    )

    args = parser.parse_args()

    output_path = args.output or args.input.with_stem(args.input.stem + "_bw")

    convert_to_bw(args.input, output_path, threshold=args.threshold)


if __name__ == "__main__":
    main()
