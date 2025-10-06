#!/usr/bin/env python3
import argparse
from google.cloud import vision

def detect_text(path: str) -> str:
    """
    Return the full detected text in the image at `path`.
    Works for Hebrew and other languages.
    """
    client = vision.ImageAnnotatorClient()

    if path.startswith("gs://"):
        image = vision.Image(source=vision.ImageSource(gcs_image_uri=path))
    else:
        with open(path, "rb") as f:
            image = vision.Image(content=f.read())

    response = client.document_text_detection(image=image)
    if response.error.message:
        raise RuntimeError(f"Vision API error: {response.error.message}")

    return response.full_text_annotation.text or ""

def main():
    parser = argparse.ArgumentParser(description="Detect text in an image (any language)")
    parser.add_argument("path", help="Local image path or GCS URI (gs://...)")
    parser.add_argument("--out", "-o", help="Write output to file instead of stdout", default=None)
    args = parser.parse_args()

    text = detect_text(args.path)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Wrote detected text to {args.out}")
    else:
        print(text)

if __name__ == "__main__":
    main()
