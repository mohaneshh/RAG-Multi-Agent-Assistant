<<<<<<< HEAD
# RAG-Powered Multi-Agent Q&A Assistant

This project implements a simple "knowledge assistant" that retrieves relevant information from a document collection and generates natural-language answers using a Large Language Model (LLM).

## Architecture

The system consists of the following components:

1. **Data Ingestion**: Processes text and PDF documents, chunks them for better retrieval.
2. **Vector Store**: Uses Chroma DB with HuggingFace embeddings to store and retrieve document chunks.
3. **LLM Integration**: Uses Google's Gemini AI to generate responses.
4. **Agent Workflow**: Routes queries to appropriate tools based on keywords:
   - Calculator tool for mathematical queries
   - Dictionary tool for definition queries
   - RAG pipeline for knowledge-based queries
5. **User Interface**: Streamlit web interface for interacting with the assistant.

## Key Design Choices

- **Cost-Free Implementation**: Uses Google's Gemini AI instead of OpenAI to avoid API costs.
- **Local Vector Database**: Uses Chroma DB for local storage of vector embeddings.
- **HuggingFace Embeddings**: Uses the all-MiniLM-L6-v2 model for generating embeddings.
- **Simple Agent Routing**: Uses keyword detection to route queries to appropriate tools.
- **Logging**: Includes detailed logging for debugging and understanding the agent's decisions.

## How to Run

1. Clone the repository
2. Install dependencies:
=======
# RAG-Multi-Agent-Assistant
This project was developed as part of an internship assignment to create an intelligent question-answering system using Retrieval-Augmented Generation (RAG) and a multi-agent architecture. 
>>>>>>> 1591d23f015607e9b0ce48a07dc8496a746e0022
