import streamlit as st
import fitz  # PyMuPDF for parsing PDF
import os
from docx import Document

# Function to extract main headings and their content from PDF document
def extract_headings_and_content(pdf_file):
    main_headings = []
    headings_content = {}
    with fitz.open(pdf_file) as doc:
        for page in doc:
            output = page.get_text("blocks")
            previous_block_id = 0
            heading = ""
            content = ""
            for block in output:
                if block[6] == 0:  # We only take the text
                    if previous_block_id != block[5]:  # Compare the block number
                        if heading:  # If heading is not empty, store previous heading and content
                            main_headings.append(heading)
                            headings_content[heading] = content.strip()
                        heading = block[4].strip()
                        content = ""  # Initialize content with an empty string
                    else:
                        content += block[4].strip() + "\n"  # Append text to content
                    previous_block_id = block[5]
            # Store last heading and content pair
            if heading:
                main_headings.append(heading)
                headings_content[heading] = content.strip()
    return main_headings, headings_content

# Function to download content as a Word document
def download_word_document(content, filename):
    doc = Document()
    doc.add_paragraph(content)
    doc.save(filename)

# Main function for PDF Heading Extraction
def pdf_heading_extraction():
    st.title("PDF Heading Extraction")

    # Allow users to upload PDF document
    uploaded_file = st.file_uploader("Upload PDF document", type=["pdf"])

    if uploaded_file:
        st.success("PDF uploaded successfully!")

        # Extract main headings and their content from PDF
        temp_file_path = "temp_uploaded_file.pdf"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(uploaded_file.getbuffer())

        main_headings, headings_content = extract_headings_and_content(temp_file_path)

        # Display extracted main headings in dropdown menu
        if len(main_headings) > 0:
            selected_heading = st.selectbox("Select a main heading:", main_headings)

            # Display content of selected heading
            st.subheader(f"Content under '{selected_heading}':")
            st.write(headings_content[selected_heading])

            # Download button for Word document
            st.markdown("<hr>", unsafe_allow_html=True)
            st.subheader("Download")
            st.write("Click the button below to download:")
            st.download_button(f"Download Content as Word (docx)", headings_content[selected_heading], f"{selected_heading}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

        else:
            st.warning("No main headings found in the uploaded PDF.")

        # Remove temporary file
        os.remove(temp_file_path)

# Main function to create Streamlit interface
def main():
    st.set_page_config(page_title="PDF Heading Extraction", page_icon=":notebook:", layout="wide")

    st.sidebar.title("Menu")
    menu_option = st.sidebar.radio(
        "Select Option",
        ["PDF Heading Extraction"]
    )

    if menu_option == "PDF Heading Extraction":
        pdf_heading_extraction()

if __name__ == "__main__":
    main()
