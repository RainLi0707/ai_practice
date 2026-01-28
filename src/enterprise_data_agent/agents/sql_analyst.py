from enterprise_data_agent.core.base_agent import BaseAgent
from enterprise_data_agent.services.mcp_client import MCPClientService

class SQLAnalystAgent(BaseAgent):
    def __init__(self, memory):
        super().__init__("SQLAnalyst", memory)
        self.mcp = MCPClientService()

    def get_system_prompt(self):
        return """You are an expert SQL Analyst.
Your goal is to translate natural language questions into SQL queries for the 'sales_data' table.
The schema is: sales_data (id, product_name, amount, date).

If you generate a SQL query, return it in a JSON block like this:
```json
{"tool": "query_sales_db", "parameters": {"sql_query": "SELECT * FROM..."}}
```
If you cannot answer, explain why.
"""

    async def process(self, input_text: str):
        # 1. Think & Generate SQL
        response = await super().process(input_text)
        
        # 2. Parse Tool Call
        if "```json" in response:
            import json
            try:
                clean_json = response.split("```json")[1].split("```")[0].strip()
                data = json.loads(clean_json)
                
                if data["tool"] == "query_sales_db":
                    # 3. Execute Tool via MCP
                    print(f"[SQLAnalyst] Executing SQL: {data['parameters']['sql_query']}")
                    result = await self.mcp.execute_tool("query_sales_db", data["parameters"])
                    
                    # 4. Return Data
                    summary = f"SQL Result:\n{result}"
                    self.memory.add_entry(self.name, "Orchestrator", summary, "data")
                    return summary
            except Exception as e:
                return f"Error parsing SQL tool: {e}"
        
        return response
