import logging

from .api.application import ApplicationService
from .api.device import DeviceService
from .api.device_profile import DeviceProfileService
from .api.fuota import (
    FuotaService,  # Add this line
    FuotaUtils,
)
from .api.gateway import GatewayService
from .api.integration import IntegrationService
from .api.tenant import TenantService
from .utils.logging import setup_logging

logger = setup_logging(level=logging.DEBUG)

__all__ = [
    "ApplicationService",
    "DeviceProfileService",
    "DeviceService",
    "GatewayService",
    "IntegrationService",
    "TenantService",
    "FuotaService",
    "FuotaUtils",
    "models",
]
