import streamlit as st
import spacy
from spacy.matcher import PhraseMatcher
from PyPDF2 import PdfReader

# Load spaCy English language model
nlp = spacy.load('en_core_web_sm')

# Function to extract relevant information from PDF documents based on user query
def get_pdf_response(query, uploaded_files):
    response = "I'm sorry, I couldn't find any relevant information."
    results = []

    # Process user query with spaCy
    query_doc = nlp(query.lower())

    # Initialize PhraseMatcher
    matcher = PhraseMatcher(nlp.vocab)

    # Add user query to PhraseMatcher
    matcher.add("QUERY", [query_doc])

    # Loop through each uploaded PDF document
    for uploaded_file in uploaded_files:
        with uploaded_file as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text = page.extract_text()
                # Process PDF text with spaCy
                doc = nlp(text.lower())
                matches = matcher(doc)
                # Extract matched sentences from PDF
                for match_id, start, end in matches:
                    match_sentence = doc[start:end].sent.text
                    results.append(f"From {uploaded_file.name}: \n{match_sentence}\n")
    if results:
        response = "\n\n".join(results)
    return response

# Main function for the PDF CHAT BOT page
def pdf_chat_bot_page():
    st.title("PDF CHAT BOT")

    # Allow users to upload PDF documents
    uploaded_files = st.file_uploader("Upload PDF documents", type=["pdf"], accept_multiple_files=True)

    # Allow users to input queries
    user_query = st.text_input("Ask a question about the PDF documents")

    # Process user query and provide response
    if st.button("Submit"):
        if uploaded_files and user_query:
            response = get_pdf_response(user_query, uploaded_files)
            st.success("Chatbot Response:")
            st.write(response)
        else:
            st.warning("Please upload PDF documents and enter a query.")

# Main function to create Streamlit interface
def main():
    st.sidebar.title("Menu")
    menu_option = st.sidebar.radio(
        "Select Option",
        ["PDF CHAT BOT"]
    )

    if menu_option == "PDF CHAT BOT":
        pdf_chat_bot_page()

if __name__ == "__main__":
    main()
