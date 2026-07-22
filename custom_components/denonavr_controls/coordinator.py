"""Data coordinator for Denon AVR Controls."""

import asyncio
from collections.abc import Awaitable, Callable
import logging

from denonavr import DenonAVR
from denonavr.exceptions import DenonAvrError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.httpx_client import get_async_client
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DEFAULT_POWER_OFF_DELAY,
    DEFAULT_POWER_ON_DELAY,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class DenonControlsCoordinator(DataUpdateCoordinator[None]):
    """Coordinate receiver updates and serialize commands."""

    def __init__(self, hass: HomeAssistant, host: str) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=DEFAULT_SCAN_INTERVAL,
        )
        self.receiver = DenonAVR(host=host, timeout=5)
        self.receiver.set_async_client_getter(lambda: get_async_client(hass))
        self.command_lock = asyncio.Lock()

    async def async_setup(self) -> None:
        """Connect to and initialize the receiver."""
        await self.receiver.async_setup()

    async def _async_update_data(self) -> None:
        """Read current receiver and Audyssey settings."""
        try:
            async with self.command_lock:
                await self.receiver.async_update()
                await self.receiver.async_update_audyssey()
        except DenonAvrError as err:
            raise UpdateFailed(f"Unable to update receiver: {err}") from err

    async def async_run_command(self, command: Callable[[], Awaitable[None]]) -> None:
        """Run one command at a time and refresh the receiver afterward."""
        async with self.command_lock:
            await command()
            await self.receiver.async_update_audyssey()
        self.async_set_updated_data(None)

    async def async_recover_audio(self) -> None:
        """Power cycle the receiver and restore its selected input."""
        async with self.command_lock:
            await self.receiver.async_update()
            previous_input = self.receiver.input_func
            await self.receiver.async_power_off()
            await asyncio.sleep(DEFAULT_POWER_OFF_DELAY)
            await self.receiver.async_power_on()
            await asyncio.sleep(DEFAULT_POWER_ON_DELAY)
            await self.receiver.async_update()
            if previous_input in self.receiver.input_func_list:
                await self.receiver.async_set_input_func(previous_input)
            await self.receiver.async_update_audyssey()
        self.async_set_updated_data(None)


def coordinator_from_entry(
    hass: HomeAssistant, entry: ConfigEntry
) -> DenonControlsCoordinator:
    """Create a coordinator from a config entry."""
    return DenonControlsCoordinator(hass, entry.data[CONF_HOST])
