from Crypto.Cipher import AES
from google.protobuf import duration_pb2

from ...proto.fuota import fuota_pb2


class FuotaUtils:
    @staticmethod
    def get_multicast_group_type(group_type):
        if group_type.upper() == "CLASS_B":
            return fuota_pb2.MulticastGroupType.CLASS_B
        elif group_type.upper() == "CLASS_C":
            return fuota_pb2.MulticastGroupType.CLASS_C
        else:
            raise ValueError("Invalid multicast group type. Must be 'CLASS_B' or 'CLASS_C'")

    @staticmethod
    def create_duration(seconds):
        return duration_pb2.Duration(seconds=seconds)

    @staticmethod
    def get_request_fragmentation_session_status(status):
        status_map = {
            "AFTER_FRAGMENT_ENQUEUE": fuota_pb2.RequestFragmentationSessionStatus.AFTER_FRAGMENT_ENQUEUE,
            "AFTER_SESSION_TIMEOUT": fuota_pb2.RequestFragmentationSessionStatus.AFTER_SESSION_TIMEOUT,
            "NO_REQUEST": fuota_pb2.RequestFragmentationSessionStatus.NO_REQUEST,
        }
        return status_map.get(status.upper(), fuota_pb2.RequestFragmentationSessionStatus.NO_REQUEST)

    @staticmethod
    def get_region(region_str):
        region_map = {
            "EU868": fuota_pb2.Region.EU868,
            "US915": fuota_pb2.Region.US915,
            "CN779": fuota_pb2.Region.CN779,
            "EU433": fuota_pb2.Region.EU433,
            "AU915": fuota_pb2.Region.AU915,
            "CN470": fuota_pb2.Region.CN470,
            "AS923": fuota_pb2.Region.AS923,
            "AS923_2": fuota_pb2.Region.AS923_2,
            "AS923_3": fuota_pb2.Region.AS923_3,
            "AS923_4": fuota_pb2.Region.AS923_4,
            "KR920": fuota_pb2.Region.KR920,
            "IN865": fuota_pb2.Region.IN865,
            "RU864": fuota_pb2.Region.RU864,
            "ISM2400": fuota_pb2.Region.ISM2400,
        }
        return region_map.get(region_str.upper(), fuota_pb2.Region.EU868)

    @staticmethod
    def create_deployment_config(**kwargs):
        return {
            "multicast_timeout": kwargs.get("multicast_timeout", 6),
            "multicast_ping_slot_period": kwargs.get("multicast_ping_slot_period", 1),
            "unicast_timeout": kwargs.get("unicast_timeout", 60),
            "unicast_attempt_count": kwargs.get("unicast_attempt_count", 1),
            "fragmentation_fragment_size": kwargs.get("fragmentation_fragment_size", 50),
            "fragmentation_redundancy": kwargs.get("fragmentation_redundancy", 1),
            "fragmentation_session_index": kwargs.get("fragmentation_session_index", 0),
            "fragmentation_matrix": kwargs.get("fragmentation_matrix", 0),
            "fragmentation_block_ack_delay": kwargs.get("fragmentation_block_ack_delay", 1),
            "fragmentation_descriptor": kwargs.get("fragmentation_descriptor", b"\x00\x00\x00\x00"),
        }

    @staticmethod
    def get_key(key, b):
        cipher = AES.new(key, AES.MODE_ECB)
        return cipher.encrypt(b)

    @staticmethod
    def get_mc_root_key_for_gen_app_key(gen_app_key: str) -> str:
        """
        Generate McRootKey from GenAppKey using AES encryption.

        :param gen_app_key: str, 32-character hex string representing the 16-byte GenAppKey
        :return: str, 32-character hex string representing the 16-byte McRootKey
        """
        try:
            # Convert hex string to bytes
            gen_app_key_bytes = bytes.fromhex(gen_app_key)
            if len(gen_app_key_bytes) != 16:
                raise ValueError("GenAppKey must be 16 bytes (32 hex characters)")

            # Create AES cipher
            cipher = AES.new(gen_app_key_bytes, AES.MODE_ECB)

            # Encrypt 16 zero bytes
            mc_root_key_bytes = cipher.encrypt(b"\x00" * 16)

            # Convert McRootKey back to hex string
            return mc_root_key_bytes.hex()
        except ValueError as ve:
            raise ValueError(f"Invalid GenAppKey: {str(ve)}")
        except Exception as e:
            raise Exception(f"Failed to generate McRootKey: {str(e)}")

    @staticmethod
    def create_deployment_devices(devices):
        deployment_devices = []
        for device in devices:
            dev_eui = device["dev_eui"]
            gen_app_key = device["gen_app_key"]
            mc_root_key = FuotaUtils.get_mc_root_key_for_gen_app_key(gen_app_key)
            deployment_devices.append(fuota_pb2.DeploymentDevice(dev_eui=dev_eui, mc_root_key=mc_root_key))
        return deployment_devices
