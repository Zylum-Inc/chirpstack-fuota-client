import grpc

from ...proto.fuota import fuota_pb2, fuota_pb2_grpc
from ...utils.helpers import auth_header, create_channel
from .utils import FuotaUtils


class FuotaService:
    def __init__(self, server_address, api_token):
        self.server_address = server_address
        self.api_token = api_token
        self.channel = create_channel(self.server_address)
        self.stub = fuota_pb2_grpc.FuotaServerServiceStub(self.channel)

    def create_deployment(
        self, application_id, devices, multicast_group_type, multicast_dr, multicast_frequency, **kwargs
    ):
        try:
            deployment_devices = FuotaUtils.create_deployment_devices(devices)

            multicast_group_type = FuotaUtils.get_multicast_group_type(multicast_group_type)
            if "multicast_region" in kwargs:
                kwargs["multicast_region"] = FuotaUtils.get_region(kwargs["multicast_region"])
            if "request_fragmentation_session_status" in kwargs:
                kwargs["request_fragmentation_session_status"] = FuotaUtils.get_request_fragmentation_session_status(
                    kwargs["request_fragmentation_session_status"]
                )

            if "unicast_timeout" in kwargs:
                kwargs["unicast_timeout"] = FuotaUtils.create_duration(kwargs["unicast_timeout"])

            deployment = fuota_pb2.Deployment(
                application_id=application_id,
                devices=deployment_devices,
                multicast_group_type=multicast_group_type,
                multicast_dr=multicast_dr,
                multicast_frequency=multicast_frequency,
                **kwargs,
            )
            request = fuota_pb2.CreateDeploymentRequest(deployment=deployment)
            response = self.stub.CreateDeployment(request, metadata=auth_header(self.api_token))
            return response
        except grpc.RpcError as e:
            raise Exception(f"Failed to create FUOTA deployment: {str(e)}")

    def get_deployment_status(self, deployment_id):
        try:
            request = fuota_pb2.GetDeploymentStatusRequest(id=deployment_id)
            response = self.stub.GetDeploymentStatus(request, metadata=auth_header(self.api_token))
            return response
        except grpc.RpcError as e:
            raise Exception(f"Failed to get FUOTA deployment status: {str(e)}")

    def get_deployment_device_logs(self, deployment_id, dev_eui):
        try:
            request = fuota_pb2.GetDeploymentDeviceLogsRequest(deployment_id=deployment_id, dev_eui=dev_eui)
            response = self.stub.GetDeploymentDeviceLogs(request, metadata=auth_header(self.api_token))
            return response
        except grpc.RpcError as e:
            raise Exception(f"Failed to get FUOTA deployment device logs: {str(e)}")
