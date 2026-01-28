# AI Agent 實作練習

### 📂 Repository Structure & Practice Items (專案結構與練習重點)
This repository is organized to demonstrate Enterprise AI patterns. Below is the detailed breakdown of each file and the concept it practices.
#### `src/enterprise_data_agent/` (Core Framework)
**🧠 Core Layer (核心基礎)**
*   **`core/base_agent.py`**
    *   *Practice*: **Abstract Base Class in AI**.
    *   *Concept*: Defines the standard `think` -> `act` loop used by all agents.
*   **`core/memory.py`**
    *   *Practice*: **Context Management & Persistence**.
    *   *Concept*: Implements a shared state store (like Redis) so agents can share data context without re-prompting.
*   **`core/llm.py`**
    *   *Practice*: **High-Performance Inference**.
    *   *Concept*: Qwen-VL-Instruct integration with **4-bit quantization (BitsAndBytes)** for efficient local execution.
**🤖 Agents Layer (多智能體協作)**
*   **`agents/orchestrator.py`**
    *   *Practice*: **A2A (Agent-to-Agent) & Router Pattern**.
    *   *Concept*: The "Manager" that parses natural language and delegates tasks via JSON protocols.
*   **`agents/sql_analyst.py`**
    *   *Practice*: **MCP Tool Use & Text-to-SQL**.
    *   *Concept*: An agent specialized in converting questions to SQL and executing them via MCP.
*   **`agents/data_scientist.py`**
    *   *Practice*: **Code Interpreter & Tool Calling**.
    *   *Concept*: An agent that writes and executes Python code for data analysis.
**🔌 Services Layer (外部整合)**
*   **`services/mcp_client.py`**
    *   *Practice*: **Model Context Protocol (MCP) Client**.
    *   *Concept*: Implements the standard protocol to connect with external tools (Servers).
*   **`services/python_sandbox.py`**
    *   *Practice*: **Sandboxed Execution**.
    *   *Concept*: Simulates a secure environment for AI-generated code execution.
#### `src/tools/` (External Tools)
*   **`tools/my_mcp_server.py`**
    *   *Practice*: **MCP Server Implementation**.
    *   *Concept*: A standard MCP server exposing SQL capabilities to the agents.



### Enterprise Multi-Agent Data Framework

#### 🚀 Project Overview (專案簡介)
A modular **Multi-Agent System** designed to automate enterprise data analysis tasks. It features a **Hub-and-Spoke architecture** where an Orchestrator coordinates specialized agents (SQL Analyst & Data Scientist) to answer complex business questions.

#### ✨ Key Features (核心亮點)
*   **Multi-Agent Orchestration**: Implemented **A2A (Agent-to-Agent)** communication using JSON protocols to delegate tasks between Manager and Workers.
*   **MCP Integration**: utilizing **Model Context Protocol (MCP)** to securely connect LLMs with local databases.
*   **Python Sandbox**: Integrated a local code execution environment for real-time data visualization.
*   **Shared Memory**: Implemented a persistent context store (Redis-style) for maintaining state across agent interactions.

#### 🛠️ Tech Stack (技術棧)
*   **Core**: Python 3.10, Transformers (Qwen-VL-Instruct)
*   **Agentic Patterns**: ReAct, Tool Calling, Router Pattern
*   **Protocols**: MCP (Model Context Protocol)
*   **Data**: Pandas, SQLite, FAISS (RAG)



#### 💻 How to Run (如何執行)
```bash
python enterprise_data_agent/main.py
```

---


