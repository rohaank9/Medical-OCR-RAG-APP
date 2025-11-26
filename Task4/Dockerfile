FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy RAG API code
COPY rag_api.py .
COPY gemini_ocr_improve.py .
COPY chroma_index.py .
COPY ./chroma_db ./chroma_db

EXPOSE 8001

CMD ["uvicorn", "rag_api:app", "--host", "0.0.0.0", "--port", "8001"]
