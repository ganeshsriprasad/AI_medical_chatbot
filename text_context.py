import easyocr
import numpy as np
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import openai  # OpenAI API for generating structured context
from dotenv import load_dotenv
import os

# Initialize EasyOCR Reader
reader = easyocr.Reader(["en"])

# Initialize BLIP for Image Captioning
device = "cuda" if torch.cuda.is_available() else "cpu"
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

# Load environment variables from .env file
load_dotenv()

# Replace hardcoded OpenAI API key with environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

def detect_image_type(image_path):
    """Uses BLIP to auto-detect what the image contains"""
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, return_tensors="pt").to(device)
    output = model.generate(**inputs)
    description = processor.decode(output[0], skip_special_tokens=True)
    return description

def extract_text_from_image(image_path):
    """Extracts text from an image using OCR"""
    img_pil = Image.open(image_path)
    img_array = np.array(img_pil)

    # Perform OCR
    extracted_text = reader.readtext(img_array, detail=0)
    return " ".join(extracted_text) if extracted_text else "No readable text found."

def generate_context(image_description, text):
    """Uses OpenAI's GPT to generate structured context based on detected type & extracted text"""
    openai.api_key = openai_api_key

    prompt = f"""
    The following text was extracted from an image: 
    "{text}"

    The image appears to contain: "{image_description}".

    Based on the text and detected image type, explain what the image represents, its key components, and its overall purpose.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",  
        messages=[{"role": "system", "content": "You are an AI trained to analyze image-based text and infer meaning."},
                  {"role": "user", "content": prompt}],
        temperature=0.5
    )

    return response["choices"][0]["message"]["content"].strip()

# Provide image path
image_path = "/home/ganesh.sri/rag_chatbot/undefined.png"

# Step 1: Detect what the image represents (Architecture Flow, Chart, Table, etc.)
image_description = detect_image_type(image_path)

# Step 2: Extract text from image using OCR
extracted_text = extract_text_from_image(image_path)

# Step 3: Generate structured context using GPT-4 (without manually defining image type)
context_description = generate_context(image_description, extracted_text)

# Step 4: Store results in a structured format
result = {
    "image_path": image_path,
    "detected_image_type": image_description,
    "extracted_text": extracted_text,
    "contextual_understanding": context_description
}

# Print Output
print("\n🔹 Image Type Detected:", result["detected_image_type"])
print("\n🔹 Extracted Text:\n", result["extracted_text"])
print("\n🔹 Contextual Understanding:\n", result["contextual_understanding"])
