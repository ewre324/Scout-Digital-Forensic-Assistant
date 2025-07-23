import os
from .agent import Agent
from utils.logger import logger
from colorama import Fore

class Scout:
    def __init__(self, evidence_file: str, max_iterations: int = 100, 
                 llm_model: str = "gpt-3.5-turbo", keep_history: int = 10):
        self.evidence_file = evidence_file
        self.max_iterations = max_iterations
        self.llm_model = llm_model
        self.keep_history = keep_history
        
        if not os.path.exists(evidence_file):
            raise FileNotFoundError(f"Evidence file not found: {evidence_file}")

        with open(self.evidence_file, 'r', errors='ignore') as f:
            self.file_contents = f.read()

    def run(self):
        """Run the analysis on the target evidence file."""
        agent = Agent(self.evidence_file, self.file_contents, llm_model=self.llm_model, keep_history=self.keep_history)
        logger.info(f"{Fore.WHITE}Starting evidence analysis...{Fore.RESET}")
        agent.run()
