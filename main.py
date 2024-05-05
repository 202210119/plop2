import streamlit as st
import requests
from transformers import pipeline

# Initialize the pipeline for text summarization
summarization_pipeline = pipeline("summarization", model="t5-small", tokenizer="t5-small")

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
    # Tokenize the input text into sentences using Transformers tokenizer
    sentences = summarization_pipeline(input_text, max_length=512, truncation=True)
    summarized_text = ""
    for sentence in sentences:
        summarized_sentence = query({"inputs": sentence["summary_text"].strip()})
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
