# Enterprise Data Agent 專案詳解文檔

這份文檔詳細剖析了 `enterprise_data_agent` 專案中每個檔案的用途、使用的核心 AI 技術，以及底層的實作代碼與通訊協議。

---

## 1. 📂 目錄結構與核心功能 (Directory & Core Functions)

### `core/` (基礎建設層)
這裡存放所有 Agent 共用的基礎能力，相當於「人類的神經系統」。

| 檔案 | 核心功能 | 關鍵技術 |
| :--- | :--- | :--- |
| **`llm.py`** | **模型引擎**。封裝了 `transformers` 載入本地模型 (Qwen) 的邏輯，提供統一的 `generate()` 介面。 | **Inference** (推論), **Quantization** (4-bit 量化) |
| **`memory.py`** | **共享記憶體**。實作了一個類似 Redis 的 Log 系統，讓所有 Agent 可以讀寫同一個 Context。 | **Context Management** (上下文管理), **Persistence** (持久化) |
| **`base_agent.py`** | **Agent 基類**。定義了所有 Agent 的標準行為：接收 Input -> 讀取 Memory -> 呼叫 LLM -> 寫入 Memory。 | **OO Design** (物件導向), **Prompt Engineering** |

### `services/` (外部工具層)
這裡存放 Agent 可以使用的「手」與「感官」。

| 檔案 | 核心功能 | 關鍵技術 |
| :--- | :--- | :--- |
| **`mcp_client.py`** | **MCP 客戶端**。負責與外部的 `my_mcp_server.py` 進行標準化連線。 | **MCP** (Model Context Protocol), **Stdio Process** |
| **`python_sandbox.py`** | **Python 執行環境**。模擬一個安全的沙箱，讓 Agent 可以在裡面跑 Pandas 畫圖。 | **Tool Execution**, **Sandbox** (模擬) |

### `agents/` (職能角色層)
這裡定義了具體的「員工」，每個員工有不同的 Prompt 和可用的工具。

| 檔案 | 核心功能 | 關鍵技術 |
| :--- | :--- | :--- |
| **`sql_analyst.py`** | **SQL 專家**。負責將自然語言轉成 SQL 語法並查詢。 | **Text-to-SQL**, **MCP Tool Use** |
| **`data_scientist.py`** | **數據科學家**。負責寫 Python 程式碼分析數據。 | **Code Generation**, **Tool Calling** |
| **`orchestrator.py`** | **經理 (總指揮)**。負責判斷任務類型並分派給上述兩人。 | **A2A** (Agent-to-Agent), **Reasoning** |

---

## 2. 🛠️ 核心技術與實作代碼 (Core Technologies)

這裡深入解說三大關鍵技術在代碼中是如何實現的。

### (1) A2A (Agent-to-Agent Multiplexing)
**定義**：一個 Agent (Manager) 將任務轉發給另一個 Agent (Worker)。
**實作檔案**：`agents/orchestrator.py`

**代碼邏輯**：
Orchestrator 的 System Prompt 規定如果需要分派任務，必須輸出特定的 JSON。程式碼解析到 JSON 後，呼叫對應 Agent 的 `.process()` 方法。

```python
# agents/orchestrator.py

# 1. 解析 LLM 回傳的 JSON 指令
if "```json" in response:
    plan = json.loads(...)
    target = plan.get("delegate_to") # 讀取目標: "SQLAnalyst"

    # 2. 根據目標叫叫對應的 Agent (A2A)
    if target == "SQLAnalyst":
        # 呼叫 SQL Agent 處理，並等待結果
        result = await self.sql_agent.process(plan.get("message"))
```

### (2) MCP (Model Context Protocol)
**定義**：Agent 透過標準協議呼叫外部獨立運行的 Server 工具。
**實作檔案**：`agents/sql_analyst.py` & `services/mcp_client.py`

**代碼邏輯**：
SQL Analyst 決定呼叫工具後，透過 `MCPClientService` 建立一條通往 `my_mcp_server.py` 的管線。

```python
# agents/sql_analyst.py
if data["tool"] == "query_sales_db":
    # 呼叫 MCP Service
    result = await self.mcp.execute_tool("query_sales_db", data["parameters"])

# services/mcp_client.py
async def execute_tool(...):
    # 建立與 Server 的連線 (Stdio)
    async with stdio_client(self.server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 透過協議執行工具
            result = await session.call_tool(tool_name, arguments=arguments)
```

### (3) Tool Calling (Local Function Execution)
**定義**：Agent 輸出指令，由本地程式碼直接執行函式 (非 MCP 協議)。
**實作檔案**：`agents/data_scientist.py`

**代碼邏輯**：
Data Scientist 輸出身為 Python 程式碼的字串，我們使用 `exec()` 來執行它。

```python
# agents/data_scientist.py
if data["tool"] == "execute_python":
    code = data["parameters"]["code"]
    # 執行 Python 程式碼
    result = self.sandbox.execute(code)

# services/python_sandbox.py
def execute(self, code):
    # 使用 exec() 執行字串形式的代碼
    exec(code, safe_globals) 
```

---

## 3. 📝 JSON 通訊協議說明 (Protocol Specification)

為了讓 LLM 精準控制系統，我們定義了三種 JSON 格式，分別對應三種用途。

### Type A: 任務分派 (Delegation)
*   **使用者**: `OrchestratorAgent` (Manager)
*   **用途**: 將任務指派給屬下。

```json
{
  "delegate_to": "SQLAnalyst",     // 目標 Agent 名稱 (SQLAnalyst / DataScientist)
  "message": "Query total sales"   // 要傳給對方的話 (Prompt)
}
```
*   `delegate_to`: 路由的依據。
*   `message`: 這段文字會變成 Worker Agent 的 `input_text`。

### Type B: 工具呼叫 (Tool Call - SQL)
*   **使用者**: `SQLAnalystAgent`
*   **用途**: 執行 SQL 查詢。

```json
{
  "tool": "query_sales_db",        // 工具名稱 (必須對應 MCP Server 裡的定義)
  "parameters": {
    "sql_query": "SELECT * FROM sales_data"  // SQL 語句
  }
}
```

### Type C: 工具呼叫 (Tool Call - Code)
*   **使用者**: `DataScientistAgent`
*   **用途**: 執行 Python 分析。

```json
{
  "tool": "execute_python",        // 工具名稱
  "parameters": {
    "code": "print(df.describe())" // 要執行的 Python 完整程式碼
  }
}
```

---

## 4. 總結

這個專案展示了企業級 Agent 開發的三個層次：
1.  **Level 1 (Tool Integration)**: 使用 MCP 與 Sandbox 讓 AI 有手腳。
2.  **Level 2 (Protocol Design)**: 定義嚴謹的 JSON 格式讓 AI 穩定輸出。
3.  **Level 3 (Architecture)**: 使用 Manager-Worker 模式 (A2A) 處理複雜任務，而不是讓一個 Agent 什麼都做。
