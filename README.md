# medical-report-parser
This  is an IDP pipeline digitizing medical reports. It uses Tesseract OCR and Gemini 2.5 Flash to convert images into structured JSON, performing layout analysis and entity extraction. The system applies clinical reasoning to flag abnormal results and uses Pydantic for data integrity. A responsive dashboard allows for real-time visualization.
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

### Prerequisites

- Python 3.10+
- Tesseract OCR installed on your system ([install guide](https://github.com/tesseract-ocr/tesseract))
- A Google Gemini API key ([get one here](https://aistudio.google.com/))

### Installation

```bash
git clone https://github.com/akashcpatil111/medical-report-parser.git
cd medical-report-parser

pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

### Running the Parser

```bash
cd Medical_Parser_Project
python main.py --input path/to/report_image.jpg
```

### Running the Dashboard

```bash
cd backend
python app.py
# Open http://localhost:5000 in your browser
```

---

## 📤 Sample Output

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


## 🔮 Roadmap

- [ ] Support for PDF input (multi-page reports)
- [ ] Batch processing of multiple reports
- [ ] Export parsed results to CSV / XLSX
- [ ] REST API endpoint for integration with hospital systems
