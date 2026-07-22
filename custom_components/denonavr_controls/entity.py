"""Base entity for Denon AVR Controls."""

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import DenonControlsCoordinator


class DenonControlsEntity(CoordinatorEntity[DenonControlsCoordinator]):
    """Base class for receiver control entities."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: DenonControlsCoordinator, key: str) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        receiver = coordinator.receiver
        device_id = receiver.serial_number or receiver.host
        self._attr_unique_id = f"{device_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            configuration_url=f"http://{receiver.host}/",
            manufacturer=receiver.manufacturer,
            model=receiver.model_name,
            name=f"{receiver.name} controls",
        )
