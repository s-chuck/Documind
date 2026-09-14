from PIL import Image
import pytesseract

path = r"C:\Users\aswal\Desktop\Documind\storage\0dfbefab-0edd-4235-8f41-cf2f85536dcd.png"

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