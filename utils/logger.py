import json
import logging
import os

import colorlog
from fastapi.responses import JSONResponse


class UTF8JSONFormatter(logging.Formatter):
    """
    A logging formatter to format log messages in UTF-8 JSON format.

    Args:
        record (logging.LogRecord): Log record containing the message and metadata.

    Returns:
        str: A formatted log message in UTF-8 JSON format.

    Example:
        >>> formatter = UTF8JSONFormatter()
        >>> log_message = formatter.format(record)
        '{"message": "example"}'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    def format(self, record):
        if isinstance(record.msg, dict):
            record.msg = json.dumps(record.msg, ensure_ascii=False)
        elif isinstance(record.msg, str):
            try:
                json_msg = json.loads(record.msg)
                record.msg = json.dumps(json_msg, ensure_ascii=False, indent=2)
            except json.JSONDecodeError:
                pass
        return super().format(record)


def setup_logger() -> logging.Logger:
    """
    Set up and configure a logger that only outputs to the console (no file logging).

    Returns:
        logging.Logger: Configured logger instance.

    Example:
        >>> logger = setup_logger()
        >>> logger.info("Logger is ready.")

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    logger = colorlog.getLogger(__name__)

    if not logger.handlers:
        # Console handler for colored logs
        console_handler = colorlog.StreamHandler()
        console_handler.setFormatter(
            colorlog.ColoredFormatter(
                "%(log_color)s%(levelname)s:%(name)s:%(pathname)s:"
                "%(funcName)s:%(lineno)d:%(message)s",
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red,bg_white",
                },
            )
        )
        logger.addHandler(console_handler)

        logger.setLevel(logging.DEBUG)

    return logger


def handle_response(
    message: str, status_code: int = 400
) -> JSONResponse:
    """
    Handle and log an HTTP response with a given message and status code.

    Args:
        message (str): Response message to be logged and returned.
        status_code (int, optional): HTTP status code. Defaults to 400.

    Returns:
        JSONResponse: Response object containing the status code and message.

    Example:
        >>> response = handle_response("Success", 200)
        >>> response.status_code
        200

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    logger = setup_logger()

    if 200 <= status_code < 300:
        logger.info(message)
    else:
        logger.error(message)

    return JSONResponse(
        status_code=status_code,
        content={"status": status_code, "message": message},
    )
