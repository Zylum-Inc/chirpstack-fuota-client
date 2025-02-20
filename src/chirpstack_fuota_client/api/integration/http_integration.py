import grpc
from chirpstack_api import api

from ...utils.helpers import auth_header
from .base import BaseIntegration


class HttpIntegration(BaseIntegration):
    def __init__(self, stub, api_token):
        self.stub = stub
        self.api_token = api_token

    def create(self, application_id, event_endpoint_url, headers=None):
        req = api.CreateHttpIntegrationRequest(
            integration=api.HttpIntegration(
                application_id=application_id,
                headers={} if headers is None else headers,
                event_endpoint_url=event_endpoint_url,
            )
        )
        try:
            return self.stub.CreateHttpIntegration(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to create HTTP integration: {str(e)}")

    def get(self, application_id):
        req = api.GetHttpIntegrationRequest(application_id=application_id)
        try:
            return self.stub.GetHttpIntegration(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return None
            raise Exception(f"Failed to get HTTP integration: {str(e)}")

    def update(self, application_id, event_endpoint_url, headers=None):
        req = api.UpdateHttpIntegrationRequest(
            integration=api.HttpIntegration(
                application_id=application_id,
                headers={} if headers is None else headers,
                event_endpoint_url=event_endpoint_url,
            )
        )
        try:
            return self.stub.UpdateHttpIntegration(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to update HTTP integration: {str(e)}")

    def delete(self, application_id):
        req = api.DeleteHttpIntegrationRequest(application_id=application_id)
        try:
            return self.stub.DeleteHttpIntegration(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to delete HTTP integration: {str(e)}")
