from PIL import Image
import pytesseract

path = r""

image = Image.open(path)

print("IMAGE MODE:", image.mode)
print("IMAGE SIZE:", image.size)

image = image.convert("RGB")

text = pytesseract.image_to_string(
    image,
    config="--psm 6",
)

print("OCR RESULT:")
print(repr(text))
