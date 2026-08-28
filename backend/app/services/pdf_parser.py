"""
Pulls plain text out of an uploaded resume PDF so it can be handed to the LLM.
Using pdfplumber instead of writing our own PDF parser - reading PDF byte
structure by hand is a solved problem, no reason to redo it.
"""
import io
import pdfplumber


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    extracted_pages = []

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_pages.append(page_text)

    full_text = "\n".join(extracted_pages).strip()

    if not full_text:
        raise ValueError(
            "Could not extract any text from this PDF. "
            "It might be a scanned image rather than a text-based PDF."
        )

    return full_text
