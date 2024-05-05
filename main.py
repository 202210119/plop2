import streamlit as st
import requests
import subprocess
import nltk

# Function to download NLTK data
def download_nltk_data():
    subprocess.run(["python", "-m", "nltk.downloader", "punkt"])

# Download NLTK data (if not already downloaded)
download_nltk_data()

API_URL = "https://api-inference.huggingface.co/models/Falconsai/text_summarization"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    response_json = response.json()
    if isinstance(response_json, list):
        return response_json[0]["summary_text"]
    else:
        return response_json["summary_text"][:200]

def get_summary(input_text):
    sentences = nltk.sent_tokenize(input_text)
    summarized_text = ""
    for sentence in sentences:
        summarized_sentence = query({"inputs": sentence.strip()})
        summarized_sentences = summarized_sentence.split('.')
        for s in summarized_sentences:
            if s.strip():
                summarized_text += "-" + s.strip() + ".\n"
    return summarized_text

st.title("Text Summarizer")

input_text = st.text_area("Enter Text:", height=300)
if st.button("Summarize"):
    summary = get_summary(input_text)
    st.text_area("Summary:", value=summary, height=500)
