from enterprise_data_agent.core.base_agent import BaseAgent
from enterprise_data_agent.services.python_sandbox import PythonSandboxService

class DataScientistAgent(BaseAgent):
    def __init__(self, memory):
        super().__init__("DataScientist", memory)
        self.sandbox = PythonSandboxService()

    def get_system_prompt(self):
        return """You are a Python Data Scientist.
Your goal is to write pandas/matplotlib code to analyze data.
You have access to a variable 'df' if data was previously queried.

If you generate code, return it in a JSON block like this:
```json
{"tool": "execute_python", "parameters": {"code": "print('hello')"}}
```
"""

    async def process(self, input_text: str):
        response = await super().process(input_text)
        
        if "```json" in response:
            import json
            try:
                clean_json = response.split("```json")[1].split("```")[0].strip()
                data = json.loads(clean_json)
                
                if data["tool"] == "execute_python":
                    code = data["parameters"]["code"]
                    print(f"[DataScientist] Running Code...\n{code}")
                    result = self.sandbox.execute(code)
                    
                    self.memory.add_entry(self.name, "Orchestrator", result, "result")
                    return result
            except Exception as e:
                return f"Error parsing Python tool: {e}"
                
        return response
