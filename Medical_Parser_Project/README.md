# Medical Report Parser (Vision-to-JSON)

Digitize paper-based reports into machine-readable JSON using Tesseract OCR and Google Gemini.

## Phase 1: Environment Setup

1.  **Install Tesseract OCR**:
    *   **Windows**: Download the installer from [UB Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki).
    *   During installation, note the installation path (usually `C:\Program Files\Tesseract-OCR`).
    *   **CRITICAL**: Add this path to your System Environment Variable `PATH` so the specific command `tesseract` works in your terminal.
    *   **Mac**: Run `brew install tesseract`.

2.  **API Key**:
    *   Get a Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/).
    *   Set it as an environment variable `GEMINI_API_KEY` or paste it directly in `app.py` (line 15) for testing.

## Phase 2: Installation

Open your terminal in this folder and run:

```bash
pip install -r requirements.txt
```

## Phase 3: Running & Testing

Run the application:

```bash
python app.py
```

### What happens?
1.  **Image Generation**: A file `medical_report_test.png` is created automatically.
2.  **OCR**: Tesseract reads the text from the image.
3.  **Parsing**: Gemini converts the raw text into structured JSON.

### Expected Output
You should see a structured JSON object in your terminal:

```json
{
    "patient_name": "John Doe",
    "tests": [
        { "test_name": "Hemoglobin", "value": 14.5, "unit": "g/dL", "status": "Normal" },
        ...
    ]
}
```

## Phase 4: Customization

To test with your own report:
1.  Place your image in this folder.
2.  Rename it to `my_report.png` (or update line 23 in `app.py`).
3.  Run `python app.py` again.
