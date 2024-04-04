import PyPDF2

import os
import time

import google.generativeai as genai
import streamlit as st

# Authenticate with Google API Key (replace with your actual key)
os.environ['GOOGLE_API_KEY'] = 'YOUR_GOOGLE_API_KEY'
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Load Generative AI model
model = genai.GenerativeModel('gemini-pro')

def extract_text_from_pdf(pdf_file):
    """Extracts text from a PDF document."""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def type_line_by_line(message):
    """Simulates word-by-word printing effect without new lines."""
    lines = message.split('\n')
    for line in lines:
        words = line.split()
        word_count = 0
        line_text = ''
        for word in words:
            if word_count < 10:
                line_text += word + ' '
                word_count += 1
            else:
                st.write(line_text)  # Print the line with 10 words
                line_text = word + ' '  # Start a new line
                word_count = 1
        st.write(line_text)  # Print the remaining words in the line
        time.sleep(0.1)  # Adjust the delay between words here

def is_legal_topic(input_text):
    """Checks if input text contains legal keywords (can be improved with NLP)."""
    legal_keywords = [
        'legal', 'attorney', 'advocate', 'barrister', 'solicitor', 'counsel',
        'jurist', 'lawyer', 'litigator', 'paralegal', 'esquire', 'jurisprudence',
        'litigation', 'counselor', 'legalize', 'defendant', 'plaintiff',
        'prosecutor', 'defense', 'judge', 'court', 'law', 'legalize', 'contract',
        'verdict', 'trial', 'brief', 'evidence', 'witness', 'testimony',
        'deposition', 'appeal', 'settlement', 'arbitration', 'mediation',
        'discovery', 'precedent', 'habeas corpus', 'injunction', 'subpoena',
        'pleading', 'complaint', 'indictment', 'affidavit', 'summons',
        'cross-examination', 'objection', 'ruling', 'statute', 'constitution',
        # ... (add more relevant legal keywords)
    ]
    for keyword in legal_keywords:
        if keyword.lower() in input_text.lower():
            return True
    return False

def main():
    st.title("Lawyer.AI (Disclaimer: Informational purposes only, consult an attorney)")

    # Layout for Text Input and Generate Button
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Text Input")
        user_input = st.text_input("Enter your legal question:")

    with col2:
        generate_text_button = st.button("Generate from Text")

    # Layout for PDF Upload and Generate Button
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("PDF Upload")
        uploaded_file = st.file_uploader("Upload PDF document:", type="pdf")

    with col4:
        generate_pdf_button = st.button("Generate from PDF")

    # Stop processing if Terminate button is clicked
    if st.button("Terminate"):
        st.stop()

    # Text Input Processing
    if generate_text_button:
        if user_input:
            if is_legal_topic(user_input):
                try:
                    response = model.generate_content(user_input)
                    st.write("Response:")
                    type_line_by_line(response.text)
                except google.api_core.exceptions.InternalServerError:
                    st.error("Generative AI API encountered a temporary error. Please try again later.")
                #except google.api_core.exceptions.DeadlineExceeded:

    if generate_pdf_button:
        if uploaded_file is not None:
            if uploaded_file.name != '':  # Check for empty file
                if os.path.splitext(uploaded_file.name)[1].lower() == '.pdf':  # Check file extension
                    try:
                        extracted_text = extract_text_from_pdf(uploaded_file)
                        if extracted_text:
                            if is_legal_topic(extracted_text):
                                response = model.generate_content(extracted_text)
                                # ... rest of processing
                        else:
                            st.error("Failed to extract text from uploaded PDF. Please try again.")
                    except Exception as e:  # Catch generic exceptions
                        st.error(f"Error processing PDF: {e}")
                else:
                    st.error("Invalid file type. Please upload a PDF document.")


if __name__ == "__main__":
    main()
