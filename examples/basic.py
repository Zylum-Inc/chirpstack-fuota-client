import os

from dotenv import load_dotenv
from rich import print
from rich.traceback import install

from chirpstack_fuota_client import (
    ApplicationService,
    DeviceProfileService,
    DeviceService,
    GatewayService,
    TenantService,
)

install()
load_dotenv()

server_address = os.getenv("SERVER_ADDRESS")
api_token = os.getenv("API_TOKEN")

# Create Tenant
tenant_service = TenantService(server_address, api_token)
tenant = tenant_service.create("TAS managed organization")
tenant_id = tenant.id

# Create Application
app_service = ApplicationService(server_address, api_token)
app = app_service.create(tenant_id=tenant_id, name="TAS managed application", tags={"environment": "prod"})
app_id = app.id

# Create Device Profile
dev_prof_service = DeviceProfileService(server_address, api_token)
device_profile = dev_prof_service.create(
    tenant_id,
    "My Device Profile",
    region="US915",
    mac_version="LORAWAN_1_0_3",
    reg_params_revision="RP002_1_0_3",
    flush_queue_on_activate=True,
    supports_otaa=True,
)
device_profile_id = device_profile.id

# Create Gateway
gateway_service = GatewayService(server_address, api_token)
gateway_id = "62d024cf42059166"
gateway = gateway_service.create(
    tenant_id=tenant_id, gateway_id=gateway_id, name="zephyrus_gw_3", description="zephyrus_gw_3", stats_interval=30
)

# Create Device
device_service = DeviceService(server_address, api_token)
dev_eui = "40b9693dc8637506"
device = device_service.create(
    application_id=app_id,
    name="TAS Dev Node 1",
    dev_eui=dev_eui,
    app_key="ad5a4cb874b1659181ce84f9c7e33c37",
    mac_version="LORAWAN_1_0_3",
    device_profile_id=device_profile_id,
    description="A sample device",
    is_disabled=False,
    tags={"location": "building-1", "floor": "3", "type": "sensor"},
)

# Send a downlink message
downlink = device_service.queue_downlink(dev_eui=dev_eui, data="Hi", confirmed=True, fport=10)
downlink_id = downlink.id

print(f"Created tenant: {tenant_id}")
print(f"Created application: {app_id}")
print(f"Created device profile: {device_profile_id}")
print(f"Added gateway: {gateway_id}")
print(f"Added device: {dev_eui}")
print(f"Sent Downlink id: {downlink_id}")
