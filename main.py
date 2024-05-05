import streamlit as st
import requests

# Define the API URL and authorization headers for text summarization model
API_URL = "https://api-inference.huggingface.co/models/Falconsai/text_summarization"
headers = {"Authorization": "Bearer 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"}

# Function to query the text summarization model with the provided text
def query_text_summarization_model(text):
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Function to extract and enhance notes from the inputted essay text
def extract_and_enhance_notes(essay_text):
    # Query the text summarization model to generate summary of essay
    summary_response = query_text_summarization_model(essay_text)
    if 'generated_text' in summary_response:
        summary = summary_response['generated_text']
        # Split the summary into sentences
        sentences = summary.split(". ")
        # Capitalize the first letter and add period at the end to ensure full sentence
        notes = [sentence.capitalize() + "." for sentence in sentences]
        return notes
    else:
        return []

# Streamlit UI
st.title("Essay Notes Extractor and Enhancer")

# Input text box for the essay
essay_text = st.text_area("Input Essay:", height=300)

# Button to trigger note extraction and enhancement
if st.button("Extract and Enhance Notes"):
    if essay_text:
        # Extract and enhance notes from the inputted essay text
        enhanced_notes = extract_and_enhance_notes(essay_text)
        # Display the enhanced notes
        st.subheader("Enhanced Notes:")
        for note in enhanced_notes:
            st.write(note)
    else:
        st.warning("Please input an essay first.")
