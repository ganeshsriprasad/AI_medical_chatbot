# RAG Chatbot for Parkinson's Disease

This project is a **Retrieval-Augmented Generation (RAG) Chatbot** designed to assist with Parkinson's disease-related queries. It combines the power of **OpenAI's GPT models** and **Azure Cognitive Search** to provide accurate and context-aware responses by leveraging both generative AI and a custom knowledge base.

## Features
- **PDF Text Extraction**: Extracts and processes text from PDF documents using PyMuPDF.
- **Image Text Recognition**: Utilizes EasyOCR and BLIP for extracting and analyzing text from images.
- **Custom Knowledge Base**: Stores and retrieves embeddings in Azure Cognitive Search for efficient document retrieval.
- **OpenAI Integration**: Generates embeddings and conversational responses using OpenAI's GPT models.
- **FastAPI and Flask**: Provides RESTful APIs and a user-friendly web interface for interaction.
- **Environment Variable Management**: Securely manages API keys and sensitive data using `.env` files.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ganeshsriprasad/AI_medical_chatbot.git
   ```

2. Navigate to the project directory:
   ```bash
   cd AI_medical_chatbot
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up the `.env` file with your API keys and endpoints:
   ```env
   SEARCH_ENDPOINT=<your-azure-search-endpoint>
   INDEX_NAME=<your-index-name>
   API_KEY=<your-azure-api-key>
   OPENAI_API_KEY=<your-openai-api-key>
   ```

## Usage

1. Start the Flask or FastAPI server:
   ```bash
   python my_app.py  # For Flask
   python app1.py    # For FastAPI
   ```

2. Access the web interface:
   - Flask: Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.
   - FastAPI: Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

3. Interact with the chatbot by uploading documents or asking questions.

## Project Structure
- `my_app.py`: Flask application for the chatbot.
- `app1.py`: FastAPI application for the chatbot.
- `embedding_generator.py`: Generates embeddings for text chunks.
- `store_data_embeddings.py`: Stores embeddings in Azure Cognitive Search.
- `text_context.py`: Handles image text extraction and context generation.
- `templates/`: HTML templates for the web interface.
- `static/`: Static files (CSS, JS) for the web interface.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- OpenAI for their powerful GPT models.
- Azure Cognitive Search for enabling efficient document retrieval.
- The open-source community for providing valuable tools and libraries.
