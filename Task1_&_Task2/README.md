# Task 1 & Task 2 Module
Task 1 & Task 2 – Medical Notes Digitization, Structuring & Summarization

This module implements Task 1 and Task 2 from the “AI Developer Assessment” using Python, Gemini OCR, and ChromaDB.

It provides:

OCR extraction from handwritten medical notes

Clean & structured JSON generation

Clinical summary JSON generation

Vector indexing via ChromaDB

Search API using FastAPI

Web-based API testing through Swagger UI

📁 1. Folder Structure
Task1_&_Task2/
│
├── gemini_ocr_improve.py      # Task-1 OCR + structured JSON + Task-2 summary JSON
├── chroma_index.py            # Index Task-1 JSON files into Chroma vector DB
├── search_api.py              # FastAPI semantic search API
│
├── requirements.txt
├──notes             #Contain example images with prescription including handwritten and real medical transcription
├── outputs/
│   ├── raw/                   # OCR raw text
│   ├── clean/                 # Structured JSON (Task-1)
│   ├── task2/                 # Summary JSON (Task-2)
│
└── README.md

🚀 2. Environment Setup
Step 1 — Create virtual environment
python -m venv venv

Step 2 — Activate it
Windows:
venv\Scripts\activate

Linux/Mac:
source venv/bin/activate

Step 3 — Install dependencies
pip install -r requirements.txt

Example requirements.txt (recommended):
fastapi
uvicorn
chromadb
sentence-transformers
google-generativeai
python-multipart


✔ You do NOT need AWS Textract or GCP Document  since Gemini OCR is Used.

🔑 3. Configure Gemini API Key

Set your API key:

Windows PowerShell:
setx GEMINI_API_KEY "your_key_here"

Linux/Mac:
export GEMINI_API_KEY="your_key_here"


Check:

echo %GEMINI_API_KEY%   (Windows)
echo $GEMINI_API_KEY    (Linux/Mac)

📤 4. Upload Notes & Run Task-1 and Task-2 Processing

Put JPG / PNG / PDF files inside a folder, e.g.:

notes/
   94.jpg
   98.jpg
   981.jpg


Then run:

python gemini_ocr_improve.py notes/


This automatically creates:

📁 outputs/raw/

Raw OCR text extracted by Gemini

📁 outputs/clean/

Structured JSON containing:

patient info

doctor

diagnosis

prescriptions

cleaned OCR text

📁 outputs/task2/

Task-2 summary JSON containing:

Patient

Diagnosis

Treatment

Follow-up

✔ This completes Task 1 & Task 2.

📚 5. Index the Task-1 JSON into ChromaDB

Run:

python chroma_index.py --folder outputs/clean


This creates:

/chroma_db


and indexes every JSON file for semantic search.

🌐 6. Run the Search API (FastAPI)

Start API server:

uvicorn search_api:app --reload


You should see:

INFO:     Application startup complete.

🔍 7. How to Query the API
✔ Option A — Browser (no frontend, no linking)

Use FastAPI Swagger UI:

http://127.0.0.1:8000/docs


Steps:

Open /docs

Find GET /search

Click Try It Out

Enter search query:

fever


Click Execute

✔ Option B — Query via URL

Direct URL:

http://127.0.0.1:8000/search?q=fever

✔ Option C — Query via cURL
curl "http://127.0.0.1:8000/search?q=fever"

🎯 8. How This Module Fulfills All Assessment Requirements
✅ Task 1 Requirements

✔ OCR extraction using LLM (Gemini OCR allowed)
✔ Clean structured JSON output
✔ Storage in vector DB (ChromaDB)
✔ Search API via FastAPI
✔ Demonstration with /search?q=...
✔ Working example outputs in outputs/clean/

✅ Task 2 Requirements

✔ Uses a free-tier LLM (Gemini)
✔ Batch processing of multiple notes (directory support)
✔ Produces JSON with fields:

Patient

Diagnosis

Treatment

Follow-up

✔ Fully automated end-to-end pipeline
✔ Summary outputs stored in outputs/task2/
✔ Consistent schema for all notes

📝 9. Example Summary Output (Task-2)
{
  "Patient": "Rohaan Khan",
  "Diagnosis": "Viral Fever",
  "Treatment": "Remdesivir 200mg IV; Paracetamol 650mg",
  "Follow-up": null
}

🧪 10. Example Full Workflow (Copy/Paste)
cd Task1_&_Task2

python gemini_ocr_improve.py notes/

python chroma_index.py --folder outputs/clean

uvicorn search_api:app --reload


Then open:

http://127.0.0.1:8000/docs

🎉 You’re Done!

Task 1 & Task 2 are complete, fully functional, reproducible, and meet every requirement of the assessment.
