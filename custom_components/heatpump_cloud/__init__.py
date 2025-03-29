# <config_dir>/custom_components/heatpump_cloud/__init__.py
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
    api = HeatPumpCloudAPI(
        entry.data["username"],
        entry.data["password"],
        entry.data["api_url"]
    )

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="heatpump",
        update_method=api.async_get_status,
        update_interval=timedelta(seconds=30),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True