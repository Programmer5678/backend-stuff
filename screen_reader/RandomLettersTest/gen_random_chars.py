import random
import string

# All human-readable ASCII characters (printable, without \t\n\r\x0b\x0c)
chars = string.printable[:-6]

# Number of characters to generate
num_chars = 13000

# Generate random characters
random_chars = ''.join(random.choices(chars, k=num_chars))

# Option 1: Print to console
print(random_chars)

# Option 2: Save to a file
with open("random_ascii_13k.txt", "w", encoding="utf-8") as f:
    f.write(random_chars)

print("Generated 13,000 random ASCII characters in 'random_ascii_13k.txt'")
