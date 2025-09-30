import argparse
import base64
import os
import re
import string
from reedsolo import RSCodec, ReedSolomonError
from constants import *
from alternative_base64 import alt_b64decode, alt_b64encode, alternative_base64_char_to_num, num_to_alternative_base64_char


    
    
def remove_all_whitespace(s: str) -> str:
    return "".join(s.split())



# DECODED_CHUNK_SIZE = 48  # 48 data symbols per block

# def decode_chunk(e_chunk):
#     """
#     Decodes a single RS-encoded chunk (64 Base64 characters) and returns the original 48-character Base64 string.
#     """
    
#     rsc = RSCodec(nsym=63-DECODED_CHUNK_SIZE+1, c_exp=6)  # same parameters as encode
    
#     # Convert each Base64 char back to integer
#     e_chunk_nums = [base64_char_to_num(ch) for ch in e_chunk]
    
#     # RS decode expects bytes
#     try: 
#         decoded_nums = rsc.decode(e_chunk_nums)[0]
#     except ReedSolomonError as e: 
#         raise Exception(f"error decoding {e_chunk}") from e
    
#     # Convert back to Base64 string
#     decoded_chunk_str = "".join( [ num_to_base64_char(n) for n in decoded_nums ] )
    
#     return decoded_chunk_str
 
 
# def encode_chunk(chunk):
#     """
#     Encodes a single chunk (up to 48 Base64 characters) using RS encoding and returns the encoded 63-character Base64 string.
#     """
#     rsc = RSCodec(nsym=63-DECODED_CHUNK_SIZE+1, c_exp=6)  # 15 parity symbols, GF(2^6)

#     # Convert each Base64 char to integer
#     chunk_nums = [ base64_char_to_num(ch) for ch in chunk] # convert to number between 0-63 so can be 
#     #coefficient of polyonomial over GF(64)
#     encoded_chunk = rsc.encode(chunk_nums) # encode - get 64 values in GF(64). any correct 48 uniquely define it
#     # though doesnt allow 64-48 errors - rather (64-48)/2 errors. because these are unknown errors. not ommision - could be misread. so need PGZ algo do find em
#     encoded_chunk_str = "".join( [ num_to_base64_char(ch) for ch in list( encoded_chunk ) ] ) #join the GF(64) vals as base64 chars
    
#     return encoded_chunk_str







def get_rsc(decoded_chunk_size):
    return RSCodec(nsym=TOTAL_EXPECTED_LEN-decoded_chunk_size, c_exp=6)  # 15 parity symbols, GF(2^6)

def rs_encode_chunk(chunk):
    """
    Encodes a single chunk (up to 48 Base64 characters) using RS encoding and returns the encoded 63-character Base64 string.
    """
        
    rsc = get_rsc( len(chunk) )  # 15 parity symbols, GF(2^6)

    # Convert each Base64 char to integer
    chunk_nums = [ alternative_base64_char_to_num(ch) for ch in chunk] # convert to number between 0-63 so can be 
    #coefficient of polyonomial over GF(64)
    encoded_chunk = rsc.encode(chunk_nums) # encode - get 64 values in GF(64). any correct 48 uniquely define it
    # though doesnt allow 64-48 errors - rather (64-48)/2 errors. because these are unknown errors. not ommision - could be misread. so need PGZ algo do find em
    
    # print( [ num_to_alternative_base64_char(ch) for ch in list( encoded_chunk ) ]  )
    encoded_chunk_str = "".join( [ num_to_alternative_base64_char(ch) for ch in list( encoded_chunk ) ] ) #join the GF(64) vals as base64 chars
    
    return encoded_chunk_str



