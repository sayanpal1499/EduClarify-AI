import fitz  # PyMuPDF


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract text from a Streamlit UploadedFile PDF object.

    Returns up to 4000 characters to stay within the prompt token budget.
    """
    try:
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = "".join(page.get_text() for page in doc)
        return text[:4000]
    except Exception as e:
        return f"PDF extraction failed: {str(e)}"
