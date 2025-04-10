from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from google.genai import types
from google import genai
from schemas import ResumeSchema
import json
import pathlib
import docx
from markitdown import MarkItDown
import os
import tempfile
from prompt_manager import prompt_manager

app = FastAPI(title="Resume Details Extractor API")

# Default prompt that enforces the resume details schema
RESUME_DETAILS_EXTRACTOR = prompt_manager.get_resume_extractor_prompt()
# Formatter prompt for plain JSON structuring
RESUME_DETAILS_FORMATTER = (
    "Your job is to format the given context in valid JSON structure without changing any context. "
    "Ensure that all keys and string values are enclosed in double quotes and the output is valid JSON."
)
# RESUME_DETAILS_FORMATTER = "Your job is to format the given context in valid JSON structure without changing any context."

GOOGLE_API_KEY = "AIzaSyDgzJX7XWg5lC5XiWVKvOfp1Et1dX82I6Q"
client = genai.Client(api_key=GOOGLE_API_KEY)

def docx_to_text_markitdown(docx_path):
    converter = MarkItDown()
    result = converter.convert(docx_path)
    return result.text_content

@app.post("/extract_resume_details/")
async def extract_resume_details(file: UploadFile = File(...)):
    try:
        file_extension = pathlib.Path(file.filename).suffix.lower()

        if file_extension == '.pdf':
            file_bytes = await file.read()
            resume_part = types.Part.from_bytes(data=file_bytes, mime_type='application/pdf')
        elif file_extension == '.docx':
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
                tmp_file.write(await file.read())
                docx_path = tmp_file.name
            resume_text = docx_to_text_markitdown(docx_path)
            resume_part = types.Part.from_text(text=resume_text)
            os.unlink(docx_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload a PDF or DOCX file.")

        # Approach 1: Schema-Enforced structured JSON
        schema_response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[resume_part, RESUME_DETAILS_EXTRACTOR],
            config={
                'response_mime_type': 'application/json',
                'response_schema': ResumeSchema,
            },
        )

        # Approach 2: Formatter-Based structured JSON (plain formatting)
        formatter_response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[resume_part, RESUME_DETAILS_FORMATTER],
            config={'response_mime_type': 'application/json'}
        )

        try:
            schema_structured = json.loads(schema_response.text)
        except json.JSONDecodeError as e:
            schema_structured = {"error": f"Schema response decoding failed: {e}", "raw": schema_response.text}

        try:
            formatter_structured = json.loads(formatter_response.text)
        except json.JSONDecodeError as e:
            formatter_structured = {"error": f"Formatter response decoding failed: {e}", "raw": formatter_response.text}

        return JSONResponse(content={
            "schema_structured": schema_structured,
            "formatter_structured": formatter_structured
        }, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
