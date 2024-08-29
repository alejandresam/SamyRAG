import os
import streamlit as st
from create_database import generate_data_store  # Import generate_data_store function
#from query_data   # A refactored function from query_data.py
from file_converter import convert_pdf_to_markdown  # Implement this function for file conversion
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
import time

# Constants
DATA_PATH = "data/books"
CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

# Initialize global variables outside the main function for performance
embedding_function = OpenAIEmbeddings()
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

def save_uploaded_file(uploaded_file):
    """Saves the uploaded file to the data/books directory after converting to markdown chunks."""
    try:
        if uploaded_file is not None and uploaded_file.type == "application/pdf":
            # Convert PDF to Markdown chunks
            markdown_chunks = convert_pdf_to_markdown(uploaded_file)

            # Ensure the data directory exists
            os.makedirs(DATA_PATH, exist_ok=True)

            # Save each chunk as a separate markdown file
            for i, chunk in enumerate(markdown_chunks):
                filename = os.path.join(DATA_PATH, f"{uploaded_file.name.split('.')[0]}_chunk_{i}.md")
                
                # Open the file with UTF-8 encoding
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(chunk.page_content)  # Save the chunk's content as Markdown
            
            return f"Converted and saved {len(markdown_chunks)} chunks."

    except Exception as e:
        st.error(f"Failed to process the uploaded PDF: {e}")
    return None

def query_data(user_query):
    """Queries the database and generates a response using the user's query."""
    try:
        # Search the database for relevant documents
        results = db.similarity_search_with_relevance_scores(user_query, k=3)

        # Check if results are found and meet the relevance threshold
        if not results or results[0][1] < 0.7:
            st.warning("No relevant documents found or relevance is too low.")
            return None

        # Extract content for the prompt
        context = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context, question=user_query)

        # Use OpenAI Chat model to generate the response
        model = ChatOpenAI()
        response_text = model.predict(prompt)

        return response_text, [doc.metadata.get("source", "Unknown source") for doc, _ in results]
    except Exception as e:
        st.error(f"Error querying data: {e}")
        return None, None

def main():
    # Title and Introduction
    st.title("SafetyAi: Your Fleet Management Assistant")
    st.markdown("""
    Hello! My name is **SafetyAi**. I'm here to assist you with managing your fleet safely and efficiently. 
    Please upload any relevant fleet management documents (PDF format) like vehicle inspection reports, maintenance records, driver logs, and more.
    Once uploaded, you can ask me any questions regarding the documents or for guidance on fleet safety and management.
    """)

    # Upload Section
    st.header("📁 Upload Your Fleet Management Documents")
    uploaded_file = st.file_uploader("Upload a PDF document (e.g., vehicle inspection reports, maintenance records, etc.)", type=['pdf'])

    if uploaded_file:
        st.info("Processing your document, please wait...")
        save_path = save_uploaded_file(uploaded_file)
        if save_path:
            st.success(f"Document '{uploaded_file.name}' has been successfully uploaded and saved!")
            st.info("Updating the database with the new document...")
            with st.spinner('Regenerating the vector store with your documents...'):
                generate_data_store()  # Regenerate the vector store with new documents
                time.sleep(1)  # Simulate waiting time
            st.success("Database updated successfully! You can now ask questions related to your documents.")

    # Automated Greeting by SafetyAi
    st.header("💬 Chat with SafetyAi")
    st.write("Hi! I'm SafetyAi, your virtual assistant for fleet management. Please ask any questions you have about your fleet or your documents!")

    # User Input Section
    user_query = st.text_input("Enter your question:", "")

    if st.button("Ask SafetyAi"):
        if user_query:
            response_text, sources = query_data(user_query)
            if response_text:
                st.write("### 🤖 SafetyAi's Response")
                st.write(response_text)

                # Display sources
                st.write("### 📄 Relevant Documents or Sources")
                for source in sources:
                    st.write(f"- {source}")
            else:
                st.warning("I couldn't find any relevant information in the documents you provided. Please try asking something else.")
        else:
            st.warning("Please enter a question to ask SafetyAi.")

    # Footer with Additional Instructions
    st.markdown("""
    ---
    🔄 You can upload more documents or ask additional questions anytime. SafetyAi is here to help you with your fleet management needs!
    """)

if __name__ == "__main__":
    main()