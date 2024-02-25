import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
import os

# Function to create a PDF from text input and images
def create_pdf_from_text_and_images(text_input, image_files, output_file):
    c = canvas.Canvas(output_file, pagesize=letter)

    # Add text input to PDF
    c.drawString(100, 750, "Text Input:")
    c.drawString(100, 730, text_input)

    # Add images to PDF
    y_offset = 700
    for image_file in image_files:
        image = Image.open(image_file)
        width, height = image.size
        aspect_ratio = height / width
        image_width = 300
        image_height = int(image_width * aspect_ratio)
        c.drawImage(image_file, 100, y_offset - image_height, width=image_width, height=image_height)
        y_offset -= (image_height + 20)  # Adjust vertical position for next image

    c.save()

# Main function for creating PDF
def main():
    st.title("Create PDF from Text Input and Images")

    # Text input
    text_input = st.text_area("Enter your text here:")

    # Image input
    st.write("Upload your images:")
    uploaded_files = st.file_uploader("Upload images", accept_multiple_files=True)

    # Button to generate PDF
    if st.button("Generate PDF"):
        if text_input.strip() != "":
            image_files = []
            for uploaded_file in uploaded_files:
                with open(uploaded_file.name, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                image_files.append(uploaded_file.name)
            output_file = "text_and_images_pdf.pdf"
            create_pdf_from_text_and_images(text_input, image_files, output_file)
            st.success("PDF generated successfully!")
            st.markdown(get_binary_file_downloader_html(output_file, 'PDF'), unsafe_allow_html=True)
            for image_file in image_files:
                os.remove(image_file)  # Remove temporary image files
        else:
            st.warning("Please enter some text before generating the PDF.")

# Function to generate a direct download link for files
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = data.encode('latin-1', errors='ignore')
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{bin_file}">{file_label}</a>'
    return href

if __name__ == "__main__":
    main()
