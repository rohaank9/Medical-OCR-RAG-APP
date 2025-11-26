# Task 3 – Mini RAG Medical Question Answering System (Independent Version)

This module implements **Task 3** from the *AI Developer Assessment*, using:

- **Gemini OCR** for digitizing medical notes  
- **ChromaDB** for vector retrieval  
- **Gemini 2.5 Flash** for LLM reasoning  
- **FastAPI** for the RAG backend  
- **Streamlit** for the chatbot UI  

> **IMPORTANT:**  
> Task-3 now includes its own local copies of:
> - `gemini_ocr_improve.py`
> - `chroma_index.py`
>
> This means **Task-3 can run independently**, even if Task-1 & Task-2 are not executed separately.

---

## ⚠️ IMPORTANT WARNING — MUST READ

When you upload **new medical notes** via the **Streamlit UI**:

- Streamlit calls `/upload`  
- OCR → JSON → indexing **does run**  
- But **FastAPI will NOT auto-reload**

### 👉 You MUST manually restart the RAG API:

```bash
uvicorn rag_api:app --reload --port 8001
```

Without restarting, newly added documents **will not appear in RAG answers**.

---

## 📁 1. Folder Structure

```
Task3/
│
├── rag_api.py                 # FastAPI RAG backend (retrieval + Gemini answering)
├── streamlit_app.py           # Streamlit chatbot UI
│
├── gemini_ocr_improve.py      # OCR + structured JSON generator (local copy)
├── chroma_index.py            # ChromaDB indexer (local copy)
│
├── requirements.txt           # Dependencies for Task 3
└── README.md
```

Since `gemini_ocr_improve.py` and `chroma_index.py` are included here,  
**Task-3 can run independently without Task-1_&_Task2.**

---

## 🚀 2. Environment Setup

### Step 1 — Create virtual environment
```bash
python -m venv venv
```

### Step 2 — Activate
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

### Required packages
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
```bash
setx GEMINI_API_KEY "your_key_here"     # Windows
export GEMINI_API_KEY="your_key_here"   # Linux/Mac
```

---

## 🧩 3. How Task-3 Works Independently

Task-3 can be run even if Task-1 & Task-2 were never executed because:

- It includes **Gemini OCR** → extracts text  
- It includes **JSON structuring logic** → creates Task-1-style JSON  
- It includes **Chroma indexer** → creates embeddings + vector DB  
- It includes **FastAPI RAG** → answers questions  
- It includes **Streamlit chatbot** → user-friendly UI  

### **Independent Processing Workflow**

```
Upload Note → gemini_ocr_improve.py → JSON → chroma_index.py → ChromaDB →
rag_api.py (RAG) → streamlit_app.py (UI)
```

---

## 🔧 4. Running the RAG API (Backend)

Start the backend:

```bash
uvicorn rag_api:app --reload --port 8001
```

Test:
```
http://127.0.0.1:8001/
```

---

## 💬 5. Running the Streamlit Chatbot (Frontend)

In a new terminal:

```bash
streamlit run streamlit_app.py
```

Features include:

- Upload handwritten or scanned medical notes  
- Automatic OCR + JSON creation  
- Auto-indexing into ChromaDB  
- Ask medical questions (“pneumonia patients?”, “most frequent treatment?”, etc.)

---

## 🧪 6. Sample Queries (Required by Assessment)

### ✔ Diagnosis Query  
**“Which patients had pneumonia?”**

### ✔ Frequent Treatment Query  
**“What treatment was prescribed most frequently?”**

### ✔ Clinical QA  
**“What is the diagnosis for the patient in 94.jpg?”**

---

## 🎯 7. How Task-3 Requirements Are Fulfilled

Based on the assessment:  
:contentReference[oaicite:0]{index=0}

### ✔ Ingest at least 10 notes  
Via upload UI + `gemini_ocr_improve.py` + `chroma_index.py`.

### ✔ Build RAG capable of answering the two required queries  
Implemented in `rag_api.py`:
- Diagnosis-based patient lookup  
- Treatment frequency ranking  

### ✔ Provide REST API or a chatbot  
You implemented BOTH:
- `/ask` and `/upload` in FastAPI  
- Streamlit web chatbot  

### ✔ Provide sample queries  
Included above.

---

## 📦 8. End-to-End Pipeline

```
User Upload
   ↓
Gemini OCR (gemini_ocr_improve.py)
   ↓
Structured JSON
   ↓
Indexing into ChromaDB (chroma_index.py)
   ↓
FastAPI RAG Engine (rag_api.py)
   ↓
Streamlit Chatbot (streamlit_app.py)
   ↓
Final Answer
```

---

# 🎉 Task 3 Successfully Completed (Standalone Version)!
