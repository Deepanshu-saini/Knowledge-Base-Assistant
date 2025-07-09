# LLM-Powered Knowledge Assistant API

A Django-based backend system that powers a Knowledge Assistant API using Retrieval-Augmented Generation (RAG) with HuggingFace models and FAISS for vector search. The system answers user questions based on uploaded knowledge base documents (PDF, Markdown, or text files).

---

## Features
- **Document Ingestion:** Upload and process PDF, Markdown, or text files.
- **Chunking & Embedding:** Documents are chunked and embedded using HuggingFace models.
- **Vector Search:** FAISS is used for fast retrieval of relevant chunks.
- **LLM Answer Generation:** Uses a HuggingFace LLM to generate answers from retrieved context.
- **REST API:** Built with Django REST Framework.

---

## Setup Instructions

### 1. Clone the Repository
```sh
git clone <your-repo-url>
cd LLM-Powered-Knowledge-Assistant-API
```

### 2. Create and Activate a Virtual Environment
```sh
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Linux/Mac
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Run Migrations
```sh
python manage.py makemigrations
python manage.py migrate
```

### 5. (Optional) Create a Superuser
```sh
python manage.py createsuperuser
```

### 6. Start the Development Server
```sh
python manage.py runserver
```

---

## Usage

### 1. Upload Documents
- **Via Django Admin:**
  - Go to `http://127.0.0.1:8000/admin/` and upload a document under "Documents".
- **Via API:**
  - Use Postman/cURL to POST to `/api/documents/` with a file and name.

### 2. Ask Questions
Send a POST request to `/api/ask-question/`:
```sh
curl -X POST http://localhost:8000/api/ask-question/ \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the use of mitochondria?"}'
```

**Response Example:**
```json
{
  "answer": "The mitochondria is known as the powerhouse of the cell...",
  "sources": ["Science Class IX - Page 3"]
}
```

---

## Notes
- The first request may take longer as models are loaded into memory.
- Models are downloaded to your HuggingFace cache on first use.
- If you see OpenMP warnings, you can suppress them by setting `KMP_DUPLICATE_LIB_OK=TRUE`.

---

## Troubleshooting
- **No answer or slow response:** Wait for model loading, check server logs for errors.
- **No chunks after upload:** Ensure the document is a valid PDF/Markdown/Text and check the Django admin for chunk creation.
- **PyTorch not found:** Make sure `torch` is installed (`pip install torch`).

---

## License
MIT 