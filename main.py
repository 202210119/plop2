import streamlit as st
import requests

# Define the API URL and authorization headers for GPT-2
API_URL = "https://api-inference.huggingface.co/models/openai-community/gpt2"
headers = {"Authorization": "Bearer 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"}

# Function to query the GPT-2 model with a given prompt
def query_gpt2_model(prompt):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Function to extract notes from the inputted text and enhance them using GPT-2
def extract_and_enhance_notes(essay_text):
    # Split essay into sentences
    sentences = essay_text.split(". ")
    print("Sentences:", sentences)  # Print sentences for debugging
    notes = []
    for sentence in sentences:
        # Enhance each sentence using GPT-2
        enhanced_sentence = query_gpt2_model(sentence)
        print("Enhanced sentence:", enhanced_sentence)  # Print enhanced sentence for debugging
        if 'generated_text' in enhanced_sentence:
            enhanced_note = enhanced_sentence['generated_text']
            notes.append(enhanced_note)
    # Return the enhanced notes
    return notes

# Streamlit UI
st.title("Essay Notes Extractor and Enhancer")

# Input text box for the essay
essay_text = st.text_area("Input Essay:", height=300)

# Button to trigger note extraction and enhancement
if st.button("Extract and Enhance Notes"):
    if essay_text:
        # Extract and enhance notes from the inputted essay text
        enhanced_notes = extract_and_enhance_notes(essay_text)
        print("Enhanced notes:", enhanced_notes)  # Print enhanced notes for debugging
        # Display the enhanced notes
        st.subheader("Enhanced Notes:")
        for note in enhanced_notes:
            st.write(note)
    else:
        st.warning("Please input an essay first.")
