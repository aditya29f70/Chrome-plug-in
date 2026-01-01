# Built a Chrome Extension that helps users summarize content and extract key concepts from:

• YouTube videos
• Web browser page text

All directly from the browser using a Retrieval-Augmented Generation (RAG) pipeline.

# Tech Stack Used

-> Frontend
• HTML, JavaScript
• Chrome Extension APIs (Manifest V3)
-> Backend
• Flask (Python)
-> AI / LLM Stack
• LangChain
• LLM: HuggingFace – Qwen/Qwen2.5-1.5B-Instruct
• Embeddings: HuggingFace – BAAI/bge-small-en-v1.5

# RAG Indexing Pipeline

-> 1. Document Loaders
• YouTube: YouTubeTranscriptApi
• Web pages: WebBaseLoader
-> 2. Text Splitting
• RecursiveCharacterTextSplitter
-> 3. Vector Store
• FAISS for similarity search

• Implemented an end-to-end RAG workflow (load → split → embed → retrieve → generate)
• Integrated LangChain with a Chrome Extension frontend
• Built a clean separation between browser-based UI and Python backend
• Used open-source LLMs and embeddings instead of paid APIs
