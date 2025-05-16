import sys
import logging

def logger(name = "logger"):
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.addFilter(lambda log: log.levelno < logging.WARNING)
        stdout_handler.setFormatter(logging.Formatter("%(levelname)s\t%(message)s"))
        logger.addHandler(stdout_handler)
        
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.WARNING)
        stderr_handler.setFormatter(logging.Formatter("%(levelname)s\t%(message)s"))
        logger.addHandler(stderr_handler)
    
    return logger
