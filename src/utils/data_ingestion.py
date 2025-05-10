import os
from langchain.schema import Document  # Add this import
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_documents(data_dir):
    """
    Load documents from a directory.
    """
    documents = []
    for filename in os.listdir(data_dir):
        if filename.endswith('.txt') or filename.endswith('.md'):
            file_path = os.path.join(data_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                documents.append(Document(page_content=content, metadata={"source": filename}))
    
    return documents

def chunk_documents(documents, chunk_size=1000, chunk_overlap=200):
    """
    Split documents into chunks for better processing.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    
    chunks = text_splitter.split_documents(documents)
    return chunks