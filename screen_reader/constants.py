# SYNC_SYMBOLS = ['&', '$', '!', ',']
#  [ '&', '$', '<', '/']  
TOTAL_EXPECTED_LEN = 63  # total expected length without syncs
SYNC_GAP = 3  # number of data symbols between syncs
ERASURE_CHAR = "^"

DECODED_CHUNK_SIZE = 48  # 48 data symbols per block

# Standard Base64 alphabet
# B64_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

# # Mapping: char -> number
# B64_TO_NUM = {ch: i for i, ch in enumerate(B64_ALPHABET)}

# # print(B64_TO_NUM['r'])

# # Mapping: number -> char
# NUM_TO_B64 = {i: ch for i, ch in enumerate(B64_ALPHABET)}

# SEP = "#"


# Simple conservative map of common visual lookalikes -> ASCII
LOOKALIKE_MAP = {
    # Cyrillic -> Latin (common confusables)
    # "а": "a", "А": "A",
    # "в": "b", "В": "B",
    # "с": "c", "С": "C",
    # "е": "e", "Е": "E",
    # "о": "o", "О": "O",
    # "р": "p", "Р": "P",
    # "к": "k", "К": "K",
    # "м": "m", "М": "M",
    # "н": "n", "Н": "H",  # uppercase Н looks like Latin H
    # "т": "t", "Т": "T",
    # "х": "x", "Х": "X",
    # "у": "y", "У": "Y",
    # "г": "r",             # your problematic case: Cyrillic г -> Latin r
    # "і": "i",             # Ukrainian i
    # "ј": "j",             # Cyrillic small je -> j

    # # Greek -> Latin (some common ones)
    # "ο": "o", "О": "O",
    # "α": "a", "Α": "A",
    # "ρ": "p", "Ρ": "P",
    # "ι": "i", "Ι": "I",
    # "κ": "k", "Κ": "K",
    # "τ": "t", "Τ": "T",
    # "ν": "v", "Ν": "N",
    # "μ": "m", "Μ": "M",

    # # Fullwidth digits/punct you might see
    # "０": "0", "１": "1", "２": "2", "３": "3", "４": "4",
    # "５": "5", "６": "6", "７": "7", "８": "8", "９": "9",
    # "＃": "#", "＄": "$", "＠": "@",
    # "，": ",", "．": ".", "：": ":", "；": ";", "！": "!", "？": "?",
    
    
    # "¡" : "i",  # upside-down i
    # "Ｉ" : "I", # fullwidth I    
    
    
    #    # -----------------------
    # # Latin letters with diacritics -> ASCII
    # # Uppercase
    # # -----------------------
    # "Ā": "A", "Ă": "A", "Ą": "A", "Á": "A", "À": "A", "Â": "A", "Ä": "A", "Ã": "A", "Å": "A",
    # "Ć": "C", "Ĉ": "C", "Ċ": "C", "Č": "C",
    # "Ď": "D", "Đ": "D",
    # "Ē": "E", "Ĕ": "E", "Ė": "E", "Ę": "E", "Ě": "E", "É": "E", "È": "E", "Ê": "E", "Ë": "E",
    # "Ĝ": "G", "Ğ": "G", "Ġ": "G", "Ģ": "G",
    # "Ĥ": "H", "Ħ": "H",
    # "Ĩ": "I", "Ī": "I", "Į": "I", "İ": "I", "Í": "I", "Ì": "I", "Î": "I", "Ï": "I",
    # "Ĵ": "J",
    # "Ķ": "K",
    # "Ĺ": "L", "Ļ": "L", "Ľ": "L", "Ł": "L",
    # "Ń": "N", "Ņ": "N", "Ň": "N", "Ñ": "N",
    # "Ō": "O", "Ŏ": "O", "Ő": "O", "Ó": "O", "Ò": "O", "Ô": "O", "Ö": "O", "Õ": "O",
    # "Ŕ": "R", "Ŗ": "R", "Ř": "R",
    # "Ś": "S", "Ŝ": "S", "Ş": "S", "Š": "S",
    # "Ť": "T", "Ţ": "T", "Ŧ": "T",
    # "Ũ": "U", "Ū": "U", "Ů": "U", "Ű": "U", "Ų": "U", "Ú": "U", "Ù": "U", "Û": "U", "Ü": "U",
    # "Ŵ": "W",
    # "Ŷ": "Y", "Ÿ": "Y",
    # "Ź": "Z", "Ż": "Z", "Ž": "Z",

    # # -----------------------
    # # Lowercase
    # # -----------------------
    # "ā": "a", "ă": "a", "ą": "a", "á": "a", "à": "a", "â": "a", "ä": "a", "ã": "a", "å": "a", "ċ": "c",
    # "ć": "c", "ĉ": "c", "č": "c", "ç": "c",
    # "ď": "d", "đ": "d",
    # "ē": "e", "ĕ": "e", "ė": "e", "ę": "e", "ě": "e", "é": "e", "è": "e", "ê": "e", "ë": "e",
    # "ĝ": "g", "ğ": "g", "ġ": "g", "ģ": "g",
    # "ĥ": "h", "ħ": "h",
    # "ĩ": "i", "ī": "i", "į": "i", "ı": "i", "í": "i", "ì": "i", "î": "i", "ï": "i",
    # "ĵ": "j",
    # "ķ": "k",
    # "ĺ": "l", "ļ": "l", "ľ": "l", "ł": "l",
    # "ń": "n", "ņ": "n", "ň": "n", "ñ": "n",
    # "ō": "o", "ŏ": "o", "ő": "o", "ó": "o", "ò": "o", "ô": "o", "ö": "o", "õ": "o",
    # "ŕ": "r", "ŗ": "r", "ř": "r",
    # "ś": "s", "ŝ": "s", "ş": "s", "š": "s",
    # "ť": "t", "ţ": "t", "ŧ": "t",
    # "ũ": "u", "ū": "u", "ů": "u", "ű": "u", "ų": "u", "ú": "u", "ù": "u", "û": "u", "ü": "u",
    # "ŵ": "w",
    # "ŷ": "y", "ÿ": "y",
    # "ź": "z", "ż": "z", "ž": "z",
    
    
    # "Ạ" : "A",  # A with dot below
    # "ạ" : "a",  # a with dot below
    # "Ĳ" : "IJ", # ligature
    # "ĳ" : "ij", # ligature
    
    # "|" : "l",  # common substitution
    # "$": "S",  # common substitution
    # "@": "a",  # common substitution
    # "%" : "#",
    
    
    "S" : "$",
    "\U00011089": "*",   # 𑂉 (Kaithi digit three, but visually star-like) → '*'
    "⭑": "*" ,          # Black small star → '*'
    "0" : "o" ,
    "O" : "o",
    "1" : "I"
    
}


SEP = "G"
SYNC_SYMBOLS = ['E', 'R', '7', 'B']

NUM_OF_DIGITS_LEN_OF_INPUT = 10

ALTERNATIVE_BASE64_ALPHABET = b"H5Db6t&mra9fe4AjJF8MhndPgTYQN*3u<p%yU/!ikqvIw>KcCL2s,?WoXVZ$\"x;#"
