# from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
# from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import openai 
from dotenv import load_dotenv
import os
import shutil

# Load environment variables. Assumes that project contains .env file with API keys
load_dotenv()
#---- Set OpenAI API key 
# Change environment variable name from "OPENAI_API_KEY" to the name given in 
# your .env file.
openai.api_key = os.environ['OPENAI_API_KEY']

CHROMA_PATH = "chroma"
DATA_PATH = "data/books"


def main():
    generate_data_store()


def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    return documents


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[10]
    print(document.page_content)
    print(document.metadata)

    return chunks


def save_to_chroma(chunks):
    """
    Saves document chunks to Chroma vector store, clearing existing data first.
    
    Args:
        chunks: List of document chunks to save in the vector store.
    """
    # Clear out the database first. Ensure no processes are using the database.
    if os.path.exists(CHROMA_PATH):
        # Close any existing connections to the Chroma vector store
        try:
            db = Chroma(persist_directory=CHROMA_PATH, embedding_function=OpenAIEmbeddings())
            db.close()  # Explicitly close the database connection
        except Exception as e:
            print(f"Warning: Failed to close the database properly. {e}")

        # Attempt to remove the directory
        try:
            shutil.rmtree(CHROMA_PATH)
        except PermissionError as e:
            print(f"Error: Could not delete Chroma directory. {e}")
            return

    # Create a new DB from the documents
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )
    db.persist()  # Save changes to the database
    db.close()  # Ensure the database is closed after use
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

if __name__ == "__main__":
    main()
