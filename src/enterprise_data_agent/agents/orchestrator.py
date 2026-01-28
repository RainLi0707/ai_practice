from enterprise_data_agent.core.base_agent import BaseAgent
from enterprise_data_agent.agents.sql_analyst import SQLAnalystAgent
from enterprise_data_agent.agents.data_scientist import DataScientistAgent

class OrchestratorAgent(BaseAgent):
    def __init__(self, memory):
        super().__init__("Orchestrator", memory)
        # Initialize Sub-Agents
        self.sql_agent = SQLAnalystAgent(memory)
        self.ds_agent = DataScientistAgent(memory)

    def get_system_prompt(self):
        return """You are the Manager of a Data Team.
You have two workers:
1. SQLAnalyst: Can query database.
2. DataScientist: Can write Python code to analyze/plot.

Your job is to break down the user request.
- If it involves getting data -> Delegate to SQLAnalyst.
- If it involves analyzing/plotting data -> Delegate to DataScientist.

Reply with JSON to delegate:
```json
{"delegate_to": "SQLAnalyst", "message": "Query total sales..."}
```
Or reply with text to answer the user directly.
"""

    async def run_mission(self, user_objective):
        self.memory.add_entry("User", self.name, user_objective)
        print(f"\n[Manager] Received Mission: {user_objective}")
        
        # 1. Plan / Delegate
        # In a real loop, this would run multiple times. Simplified for demo.
        response = await self.process(user_objective)
        
        if "```json" in response:
            import json
            try:
                clean = response.split("```json")[1].split("```")[0].strip()
                plan = json.loads(clean)
                
                target = plan.get("delegate_to")
                msg = plan.get("message")
                
                if target == "SQLAnalyst":
                    print(f"[Manager] Delegating to SQLAnalyst: {msg}")
                    result = await self.sql_agent.process(msg)
                    # For simple demo, we pass result to DS automatically if needed
                    # In real world, Manager decides again.
                    return f"Mission Result: {result}"
                    
                elif target == "DataScientist":
                    print(f"[Manager] Delegating to DataScientist: {msg}")
                    result = await self.ds_agent.process(msg)
                    return f"Mission Result: {result}"
                    
            except Exception as e:
                print(f"Planning Error: {e}")
        
        return response
