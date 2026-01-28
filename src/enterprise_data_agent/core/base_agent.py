from enterprise_data_agent.core.llm import LLMEngine
from enterprise_data_agent.core.memory import SharedMemory

class BaseAgent:
    def __init__(self, name: str, memory: SharedMemory):
        self.name = name
        self.memory = memory
        self.llm = LLMEngine()

    def get_system_prompt(self):
        return f"You are {self.name}."

    async def process(self, input_text: str) -> str:
        """
        Main entry point for the agent to do work.
        Should be overridden by subclasses or use generic logic.
        """
        prompt = self.get_system_prompt()
        context = self.memory.get_context_text()
        response = self.llm.generate(prompt, context, input_text)
        
        # Record thought
        self.memory.add_entry(self.name, "Self", f"Thought: {response}", "thought")
        
        return response
