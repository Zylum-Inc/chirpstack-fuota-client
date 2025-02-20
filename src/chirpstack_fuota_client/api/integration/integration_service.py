import grpc
from chirpstack_api import api

from ...utils.helpers import auth_header, create_channel
from .http_integration import HttpIntegration


class IntegrationService:
    def __init__(self, server_address, api_token):
        self.server_address = server_address
        self.api_token = api_token
        self.channel = create_channel(self.server_address)
        self.stub = api.ApplicationServiceStub(self.channel)
        self.integrations = {"http": HttpIntegration(self.stub, self.api_token)}

    def create(self, integration_type, application_id, **kwargs):
        if integration_type not in self.integrations:
            raise ValueError(f"Unsupported integration type: {integration_type}")

        existing_integration = self.get(integration_type, application_id)
        if existing_integration is not None:
            raise Exception(
                f"{integration_type.capitalize()} integration already exists for application {application_id}"
            )

        return self.integrations[integration_type].create(application_id, **kwargs)

    def get(self, integration_type, application_id):
        if integration_type not in self.integrations:
            raise ValueError(f"Unsupported integration type: {integration_type}")
        return self.integrations[integration_type].get(application_id)

    def update(self, integration_type, application_id, **kwargs):
        if integration_type not in self.integrations:
            raise ValueError(f"Unsupported integration type: {integration_type}")
        return self.integrations[integration_type].update(application_id, **kwargs)

    def delete(self, integration_type, application_id):
        if integration_type not in self.integrations:
            raise ValueError(f"Unsupported integration type: {integration_type}")
        return self.integrations[integration_type].delete(application_id)

    def list(self, application_id):
        req = api.ListIntegrationsRequest(application_id=application_id)
        try:
            return self.stub.ListIntegrations(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to list integrations: {str(e)}")
