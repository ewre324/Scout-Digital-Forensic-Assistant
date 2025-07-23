import logging
from colorama import Fore, Style, init

# Initialize colorama
init()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=f'{Fore.GREEN}%(asctime)s - %(name)s - %(levelname)s - {Style.RESET_ALL}%(message)s'
)
logger = logging.getLogger("Scout")
