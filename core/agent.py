# scout/core/agent.py
import os
from utils.logger import logger
from colorama import Fore
from prompts.system import SYSTEM_PROMPT
from prompts.tooluse import TOOLUSE_PROMPT
from .caller import Caller
from llm import LLM
from summarizer import Summarizer
from reporter import Reporter

class Agent:
    def __init__(self, file: str, initial_data: bytes, llm_model: str = "o3-mini", keep_history: int = 10):
        self.llm = LLM(llm_model)
        self.file = file
        self.llm_model = llm_model
        self.keep_history = keep_history
        self.initial_data = initial_data
        
        # Decode the initial data for the prompt
        initial_data_str = initial_data.decode('utf-8', errors='ignore')

        self.history = [
            {"role": "user", "content": f"Analyzing evidence file: {self.file}"},
            {"role": "user", "content": "File content snippet:\n" + initial_data_str[:500]}
        ]
        self.SYSTEM_PROMPT = SYSTEM_PROMPT.format(file=self.file)
        
    def tool_use(self, response: str) -> str:
        response = self.llm.prompt(TOOLUSE_PROMPT.format(
            response=response,
            file=self.file
        ))
        return response.strip('```')

    def run(self) -> None:
        while True:
            messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]

            if len(self.history) > self.keep_history:
                keep_beginning = 4
                keep_ending = self.keep_history - keep_beginning
                
                first_messages = self.history[:keep_beginning]
                last_messages = self.history[-keep_ending:]
                middle_messages = self.history[keep_beginning:-keep_ending]
                summary = Summarizer(self.llm_model).summarize_conversation(middle_messages)
                self.history = first_messages + [
                    {"role": "assistant", "content": f"[SUMMARY OF PREVIOUS CONVERSATION: {summary}]"}
                ] + last_messages
                
                messages.extend(self.history)
            else:
                messages.extend(self.history)

            logger.info(f"{Fore.YELLOW}Waiting for LLM response...{Fore.RESET}")
            response = self.llm.action(messages, temperature=0.3)
            logger.info(f"{Fore.CYAN}LLM Response: {response}{Fore.RESET}")
            self.history.append({"role": "assistant", "content": response})
            
            tool_command = self.tool_use(response)

            if "analysis_complete" in tool_command:
                logger.info(f"{Fore.GREEN}Analysis complete, generating report.{Fore.RESET}")
                report = Reporter(self.file, self.llm_model)
                report.generate_summary_report(self.history)
                raise SystemExit(0)
            
            tool_response = Caller(file=self.file, llm_model=self.llm_model).call_tool(tool_command)
            self.history.append({"role": "user", "content": str(tool_response)})
