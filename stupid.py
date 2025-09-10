
import fitz  # PyMuPDF
import logging
import openai


def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    try:
        doc = fitz.open(pdf_path)
        text = "".join([page.get_text() for page in doc])
        logging.info("Successfully extracted text from PDF.")
        return text
    except Exception as e:
        logging.error(f"Error extracting text: {e}")
        return None
    
# Provide the correct PDF path
pdf_path = "/home/ganesh.sri/rag_chatbot /parkinsons_disease.pdf"
# Extract and print the full text
extracted_text = extract_text_from_pdf(pdf_path)
print(extracted_text)