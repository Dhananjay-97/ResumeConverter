import json
import os
import pathlib
import tempfile
import logging

from decouple import config
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from google import genai
from google.genai import types
from markitdown import MarkItDown

from prompt_manager import prompt_manager
from schemas import ResumeSchema

app = FastAPI(title="Resume Details Extractor API")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
logger = logging.getLogger(__name__)

# Default prompt that enforces the resume details schema
RESUME_DETAILS_EXTRACTOR = prompt_manager.get_resume_extractor_prompt()

# Formatter prompt for plain JSON structuring
RESUME_DETAILS_FORMATTER = prompt_manager.get_resume_formatter_prompt()


GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")
    
client = genai.Client(api_key=GOOGLE_API_KEY)


def docx_to_text_markitdown(docx_path):
    logger.info(f"Converting DOCX file: {docx_path} to text using markitdown")
    converter = MarkItDown()
    result = converter.convert(docx_path)
    logger.info(f"DOCX conversion to text completed.")
    return result.text_content


@app.post("/extract_resume_details/")
async def extract_resume_details(file: UploadFile = File(...)):
    logger.info(f"Received request to extract resume details for file: {file.filename}")
    try:
        file_extension = pathlib.Path(file.filename).suffix.lower()

        if file_extension == ".pdf":
            file_bytes = await file.read()
            resume_part = types.Part.from_bytes(
                data=file_bytes, mime_type="application/pdf"
            )
            logger.debug(f"File type detected: PDF")
        elif file_extension == ".docx":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
                tmp_file.write(await file.read())
                logger.debug(f"Saving uploaded DOCX to temporary file: {tmp_file.name}")
                docx_path = tmp_file.name
            resume_text = docx_to_text_markitdown(docx_path)
            resume_part = types.Part.from_text(text=resume_text)
            os.unlink(docx_path)
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Please upload a PDF or DOCX file.",
            )

        # Approach 1: Schema-Enforced structured JSON
        schema_response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[resume_part, RESUME_DETAILS_EXTRACTOR],
            config={
                "response_mime_type": "application/json",
                "response_schema": ResumeSchema,
            },
        )
        logger.debug(f"Schema-enforced JSON response generated.")

        # Approach 2: Formatter-Based structured JSON (plain formatting)
        formatter_response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[resume_part, RESUME_DETAILS_FORMATTER],
            config={"response_mime_type": "application/json"},
        )

        logger.debug(f"Formatter-based JSON response generated.")

        try:
            schema_structured = json.loads(schema_response.text)
            logger.debug(f"Schema response JSON decoded successfully.")
        except json.JSONDecodeError as e:
            schema_structured = {
                "error": f"Schema response decoding failed: {e}",
                "raw": schema_response.text,
            }
            logger.error(f"Schema response JSON decoding error: {e}", exc_info=True)

        try:
            formatter_structured = json.loads(formatter_response.text)
            logger.debug(f"Formatter response JSON decoded successfully.")
        except json.JSONDecodeError as e:
            formatter_structured = {
                "error": f"Formatter response decoding failed: {e}",
                "raw": formatter_response.text,
            }
            logger.error(f"Formatter response JSON decoding error: {e}", exc_info=True)

        return JSONResponse(
            content={
                "schema_structured": schema_structured,
                "formatter_structured": formatter_structured,
            },
            status_code=200,
        )
        logger.info(f"Resume details extraction and JSON response completed successfully for file: {file.filename}")


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8090)
    logger.info("Resume Details Extractor API started successfully.")
