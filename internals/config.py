"""
Configuration module for the server.
"""
# Standard Library Imports
from secrets import token_urlsafe as tokenUrlsafe
from socket import gethostbyname, gethostname

# Third Party Imports
from dynaconf import Dynaconf

# Load the settings object
settings: Dynaconf = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["config.yaml", ".env"],
    load_dotenv=True,
    environments=True,
    env_switcher="development",
    lowercase_read=True
)


# Create a class to consume the settings object

class Config:
    """
    Adapter and logic processing class for the settings object.
    """

    def __init__(self) -> None:
        """
        Initializes the Config object.
        """
        self.server = self.Server()
        self.logging = self.Logging()

    class Server:
        """
        Contains server related config data.
        """
        __slots__ = [
            "host",
            "port",
            "debug",
            "secretKey",
            "theme",
            "owner",
            "auth"
        ]

        def __init__(self) -> None:
            """
            Initializes the server object.
            """
            self.host: str = settings.server.host if settings.server.host != "auto" else gethostbyname(gethostname())
            self.port: int = settings.server.port
            self.debug: bool = settings.server.debug == "True"
            self.secretKey: str = settings.server.secretKey if settings.server.secretKey != "auto" else tokenUrlsafe(32)
            self.theme: str = settings.server.theme

            self.owner = self.Owner()
            self.auth = self.Auth()

        class Owner:
            """
            Contains owner related config data.
            """
            __slots__ = [
                "name",
                "email"
            ]

            def __init__(self) -> None:
                """
                Initializes the owner object.
                """
                self.name: str = settings.server.owner.name
                self.email: str = settings.server.owner.email  # This is throwing an error

        class Auth:
            """
            Contains auth related config data.
            """
            __slots__ = [
                "username",
                "password"
            ]

            def __init__(self) -> None:
                """
                Initializes the auth object.
                """
                self.username = settings.server.auth.username
                self.password = settings.server.auth.password

    class Logging:
        """
        Contains logging related config data.
        """
        __slots__ = [
            "handlers",
            "level",
            "db"
        ]

        def __init__(self) -> None:
            """
            Initializes the logging object.
            """
            self.handlers: list[str] = settings.logging.handlers
            match settings.logging.level:
                case "DEBUG":
                    self.level: int = 10
                case "INFO":
                    self.level: int = 20
                case "WARNING":
                    self.level: int = 30
                case "ERROR":
                    self.level: int = 40
                case "CRITICAL":
                    self.level: int = 50
                case _:
                    self.level: int = 20

            # Only initialize the db object if the db handler is in the handlers list
            if "db" in self.handlers:
                self.db = self.Db()

        class Db:
            """
            Contains logging database related config data.
            """
            __slots__ = [
                "host",
                "port",
                "name",
                "user",
                "password"
            ]

            def __init__(self) -> None:
                """
                Initializes the db object.
                """
                self.host: str = settings.logging.db.host
                self.port: int = settings.logging.db.port
                self.name: str = settings.logging.db.name
                self.user: str = settings.logging.db.user
                self.password: str = settings.logging.db.password

    class Db:
        """
        Contains logging database related config data.
        """
        __slots__ = [
            "host",
            "port",
            "name",
            "user",
            "password"
        ]

        def __init__(self) -> None:
            """
            Initializes the db object.
            """
            self.host: str = settings.db.host
            self.port: int = settings.db.port
            self.name: str = settings.db.name
            self.user: str = settings.db.user
            self.password: str = settings.db.password
