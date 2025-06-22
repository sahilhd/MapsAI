# chatgpt_agent.py

import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import Optional

# Load environment variables from .env file
load_dotenv()

class ChatGPTAgent:
    """
    Wrapper for the OpenAI Python SDK ≥1.0.0, using the new chat.completions.create interface.
    """
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model

    def chat(self, prompt: str, temperature: float = 0.7, max_tokens: int = 512) -> str:
        """
        Send a user prompt to ChatGPT and return the assistant's response content.
        """
        resp = self.client.chat.completions.create(  # new method name :contentReference[oaicite:3]{index=3}
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user",   "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        # access via .choices[0].message.content
        return resp.choices[0].message.content.strip()  # same structure, just new client :contentReference[oaicite:4]{index=4}
