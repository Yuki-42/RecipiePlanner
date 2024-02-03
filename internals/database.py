"""
Contains the main database class for RecipiePlanner.
"""

# Standard Imports
from sqlite3 import connect, Connection, Cursor
from pathlib import Path

# Local Imports
from .logging import createLogger, SuppressedLoggerAdapter
from .dotenvSuper import Config


class Database:
    """
    Main database class for RecipiePlanner.
    """
    # Type hints
    logger: SuppressedLoggerAdapter
    databasePath: Path

    def __init__(self, config: Config, databasePath: Path = Path("ServerData/database.db")) -> None:
        """
        Initializes the database object.

        Args:
            config (Config): The configuration object for the server.
            databasePath (Path): The path to the database file.
        """
        # Create the logger
        self.logger: SuppressedLoggerAdapter = createLogger("Database", level="INFO")

        # Set the database path
        self.databasePath: Path = databasePath

        # Create the connection
        self.connection: Connection = connect(self.databasePath)

    def __del__(self) -> None:
        """
        Closes the database connection when the object is deleted.
        """
        self.connection.close()

    def execute(self, query: str, *args) -> Cursor:
        """
        Executes a query on the database.

        Args:
            query (str): The query to execute.
            *args: The arguments to pass to the query.

        Returns:
            Cursor: The cursor object for the query.
        """
        # Log the query
        self.logger.debug(f"Executing query: {query}")

        # Execute the query
        cursor: Cursor = self.connection.cursor()
        cursor.execute(query, args)
        return cursor
