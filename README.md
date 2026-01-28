# AI Agent 實作練習

### Repo 結構
```text
my-ai-agent-portfolio/
├── README.md                  
├── enterprise_data_agent/      # (主專案) 
│   ├── main.py
│   ├── ...
├── learning_modules/           # (練習過程) 
│   ├── practice_memory.py
│   ├── practice_tool_calling.py
│   ├── mcp_basic/              
└── docs/                       
    ├── architecture.md
    ├── devops_practices.md
```


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


