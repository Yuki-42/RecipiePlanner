"""
Initializes the logging module.
"""

from .adapters import SuppressedLoggerAdapter
from .funcs import createLogger

__all__ = [
    "SuppressedLoggerAdapter"
]
