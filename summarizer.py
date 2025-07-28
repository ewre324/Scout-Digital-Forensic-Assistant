# scout/summarizer.py
from llm import LLM
from typing import List, Dict

class Summarizer:
    def __init__(self, llm_model: str = "o3-mini") -> None:
        self.llm = LLM(llm_model)

    def summarize_conversation(self, conversation: List[Dict[str, str]]) -> str:
        conversation_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation])
        
        prompt = f"""
        You are a summarizer agent for a digital forensics investigation. Your task is to summarize the following conversation, focusing on the key technical details and findings.

        **Conversation:**

        {conversation_str}

        **Summary Requirements:**

        * Provide a bullet-point summary.
        * Include details on the evidence examined, tools used, and key findings.
        * Mention any hypotheses that were formed or discarded.
        * Focus on the technical aspects of the analysis.
        """

        output = self.llm.prompt(prompt)
        return "To reduce context, here is a summary of the previous part of the conversation:\n" + output
