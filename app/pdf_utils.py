from pypdf import PdfReader
from typing import List,Optional
from io import BytesIO

def extract_text_from_pdf(file: BytesIO) -> str:
    """
    Extracts text from a PDF file.

    Args:
        file (BytesIO): A file-like object containing the PDF data.

    Returns:
        str: The extracted text from the PDF.
    """
    reader = PdfReader(file)
    text = " "
    for page in reader.pages:
        text += page.extract_text() or ""
    return text