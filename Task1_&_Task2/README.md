# Task 1 & Task 2 – Medical Notes Digitization, Structuring & Summarization

This module implements **Task 1** and **Task 2** from the *AI Developer Assessment* using **Python**, **Gemini OCR**, and **ChromaDB**.

It provides:

- OCR extraction from handwritten medical notes  
- Clean & structured JSON generation  
- Clinical summary JSON generation  
- Vector indexing via ChromaDB  
- Search API using FastAPI  
- Web-based API testing through Swagger UI  

---

## 📁 1. Folder Structure

```
Task1_&_Task2/
│
├── gemini_ocr_improve.py      # Task-1 OCR + structured JSON + Task-2 summary JSON
├── chroma_index.py            # Index Task-1 JSON files into Chroma vector DB
├── search_api.py              # FastAPI semantic search API
│
├── requirements.txt
├── notes/                     # Contains example handwritten & real medical notes
│
├── outputs/
│   ├── raw/                   # OCR raw text
│   ├── clean/                 # Structured JSON (Task-1)
│   ├── task2/                 # Summary JSON (Task-2)
│
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

### Recommended `requirements.txt`
```
fastapi
uvicorn
chromadb
sentence-transformers
google-generativeai
python-multipart
```

✔ AWS Textract / GCP Document AI not required — **Gemini OCR is used.**

---

## 🔑 3. Configure Gemini API Key

Set your API key:

#### Windows PowerShell:
```bash
setx GEMINI_API_KEY "your_key_here"
```

#### Linux/Mac:
```bash
export GEMINI_API_KEY="your_key_here"
```

Verify:

```bash
echo %GEMINI_API_KEY%     # Windows
echo $GEMINI_API_KEY      # Linux/Mac
```

---

## 📤 4. Upload Notes & Run Task-1 and Task-2 Processing

Place JPG / PNG / PDF files inside the `notes/` folder:

```
notes/
   94.jpg
   98.jpg
   981.jpg
```

### Run OCR + Structuring + Summary:
```bash
python gemini_ocr_improve.py notes/
```

This automatically generates:

### 📁 `outputs/raw/`
Raw OCR text extracted via Gemini

### 📁 `outputs/clean/`
Structured JSON containing:
- patient  
- doctor  
- diagnosis  
- prescriptions  
- cleaned_text  

### 📁 `outputs/task2/`
Task-2 summary JSON:
- Patient  
- Diagnosis  
- Treatment  
- Follow-up  

✔ This completes **Task 1 & Task 2**.

---

## 📚 5. Index Task-1 JSON into ChromaDB

```bash
python chroma_index.py --folder outputs/clean
```

This creates the vector store:

```
/chroma_db
```

---

## 🌐 6. Run the Search API (FastAPI)

Start the API server:

```bash
uvicorn search_api:app --reload
```

Expected message:

```
INFO:     Application startup complete.
```

---

## 🔍 7. How to Query the API

### ✔ Option A — Web Browser (Swagger UI)

Open:
```
http://127.0.0.1:8000/docs
```

Steps:
1. Open `/docs`  
2. Find **GET /search**  
3. Click **Try It Out**  
4. Enter query:
   ```
   fever
   ```
5. Click **Execute**

---

### ✔ Option B — Direct URL

```
http://127.0.0.1:8000/search?q=fever
```

---

### ✔ Option C — cURL

```bash
curl "http://127.0.0.1:8000/search?q=fever"
```

---

## 🎯 8. How This Module Fulfills All Assessment Requirements

### ✔ Task 1 Requirements
- OCR extraction using LLM (Gemini OCR allowed)  
- Clean structured JSON output  
- Storage in Chroma vector DB  
- Search API via FastAPI  
- Demonstration using `/search?q=...`  
- Example outputs provided in `outputs/clean/`  

### ✔ Task 2 Requirements
- Uses a free-tier LLM (Gemini)  
- Batch processing of multiple notes  
- Outputs JSON with:
  - Patient  
  - Diagnosis  
  - Treatment  
  - Follow-up  
- Fully automated pipeline  
- Summary files stored in `outputs/task2/`  
- Consistent schema across all inputs  

---

## 📝 9. Example Summary Output (Task-2)

```json
{
  "Patient": "Rohaan Khan",
  "Diagnosis": "Viral Fever",
  "Treatment": "Remdesivir 200mg IV; Paracetamol 650mg",
  "Follow-up": null
}
```

---

## 🧪 10. Example Full Workflow (Copy/Paste)

```bash
cd Task1_&_Task2

python gemini_ocr_improve.py notes/

python chroma_index.py --folder outputs/clean

uvicorn search_api:app --reload
```

Then open in your browser:

```
http://127.0.0.1:8000/docs
```

---

# 🎉 You’re Done!

**Task 1 & Task 2 are fully functional, reproducible, and meet all assessment requirements.**
