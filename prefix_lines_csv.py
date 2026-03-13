with open("contacts.csv", "r") as f:
    old = f.read()
    
old_lines = old.splitlines()

new_lines = [ f"PotentialMay_{index}_{line}" for index, line in enumerate(old_lines) ]

new = "\n".join(new_lines)

with open("contacts.csv", "w") as f:
    f.write(new)