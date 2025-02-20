import grpc
from chirpstack_api import api

from ..utils.helpers import auth_header, create_channel


class GatewayService:
    def __init__(self, server_address, api_token):
        self.server_address = server_address
        self.api_token = api_token
        self.channel = create_channel(self.server_address)
        self.stub = api.GatewayServiceStub(self.channel)

    def create(self, tenant_id, gateway_id, name, description="", location=None, **kwargs):
        try:
            existing_gateway = self.get_by_name(tenant_id, name)
            if existing_gateway:
                return existing_gateway

            req = api.CreateGatewayRequest(
                gateway=api.Gateway(
                    gateway_id=gateway_id,
                    name=name,
                    description=description,
                    location=location,
                    tenant_id=tenant_id,
                    **kwargs,
                )
            )
            return self.stub.Create(req, metadata=auth_header(self.api_token))

        except grpc.RpcError as e:
            raise Exception(f"Failed to create gateway: {str(e)}")

    def get(self, gateway_id):
        req = api.GetGatewayRequest(gateway_id=gateway_id)
        try:
            return self.stub.Get(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to get gateway: {str(e)}")

    def get_by_name(self, tenant_id, name):
        req = api.ListGatewaysRequest(limit=1, search=name, tenant_id=tenant_id)
        try:
            resp = self.stub.List(req, metadata=auth_header(self.api_token))
            for gateway in resp.result:
                if gateway.name == name:
                    return gateway
            return None
        except grpc.RpcError as e:
            raise Exception(f"Failed to get gateway by name: {str(e)}")

    def update(self, gateway_id, name, description="", location=None, **kwargs):
        req = api.UpdateGatewayRequest(
            gateway=api.Gateway(gateway_id=gateway_id, name=name, description=description, location=location, **kwargs)
        )
        try:
            self.stub.Update(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to update gateway: {str(e)}")

    def delete(self, gateway_id):
        req = api.DeleteGatewayRequest(gateway_id=gateway_id)
        try:
            self.stub.Delete(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to delete gateway: {str(e)}")

    def list(self, tenant_id, limit=10, offset=0):
        req = api.ListGatewaysRequest(
            tenant_id=tenant_id,
            limit=limit,
            offset=offset,
        )
        try:
            return self.stub.List(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to list gateways: {str(e)}")
