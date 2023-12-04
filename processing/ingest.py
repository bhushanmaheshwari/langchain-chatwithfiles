from PyPDF2 import PdfReader
from utils.logs import add_log

def get_pdf_text(pdf):
    add_log("reading PDF file")
    
    text = ""
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

