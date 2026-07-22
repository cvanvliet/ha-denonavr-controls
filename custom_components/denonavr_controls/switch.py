"""Switch entities for Denon AVR Controls."""

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import DenonControlsConfigEntry
from .entity import DenonControlsEntity


async def async_setup_entry(
    hass,
    entry: DenonControlsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up switch controls."""
    async_add_entities([DynamicEqSwitch(entry.runtime_data)])


class DynamicEqSwitch(DenonControlsEntity, SwitchEntity):
    """Control Audyssey Dynamic EQ."""

    _attr_translation_key = "dynamic_eq"

    def __init__(self, coordinator) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, "dynamic_eq")

    @property
    def is_on(self) -> bool | None:
        """Return whether Dynamic EQ is enabled."""
        return self.coordinator.receiver.audyssey.dynamic_eq

    async def async_turn_on(self, **kwargs) -> None:
        """Enable Dynamic EQ."""
        await self.coordinator.async_run_command(
            self.coordinator.receiver.audyssey.async_dynamiceq_on
        )

    async def async_turn_off(self, **kwargs) -> None:
        """Disable Dynamic EQ."""
        await self.coordinator.async_run_command(
            self.coordinator.receiver.audyssey.async_dynamiceq_off
        )
