import json
from typing import Optional, List
from mcp.types import CallToolResult, Tool, TextContent
from mcp_client import MCPClient
from openai.types.chat.chat_completion import ChatCompletion


class ToolManager:
    @classmethod
    async def get_all_tools(cls, clients: dict[str, MCPClient]) -> list[Tool]:
        tools = []
        for client in clients.values():
            tool_models = await client.list_tools()
            tools += [
                {
                    "name": t.name,
                    "description": t.description,
                    "input_schema": t.inputSchema,
                }
                for t in tool_models
            ]
        return tools

    @classmethod
    async def _find_client_with_tool(
        cls, clients: list[MCPClient], tool_name: str
    ) -> Optional[MCPClient]:
        for client in clients:
            tools = await client.list_tools()
            tool = next((t for t in tools if t.name == tool_name), None)
            if tool:
                return client
        return None

    @classmethod
    async def execute_tool_requests(
        cls, clients: dict[str, MCPClient], message: ChatCompletion
    ) -> list[dict]:
        """Executes tool calls from an OpenAI/Ollama ChatCompletion response."""
        tool_calls = message.choices[0].message.tool_calls or []
        tool_result_messages = []

        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_use_id = tool_call.id

            try:
                tool_input = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                tool_input = {}

            client = await cls._find_client_with_tool(
                list(clients.values()), tool_name
            )

            if not client:
                tool_result_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_use_id,
                    "content": "Could not find that tool",
                })
                continue

            try:
                tool_output: CallToolResult | None = await client.call_tool(
                    tool_name, tool_input
                )
                content_list = []
                if tool_output:
                    content_list = [
                        item.text
                        for item in tool_output.content
                        if isinstance(item, TextContent)
                    ]
                result_content = json.dumps(content_list)

            except Exception as e:
                result_content = json.dumps({"error": str(e)})

            tool_result_messages.append({
                "role": "tool",
                "tool_call_id": tool_use_id,
                "content": result_content,
            })

        return tool_result_messages