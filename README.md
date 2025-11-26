# 🟦 Regency RAG: Local AI Engineering Assistant

Regency is a locally-hosted Retrieval Augmented Generation (RAG) system designed for offline engineering research. It allows users to query technical PDF documentation using natural language, leveraging the Llama 3 LLM on consumer hardware.

## ⚡ Architecture

* **Engine:** Llama 3 (8B Quantized) via Ollama
* **Vector Store:** ChromaDB (Persistent local embeddings)
* **Ingestion:** PyPDF crawler with custom chunking logic
* **Interface:** Streamlit (Dark Mode GUI)
* **Synthesis:** Top-K (k=3) Multi-Source Context Injection

## 🛠️ Installation

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/YourUsername/regency-rag.git](https://github.com/YourUsername/regency-rag.git)
    cd regency-rag
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Knowledge Base**
    * Create a folder named `knowledge_base`
    * Drop your PDF technical manuals/textbooks inside.

4.  **Ingest Data**
    ```bash
    python ingest_v2.py
    ```

5.  **Launch Control Center**
    ```bash
    python -m streamlit run app.py
    ```

## 🚀 Features

* **Privacy-First:** 100% offline execution. No data leaves the local machine.
* **Source Citations:** Every answer cites the specific PDF filename and page context.
* **Hardware Optimized:** Designed to run efficiently on 12GB VRAM.

---
*Built by Ahmad Qatanani 
