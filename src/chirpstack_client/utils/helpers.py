import grpc

from ..utils.logging import logger


def auth_header(api_token):
    """Create authorization header with Bearer token."""
    return [("authorization", f"Bearer {api_token}")]


def create_channel(server_address):
    """Create gRPC channel with TLS support for https URLs."""
    if server_address.startswith("https://"):
        server_address = server_address.replace("https://", "")
        logger.debug(f"Creating secure channel for: {server_address}")
        credentials = grpc.ssl_channel_credentials()
        return grpc.secure_channel(server_address, credentials)
    else:
        logger.debug(f"Creating insecure channel for: {server_address}")
        return grpc.insecure_channel(server_address)
