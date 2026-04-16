from .decode import decode
import argparse

def main():
    parser = argparse.ArgumentParser(description="Read QR image(s) and write raw bytes to a single output file.")
    parser.add_argument('-i', '--input', required=True, help="Input file or directory containing image files")
    parser.add_argument('-o', '--output', required=True, help="Output file path (binary, will be overwritten)")
    parser.add_argument('--base45', action='store_true', help="Decode QR text as Base45 before writing bytes")
    args = parser.parse_args()

    decode(args.input, args.output, args.base45 )

if __name__ == "__main__":
    main()