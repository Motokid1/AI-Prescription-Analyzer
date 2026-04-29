---

# 🧠 AI Prescription Analyzer

A production-ready **AI-powered healthcare application** that converts complex medical prescriptions (PDF/image/text) into **structured, patient-friendly insights** using OCR, LLMs, and intelligent processing pipelines.

---

# 🚀 Features

* 📄 Upload prescription (PDF / Image / Text)
* 🔍 Advanced OCR (PaddleOCR with smart preprocessing)
* 🧠 AI-powered extraction using LLM (Groq + LangChain)
* 🧾 Dynamic prescription understanding (no fixed format)
* 💊 Medicine breakdown (dosage, frequency, duration, refills)
* 📅 Daily medicine schedule generation
* ⚠️ Missing / unclear information detection
* 🧹 OCR cleanup agent for noisy inputs
* 📊 Confidence-aware extraction
* 🖥️ Clean, modern React UI
* 🛡️ Safety-first medical disclaimer

---

# 🏗️ Architecture

```text
                ┌────────────────────────────┐
                │        React UI            │
                │  (Vite + Axios + CSS)     │
                └────────────┬──────────────┘
                             │ HTTP API
                             ▼
                ┌────────────────────────────┐
                │       FastAPI Backend      │
                └────────────┬──────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
 OCR Pipeline        Cleanup Agent        Extraction Agent
(PaddleOCR)          (LLM)                (LLM Dynamic JSON)
        │                    │                    │
        └────────────┬───────┴───────┬────────────┘
                     ▼               ▼
             Explanation Agent   Checker + Scheduler
                     │               │
                     └───────┬───────┘
                             ▼
                  Structured API Response
```

---

# 🧠 Core Workflow

```text
1. User uploads prescription
2. OCR Pipeline extracts raw text
3. Smart OCR retry (fast → enhanced if needed)
4. OCR Cleanup Agent removes noise
5. Extraction Agent converts text → structured JSON
6. Explanation Agent simplifies medicines
7. Checker detects missing info
8. Schedule Agent generates daily plan
9. Response sent to UI
10. UI renders patient-friendly output
```

---

# ⚙️ Technologies Used

## Backend

* FastAPI
* Python 3.11+
* LangChain Core (LCEL)
* Groq LLM (llama-3.3-70b-versatile)
* PaddleOCR
* OpenCV
* Pydantic v2
* PyMuPDF

## Frontend

* React + Vite
* Axios
* CSS (custom styling)
* Lucide Icons

## AI / NLP

* LLM-based structured extraction
* Prompt engineering
* OCR post-processing
* Confidence-aware parsing

---

# 📁 Project Structure

```text
AI-Prescription-Analyzer/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py
│   │   │
│   │   ├── services/
│   │   │   ├── ocr_service.py
│   │   │   ├── pdf_service.py
│   │   │   ├── prescription_agent.py
│   │   │   ├── medicine_agent.py
│   │   │   ├── checker_agent.py
│   │   │   ├── schedule_agent.py
│   │   │   └── ocr_cleanup_agent.py
│   │   │
│   │   ├── prompts/
│   │   │   ├── extraction_prompt.py
│   │   │   ├── medicine_prompt.py
│   │   │   ├── checker_prompt.py
│   │   │   └── schedule_prompt.py
│   │   │
│   │   ├── schemas.py
│   │   ├── config.py
│   │   ├── main.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── UploadBox.jsx
│   │   │   ├── TextInputBox.jsx
│   │   │   ├── MedicineCard.jsx
│   │   │   ├── ResultSection.jsx
│   │   │   ├── ScheduleTable.jsx
│   │   │   ├── MissingInfoCard.jsx
│   │   │   └── LoadingSpinner.jsx
│   │   │
│   │   ├── pages/
│   │   │   └── PrescriptionAnalyzer.jsx
│   │   │
│   │   ├── api/
│   │   │   └── prescriptionApi.js
│   │   │
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│
├── README.md
```

---

# 🔍 Backend Modules Explained

## OCR Service (`ocr_service.py`)

* Multi-stage OCR pipeline
* Fast-first strategy (performance optimized)
* Preprocessing:

  * shadow removal
  * contrast enhancement
  * thresholding
* Extracts:

  * full OCR text
  * probable medicine lines

---

## OCR Cleanup Agent (`ocr_cleanup_agent.py`)

* Removes noise from OCR output
* Uses LLM to:

  * remove garbage text
  * preserve medical context
  * normalize structure

---

## Extraction Agent (`prescription_agent.py`)

* Converts cleaned text → structured JSON
* Handles:

  * dynamic prescription formats
  * abbreviations
  * missing values
* Uses robust JSON parsing fallback

---

## Medicine Agent (`medicine_agent.py`)

* Converts medicines → simple explanation
* Adds safety notes
* Handles parsing failures gracefully

---

## Checker Agent (`checker_agent.py`)

* Detects:

  * missing dosage
  * unclear names
  * incomplete instructions

---

## Schedule Agent (`schedule_agent.py`)

* Converts frequency → time slots
* Example:

  * BD → Morning + Night
  * TDS → Morning + Afternoon + Night

---

# 🎨 Frontend Flow

```text
User Input → API Call → Response → UI Rendering
```

UI shows:

* Cleaned prescription
* Raw OCR text
* Medicine cards
* Schedule table
* Missing info warnings
* Safety disclaimer

---

# 🧠 Best Practices Followed

## Architecture

* Modular service-based backend
* Separation of concerns (OCR / LLM / API)
* Scalable agent-based design

## AI Engineering

* Prompt engineering with structured outputs
* JSON parsing fallback handling
* Multi-step LLM pipeline (cleanup → extraction)

## Performance

* Smart OCR retry (fast-first)
* Lazy model loading
* Reduced unnecessary LLM calls

## Robustness

* Handles malformed OCR
* Handles invalid JSON from LLM
* Graceful fallback responses

## UX

* Shows both raw and cleaned text
* Confidence indicators
* Clear error messages

## Security

* Uses `.env` for API keys
* No hardcoded secrets

---

# ⚡ Performance Optimization

```text
Fast Path:
1 OCR run → if good → done

Fallback Path:
3 OCR runs → merge → cleanup → extraction
```

---

# ▶️ How to Run

## Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

## Frontend

```bash
cd frontend
npm install
npm run dev
```

---

# 🌐 API Endpoint

```http
POST /api/v1/analyze
```

### Input:

* file (optional)
* text (optional)

### Output:

```json
{
  "raw_text": "...",
  "cleaned_text": "...",
  "medicines": [...],
  "explanations": [...],
  "daily_schedule": [...],
  "missing_information": [...]
}
```

---

# ⚠️ Limitations

* Handwritten prescriptions may still have low confidence
* OCR accuracy depends on image quality
* LLM may require manual validation for critical cases

---

# 🚀 Future Enhancements

* TrOCR handwriting fallback
* Drug interaction checker
* Auto prescription correction UI
* Multilingual OCR support
* Pharmacy integration
* PDF export

---

# 🛡️ Disclaimer

> This system is for informational purposes only.
> Always consult a doctor or pharmacist before making medical decisions.

---

# 👨‍💻 Author

**Rohith Ganesh Adigopula**
Systems Engineer @ TCS
AI | Backend | Cloud | GenAI

---

