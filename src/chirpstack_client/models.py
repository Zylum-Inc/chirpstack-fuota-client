from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Tenant:
    id: str
    name: str
    description: Optional[str] = None
    can_have_gateways: bool = True
    max_devices: int = 0
    max_gateways: int = 0


@dataclass
class Application:
    id: str
    name: str
    description: Optional[str] = None
    tenant_id: str


@dataclass
class DeviceProfile:
    id: str
    name: str
    tenant_id: str
    supports_class_b: bool = False
    supports_class_c: bool = False
    mac_version: str = "1.0.3"
    reg_params_revision: str = "B"
    adr_algorithm_id: str = "default"
    payload_codec_runtime: str = "NONE"
    flush_queue_on_activate: bool = True


@dataclass
class Device:
    dev_eui: str
    name: str
    application_id: str
    device_profile_id: str
    description: Optional[str] = None
    is_disabled: bool = False


@dataclass
class Gateway:
    gateway_id: str
    name: str
    tenant_id: str
    description: Optional[str] = None
    location: Optional[Dict[str, float]] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class DeviceKeys:
    dev_eui: str
    nwk_key: str
    app_key: str


@dataclass
class MulticastGroup:
    id: str
    name: str
    application_id: str
    mc_addr: str
    mc_nwk_s_key: str
    mc_app_s_key: str
    f_cnt: int
    group_type: str
