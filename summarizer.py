# scout/summarizer.py
from llm import LLM
from typing import List, Dict

class Summarizer:
    def __init__(self, llm_model: str = "o3-mini") -> None:
        self.llm = LLM(llm_model)

    def summarize_conversation(self, conversation: List[Dict[str, str]]) -> str:
        conversation_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation])
        
        prompt = f"""
        You are a summarizer agent. Your job is to summarize the following conversation from a digital forensics investigation:

        {conversation_str}

        Please provide a bullet point summary that includes:
        - What evidence was examined
        - What tools were used
        - What the key findings were
        - Any hypotheses that were formed

        Keep the summary focused on the technical details and actions taken.
        """

        output = self.llm.prompt(prompt)
        return "To reduce context, here is a summary of the previous part of the conversation:\n" + output
