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

    def _execute(self, query: str, *args) -> Cursor:
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

    def addUser(self, email: str, rawPassword: str) -> int:
        """
        Adds a user to the database.

        Args:
            email (str): The email of the user.
            rawPassword (str): The password of the user.

        Returns:
            int: The ID of the user.
        """

        # Hash password
        password: str = pbkdf2_sha512.hash(rawPassword)

        # Remove raw password from memory
        rawPassword = None
        del rawPassword

        # Execute the query
        cursor: Cursor = self._execute("INSERT INTO users (email, password) VALUES (?, ?)", email, password)

        # Get the ID of the user
        uid: int = cursor.lastrowid

        # Commit the changes
        self.connection.commit()

        # Return the ID of the user
        return uid
