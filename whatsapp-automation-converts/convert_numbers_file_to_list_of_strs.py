# Read numbers from file
with open('numbers.txt') as f:
    lines = f.read().splitlines()

# Clean and format numbers
cleaned_numbers = []
for line in lines:
    number = line.replace('-', '')        # remove dashes
    if number.startswith('0'):
        number = '972' + number[1:]       # replace starting 0 with 972
    cleaned_numbers.append(number)

# Print formatted output
print('\"' + '\",\n\"'.join(cleaned_numbers) + '\"')
