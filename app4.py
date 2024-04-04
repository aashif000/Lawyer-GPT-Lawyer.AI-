import PyPDF2
import streamlit as st
import nltk
from nltk.corpus import stopwords
import google.generativeai as genai
import os

# Download NLTK resources (if not already downloaded)
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('averaged_perceptron_tagger')  # Added this line to download the required resource

# Set up Google API key
os.environ['GOOGLE_API_KEY'] = "your_google_api_key"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Load Generative AI model
model = genai.GenerativeModel('gemini-pro')

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return None

# Function to summarize legal content of PDF
def summarize_legal_pdf(text):
    stop_words = set(stopwords.words('english'))
    sentences = nltk.sent_tokenize(text)
    named_entities = []
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        words = [word for word in words if word.lower() not in stop_words and word.isalnum()]
        tagged_words = nltk.pos_tag(words)
        named_entities.extend(nltk.ne_chunk(tagged_words))
    
    legal_info = []
    for entity in named_entities:
        if isinstance(entity, nltk.tree.Tree):
            if entity.label() == 'ORGANIZATION' or entity.label() == 'GPE' or entity.label() == 'DATE':
                legal_info.append(' '.join([leaf[0] for leaf in entity]))
    
    summary_sentences = []
    for sentence in sentences:
        if any(info in sentence for info in legal_info):
            summary_sentences.append(sentence)
    
    summary = " ".join(summary_sentences)[:200]
    return summary

# Function to generate chatbot response
def generate_chatbot_response(user_question):
    response = model.generate_content(user_question)
    return response.text.strip()

# Main function
def main():
    st.title("Legal Document Chatbot")
    st.header("(Disclaimer: Informational purposes only. Consult a lawyer for legal matters.)")

    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    if uploaded_file is not None:
        st.write("File uploaded successfully!")
        st.write("Ask your question about the uploaded PDF:")
        user_question = st.text_input("")

        if st.button("Generate Answer"):
            extracted_text = extract_text_from_pdf(uploaded_file)
            if extracted_text:
                summary = summarize_legal_pdf(extracted_text)
                st.write(f"**Summary of the legal content:**")
                st.write(summary)

                if user_question:
                    st.write("Chatbot Response:")
                    chatbot_response = generate_chatbot_response(user_question)
                    st.write(chatbot_response)
                else:
                    st.warning("Please ask a question about the uploaded PDF.")

# Run the app
if __name__ == '__main__':
    main()
