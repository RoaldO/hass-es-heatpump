"""
ES Heatpump integration, implemented using http calls to myheatpump.com.
"""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger("es")
_LOGGER.debug("initialization started")

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the ES Heat Pump from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data
    return True

_LOGGER.debug("initialization done")
