# scout/llm.py
import ollama
from typing import Dict, List

class LLM:
    def __init__(self, model: str = "llama3"):
        """Initialize LLM with the specified Ollama model."""
        self.client = ollama
        self.model = model

    def action(self, messages: List[Dict[str, str]], temperature: float = 0.0) -> str:
        """
        Sends a chat request to the local Ollama model.
        """
        response = self.client.chat(
            model=self.model,
            messages=messages,
            options={
                "temperature": temperature
            }
        )
        return response['message']['content']

    def prompt(self, prompt: str, temperature: float = 0.0) -> str:
        """
        Sends a single prompt to the local Ollama model.
        """
        messages = [{"role": "user", "content": prompt}]
        response = self.client.chat(
            model=self.model,
            messages=messages,
            options={
                "temperature": temperature
            }
        )
        return response['message']['content']
