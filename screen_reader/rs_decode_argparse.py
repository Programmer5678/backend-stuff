import base64
import os
import argparse
from rs_encoding import decode_dir, decode_file


def remove_all_whitespace(s: str) -> str:
    return "".join(s.split())

parser = argparse.ArgumentParser(description="RS decode a Base64 file (RS(64,48))")
parser.add_argument("--input", "-i", required=True, help="Path to input file or directory")
parser.add_argument("--output", "-o", required=True, help="Path to output file or directory")

args = parser.parse_args()

decode_dir(args.input, args.output) if os.path.isdir(args.input) else decode_file(args.input, args.output) 
