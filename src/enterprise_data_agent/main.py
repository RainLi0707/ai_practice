import asyncio
import sys
import os

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from enterprise_data_agent.core.memory import SharedMemory
from enterprise_data_agent.agents.orchestrator import OrchestratorAgent

async def main():
    print("=== Enterprise Data Scientist Agent Framework (EDSAF) ===")
    session_id = input("Enter Session ID (e.g. 'ProjectX'): ").strip() or "test"
    
    # Init Shared Infrastructure
    memory = SharedMemory(session_id)
    manager = OrchestratorAgent(memory)
    
    print(f"\n[System] Session '{session_id}' loaded.")
    print("[System] The Team is ready: Manager, SQLAnalyst, DataScientist.")
    
    while True:
        try:
            task = input("\n[User] Assign Task (or 'exit'): ")
            if task.lower() in ["exit", "quit"]:
                break
                
            print(f"\n--- Starting Mission: {task} ---")
            result = await manager.run_mission(task)
            print(f"\n[System] Mission Complete.\n{result}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
