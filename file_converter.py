# In your conversion script (e.g., file_converter.py)

import pdfplumber
from markdown import markdown
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from utils import clean_text  # Import the utility function

def convert_pdf_to_markdown(uploaded_file):
    """
    Converts the uploaded PDF file to Markdown format and splits it into chunks.
    
    Args:
        uploaded_file: The PDF file uploaded by the user.
        
    Returns:
        A list of Markdown formatted chunks.
    """
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            extracted_text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    # Use the utility function to clean the text
                    extracted_text += clean_text(page_text) + "\n"

        # Convert the cleaned text to Markdown
        markdown_text = markdown(extracted_text)

        # Handle encoding issues
        markdown_text = markdown_text.encode('utf-8', 'ignore').decode('utf-8', 'ignore')

        # Split the text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=100,
            length_function=len,
            add_start_index=True,
        )

        # Wrap in Document object
        document = Document(page_content=markdown_text, metadata={"source": uploaded_file.name})

        # Split into chunks
        chunks = text_splitter.split_documents([document])

        return chunks

    except Exception as e:
        raise RuntimeError(f"Failed to convert PDF to Markdown: {e}")
