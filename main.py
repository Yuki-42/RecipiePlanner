"""
Main script for project.
"""
from base64 import b64decode
from logging import getLogger
# Standard imports
from secrets import token_urlsafe

# Third party imports
from flask import Flask, Response, render_template as render, request

from internals.clogging import SuppressedLoggerAdapter, createLogger
from internals.config import Config

# Constants
EXPECTED_COOKIES: list[str]

# Constants
config: Config = Config()

# Create the logger
logger: SuppressedLoggerAdapter = createLogger(
    "endpoints",
    level=config.logging.level,
    includeRequest=True,
    config=config
)

# Kill the standard werkzeug logger
werkzeugLogger = getLogger("werkzeug")
werkzeugLogger.disabled = True

# Add a workaround for a bug in FlaskInjector
Flask.url_for.__annotations__ = {}

# Create the Flask app
app: Flask = Flask(__name__, static_folder="static", template_folder="templates")

# Set static and template folders
app.static_folder = "static"
app.template_folder = "templates"


# Processors
@app.before_request
def beforeRequest() -> Response | None:
    """
    Runs before each request. Ensures that the user is logged in.

    If the user is not logged in, respond with a 401 error code.

    Returns:
        None
    """
    # Set request uuid
    g.uuid = uuid4()
    g.completed = False
    logger.info(  # 2 spaces here to match the indentation of the response log
        f"Request  [{g.uuid}] [{request.method}] [{request.path}] from {request.headers["X-Forwarded-For"] if "X-Forwarded-For" in request.headers else request.remote_addr} with "
        f"with cookies {request.cookies.to_dict()}"
    )

    # Check if the request is for static
    if request.path == "/static/css/_colours.css" and request.method == "GET":
        # Return the correct colour css file based on the theme
        return app.send_static_file(f"css/{request.cookies.get("theme", config.server.theme)}_colours.css")

    # Check if the request is coming from the server or is from one of the development machines
    if request.remote_addr == config.server.host or (request.remote_addr in ["192.168.0.223"] and config.server.debug):
        # Continue to route
        return

    fail: Response = Response(
        "Unauthorized",
        headers={"WWW-Authenticate": "Basic realm='Login Required.'"},
        status=401
    )

    if "Authorization" not in request.headers:
        return fail

    # Decode the authorization header and check if it is correct
    username, password = b64decode(request.headers["Authorization"].split(" ")[1]).decode("utf-8").split(":")

    if password != config.server.auth.password or username != config.server.auth.username:
        return fail


@app.context_processor
def processor() -> dict:
    """
    Injects site-wide variables into the template context.
    """
    return {
        "year": datetime.now().year,
        "reCapchaSiteKey": config.server.recaptcha.siteKey
    }


@app.after_request
def afterRequest(
        response: Response
) -> Response:
    """
    Runs after each request. Logs the response and deals with cookies.

    Args:
        response (Response): The response to log.

    Returns:
        Response: The response.
    """
    g.completed = True
    g.response = response
    logger.info(f"Response [{g.uuid}] [{response.status_code}]")
    # Add a theme cookie to the response if the user doesn't have one
    if "theme" not in request.cookies:
        response.set_cookie("theme", config.server.theme, samesite="Strict")

    # Purge any cookies that are not expected
    for cookie in request.cookies:
        if cookie not in EXPECTED_COOKIES:
            response.delete_cookie(cookie)

    return response


# Create the routes
@app.route("/")
def index() -> str | Response:
    """
    Index route for the server.

    Returns:
        str | Response: The rendered index page.
    """
    return render("index.html")  # This is just for testing


# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, use_reloader=True)
