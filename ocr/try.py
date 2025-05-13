import easyocr
reader = easyocr.Reader(['en'])  # 'he' = Hebrew
results = reader.readtext('myimage.webp')
print(results)