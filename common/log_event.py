import logging
from datetime import datetime

"""
Create a log message for an event
"""
def log_event(system, event, user, description):
    logger = logging.getLogger(__name__)
    message = f"System: {system}, Event: {event}, User: {user}, Description: {description}"
    logger.info(message)
    timestamp = datetime.now().strftime("[%d/%b/%Y %H:%M:%S]")
    message = f"{timestamp} {message}"
    print(message)