import streamlit as st
import requests

# Define the API URL and authorization headers
API_URL = "https://api-inference.huggingface.co/models/deepset/tinyroberta-squad2"
headers = {"Authorization": "Bearer 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"}

# Function to query the model with a given question and context
def query_model(question, context):
    payload = {"inputs": {"question": question, "context": context}}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Function to extract notes from the inputted text
def extract_notes(essay_text):
    # Split essay into sentences
    sentences = essay_text.split(". ")
    notes = []
    for sentence in sentences:
        # Extract notes from each sentence using the model
        note = query_model("What is this sentence about?", sentence)
        # Check if 'answer' key exists in the response
        if 'answer' in note:
            note_text = note['answer']
            # Capitalize the first letter and add period at the end to ensure full sentence
            note_text = note_text.capitalize() + "."
            notes.append(note_text)
    # Join all the notes into a single string
    notes_text = "\n".join(notes)
    return notes_text

# Streamlit UI
st.title("Essay Notes Extractor")

# Input text box for the essay
essay_text = st.text_area("Input Essay:", height=300)

# Button to trigger note extraction
if st.button("Extract Notes"):
    if essay_text:
        # Extract notes from the inputted essay text
        extracted_notes = extract_notes(essay_text)
        # Display the extracted notes
        st.subheader("Extracted Notes:")
        st.write(extracted_notes)
    else:
        st.warning("Please input an essay first.")
