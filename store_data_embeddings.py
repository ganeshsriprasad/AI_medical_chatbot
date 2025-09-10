import fitz  # PyMuPDF
import logging
import openai
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchFieldDataType, VectorSearch, HnswAlgorithmConfiguration
import tiktoken
import uuid
from embedding_generator import generate_embeddings


import certifi
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Replace hardcoded keys with environment variables
search_service_endpoint = os.getenv("SEARCH_ENDPOINT")
search_api_key = os.getenv("API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

def store_embeddings_in_azure(chunks, embeddings, search_service_endpoint=search_service_endpoint, search_api_key=search_api_key, index_name=index_name):
    """Stores vector embeddings in Azure AI Search."""
    try:
        credential = AzureKeyCredential(search_api_key)
        client = SearchClient(endpoint=search_service_endpoint, index_name=index_name, credential=credential)
        
        documents = [
    {
        "id": str(uuid.uuid4()),
        "text": chunk,
        "vector": embedding["embedding"]  # Extract the actual embedding array
    }
    for chunk, embedding in zip(chunks, embeddings["data"])  # Extract embeddings correctly
    ]   
        
        import json
        print(json.dumps(documents[:2], indent=2))  # Print the first 2 documents

        
        client.upload_documents(documents)
        logging.info("Successfully stored embeddings in Azure AI Search.")
    except Exception as e:
        logging.error(f"Error storing embeddings in Azure AI Search: {e}")

# Paths and Keys
pdf_path = "/home/ganesh.sri/rag_chatbot /parkinsons_disease.pdf"

index_name = "pk-docs"


# Execution
# text = extract_text_from_pdf(pdf_path)
# if text:
#     chunks = chunk_text(text)
#     embeddings = generate_embeddings(chunks, openai_api_key)
#     if embeddings:
#         store_embeddings_in_azure(chunks, embeddings, search_service_endpoint, search_api_key, index_name)