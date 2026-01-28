import json
import os
import time

class SharedMemory:
    """
    A Shared Memory system that acts like a 'Blackboard' for all agents.
    It persists conversation history and shared data (e.g. dataframes metadata).
    """
    def __init__(self, session_id="default"):
        self.session_id = session_id
        self.storage_dir = "memory_store"
        os.makedirs(self.storage_dir, exist_ok=True)
        self.history = []
        self.shared_context = {} # Dictionary to store variables (e.g. "last_sql_result")
        self.load()

    def add_entry(self, source_agent: str, target: str, content: str, entry_type="text"):
        """
        Record an interaction.
        source_agent: 'User', 'Orchestrator', 'SQLAgent', etc.
        target: 'Orchestrator', 'User', etc.
        """
        entry = {
            "timestamp": time.time(),
            "source": source_agent,
            "target": target,
            "type": entry_type, # 'text', 'tool_call', 'tool_result'
            "content": content
        }
        self.history.append(entry)
        self.save()

    def get_context_text(self, limit=10):
        """
        Convert history to a string format for LLM Prompting.
        Returns the last N turns.
        """
        context = ""
        for entry in self.history[-limit:]:
            context += f"[{entry['source']} -> {entry['target']}]: {entry['content']}\n"
        return context

    def set_shared_data(self, key, value):
        self.shared_context[key] = value
        self.save()

    def get_shared_data(self, key):
        return self.shared_context.get(key)

    def save(self):
        data = {
            "history": self.history,
            "shared_context": self.shared_context
        }
        with open(f"{self.storage_dir}/{self.session_id}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self):
        path = f"{self.storage_dir}/{self.session_id}.json"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.history = data.get("history", [])
                self.shared_context = data.get("shared_context", {})
