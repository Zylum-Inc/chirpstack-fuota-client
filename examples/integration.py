import os

from dotenv import load_dotenv
from rich import print
from rich.traceback import install

from chirpstack_client import IntegrationService

install()
load_dotenv()

server_address = os.getenv("SERVER_ADDRESS")
api_token = os.getenv("API_TOKEN")

app_id = "dbde71df-801e-48bd-bc5c-3fb1dc01a2e6"
endpoint_url = "http://172.17.0.1:8005/integrations/chirpstack/d6ff3fd9-a2b0-4d8c-bc1d-7070b0964b88/data/messages/"

integration_service = IntegrationService(server_address, api_token)
integration = integration_service.create(
    integration_type="http", application_id=app_id, event_endpoint_url=endpoint_url
)

print(f"Created integration: {integration}")
