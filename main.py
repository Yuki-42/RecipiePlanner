"""
Main script for project.
"""

# Standard imports
from secrets import token_urlsafe

# Third party imports
from flask import Flask, Response, render_template as render

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


# Create the routes
@app.route("/")
def index() -> str | Response:
    """
    Index route for the server.

    Returns:
        str | Response: The rendered index page.
    """
    return render("planner.html")  # This is just for testing


# Run the app
if __name__ == "__main__":
    app.run(host=config.host, port=config.port, use_reloader=True)
