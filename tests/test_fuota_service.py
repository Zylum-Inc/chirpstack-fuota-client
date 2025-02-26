import pytest
from unittest.mock import MagicMock, patch
import grpc
from chirpstack_fuota_client.api.fuota.service import FuotaService
from chirpstack_fuota_client.proto.fuota import fuota_pb2, fuota_pb2_grpc

@pytest.fixture
def mock_stub():
    mock = MagicMock(spec=fuota_pb2_grpc.FuotaServerServiceStub)
    mock.CreateDeployment = MagicMock()
    mock.GetDeploymentStatus = MagicMock()
    mock.GetDeploymentDeviceLogs = MagicMock()
    return mock

@pytest.fixture
def fuota_service(mock_stub):
    service = FuotaService(server_address='localhost:50051', api_token='test_token')
    service.stub = mock_stub
    return service

def test_create_deployment_success(fuota_service, mock_stub):
    mock_stub.CreateDeployment.return_value = fuota_pb2.CreateDeploymentResponse()
    response = fuota_service.create_deployment(
        application_id='app_id',
        devices=[],
        multicast_group_type='CLASS_B',
        multicast_dr=0,
        multicast_frequency=868100000
    )
    assert isinstance(response, fuota_pb2.CreateDeploymentResponse)
    mock_stub.CreateDeployment.assert_called_once()

def test_create_deployment_failure(fuota_service, mock_stub):
    mock_stub.CreateDeployment.side_effect = grpc.RpcError('Failed to create deployment')
    with pytest.raises(Exception, match='Failed to create FUOTA deployment'):
        fuota_service.create_deployment(
            application_id='app_id',
            devices=[],
            multicast_group_type='CLASS_B',
            multicast_dr=0,
            multicast_frequency=868100000
        )

def test_get_deployment_status_success(fuota_service, mock_stub):
    mock_stub.GetDeploymentStatus.return_value = fuota_pb2.GetDeploymentStatusResponse()
    response = fuota_service.get_deployment_status(deployment_id='deployment_id')
    assert isinstance(response, fuota_pb2.GetDeploymentStatusResponse)
    mock_stub.GetDeploymentStatus.assert_called_once()

def test_get_deployment_status_failure(fuota_service, mock_stub):
    mock_stub.GetDeploymentStatus.side_effect = grpc.RpcError('Failed to get deployment status')
    with pytest.raises(Exception, match='Failed to get FUOTA deployment status'):
        fuota_service.get_deployment_status(deployment_id='deployment_id')

def test_get_deployment_device_logs_success(fuota_service, mock_stub):
    mock_stub.GetDeploymentDeviceLogs.return_value = fuota_pb2.GetDeploymentDeviceLogsResponse()
    response = fuota_service.get_deployment_device_logs(deployment_id='deployment_id', dev_eui='dev_eui')
    assert isinstance(response, fuota_pb2.GetDeploymentDeviceLogsResponse)
    mock_stub.GetDeploymentDeviceLogs.assert_called_once()

def test_get_deployment_device_logs_failure(fuota_service, mock_stub):
    mock_stub.GetDeploymentDeviceLogs.side_effect = grpc.RpcError('Failed to get deployment device logs')
    with pytest.raises(Exception, match='Failed to get FUOTA deployment device logs'):
        fuota_service.get_deployment_device_logs(deployment_id='deployment_id', dev_eui='dev_eui')