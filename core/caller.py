import os
import subprocess
from utils.logger import logger
from colorama import Fore, Style
from typing import Dict, Optional, Any

def sanitize_command(command: str) -> str:
    # Basic sanitization
    return command

class Caller:
    def __init__(self, file: str, llm_model: str = "o3-mini") -> None:
        self.file = file
        self.llm_model = llm_model

    def call_tool(self, tool_call_command: str) -> Any:
        logger.info(f"{Fore.GREEN}Running tool: {tool_call_command} {self.file}{Style.RESET_ALL}")

        def file_tool(command: str) -> str:
            """
            Run a command related to file analysis.
            Example: file_tool("strings") to run strings on the file.
            """
            try:
                # A more robust implementation would have a map of file tools
                if command == "strings":
                    output = subprocess.run(["strings", self.file], capture_output=True, text=True)
                    return f"Output of 'strings' on {self.file}:\n{output.stdout}"
                else:
                    return f"Unknown file tool command: {command}"
            except Exception as e:
                return f"Error running file tool: {e}"
        
        def bash_shell(command: str) -> str:
            """Execute a shell command."""
            cmd = sanitize_command(command)
            try:
                output = subprocess.run(cmd, shell=True, text=True, capture_output=True, check=False)
                return f"STDOUT:\n{output.stdout}\nSTDERR:\n{output.stderr}"
            except Exception as e:
                return f"Error running command: {str(e)}"

        def analysis_complete() -> None:
            """Signal that the analysis is complete."""
            exit()

        local_ns = {
            "file_tool": file_tool,
            "bash_shell": bash_shell,
            "analysis_complete": analysis_complete
        }

        try:
            tool_response = eval(tool_call_command, {}, local_ns)
            logger.info(f"{Fore.CYAN}Tool Response: {tool_response}{Style.RESET_ALL}")
            return tool_response
        except Exception as e:
            error_msg = f"Error executing tool command: {tool_call_command}\nType: {type(e).__name__}\nDetails: {str(e)}"
            logger.error(f"{Fore.RED} {error_msg}{Style.RESET_ALL}")
            return error_msg
