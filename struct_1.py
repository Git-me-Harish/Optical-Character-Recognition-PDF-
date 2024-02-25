import streamlit as st
import fitz  # PyMuPDF for parsing PDF
import re  # Regular expressions for pattern matching
import spacy  # Advanced NLP library
from spacy.matcher import Matcher
from PyPDF2 import PdfWriter  # Corrected import statement
from io import BytesIO  # Required for handling file bytes
import os

# Function to analyze content and identify sections using NLP techniques
def analyze_content(text):
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)

    # Define patterns for section titles using NER and pattern matching
    patterns = [
        [{"ENT_TYPE": "ORG", "OP": "+"}],  # Organizations
        [{"ENT_TYPE": "PERSON", "OP": "+"}],  # Persons
        [{"ENT_TYPE": "LOC", "OP": "+"}]  # Locations
    ]
    matcher.add("SectionTitle", patterns)

    doc = nlp(text)
    matches = matcher(doc)
    sections = []
    section = []
    for match_id, start, end in matches:
        section.append(doc[start:end].text)
    if section:
        sections.append(section)

    return sections

# Function to create a template based on content analysis
def create_template(sections):
    template = {}
    for section in sections:
        if section:
            section_title = " ".join(section)
            template[section_title] = []
    return template

# Function to extract content from the PDF
def extract_content(uploaded_file):
    content = []
    with fitz.open(uploaded_file) as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            content.append(text)
    return content

# Function to organize content based on the template
def organize_content(content, template):
    organized_content = {section: [] for section in template.keys()}
    current_section = ""
    for line in content:
        for section_title in template.keys():
            if section_title in line:
                current_section = section_title
                break
        if current_section:
            organized_content[current_section].append(line)
    return organized_content

# Function to generate the structured PDF
def generate_structured_pdf(organized_content):
    structured_pdf_path = "structured.pdf"
    pdf_writer = PdfWriter()
    for section, lines in organized_content.items():
        pdf_writer.add_page()  # Add a new page for each section
        for line in lines:
            pdf_writer.addText(50, 50, line)  # Add text to the page
    with open(structured_pdf_path, "wb") as output_file:
        pdf_writer.write(output_file)  # Write the PDF to file
    return structured_pdf_path

# Main function for PDF Structuring
def pdf_structuring(uploaded_file):
    st.title("PDF Structuring Tool")

    # Extract content from the PDF
    content = extract_content(uploaded_file)

    # Analyze content and identify sections
    sections = []
    for page_text in content:
        sections.extend(analyze_content(page_text))

    # Create template based on content analysis
    template = create_template(sections)

    # Organize content based on the template
    organized_content = organize_content(content, template)

    # Generate the structured PDF
    structured_pdf_path = generate_structured_pdf(organized_content)

    # Provide download option for the structured PDF
    st.markdown(f"Download the structured PDF: [Structured PDF]({structured_pdf_path})")

# Main function to create Streamlit interface
def main():
    st.sidebar.title("Menu")
    menu_option = st.sidebar.radio(
        "Select Option",
        ["PDF Structuring"]
    )

    if menu_option == "PDF Structuring":
        uploaded_file = st.file_uploader("Upload Unordered PDF", type=["pdf"])
        if uploaded_file:
            pdf_structuring(uploaded_file)

if __name__ == "__main__":
    main()
