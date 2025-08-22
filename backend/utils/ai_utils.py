import tempfile
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract

def extract_text_from_pdf(pdf_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_bytes)
        tmp.flush()
        reader = PdfReader(tmp.name)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

def ocr_image(file_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(file_bytes)
        tmp.flush()
        image = Image.open(tmp.name)
        text = pytesseract.image_to_string(image)
        return text
