import os
import json
import google.generativeai as genai

def setup_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ GEMINI_API_KEY is not set.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")

# ----------------------------------------------------
# 1️⃣ Extract RAW TEXT from image/PDF
# ----------------------------------------------------
def gemini_extract_raw_text(file_path):
    model = setup_gemini()

    with open(file_path, "rb") as f:
        bytes_data = f.read()

    mime = "application/pdf" if file_path.lower().endswith(".pdf") else "image/jpeg"

    prompt = "Extract ALL readable text from this medical note. Return plain text only."

    response = model.generate_content(
        [
            prompt,
            {"mime_type": mime, "data": bytes_data}
        ],
        request_options={"timeout": 60}   # 30 sec timeout
    )


    return response.text.strip()


# ----------------------------------------------------
# 2️⃣ Structured JSON (Task 1)
# ----------------------------------------------------
def gemini_structure(raw_text):
    model = setup_gemini()

    prompt = f"""
    You are a medical AI. Convert the OCR text below into structured JSON.

    Return JSON with this EXPLICIT structure:

    {{
      "patient": {{
          "name": string or null,
          "age": string or null,
          "gender": string or null
      }},
      "doctor": string or null,
      "hospital": string or null,
      "date": string or null,
      "diagnosis": string or null,
      "prescriptions": [
          {{
            "drug": string or null,
            "dose": string or null,
            "frequency": string or null,
            "duration": string or null
          }}
      ],
      "cleaned_text": string
    }}

    Rules:
    - Use ONLY what is present.
    - No hallucinations.
    - cleaned_text = corrected OCR version.
    - Always return valid JSON.

    TEXT:
    {raw_text}
    """

    response = model.generate_content(prompt)
    return response.text


# ----------------------------------------------------
# 3️⃣ Convert to Task-2 Summary JSON (Assessment Required)
# ----------------------------------------------------
def convert_for_task2(structured_dict):
    patient = structured_dict.get("patient", {})

    # Combine prescriptions → Treatment string
    treatments = []
    for p in structured_dict.get("prescriptions", []):
        drug = p.get("drug")
        dose = p.get("dose")
        freq = p.get("frequency")

        if drug:
            combined = drug
            if dose:
                combined += f" {dose}"
            if freq:
                combined += f", {freq}"
            treatments.append(combined)

    treatment_str = "; ".join(treatments) if treatments else None

    summary = {
        "Patient": patient.get("name"),
        "Diagnosis": structured_dict.get("diagnosis"),
        "Treatment": treatment_str,
        "Follow-up": None
    }

    return summary


# ----------------------------------------------------
# 4️⃣ Process files → produce BOTH outputs
# ----------------------------------------------------
def process_path(path):
    os.makedirs("outputs/raw", exist_ok=True)
    os.makedirs("outputs/clean", exist_ok=True)
    os.makedirs("outputs/task2", exist_ok=True)

    if os.path.isfile(path):
        files = [path]
    else:
        files = [
            os.path.join(path, f)
            for f in os.listdir(path)
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".pdf"))
        ]

    for f in files:
        base = os.path.basename(f)
        print(f"\n🔍 Processing {base}")

        # ---- RAW TEXT ----
        raw_text = gemini_extract_raw_text(f)
        raw_out = f"outputs/raw/{base}.txt"
        with open(raw_out, "w", encoding="utf8") as fw:
            fw.write(raw_text)
        print(f"📄 Saved raw text → {raw_out}")

        # ---- STRUCTURED JSON ----
        structured = gemini_structure(raw_text)
        import re
        structured_clean = re.sub(r"```[a-zA-Z0-9_-]*", "", structured)
        structured_clean = structured_clean.replace("```", "").strip()


        try:
            structured_dict = json.loads(structured_clean)
            structured_dict["raw_text"] = raw_text
        except:
            structured_dict = {"error": "Invalid JSON", "raw": structured_clean}

        json_out = f"outputs/clean/{base}.json"
        with open(json_out, "w", encoding="utf8") as fw:
            json.dump(structured_dict, fw, indent=2)
        print(f"✅ Saved Task-1 structured JSON → {json_out}")

        # ---- TASK 2 SUMMARY JSON ----
        if "error" not in structured_dict:
            summary = convert_for_task2(structured_dict)
        else:
            summary = {"error": "cannot convert", "source": base}

        summary_out = f"outputs/task2/{base}_summary.json"
        with open(summary_out, "w", encoding="utf8") as fw:
            json.dump(summary, fw, indent=2)
        print(f"📘 Saved Task-2 summary JSON → {summary_out}")


# ----------------------------------------------------
# MAIN
# ----------------------------------------------------
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("❌ ERROR: Please provide a file path.")
        sys.exit(1)

    path = sys.argv[1]
    process_path(path)
