from pathlib import Path
import pymupdf
import pytesseract
from PIL import Image, ImageFile, ImageEnhance
import sys
from docx import Document as DocxDocument
sys.stdout.reconfigure(encoding="utf-8")
ImageFile.LOAD_TRUNCATED_IMAGES = True
MIN_NATIVE_TEXT_CHARS = 50


def extract_text_from_txt(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8")

# def extract_text_from_image(file_path: str) -> str:
#     print("IMAGE PROCESSOR CALLED:", file_path)

#     image = Image.open(file_path)

#     # Convert to grayscale
#     image = image.convert("L")

#     # Increase contrast
#     image = ImageEnhance.Contrast(image).enhance(2)

#     # Resize
#     image = image.resize(
#         (image.width * 2, image.height * 2)
#     )

#     # OCR
#     text = pytesseract.image_to_string(
#         image,
#         config="--psm 6"
#     ).strip()

#     print("IMAGE OCR RESULT:", repr(text))

#     return text

def extract_text_from_docx(file_path: str) -> str:
    document = DocxDocument(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs)


def extract_text_from_pdf(file_path: str) -> str:
    pages_text: list[str] = []

    with pymupdf.open(file_path) as document:

        for page_number, page in enumerate(document, start=1):

            # --------------------------------------------------
            # 1. Try native PDF text extraction
            # --------------------------------------------------
            native_text = page.get_text("text").strip()
            print(native_text)
            print("Native length:", len(native_text))
            print("=================================")
            # --------------------------------------------------
            # 2. Decide whether native extraction is sufficient
            # --------------------------------------------------
            word_count = len(native_text.split())

            if len(native_text) >= MIN_NATIVE_TEXT_CHARS and word_count >= 10:
                pages_text.append(
                    f"--- Page {page_number} ---\n"
                    f"{native_text}"
                )
                continue
            # --------------------------------------------------
            # 3. Native text is missing / suspiciously small.
            #    Render the page and use OCR.
            # --------------------------------------------------
            pixmap = page.get_pixmap(
                dpi=300,
                alpha=False,
            )

            image = Image.frombytes(
                "RGB",
                [pixmap.width, pixmap.height],
                pixmap.samples,
            )

            ocr_text = pytesseract.image_to_string(
                image,
                lang="eng+hin",
            ).strip()

            print("\n========== OCR TEXT ==========")
            print(ocr_text)
            print("OCR length:", len(ocr_text))
            print("==============================")

            # --------------------------------------------------
            # 4. Prefer whichever extraction actually produced
            #    useful content.
            # --------------------------------------------------
            if ocr_text:
                pages_text.append(
                    f"--- Page {page_number} ---\n"
                    f"{ocr_text}"
                )
            elif native_text:
                # OCR failed, but native extraction gave us
                # something. Don't throw that information away.
                pages_text.append(
                    f"--- Page {page_number} ---\n"
                    f"{native_text}"
                )

    return "\n\n".join(pages_text)
# def extract_text_from_pdf(file_path: str) -> str:
#     document = pymupdf.open(file_path)

#     pages_text = []
# #According to the below logic if i have text the program will go to if block and append the text but 
# #a pdf have both text and image so we have to come up with a new stratergy bcs if we only consider this much
# #then it won't be a good extractor

#     # for page in document:
#     #     text = page.get_text().strip()

#     #     if text:
#     #         # Normal text PDF
#     #         pages_text.append(text)

#     #     else:
#     #         # Scanned/image PDF → OCR
#     #         pixmap = page.get_pixmap(dpi=300)

#     #         image = Image.frombytes(
#     #             "RGB",
#     #             [pixmap.width, pixmap.height],
#     #             pixmap.samples,
#     #         )

#     #         ocr_text = pytesseract.image_to_string(image)

#     #         pages_text.append(ocr_text.strip())
#     for page_number, page in enumerate(document, start=1):
#         # 1. Extract embedded PDF text
#         text = page.get_text().strip()

#         page_content = []

#         if text:
#             page_content.append(text)

#         # 2. Find images on the page
#         images = page.get_images(full=True)

#         if images:

#             # Render the entire page as an image
#             pixmap = page.get_pixmap(dpi=300)

#             image = Image.frombytes(
#                 "RGB",
#                 [pixmap.width, pixmap.height],
#                 pixmap.samples,
#             )

#             # OCR the rendered page
#             ocr_text = pytesseract.image_to_string(image, lang="eng+hin").strip()

#             if ocr_text:
#                 page_content.append(ocr_text)
#             #3. Store everything from this page
#         if page_content:
#             pages_text.append(
#                 f"--- Page {page_number} ---\n"
#                 + "\n".join(page_content)
#             )
#     document.close()

#     return "\n\n".join(pages_text)

#created one function so rest of our application don't need to call different methods
#it can just call extract_text give file_path and then we can extract the extension and using that call right method.
def extract_text(file_path: str) -> str:
    extension = Path(file_path).suffix.lower()

    if extension == ".txt":
        return extract_text_from_txt(file_path)

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    if extension == ".docx":
        return extract_text_from_docx(file_path)

    raise ValueError(f"Unsupported file type: {extension}")