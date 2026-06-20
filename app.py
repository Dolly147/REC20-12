
 # Reads API key from .env file
from dotenv import load_dotenv
import os  # Used for reading environment variables
from pypdf import PdfReader
# Creates embeddings
from sentence_transformers import SentenceTransformer
# Vector database for storing the embeddings
import faiss
# Numerical operations
import numpy as np
# Gemini SDK
import google.generativeai as genai


# Load environment variables and gemini api 
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
llm = genai.GenerativeModel("gemini-2.5-flash")
print("Gemini API Loaded")
print(api_key[:10])

#step 1 : Read Pdf 
print("Reading PDF...")
reader = PdfReader("data/RegsNavyIV.pdf")
full_text = ""
for page in reader.pages:
    text = page.extract_text()
    # Sometimes page may be empty
    if text:
        full_text += text + "\n"
print("PDF Loaded")
print()

#step 2 : chuncking 

print("Creating Chunks...")
chunks = []
# Number of characters per chunk
chunk_size = 1000
# Keeps some previous context
overlap = 200
# Move by 400 characters
for i in range(0, len(full_text), chunk_size - overlap):
    chunk = full_text[i:i + chunk_size]
    chunks.append(chunk)
print(f"Total Chunks : {len(chunks)}")
print()


# step 3: Create embeddings
print("Creating Embeddings...")
# Small, free and fast embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)
# Convert every chunk into vectors
embeddings = embedding_model.encode(
    chunks
)
# FAISS needs float32
embeddings = np.array(
    embeddings,
    dtype=np.float32
)
print("Embeddings Created")
print()


# step 4: create vector database


print("Building FAISS Index...")
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)
print("FAISS Index Ready")
print()


# Step 5: Ask questions to the system

while True:
    print("--------------------------------")
    question = input("Ask Question : ")

    if question.lower() == "exit":
        break
    print()


# convert QUESTION to EMBEDDING
    
    query_embedding = embedding_model.encode(
        [question]
    )
    query_embedding = np.array(
        query_embedding,
        dtype=np.float32
    )

# Retrive Top K Chunks
    k = 5
    distances, indices = index.search(
        query_embedding,
        k
    )

# Build context 

    context = ""

    source_chunks = []

    print("\nRetrieved Chunks:")
    for idx in indices[0]:
        print("--------------------------------")
        print(f"Chunk {idx}")
        print(chunks[idx][:500])
        context += chunks[idx]
        context += "\n\n"

        source_chunks.append(idx)

#Prompt for gemini

    prompt = f"""
You are a procurement assistant.

Answer ONLY using the context below.

If answer is not present,
say:

'I cannot answer from the provided document.'

Context:
{context}

Question:
{question}

Provide:
1. Answer
2. Sources
"""

#send to gemini

    response = llm.generate_content(
        prompt
    )

#print answer 

    print("ANSWER")
    print("--------------------------------")
    print(response.text)

    print()
    print("Retrieved Chunks")

    for chunk_id in source_chunks:
        print(f"Chunk {chunk_id}")

    print()