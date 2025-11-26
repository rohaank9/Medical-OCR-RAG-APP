# rag_api.py
import os
import json
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import chromadb
import google.generativeai as genai
from fastapi import UploadFile, File
from pathlib import Path
import subprocess
import signal
# ------------- Config -------------
GEMINI_MODEL = "gemini-2.5-flash"
CHROMA_DB_PATH = "chroma_db"
CHROMA_COLLECTION_NAME = "medical_notes"

# retrieval settings
TOP_K = 10
MAX_CONTEXT_CHARS_PER_DOC = 1200    # safe default; tune for tokens vs cost
MAX_TOTAL_CONTEXT_CHARS = 3500      # stop when context big

# ------------- FastAPI app -------------
app = FastAPI(title="RAG Medical QA API")

# Allow CORS if needed -- optional
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------- Setup Chroma and Gemini -------------
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
from chromadb.utils import embedding_functions

collection = client.get_or_create_collection(
    name=CHROMA_COLLECTION_NAME,
    embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
)


def setup_genai_client():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY not set")
    genai.configure(api_key=key)
    return genai.GenerativeModel(GEMINI_MODEL)

MODEL = None
try:
    MODEL = setup_genai_client()
except Exception as e:
    # We'll raise on calls if not configured
    MODEL = None

# ------------- Request/Response models -------------
class AskRequest(BaseModel):
    question: str
    top_k: int = TOP_K
    return_docs: bool = True

# ------------- utilities -------------
def normalize_score(distance: float) -> float:
    # convert distance -> similarity; for display only
    return round(1 / (1 + distance), 4)

def build_context_from_results(results: Dict[str, Any], max_chars_total=MAX_TOTAL_CONTEXT_CHARS):
    """
    Build an ordered context string from chroma query results.
    Returns: (context_text, provenance_list)
    """
    docs = results["documents"][0]
    ids = results["ids"][0]
    dists = results.get("distances", [[]])[0]
    metas = results["metadatas"][0]

    context_parts = []
    provenance = []
    total_chars = 0

    for i, doc_text in enumerate(docs):
        if total_chars >= max_chars_total:
            break
        doc_id = ids[i]
        meta = metas[i] or {}
        # choose snippet: cleaned_text was indexed; we can take first N chars
        snippet = (doc_text or "").strip().replace("\n", " ")
        snippet = snippet[:MAX_CONTEXT_CHARS_PER_DOC]
        header = f"---DOC ID: {doc_id} | patient: {meta.get('patient_name') or meta.get('patient') or 'unknown'} | date: {meta.get('date') or meta.get('source_file') }---\n"
        block = header + snippet + "\n"
        context_parts.append(block)
        total_chars += len(block)
        provenance.append({
            "id": doc_id,
            "patient": meta.get("patient_name"),
            "doctor": meta.get("doctor"),
            "diagnosis": meta.get("diagnosis"),
            "score": normalize_score(dists[i]) if dists else None,
        })

    context_text = "\n".join(context_parts)
    return context_text, provenance

