# This script will contain the logic for logging.
import logging
import sys
from datetime import datetime
from pathlib import Path

# Color codes for pretty console output
COLORS = {
    "DEBUG": "\033[94m",   # Blue
    "INFO": "\033[92m",    # Green
    "WARNING": "\033[93m", # Yellow
    "ERROR": "\033[91m",   # Red
    "CRITICAL": "\033[95m" # Magenta
}
RESET = "\033[0m"

def setup_logger(name="guardian_logger", log_dir="logs", log_level=logging.INFO):
    """Set up both file and console logging with timestamps and colors."""
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_file = f"{log_dir}/guardian_{datetime.now().strftime('%Y%m%d')}.log"

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.handlers.clear()  # Avoid duplicate logs

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)

    # Formatter for file logs
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)

    # Formatter for console logs (color-coded)
    class ColorFormatter(logging.Formatter):
        def format(self, record):
            log_color = COLORS.get(record.levelname, "")
            message = super().format(record)
            return f"{log_color}{message}{RESET}"

    console_formatter = ColorFormatter("%(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.info("Logger initialized successfully.")
    return logger
