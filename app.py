import os
import streamlit as st
from dotenv import load_dotenv
# Use absolute imports
from src.utils.data_ingestion import load_documents, chunk_documents
from src.utils.vector_store import VectorStore
from src.agents.rag_agent import RAGAgent

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Initialize vector store
@st.cache_resource
def initialize_vector_store():
    vector_store = VectorStore(persist_directory="chroma_db")
    
    # Check if the vector store already exists
    if not vector_store.db:
        # Load and process documents
        documents = load_documents("data")
        chunks = chunk_documents(documents)
        vector_store.create_from_documents(chunks)
    
    return vector_store

# Initialize agent
@st.cache_resource
def initialize_agent(_vector_store):
    return RAGAgent(_vector_store, api_key)

def main():
    st.title("RAG-Powered Multi-Agent Q&A Assistant")
    
    # Add sidebar with refresh button
    with st.sidebar:
        st.header("Document Management")
        if st.button("Refresh Document Index"):
            with st.spinner("Refreshing document index..."):
                # Get the vector store instance and refresh it
                vector_store = initialize_vector_store()
                vector_store.refresh_index(data_dir="data")
                st.success("Document index refreshed! New documents are now available.")
                # Force reinitialization of components
                st.cache_resource.clear()
                st.rerun()
    
    # Initialize components
    vector_store = initialize_vector_store()
    agent = initialize_agent(vector_store)
    
    # Add a key to the session state to track if we should clear the form
    if "clear_form" not in st.session_state:
        st.session_state.clear_form = False
    
    # User input with a conditional default value
    default_value = "" if st.session_state.clear_form else st.session_state.get("previous_query", "")
    query = st.text_input("Ask a question:", value=default_value)
    
    # Store the current query for next run
    if query:
        st.session_state.previous_query = query
    
    # Create two columns for Submit and Clear buttons
    col1, col2 = st.columns([4, 1])
    
    with col1:
        submit_button = st.button("Submit", use_container_width=True)
    
    with col2:
        clear_button = st.button("Clear", use_container_width=True)
    
    # Handle Clear button action
    if clear_button:
        # Set the clear flag and remove any previous results
        st.session_state.clear_form = True
        if "previous_query" in st.session_state:
            del st.session_state.previous_query
        if "result" in st.session_state:
            del st.session_state.result
        st.rerun()
    else:
        # Reset the clear flag
        st.session_state.clear_form = False
    
    # Handle Submit button action
    if submit_button and query:
        with st.spinner("Processing your query..."):
            result = agent.process_query(query)
            # Store the result in session state
            st.session_state.result = result
    
    # Display results if available
    if "result" in st.session_state and not st.session_state.clear_form:
        result = st.session_state.result
        st.subheader("Agent Decision")
        st.info(f"Used: {result['tool']}")
        
        if result['context']:
            with st.expander("Retrieved Context"):
                st.write(result['context'])
        
        st.subheader("Answer")
        st.write(result['answer'])

if __name__ == "__main__":
    main()