def add_sync_symbols(chunk):
    """
    Adds sync symbols into the chunk after every 3 characters.
    The sync symbols cycle through ['&', '$', '!', ','].
    """
    final_str = []
    for i, ch in enumerate(chunk, 1):  # start from 1 for easier mod
        final_str.append(ch)
        if i % SYNC_GAP == 0:  # after every 4 characters
            final_str.append( SYNC_SYMBOLS[(i // SYNC_GAP - 1) % len(SYNC_SYMBOLS)] )
            
    return "".join(final_str)  




def encode_chunk(chunk):
    return add_sync_symbols( rs_encode_chunk(chunk) )




def expected_distance(sync_chars, sync_a, sync_b):
    """
    Computes the expected distance k (in original data symbols) between two sync symbols
    in a circular list of sync positions.

    Parameters:
    - sync_positions: list of positions (indexes) of all sync symbols in the final chunk
    - sync_a: the reference sync symbol (start)
    - sync_b: the target sync symbol

    Returns:
    - k: expected distance in original data symbols
    """
    if sync_a not in sync_chars or sync_b not in sync_chars:
        raise ValueError("Both sync symbols must be in sync_positions list")

    # Reorder sync_positions so it starts from sync_a
    idx_a = sync_chars.index(sync_a)
    circular_list = sync_chars[idx_a:] + sync_chars[:idx_a]

    # Find index of sync_b in circular list
    idx_b = circular_list.index(sync_b)

    # distance in final chunk indexes (wrap-around handled by circular_list)
    d_index = idx_b if idx_b != 0 else len(sync_chars)  # if same element, full circle

    # expected distance in original data symbols
    k = d_index * SYNC_GAP  # same as distance*3 + distance

    return k

def split_sync_parts(s):
    """
    Splits the input string into alternating data parts and sync symbols.
    Returns (parts, syncs).
    """
    parts = []
    syncs = []
    buffer = ""
    for ch in s:
        if ch in SYNC_SYMBOLS:
            parts.append(buffer)
            buffer = ""
            syncs.append(ch)
        else:
            buffer += ch
    parts.append(buffer)
    return parts, syncs

# def build_corrected_parts(parts, syncs):
#     """
#     Given parts and syncs, build the corrected parts list as in remove_sync_symbols.
#     """
        
#     len_so_far = 0
#     new_parts = []
#     for i, chunk in enumerate(parts):
#         if i == 0:
#             exp_len = (1 + SYNC_SYMBOLS.index( syncs[0] )) * SYNC_GAP
#         elif i == len(parts) - 1:
#             exp_len = TOTAL_EXPECTED_LEN - len_so_far
#         else:
#             sync_a = syncs[i - 1]
#             sync_b = syncs[i]
#             exp_len = expected_distance(SYNC_SYMBOLS, sync_a, sync_b)
#         str_to_add = ERASURE_CHAR * exp_len if (len(chunk) != exp_len or (len(chunk) != SYNC_GAP and i != len(parts) - 1)) else chunk
#         len_so_far += len(str_to_add)
#         new_parts.append(str_to_add)
#     return "".join(new_parts)

def build_corrected_parts(parts, syncs):
    """
    Given parts and syncs, build the corrected parts list as in remove_sync_symbols,
    with debug prints showing replacements with ERASURE_CHAR.
    """
        
        
    len_so_far = 0
    new_parts = []
    for i, chunk in enumerate(parts):
        if i == 0:
            exp_len = (1 + SYNC_SYMBOLS.index(syncs[0])) * SYNC_GAP
        elif i == len(parts) - 1:
            exp_len = TOTAL_EXPECTED_LEN - len_so_far
        else:
            sync_a = syncs[i - 1]
            sync_b = syncs[i]
            exp_len = expected_distance(SYNC_SYMBOLS, sync_a, sync_b)
        
        # Decide whether to replace with ERASURE_CHAR
        if len(chunk) != exp_len or (len(chunk) != SYNC_GAP and i != len(parts) - 1):
            print(f"[DEBUG] Replacing chunk {i} ('{chunk}') with ERASURE_CHAR * {exp_len}")
            str_to_add = ERASURE_CHAR * exp_len
        else:
            str_to_add = chunk
            print(f"[DEBUG] Keeping chunk {i} as-is: '{chunk}'")
        
        len_so_far += len(str_to_add)
        new_parts.append(str_to_add)
    
    result = "".join(new_parts)
    print(f"[DEBUG] Final corrected string length: {len(result)}")
    return result


def remove_sync_symbols(s):
    
    """
    Remove sync symbols and validate/repair substrings between them
    based on expected_distance.
    """
    
    print(f"\n\n\nAttempting to remove sync symbols from {s}\n")
    
    parts, syncs = split_sync_parts(s)
    
    if len(syncs) == 0:
        # No sync symbols, just check length
        raise Exception(f"No sync symbols found in chunk {s}")
    
    return build_corrected_parts(parts, syncs)





def rs_decode_chunk(e_chunk):
    """
    Decodes a single RS-encoded chunk (64 Base64 characters) and returns the original 48-character Base64 string.
    """
    
    ARBITRARY_NUM = 0  # arbitrary number to use for erasures
    
    rsc =  get_rsc( DECODED_CHUNK_SIZE )  # same parameters as encode
    
    erase_pos = [i for i, ch in enumerate(e_chunk) if ch == ERASURE_CHAR]
    
    
    print("e_chunk: ", e_chunk)
    
    
    
    
    # Convert each Base64 char back to integer
    e_chunk_nums = [ alternative_base64_char_to_num(ch) if ch != ERASURE_CHAR else ARBITRARY_NUM for ch in e_chunk]
    
    # RS decode expects bytes
    try: 
        # print( e_chunk_nums, erase_pos )
        decoded_nums = rsc.decode(e_chunk_nums, erase_pos = erase_pos)[0]
    except ReedSolomonError as e: 
        raise Exception(f"error in Reed Solomon decoding {e_chunk}") from e
    
    # Convert back to Base64 string
    decoded_chunk_str = "".join( [ num_to_alternative_base64_char(n) for n in decoded_nums ] )
    
    return decoded_chunk_str

# 2 things we are calculating - does it fit and if it doesnt how many 
def decode_chunk(chunk):
    
    if len(chunk) < 10:
        return False
    
    return rs_decode_chunk( remove_sync_symbols(chunk) )
    
    
def test_add_and_remove_sync_symbol_funcs_work( test_input , test_output ):
        
    print(f"{test_input}\n{test_output}\n\n")
    
    assert len(test_input) == TOTAL_EXPECTED_LEN
    assert len(test_output) == TOTAL_EXPECTED_LEN
    
    for i in range(len(test_input)):
        assert test_output[i] == ERASURE_CHAR or test_input[i] == test_output[i]
    
    
def test_encode_decode_chunk_funcs_work(add_errors_func):
    # test encode and decode chunk functions work correctly
    input_str = "QUJDREVGR0hJSktMTU5PUFFSU1RVVldYWVo0NTY3ODkwMTIz"
    encoded = encode_chunk( input_str )
    encoded_with_errors = add_errors_func( encoded )
    
    
    try:
    
        assert input_str == decode_chunk( encoded_with_errors )
        
        print(
            f"Original:            {input_str}\n"
            f"Encoded:             {encoded}\n"
            f"WithErr:             {encoded_with_errors}\n"
            f"Remove sync symbols: {remove_sync_symbols(encoded_with_errors)}\n"
            f"Decoded:             {decode_chunk(encoded_with_errors)}\n"
        )
        
    except:
        print(
            f"Original:            {input_str}\n"
            f"Encoded:             {encoded}\n"
            f"WithErr:             {encoded_with_errors}\n"
            f"Remove sync symbols: {remove_sync_symbols(encoded_with_errors)}\n"
        )
        
        raise 
        
    
    
    
def battery_of_tests():
    
    ARBITRARY_ERROR_CHAR = "L"
    
    test_encode_decode_chunk_funcs_work( lambda x: x ) # no errors
    test_encode_decode_chunk_funcs_work( lambda s : s[:5] + s[6:] ) # delete one char
    test_encode_decode_chunk_funcs_work( lambda s: s[:5] + ARBITRARY_ERROR_CHAR + s[5:] ) # insert one char
    test_encode_decode_chunk_funcs_work( lambda s: s[:5] + 3 * ARBITRARY_ERROR_CHAR + s[5:16] + s[17:] ) # insert multiple char + delete one char
    test_encode_decode_chunk_funcs_work( lambda s: ARBITRARY_ERROR_CHAR + s )  # insert at start 
    test_encode_decode_chunk_funcs_work( lambda s: s + ARBITRARY_ERROR_CHAR ) # insert at end   
    test_encode_decode_chunk_funcs_work( lambda s: s[:SYNC_GAP] + ARBITRARY_ERROR_CHAR + s[SYNC_GAP+1:] ) # change first sync char
    test_encode_decode_chunk_funcs_work( lambda s: ARBITRARY_ERROR_CHAR + s[:SYNC_GAP] + ARBITRARY_ERROR_CHAR + s[SYNC_GAP+1:] ) # change first sync char and insert at start
    
    test_encode_decode_chunk_funcs_work( 
    lambda s: s[:5] + ARBITRARY_ERROR_CHAR + s[5:16] + s[17:20] + ARBITRARY_ERROR_CHAR + s[20:22] + ARBITRARY_ERROR_CHAR + s[22:]  )
    # insert 3 char + delete one char
    
    test_encode_decode_chunk_funcs_work( lambda s: s[ :(2*SYNC_GAP+1) ] + ARBITRARY_ERROR_CHAR + s[ (2*SYNC_GAP+2) :] ) # change second sync char
    test_encode_decode_chunk_funcs_work( lambda s: s[ :(2*SYNC_GAP+1) ] + ARBITRARY_ERROR_CHAR + s[ (2*SYNC_GAP+2) : 16] + s[ 17 :] ) # change second sync char + delete one char
    
        
# battery_of_tests()

 
# # in cases where chunk is 63 or 65 chars long, try to fix it by removing or adding a char
# # we should not fear false positives as we have 15 parity symbols and rarely will a random string decode to something valid
# # although the chance does increase as we test more possibilities
# # Future - we could add a checksum to each chunk to verify correctness or use sync strings to handle insertions/deletions
# # for now just try removing or adding a char and see if it decodes
# # otherwise raise error
# def decode_chunk_with_fixes(e_chunk):
    
            
#     if len(e_chunk) == TOTAL_EXPECTED_LEN:
#         decode_chunk_str = decode_chunk(e_chunk)
#         return decode_chunk_str
    
#     elif len(e_chunk) == TOTAL_EXPECTED_LEN + 1: 
#         for i in range(len(e_chunk)):
#             try:
#                 decode_chunk_str = decode_chunk( e_chunk[:i] + e_chunk[i+1:] )
#                 print(f"Warning: chunk length 65, removed char at pos {i} ({e_chunk[i]}) to decode")
                
#                 return decode_chunk_str
#             except ReedSolomonError:
#                 continue
            
#         raise ValueError(f"Encoded chunk {e_chunk} must be exactly 63 Base64 characters. It was 644, likely due to an extra character. Tried removing each character to decode. Did not succeed.")
            
#     elif len(e_chunk) == TOTAL_EXPECTED_LEN - 1:
        
#         ARBITRARY_CHAR = "A" # could be anything in base64 alphabet
        
#         for i in reversed(range(len(e_chunk))):
#             try:
#                 try_fix = e_chunk[:i] + ARBITRARY_CHAR + e_chunk[i:]
                
#                 # print(f"Trying to insert {ARBITRARY_CHAR} at pos {i} in {e_chunk} to get {try_fix}")
                
#                 decode_chunk_str  = decode_chunk( try_fix )
                
#                 #Note -  we may not insert at the "correct" position, but if we get a valid decode, it is likely correct as out parity symbols make false positives unlikely
#                 # Much more likely is that we have so many correct symbols that define the chunk that we can correct even with wrong insert position
#                 print(f"Warning: chunk length 62, inserted arbitrary char {ARBITRARY_CHAR} at pos {i} to decode {try_fix} to {decode_chunk_str}")
#                 return decode_chunk_str
            
#             except ReedSolomonError:
#                 continue
            
#         raise ValueError(f"Encoded chunk {e_chunk} must be exactly 63 Base64 characters. It was 62, likely due to a missing character. Tried adding character to decode. Did not succeed.")
        

#     else:
#         raise ValueError(f"Encoded chunk must be exactly 63 Base64 characters. It was {len(e_chunk)}")
    
    
 
# # cant handle deletions.inserts. might have to look towards sync strings, guessing delete position for small number of deletes/inserts - perhaps  2
# # https://www.cs.cmu.edu/~venkatg/teaching/au18-coding-theory/lec-scribes/insdel-coding.pdf
# def decode_file(encoded_file):
#     """
#     Reads an RS-encoded file (Base64 symbols separated by SEP), decodes it,
#     and returns the original Base64 string.
#     """
#     # Read file
#     with open(encoded_file, "r") as f:
#         data = remove_all_whitespace( f.read() )

#     # Split chunks. chunks are seperated by one(or more) SEP in a row
#     encoded_chunks = [ e for e in re.split(f"{SEP}+", data) if e != "" ]
    
#     print(encoded_chunks)
#     exit(-1)

#     rsc = RSCodec(nsym=15, c_exp=6)  # same parameters as encode

#     decoded_b64 = []

#     for e_chunk in encoded_chunks:
        
#         # decode_chunk_str = decode_chunk(e_chunk)
        
#         try:
#             decode_chunk_str = decode_chunk_with_fixes(e_chunk)
#         except Exception as e:
#             raise e from Exception(f"decoded_b64 at time of error: {decoded_b64}")    
        
#         decoded_b64.append( decode_chunk_str )
        
        
        
        
        
        
        

#     # Return as a single string
#     return "".join(decoded_b64)
# cant handle deletions.inserts. might have to look towards sync strings, guessing delete position for small number of deletes/inserts - perhaps  2
# https://www.cs.cmu.edu/~venkatg/teaching/au18-coding-theory/lec-scribes/insdel-coding.pdf
def decode_chunks_from_str(encoded_str : str, encoded_file_name) -> str:
    """
    Reads an RS-encoded file (Base64 symbols separated by SEP), decodes it,
    and returns the original Base64 string.
    """
    # # Read file
    # with open(encoded_file, "r") as f:
    #     data = remove_all_whitespace( f.read() )
    
    data = remove_all_whitespace( encoded_str )

    # Split chunks. chunks are seperated by one(or more) SEP in a row
    encoded_chunks = [ e for e in re.split(f"{SEP}+", data) if e != "" ]
    
    # print(encoded_chunks)


    decoded_b64 = []

    for e_chunk in encoded_chunks:
        
        # decode_chunk_str = decode_chunk(e_chunk)
        
        if len(e_chunk) < 10: # may not be "real" chunk - because of insert of non-seps between seps or of seps themselves(which is often unsalvageable)
            print(f"Warning: chunk too short to decode (less than 10 chars): {e_chunk} in file {encoded_file_name}, skipping")
            continue
        
        try:
            decode_chunk_str = decode_chunk(e_chunk)
        except Exception as e:
            raise Exception(f"Problem is in file {encoded_file_name} , decoded_b64 at time of error: {decoded_b64}") from e
        
        decoded_b64.append( decode_chunk_str )
        
    # Return as a single string
    return "".join(decoded_b64)












def handle_split_chunk(content_cur, file_list, index, input_dir):
    """Check and decode a chunk split between current and next file."""
    fpath_next = os.path.join(input_dir, file_list[index+1]) if index < len(file_list) - 1 else None
    # Check for chunk that might be split between current and next file    
    if fpath_next:
        with open(fpath_next, "r", encoding="utf-8") as f:
            content_next = remove_all_whitespace(f.read())
            
        # Check if current file ends with SEP and next file starts with SEP
        if content_cur and content_next and not (content_cur.endswith(SEP) or content_next.startswith(SEP)):
            end_cur = content_cur.split(SEP)[-1]
            start_next = content_next.split(SEP)[0]
            
            in_between_files_chunk = end_cur + start_next
            
            print(f"Start decoding chunk split between files {file_list[index]} and {file_list[index+1]}: {in_between_files_chunk}")
            
            decoded = decode_chunks_from_str(in_between_files_chunk, f"In between {file_list[index]} and next file") # try to decode chunk split between files
            
            print(f"Finished decoding chunk split between files {file_list[index]} and {file_list[index+1]}: {in_between_files_chunk}")
            
            return decoded
        
    return ""


def decoded_chunks_to_final_res(s : str) -> bytes:
    
    """
    Decode string back to raw bytes.
    Expects 10 ASCII digits prefix with original length.
    """
    as_bytes = alt_b64decode(s.encode("ascii"))
    
    # Extract length (first 10 bytes are ASCII digits)
    len_of_original = int(as_bytes[:NUM_OF_DIGITS_LEN_OF_INPUT].decode("ascii"))
    
    # Extract only the original data portion
    return as_bytes[NUM_OF_DIGITS_LEN_OF_INPUT:NUM_OF_DIGITS_LEN_OF_INPUT + len_of_original]



def decode_file(input_file: str, output_file: str):
    """
    Read a single file, decode it, and write to output file.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        data = f.read()
        
    res = decoded_chunks_to_final_res( decode_chunks_from_str(data, input_file) )

    with open(output_file, "wb") as f:
        f.write( res )


def decode_dir_content(input_dir: str) -> bytes:
    """
    Decode all files in a directory (assumes RS/Base64 + SEP encoding) and
    return the decoded bytes.
    """
    res_b64 = ""
    file_list = sorted(os.listdir(input_dir))  # sort to ensure order

    for index, fname in enumerate(file_list):
        print(f"Start decoding file {index+1}/{len(file_list)}: {fname}")
        fpath_cur = os.path.join(input_dir, fname)

        with open(fpath_cur, "r", encoding="utf-8") as f:
            content_cur = remove_all_whitespace(f.read())

        # Remove the first and last SEP wrappers
        main_part = content_cur.rsplit(SEP, 1)[0].split(SEP, 1)[1]

        # Decode the main part
        decoded = decode_chunks_from_str(main_part, fname)
        res_b64 += decoded

        print(f"Finished decoding file {index+1}/{len(file_list)}: {fname}")

        # Handle chunk split between current and next file
        res_b64 += handle_split_chunk(content_cur, file_list, index, input_dir)

    # Finally decode Base64 to bytes
    return decoded_chunks_to_final_res( res_b64 )


def decode_dir(input_dir: str, output_file: str):
    """
    Decode all files in a directory and write the fully decoded bytes to output file.
    """
    decoded_bytes = decode_dir_content(input_dir)

    with open(output_file, "wb") as f:
        f.write(decoded_bytes)



def encode_chunks_of_str(data: bytes) -> str:
    """
    Core function:
    Encode raw bytes to Base64, chunk, add separators, and return final string.
    """
    
    
    b64_data = alt_b64encode(data).decode("ascii")
    
    encoded_chunks = []
    for i in range(0, len(b64_data), DECODED_CHUNK_SIZE):
        chunk = b64_data[i:i+DECODED_CHUNK_SIZE]
        
        encoded_chunk_str = encode_chunk(chunk)
        encoded_chunks.append(encoded_chunk_str)

    # Join chunks with SEP - 3 SEP for redundancy, remove whitespaces
    encoded_str = 3 * SEP + "".join((3 * SEP).join(encoded_chunks).split()) + 3 * SEP
    return encoded_str


def encode_data_to_str(data: bytes) -> str:
    """
    Wrapper:
    Prepend the data length (as fixed-width ASCII digits) and encode with build_encoded_str.
    """
    
    data_with_len_prepended = str(len(data)).encode("ascii").rjust(NUM_OF_DIGITS_LEN_OF_INPUT, b"0") + data
    return encode_chunks_of_str(data_with_len_prepended)

    


def encode_file(input_file: str, output_file: str):
    """
    Read input file, encode it using encode_data_to_str, and write to output file.
    """
    with open(input_file, "rb") as f:
        data = f.read()

    encoded_str = encode_data_to_str(data)

    with open(output_file, "w") as f:
        f.write(encoded_str)

    
    
        
        
 

