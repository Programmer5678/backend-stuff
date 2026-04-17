import argparse
from .encode import encode

def main():
    parser = argparse.ArgumentParser(description="Split file into QR-40 sized Base45 chunks.")
    parser.add_argument('-i', '--input', required=True, help="Input file path")
    parser.add_argument('-o', '--output', required=True, help="Output folder for QR images")
    parser.add_argument('--ecc', choices=['L','M','Q','H'], default='Q', help="QR error correction level (default Q)")
    parser.add_argument('--box-size', type=int, default=8, help="Pixels per module (default 8)")
    parser.add_argument('--border', type=int, default=4, help="Quiet zone in modules (default 4)")
    args = parser.parse_args()

    encode(args.input, args.output, args.ecc, args.box_size, args.border)


if __name__ == "__main__":
    main()
