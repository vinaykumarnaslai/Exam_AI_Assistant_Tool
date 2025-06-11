# ocr_engine.py
import pytesseract
from PIL import Image

# Set the path to tesseract.exe if not auto-detected
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_path="screenshot.png"):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text.strip()
