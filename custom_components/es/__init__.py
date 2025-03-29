"""
ES Heatpump integration, implemented using http calls to myheatpump.com.
"""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .climate import HeatPumpEntity
from . import const
from . import climate

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the ES Heat Pump from a config entry."""
    _LOGGER.debug("async_setup_entry()")
    hass.data.setdefault(const.DOMAIN, {})
    hass.data[const.DOMAIN][entry.entry_id] = entry.data

    name = hass.data[const.DOMAIN][entry.entry_id][const.CONF_NAME]
    url = hass.data[const.DOMAIN][entry.entry_id][const.CONF_URL]
    username = hass.data[const.DOMAIN][entry.entry_id][const.CONF_USERNAME]
    password = hass.data[const.DOMAIN][entry.entry_id][const.CONF_PASSWORD]

    climate_entity = HeatPumpEntity(name, url, username, password)

    return True
