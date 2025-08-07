# scout/core/agent.py
import os
import json
from utils.logger import logger
from colorama import Fore
from prompts import get_system_prompt, get_tools_json
from .caller import call_tool
from .llm import LLM, Summarizer, Reporter

class Agent:
    def __init__(self, llm: LLM, file: str, initial_data: bytes, keep_history: int = 10):
        self.llm = llm
        self.file = file
        self.keep_history = keep_history
        self.initial_data = initial_data
        
        initial_data_str = initial_data.decode('utf-8', errors='ignore')
        self.history = [
            {"role": "user", "content": f"Analyzing evidence file: {self.file}"},
            {"role": "user", "content": "File content snippet:\n" + initial_data_str[:500]}
        ]
        
        tools_json = get_tools_json()
        self.system_prompt = get_system_prompt(self.file, tools_json)

    def run(self) -> None:
        while True:
            messages = [{"role": "system", "content": self.system_prompt}]

            if len(self.history) > self.keep_history:
                summary = Summarizer(self.llm).summarize_conversation(self.history)
                self.history = self.history[-self.keep_history:]
                messages.extend([{"role": "system", "content": summary}])

            messages.extend(self.history)

            logger.info(f"{Fore.YELLOW}Waiting for LLM response...{Fore.RESET}")
            response_str = self.llm.action(messages, temperature=0.1)
            
            try:
                response_json = json.loads(response_str)
                reasoning = response_json.get("reasoning", "")
                tool_command = response_json.get("command", "")
                logger.info(f"{Fore.CYAN}LLM Reasoning: {reasoning}{Fore.RESET}")
            except json.JSONDecodeError:
                logger.error(f"{Fore.RED}Failed to decode LLM response as JSON: {response_str}{Fore.RESET}")
                reasoning = "No reasoning provided."
                tool_command = "" # Or handle error appropriately

            self.history.append({"role": "assistant", "content": response_str})

            if not tool_command or "analysis_complete" in tool_command:
                logger.info(f"{Fore.GREEN}Analysis complete, generating report.{Fore.RESET}")
                report = Reporter(self.llm, self.file)
                report.generate_summary_report(self.history)
                break
            
            tool_response = call_tool(tool_command)
            self.history.append({"role": "user", "content": str(tool_response)})
