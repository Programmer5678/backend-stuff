import argparse
import base64
import re
import string
from reedsolo import RSCodec, ReedSolomonError


# Standard Base64 alphabet
B64_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

# Mapping: char -> number
B64_TO_NUM = {ch: i for i, ch in enumerate(B64_ALPHABET)}

# print(B64_TO_NUM['r'])

# Mapping: number -> char
NUM_TO_B64 = {i: ch for i, ch in enumerate(B64_ALPHABET)}

SEP = "#"

# Helper functions
def base64_char_to_num(ch):
    
    # print(B64_TO_NUM)
    
    # print( ord( ch ) )
    
    """Convert Base64 character to number (0-63)."""
    return B64_TO_NUM[ch]

def num_to_base64_char(num):
    """Convert number (0-63) to Base64 character."""
    if not (0 <= num < 64):
        raise ValueError("Number must be in 0-63")
    return NUM_TO_B64[num]
    
    
    
def remove_all_whitespace(s: str) -> str:
    return "".join(s.split())
 
# cant handle deletions.inserts. might have to look towards sync strings, guessing delete position for small number of deletes/inserts - perhaps  2
# https://www.cs.cmu.edu/~venkatg/teaching/au18-coding-theory/lec-scribes/insdel-coding.pdf
def decode_file(encoded_file):
    """
    Reads an RS-encoded file (Base64 symbols separated by SEP), decodes it,
    and returns the original Base64 string.
    """
    # Read file
    with open(encoded_file, "r") as f:
        data = remove_all_whitespace( f.read() )
        
        

    # Split chunks. chunks are seperated by one(or more) SEP in a row
    encoded_chunks = re.split(f"{SEP}+", data)

    rsc = RSCodec(nsym=15, c_exp=6)  # same parameters as encode

    decoded_b64 = []

    for e_chunk in encoded_chunks:
        
        
        # Convert each Base64 char back to integer
        e_chunk_nums = [base64_char_to_num(ch) for ch in e_chunk ]
                
        # RS decode expects bytes
        try: 
            decoded_nums = rsc.decode(e_chunk_nums)[0]
        except Exception as e: 
            raise e from Exception(f"error decoding {e_chunk}")
        
        chunk_str = "".join( [ num_to_base64_char(n) for n in decoded_nums ] )
        # print(chunk_str)
        
        decoded_b64.append(chunk_str)
        

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
        
        chunk = b64_data[i:i+chunk_size] # get chunk
        chunk_nums = [ base64_char_to_num(ch) for ch in chunk] # convert to number between 0-63 so can be 
        #coefficient of polyonomial over GF(64)
        encoded_chunk = rsc.encode(chunk_nums) # encode - get 64 values in GF(64). any correct 48 uniquely define it
        # though doesnt allow 64-48 errors - rather (64-48)/2 errors. because these are unknown errors. not ommision - could be misread. so need PGZ algo do find em
        encoded_chunk_str = "".join( [ num_to_base64_char(ch) for ch in list( encoded_chunk ) ] ) #join the GF(64) vals as base64 chars
        

        encoded_chunks.append(encoded_chunk_str)
        
    encoded_str = ( 3 * SEP ) .join( encoded_chunks ) #3 seps - for redundancy if ocr misses one of em.
        
        
    with open(output_file, "w") as f:
        f.write(encoded_str)
    
    
    # print( decode_file(output_file) )
        
        
 

