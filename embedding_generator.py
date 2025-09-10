import openai
from openai import OpenAI
from dotenv import load_dotenv
import os

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchFieldDataType, VectorSearch, HnswAlgorithmConfiguration
import tiktoken
import uuid
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

import logging

import fitz  # PyMuPDF
import logging

load_dotenv()

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




def chunk_text(text, chunk_size=500, overlap=50):
    """Splits text into overlapping chunks of specified size."""
    try:
        sentences = text.split('. ')
        chunks = []
        chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence.split())
            if current_length + sentence_length > chunk_size:
                chunks.append(". ".join(chunk))
                chunk = chunk[-overlap:]  # Keep overlap
                current_length = sum(len(s.split()) for s in chunk)
            chunk.append(sentence)
            current_length += sentence_length
        
        if chunk:
            chunks.append(". ".join(chunk))
        
        logging.info(f"Successfully split text into {len(chunks)} chunks.")
        return chunks
    except Exception as e:
        logging.error(f"Error chunking text: {e}")
        return []



# Replace hardcoded API key with environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

def generate_embeddings(chunks, openai_api_key=openai_api_key):
    """Generates vector embeddings for each chunk using OpenAI."""
    openai.api_key = openai_api_key
    client = OpenAI(api_key=openai_api_key)  # Use the environment variable

    embeddings = []
    try:
        for chunk in chunks:
            response = client.embeddings.create(
                input=chunks,
                model="text-embedding-ada-002"
            )
            embeddings = [item.embedding for item in response.data]  # Extract embeddings properly
        logging.info("Successfully generated embeddings.")
        return embeddings
    except Exception as e:
        logging.error(f"Error generating embeddings: {e}")
        return []