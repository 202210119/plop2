import tkinter as tk
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
def extract_notes():
    essay_text = essay_textbox.get("1.0", "end-1c")
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
    # Delete previous content in notes_textbox and insert the new notes
    notes_textbox.delete(1.0, tk.END)
    notes_textbox.insert(tk.END, notes_text)

# Create the main Tkinter window
root = tk.Tk()
root.title("Essay Notes Extractor")

# Create text box for inputting the essay
essay_label = tk.Label(root, text="Input Essay:")
essay_label.pack()
essay_textbox = tk.Text(root, height=10, width=50)
essay_textbox.pack()

# Create button to trigger note extraction
extract_button = tk.Button(root, text="Extract Notes", command=extract_notes)
extract_button.pack()

# Create text box for displaying the notes
notes_label = tk.Label(root, text="Extracted Notes:")
notes_label.pack()
notes_textbox = tk.Text(root, height=10, width=50)
notes_textbox.pack()

root.mainloop()
