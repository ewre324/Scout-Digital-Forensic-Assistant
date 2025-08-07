# scout/core/llm.py
import ollama
from typing import Dict, List
import os
from tabulate import tabulate
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

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

class Summarizer:
    def __init__(self, llm: LLM) -> None:
        self.llm = llm

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

        messages = [{"role": "user", "content": prompt}]
        output = self.llm.action(messages)
        return "To reduce context, here is a summary of the previous part of the conversation:\n" + output

class Reporter:
    def __init__(self, llm: LLM, filename):
        self.llm = llm
        self.filename = filename
        
    def generate_summary_report(self, history, ground_truth=None, predictions=None):
        system_prompt = f"""
        You are a digital forensics report writer. Your task is to analyze the conversation history and create a detailed technical report about the evidence analysis.

        The report should include:
        1.  **Executive Summary**: A brief overview of the findings.
        2.  **Evidence Analyzed**: Details about the evidence file (`{self.filename}`).
        3.  **Analysis Walkthrough**: A step-by-step description of the tools used and the information discovered.
        4.  **Key Findings**: A list of the most important artifacts and their significance.
        5.  **Quantitative Analysis**: A summary of the model's performance metrics.
        6.  **Conclusion**: A summary of the investigation and any final hypotheses.

        Format the output as a proper markdown document.
        """

        system_prompt = [{"role": "system", "content": system_prompt}]
        messages = [{"role": item["role"], "content": item["content"]} for item in history]
        
        summary = self.llm.action(system_prompt + messages)
        
        if ground_truth and predictions:
            precision = precision_score(ground_truth, predictions)
            recall = recall_score(ground_truth, predictions)
            f1 = f1_score(ground_truth, predictions)

            performance_data = [
                ["Precision", f"{precision:.2f}"],
                ["Recall", f"{recall:.2f}"],
                ["F1-Score", f"{f1:.2f}"]
            ]
            performance_table = tabulate(performance_data, headers=["Metric", "Score"], tablefmt="pipe")

            summary += f"\n\n## Quantitative Analysis\n\n{performance_table}"

        base = os.path.splitext(os.path.basename(self.filename))[0]
        os.makedirs("results", exist_ok=True)
        report_path = f"results/{base}_forensic_report.md"
        
        with open(report_path, "w") as f:
            f.write(summary)
        
        print(f"Forensic report generated: {report_path}")
