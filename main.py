import streamlit as st
import requests
from nltk.tokenize import sent_tokenize
import nltk
import fitz

nltk.download('punkt')

API_URL = "https://api-inference.huggingface.co/models/Falconsai/text_summarization"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    response_json = response.json()
    if isinstance(response_json, list):
        if response_json:
            return response_json[0].get("summary_text", "")[:200]
        else:
            return "No summary available"
    else:
        return response_json.get("summary_text", "")[:200]

def get_summary(input_text):
    sentences = sent_tokenize(input_text)
    summarized_text = ""
    for sentence in sentences:
        summarized_sentence = query({"inputs": sentence.strip()})
        summarized_sentences = summarized_sentence.split('.')
        for s in summarized_sentences:
            if s.strip():
                summarized_text += "-" + s.strip() + ".\n"
    return summarized_text

def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        if uploaded_file.type == "application/pdf":
            pdf_content = uploaded_file.read()
            pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                text += page.get_text()
            pdf_document.close()
        else:
            st.error("Please upload a valid PDF file.")
    except Exception as e:
        st.error(f"Error occurred while extracting text from PDF: {str(e)}")
    return text

st.title("MUNI.AI")

st.markdown("""
### Instructions

1. Copy the text you want to get notes from or upload a PDF file.
2. Press the button to get notes.
3. Copy the output and enjoy easier note-taking.

*Note: If there is an error, refresh the page. If the issue still persists, contact 202210119@feualabang.edu.ph*
""")

background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://raw.githubusercontent.com/202210119/plop2/main/watermark.png");
    background-repeat: repeat;
    opacity: 0.5;
}
</style>
"""
st.markdown(background_image, unsafe_allow_html=True)

input_option = st.radio("Select input option:", ("Paste Text", "Upload PDF"))

if input_option == "Paste Text":
    input_text = st.text_area("Enter Text:", height=300)
elif input_option == "Upload PDF":
    uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])
    if uploaded_file is not None:
        input_text = extract_text_from_pdf(uploaded_file)

if st.button("Get Notes"):
    summary = get_summary(input_text)
    st.markdown(f"<div style='white-space: pre-line; user-select: none;'>{summary}</div>", unsafe_allow_html=True)
