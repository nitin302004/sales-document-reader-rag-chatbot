# Sales Document Reader & RAG Chatbot

An AI-powered document processing and question-answering application for sales documents.

The application allows users to upload sales documents, extract structured sales information, and ask questions about PDF documents using a Retrieval-Augmented Generation (RAG) pipeline.

The project uses Streamlit for the frontend, FastAPI for the backend, LangGraph for workflow orchestration, OpenAI for LLM and embeddings, and Chroma as the vector database.

---

## 🚀 Features

- 📄 Upload sales documents
- 🔍 Extract structured sales information
- 📑 Support for PDF, DOCX and TXT documents
- 🤖 AI-powered document processing
- 🧠 LangGraph-based document workflow
- 🔗 Retrieval-Augmented Generation (RAG)
- 🗄️ Chroma vector database
- 💬 Ask questions about uploaded PDF documents
- ⚡ FastAPI backend
- 🎨 Streamlit frontend
- 🐳 Docker support
- ☸️ Kubernetes deployment configuration

---

## 📊 Sales Information Extraction

The application is designed to identify important sales attributes such as:

- Order ID
- Product
- Category
- Seller
- Quantity
- Unit Price
- Discount
- Revenue
- Region
- Sales Channel

Example:

```text
Order ID: ORD-2026-001
Product: Laptop
Category: Electronics
Seller: Amazon
Quantity: 25
Unit Price: 74999
Discount: 10%
Revenue: 1,687,478
Region: South India
Sales Channel: Amazon
```

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │      Streamlit      │
                         │     Frontend UI     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │       FastAPI       │
                         │       Backend       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      LangGraph      │
                         │ Workflow / Router   │
                         └──────────┬──────────┘
                                    │
                   ┌────────────────┼────────────────┐
                   │                │                │
                   ▼                ▼                ▼
                ┌──────┐        ┌──────┐        ┌──────┐
                │ TXT  │        │ DOCX │        │ PDF  │
                └───┬──┘        └───┬──┘        └───┬──┘
                    │               │               │
                    ▼               ▼               ▼
                 NLP /          Document          Text
                 Rules           Parsing         Extraction
                                                    │
                                                    ▼
                                                Chunking
                                                    │
                                                    ▼
                                           OpenAI Embeddings
                                                    │
                                                    ▼
                                             Chroma Vector DB
                                                    │
                                                    ▼
                                                Retrieval
                                                    │
                                                    ▼
                                               OpenAI LLM
                                                    │
                                                    ▼
                                                 Answer
```

---

# 📄 Document Processing

## TXT Documents

TXT documents are processed using text and NLP-based techniques to identify relevant sales information.

The processing pipeline identifies fields such as:

```text
Order ID
Product
Category
Seller
Quantity
Unit Price
Discount
Revenue
Region
Sales Channel
```

---

## DOCX Documents

DOCX documents are processed using Python-based document parsing.

The extracted document content is passed through the sales information extraction pipeline to identify relevant fields.

---

## PDF Documents

PDF documents are processed using an LLM-powered Retrieval-Augmented Generation pipeline.

The PDF processing workflow is:

```text
PDF Upload
    │
    ▼
Text Extraction
    │
    ▼
Document Chunking
    │
    ▼
OpenAI Embeddings
    │
    ▼
Chroma Vector Store
    │
    ▼
Similarity Search
    │
    ▼
Relevant Document Chunks
    │
    ▼
OpenAI LLM
    │
    ▼
Answer
```

This allows users to ask questions about the uploaded sales document.

---

# 💬 RAG Chatbot

The application provides a chatbot for interacting with uploaded PDF sales documents.

Example questions:

```text
What is the total revenue?

Which product generated the highest revenue?

How many units were sold?

What is the unit price?

What discount was applied?

Which region generated the most sales?

What is the sales channel?

What is the Order ID?
```

The system retrieves relevant information from the document and provides it as context to the LLM before generating the answer.

---

# 🔗 LangGraph Workflow

LangGraph is used to organize and control the document-processing workflow.

The uploaded document is routed according to its file type.

```text
                    Document Upload
                           │
                           ▼
                         Router
                    ┌──────┼──────┐
                    │      │      │
                    ▼      ▼      ▼
                   TXT    DOCX    PDF
                    │      │      │
                    ▼      ▼      ▼
                  Text   Parser   PDF
                Processing       Processing
                                   │
                                   ▼
                              Vector Store
                                   │
                                   ▼
                                  RAG
                                   │
                                   ▼
                                  LLM
                                   │
                                   ▼
                                Answer
