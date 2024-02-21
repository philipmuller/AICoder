from typing import Protocol, Optional
import openai
from dotenv import load_dotenv
import os
import requests

class AIEngine(Protocol):
    def send(self, message: str) -> str:
        ...


class OpenAIEngine:
    key: str
    system: str

    def __init__(self, api_key: Optional[str], system_prompt: Optional[str]) -> None:
        load_dotenv()
        self.key = api_key or os.getenv("OPENAI_KEY") or ""
        self.system = system_prompt or "You are a helpful assistant"

    def send(self, message: str) -> str:
        openai.api_key = self.key
        result = openai.ChatCompletion.create(model="gpt-4",
            messages=[
                {"role": "system", "content": self.system},
                {"role": "user", "content": message}
            ])
        content = result["choices"][0]["message"]["content"]
        print(f"CONTENT IS: {content}")
        return content

class OLlamaEngine:
    system: str

    def __init__(self, system_prompt: Optional[str]) -> None:
        self.system = system_prompt or "You are a helpful assistant"

    def send(self, message: str) -> str:
        result = requests.post(url='http://localhost:11434/api/generate',
            json={
                "model": "mistral",
                "stream": False,
                "prompt": message,
                "system": self.system
            }
        )
        print("ABOUT TO PRINT RESULT CONTENT")
        print(result.content)
        content = result.json()["response"]
        print(f"CONTENT IS: {content}")
        return content
