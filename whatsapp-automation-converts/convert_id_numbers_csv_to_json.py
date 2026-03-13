
def reformat(line):
    split = line.split(",")
    id = split[0]
    raw_number = split[1]
    
    number = raw_number.replace('-', '')        # remove dashes
    if number.startswith('0'):
        number = '972' + number[1:]       # replace starting 0 with 972
        
    return r'{"id": "' + id + r'", "phone_number": "' + number + r'"}'

with open("not_interested_may.csv") as f:
    s = f.read()
    lines = [ l for l in s.split("\n") if l.strip() != '' ] 
    lines_as_json = [ reformat(l) for l in lines ]
    
    print(r'"participants": [' + "\n,".join(lines_as_json) + ']')
    