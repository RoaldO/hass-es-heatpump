"""
ES Heatpump integration, implemented using http calls to myheatpump.com.
"""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .climate import HeatPumpEntity
from .const import DOMAIN
from . import climate

_LOGGER = logging.getLogger(__name__)
_LOGGER.debug("initialization started")

# async def async_setup(hass: HomeAssistant, entry: ConfigEntry):
#     """Set up the ES Heat Pump from a config entry."""
#     _LOGGER.debug("async_setup()")
#     hass.data.setdefault(DOMAIN, {})
#     _LOGGER.debug(f"{entry=}")
#
#     """
#         2025-03-27 20:41:01.142 ERROR (MainThread) [homeassistant.setup] Error during setup of component es: 'NodeDictClass' object has no attribute 'data'
#     Traceback (most recent call last):
#       File "/usr/src/homeassistant/homeassistant/setup.py", line 422, in _async_setup_component
#         result = await task
#                  ^^^^^^^^^^
#       File "/config/custom_components/es/__init__.py", line 18, in async_setup
#         hass.data[DOMAIN][entry.entry_id] = entry.data
#                                             ^^^^^^^^^^
#     AttributeError: 'NodeDictClass' object has no attribute 'data'
#     """
#     # hass.data[DOMAIN][entry.entry_id] = entry.data
#     _LOGGER.debug("async_setup():RETURN")
#     return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the ES Heat Pump from a config entry."""
    _LOGGER.debug("async_setup_entry()")
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    name = hass.data[const.DOMAIN][entry.entry_id][const.CONF_NAME]
    # url = hass.data[const.DOMAIN][entry.entry_id][const.CONF_URL]
    # api_key = hass.data[const.DOMAIN][entry.entry_id][const.CONF_API_KEY]
    # username = hass.data[const.DOMAIN][entry.entry_id][const.CONF_USERNAME]
    password = hass.data[const.DOMAIN][entry.entry_id][const.CONF_PASSWORD]
    # min_temp = hass.data[const.DOMAIN][entry.entry_id][const.CONF_MIN_TEMP]
    # max_temp = hass.data[const.DOMAIN][entry.entry_id][const.CONF_MAX_TEMP]

    climate_entity = HeatPumpEntity(name, "my-url", "my-api_key", "my-username", password) #, min_temp, max_temp)

    _LOGGER.debug("async_setup_entry():RETURN")
    return True


_LOGGER.debug("initialization done")
