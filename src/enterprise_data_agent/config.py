# Global Configuration

# LLM Settings
MODEL_ID = "Qwen/Qwen3-VL-8B-Instruct"
USE_4BIT = True
MAX_NEW_TOKENS = 512

# Paths
MEMORY_DIR = "memory_store"
OUTPUT_DIR = "outputs" # Where charts/csvs will be saved

import os

# Dynamic Path Resolution
# config.py is in src/enterprise_data_agent/config.py
# We want src/tools/my_mcp_server.py
current_dir = os.path.dirname(os.path.abspath(__file__)) # .../src/enterprise_data_agent
src_dir = os.path.dirname(current_dir) # .../src
MCP_SERVER_SCRIPT = os.path.join(src_dir, "tools", "my_mcp_server.py") 
