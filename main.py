"""
Main script for project.
"""

# Standard imports
from secrets import token_urlsafe

# Third party imports
from flask import Flask

# Package Relative Imports
from internals.dotenvSuper import Config
from internals.logging import createLogger, SuppressedLoggerAdapter

# Create the Config
config: Config = Config()

# Create the logger
logger: SuppressedLoggerAdapter = createLogger("Main", level=config.loggingLevel)

# Create the Flask app
app: Flask = Flask(__name__)

# Generate the secret key for the Flask app randomly
app.secret_key = token_urlsafe(128)