```

This modular workflow makes it easier to extend the application with additional document formats and processing methods.

---

# 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| FastAPI | Backend REST API |
| Streamlit | Frontend web application |
| LangGraph | Workflow orchestration |
| LangChain | LLM and RAG components |
| OpenAI | LLM and embeddings |
| Chroma | Vector database |
| spaCy | NLP processing |
| PyPDF | PDF text extraction |
| python-docx | DOCX processing |
| Pydantic | Data validation |
| Docker | Containerization |
| Kubernetes | Deployment configuration |

---

# 📁 Project Structure

```text
sales_document_reader_chatbot/
│
├── api/
│   ├── __init__.py
│   ├── api.py
│   ├── graph_builder.py
│   │
│   ├── nodes/
│   │   ├── __init__.py
│   │   ├── chat_history.py
│   │   ├── docx_processing.py
│   │   ├── pdf_processing.py
│   │   ├── router.py
│   │   └── text_processing.py
│   │
│   ├── tools/
│   │   └── __init__.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── state.py
│
├── app/
│   └── app.py
│
├── images/
│
├── .streamlit/
│   └── config.toml
│
├── Dockerfile.fastapi
├── Dockerfile.streamlit
├── entrypoint.sh
├── k8-build.yaml
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

## Prerequisites

Make sure you have:

- Python 3.11+
- Git
- OpenAI API key

---

## 1. Clone the Repository

```bash
git clone https://github.com/nitin302004/sales-document-reader-rag-chatbot.git

cd sales-document-reader-rag-chatbot
```

---

## 2. Create a Virtual Environment

### macOS / Linux

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Configuration

Create a `.env` file in the root directory.

```text
OPENAI_API_KEY=your_openai_api_key
```

The project uses the environment variable to access OpenAI services.

**Never commit your `.env` file or API key to GitHub.**

The `.gitignore` file is configured to exclude `.env`.

---

# ▶️ Running the Application

The application consists of two components:

1. FastAPI backend
2. Streamlit frontend

Both should be running at the same time.

---

## 1. Start FastAPI

From the project root:

```bash
./.venv/bin/uvicorn api.api:app --reload --port 8000
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

FastAPI interactive documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 2. Start Streamlit

Open another terminal.

Navigate to the project:

```bash
cd /Users/nitin/Downloads/sales_document_reader_chatbot
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Run:

```bash
streamlit run app/app.py
```

The Streamlit application will be available at:

```text
http://localhost:8501
```

---

# 🔄 Application Workflow

```text
User
 │
 ▼
Upload Sales Document
 │
 ▼
Streamlit Frontend
 │
 ▼
FastAPI Backend
 │
 ▼
LangGraph Router
 │
 ├───────────────┐
 │               │
 ▼               ▼
TXT/DOCX        PDF
 │               │
 ▼               ▼
Extraction     Text Extraction
 │               │
 │               ▼
 │            Chunking
 │               │
 │               ▼
 │        OpenAI Embeddings
 │               │
 │               ▼
 │          Chroma DB
 │               │
 │               ▼
 │             RAG
 │               │
 └───────┬───────┘
         │
         ▼
      Response
```

---

# 🧠 RAG Architecture

The PDF question-answering system follows the standard RAG architecture:

```text
                  Uploaded PDF
                       │
                       ▼
                Text Extraction
                       │
                       ▼
                 Text Splitting
                       │
                       ▼
              Generate Embeddings
                       │
                       ▼
               Chroma Vector DB
                       │
                  User Question
                       │
                       ▼
                  Similarity Search
                       │
                       ▼
              Relevant PDF Chunks
                       │
                       ▼
                   OpenAI LLM
                       │
                       ▼
                    Response
```

RAG helps the application provide document-grounded answers by retrieving relevant sections of the uploaded document before generating a response.

---

# 🌐 API

The backend is implemented using FastAPI.

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

The API handles document uploads and chatbot-related operations.

---

# 🐳 Docker

The repository contains separate Docker configurations for the application components:

```text
Dockerfile.fastapi
Dockerfile.streamlit
```

These can be used to containerize the FastAPI backend and Streamlit frontend.

---

# ☸️ Kubernetes

The repository also contains:

```text
k8-build.yaml
```

which provides Kubernetes deployment configuration for deploying the application in a containerized environment.

---

# 🔒 Security

Sensitive information should be stored using environment variables.

The following are excluded from Git:

```text
.env
.venv/
__pycache__/
*.pyc
.chroma/
chroma/
chroma_db/
.DS_Store
```

API keys should never be hardcoded in source code or committed to the repository.

---

# 🚀 Future Improvements

The current project is a Proof of Concept.

Possible future improvements include:

- Improved sales entity extraction
- More accurate PDF table extraction
- Better document chunking
- Metadata-aware retrieval
- Improved RAG evaluation
- Better handling of large documents
- Persistent production-grade vector storage
- Authentication and authorization
- Asynchronous document processing
- Automated unit and integration testing
- Improved logging and monitoring
- Cloud deployment
- Additional document formats
- Improved UI and visualization of extracted sales data

---

# 👨‍💻 Author

**Nitin**

GitHub:

https://github.com/nitin302004

Project Repository:

https://github.com/nitin302004/sales-document-reader-rag-chatbot

---

# 📌 Disclaimer

This project is a Proof of Concept for sales document processing and Retrieval-Augmented Generation.

The accuracy of extracted information and generated answers depends on the structure and quality of the uploaded documents and the underlying language model.
