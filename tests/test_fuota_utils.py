import pytest
from Crypto.Cipher import AES
from google.protobuf import duration_pb2
from chirpstack_fuota_client.api.fuota.utils import FuotaUtils
from chirpstack_fuota_client.proto.fuota import fuota_pb2

def test_get_multicast_group_type():
    assert FuotaUtils.get_multicast_group_type("CLASS_B") == fuota_pb2.MulticastGroupType.CLASS_B
    assert FuotaUtils.get_multicast_group_type("CLASS_C") == fuota_pb2.MulticastGroupType.CLASS_C
    with pytest.raises(ValueError):
        FuotaUtils.get_multicast_group_type("INVALID")

def test_create_duration():
    duration = FuotaUtils.create_duration(60)
    assert isinstance(duration, duration_pb2.Duration)
    assert duration.seconds == 60

def test_get_request_fragmentation_session_status():
    assert FuotaUtils.get_request_fragmentation_session_status("AFTER_FRAGMENT_ENQUEUE") == fuota_pb2.RequestFragmentationSessionStatus.AFTER_FRAGMENT_ENQUEUE
    assert FuotaUtils.get_request_fragmentation_session_status("AFTER_SESSION_TIMEOUT") == fuota_pb2.RequestFragmentationSessionStatus.AFTER_SESSION_TIMEOUT
    assert FuotaUtils.get_request_fragmentation_session_status("NO_REQUEST") == fuota_pb2.RequestFragmentationSessionStatus.NO_REQUEST
    assert FuotaUtils.get_request_fragmentation_session_status("INVALID") == fuota_pb2.RequestFragmentationSessionStatus.NO_REQUEST

def test_get_region():
    assert FuotaUtils.get_region("EU868") == fuota_pb2.Region.EU868
    assert FuotaUtils.get_region("US915") == fuota_pb2.Region.US915
    assert FuotaUtils.get_region("INVALID") == fuota_pb2.Region.EU868

def test_create_deployment_config():
    config = FuotaUtils.create_deployment_config()
    assert config["multicast_timeout"] == 6
    assert config["multicast_ping_slot_period"] == 1
    assert config["unicast_timeout"] == 60
    assert config["unicast_attempt_count"] == 1
    assert config["fragmentation_fragment_size"] == 50
    assert config["fragmentation_redundancy"] == 1
    assert config["fragmentation_session_index"] == 0
    assert config["fragmentation_matrix"] == 0
    assert config["fragmentation_block_ack_delay"] == 1
    assert config["fragmentation_descriptor"] == b"\x00\x00\x00\x00"

def test_get_key():
    key = b"thisisakey123456"
    data = b"thisisdata123456"
    cipher = AES.new(key, AES.MODE_ECB)
    expected = cipher.encrypt(data)
    assert FuotaUtils.get_key(key, data) == expected

def test_get_mc_root_key_for_gen_app_key():
    gen_app_key = "00112233445566778899aabbccddeeff"
    mc_root_key = FuotaUtils.get_mc_root_key_for_gen_app_key(gen_app_key)
    assert len(mc_root_key) == 32
    with pytest.raises(ValueError):
        FuotaUtils.get_mc_root_key_for_gen_app_key("invalidkey")

def test_create_deployment_devices():
    devices = [
        {"dev_eui": "0011223344556677", "gen_app_key": "00112233445566778899aabbccddeeff"}
    ]
    deployment_devices = FuotaUtils.create_deployment_devices(devices)
    assert len(deployment_devices) == 1
    assert deployment_devices[0].dev_eui == "0011223344556677"
    assert len(deployment_devices[0].mc_root_key) == 32