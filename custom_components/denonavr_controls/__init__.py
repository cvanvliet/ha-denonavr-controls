"""The Denon AVR Controls integration."""

from denonavr.exceptions import DenonAvrError

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import PLATFORMS
from .coordinator import DenonControlsCoordinator, coordinator_from_entry

type DenonControlsConfigEntry = ConfigEntry[DenonControlsCoordinator]


async def async_setup_entry(
    hass: HomeAssistant, entry: DenonControlsConfigEntry
) -> bool:
    """Set up Denon AVR Controls from a config entry."""
    coordinator = coordinator_from_entry(hass, entry)
    try:
        await coordinator.async_setup()
    except DenonAvrError as err:
        raise ConfigEntryNotReady from err
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    await coordinator.async_config_entry_first_refresh()
    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: DenonControlsConfigEntry
) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
