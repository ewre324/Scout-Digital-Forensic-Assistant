import subprocess
from utils.logger import logger
from colorama import Fore, Style

def call_tool(command: str) -> str:
    """
    Execute a shell command and return the output.
    """
    logger.info(f"{Fore.GREEN}Running command: {command}{Style.RESET_ALL}")
    try:
        # We use shell=True for convenience, but in a real-world scenario,
        # we would want to be much more careful about command injection.
        # For this educational tool, we'll accept the risk.
        result = subprocess.run(
            command,
            shell=True,
            text=True,
            capture_output=True,
            check=False
        )
        output = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        logger.info(f"{Fore.CYAN}Tool Output:\n{output}{Style.RESET_ALL}")
        return output
    except Exception as e:
        error_msg = f"Error running command: {command}\nError: {str(e)}"
        logger.error(f"{Fore.RED}{error_msg}{Style.RESET_ALL}")
        return error_msg
