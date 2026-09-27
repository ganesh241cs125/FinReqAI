import json
from typing import Any
from ..config import OPENAI_API_KEY, OPENAI_MODEL

class LLMService:
    def __init__(self):
        self.enabled = bool(OPENAI_API_KEY)
        self.client = None
        if self.enabled:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=OPENAI_API_KEY)
            except Exception:
                self.enabled = False

    def json(self, system: str, user: str, fallback: Any):
        if not self.enabled or self.client is None:
            return fallback
        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                temperature=0.1,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            return json.loads(response.choices[0].message.content)
        except Exception:
            return fallback

    def text(self, system: str, user: str, fallback: str):
        if not self.enabled or self.client is None:
            return fallback
        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                temperature=0.2,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            return response.choices[0].message.content
        except Exception:
            return fallback
