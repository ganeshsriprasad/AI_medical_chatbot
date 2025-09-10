import fitz  # PyMuPDF for extracting text
import easyocr  # OCR for images
import pdf2image  # Convert PDF images for OCR
import numpy as np
import io
from PIL import Image

# Initialize EasyOCR Reader
reader = easyocr.Reader(["en"])

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF while also performing OCR on images within the PDF."""
    doc = fitz.open(pdf_path)
    full_text = []

    for page_num in range(len(doc)):
        page = doc[page_num]

        # Extract regular text
        text = page.get_text("text")
        full_text.append(text.strip())

        # Extract images and perform OCR
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]  # Image reference
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            # Convert to PIL Image
            img_pil = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img_pil)

            # Perform OCR
            extracted_text = reader.readtext(img_array, detail=0)
            if extracted_text:
                full_text.append(f"\n[Extracted from Image {img_index + 1} on Page {page_num + 1}]\n" + " ".join(extracted_text))

    return "\n".join(full_text)




# Provide the correct PDF path
pdf_path = "/home/ganesh.sri/rag_chatbot /parkinsons_disease.pdf"
# Extract and print the full text
extracted_text = extract_text_from_pdf(pdf_path)
print(extracted_text)



