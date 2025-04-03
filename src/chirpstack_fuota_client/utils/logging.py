import logging
import sys

LOG_FORMAT = "CHIRPSTACK-FUOTA-CLIENT - %(levelname)s: \t%(message)s"


def setup_logging(level=logging.CRITICAL, **kwargs):
    """Configure logging for the chirpstack client.

    Args:
        level: Logging level (default: DEBUG)
    """
    custom_logger = logging.getLogger("chirpstack_fuota_client")
    custom_logger.setLevel(level)
    
    # Create console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    
    # Create formatter and add it to the handlers
    formatter = logging.Formatter(LOG_FORMAT)
    ch.setFormatter(formatter)
    
    # Add the handlers to the logger
    if not custom_logger.handlers:
        custom_logger.addHandler(ch)
    
    # Set log levels for noisy third-party libraries
    logging.getLogger("grpc").setLevel(logging.WARNING)
    logging.getLogger("google").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    custom_logger.info("Logging initialized with level %s", logging.getLevelName(level))

    return custom_logger

# Create default logger instance
logger = setup_logging()
