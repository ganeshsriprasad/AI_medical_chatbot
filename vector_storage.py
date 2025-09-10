from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import os

# Load Azure AI Search credentials
search_service = os.getenv("AZURE_SEARCH_SERVICE")
index_name = os.getenv("AZURE_SEARCH_INDEX")
search_key = os.getenv("AZURE_SEARCH_KEY")

search_client = SearchClient(
    endpoint=f"https://{search_service}.search.windows.net",
    index_name=index_name,
    credential=AzureKeyCredential(search_key)
)

def store_embedding(doc_id, text, embedding):
    document = {
        "id": doc_id,
        "content": text,
        "vector": embedding
    }
    search_client.upload_documents([document])
    print(f"Document {doc_id} uploaded successfully.")

# Example Usage
if __name__ == "__main__":
    sample_text = "Parkinson’s disease is a movement disorder that worsens over time."
    sample_embedding = [0.1, 0.2, 0.3, 0.4, 0.5]  # Replace with actual embedding
    store_embedding("doc_1", sample_text, sample_embedding)
