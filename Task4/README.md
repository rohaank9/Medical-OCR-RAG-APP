# Task 4 – Deployment (Docker-Based)

Because cloud deployment (AWS/GCP/HuggingFace/Railway) requires billing,  
this task is delivered using **local Docker deployment**, which is explicitly allowed by the assessment:

> “Public endpoint if possible, otherwise local Docker instructions.”

This Task-4 module provides:
- A Dockerized FastAPI RAG backend  
- Docker build + run instructions  
- A working local endpoint  
- Short usage summary  
- Deployment scripts  

---

## 📁 Folder Structure

```
Task4/
│
├── Dockerfile
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## 🐳 1. Build Docker Image

```bash
docker build -t rag-api .
```

---

## ▶️ 2. Run the Container

```bash
docker run -p 8001:8001 rag-api
```

Now your API is live at:

```
http://localhost:8001
```

---

## 🤖 3. Example Query (Task-3 RAG)

### Using browser:
```
http://localhost:8001/ask?q=Which patients had pneumonia?
```

### Or using curl:
```bash
curl "http://localhost:8001/ask?q=Which patients had pneumonia?"
```

---

## 🧠 4. docker-compose usage (optional)

```bash
docker compose up --build
```

---

## 🎉 Completed Deliverables

✔ Dockerfile  
✔ Deployment scripts  
✔ Working local endpoint  
✔ Usage instructions  
✔ Fully functional RAG system inside container  

This satisfies **Task 4**.

