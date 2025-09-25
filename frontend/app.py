import streamlit as st
import requests
import os
import plotly.io as pio

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖",
    layout="centered",
)

st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 800px;
    }
    h1 {
        font-size: 2.5rem;
        font-weight: 700;
        color: #4B0082; /* Deep purple for a rich, tech-like feel */
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        background: -webkit-linear-gradient(45deg, #4B0082, #8A2BE2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    h3 {
        color: #333;
        font-size: 1.5rem;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        border-left: 5px solid #4B0082;
        padding-left: 10px;
    }
    .stButton>button {
        background-color: #4B0082;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #6A5ACD;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }
    .stTextArea label, .stFileUploader label {
        font-weight: bold;
        color: #333;
    }
    .stInfo, .stSuccess, .stError, .stWarning {
        border-left: 5px solid;
        border-radius: 5px;
        padding: 10px;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .stInfo { border-color: #4682B4; background: #E6F0F8; color: #2C5B85; }
    .stSuccess { border-color: #2E8B57; background: #E9F4ED; color: #226941; }
    .stError { border-color: #DC143C; background: #F8E7E9; color: #9B1028; }
    .stWarning { border-color: #FFD700; background: #FFF9E9; color: #B39600; }
</style>
""", unsafe_allow_html=True)


st.title("AI Assistant")
st.markdown("---")


# --- File Upload Section ---
st.markdown("### Upload a file")
uploaded_file = st.file_uploader(
    "Upload a document (.pdf, .docx) or a data file (.csv, .xlsx)",
    type=["pdf", "docx", "csv", "xlsx"]
)
if st.button("Upload"):
    if uploaded_file:
        with st.spinner(f"Uploading {uploaded_file.name}..."):
            try:
                files = {
                    'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
                }
                response = requests.post(f"{BACKEND_URL}/upload_file", files=files)
                if response.status_code == 200:
                    result = response.json()
                    st.session_state["uploaded_file_name"] = result.get("file_name")
                    status_message = result.get("status")
                    st.success(status_message)
                else:
                    st.error(f"Error: {response.status_code} - {response.json().get('detail', 'Unknown error')}")
            except requests.exceptions.ConnectionError:
                st.error("Connection error. Is the FastAPI backend running and accessible?")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please upload a file first.")
st.markdown("---")


# --- Query Section ---
st.markdown("### Ask a question")
query = st.text_area("Enter your query:", height=100)
if st.button("Analyze"):
    if query:
        with st.spinner("Analyzing query..."):
            try:
                payload = {
                    "query": query,
                    "file_name": st.session_state.get("uploaded_file_name")
                }
                response = requests.post(f"{BACKEND_URL}/analyze_query", json=payload)
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"Response from {result.get('agent')} agent:")
                    response_content = result.get("response")
                    if isinstance(response_content, dict):
                        response_type = response_content.get("type")
                        if response_type == "text":
                            st.write(response_content.get("message"))
                        elif response_type == "plot":
                            fig = pio.from_json(response_content.get("plot"))
                            st.plotly_chart(fig, use_container_width=True)
                            if "caption" in response_content:
                                st.caption(response_content["caption"])
                        else:
                            st.warning("Unexpected response type from the backend.")
                    else:
                        st.warning("Unexpected response format. Expected a dictionary from the backend.")

                else:
                    st.error(f"Error: {response.status_code} - {response.json().get('detail', 'Unknown error')}")

            except requests.exceptions.ConnectionError:
                st.error("Connection error. Is the FastAPI backend running and accessible?")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please enter a query.")
