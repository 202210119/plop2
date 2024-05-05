import streamlit as st
import requests

# Define the API URL and authorization headers for the summarizer model
API_URL = "https://api-inference.huggingface.co/models/Falconsai/text_summarization"
headers = {"Authorization": "Bearer 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"}

# Function to query the summarizer model with the provided text
def query_summarizer_model(text):
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Function to split the input text into sentences and summarize each
def split_and_summarize(text):
    # Split the input text into sentences
    sentences = text.split(". ")
    summaries = []
    # Summarize each sentence
    for sentence in sentences:
        summary_response = query_summarizer_model(sentence)
        if 'generated_text' in summary_response:
            summary = summary_response['generated_text']
            summaries.append(summary)
    return summaries

# Streamlit UI
st.title("Sentence Summarizer")

# Input text box for the essay
essay_text = st.text_area("Input Text:", height=300)

# Button to trigger sentence summarization
if st.button("Summarize Sentences"):
    if essay_text:
        # Split the input text into sentences and summarize each
        summaries = split_and_summarize(essay_text)
        # Display the summaries
        st.subheader("Summarized Sentences:")
        for summary in summaries:
            st.write(summary)
    else:
        st.warning("Please input some text first.")
