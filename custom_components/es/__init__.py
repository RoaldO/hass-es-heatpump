# <config_dir>/custom_components/es/__init__.py
from __future__ import annotations
import logging
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import HeatPumpCloudAPI
from . import const

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up heatpump cloud from a config entry."""
    _LOGGER.debug('async_setup_entry')
    api = HeatPumpCloudAPI(
        entry.data["username"],
        entry.data["password"],
        entry.data["api_url"]
    )
    _LOGGER.debug(f'async_setup_entry:{api=}')

    # Verify authentication works during setup
    try:
        await api.authenticate()
    except Exception as err:
        _LOGGER.error("Initial authentication failed: %s", err)
        return False

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="heatpump",
        update_method=api.async_get_status,
        update_interval=timedelta(seconds=30),
    )
    _LOGGER.debug(f'async_setup_entry:{coordinator=}')

    await coordinator.async_config_entry_first_refresh()
    _LOGGER.debug(f'async_setup_entry:async_config_entry_first_refresh()')

    hass.data.setdefault(const.DOMAIN, {})
    _LOGGER.debug('async_setup_entry:hass.data.setdefault(DOMAIN, {})')
    hass.data[const.DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "api": api
    }
    _LOGGER.debug('async_setup_entry:hass.data[DOMAIN][entry.entry_id] = coordinator')

    await hass.config_entries.async_forward_entry_setups(entry, const.PLATFORMS)
    _LOGGER.debug('hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)')
    return True