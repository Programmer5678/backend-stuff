import argparse
import base64
import string
from reedsolo import RSCodec, ReedSolomonError


# Standard Base64 alphabet
B64_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

# Mapping: char -> number
B64_TO_NUM = {ch: i for i, ch in enumerate(B64_ALPHABET)}

# Mapping: number -> char
NUM_TO_B64 = {i: ch for i, ch in enumerate(B64_ALPHABET)}

SEP = "###"

# Helper functions
def base64_char_to_num(ch):
    
    # print(B64_TO_NUM)
    """Convert Base64 character to number (0-63)."""
    return B64_TO_NUM[ch]

def num_to_base64_char(num):
    """Convert number (0-63) to Base64 character."""
    if not (0 <= num < 64):
        raise ValueError("Number must be in 0-63")
    return NUM_TO_B64[num]
    
    
def decode_file(encoded_file):
    """
    Reads an RS-encoded file (Base64 symbols separated by SEP), decodes it,
    and returns the original Base64 string.
    """
    # Read file
    with open(encoded_file, "r") as f:
        data = f.read()

    # Split chunks
    encoded_chunks = data.split(SEP)

    rsc = RSCodec(nsym=15, c_exp=6)  # same parameters as encode

    decoded_b64 = []

    for e_chunk in encoded_chunks:
        
        
        
        
        # Convert each Base64 char back to integer
        e_chunk_nums = [base64_char_to_num(ch) for ch in e_chunk ]
        
        # RS decode expects bytes
        decoded_nums = rsc.decode(e_chunk_nums)[0]
        
        chunk_str = "".join( [ num_to_base64_char(n) for n in decoded_nums ] )
        
        print(chunk_str)
        

    # Return as a single string
    return "".join(decoded_b64)


def encode_file(input_file, output_file, needb64):
    # Read input file as bytes
    with open(input_file, "rb") as f:
        data = f.read()

    # Convert to Base64 string (as bytes)
    #actually i dont think we need this...
    b64_data = (base64.b64encode(data) if needb64 else data).decode('ascii').strip(string.whitespace + "=")    
    
    # RSCodec: 16 parity symbols (n=64, k=48)
    rsc = RSCodec(nsym=15, c_exp=6) 
    # Why c_exp=6? for the same reason c_exp = 8 is default. 
    # we transmit our data as 2^6 symbols unlike most data which is in bytes = 2^8. We fail or succeed a char as a whole or not at all. 
    # so avoid one char fail for example 'c' being spread across 2 chars
    chunk_size = 48  # 48 data symbols per block

    encoded_chunks = []
    for i in range(0, len(b64_data), chunk_size):
        
        chunk = b64_data[i:i+chunk_size]
        chunk_nums = [ base64_char_to_num(ch) for ch in chunk]
        encoded_chunk = rsc.encode(chunk_nums)
        encoded_chunk_str = "".join( [ num_to_base64_char(ch) for ch in list( encoded_chunk ) ] )
        
        print("2: ", chunk )
        
        #print( "Chunk: ",chunk, ", encoded: ", encoded, ", encoded length: ", len(encoded) )
        
        encoded_chunks.append(encoded_chunk_str)
        
    encoded_str = SEP.join( encoded_chunks )
        
        
    with open(output_file, "w") as f:
        f.write(encoded_str)
        
    
    
    print( decode_file(output_file) )
        
        
            
        
    # print( encoded_chunks )

    # # Write encoded bytes to output file
    # with open(output_file, "wb") as f:
    #     f.write(b''.join(encoded_chunks))

    # # Test decoding immediately
    # decoded_blocks = []
    # for chunk in encoded_chunks:
    #     try:
    #         decoded_bytes = rsc.decode(chunk)[0]
    #         decoded_blocks.append(decoded_bytes.decode('ascii'))
    #     except ReedSolomonError:
    #         decoded_blocks.append(None)

    # print(decoded_blocks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RS encode a Base64 file (RS(64,48))")
    parser.add_argument("--input", "-i", required=True, help="Path to input file")
    parser.add_argument("--output", "-o", required=True, help="Path to output encoded file")
    parser.add_argument(
        "--needb64", "-n",
        required=True,
        choices=["true", "false"],
        help="Specify whether to Base64 encode first (true/false)"
    )
    args = parser.parse_args()
    
    needb64 = True if args.needb64 == "true" else False

    encode_file(args.input, args.output, needb64 )
