import argparse
from rs_encoding import encode_file


parser = argparse.ArgumentParser(description="RS encode a Base64 file (RS(64,48))")
parser.add_argument("--input", "-i", required=True, help="Path to input file")
parser.add_argument("--output", "-o", required=True, help="Path to output encoded file")
# parser.add_argument(
#     "--needb64", "-n",
#     required=True,
#     choices=["true", "false"],
#     help="Specify whether to Base64 encode first (true/false)"
# )
args = parser.parse_args()

# needb64 = True if args.needb64 == "true" else False

encode_file(args.input, args.output )