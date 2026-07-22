"""Constants for Denon AVR Controls."""

from datetime import timedelta

from homeassistant.const import Platform

DOMAIN = "denonavr_controls"
PLATFORMS = [Platform.BUTTON, Platform.SELECT, Platform.SWITCH]

DEFAULT_POWER_OFF_DELAY = 5
DEFAULT_POWER_ON_DELAY = 12
DEFAULT_SCAN_INTERVAL = timedelta(seconds=30)
