# Medical-OCR-RAG-APP


This repository contains the **complete, end-to-end solution** implemented using:

- **Gemini OCR & Gemini 2.5 Flash**
- **ChromaDB + Sentence Transformers**
- **FastAPI REST APIs**
- **Streamlit Chatbot UI**
- **Docker deployment (Task 4)**

Each task is isolated in its own folder and can be executed independently.

---

# 📦 Repository Structure

```
IntraIntel_Assessment/
│
├── Task1_&_Task2/
│     ├── gemini_ocr_improve.py
│     ├── chroma_index.py
│     ├── search_api.py
│     ├── requirements.txt
│     ├── notes/
│     ├── outputs/
│     └── README.md
│
├── Task3/
│     ├── rag_api.py
│     ├── streamlit_app.py
│     ├── gemini_ocr_improve.py       # Local copy for independent execution
│     ├── chroma_index.py             # Local copy for independent execution
│     ├── requirements.txt
│     └── README.md
│
└── Task4/
      ├── Dockerfile
      ├── requirements.txt
      ├── docker-compose.yml
      └── README.md
```

---

# 🔧 Global Environment Setup

You can run all tasks inside a shared virtual environment.

### 1. Create virtual environment
```bash
python -m venv venv
```

### 2. Activate
**Windows**
```bash
venv\Scripts\activate
```
**Mac/Linux**
```bash
source venv/bin/activate
```

### 3. Install dependencies per task
Example:
```bash
cd Task1_&_Task2
pip install -r requirements.txt
```

### 4. Configure Gemini API Key
```bash
setx GEMINI_API_KEY "your_key_here"     # Windows
export GEMINI_API_KEY="your_key_here"   # Linux/Mac
```

---

# 📝 **Task Summaries**

---

## 🧾 Task 1 – OCR Digitization
- Upload JPG/PNG/PDF medical notes  
- Gemini OCR → raw text  
- Stored in `outputs/raw/`  

➡️ Detailed instructions: **Task1_&_Task2/README.md**

---

## 📋 Task 2 – Structured JSON & Summary
- Extracts:
  - patient
  - diagnosis
  - prescriptions
- Outputs structured JSON in `outputs/clean/`
- Produces Task-2 summary JSON in `outputs/task2/`
- Can batch process multiple notes

➡️ Detailed instructions: **Task1_&_Task2/README.md**

---

## 🤖 Task 3 – Mini RAG Medical QA System (Standalone)

Task 3 includes **its own copies** of OCR & indexing modules:

- `gemini_ocr_improve.py`
- `chroma_index.py`

So it works **completely independently**.

### Features:
✔ “Which patients had X diagnosis?”  
✔ “Most frequent treatment?”  
✔ General clinical QA  
✔ Streamlit chatbot  
✔ FastAPI RAG backend  

### Warning:
After uploading new notes via Streamlit, **restart RAG API**:
```bash
uvicorn rag_api:app --reload --port 8001
```

➡️ Detailed instructions: **Task3/README.md**

---

## 🚀 Task 4 – Deployment (Docker-Based)

Cloud deployment (AWS/GCP/HuggingFace/Railway) could not be used due to billing restrictions.

The assessment explicitly allows:

> “Public endpoint if possible, **otherwise local Docker instructions**.”

Task 4 provides:
- Dockerfile  
- docker-compose.yml  
- Working local endpoint  
- Deployment scripts  

### Example:
```bash
docker build -t rag-api .
docker run -p 8001:8001 rag-api
```

Endpoint:
```
http://localhost:8001
```

➡️ Detailed instructions: **Task4/README.md**

---

# 🧠 **Decision Log & Architecture Rationale**

This section explains **why** specific technologies were chosen, compliant with assessment constraints.

---

## 🚫 1. Why Not AWS Textract or GCP Document AI?

Because both require **billing activation**, which was not possible due to:
- credit card verification
- auto-upgrade risk
- OCR usage cost

### ✔ Decision:
Use **Gemini OCR (Gemini 2.5 Flash Vision)**.

### ✔ Why Gemini OCR?
- Free-tier available  
- Excellent accuracy for handwritten notes  
- Zero cost  
- Supports vision → no additional OCR pipeline needed  
- Works perfectly with FastAPI + Streamlit  

---

## 🤖 2. Why Not LangChain or LlamaIndex?



LangChain not used because:
- Adds complexity  
- Harder to debug  
- Slower inside Docker  
- Unnecessary abstractions  
- Pure Python gives full control and transparency  

Thus, pure Python + ChromaDB was the cleanest solution.

---

## 🧬 3. Why ChromaDB + Sentence Transformers?

Alternatives considered:
- Pinecone → billing  
- Qdrant Cloud → billing  
- FAISS → lacks metadata filtering  
- Milvus → heavy & large setup  

### ✔ ChromaDB chosen because:
- Free & lightweight  
- Persistent local store  
- Easy metadata filtering  
- Perfect for Docker  

### ✔ Sentence Transformers (MiniLM) chosen because:
- Fast  
- High accuracy  
- Free  
- Works well in limited-resource environments  

---

## 🔮 4. Why Gemini 2.5 Flash for RAG?

Gemini selected over GPT/Claude/LLaMA because:
- Free tier  
- Strong JSON structuring  
- Great reasoning ability  
- Supports context-grounded answers  
- Simple API  

Perfect for medical note extraction + RAG.

---

## 💡 5. Thought Process Behind Architecture

### ✔ Keep tasks modular  
Each task runs independently.

### ✔ Local-first deployment  
No dependence on external cloud services.

### ✔ Reproducibility  
Anyone can clone the repo and run the system locally with:
```
python gemini_ocr_improve.py notes/
python chroma_index.py --folder outputs/clean
uvicorn rag_api:app --reload
```

### ✔ Docker for Deployment (Task 4)  
Ensures cross-platform portability.

---

## 🤝 6. AI Tools Used During Development

### ✔ ChatGPT (GPT-5.1)
Used for:
- Debugging  
- Prompt improvements  
- Architecture discussion  
- Documentation refinement  
- Fixing embedding logic  
- Validating RAG patterns  

### ✔ Perplexity AI
Used for:
- API documentation checks  
- Model comparisons  
- Research on embeddings & vector DB behaviors  

Documenting tool usage matches assessment expectations for transparency.

---

## 🌟 7. Benefits of This Solution

- 100% free-tier compatible  
- Reproducible  
- Zero cloud reliance  
- Modular design  
- Works fully offline except for Gemini API  
- Accurate OCR + structured JSON  
- Fast RAG retrieval  
- Clean Docker deployment  
- Detailed documentation for reviewers  

---

# ▶️ Quickstart: Run Complete System

### 1. Run OCR + Indexing (Task 1 & 2)
```bash
cd Task1_&_Task2
python gemini_ocr_improve.py notes/
python chroma_index.py --folder outputs/clean
```

### 2. Start RAG API (Task 3)
```bash
cd ../Task3
uvicorn rag_api:app --reload --port 8001
```

### 3. Optional: Streamlit Chatbot
```bash
streamlit run streamlit_app.py
```

---

# 🐳 Quickstart: Docker Deployment (Task 4)

```bash
cd Task4
docker build -t rag-api .
docker run -p 8001:8001 rag-api
```

Or:

```bash
docker compose up --build
```

API available at:
```
http://localhost:8001
```

---

# 🎉 Final Notes

- All tasks (1–4) are fully completed  
- All requirements from the assessment PDF are satisfied  
- Each module is documented, reproducible, and independently testable  
- Docker deployment fulfills Task-4 without needing AWS/GCP  

