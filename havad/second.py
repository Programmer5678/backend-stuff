import os
from generator import html_to_js_string


def splitUp():
    
    with open("solider-form-base.html", "r", encoding="utf-8") as f:
        html = f.read()
    # Case-insensitive split on </body>
    parts = html.split("</body>", 1)

    if len(parts) == 2:
        htmlStart = html[:len(parts[0])]
        htmlEnd = html[len(parts[0]):]
        
        return ( htmlStart, htmlEnd )
    else:
        raise ValueError("</body> tag not found.")


def createFile(htmlStart, htmlEnd, htmlStartJsStr, htmlEndJsStr):
    submitHandler = ""
    with open("submit-handler.js", "r", encoding="utf-8") as f:
        submitHandler = f.read()

    with open("solider-form.html", "w", encoding="utf-8") as f:
        f.write(htmlStart)
        f.write("\n<script>\n")
        f.write(htmlStartJsStr)
        f.write(htmlEndJsStr)
        f.write(submitHandler)
        f.write("\n</script>\n")
        f.write(htmlEnd)


(htmlStart, htmlEnd) = splitUp()

with open("htmlStart.txt", "w", encoding="utf-8") as f:
    f.write(htmlStart)

with open("htmlEnd.txt", "w", encoding="utf-8") as f:
    f.write(htmlEnd)

htmlStartJsStr = "const htmlStart = " + html_to_js_string("htmlStart.txt")  + ";"
htmlEndJsStr = "const htmlEnd = " + html_to_js_string("htmlEnd.txt") + ";"

# print(htmlStartJsStr)
# print(htmlEndJsStr)

createFile( htmlStart, htmlEnd, htmlStartJsStr, htmlEndJsStr )


