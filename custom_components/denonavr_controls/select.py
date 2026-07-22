"""Select entities for Denon AVR Controls."""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from homeassistant.components.select import SelectEntity
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import DenonControlsConfigEntry
from .entity import DenonControlsEntity


@dataclass(frozen=True, kw_only=True)
class AudysseySelectDescription:
    """Describe an Audyssey select."""

    key: str
    translation_key: str
    value_fn: Callable
    options_fn: Callable
    set_fn: Callable[[str], Awaitable[None]]


async def async_setup_entry(
    hass,
    entry: DenonControlsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Audyssey select controls."""
    coordinator = entry.runtime_data
    audyssey = coordinator.receiver.audyssey
    descriptions = (
        AudysseySelectDescription(
            key="dynamic_volume",
            translation_key="dynamic_volume",
            value_fn=lambda: audyssey.dynamic_volume,
            options_fn=lambda: audyssey.dynamic_volume_setting_list,
            set_fn=audyssey.async_set_dynamicvol,
        ),
        AudysseySelectDescription(
            key="reference_level_offset",
            translation_key="reference_level_offset",
            value_fn=lambda: audyssey.reference_level_offset,
            options_fn=lambda: audyssey.reference_level_offset_setting_list,
            set_fn=audyssey.async_set_reflevoffset,
        ),
        AudysseySelectDescription(
            key="multi_eq",
            translation_key="multi_eq",
            value_fn=lambda: audyssey.multi_eq,
            options_fn=lambda: audyssey.multi_eq_setting_list,
            set_fn=audyssey.async_set_multieq,
        ),
    )
    async_add_entities(
        AudysseySelect(coordinator, description) for description in descriptions
    )


class AudysseySelect(DenonControlsEntity, SelectEntity):
    """Represent an Audyssey setting."""

    def __init__(self, coordinator, description: AudysseySelectDescription) -> None:
        """Initialize an Audyssey select."""
        super().__init__(coordinator, description.key)
        self.entity_description = description
        self._attr_translation_key = description.translation_key

    @property
    def current_option(self) -> str | None:
        """Return the current setting."""
        return self.entity_description.value_fn()

    @property
    def options(self) -> list[str]:
        """Return available settings."""
        return self.entity_description.options_fn()

    async def async_select_option(self, option: str) -> None:
        """Change the setting."""
        if self.entity_description.key == "reference_level_offset":
            await self.coordinator.async_request_refresh()
        await self.coordinator.async_run_command(
            lambda: self.entity_description.set_fn(option)
        )
