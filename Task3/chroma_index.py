"""
FINAL chroma_index.py — with canonical treatment string
This version:
✔ canonicalizes each prescription
✔ sorts them so duplicates ALWAYS match
✔ joins into ONE stable string for Chroma
✔ produces correct analytics
"""

import os
import json
import glob
from pathlib import Path
import re
import chromadb
from chromadb.utils import embedding_functions
import argparse


# ==========================================
# 1. Canonical prescription
# ==========================================
def canonicalize_prescription(p):
    """Turn each prescription entry into stable canonical format"""
    drug = (p.get("drug") or "").lower().strip()
    dose = (p.get("dose") or "").lower().strip()
    freq = (p.get("frequency") or "").lower().strip()

    # Normalize spacing
    drug = re.sub(r"\s+", " ", drug)
    dose = re.sub(r"\s+", " ", dose)
    freq = re.sub(r"\s+", " ", freq)

    # Normalize IV
    dose = re.sub(r"i\.?v\.?", "iv", dose)
    freq = re.sub(r"i\.?v\.?", "iv", freq)

    # Normalize mg
    dose = re.sub(r"(\d+)\s*mg", r"\1mg", dose)

    # Build final canonical string
    final = f"{drug} {dose} {freq}".strip()
    final = re.sub(r"\s+", " ", final)  # compress spaces

    return final


# ==========================================
# 2. Initialize Chroma
# ==========================================
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="medical_notes",
    embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
)


# ==========================================
# 3. Load structured JSON files
# ==========================================
def load_parsed_files(folder="outputs/clean"):
    files = sorted(glob.glob(os.path.join(folder, "*.json")))
    items = []

    for f in files:
        try:
            data = json.load(open(f, "r", encoding="utf8"))
        except:
            print(f"⚠ Skipping unreadable JSON: {f}")
            continue

        doc_id = Path(f).stem

        text = data.get("cleaned_text") or data.get("raw_text")
        if not text:
            print(f"⚠ Skipping {f} — no text found")
            continue

        patient = data.get("patient", {})

        # --------------------------
        # Canonical treatments LIST
        # --------------------------
        canonical_list = []
        for p in data.get("prescriptions", []):
            c = canonicalize_prescription(p)
            if c:
                canonical_list.append(c)

        # --------------------------
        # Convert LIST → stable STRING for Chroma
        # --------------------------
        if canonical_list:
            # Sort so duplicates produce identical strings
            canonical_list = sorted(canonical_list)

            # One stable canonical string:
            final_treatments = " | ".join(canonical_list)
        else:
            final_treatments = ""

        # --------------------------
        # Metadata (All must be strings)
        # --------------------------
        metadata = {
            "source": os.path.basename(f),
            "patient_name": patient.get("name") or "",
            "age": patient.get("age") or "",
            "gender": patient.get("gender") or "",
            "doctor": data.get("doctor") or "",
            "hospital": data.get("hospital") or "",
            "diagnosis": data.get("diagnosis") or "",
            "treatments": final_treatments,   # ALWAYS a canonical string ✔
        }

        items.append((doc_id, text, metadata))

    return items



# ==========================================
# 4. Index into Chroma
# ==========================================
def index_all(folder="outputs/clean", batch=32):
    items = load_parsed_files(folder)
    if not items:
        print("❌ No JSON files found")
        return

    print(f"📂 Indexing {len(items)} files...")

    ids, docs, metas = [], [], []

    for idx, (doc_id, text, meta) in enumerate(items, start=1):
        ids.append(doc_id)
        docs.append(text)
        metas.append(meta)

        if len(ids) == batch or idx == len(items):
            collection.add(ids=ids, documents=docs, metadatas=metas)
            print(f"Indexed batch of {len(ids)}")
            ids, docs, metas = [], [], []

    print("✅ Indexing complete.")


# ==========================================
# 5. Optional search test
# ==========================================
def query_text(q, n=5):
    return collection.query(query_texts=[q], n_results=n)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, default="outputs/clean")
    parser.add_argument("--query", type=str)
    args = parser.parse_args()

    index_all(folder=args.folder)

    if args.query:
        from pprint import pprint
        pprint(query_text(args.query))
