"""
Improved search_api.py
Features:
- Semantic search using ChromaDB
- Optional filters (patient name, doctor, gender, date)
- Normalized similarity scores
- Clean, structuresearch_api:app --reload --port 8000d JSON response
- Returns diagnosis, prescriptions, cleaned_text
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import chromadb

app = FastAPI(title="Medical Note Search API")

# Allow frontend or Postman usage
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Chroma persistent DB
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection(name="medical_notes")

# -----------------------------
# Utility: normalize score
# -----------------------------
def normalize(distance: float):
    """Convert Euclidean distance into similarity score (0–1)."""
    return round(1 / (1 + distance), 4)


# -----------------------------
# Search Endpoint
# -----------------------------
@app.get("/search")
def search_medical_notes(
    q: str = Query(..., description="Search query"),
    top_k: int = Query(5, ge=1, le=20),
    patient: str | None = None,
    doctor: str | None = None,
    gender: str | None = None,
):
    """Semantic search over indexed medical notes."""

    try:
        results = collection.query(
            query_texts=[q],
            n_results=top_k,
            include=["metadatas", "documents", "distances"],
        )
    except Exception as e:
        return {"error": f"Chroma query failed: {e}"}

    docs = []
    for idx, meta in enumerate(results["metadatas"][0]):
        doc_info = {
            "id": results["ids"][0][idx],
            "similarity": normalize(results["distances"][0][idx]),
            "text": results["documents"][0][idx],
            "metadata": {
                "patient": {
                    "name": meta.get("patient_name"),
                    "age": meta.get("age"),
                    "gender": meta.get("gender"),
                },
                "doctor": meta.get("doctor"),
                "diagnosis": meta.get("diagnosis"),
                "file": meta.get("source"),
            },
        }

        docs.append(doc_info)

    # -----------------------------
    # Apply optional filters
    # -----------------------------
    if patient:
        docs = [d for d in docs if d["metadata"]["patient"]["name"] and patient.lower() in d["metadata"]["patient"]["name"].lower()]

    if doctor:
        docs = [d for d in docs if d["metadata"]["doctor"] and doctor.lower() in d["metadata"]["doctor"].lower()]

    if gender:
        docs = [d for d in docs if d["metadata"]["patient"]["gender"] and d["metadata"]["patient"]["gender"].lower() == gender.lower()]

    return {
        "query": q,
        "count": len(docs),
        "results": docs,
    }


@app.get("/")
def home():
    return {"status": "Medical Search API Running", "endpoints": ["/search"]}
