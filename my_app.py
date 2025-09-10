import fitz  # PyMuPDF for PDF text extraction
import openai
import requests
import json
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv

load_dotenv()

# Replace hardcoded values with environment variables
search_endpoint = os.getenv("SEARCH_ENDPOINT")
index_name = os.getenv("INDEX_NAME")
api_key = os.getenv("API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

pdf_path = "C:/Users/Ganesh.Sri/Downloads/parkinsons_disease.pdf"
text = extract_text_from_pdf(pdf_path)
print("Extracted text:", text[:100])  # Print first 500 characters for verification

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

import openai

def generate_embeddings(text_chunks, openai_api_key):
    openai.api_key = openai_api_key  # Set API key

    embeddings = []
    for chunk in text_chunks:
        response = openai.embeddings.create(
            model="text-embedding-ada-002",  # Ensure you are using a correct embedding model
            input=chunk
        )
        embeddings.append(response.data[0].embedding)  # Access the embedding correctly

    return embeddings


def store_embeddings_in_azure_search(embeddings, text_chunks, search_endpoint, index_name, api_key):
    search_client = SearchClient(endpoint=search_endpoint, index_name=index_name, credential=api_key)
    documents = [
        {"id": str(i), "content": text, "embedding": emb}
        for i, (text, emb) in enumerate(zip(text_chunks, embeddings))
    ]
    search_client.upload_documents(documents)

def retrieve_similar_documents(query, search_endpoint=search_endpoint, index_name=index_name, api_key=api_key, openai_api_key=openai_api_key):
    search_client = SearchClient(endpoint=search_endpoint, index_name=index_name, credential=api_key)
    query_embedding = generate_embeddings([query], openai_api_key)[0]
    results = search_client.search( 
        search_text=None,
        vector=query_embedding,
        top=3,
        select=["content"]
    )
    return [doc["content"] for doc in results]

def get_response_from_openai(query, context, openai_api_key):
    prompt = f"Context: {context}\nUser: {query}\nAssistant:"
    response = openai.Completion.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=200,
        api_key=openai_api_key
    )
    return response["choices"][0]["text"].strip()

app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    return render_template("my_app.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_query = data.get("query")

    similar_docs = retrieve_similar_documents(user_query)
    context = " ".join(similar_docs)
    response = get_response_from_openai(user_query, context, openai_api_key)

    return jsonify({"query": user_query, "response": response})

if __name__ == "__main__":
    app.run(debug=True)
