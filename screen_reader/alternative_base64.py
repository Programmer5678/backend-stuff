# Base64 alphabet

# B64_ALPHABET = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

from constants import ALTERNATIVE_BASE64_ALPHABET


def alt_b64encode(data: bytes) -> bytes:
    """Encode bytes to Base64 (returns bytes)."""
    bits = ''.join(f'{byte:08b}' for byte in data)  # convert all bytes to bit string
    # pad bits to multiple of 6
    padding_bits = (6 - len(bits) % 6) % 6
    bits += '0' * padding_bits

    # convert each 6-bit chunk to a Base64 character
    b64 = bytes([ALTERNATIVE_BASE64_ALPHABET[int(bits[i:i+6], 2)] for i in range(0, len(bits), 6)])

    return b64


def alt_b64decode(b64_data: bytes) -> bytes:
    """Decode Base64 bytes back to original bytes, without relying on '=' padding.
    Validates that truncated bits are indeed null padding bits.
    """
    # strip '=' if present (optional, some encoders omit padding)
    # b64_data = b64_data.rstrip(b'=')

    # convert Base64 chars to bit string
    bits = ''.join(f'{ALTERNATIVE_BASE64_ALPHABET.index(byte):06b}' for byte in b64_data)

    # check and remove extra bits so length is divisible by 8
    extra = len(bits) % 8
    if extra:
        # validate trailing bits are actually zero padding
        if any(bit != "0" for bit in bits[-extra:]):
            raise ValueError("Invalid Base64: non-zero padding bits detected")
        bits = bits[:-extra]

    # convert each 8-bit chunk to bytes
    decoded = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    return decoded





# Helper functions
def alternative_base64_char_to_num(ch):
    
    """Convert Base64 character to number (0-63)."""
    try:
        return ALTERNATIVE_BASE64_ALPHABET.decode("ascii").index(ch)
    except:
        print(f"could not decode {ch}")

def num_to_alternative_base64_char(num):
    """Convert number (0-63) to Base64 character."""
    if not (0 <= num < 64):
        raise ValueError("Number must be in 0-63")
    
    return ALTERNATIVE_BASE64_ALPHABET.decode("ascii")[num]

