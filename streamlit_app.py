import json

import requests
import streamlit as st
import logging

# Configure logging for streamlit app (optional, might log to streamlit console)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
logger = logging.getLogger(__name__)

st.title("Resume Details Extractor")

logger.info("Streamlit app started.")

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF or DOCX)", type=["pdf", "docx"]
)

if uploaded_file is not None:
    if st.button("Extract Details"):
        files = {"file": uploaded_file}
        logger.info(f"User uploaded file: {uploaded_file.name}. Sending request to API.")
        api_url = "https://resumestandardizer-backend.onrender.com/extract_resume_details/"

        try:
            response = requests.post(api_url, files=files)
            response.raise_for_status()
            logger.info(f"API request successful. Status code: {response.status_code}")
            logger.debug(f"API response content: {response.text}")

            result = response.json()
            schema_json = result.get("schema_structured", {})
            formatter_json = result.get("formatter_structured", {})

            st.success("Resume processed successfully!")

            # Display the structured JSON results in a two-column layout.
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("✅ Schema-Enforced JSON")
                st.json(schema_json, expanded=True)

            with col2:
                st.subheader("🧩 Formatter-Based JSON")
                st.json(formatter_json, expanded=True)

            # Download buttons for each response
            st.markdown("### 📥 Download Options")
            colA, colB = st.columns(2)
            with colA:
                st.download_button(
                    "Download Schema JSON",
                    data=json.dumps(schema_json, indent=4),
                    file_name="resume_schema.json",
                    mime="application/json",
                )
            with colB:
                st.download_button(
                    "Download Formatter JSON",
                    data=json.dumps(formatter_json, indent=4),
                    file_name="resume_formatter.json",
                    mime="application/json",
                )

        except requests.exceptions.RequestException as e:
            logger.error(f"API request error: {e}")
            st.error(f"API error: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error from API response: {e}")
            st.error(f"JSON decode error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in streamlit app: {e}", exc_info=True)
            st.error(f"Unexpected error: {e}")
