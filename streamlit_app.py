import streamlit as st
import requests
import json

st.title("Resume Details Extractor")

uploaded_file = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    if st.button("Extract Details"):
        files = {"file": uploaded_file}
        api_url = "https://resumeconverter.onrender.com/8080/extract_resume_details/"
        # api_url = "http://localhost:8080/extract_resume_details/"

        try:
            response = requests.post(api_url, files=files)
            response.raise_for_status()

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
                    mime="application/json"
                )
            with colB:
                st.download_button(
                    "Download Formatter JSON",
                    data=json.dumps(formatter_json, indent=4),
                    file_name="resume_formatter.json",
                    mime="application/json"
                )

        except requests.exceptions.RequestException as e:
            st.error(f"API error: {e}")
        except json.JSONDecodeError as e:
            st.error(f"JSON decode error: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
