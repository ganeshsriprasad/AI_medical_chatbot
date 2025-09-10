from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import fitz  # PyMuPDF
import openai
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.core.exceptions import HttpResponseError
from azure.search.documents.models import VectorizedQuery
import uvicorn
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing (restrict in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Azure AI Search Configuration
search_service_endpoint = os.getenv("SEARCH_ENDPOINT")
search_api_key = os.getenv("API_KEY")
index_name = "pk-docs"

# OpenAI API Key
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

# Initialize Azure Search Client
credential = AzureKeyCredential(search_api_key)
search_client = SearchClient(endpoint=search_service_endpoint, index_name=index_name, credential=credential)

# Pydantic Model for Chat Requests
class ChatRequest(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
async def home():
    """Render the chatbot UI."""
    with open("templates/index1.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/chat")
async def chat(request: ChatRequest):
    """Handles user queries, retrieves relevant documents from vector DB, and generates responses using OpenAI."""
    user_query = request.query.strip().lower()
    if not user_query:
        raise HTTPException(status_code=400, detail="Empty query")

    # Convert user query to an embedding using OpenAI
    try:
        embedding_response = openai.embeddings.create(
            model="text-embedding-3-small",
            input=[user_query]
        )
        user_embedding = embedding_response.data[0].embedding
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Embedding generation failed")

    # Ensure the embedding is not None
    if not user_embedding:
        raise HTTPException(status_code=500, detail="Failed to generate embedding")

    # Perform Vector Search on Azure AI Search
    try:
        vector_query = VectorizedQuery(
            vector=user_embedding,
            k_nearest_neighbors=3,
            fields="vector",
            exhaustive=True
        )

        search_results = search_client.search(
            search_text="",
            vector_queries=[vector_query],
            select=["id", "text"]
        )

        context_text = "\n".join([doc["text"] for doc in search_results]) or "No relevant documents found."
    
    except HttpResponseError as e:
        raise HTTPException(status_code=500, detail="Vector search failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

    # Generate response using OpenAI
    try:
        openai_response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI chatbot answering questions based on retrieved documents. If the provided user query is a greeting, respond appropriately without mentioning any headers. Also, when there is a question not related to the provided documents, respond with 'I'm sorry, I do not have this information.' Provide **structured responses** with headings, bullet points, and bold keywords for better readability."},
                {"role": "user", "content": f"Question: {user_query}\nContext: {context_text}"}
            ]
        )
        answer = openai_response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate response")

    return {"answer": answer}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5001)
