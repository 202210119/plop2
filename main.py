
You sent
import streamlit as st
import requests
from nltk.tokenize import sent_tokenize
import nltk

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

st.title("MUNI.AI")

st.markdown("""
### Instructions

1. Copy the text you want to get notes from.
2. Press the button to get notes.
3. Copy the output and enjoy easier note-taking.

*Note:* If it gives an error, refresh the page. If the issue still persists, contact 202210119@feualabang.edu.ph.
""")

input_text = st.text_area("Enter Text:", height=300)
if st.button("Get Notes"):
    summary = get_summary(input_text)
    st.text_area("Notes:", value=summary, height=500)
