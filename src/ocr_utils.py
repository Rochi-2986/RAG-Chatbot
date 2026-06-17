from pdf2image import convert_from_path
import pytesseract


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text_from_scanned_pdf(pdf_path):

    images = convert_from_path(pdf_path)

    full_text = ""

    for image in images:
        text = pytesseract.image_to_string(image)
        full_text += text + "\n"

    return full_text