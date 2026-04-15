import re

def html_to_js_string(filename):
    output = '"'

    with open(filename, "r", encoding="utf-8") as file:
        for index, line in enumerate(file):
            if index != 0:
                output += ' + "'

            trimmed_line = line[:-1] if line.endswith('\n') else line

            processed_line = re.sub('<', '<" + "', re.sub('"', '\\"', trimmed_line))

            output += (processed_line + ' \\n"\n')

    return output


        
