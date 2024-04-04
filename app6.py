import PyPDF2
import streamlit as st
import nltk
from nltk.corpus import stopwords
import openai
import os
import time
import google.generativeai as genai

# Download NLTK resources (if not already downloaded)
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('averaged_perceptron_tagger')  # Added this line to download the required resource

# Set up OpenAI API key
openai.api_key = "your_openai_api_key"

# Set up Google Generative AI
os.environ['GOOGLE_API_KEY'] = st.secrets['GOOGLE_API_KEY']
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
    completion = openai.Completion.create(
        engine="davinci",
        prompt=user_question,
        max_tokens=150,
        temperature=0.7
    )
    return completion.choices[0].text.strip()

# Function to simulate word-by-word printing effect without new lines
def type_line_by_line(message):
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
        time.sleep(0.3)


def pdf_up():
  st.title("GPT Arena")
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
              response = model.generate_content(summary)
              
              st.write(summary)
              prompt = f"Given the summary of the legal content extracted from the PDF in ten lines:\n{summary}\nGenerate a response."
              response = model.generate_content(prompt)
              message = response.text
              words = message.split()
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
                  time.sleep(0.3) 
                      
                      
              if user_question:
                  st.write("Response:")
                  #chatbot_response = generate_chatbot_response(user_question)
                  response = model.generate_content(user_question)
                  # Display response
                  message = response.text
                  words = message.split()
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
                      time.sleep(0.3)
                  #st.write(response.text)
                  #st.write(chatbot_response)
              else:
                  st.warning("Please ask a question about the uploaded PDF.")
def main():
    st.title("Lawyer.AI")
    st.write("**Disclaimer:** This application's responses are for informational purposes only and do not constitute legal advice. Always consult with a licensed attorney for legal matters.")

    # Sidebar Navigation
    with st.sidebar:
        st.subheader("Navigation")
        st.text("Input")
        selected_option = st.selectbox("", ["Prompt Input", "PDF Upload"])

    # Layout for Inputs and Response
    col1, col2 = st.columns(2)

    with col1:
        if selected_option == "Prompt Input":
            st.subheader("Prompt Input")
            user_input = st.text_input("Enter your legal question:")
        elif selected_option == "PDF Upload":
            st.subheader("PDF Upload")
            #uploaded_file = st.file_uploader("Upload PDF document:", type="pdf")
            pdf_up()
            

    with col2:
        # Generate button can be placed outside or inside col2 based on preference
        generate_text_button = st.button("Generate")

    # Stop processing if Terminate button is clicked
    if st.button("Terminate"):
        st.stop()

    # Response Container (consider styling for separation)
    response_container = st.container()
    
    if generate_text_button:
        if selected_option == "Prompt Input":
            if user_input:  # Moved inside conditional block
                prompt = f"Given the user input, \n{user_input}\nGenerate a response only related to law."
                response = model.generate_content(user_input)
                with response_container:
                    st.write("Response:")
                    type_line_by_line(response.text)
            else:
                st.write("Please enter your legal question.")  # Handle missing input

        # PDF Processing
        if selected_option == "PDF Upload":
          pdf_up()
      

# Run the app
if __name__ == '__main__':
    main()
