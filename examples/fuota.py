import os

from dotenv import load_dotenv
from rich import print
from rich.traceback import install

from chirpstack_fuota_client import FuotaService, FuotaUtils

install()
load_dotenv()

server_address = os.getenv("SERVER_ADDRESS")
api_token = os.getenv("API_TOKEN")
fuota_server_address = os.getenv("FUOTA_SERVER_ADDRESS")

app_id = "dbde71df-801e-48bd-bc5c-3fb1dc01a2e6"
dev_eui = "40b9693dc8637506"

fuota_service = FuotaService(fuota_server_address, api_token)

devices = [{"dev_eui": dev_eui, "gen_app_key": "09000000000000000000000000000000"}]

deployment_config = FuotaUtils.create_deployment_config(
    multicast_timeout=6,
    unicast_timeout=60,
    fragmentation_fragment_size=50,
    fragmentation_redundancy=1,
)

deployment_response = fuota_service.create_deployment(
    application_id=app_id,
    devices=devices,
    multicast_group_type="CLASS_C",
    multicast_dr=5,
    multicast_frequency=868100000,
    multicast_group_id=0,
    multicast_region="EU868",
    request_fragmentation_session_status="AFTER_SESSION_TIMEOUT",
    payload=b"\x00" * 100,
    **deployment_config,
)

print(f"Created FUOTA deployment with ID: {deployment_response.id}")

# Get deployment status
status_response = fuota_service.get_deployment_status(deployment_response.id)
print(f"Deployment status: {status_response}")

# Get device logs for the deployment
logs_response = fuota_service.get_deployment_device_logs(deployment_response.id, dev_eui)
print(f"Device logs: {logs_response}")
