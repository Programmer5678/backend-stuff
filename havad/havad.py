import gzip
import base64
import io
import urllib.parse
import json


encoded_compressed_base64 = """ 
H4sIAAAAAAAAA3WQMW7DMAxF76K5SxVP3YLuQZcegLbomIhEGRTd1Ahy98SQ7FRBOv73BOF%2FXowDRfNhzJvpSZIeIJQ4oqTI4A9TaFEyC5F1SN%2FsVtBDIE8gpHMGEv36HYJOgu854S%2BE0a%2BpOFs5W7ld5XaVayrXrN2UfkApcs6O%2Bp66yeu8F4SUYZpIob1X1vkzhhEEXRZn8p74yJjSXQTgwrscUB6H2dDXEHkbi66F7vR49edUy7Cmqa9VxiYV5KMOJZ4RTksF%2B1%2BpIsA5WpaCXziypqdq9kVdu%2FW93gCpiaIV9wEAAA%3D%3D"""
# Example: compressed Base64 string (from JS gzip + btoa)
compressed_base64 = decoded_string = urllib.parse.unquote(encoded_compressed_base64)

# Step 1: Decode from Base64 to bytes
compressed_bytes = base64.b64decode(compressed_base64)

# Step 2: Decompress using gzip
with gzip.GzipFile(fileobj=io.BytesIO(compressed_bytes)) as f:
    decompressed_bytes = f.read()

# Convert bytes to string
decompressed_text = decompressed_bytes.decode('utf-8')

json_input = json.loads(decompressed_text)

print("Decompressed:", json_input)


script_str = ""
for (name, val) in json_input.items():
    
    # formatted_val = val
    
    # if isinstance(val, str):
    #     formatted_val = "'" + val + "'"
    
    script_str += f"document.getElementsByName('{name}')[0].value = '{val}';\n" 
    
    with open("solider-form2.js", 'w') as file:
        file.write(script_str)
    
    
print(script_str)

