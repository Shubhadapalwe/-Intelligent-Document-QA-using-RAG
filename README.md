# Intelligent Document Question Answering using RAG

**Ask questions about your PDFs using local AI.** A Streamlit application that extracts PDF text, builds semantic embeddings, retrieves relevant passages with FAISS, and generates document-grounded answers using Llama 3 through Ollama.

**Tech stack:** Python · Streamlit · PyPDF2 · Sentence Transformers (`all-MiniLM-L6-v2`) · FAISS · Ollama · Llama 3

## Overview

Upload a text-based PDF, process it into searchable chunks, and ask questions in natural language. The application displays generated answers and lets you inspect retrieved source passages. The local model runs through Ollama, so no hosted LLM API is required for inference.

## Features

- **PDF ingestion:** Extracts selectable text from uploaded PDFs.
- **Configurable chunking:** Adjust chunk size and overlap in the sidebar.
- **Semantic search:** Uses Sentence Transformers embeddings and FAISS to find relevant passages.
- **Local answer generation:** Sends retrieved context to Llama 3 via Ollama.
- **Source inspection:** Expand retrieved passages to review supporting text and similarity scores.
- **Clear fallback:** Can return a not-found response when the supplied context does not support an answer.

## 📸 Application Screenshots

### 1. Upload a PDF
Upload a PDF document through the Streamlit interface.

![PDF Upload Interface](screenshots/dashboard.png)

### 2. Select a Document
Choose a PDF file for processing.

![PDF File Selection](screenshots/document-upload.png)

### 3. Process and Embed the Document
Extract text, generate embeddings, and prepare the FAISS index.

![Document Processing](screenshots/document-processing.png)

### 4. Document Indexing Completed
Successfully processed 19 pages into 62 searchable chunks.

![Document Indexing](screenshots/indexing-success.png)

### 5. AI-Powered Question Answering
Ask questions and receive document-grounded answers using Llama 3.2.

![Successful Answer](screenshots/question-answer.png)

### 6. Semantic Search and Source Retrieval
Inspect retrieved document passages and similarity scores.

![Retrieved Sources](screenshots/source-retrieval.png)

<details>
<summary><b>Development and Local Model Screenshots</b></summary>

### Ollama Server
![Ollama Server](screenshots/ollama-server.png)

### Local LLM Testing
![Ollama Model Test](screenshots/ollama-model-test.png)

</details>
<summary>Development and local model screenshots</summary>

**Streamlit development server**

![Streamlit terminal](screenshots/05-streamlit-server.jpeg)

**Ollama model running locally**

![Ollama terminal](screenshots/06-ollama-model-test.jpeg)

</details>

## How it works

```text
PDF upload
   ↓
Text extraction (PyPDF2)
   ↓
Overlapping text chunks
   ↓
Sentence embeddings (all-MiniLM-L6-v2)
   ↓
FAISS vector index
   ↓
User question → Query embedding → Top-k relevant chunks
                                      ↓
                              Prompt with context
                                      ↓
                              Llama 3 via Ollama
                                      ↓
                              Answer + source passages
```

## Run locally

### Prerequisites

- Python 3.10+ (check your project's dependency compatibility)
- Ollama installed
- The Llama 3 model pulled locally

### Setup

```bash
# From the project directory
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
```

Start Ollama in a separate terminal (or confirm the Ollama app is already running):

```bash
ollama serve
```

Pull the model **tag configured in your application**. For example, if the code uses `llama3.2:3b`:

```bash
ollama pull llama3.2:3b
ollama list
curl http://localhost:11434/api/tags
```

**Important:** The model name in your Python code must match an installed Ollama model tag. If the code uses `llama3`, either pull that model or update the configuration to the installed tag.

Run the Streamlit app from the project directory:

```bash
python -m streamlit run app.py
```

Open the local address displayed by Streamlit (normally `http://localhost:8501`). Upload a text-based PDF, click **Process document**, switch to **Ask questions**, and submit a question.

## Example question

**Question:** Explain the Intelligent Document QA system, including its architecture and technologies.

**Example response:** The system extracts PDF text with PyPDF2, splits it into chunks, creates Sentence Transformers embeddings, retrieves matching chunks using FAISS, and uses Llama 3 through Ollama to answer from the retrieved context.

*The response shown is an example from the supplied document; model outputs may vary.*

## Configuration

The sidebar exposes these controls:

| Setting | Example shown | Purpose |
| --- | ---: | --- |
| Chunk size | 900 characters | Length of text segments |
| Chunk overlap | 150 characters | Shared text between adjacent segments |
| Relevant chunks | 3 | Number of retrieved passages passed to generation |

These are screenshot settings, not universally optimal values. Test different settings for your documents.

## Limitations and future improvements

- Text extraction is designed for **text-based PDFs**; scanned documents may require OCR.
- Retrieval quality depends on document structure, chunking, and embedding relevance.
- A local LLM can still produce incomplete or incorrect answers; verify important claims against source passages.
- Future work: OCR fallback, retrieval evaluation, stronger citations, document-level access controls, and deployment hardening.

## Project status

**Working local prototype.** Screenshots demonstrate PDF indexing, retrieval display, and a generated answer. They do not establish production deployment, accuracy benchmarks, or multi-user security.

## Author

**Shubhada Palwe** — Python · AI/ML · Generative AI

GitHub: [Shubhadapalwe](https://github.com/Shubhadapalwe)
