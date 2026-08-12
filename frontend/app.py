import streamlit as st
import requests
import base64
import pandas as pd
import json
import os

# API URL
# In a real deployment, this would be an environment variable.
API_URL = os.environ.get("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Document Extractor", layout="wide")

st.title("Automated Invoice & Resume Extractor")
st.markdown("Extract structured data from Invoices and Resumes using Gemini.")

# 1. Multi-Document Selector
doc_type = st.radio("Select Document Type", ["Invoice", "Resume"], horizontal=True)

# 2. Drag-and-drop file uploader
uploaded_file = st.file_uploader(f"Upload {doc_type} (PDF or TXT)", type=["pdf", "txt"])

def display_pdf(file_bytes):
    base64_pdf = base64.b64encode(file_bytes).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    
    # 3. Side-by-Side View
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Raw Document")
        if uploaded_file.name.lower().endswith(".pdf"):
            display_pdf(file_bytes)
        else:
            st.text_area("Document Content", file_bytes.decode('utf-8'), height=600)
            
    with col2:
        st.subheader("Extracted Data")
        
        if st.button("Extract Data", type="primary"):
            with st.spinner("Extracting with LLM..."):
                endpoint = "/extract/invoice" if doc_type == "Invoice" else "/extract/resume"
                
                # Determine MIME type based on extension since Streamlit's `type` attribute can sometimes be generic
                mime_type = "application/pdf" if uploaded_file.name.lower().endswith(".pdf") else "text/plain"
                files = {"file": (uploaded_file.name, file_bytes, mime_type)}
                
                try:
                    response = requests.post(f"{API_URL}{endpoint}", files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        data = result.get("data", {})
                        metadata = result.get("metadata", {})
                        
                        # 4. Confidence Score / Retries Display
                        # E.g., "Parsed successfully with 100% Pydantic schema compliance."
                        st.success(f"✅ {metadata.get('message', 'Parsed successfully.')}")
                        
                        # Display extracted data in JSON format
                        st.json(data)
                        
                        # Format specific lists as tables for CSV export
                        list_data = None
                        if doc_type == "Invoice" and "line_items" in data and data["line_items"]:
                            list_data = pd.DataFrame(data["line_items"])
                            st.write("Line Items Table")
                            st.dataframe(list_data, use_container_width=True)
                        elif doc_type == "Resume":
                            if "experience" in data and data["experience"]:
                                list_data = pd.DataFrame(data["experience"])
                                st.write("Experience Table")
                                st.dataframe(list_data, use_container_width=True)
                        
                        # 5. Export Options
                        export_col1, export_col2 = st.columns(2)
                        with export_col1:
                            st.download_button(
                                label="Download JSON",
                                data=json.dumps(data, indent=2),
                                file_name=f"extracted_{doc_type.lower()}.json",
                                mime="application/json"
                            )
                        
                        with export_col2:
                            if list_data is not None:
                                csv = list_data.to_csv(index=False).encode('utf-8')
                                st.download_button(
                                    label="Download CSV Table",
                                    data=csv,
                                    file_name=f"extracted_{doc_type.lower()}_table.csv",
                                    mime="text/csv"
                                )
                            
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Connection Error: Is the FastAPI backend running on http://localhost:8000?")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
