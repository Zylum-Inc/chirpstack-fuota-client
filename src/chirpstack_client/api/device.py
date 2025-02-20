import grpc
from chirpstack_api import api

from ..utils.helpers import auth_header, create_channel


class DeviceService:
    """Service for managing LoRaWAN devices in ChirpStack.

    Provides methods for creating, retrieving, updating and deleting devices,
    as well as managing device keys, queue and state.
    """

    def __init__(self, server_address, api_token):
        """Initialize the device service.

        Args:
            server_address: ChirpStack server address
            api_token: API token for authentication
        """
        self.server_address = server_address
        self.api_token = api_token
        self.channel = create_channel(self.server_address)
        self.stub = api.DeviceServiceStub(self.channel)

    def create(self, application_id, name, dev_eui, app_key, mac_version, description="", tags=None, **kwargs):
        """Create a new device.

        Args:
            application_id: Application ID UUID string
            name: Device name
            dev_eui: Device EUI (64-bit hex string)
            app_key: App key for OTAA activation
            mac_version: LoRaWAN MAC version (e.g. "LORAWAN_1_0_3")
            description: Optional device description
            tags: Optional dict of device tags
            **kwargs: Additional device attributes

        Returns:
            The created device object

        Raises:
            Exception: If device creation fails
        """
        try:
            existing_device = self.get_by_name(application_id, name)
            if existing_device:
                return existing_device

            req = api.CreateDeviceRequest(
                device=api.Device(
                    application_id=application_id,
                    name=name,
                    dev_eui=dev_eui,
                    description=description,
                    tags={} if tags is None else tags,
                    **kwargs,
                )
            )
            device = self.stub.Create(req, metadata=auth_header(self.api_token))
            self.create_keys(dev_eui, app_key, mac_version)
            return device

        except grpc.RpcError as e:
            raise Exception(f"Failed to create device: {str(e)}")

    def get(self, dev_eui):
        """Get a device by its EUI.

        Args:
            dev_eui: Device EUI (64-bit hex string)

        Returns:
            Device object if found

        Raises:
            Exception: If retrieval fails
        """
        req = api.GetDeviceRequest(dev_eui=dev_eui)
        try:
            return self.stub.Get(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to get device: {str(e)}")

    def get_by_name(self, application_id, name):
        """Get a device by its name within an application.

        Args:
            application_id: Application ID UUID string
            name: Device name to search for

        Returns:
            Device object if found, None otherwise

        Raises:
            Exception: If search fails
        """
        req = api.ListDevicesRequest(
            limit=1,
            search=name,
            application_id=application_id,
        )
        try:
            resp = self.stub.List(req, metadata=auth_header(self.api_token))
            for device in resp.result:
                if device.name == name:
                    return device
            return None
        except grpc.RpcError as e:
            raise Exception(f"Failed to get device by name: {str(e)}")

    def update(self, dev_eui, name, app_key, mac_version, description="", tags=None, **kwargs):
        """Update an existing device.

        Args:
            dev_eui: Device EUI (64-bit hex string)
            name: New device name
            app_key: App key for OTAA activation
            mac_version: LoRaWAN MAC version
            description: Optional new description
            tags: Optional dict of tags to update
            **kwargs: Additional device attributes to update

        Raises:
            Exception: If update fails
        """
        device = self.get(dev_eui).device
        current_tags = dict(device.tags)

        if tags is not None:
            current_tags.update(tags)

        req = api.UpdateDeviceRequest(
            device=api.Device(dev_eui=dev_eui, name=name, description=description, tags=current_tags, **kwargs)
        )
        try:
            self.stub.Update(req, metadata=auth_header(self.api_token))
            self.update_keys(dev_eui, app_key, mac_version)
        except grpc.RpcError as e:
            raise Exception(f"Failed to update device: {str(e)}")

    def delete(self, dev_eui):
        """Delete a device.

        Args:
            dev_eui: Device EUI (64-bit hex string)

        Raises:
            Exception: If deletion fails
        """
        req = api.DeleteDeviceRequest(dev_eui=dev_eui)
        try:
            self.stub.Delete(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to delete device: {str(e)}")

    def list(self, application_id, limit=10, offset=0):
        """List devices in an application.

        Args:
            application_id: Application ID UUID string
            limit: Max number of devices to return
            offset: Offset in the result-set

        Returns:
            List response containing devices

        Raises:
            Exception: If listing fails
        """
        req = api.ListDevicesRequest(
            application_id=application_id,
            limit=limit,
            offset=offset,
        )
        try:
            return self.stub.List(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to list devices: {str(e)}")

    def create_keys(self, dev_eui, app_key, mac_version, **kwargs):
        """Create device keys.

        Args:
            dev_eui: Device EUI (64-bit hex string)
            app_key: App key for OTAA activation
            mac_version: LoRaWAN MAC version
            **kwargs: Additional key attributes

        Raises:
            Exception: If key creation fails
        """
        device_keys = self._DeviceKeys(dev_eui, app_key, mac_version, **kwargs)
        req = api.CreateDeviceKeysRequest(device_keys=device_keys)
        self.stub.CreateKeys(req, metadata=auth_header(self.api_token))

    def update_keys(self, dev_eui, app_key, mac_version, **kwargs):
        """Update device keys.

        Args:
            dev_eui: Device EUI (64-bit hex string)
            app_key: App key for OTAA activation
            mac_version: LoRaWAN MAC version
            **kwargs: Additional key attributes

        Raises:
            Exception: If key update fails
        """
        device_keys = self._DeviceKeys(dev_eui, app_key, mac_version, **kwargs)
        req = api.UpdateDeviceKeysRequest(device_keys=device_keys)
        self.stub.UpdateKeys(req, metadata=auth_header(self.api_token))

    def _DeviceKeys(self, dev_eui, app_key, mac_version, **kwargs):
        """Create a DeviceKeys object.

        Args:
            dev_eui: Device EUI (64-bit hex string)
            app_key: App key for OTAA activation
            mac_version: LoRaWAN MAC version
            **kwargs: Additional key attributes

        Returns:
            DeviceKeys object

        Raises:
            ValueError: If mac_version is invalid
        """
        device_keys = api.DeviceKeys(dev_eui=dev_eui, **kwargs)

        if mac_version.startswith("LORAWAN_1_0_"):
            device_keys.nwk_key = app_key
        elif mac_version.startswith("LORAWAN_1_1_"):
            device_keys.app_key = app_key
        else:
            raise ValueError("Invalid mac_version")

        return device_keys

    def queue_downlink(self, dev_eui, data, fport=10, **kwargs):
        """Queue a downlink message for a device.

        Args:
            dev_eui: Device EUI (64-bit hex string)
            data: Downlink payload data (string)
            fport: FPort to use (default: 10)
            **kwargs: Additional queue item attributes

        Returns:
            Created queue item

        Raises:
            Exception: If queueing fails
        """
        data = data.encode()
        req = api.EnqueueDeviceQueueItemRequest(
            queue_item=api.DeviceQueueItem(dev_eui=dev_eui, f_port=fport, data=data, **kwargs)
        )
        try:
            return self.stub.Enqueue(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to send downlink: {str(e)}")

    def get_queue_items(self, dev_eui):
        """Get queued items for a device.

        Args:
            dev_eui: Device EUI (64-bit hex string)

        Returns:
            List of queued items

        Raises:
            Exception: If retrieval fails
        """
        req = api.GetDeviceQueueItemsRequest(dev_eui=dev_eui)
        try:
            return self.stub.GetQueue(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to get queue items: {str(e)}")

    def flush_queue(self, dev_eui):
        """Flush the queue for a device.

        Args:
            dev_eui: Device EUI (64-bit hex string)

        Returns:
            Result of flush operation

        Raises:
            Exception: If flush fails
        """
        req = api.FlushDeviceQueueRequest(dev_eui=dev_eui)
        try:
            return self.stub.FlushQueue(req, metadata=auth_header(self.api_token))
        except grpc.RpcError as e:
            raise Exception(f"Failed to flush queue: {str(e)}")
