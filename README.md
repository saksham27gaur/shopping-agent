This project is an Autonomous Shopping Assistant that leverages Agentic AI principles to deliver intelligent and explainable product recommendations.

🔹 Key Features:
Agentic Workflow: Implements a structured decision pipeline inspired by Thought–Action–Observation loops
RAG-based Semantic Search: Uses embeddings with FAISS to retrieve contextually relevant products
Hybrid Intelligence: Combines deterministic filtering (budget/category) with LLM-based reasoning
Local LLM Integration: Uses Ollama for privacy-friendly, cost-free inference
Dynamic Query Handling: Supports natural language queries like “best phone under 10000 for students”
Interactive UI: Built with Streamlit for real-time interaction
🔹 Architecture:

User Query → Intent Extraction → Vector Search (RAG) → Filtering & Ranking → LLM Reasoning → Response

🔹 Tech Stack:
Python, FastAPI
FAISS (Vector DB)
Ollama (LLM inference)
Streamlit (UI)
Docker (containerization)

This project demonstrates practical implementation of Agentic AI systems.
