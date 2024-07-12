"""
Funcs module.
"""
# Standard Library Imports
from logging import FileHandler, Formatter, Handler, INFO, Logger, StreamHandler, getLogger
from os import getcwd, mkdir, path
from pathlib import Path
from sys import stdout
from typing import Dict, List

# Local Imports
from . import SuppressedLoggerAdapter
from .formatters import ColourCodedFormatter
from .handlers import DatabaseLogHandler
from ..config import Config

# Used for storing what loggers have been created to prevent duplicate request handlers
createdLoggers: Dict[str, bool] = {}


def createLogger(
        name: str,
        level: int = INFO,
        formatString: str = "[%(asctime)s] [%(loggername)s] [%(levelname)s] %(message)s",
        handlers: List[Handler] = None,
        doColour: bool = True,
        colourCoding: Dict[str, str] = None,
        doDb: bool = True,
        includeRequest: bool = False,
        config: Config = None
) -> SuppressedLoggerAdapter:
    """
    Creates a logger with the specified name, logging path, level, and formatter.

    Args:
        name (str): The name of the logger.
        level (str): The level of the logger.
        formatString (str): The format string for the logger.
        handlers (List): Additional handlers for the logger.
        doColour (bool): Whether to use colour coding in the logger for logging outputs.
        colourCoding (Dict): The colour coding for the logger. Defaults to the default colour coding defined in the
            function.
        doDb (bool): Whether to log to a database.
        includeRequest (bool): Whether to include the request information in the log.
        config (Config): The config object to use.

    Returns:
        logger (Logger): The logger object.
    """
    if not path.exists(Path(f"{getcwd()}/Logs/")):
        mkdir(Path(f"{getcwd()}/Logs/"))

    loggingDirectory: str = name
    logFileName: str = name + "_"

    if includeRequest and True in createdLoggers.values():
        includeRequest = False

    if doDb and config is None:
        raise ValueError("Config object must be provided if logging to a database.")

    # Check if the logging directory exists, if not, create it
    if not path.exists(Path(f"{getcwd()}/Logs/{loggingDirectory}")):
        mkdir(Path(f"{getcwd()}/Logs/{loggingDirectory}"))

    logger: Logger = getLogger(name)  # Sets the logger's name
    logger.setLevel(level)  # Sets the logger's level

    if logger.hasHandlers():  # This checks if the logger has already been created and if it has, it replaces the
        # handlers with the new ones
        logger.handlers.clear()

    if handlers is None:
        handlers: list[Handler] = []

    if "file" in config.logging.handlers:
        handlers.append(
            FileHandler(
                Path(
                    f"{getcwd()}/Logs/{loggingDirectory}/{logFileName}.log"
                ),
                encoding="utf-8",
            )
        )

    if "console" in config.logging.handlers:
        handlers.append(StreamHandler(stdout))

    if "db" in config.logging.handlers:
        handler: DatabaseLogHandler = DatabaseLogHandler(config)
        handler.includeRequest = includeRequest
        handlers.append(handler)

    colourFormatter: ColourCodedFormatter = ColourCodedFormatter(formatString, colourCoding=colourCoding)
    formatter: Formatter = Formatter(formatString)
    requestFormatter: Formatter = Formatter("[%(asctime)s] [Requests] [%(levelname)s] %(message)s")

    # Add the handlers to the logger
    for handler in handlers:
        # Only add colour coding to the stream handler
        if doColour and (not isinstance(handler, DatabaseLogHandler) and not isinstance(handler, FileHandler)):
            handler.setFormatter(colourFormatter)
            logger.addHandler(handler)
            continue

        # If the handler is a database log handler, set the formatter to the request formatter
        if isinstance(handler, DatabaseLogHandler) and includeRequest:
            handler.setFormatter(requestFormatter)
            logger.addHandler(handler)
            continue

        # Otherwise, set the formatter to the formatter
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # Add the logger to the createdLoggers dictionary
    createdLoggers[name] = includeRequest

    return SuppressedLoggerAdapter(logger, extra={"loggername": name})
