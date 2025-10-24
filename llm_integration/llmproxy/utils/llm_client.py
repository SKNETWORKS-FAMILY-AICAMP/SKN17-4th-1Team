import os
import requests


class LLMClient:
    def __init__(self) -> None:
        self.base = os.getenv("LLM_API_BASE", "").rstrip("/")
        self.api_key = os.getenv("LLM_API_KEY", "")

    def is_configured(self) -> bool:
        return bool(self.base)

    def chat(self, messages: list[dict], attachments: list[dict] | None = None, max_tokens: int | None = 1024) -> dict:
        """
        Thin proxy to external LLM API. Expects a simple contract like:
          POST {base}/chat {headers: Authorization}
          body: { messages: [{role, content}], attachments?: [{type, url}] }
        Returns: { choices: [{ message: { role, content } }] }
        """
        if not self.is_configured():
            # Fallback mock for development
            reply = {
                "choices": [{"message": {"role": "assistant", "content": "LLM is not configured. This is a mock reply."}}]
            }
            return reply

        url = f"{self.base}/chat"
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        data = {"messages": messages, "max_tokens": max_tokens}
        if attachments:
            data["attachments"] = attachments

        resp = requests.post(url, json=data, headers=headers, timeout=60)
        resp.raise_for_status()
        return resp.json()
