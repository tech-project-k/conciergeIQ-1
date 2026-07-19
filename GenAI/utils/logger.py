# =====================================================================
# Why it exists:
# Standardizes logging outputs across all agents, services, and routers.
# Consistent logging is vital for auditing AI outputs and debugging.
#
# What it does:
# Configures a standardized Python Logger that prints logs to stdout with 
# timestamps, module source names, and severity levels.
#
# How it works:
# Uses standard Python `logging` module to bind stream handlers and formatting rules.
#
# How it integrates:
# Any module needing to print status updates imports `get_logger(name)` to log info, 
# warning, or error outputs.
# =====================================================================

import logging
import sys

def get_logger(name: str) -> logging.Logger:
    """
    Constructs and returns a configured logger instance with standard formats.
    
    Args:
        name (str): The name of the module generating the logger.
        
    Returns:
        logging.Logger: The configured Logger instance.
    """
    logger = logging.getLogger(name)
    
    # If the logger has handlers, don't re-configure to prevent duplicate logs.
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Format string: Year-Month-Day Hour:Minute:Second | Level | Name | Message
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Print logs to standard console output (stdout)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger
