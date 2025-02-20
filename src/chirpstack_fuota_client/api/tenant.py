import grpc
from chirpstack_api import api

from ..utils.helpers import auth_header, create_channel


class TenantService:
    def __init__(self, server_address, api_token):
        self.server_address = server_address
        self.api_token = api_token
        self.channel = create_channel(self.server_address)
        self.stub = api.TenantServiceStub(self.channel)

    def create(self, name, description=""):
        try:
            existing_tenant = self.get_by_name(name)
            if existing_tenant:
                return existing_tenant

            req = api.CreateTenantRequest(
                tenant=api.Tenant(
                    name=name,
                    description=description,
                    can_have_gateways=True,
                )
            )
            return self.stub.Create(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to create tenant: {str(e)}")

    def get(self, tenant_id):
        req = api.GetTenantRequest(id=tenant_id)
        try:
            return self.stub.Get(req, metadata=auth_header(self.api_token)(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to get tenant: {str(e)}")

    def get_by_name(self, name):
        req = api.ListTenantsRequest(
            limit=1,
            search=name,
        )
        try:
            resp = self.stub.List(req, metadata=auth_header(self.api_token))
            for tenant in resp.result:
                if tenant.name == name:
                    return tenant
            return None
        except grpc.RpcError as e:
            raise Exception(f"Failed to get tenant by name: {str(e)}")

    def update(self, tenant_id, name, description=""):
        req = api.UpdateTenantRequest(
            tenant=api.Tenant(
                id=tenant_id,
                name=name,
                description=description,
            )
        )
        try:
            self.stub.Update(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to update tenant: {str(e)}")

    def delete(self, tenant_id):
        req = api.DeleteTenantRequest(id=tenant_id)
        try:
            self.stub.Delete(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to delete tenant: {str(e)}")

    def list(self, limit=10, offset=0):
        req = api.ListTenantsRequest(
            limit=limit,
            offset=offset,
        )
        try:
            return self.stub.List(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to list tenants: {str(e)}")