# ------------- Core function: get answer via Gemini -------------
def answer_with_gemini(question: str, context_text: str, provenance: List[Dict], max_response_chars: int = 2000):
    if MODEL is None:
        raise RuntimeError("Gemini client not configured")

    system = """
    You are an advanced clinical RAG assistant. 
    You ALWAYS answer using ONLY the retrieved CONTEXT and METADATA.

    You also support *analytics-style structured queries* using the metadata of documents.

    You MUST detect if the user is asking one of the following:

    1) PATIENTS BY DIAGNOSIS QUERY:
    - Question pattern: “Which patients had X diagnosis?”
    - Action:
            • Look at metadata.diagnosis in each retrieved document.
            • Return a JSON list of patient names whose diagnosis matches the requested condition.
            • Case-insensitive partial matching allowed.

    2) MOST FREQUENT TREATMENT QUERY:
    - Question pattern: “What treatment was prescribed most frequently?”
    - Action:
            • Examine metadata.treatment across all retrieved docs.
            • Count frequency of each treatment string.
            • Select the top one.
            • Return name + frequency.

    3) NORMAL CLINICAL QA:
    - Answer concisely using only the provided text context.
    - Do NOT hallucinate.
    - If unsure, return answer=null.

    OUTPUT FORMAT:
    Return a JSON object ONLY with:
    {
        "answer": string or null,
        "type": "diagnosis_query" | "treatment_frequency" | "normal",
        "patients": optional list of names,
        "treatment_stats": optional {treatment, count},
        "used_documents": [doc IDs],
        "provenance": {...},
        "confidence": "low" | "medium" | "high"
    }
    """


    user_prompt = f"""
    CONTEXT BLOCKS (includes text snippets from documents):

    {context_text}

    METADATA (JSON for each retrieved document):
    {json.dumps(provenance, indent=2)}

    QUESTION:
    {question}

    INSTRUCTIONS:
    You MUST analyze both the text snippets AND the metadata above.

    You support three types of queries:

    1) DIAGNOSIS QUERY:
    - Pattern: "Which patients had X diagnosis?"
    - Use metadata.diagnosis to find all patients whose diagnosis contains X (case-insensitive).
    - Return list of patients.

    2) TREATMENT FREQUENCY QUERY:
    - Pattern: "What treatment was prescribed most frequently?"
    - Use metadata.treatments (a canonical string of all prescriptions)
    - Count all treatments and choose the most common one.

    3) NORMAL CLINICAL QA:
    - Answer only using the context.
    - If answer not found, return answer=null.

    OUTPUT FORMAT:
    Return ONLY a JSON object with fields:
    - answer (string or null)
    - type ("diagnosis_query" | "treatment_frequency" | "normal")
    - patients (list of names, optional)
    - treatment_stats ({{treatment, count}}, optional)
    - used_documents (list of doc IDs)
    - provenance (same as provided)
    - confidence ("low" | "medium" | "high")

    No markdown. No explanation. Only JSON output.
    """


    try:
        response = MODEL.generate_content(system + "\n\n" + user_prompt)
        raw = response.text
        # remove fences if any
        clean = raw.replace("```json", "").replace("```", "").strip()
        return clean
    except Exception as e:
        return json.dumps({"error": "model_call_failed", "exception": str(e)})

# ------------- API Endpoint -------------
@app.post("/ask")
def ask(req: AskRequest):
    q = req.question
    top_k = min(max(1, req.top_k), 10)


    # 1) retrieve from Chroma
    try:
        results = collection.query(
            query_texts=[q],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chroma query error: {e}")

    if not results or not results.get("documents"):
        return {"answer": None, "provenance": [], "used_documents": []}

    context_text, prov = build_context_from_results(results)
    # 2) call Gemini with context
    model_output = answer_with_gemini(q, context_text, prov)

    # 3) try to parse JSON
# Parse model output
    try:
        parsed = json.loads(model_output)
    except Exception:
        return {
            "raw_model_output": model_output,
            "context_preview": context_text[:1200],
            "provenance": prov,
            "used_documents": [p["id"] for p in prov]
        }

    # ALWAYS override provenance + used_documents from our real metadata
    parsed["provenance"] = prov
    parsed["used_documents"] = [p["id"] for p in prov]

    # Ensure optional fields exist for Streamlit
    parsed.setdefault("patients", [])
    parsed.setdefault("treatment_stats", {})

    return parsed

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Accept image/PDF upload → run Gemini OCR pipeline → update Chroma DB.
    Called from Streamlit UI.
    """
    try:
        # 1. Save uploaded file to ./uploads/
        os.makedirs("uploads", exist_ok=True)
        save_path = Path("uploads") / file.filename
        
        with open(save_path, "wb") as f:
            f.write(await file.read())

        # 2. Run your Gemini OCR → JSON generator script
        # This will save JSON into outputs/clean/
        import sys

        subprocess.run(
            [sys.executable, "gemini_ocr_improve.py", str(save_path)],
            check=True
        )
        # 3. Re-index Chroma so RAG can use new document
        subprocess.run(
            [sys.executable, "chroma_index.py"],
            check=True
        )
        
        
        

        return {
            "status": "success",
            "message": f"File processed and indexed: {file.filename}"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# ------------- Health -------------
@app.get("/")
def home():
    return {"status": "RAG API running"}

# ------------- Run instructions in comments -------------
# uvicorn rag_api:app --reload --port 8001
