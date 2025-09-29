from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import asyncio
import os
import sys


class MCPClient:
    def __init__(self):
        # Create server parameters for stdio connection
        # Ensure we run the server with the same Python interpreter / venv
        # Use the working example server from 01-first-server/solution/python/server.py
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        server_script = os.path.abspath(
            os.path.join(base_dir, "server", "calc_server.py")
        )
        print(f"Using server script at: {server_script}")

        self.server_params = StdioServerParameters(
            command=sys.executable,  # Use the same python interpreter that's running this client
            args=[server_script],  # Absolute path to server script
            env=None,  # Optional environment variables
        )

    async def run(self):
        try:
            async with stdio_client(self.server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    # Initialize the connection
                    await session.initialize()

                    # List available resources
                    resources = await session.list_resources()
                    print("LISTING RESOURCES")
                    for resource in resources:
                        print("Resource: ", resource)

                    # List available resources templates
                    resource_templates = await session.list_resource_templates()
                    print("LISTING RESOURCE TEMPLATES")
                    for template in resource_templates:
                        print("Template: ", template)

                    # List available tools
                    tools = await session.list_tools()
                    print("LISTING TOOLS")
                    for tool in tools.tools:
                        print("Tool: ", tool.name)

                    # Read a resource
                    print("READING RESOURCE")
                    content, mime_type = await session.read_resource("greeting://hello")
                    print(f"Content: {content}, MIME Type: {mime_type}")

                    # Call a tool
                    print("CALL TOOL")
                    result = await session.call_tool("add", arguments={"a": 1, "b": 7})
                    print(result.content)

        except Exception as e:
            import traceback

            print(f"❌ Error running MCP client: {e}")
            traceback.print_exc()
            raise


async def main():
    client = MCPClient()
    await client.run()


if __name__ == "__main__":
    asyncio.run(main())
