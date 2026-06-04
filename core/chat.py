from core.claude import Claude
from mcp_client import MCPClient
from core.tools import ToolManager


class Chat:
    def __init__(self, claude_service: Claude, clients: dict[str, MCPClient]):
        self.claude_service = claude_service
        self.clients = clients
        self.messages = []

    async def _process_query(self, query: str):
        self.messages.append({"role": "user", "content": query})

    async def run(self, query: str) -> str:
        await self._process_query(query)

        while True:
            response = self.claude_service.chat(
                messages=self.messages,
                tools=await ToolManager.get_all_tools(self.clients),
            )

            # Add assistant message (preserves tool_calls if any)
            self.claude_service.add_assistant_message(self.messages, response)

            finish_reason = response.choices[0].finish_reason

            if finish_reason == "tool_calls":
                # Print any text the model said before calling tools
                text = self.claude_service.text_from_message(response)
                if text:
                    print(text)

                # Execute tools and get result messages
                tool_result_messages = await ToolManager.execute_tool_requests(
                    self.clients, response
                )

                # Add each tool result as its own message
                self.messages.extend(tool_result_messages)

            else:
                # Final answer
                return self.claude_service.text_from_message(response)