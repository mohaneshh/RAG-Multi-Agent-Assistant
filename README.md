# RAG-Powered Multi-Agent Q&A Assistant 🤖📚

An intelligent question-answering system built using **Retrieval-Augmented Generation (RAG)** and a **multi-agent architecture**. This project was developed as part of an internship assignment to showcase capabilities in document intelligence, tool use, and LLM integration.

---

## 🚀 Project Overview

The assistant is capable of:
- Answering questions based on document content
- Performing calculations (math queries)
- Providing word definitions
- Dynamically processing newly added documents

---

## ⚙️ Quick Start Guide

### 🔒 Prerequisites
- Python 3.8 or higher
- Google API key (for Gemini AI access)

---

### 📥 Installation

1. **Clone the repository**
```bash
git clone https://github.com/mohaneshh/RAG-Multi-Agent-Assistant.git
cd RAG-Multi-Agent-Assistant
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Add your Google API key**
Create a .env file in the root directory and add your key:
```bash
GOOGLE_API_KEY=your_google_api_key_here
```

▶️ Running the Application
Start the Streamlit app:
```bash
streamlit run app.py
```

Then open your browser at:
```bash
http://localhost:8501
```

💬 How to Use
Type your question in the input field.
Click Submit to get an answer.
Use Clear to reset the chat.
Add .txt files to the data/ directory to expand the system's knowledge.
Click "Refresh Document Index" in the sidebar to load new content.


**❓ Example Questions:**

"What are the applications of quantum computing?"

"Calculate 3456 * 789"

"Define artificial intelligence"


**🧠 System Architecture:**

1. Data Ingestion

Reads .txt files
Splits content into chunks using LangChain


2. Vector Store

Uses ChromaDB with HuggingFace embeddings for semantic search


3. Multi-Agent System

RAG Agent: Answers content-based queries using Gemini
Calculator Agent: Solves math expressions
Dictionary Agent: Provides definitions


4. User Interface

Built using Streamlit for easy interaction


**🛠 Troubleshooting**

New documents not searchable? → Click Refresh Document Index in the sidebar.

Invalid API key? → Ensure your .env file is correct and the key is active.

Wrong file format? → Use only .txt files for ingestion.


**📄 License**
This project is open-sourced under the MIT License.

**🙋‍♂️ Author**
Mohanesh R


Sample input and output:
![Screenshot (99)](https://github.com/user-attachments/assets/ef9eec03-6aae-45ef-a0fe-57af1531d4ac)


Add new doc (.txt file) in the **data** folder then click on Refresh Document Index Button to ask questions on the new document.
