"""
Structured logging setup using Logfire for compliance and observability.
"""
import logfire
import sys

logfire.configure(
    send_to_logfire="if-token-present",
    json=True,
    level="INFO",
    stream=sys.stdout,
)

def get_logger(name: str):
    """
    Returns a Logfire logger instance.

    Args:
        name (str): Logger name.

    Returns:
        logfire.Logger: Configured logger.
    """
    return logfire.get_logger(name)
