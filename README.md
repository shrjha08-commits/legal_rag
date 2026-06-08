# PathLex: Agentic RAG with LLM Compiler Paradigm for Legal Tech

PathLex is an innovative, domain-specific Agentic RAG framework optimized for dense legal text processing (CUAD/AILA). By replacing standard sequential ReAct loops with an **LLM Compiler architecture**, PathLex extracts parallelizable execution dependency graphs, dropping latency by up to 50% on multi-source legal lookups.

## 🛠️ System Capabilities & Architecture
* **Structural Hierarchy Parsing:** Avoids naive token counting by chunking along nested contractual clauses (`ARTICLE`, `SECTION`).
* **Asynchronous Execution Planner:** Generates a Directed Acyclic Graph (DAG) to execute multiple tool tasks concurrently via `asyncio`.
* **Hybrid Storage Layer:** Unites vector proximity models (`all-MiniLM-L6-v2`) inside a high-speed Qdrant engine.

## 🚀 Quick Start
```bash
git clone [https://github.com/shrjha08-commits/legal_rag.git](https://github.com/shrjha08-commits/legal_rag.git)
cd legal_rag
python -m venv venv
source venv/bin/activate  # venv\Scripts\activate on Windows
pip install -r requirements.txt
python async_agent.py
