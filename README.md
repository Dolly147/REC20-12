# Plain-Vanilla RAG System

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system over a PDF document.

The system:

* Reads a PDF document
* Splits the document into overlapping chunks
* Converts chunks into embeddings
* Stores embeddings in a FAISS vector database
* Retrieves relevant chunks for a user question
* Uses Gemini to generate answers using only the retrieved context
* Returns answers with citations

---

## Architecture

PDF
↓
Text Extraction
↓
Chunking
↓
Embeddings
↓
FAISS Index
↓
Question Embedding
↓
Top-K Retrieval
↓
Gemini
↓
Answer + Sources

---

## Design Choices

### Chunking

* Chunk Size: 1000 characters
* Overlap: 200 characters

Reason:
Legal and policy documents contain long sections. Larger chunks preserve context, and overlap prevents information loss.

### Embedding Model

* all-MiniLM-L6-v2

Reason:
Lightweight, fast, and suitable for semantic similarity search.

### Vector Database

* FAISS

Reason:
Efficient nearest-neighbor similarity search on embeddings.

### Retrieval

* Top-K = 5

Reason:
Information may span multiple chunks.

### Generation Model

* Gemini 1.5 Flash

Reason:
Fast inference and easy integration.

---

## Handling Unanswerable Questions

If the answer is not present in the retrieved context, the system returns:

"I cannot answer from the provided document."

This avoids hallucinations.

---

## Installation

pip install -r requirements.txt

Create .env:

GEMINI_API_KEY=your_api_key

Run:

python app.py

---

## Example Questions

What is regulation 241?

What is grant of refreshment?

Who is eligible for outfit allowance?

What amounts are specified?

---

## Evaluation Metrics

1. Retrieval Quality
2. Answer Correctness
3. Grounding/Citations
4. Handling Unanswerable Questions
