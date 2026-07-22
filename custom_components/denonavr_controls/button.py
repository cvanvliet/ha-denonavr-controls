"""Button entities for Denon AVR Controls."""

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import DenonControlsConfigEntry
from .entity import DenonControlsEntity


async def async_setup_entry(
    hass,
    entry: DenonControlsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up receiver buttons."""
    coordinator = entry.runtime_data
    async_add_entities(
        [
            DenonButton(
                coordinator,
                ButtonEntityDescription(
                    key="refresh_audyssey", translation_key="refresh_audyssey"
                ),
                coordinator.async_request_refresh,
            ),
            DenonButton(
                coordinator,
                ButtonEntityDescription(
                    key="recover_audio", translation_key="recover_audio"
                ),
                coordinator.async_recover_audio,
            ),
        ]
    )


class DenonButton(DenonControlsEntity, ButtonEntity):
    """Represent a receiver command button."""

    def __init__(self, coordinator, description, press_action) -> None:
        """Initialize the button."""
        super().__init__(coordinator, description.key)
        self.entity_description = description
        self._press_action = press_action

    async def async_press(self) -> None:
        """Run the receiver command."""
        await self._press_action()
