# <config_dir>/custom_components/heatpump_cloud/climate.py (updated)
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    HVAC_MODE_HEAT,
    HVAC_MODE_COOL,
    HVAC_MODE_OFF,
    SUPPORT_TARGET_TEMPERATURE,
)
from homeassistant.const import TEMP_CELSIUS, ATTR_TEMPERATURE

from .const import DOMAIN

SUPPORTED_MODES = [HVAC_MODE_HEAT, HVAC_MODE_COOL, HVAC_MODE_OFF]


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup climate platform with API instance"""
    data = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([HeatPumpClimate(data["coordinator"], data["api"])])


class HeatPumpClimate(ClimateEntity):
    """Climate entity with cookie-based API"""

    def __init__(self, coordinator, api):
        self.coordinator = coordinator
        self._api = api
        self._attr_name = "Heat Pump"
        self._attr_temperature_unit = TEMP_CELSIUS
        self._attr_supported_features = SUPPORT_TARGET_TEMPERATURE
        self._attr_hvac_modes = SUPPORTED_MODES

    @property
    def current_temperature(self):
        return self.coordinator.data.get("current_temp")

    @property
    def target_temperature(self):
        return self.coordinator.data.get("target_temp")

    @property
    def hvac_mode(self):
        return self.coordinator.data.get("mode")

    async def async_set_temperature(self, **kwargs):
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is not None:
            await self._api.async_set_temperature(temperature)
            await self.coordinator.async_request_refresh()

    async def async_set_hvac_mode(self, hvac_mode):
        await self._api.async_set_mode(hvac_mode)
        await self.coordinator.async_request_refresh()