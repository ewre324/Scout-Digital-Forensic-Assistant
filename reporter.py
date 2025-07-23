# scout/reporter.py
import os
from llm import LLM
from pathlib import Path

class Reporter:
    def __init__(self, filename, llm_model: str = "o3-mini"):
        self.llm = LLM(llm_model)
        self.filename = filename
        
    def generate_summary_report(self, history):
        system_prompt = f"""
        You are a digital forensics report writer. Your task is to analyze the conversation history and create a detailed technical report about the evidence analysis.

        The report should include:
        1.  **Executive Summary**: A brief overview of the findings.
        2.  **Evidence Analyzed**: Details about the evidence file (`{self.filename}`).
        3.  **Analysis Walkthrough**: A step-by-step description of the tools used and the information discovered.
        4.  **Key Findings**: A list of the most important artifacts and their significance.
        5.  **Conclusion**: A summary of the investigation and any final hypotheses.

        Format the output as a proper markdown document.
        """

        system_prompt = [{"role": "system", "content": system_prompt}]
        messages = [{"role": item["role"], "content": item["content"]} for item in history]
        
        summary = self.llm.action(system_prompt + messages)
        
        base = os.path.splitext(os.path.basename(self.filename))[0]
        os.makedirs("results", exist_ok=True)
        report_path = f"results/{base}_forensic_report.md"
        
        with open(report_path, "w") as f:
            f.write(summary)
        
        print(f"Forensic report generated: {report_path}")
