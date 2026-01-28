import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from enterprise_data_agent.config import MCP_SERVER_SCRIPT

class MCPClientService:
    def __init__(self):
        self.server_params = StdioServerParameters(
            command=sys.executable,
            args=[MCP_SERVER_SCRIPT], 
            env=None
        )

    async def execute_tool(self, tool_name: str, arguments: dict):
        """Connects to server, runs tool, returns result."""
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                try:
                    result = await session.call_tool(tool_name, arguments=arguments)
                    return result.content[0].text
                except Exception as e:
                    return f"MCP Error: {e}"
