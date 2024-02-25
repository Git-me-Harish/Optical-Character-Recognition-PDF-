import streamlit as st
import fitz  # PyMuPDF for parsing PDF

# Function to extract headings from PDF document
def extract_headings(pdf_file):
    headings = []
    with fitz.open(pdf_file) as doc:
        for page in doc:
            output = page.get_text("blocks")
            previous_block_id = 0
            for block in output:
                if block[6] == 0:  # We only take the text
                    if previous_block_id != block[5]:  # Compare the block number
                        headings.append(block[4].strip())
                    previous_block_id = block[5]
    return headings

# Main function for PDF Heading Extraction
def pdf_heading_extraction():
    st.title("PDF Heading Extraction")

    # Allow users to upload PDF document
    uploaded_file = st.file_uploader("Upload PDF document", type=["pdf"])

    if uploaded_file:
        st.success("PDF uploaded successfully!")

        # Extract headings from PDF
        headings = extract_headings(uploaded_file)

        # Display extracted headings in dropdown menu
        if len(headings) > 0:
            selected_heading = st.selectbox("Select a heading:", headings)

            # Display selected heading content
            st.subheader("Content:")
            st.write(selected_heading)
        else:
            st.warning("No headings found in the uploaded PDF.")

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
