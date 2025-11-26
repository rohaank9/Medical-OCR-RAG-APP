# Task 3 – Mini RAG Medical Question Answering System

This module implements **Task 3** from the *AI Developer Assessment*, using:

- **ChromaDB** for vector retrieval  
- **Gemini 2.5 Flash** for LLM reasoning  
- **FastAPI** for the RAG backend  
- **Streamlit** for the chatbot UI  

Task 3 extends the work from **Task 1 & Task 2**, which generate and index the structured medical notes.

---

## ⚠️ IMPORTANT WARNING — READ BEFORE USING STREAMLIT

When you upload **new medical notes** using the **Streamlit UI**:

- Streamlit calls the `/upload` API  
- OCR → JSON → Chroma indexing **does run successfully**
- BUT **FastAPI does NOT auto-reload** after indexing  

### ✅ Therefore, you MUST restart the RAG API server manually  
Otherwise the new documents will NOT appear in retrieval or RAG answers.

### Restart command:
```bash
uvicorn rag_api:app --reload --port 8001
```

Once restarted, new documents become available.

---

## 📁 1. Folder Structure

```
Task3/
│
├── rag_api.py            # FastAPI RAG backend (retrieval + Gemini answering)
├── streamlit_app.py      # Streamlit chatbot UI
├── requirements.txt      # Dependencies for Task 3
└── README.md
```

---

## 🚀 2. Environment Setup

### Step 1 — Create virtual environment
```bash
python -m venv venv
```

### Step 2 — Activate it
#### Windows:
```bash
venv\Scripts\activate
```
#### Linux/Mac:
```bash
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Recommended requirements.txt
```
fastapi
uvicorn
chromadb
sentence-transformers
google-generativeai
streamlit
requests
python-multipart
pydantic
```

### Step 4 — Configure Gemini API Key
```
setx GEMINI_API_KEY "your_key_here"   # Windows
export GEMINI_API_KEY="your_key_here" # Linux/Mac
```

---

## 🔍 3. What This RAG System Can Answer

Your implementation supports all required Task-3 queries:

### ✔ 1️⃣ “Which patients had X diagnosis?”  
Returns a list of matching patients using metadata filtering.

### ✔ 2️⃣ “What treatment was prescribed most frequently?”  
Counts canonicalized treatments and returns the most common one.

### ✔ 3️⃣ Normal Clinical QA  
Gemini answers strictly from retrieved context only (zero hallucination).

---

## ⚙️ 4. Running the RAG API (Backend)

Start FastAPI:
```bash
uvicorn rag_api:app --reload --port 8001
```

Test endpoint:
```
http://127.0.0.1:8001/
```

---

## 💬 5. Running the Streamlit Chatbot (Frontend)

In a second terminal:
```bash
streamlit run streamlit_app.py
```

The interface allows you to:

- Upload handwritten or scanned notes  
- Trigger OCR + JSON + Indexing  
- Ask medical questions via RAG pipeline  

---

## 🧪 6. Sample Queries (As Required in Assessment)

### ✔ Diagnosis Query
```
Which patients had pneumonia?
```

### ✔ Treatment Frequency Query
```
What treatment was prescribed most frequently?
```

### ✔ Normal QA
```
What is the diagnosis for the patient in 94.jpg?
```

---

## 🎯 7. How This Module Fulfills All Task-3 Requirements

Based on the assessment:  
:contentReference[oaicite:0]{index=0}

### ✔ Vector DB ingestion  
Uses ChromaDB already populated with Task-1/Task-2 data.

### ✔ Required RAG questions implemented  
- Diagnosis-based lookup  
- Treatment frequency analysis  
- Normal QA  

### ✔ REST API or chatbot  
You implemented **BOTH**:
- FastAPI backend  
- Streamlit chatbot  

### ✔ Sample queries included  
Provided above.

---

## 🏁 8. End-to-End Flow

```
Upload → OCR → Structured JSON → Chroma Index → RAG Retrieval →
Gemini reasoning → Streamlit UI answer
```

---

# 🎉 Task 3 Successfully Completed!

