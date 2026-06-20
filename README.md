# Plain Vanilla RAG System

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system over a PDF document.

The application:

* Reads a PDF document
* Extracts text from the document
* Splits the text into overlapping chunks
* Generates embeddings for each chunk
* Stores embeddings in a FAISS vector database
* Retrieves relevant chunks for a user query
* Uses Gemini to generate answers from retrieved context
* Returns grounded answers and handles unanswerable questions

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
FAISS Vector Database
↓
Question Embedding
↓
Top-K Retrieval
↓
Gemini
↓
Answer + Sources

---

## Design Decisions

### 1. Chunking

* Chunk Size: 1000 characters
* Overlap: 200 characters

**Reason**

Large documents cannot be directly sent to the LLM because of token limitations and cost. Overlapping chunks preserve context and prevent information loss at chunk boundaries.

---

### 2. Embedding Model

* Model: all-MiniLM-L6-v2

**Reason**

This model is lightweight, fast, free to use, and performs well for semantic similarity search.

---

### 3. Vector Database

* FAISS (Facebook AI Similarity Search)

**Reason**

FAISS efficiently stores and searches high-dimensional vectors, making retrieval fast even for large documents.

---

### 4. Retrieval Strategy

* Top-K Retrieval: K = 5

**Reason**

A single chunk may not contain the complete answer. Retrieving multiple chunks improves the probability of finding all relevant information.

---

### 5. Generation Model

* Gemini 1.5 Flash

**Reason**

Gemini provides fast response generation and can be instructed to answer strictly from retrieved context.

---

## Handling Unanswerable Questions

The model is explicitly instructed:

"If the answer is not present in the retrieved context, return:

'I cannot answer from the provided document.'"

This reduces hallucinations and ensures grounded responses.

---

## Installation

### Clone Repository

git clone https://github.com/Dolly147/REC20-12.git

cd REC20-12

---

### Create Virtual Environment

Windows:

python -m venv venv

venv\Scripts\activate

---

### Install Dependencies

pip install -r requirements.txt

---

### Create Environment File

Create a file named `.env`

Add:

GEMINI_API_KEY=your_api_key_here

---

## Run Application

python app.py

---

## Example Questions

* What is regulation 241?
* What amounts are specified?
* Who is eligible for outfit allowance?
* What is grant of refreshment?

---

## Evaluation Criteria

The system can be evaluated using:

1. Retrieval Quality

   * Are relevant chunks retrieved?

2. Answer Correctness

   * Is the answer correct according to the document?

3. Grounding

   * Is the answer generated only from retrieved context?

4. Handling Unanswerable Questions

   * Does the system avoid hallucinating when information is unavailable?

---

## Technologies Used

* Python
* PyPDF
* Sentence Transformers
* FAISS
* NumPy
* Google Gemini API
* python-dotenv
