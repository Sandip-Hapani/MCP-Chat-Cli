from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion


class Claude:
    def __init__(self, model: str):
        self.client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
        )
        self.model = model

    def add_user_message(self, messages: list, message):
        # message can be a ChatCompletion or a raw string/list (tool results)
        if isinstance(message, ChatCompletion):
            messages.append({
                "role": "user",
                "content": message.choices[0].message.content or "",
            })
        else:
            # tool result parts passed as a list
            messages.append({"role": "user", "content": message})

    def add_assistant_message(self, messages: list, message):
        if isinstance(message, ChatCompletion):
            msg = message.choices[0].message
            assistant_message = {"role": "assistant", "content": msg.content or ""}
            # CRITICAL: preserve tool_calls so Ollama knows what was requested
            if msg.tool_calls:
                assistant_message["tool_calls"] = [
                    tc.model_dump() for tc in msg.tool_calls
                ]
            messages.append(assistant_message)
        else:
            messages.append({"role": "assistant", "content": message})

    def text_from_message(self, message: ChatCompletion):
        return message.choices[0].message.content or ""

    def chat(
        self,
        messages,
        system=None,
        temperature=1.0,
        stop_sequences=[],
        tools=None,
        thinking=False,
        thinking_budget=1024,
    ) -> ChatCompletion:
        all_messages = messages
        if system:
            all_messages = [{"role": "system", "content": system}] + messages

        params = {
            "model": self.model,
            "max_tokens": 8000,
            "messages": all_messages,
            "temperature": temperature,
        }

        if stop_sequences:
            params["stop"] = stop_sequences

        if tools:
            params["tools"] = [
                {
                    "type": "function",
                    "function": {
                        "name": t["name"],
                        "description": t.get("description", ""),
                        "parameters": t.get("input_schema", {}),
                    },
                }
                for t in tools
            ]

        return self.client.chat.completions.create(**params)