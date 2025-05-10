import re
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
# Change relative imports to absolute imports
from src.tools.calculator import calculator_tool
from src.tools.dictionary import dictionary_tool

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RAGAgent:
    def __init__(self, vector_store, api_key):
        self.vector_store = vector_store
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",  # Updated to use Gemini 2.0 Flash
            google_api_key=api_key,
            temperature=0.2
        )
    
    def _should_use_calculator(self, query):
        """Check if the query requires calculation."""
        # Check for comparison questions about plans or features first
        if re.search(r'\bdifference between\b.*\bplan\b', query.lower()):
            logger.info("Not routing to calculator - detected plan comparison question")
            return False
            
        calculator_keywords = ["calculate", "compute", "sum", 
                              "divide", "multiply", "add", "subtract", "plus", "minus",
                              "total", "monthly cost"]
        # Removed potentially ambiguous terms: "difference", "cost", "price"
        
        query_lower = query.lower()
        
        # Check for explicit calculation requests
        for keyword in calculator_keywords:
            if re.search(r'\b' + keyword + r'\b', query_lower):
                logger.info(f"Routing to calculator tool based on keyword: {keyword}")
                return True
        
        # Check for mathematical expressions with operators
        if re.search(r'\b\d+\s*[\+\-\*/]\s*\d+\b', query_lower):
            logger.info("Routing to calculator tool based on mathematical expression")
            return True
        
        # Check for specific calculation patterns
        if re.search(r'\b\d+\s+employees\b', query_lower) and re.search(r'\bcost\b|\bprice\b|\bplan\b', query_lower):
            logger.info("Routing to calculator tool based on quantity and cost/price pattern")
            return True
        
        # Check for "difference" only in numerical contexts
        if re.search(r'\bdifference\b', query_lower) and re.search(r'\b\d+\b.*\b\d+\b', query_lower):
            logger.info("Routing to calculator tool based on 'difference' with multiple numbers")
            return True
                
        return False
    
    def _should_use_dictionary(self, query):
        """Check if the query is asking for a definition."""
        dictionary_keywords = ["define", "definition", "meaning", "what is", "what does", "what's"]
        
        query_lower = query.lower()
        for keyword in dictionary_keywords:
            if keyword in query_lower:
                logger.info(f"Routing to dictionary tool based on keyword: {keyword}")
                return True
                
        return False
    
    def process_query(self, query):
        """
        Process a user query and return the appropriate response.
        """
        logger.info(f"Processing query: {query}")
        
        # Determine which tool to use
        if self._should_use_calculator(query):
            logger.info("Using calculator tool")
            return {
                "tool": "Calculator",
                "context": None,
                "answer": calculator_tool(query)
            }
        
        elif self._should_use_dictionary(query):
            logger.info("Using dictionary tool")
            return {
                "tool": "Dictionary",
                "context": None,
                "answer": dictionary_tool(query)
            }
        
        else:
            logger.info("Using RAG pipeline")
            # Retrieve relevant documents
            docs = self.vector_store.retrieve(query)
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Generate a more detailed prompt for LLM to encourage elaboration
            prompt = f"""
            You are a helpful AI assistant for a company. Answer the following question based on the provided context.
            Elaborate on the information and provide a comprehensive, natural-sounding response.
            If the context doesn't contain relevant information, say that you don't have enough information to answer accurately.
            
            Context:
            {context}
            
            Question: {query}
            
            Please provide a detailed, helpful response that goes beyond just repeating the information in the context.
            Explain implications, benefits, or additional relevant details when appropriate.
            """
            
            # Get response from LLM
            response = self.llm.invoke(prompt)
            
            return {
                "tool": "RAG Pipeline",
                "context": context,
                "answer": response.content
            }