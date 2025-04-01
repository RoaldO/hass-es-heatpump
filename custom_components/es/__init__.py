# <config_dir>/custom_components/es/__init__.py
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import HeatPumpCloudAPI
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["climate"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up heatpump cloud from a config entry."""
    _LOGGER.debug('async_setup_entry')
    api = HeatPumpCloudAPI(
        entry.data["username"],
        entry.data["password"],
        entry.data["api_url"]
    )
    _LOGGER.debug(f'async_setup_entry:{api=}')

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

    hass.data.setdefault(DOMAIN, {})
    _LOGGER.debug('async_setup_entry:hass.data.setdefault(DOMAIN, {})')
    hass.data[DOMAIN][entry.entry_id] = coordinator
    _LOGGER.debug('async_setup_entry:hass.data[DOMAIN][entry.entry_id] = coordinator')

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _LOGGER.debug('hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)')
    return True