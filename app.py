import os
import time

import google.generativeai as genai
import streamlit as st

os.environ['GOOGLE_API_KEY'] = st.secrets['GOOGLE_API_KEY']
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Load Generative AI model
model = genai.GenerativeModel('gemini-pro')

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
            time.sleep(0.1)  # Adjust the delay between words here
        st.write(line_text)  # Print the remaining words in the line
        time.sleep(0.3) 

def main():
    st.title("Lawyer.AI")  # Updated title

    # Input prompt for user
    user_input = st.text_input("Enter your legal question:")

    if user_input:
        # Check if the input contains legal keywords
        if is_legal_topic(user_input):
            # Generate response using Generative AI model
            response = model.generate_content(user_input)
            st.write("Response:")
            type_line_by_line(response.text)  # Display response with line-by-line effect
        else:
            st.write("Please ask a legal question.")

def is_legal_topic(input_text):
    # Function to check if the input text contains legal keywords
    legal_keywords = ['legal',
 'Attorney'
,'Advocate'
,'Barrister'
,'Solicitor'
,'Counsel'
,'Jurist'
,'Lawyer'
,'Legal'
,'Litigator'
,'Paralegal'
,'Esquire'
,'Jurisprudence'
,'Litigation'
,'Counselor'
,'Legalize'
,'Defendant'
,'Plaintiff'
,'Prosecutor'
,'Defense'
,'Judge'
,'Court'
,'Law'
,'Legalize'
,'Contract'
,'Verdict'
,'Trial'
,'Brief'
,'Evidence'
,'Witness'
,'Testimony'
,'Deposition'
,'Appeal'
,'Settlement'
,'Arbitration'
,'Mediation'
,'Discovery'
,'Precedent'
,'Habeas Corpus'
,'Injunction'
,'Subpoena'
,'Pleading'
,'Complaint'
,'Indictment'
,'Affidavit'
,'Summons'
,'Cross-examination'
,'Objection'
,'Ruling'
,'Statute'
,'Constitution'
,'Legalize'
,'Contract'
,'Verdict'
,'Trial'
,'Brief'
,'Evidence'
,'Witness'
,'Testimony'
,'Deposition'
,'Appeal'
,'Settlement'
,'Arbitration'
,'Mediation'
,'Discovery'
,'Precedent'
,'Habeas Corpus'
,'Injunction'
,'Subpoena'
,'Pleading'
,'Complaint'
,'Indictment'
,'Affidavit'
,'Summons'
,'Cross-examination'
,'Objection'
,'Ruling'
,'Statute'
,'Constitution'
,'Legalize'
,'Contract'
,'Verdict'
,'Trial'
,'Brief'
,'Evidence'
,'Witness'
,'Testimony'
,'Deposition'
,'Appeal'
,'Settlement'
,'Arbitration'
,'Mediation'
,'Discovery'
,'Precedent'
,'Habeas Corpus'
,'Injunction'
,'Subpoena'
,'Pleading'
,'Complaint'
,'Indictment'
,'Affidavit']  # List of legal keywords
    for keyword in legal_keywords:
        if keyword.lower() in input_text.lower():
            return True
    return False

if __name__ == "__main__":
    main()
