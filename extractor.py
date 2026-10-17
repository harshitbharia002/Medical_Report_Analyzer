import fitz
import pytesseract

from PIL import Image


# ==============================
# STEP 8: PDF TEXT EXTRACTION
# ==============================

def extract_text_from_pdf(file_path):

    text = ""

    document = fitz.open(file_path)

    for page in document:
        text += page.get_text()

    document.close()

    return text


# ==============================
# STEP 9: IMAGE OCR
# ==============================

def extract_text_from_image(image_path):

    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)

    return text
