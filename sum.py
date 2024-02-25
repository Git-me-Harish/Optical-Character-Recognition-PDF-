import streamlit as st
import pytesseract
from PIL import Image
from gensim.summarization import summarize

# Function to extract text from images using OCR
def extract_text_from_image(image):
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text

# Function to summarize text
def summarize_text(text, ratio=0.2):
    summary = summarize(text, ratio=ratio)
    return summary

# Main function for text summarization
def text_summarization():
    st.title("Text Summarization Tool")

    # Allow users to upload images or text files
    uploaded_file = st.file_uploader("Upload Image or Text File", type=["png", "jpg", "jpeg", "txt"])

    if uploaded_file:
        st.success("File uploaded successfully!")

        # Extract text from the uploaded file
        if uploaded_file.type.startswith('image'):
            # If the uploaded file is an image, extract text using OCR
            image = Image.open(uploaded_file)
            extracted_text = extract_text_from_image(image)
        else:
            # If the uploaded file is a text file, read the text
            extracted_text = uploaded_file.getvalue().decode("utf-8")

        # Display the extracted text
        st.subheader("Extracted Text:")
        st.text(extracted_text)

        # Summarize the extracted text
        summary_ratio = st.slider("Summary Ratio", min_value=0.1, max_value=1.0, step=0.05, value=0.2, format="%f")
        summary = summarize_text(extracted_text, ratio=summary_ratio)

        # Display the summary
        st.subheader("Summary:")
        st.text(summary)

# Main function to create Streamlit interface
def main():
    st.sidebar.title("Menu")
    menu_option = st.sidebar.radio(
        "Select Option",
        ["Text Summarization"]
    )

    if menu_option == "Text Summarization":
        text_summarization()

if __name__ == "__main__":
    main()
