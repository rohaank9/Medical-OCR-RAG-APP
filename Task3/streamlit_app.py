import streamlit as st
import requests
import json
import base64

FASTAPI_URL = "http://localhost:8001"

st.set_page_config(page_title="Medical RAG Assistant", layout="wide")

st.title("💊 Medical RAG Assistant")
st.write("Upload medical notes → OCR → JSON → ChromaDB → Ask questions.")

# ================================
# 1) FILE UPLOAD
# ================================
st.subheader("📤 Upload Image or PDF")

uploaded_file = st.file_uploader(
    "Upload handwritten medical note",
    type=["jpg", "jpeg", "png", "pdf"]
)

if uploaded_file:
    st.success("File selected! Ready to process.")

    if st.button("🔄 Run OCR + Extract JSON + Index into Chroma"):
        with st.spinner("Processing with Gemini OCR via FastAPI…"):

            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}

            try:
                resp = requests.post(f"{FASTAPI_URL}/upload", files=files)

                if resp.status_code == 200:
                    data = resp.json()
                    if data["status"] == "success":
                        st.success(f"✅ {data['message']}")
                    else:
                        st.error(data["message"])
                else:
                    st.error(f"❌ API Error: {resp.text}")

            except Exception as e:
                st.error(f"❌ Failed to contact FastAPI: {e}")

# ================================
# 2) RAG QUESTION ANSWERING
# ================================
st.subheader("💬 Ask a medical question")

query = st.text_input("Enter your question:")

if st.button("Ask"):
    if not query.strip():
        st.warning("Enter a question first.")
    else:
        with st.spinner("Thinking…"):
            try:
                resp = requests.post(f"{FASTAPI_URL}/ask", json={"question": query})
                data = resp.json()

                if "answer" in data:
                    st.success(data["answer"])

                    # Show analytics results if present
                    if data.get("type") == "diagnosis_query":
                        st.markdown("### 🧑‍⚕️ Patients with this diagnosis:")
                        patients = data.get("patients", [])
                        if patients:
                            for p in patients:
                                st.write(f"- {p}")
                        else:
                            st.write("No matching patients found.")

                    elif data.get("type") == "treatment_frequency":
                        st.markdown("### 💊 Most Frequent Treatment:")
                        stats = data.get("treatment_stats", {})
                        if stats:
                            st.write(f"**Treatment:** {stats.get('treatment')}")
                            st.write(f"**Count:** {stats.get('count')}")
                        else:
                            st.write("No treatment statistics available.")

                    # Show provenance (if exists)
                    prov = data.get("provenance", [])
                    if isinstance(prov, list):
                        st.markdown("### 📄 Sources")
                        for src in prov:
                            if isinstance(src, dict):
                                st.markdown(
                                    f"- **Doc:** {src.get('id')} | "
                                    f"**Patient:** {src.get('patient')} | "
                                    f"**Doctor:** {src.get('doctor')} | "
                                    f"**Score:** {src.get('score')}"
                                )

                else:
                    st.warning("No answer generated.")


            except Exception as e:
                st.error(f"❌ Error contacting RAG API: {e}")
