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

output_file_b64 = "decoded_result.b64"


res_b64 = decode_dir(args.input) if os.path.isdir(args.input) else decode_file(args.input) 


with open(output_file_b64, "w", encoding="utf-8") as out_f_b64:
    out_f_b64.write(res_b64)
    
    
res = base64.b64decode(res_b64)    
    
with open(args.output, "wb") as out_f:
    out_f.write(res)