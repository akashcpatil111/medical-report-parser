import os
import sys
import json
import asyncio
import pytesseract
from PIL import Image, ImageDraw, ImageFont
import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
# The environment provides the API key automatically in this workspace.
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Point to Tesseract (Update this path if Tesseract is not in your System PATH)
# On Windows, it's usually: r'C:\Program Files\Tesseract-OCR\tesseract.exe'
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

IMAGE_FILE = "medical_report_test.png"

# --- SCHEMA DEFINITION (Validation) ---
class MedicalRecord(BaseModel):
    test_name: str = Field(description="Name of the lab test")
    value: float = Field(description="Numerical result")
    unit: str = Field(description="Measurement unit")
    status: str = Field(description="Normal, High, or Low")

class ReportData(BaseModel):
    patient_name: str
    date: str
    tests: List[MedicalRecord]

# --- PHASE 1: GENERATE MOCK REPORT ---
def generate_test_image():
    """Simulates a paper report by creating an image file."""
    print(f"[*] Generating sample report: {IMAGE_FILE}...")
    img = Image.new('RGB', (800, 600), color='white')
    d = ImageDraw.Draw(img)
    
    try:
        font_header = ImageFont.load_default()
        font_text = ImageFont.load_default()
    except Exception:
        font_header = font_text = None

    content = [
        "SafeHealth Medical Lab",
        "Patient Name: John Doe",
        "Date: 2024-10-25",
        "--------------------------------------------------",
        "Test                Result      Unit      Ref Range",
        "Hemoglobin          14.5        g/dL      13.0-17.0",
        "White Blood Cells   6.5         K/uL      4.0-11.0",
        "Platelets           250         K/uL      150-450",
        "Glucose (Fasting)   115         mg/dL     70-99",
        "--------------------------------------------------",
        "Physician: Dr. Smith"
    ]
    
    y = 50
    for line in content:
        d.text((50, y), line, fill=(0,0,0))
        y += 30
    
    img.save(IMAGE_FILE)
    print("[+] Image saved successfully.")

# --- PHASE 2: OCR EXTRACTION ---
def perform_ocr(image_path):
    """Component: OCR Engine (Vision-to-Text)"""
    print("[*] Performing OCR extraction...")
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        print("--- Extracted Raw Text ---")
        print(text.strip())
        return text
    except Exception as e:
        print(f"[!] OCR Error: {e}. Ensure Tesseract is installed.")
        return None

# --- PHASE 3: MEDICAL ENTITY PARSER ---
async def structure_data_with_backoff(raw_text):
    """Component: Medical Entity Parser (LLM) with Exponential Backoff"""
    print("[*] Sending text to Gemini for Layout Analysis & Parsing...")
    
    model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')
    
    prompt = f"""
    Analyze this medical report OCR text. 
    1. Identify the layout (Header vs Table).
    2. Extract patient data and test results.
    3. Determine status (Normal/High/Low) based on provided Ref Ranges.
    
    Raw Text:
    {raw_text}
    """

    # Exponential Backoff Implementation
    for attempt in range(5):
        try:
            response = model.generate_content(
                prompt,
                generation_config={
                    "response_mime_type": "application/json",
                    "response_schema": ReportData
                }
            )
            return response.text
        except Exception as e:
            print(f"[!] Attempt {attempt + 1} failed: {e}")
            if attempt == 4:
                print("[!] API failed after 5 attempts.")
                return None
            await asyncio.sleep(2 ** attempt)

# --- MAIN EXECUTION ---
async def main():
    # 1. Setup
    if not os.path.exists(IMAGE_FILE):
        generate_test_image()
    else:
        print(f"[*] Using existing file: {IMAGE_FILE}")
    
    # 2. Vision/OCR
    raw_text = perform_ocr(IMAGE_FILE)
    if not raw_text: return
    
    # 3. Parsing
    json_result = await structure_data_with_backoff(raw_text)
    
    if json_result:
        # Parse JSON
        data = json.loads(json_result)
        
        # 1. Print to Terminal (Requirement)
        print("\n--- FINAL STRUCTURED JSON ---")
        print(json.dumps(data, indent=4))
        print("------------------------------")
        
        # 2. Save for Dashboard (Improvement) - DISABLED
        # We save as a JS file to bypass CORS issues when opening HTML locally
        # js_content = f"window.MEDICAL_DATA = {json.dumps(data, indent=4)};"
        # with open("dashboard_data.js", "w") as f:
        #     f.write(js_content)
        # print("[+] Dashboard data saved to 'dashboard_data.js'")

if __name__ == "__main__":
    asyncio.run(main())