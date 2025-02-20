import grpc
from chirpstack_api import api

from ..utils.helpers import auth_header, create_channel


class ApplicationService:
    def __init__(self, server_address, api_token):
        self.server_address = server_address
        self.api_token = api_token
        self.channel = create_channel(self.server_address)
        self.stub = api.ApplicationServiceStub(self.channel)

    def create(self, tenant_id, name, description="", **kwargs):
        try:
            existing_application = self.get_by_name(tenant_id, name)
            if existing_application:
                return existing_application

            req = api.CreateApplicationRequest(
                application=api.Application(name=name, description=description, tenant_id=tenant_id, **kwargs)
            )
            return self.stub.Create(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to create application: {str(e)}")

    def get(self, application_id):
        req = api.GetApplicationRequest(id=application_id)
        try:
            return self.stub.Get(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to get application: {str(e)}")

    def get_by_name(self, tenant_id, name):
        req = api.ListApplicationsRequest(
            limit=1,
            search=name,
            tenant_id=tenant_id,
        )
        try:
            resp = self.stub.List(req, metadata=auth_header(self.api_token))
            for app in resp.result:
                if app.name == name:
                    return app
            return None
        except grpc.RpcError as e:
            raise Exception(f"Failed to get application by name: {str(e)}")

    def update(self, application_id, name, description="", **kwargs):
        req = api.UpdateApplicationRequest(
            application=api.Application(id=application_id, name=name, description=description, **kwargs)
        )
        try:
            self.stub.Update(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to update application: {str(e)}")

    def delete(self, application_id):
        req = api.DeleteApplicationRequest(id=application_id)
        try:
            resp = self.stub.Delete(req, metadata=auth_header(self.api_token))
            print(resp)
        except grpc.RpcError as e:
            raise Exception(f"Failed to delete application: {str(e)}")

    def list(self, tenant_id, limit=10, offset=0):
        req = api.ListApplicationsRequest(
            tenant_id=tenant_id,
            limit=limit,
            offset=offset,
        )
        try:
            return self.stub.List(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to list applications: {str(e)}")
