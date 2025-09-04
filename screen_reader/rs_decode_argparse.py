import os
import argparse
from rs_encoding import decode_file

parser = argparse.ArgumentParser(description="RS decode a Base64 file (RS(64,48))")
parser.add_argument("--input", "-i", required=True, help="Path to input file or directory")
args = parser.parse_args()

output_file = "result.b64"

if os.path.isdir(args.input):
    # Process all files in directory
    with open(output_file, "w", encoding="utf-8") as out_f:
        for fname in sorted(os.listdir(args.input)):
            fpath = os.path.join(args.input, fname)
            if os.path.isfile(fpath):
                decoded = decode_file(fpath)
                out_f.write(decoded)
else:
    # Single file case
    decoded = decode_file(args.input)
    with open(output_file, "w", encoding="utf-8") as out_f:
        out_f.write(decoded)
