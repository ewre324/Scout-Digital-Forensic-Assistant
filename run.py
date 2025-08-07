import os
import argparse
from core.agent import Agent
from core.llm import LLM
from utils.logger import logger
from colorama import Fore, Style

def print_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                                                                      ║
    ║                          Scout - Digital Forensics Assistant         ║
    ║                                                                      ║
    ║                  Leveraging LLMs for Evidence Discovery              ║
    ║                                                                      ║
    ║     [+] Automated evidence processing and prioritization             ║
    ║     [+] Analysis of various file types (text, images, network)       ║
    ║     [+] Extensible with new analysis modules                         ║
    ║                                                                      ║
    ║                      -- Uncover evidence faster --                   ║
    ║                                                                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

class ScoutApp:
    def __init__(self, evidence_file: str, max_iterations: int = 100,
                 llm_model: str = "gpt-3.5-turbo", keep_history: int = 10):
        """
        Initialize the Scout digital forensics tool.
        
        Args:
            evidence_file: Path to the evidence file to analyze
            max_iterations: Maximum number of analysis iterations (default: 100)
            llm_model: LLM model to use for analysis (default: gpt-3.5-turbo)
            keep_history: Number of conversation items to maintain in context (default: 10)
        """
        self.evidence_file = evidence_file
        self.max_iterations = max_iterations
        self.llm = LLM(model=llm_model)
        self.keep_history = keep_history
        
        if not os.path.exists(evidence_file):
            raise FileNotFoundError(f"Evidence file not found: {evidence_file}")
            
        logger.info(f"Reading evidence file: {evidence_file}")
        with open(self.evidence_file, 'rb') as f:
            self.file_contents = f.read()

    def run(self):
        """Run the analysis on the target evidence file."""
        self.agent = Agent(
            llm=self.llm,
            file=self.evidence_file,
            initial_data=self.file_contents,
            keep_history=self.keep_history
        )
        logger.info(f"{Fore.WHITE}Starting evidence analysis...{Style.RESET_ALL}")
        self.agent.run()

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(
        description="Scout - A digital forensics tool leveraging LLMs",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--evidence_file", "-e",
        help="Path to the evidence file to analyze",
        required=True
    )
    
    parser.add_argument(
        "--max-iterations", "-m",
        type=int,
        help="Maximum number of analysis iterations",
        default=100
    )
    
    parser.add_argument(
        "--llm-model", "-l",
        help="LLM model to use for analysis",
        default="llama3"
    )

    parser.add_argument(
        "--keep-history", "-k", 
        type=int,
        help="Number of conversation history items to keep in context",
        default=14
    )

    args = parser.parse_args()

    if args.keep_history <= 10:
        logger.error("Keep history must be greater than 10")
        return 1

    if not os.path.exists(args.evidence_file):
        logger.error(f"File not found: {args.evidence_file}")
        return 1

    analyzer = ScoutApp(
            evidence_file=args.evidence_file,
            max_iterations=args.max_iterations,
            llm_model=args.llm_model,
            keep_history=args.keep_history
        )
    analyzer.run()

if __name__ == "__main__":
    main()
