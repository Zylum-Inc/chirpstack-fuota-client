import grpc
from chirpstack_api import api

from ..utils.helpers import auth_header, create_channel


class DeviceProfileService:
    def __init__(self, server_address, api_token):
        self.server_address = server_address
        self.api_token = api_token
        self.channel = create_channel(self.server_address)
        self.stub = api.DeviceProfileServiceStub(self.channel)

    def create(self, tenant_id, name, **kwargs):
        try:
            existing_profile = self.get_by_name(tenant_id, name)
            if existing_profile:
                return existing_profile

            req = api.CreateDeviceProfileRequest(
                device_profile=api.DeviceProfile(name=name, tenant_id=tenant_id, **kwargs)
            )
            return self.stub.Create(req, metadata=auth_header(self.api_token))

        except grpc.RpcError as e:
            raise Exception(f"Failed to create device profile: {str(e)}")

    def get(self, device_profile_id):
        req = api.GetDeviceProfileRequest(id=device_profile_id)
        try:
            return self.stub.Get(req, metadata=auth_header(self.api_token)).device_profile
        except grpc.RpcError as e:
            raise Exception(f"Failed to get device profile: {str(e)}")

    def get_by_name(self, tenant_id, name):
        req = api.ListDeviceProfilesRequest(
            limit=1,
            search=name,
            tenant_id=tenant_id,
        )
        try:
            resp = self.stub.List(req, metadata=auth_header(self.api_token))
            for profile in resp.result:
                if profile.name == name:
                    return profile
            return None
        except grpc.RpcError as e:
            raise Exception(f"Failed to get device profile by name: {str(e)}")

    def update(self, device_profile_id, name, **kwargs):
        req = api.UpdateDeviceProfileRequest(
            device_profile=api.DeviceProfile(id=device_profile_id, name=name, **kwargs)
        )
        try:
            self.stub.Update(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to update device profile: {str(e)}")

    def delete(self, device_profile_id):
        req = api.DeleteDeviceProfileRequest(id=device_profile_id)
        try:
            self.stub.Delete(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to delete device profile: {str(e)}")

    def list(self, tenant_id, limit=10, offset=0):
        req = api.ListDeviceProfilesRequest(
            tenant_id=tenant_id,
            limit=limit,
            offset=offset,
        )
        try:
            return self.stub.List(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to list device profiles: {str(e)}")
