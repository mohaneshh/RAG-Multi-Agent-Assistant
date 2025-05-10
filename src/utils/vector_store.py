import os
import logging
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, persist_directory="chroma_db"):
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Create the persist directory if it doesn't exist
        if not os.path.exists(persist_directory):
            os.makedirs(persist_directory)
        
        # Initialize the vector store
        if os.path.exists(persist_directory) and os.listdir(persist_directory):
            self.db = Chroma(
                persist_directory=persist_directory,
                embedding_function=self.embeddings
            )
        else:
            self.db = None
    
    def create_from_documents(self, documents):
        """
        Create a vector store from documents.
        """
        self.db = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        self.db.persist()
        logger.info(f"Vector store created with {len(documents)} documents")
        return self.db
    
    def retrieve(self, query, k=3):
        """
        Retrieve the top k most relevant documents for a query.
        """
        if not self.db:
            raise ValueError("Vector store is not initialized. Create it first with create_from_documents().")
        
        docs = self.db.similarity_search(query, k=k)
        return docs
    
    def refresh_index(self, data_dir="data"):
        """
        Refresh the vector store index to include new documents.
        
        Args:
            data_dir: Directory containing the documents
        """
        logger.info("Refreshing vector store index...")
        
        # Load documents
        documents = []
        for filename in os.listdir(data_dir):
            if filename.endswith('.txt') or filename.endswith('.md'):
                file_path = os.path.join(data_dir, filename)
                logger.info(f"Processing document: {file_path}")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        documents.append(Document(page_content=content, metadata={"source": filename}))
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {e}")
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)
        
        # Create a new vector store
        self.db = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        self.db.persist()
        
        logger.info(f"Vector store refreshed with {len(chunks)} chunks from {len(documents)} documents")
        return self.db