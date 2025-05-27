from fastapi import Request
import logging
from datetime import datetime

logger = logging.getLogger("bookify_logger")
logger.setLevel(logging.INFO)


def log_request(request: Request):
    logger.info(f"{datetime.now()} - {request.method} {request.url}")
