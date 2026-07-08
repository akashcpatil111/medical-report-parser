# Medical Report Parser (Vision-to-JSON)

An IDP (Intelligent Document Processing) pipeline that digitizes medical reports. It uses Tesseract OCR and Google Gemini 2.5 Flash to convert scanned/photographed reports into structured JSON — performing layout analysis, medical entity extraction, and clinical reasoning to flag abnormal results, with Pydantic enforcing strict data integrity throughout.

---

## 🧠 How It Works

```
Medical Report Image
       │
       ▼
  Tesseract OCR          ← Raw text extraction from image
       │
       ▼
  Gemini 2.5 Flash       ← Layout analysis, header vs. table distinction,
  (Custom Prompting)        medical entity recognition
       │
       ▼
  Pydantic Validation    ← Strict schema enforcement, type checking,
                            error handling
       │
       ▼
  Structured JSON        ← Patient info, test names, values, units,
                            reference ranges, abnormal flags
       │
       ▼
  HTML Dashboard         ← Visual display of parsed results
```

---

## ✨ Key Features

- **Dual-stage extraction:** OCR handles the raw scan; Gemini handles semantic understanding — separating headers, patient metadata, and tabular lab values
- **Abnormal result flagging:** Clinical reasoning logic automatically flags values outside reference ranges
- **Resilient API layer:** Exponential backoff with retry decorators handles Gemini API rate limits and transient network failures, achieving ~99% pipeline reliability
- **Strict data integrity:** Pydantic models ensure every OCR output is parsed into typed, schema-validated JSON — no silent data corruption
- **Responsive dashboard:** Real-time visualization of parsed report data in the browser

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| OCR Engine | Tesseract OCR (pytesseract) |
| LLM | Google Gemini 2.5 Flash |
| Data Validation | Pydantic v2 |
| Async / Reliability | Python asyncio, Exponential Backoff |
| Frontend Dashboard | HTML5, CSS3 |
| Language | Python 3.10+ |

---

## 🚀 Getting Started

### Phase 1: Environment Setup

1. **Install Tesseract OCR**
   - **Windows**: Download the installer from [UB Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki). During installation, note the install path (usually `C:\Program Files\Tesseract-OCR`). **CRITICAL**: add this path to your System `PATH` environment variable so the `tesseract` command works in your terminal.
   - **Mac**: Run `brew install tesseract`.

2. **API Key**
   - Get a Google Gemini API key from [Google AI Studio](https://aistudio.google.com/).
   - Set it as an environment variable `GEMINI_API_KEY`, or paste it directly into `app.py` (line 15) for local testing.

### Phase 2: Installation

```bash
pip install -r requirements.txt
```

### Phase 3: Running & Testing

```bash
python app.py
```

**What happens:**
1. **Image generation** — a sample file `medical_report_test.png` is created automatically.
2. **OCR** — Tesseract reads the raw text from the image.
3. **Parsing** — Gemini converts the raw text into structured JSON.

**📤 Sample output** — you should see a structured JSON object in your terminal:

```json
{
  "patient": {
    "name": "John Doe",
    "age": 34,
    "gender": "Male",
    "report_date": "2025-06-01"
  },
  "lab_results": [
    {
      "test_name": "Hemoglobin",
      "value": 10.2,
      "unit": "g/dL",
      "reference_range": "13.0 - 17.0",
      "status": "LOW",
      "is_abnormal": true
    },
    {
      "test_name": "Blood Glucose (Fasting)",
      "value": 95,
      "unit": "mg/dL",
      "reference_range": "70 - 100",
      "status": "NORMAL",
      "is_abnormal": false
    }
  ]
}
```

### Phase 4: Customization

To test with your own report:
1. Place your image in this folder.
2. Rename it to `my_report.png` (or update line 23 in `app.py`).
3. Run `python app.py` again.

---

## 🔮 Roadmap

- [ ] Support for PDF input (multi-page reports)
- [ ] Batch processing of multiple reports
- [ ] Export parsed results to CSV / XLSX
- [ ] REST API endpoint for integration with hospital systems
