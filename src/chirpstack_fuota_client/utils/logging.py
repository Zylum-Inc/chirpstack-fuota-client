import logging
import sys

LOG_FORMAT = "CHIRPSTACK-FUOTA-CLIENT - %(levelname)s: \t%(message)s"


def setup_logging(level=logging.INFO, **kwargs):
    """Configure logging for the chirpstack client.

    Args:
        level: Logging level (default: DEBUG)
    """
    logging.basicConfig(level=level, format=LOG_FORMAT, stream=sys.stdout, **kwargs)

    # Set log levels for noisy third-party libraries
    logging.getLogger("grpc").setLevel(logging.WARNING)
    logging.getLogger("google").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    # Create logger for chirpstack_fuota_client
    logger = logging.getLogger("chirpstack_fuota_client")
    logger.setLevel(logging.WARNING)
    logger.info("Logging initialized with level %s", logging.getLevelName(level))
    logger.setLevel(level)

    return logger


# Create default logger instance
logger = setup_logging()
