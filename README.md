# SafetyAi: Your Personal Knowledge Assistant for Fleet Management

SafetyAi is a prototype personal knowledge assistant designed to help users manage and retrieve information from their personal knowledge base using Large Language Models (LLM) and Retrieval-Augmented Generation (RAG) technology. This tool aims to enhance fleet management safety by providing insights and easy access to critical documents and information.

## 🎯 Objective

The goal is to create an intelligent assistant that uses state-of-the-art machine learning techniques to:
- Ingest and index fleet management documents.
- Retrieve relevant information efficiently.
- Generate insightful responses to user queries using LLM technology.

## ✨ Features

- **Document Ingestion**: Supports file `.pdf` formats.
- **Vector Database**: Efficiently stores and indexes documents using a vector database (`Chroma`).
- **Information Retrieval**: Fetches relevant documents based on user queries.
- **LLM-Powered Responses**: Combines retrieved information with language model-generated responses.
- **User-Friendly Chat Interface**: Web-based interface for easy interaction with SafetyAi.
- **Conversation History Management**: Maintains a record of user interactions.

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Virtual environment tool (e.g., `venv`, `conda`)
- API access to an LLM provider (e.g., OpenAI, Anthropic, Hugging Face)
- Required Python libraries (see `requirements.txt`)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone <your-repository-url>
   cd your-repository-name
   ```
2. **Set up the Virtual Environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```
3. **Install Required Packages**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up Environment Variables**
   - Create `.env` file in project root
   - Add your API keys for LLM service:
     ```bash
     OPENAI_API_KEY=your_openai_api_key
     ```
5. **Running the Application**
   To start application run:
   ```bash
   streamlit run app.py
   ```
## 🛠️ Usage Guide

### Uploading Documents

1. **Navigate to the Upload Section**:
   - Upload your fleet management documents (such as vehicle inspection reports, maintenance records, and driver logs) in PDF format.

2. **Supported Formats**:
   - `.pdf`

### Interacting with SafetyAi

1. **Initial Greeting**:
   - SafetyAi will greet you and offer to assist with your fleet management tasks.

2. **Ask Questions**:
   - Enter any question or request for information based on the uploaded documents (e.g., "Show me the latest vehicle inspection reports").

3. **View Responses and Sources**:
   - SafetyAi will generate a response based on the documents and display relevant sources.

## 🧩 System Architecture

### RAG System Implementation

- **Vector Database**:
  - Uses the `Chroma` vector database to store and index documents.
  - Provides efficient retrieval of relevant documents based on vector similarity.

- **Document Ingestion Pipeline**:
  - Supports PDF files.
  - Converts files to text, processes them into chunks, and stores them in the vector database.

### Chat Interface Development

- **Web-Based Interface**:
  - Developed using Streamlit for a user-friendly, interactive interface.
  - Handles document uploads, manages conversation history, and displays AI responses.

## 📂 Code Structure

- **`app.py`**: Main application file that sets up the web interface, handles user interactions, and integrates with the RAG system.
- **`create_database.py`**: Manages the ingestion and storage of documents in the vector database.
- **`query_data.py`**: Handles querying of the vector database and generating AI responses.
- **`utils.py`**: Contains utility functions for text cleansing and encoding handling.
- **`requirements.txt`**: Lists all Python dependencies.
- **`.env`**: Stores environment variables (e.g., API keys).

## 📊 Analysis

### Performance Evaluation

- **Retrieval Accuracy and Relevance**:
  - Evaluated using relevance scores from the vector database (e.g., similarity scores).
  - Future improvements may include fine-tuning embeddings or incorporating domain-specific knowledge.

- **LLM Response Quality**:
  - Quality assessed based on coherence, relevance, and completeness of the responses.
  - Potential for feedback loops to improve response accuracy.

## 🤝 Contributing

We welcome contributions to improve this project! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes and commit (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Open a pull request.

## ❓ FAQ and Troubleshooting

- **Issue**: `PermissionError: [WinError 32]`
  - **Solution**: Ensure no other processes are using the database file. Close any other instances of the app.

- **Issue**: `UnicodeDecodeError` during PDF processing.
  - **Solution**: Ensure your documents are UTF-8 encoded and use the utility functions provided for text cleansing.

## 🙏 Credits and Acknowledgments

- Built with Python, Streamlit, and LangChain.
- Uses OpenAI API for LLM integration.
- Inspired by best practices in fleet management and AI-driven knowledge assistants.




