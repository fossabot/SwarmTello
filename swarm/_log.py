"""
_log.py - sunnyqa233

A script to setup logger.
"""
import logging
import time
import os


# noinspection SpellCheckingInspection
def get_logger(name: str, log_folder: str = "logs", level: int = 30, unique: bool = False) -> logging.Logger:
    """
    Func to config logger.
    
    :param name: Name of the logger & name of the logfile.
    :param log_folder: Folder to save logfile.
    :param level: Min severe level to be logged. Ref: https://docs.python.org/3.9/library/logging.html#logging-levels
    :param unique: Use unique filename to prevent being overwrite.
    :return: Logger that being setup with given info.
    """
    # Create log folder if necessary
    if not os.path.isdir(log_folder):
        os.mkdir(log_folder)

    # Create file handler
    if unique:
        handler = logging.FileHandler(
            filename=f"{log_folder}/{name}-{time.time()}.log",
            mode="w",
            encoding="utf-8",
            errors="ignore"
        )
    else:
        handler = logging.FileHandler(
            filename=f"{log_folder}/{name}.log",
            mode="w",
            encoding="utf-8",
            errors="ignore"
        )

    # Define format of logfile
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
    )
    handler.setFormatter(formatter)

    # Setup logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
