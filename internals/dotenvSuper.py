"""
Contains the `Config` class for RecipiePlanner
"""

# Standard Imports
from os import environ

# Third-Party Imports
from dotenv import load_dotenv as loadDotenv

# Local Imports
from .logging import createLogger, SuppressedLoggerAdapter


class Config:
    """
    Contains the configuration for RecipiePlanner.
    """

    def __init__(self) -> None:
        """
        Initializes the configuration object.
        """
        # Load the environment variables
        loadDotenv()

        # Create the logger
        self.logger = createLogger("Config", level=self.loggingLevel)

    @property
    def host(self) -> str:
        """
        Host address for the server.
        """
        return environ.get("HOST", "192.168.0.32")

    @property
    def port(self) -> int:
        """
        Port for the server.
        """
        return int(environ.get("PORT", 80))

    @property
    def loggingLevel(self) -> str:
        """
        Logging level for the server.
        """
        return environ.get("LOGGING_LEVEL", "DEBUG")

