"""Config flow for Denon AVR Controls."""

from typing import Any

from denonavr import DenonAVR
from denonavr.exceptions import DenonAvrError
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST
from homeassistant.helpers.httpx_client import get_async_client

from .const import DOMAIN


class DenonControlsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle configuration for Denon AVR Controls."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Configure a receiver by address."""
        errors: dict[str, str] = {}
        if user_input is not None:
            host = user_input[CONF_HOST].strip()
            receiver = DenonAVR(host=host, timeout=5)
            receiver.set_async_client_getter(lambda: get_async_client(self.hass))
            try:
                await receiver.async_setup()
                await receiver.async_update()
            except DenonAvrError:
                errors["base"] = "cannot_connect"
            else:
                unique_id = receiver.serial_number or host
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured(updates={CONF_HOST: host})
                return self.async_create_entry(
                    title=receiver.name or f"Denon AVR ({host})",
                    data={CONF_HOST: host},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_HOST): str}),
            errors=errors,
        )
